"""Storage Factory

Factory for creating the appropriate storage service implementation
based on environment configuration.
"""

import os
from typing import Optional

from src.framework.domain.infrastructure.storage_service_interface import (
    StorageConfig,
    StorageServiceInterface,
)
from src.framework.infrastructure.storage.local_storage_service import LocalStorageService
from src.framework.infrastructure.storage.s3_storage_service import S3StorageService


class StorageFactory:
    """Factory for creating storage service instances."""

    @staticmethod
    def create_storage_service(
            storage_type: Optional[str] = None,
            config: Optional[StorageConfig] = None
    ) -> StorageServiceInterface:
        """Create a storage service instance based on configuration.

        Args:
            storage_type: Type of storage ('local' or 's3').
                         If not provided, reads from STORAGE_TYPE env var.
            config: Storage configuration. If not provided, uses default.

        Returns:
            StorageServiceInterface implementation

        Raises:
            ValueError: If storage_type is invalid or required env vars are missing
        """
        # Get storage type from parameter or environment
        if storage_type is None:
            storage_type = os.getenv("STORAGE_TYPE", "local")
        storage_type = storage_type.lower()

        # Create config if not provided
        if config is None:
            config = StorageConfig()

        if storage_type == "local":
            return StorageFactory._create_local_storage(config)
        elif storage_type == "s3":
            return StorageFactory._create_s3_storage(config)
        else:
            raise ValueError(
                f"Invalid storage type: {storage_type}. "
                f"Must be 'local' or 's3'"
            )

    @staticmethod
    def _create_local_storage(config: StorageConfig) -> LocalStorageService:
        """Create a local storage service instance.

        Args:
            config: Storage configuration

        Returns:
            LocalStorageService instance
        """
        base_path = os.getenv("LOCAL_STORAGE_PATH", "uploads")
        base_url = os.getenv(
            "LOCAL_STORAGE_URL",
            "http://localhost:8000/uploads"
        )

        return LocalStorageService(
            base_path=base_path,
            base_url=base_url,
            config=config
        )

    @staticmethod
    def _create_s3_storage(config: StorageConfig) -> S3StorageService:
        """Create an S3 storage service instance.

        Args:
            config: Storage configuration

        Returns:
            S3StorageService instance

        Raises:
            ValueError: If required S3 environment variables are missing
        """
        bucket_name = os.getenv("AWS_S3_BUCKET")
        if not bucket_name:
            raise ValueError(
                "AWS_S3_BUCKET environment variable is required for S3 storage"
            )

        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region_name = os.getenv("AWS_REGION", "us-east-1")

        return S3StorageService(
            bucket_name=bucket_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
            config=config
        )


# Convenience function for quick access
def get_storage_service(
        storage_type: Optional[str] = None,
        config: Optional[StorageConfig] = None
) -> StorageServiceInterface:
    """Get a storage service instance.

    This is a convenience function that wraps StorageFactory.create_storage_service.

    Args:
        storage_type: Type of storage ('local' or 's3')
        config: Storage configuration

    Returns:
        StorageServiceInterface implementation
    """
    return StorageFactory.create_storage_service(storage_type, config)
