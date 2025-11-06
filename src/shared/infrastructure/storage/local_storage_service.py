"""Local File System Storage Service Implementation

This implementation stores files in the local filesystem.
Suitable for development and testing environments.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

from src.shared.domain.infrastructure.storage_service_interface import (
    StorageConfig,
    StorageServiceInterface,
    StorageType,
    UploadedFile,
)


class LocalStorageService(StorageServiceInterface):
    """Local filesystem implementation of StorageServiceInterface."""

    def __init__(
            self,
            base_path: str = "uploads",
            base_url: str = "http://localhost:8000/uploads",
            config: Optional[StorageConfig] = None
    ):
        """Initialize local storage service.

        Args:
            base_path: Base directory for file storage (relative or absolute)
            base_url: Base URL for accessing files
            config: Storage configuration
        """
        self.base_path = Path(base_path)
        self.base_url = base_url.rstrip('/')
        self.config = config or StorageConfig()

        # Create base directory if it doesn't exist
        self.base_path.mkdir(parents=True, exist_ok=True)

    def upload_file(
            self,
            file_content: bytes,
            filename: str,
            content_type: str,
            storage_type: StorageType,
            entity_id: str,
            company_id: str,
    ) -> UploadedFile:
        """Upload a file to local filesystem.

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

        # Generate file path
        file_path = self.generate_file_path(
            storage_type=storage_type,
            company_id=company_id,
            entity_id=entity_id,
            filename=filename
        )

        # Create full path
        full_path = self.base_path / file_path

        # Create directory structure if needed
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        try:
            with open(full_path, 'wb') as f:
                f.write(file_content)
        except Exception as e:
            raise Exception(f"Failed to write file to {full_path}: {str(e)}")

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
        """Get the public URL for a file.

        Args:
            file_path: The storage path of the file

        Returns:
            Public URL to access the file
        """
        # Remove leading slash if present
        clean_path = file_path.lstrip('/')
        return f"{self.base_url}/{clean_path}"

    def delete_file(self, file_path: str) -> bool:
        """Delete a file from local filesystem.

        Args:
            file_path: The storage path of the file

        Returns:
            True if deleted successfully, False otherwise
        """
        full_path = self.base_path / file_path

        try:
            if full_path.exists() and full_path.is_file():
                full_path.unlink()
                return True
            return False
        except Exception:
            return False

    def file_exists(self, file_path: str) -> bool:
        """Check if a file exists in local filesystem.

        Args:
            file_path: The storage path of the file

        Returns:
            True if file exists, False otherwise
        """
        full_path = self.base_path / file_path
        return full_path.exists() and full_path.is_file()

    def get_file_size(self, file_path: str) -> int:
        """Get the size of a file in bytes.

        Args:
            file_path: The storage path of the file

        Returns:
            File size in bytes

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        full_path = self.base_path / file_path

        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        return full_path.stat().st_size

    def get_absolute_path(self, file_path: str) -> Path:
        """Get the absolute filesystem path for a file.

        Args:
            file_path: The storage path of the file

        Returns:
            Absolute Path object
        """
        return (self.base_path / file_path).resolve()
