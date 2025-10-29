"""Storage Service Interface - Domain Layer

This interface defines the contract for file storage operations.
Implementations can be local filesystem, S3, or any other storage backend.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class StorageType(str, Enum):
    """Types of files that can be stored."""
    CANDIDATE_RESUME = "candidate_resume"
    COMPANY_LOGO = "company_logo"
    COMPANY_DOCUMENT = "company_document"
    INTERVIEW_ATTACHMENT = "interview_attachment"


@dataclass
class UploadedFile:
    """Represents a successfully uploaded file."""
    file_path: str
    file_url: str
    file_size: int
    content_type: str
    uploaded_at: datetime


@dataclass
class StorageConfig:
    """Configuration for storage service."""
    max_file_size_mb: int = 10
    allowed_extensions: list[str] | None = None

    def __post_init__(self) -> None:
        if self.allowed_extensions is None:
            # Default to document extensions, but this should be overridden for specific use cases
            self.allowed_extensions = ['.pdf', '.doc', '.docx', '.txt']


class StorageServiceInterface(ABC):
    """Abstract interface for file storage operations.

    This interface ensures that the domain layer is decoupled from
    specific storage implementations (local, S3, etc.).
    """

    @abstractmethod
    def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str,
        storage_type: StorageType,
        entity_id: str,
        company_id: str,
    ) -> UploadedFile:
        """Upload a file to storage.

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
        pass

    @abstractmethod
    def get_file_url(self, file_path: str) -> str:
        """Get the public URL for a file.

        Args:
            file_path: The storage path of the file

        Returns:
            Public URL to access the file
        """
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> bool:
        """Delete a file from storage.

        Args:
            file_path: The storage path of the file

        Returns:
            True if deleted successfully, False otherwise
        """
        pass

    @abstractmethod
    def file_exists(self, file_path: str) -> bool:
        """Check if a file exists in storage.

        Args:
            file_path: The storage path of the file

        Returns:
            True if file exists, False otherwise
        """
        pass

    @abstractmethod
    def get_file_size(self, file_path: str) -> int:
        """Get the size of a file in bytes.

        Args:
            file_path: The storage path of the file

        Returns:
            File size in bytes

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        pass

    def validate_file(
        self,
        filename: str,
        file_size: int,
        config: Optional[StorageConfig] = None
    ) -> None:
        """Validate file before upload.

        Args:
            filename: The filename to validate
            file_size: Size of the file in bytes
            config: Storage configuration (uses default if not provided)

        Raises:
            ValueError: If validation fails
        """
        if config is None:
            config = StorageConfig()

        # Check file extension
        file_ext = '.' + filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        assert config.allowed_extensions is not None, "allowed_extensions should be set in __post_init__"
        if file_ext not in config.allowed_extensions:
            raise ValueError(
                f"File extension {file_ext} not allowed. "
                f"Allowed: {', '.join(config.allowed_extensions)}"
            )

        # Check file size
        max_size_bytes = config.max_file_size_mb * 1024 * 1024
        if file_size > max_size_bytes:
            raise ValueError(
                f"File size {file_size / 1024 / 1024:.2f}MB exceeds "
                f"maximum allowed {config.max_file_size_mb}MB"
            )

    def generate_file_path(
        self,
        storage_type: StorageType,
        company_id: str,
        entity_id: str,
        filename: str
    ) -> str:
        """Generate a consistent file path for storage.

        Args:
            storage_type: Type of file being stored
            company_id: ID of the company
            entity_id: ID of the entity
            filename: Original filename

        Returns:
            Generated file path
        """
        # Sanitize filename
        safe_filename = filename.replace(' ', '_').replace('/', '_')

        # Generate path based on storage type
        if storage_type == StorageType.CANDIDATE_RESUME:
            return f"company/{company_id}/candidates/{entity_id}/resume/{safe_filename}"
        elif storage_type == StorageType.COMPANY_LOGO:
            return f"company/{company_id}/logo/{safe_filename}"
        elif storage_type == StorageType.COMPANY_DOCUMENT:
            return f"company/{company_id}/documents/{safe_filename}"
        elif storage_type == StorageType.INTERVIEW_ATTACHMENT:
            return f"company/{company_id}/interviews/{entity_id}/{safe_filename}"

        # All enum values are covered above
        raise ValueError(f"Unknown storage type: {storage_type}")
