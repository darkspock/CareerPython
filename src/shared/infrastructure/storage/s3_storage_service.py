"""AWS S3 Storage Service Implementation

This implementation stores files in Amazon S3.
Suitable for production environments.
"""

import os
from datetime import datetime
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from src.shared.domain.infrastructure.storage_service_interface import (
    StorageConfig,
    StorageServiceInterface,
    StorageType,
    UploadedFile,
)


class S3StorageService(StorageServiceInterface):
    """AWS S3 implementation of StorageServiceInterface."""

    def __init__(
        self,
        bucket_name: str,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        region_name: str = "us-east-1",
        config: Optional[StorageConfig] = None
    ):
        """Initialize S3 storage service.

        Args:
            bucket_name: Name of the S3 bucket
            aws_access_key_id: AWS access key (optional, can use env vars)
            aws_secret_access_key: AWS secret key (optional, can use env vars)
            region_name: AWS region
            config: Storage configuration
        """
        self.bucket_name = bucket_name
        self.region_name = region_name
        self.config = config or StorageConfig()

        # Create S3 client
        session_kwargs = {
            'region_name': region_name
        }

        if aws_access_key_id and aws_secret_access_key:
            session_kwargs['aws_access_key_id'] = aws_access_key_id
            session_kwargs['aws_secret_access_key'] = aws_secret_access_key

        self.s3_client = boto3.client('s3', **session_kwargs)

        # Verify bucket exists
        self._verify_bucket()

    def _verify_bucket(self) -> None:
        """Verify that the S3 bucket exists and is accessible.

        Raises:
            Exception: If bucket doesn't exist or isn't accessible
        """
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                raise Exception(f"S3 bucket '{self.bucket_name}' not found")
            elif error_code == '403':
                raise Exception(f"Access denied to S3 bucket '{self.bucket_name}'")
            else:
                raise Exception(f"Error accessing S3 bucket: {str(e)}")

    def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str,
        storage_type: StorageType,
        entity_id: str,
        company_id: str,
    ) -> UploadedFile:
        """Upload a file to S3.

        Args:
            file_content: The binary content of the file
            filename: Original filename with extension
            content_type: MIME type (e.g., 'application/pdf')
            storage_type: Type of file being stored
            entity_id: ID of the entity (candidate_id, position_id, etc.)
            company_id: ID of the company

        Returns:
            UploadedFile with file_path and file_url

        Raises:
            ValueError: If file validation fails
            Exception: If upload fails
        """
        # Validate file
        file_size = len(file_content)
        self.validate_file(filename, file_size, self.config)

        # Generate file path (S3 key)
        file_path = self.generate_file_path(
            storage_type=storage_type,
            company_id=company_id,
            entity_id=entity_id,
            filename=filename
        )

        # Upload to S3
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_path,
                Body=file_content,
                ContentType=content_type,
                Metadata={
                    'company_id': company_id,
                    'entity_id': entity_id,
                    'storage_type': storage_type.value,
                    'original_filename': filename
                }
            )
        except ClientError as e:
            raise Exception(f"Failed to upload file to S3: {str(e)}")

        # Generate URL
        file_url = self.get_file_url(file_path)

        return UploadedFile(
            file_path=file_path,
            file_url=file_url,
            file_size=file_size,
            content_type=content_type,
            uploaded_at=datetime.utcnow()
        )

    def get_file_url(self, file_path: str) -> str:
        """Get the public URL for a file in S3.

        Args:
            file_path: The S3 key of the file

        Returns:
            Public URL to access the file (CloudFront or S3 URL)
        """
        # Generate S3 URL
        # In production, you might want to use CloudFront instead
        return f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{file_path}"

    def get_presigned_url(
        self,
        file_path: str,
        expiration: int = 3600
    ) -> str:
        """Generate a presigned URL for temporary access to a file.

        Args:
            file_path: The S3 key of the file
            expiration: URL expiration time in seconds (default 1 hour)

        Returns:
            Presigned URL for temporary access
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': file_path
                },
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            raise Exception(f"Failed to generate presigned URL: {str(e)}")

    def delete_file(self, file_path: str) -> bool:
        """Delete a file from S3.

        Args:
            file_path: The S3 key of the file

        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            return True
        except ClientError:
            return False

    def file_exists(self, file_path: str) -> bool:
        """Check if a file exists in S3.

        Args:
            file_path: The S3 key of the file

        Returns:
            True if file exists, False otherwise
        """
        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            return True
        except ClientError:
            return False

    def get_file_size(self, file_path: str) -> int:
        """Get the size of a file in S3.

        Args:
            file_path: The S3 key of the file

        Returns:
            File size in bytes

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            return response['ContentLength']
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                raise FileNotFoundError(f"File not found in S3: {file_path}")
            raise Exception(f"Error getting file size from S3: {str(e)}")

    def list_files(self, prefix: str) -> list[str]:
        """List all files with a given prefix in S3.

        Args:
            prefix: The prefix to filter files (e.g., "company/123/")

        Returns:
            List of file keys (paths)
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )

            if 'Contents' not in response:
                return []

            return [obj['Key'] for obj in response['Contents']]
        except ClientError as e:
            raise Exception(f"Error listing files from S3: {str(e)}")
