# Storage Service Usage Guide

This guide explains how to use the storage abstraction service for file uploads in CareerPython.

## Overview

The storage service provides a unified interface for file storage that works with both local filesystem (development) and AWS S3 (production). The implementation is automatically selected based on the `STORAGE_TYPE` environment variable.

## Architecture

```
StorageServiceInterface (Domain Layer)
    ↓
StorageFactory
    ↓
LocalStorageService or S3StorageService (Infrastructure Layer)
```

## Configuration

### Environment Variables

Add to your `.env` file:

```bash
# Storage type: "local" for development, "s3" for production
STORAGE_TYPE=local

# Local Storage Settings (for development)
LOCAL_STORAGE_PATH=uploads
LOCAL_STORAGE_URL=http://localhost:8000/uploads

# AWS S3 Storage Settings (for production)
AWS_S3_BUCKET=your-bucket-name
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1

# Storage Limits
MAX_FILE_SIZE_MB=10
ALLOWED_FILE_EXTENSIONS=.pdf,.doc,.docx,.txt
```

### Switching Between Local and S3

Simply change the `STORAGE_TYPE` environment variable:

- **Development**: `STORAGE_TYPE=local`
- **Production**: `STORAGE_TYPE=s3`

## Usage in Command Handlers

The storage service is automatically injected through the dependency injection container.

### Example: Upload Resume Command Handler

```python
from src.framework.domain.infrastructure.storage_service_interface import (
    StorageServiceInterface,
    StorageType,
    UploadedFile
)

class UploadCandidateResumeCommandHandler:
    def __init__(
        self,
        storage_service: StorageServiceInterface,
        repository: CompanyCandidateRepositoryInterface
    ):
        self.storage_service = storage_service
        self.repository = repository

    def execute(self, command: UploadCandidateResumeCommand) -> None:
        # Upload file
        uploaded_file: UploadedFile = self.storage_service.upload_file(
            file_content=command.file_content,
            filename=command.filename,
            content_type=command.content_type,
            storage_type=StorageType.CANDIDATE_RESUME,
            entity_id=str(command.candidate_id),
            company_id=str(command.company_id),
        )

        # Update entity with file URL
        candidate = self.repository.get_by_id(command.candidate_id)
        candidate.update_resume(
            resume_url=uploaded_file.file_url,
            uploaded_by=command.uploaded_by
        )
        self.repository.save(candidate)
```

### Example: Delete File

```python
# Delete a file
success = self.storage_service.delete_file(file_path)

if success:
    print("File deleted successfully")
else:
    print("File not found or could not be deleted")
```

### Example: Check if File Exists

```python
if self.storage_service.file_exists(file_path):
    print("File exists")
else:
    print("File not found")
```

### Example: Get File URL

```python
# Get public URL for a file
file_url = self.storage_service.get_file_url(file_path)
```

## Storage Types

The service supports different types of files with automatic path generation:

```python
class StorageType(str, Enum):
    CANDIDATE_RESUME = "candidate_resume"
    COMPANY_LOGO = "company_logo"
    COMPANY_DOCUMENT = "company_document"
    INTERVIEW_ATTACHMENT = "interview_attachment"
```

### Generated Paths

Based on storage type, files are organized as follows:

- **CANDIDATE_RESUME**: `company/{company_id}/candidates/{candidate_id}/resume/{filename}`
- **COMPANY_LOGO**: `company/{company_id}/logo/{filename}`
- **COMPANY_DOCUMENT**: `company/{company_id}/documents/{filename}`
- **INTERVIEW_ATTACHMENT**: `company/{company_id}/interviews/{interview_id}/{filename}`

## File Validation

The service automatically validates files before upload:

- **File size**: Checks against `MAX_FILE_SIZE_MB`
- **File extension**: Validates against `ALLOWED_FILE_EXTENSIONS`

Validation errors raise `ValueError` with descriptive messages.

## Return Value

Upload operations return an `UploadedFile` object:

```python
@dataclass
class UploadedFile:
    file_path: str          # Storage path (for database)
    file_url: str           # Public URL (for frontend)
    file_size: int          # Size in bytes
    content_type: str       # MIME type
    uploaded_at: datetime   # Upload timestamp
```

## Error Handling

```python
try:
    uploaded_file = self.storage_service.upload_file(...)
except ValueError as e:
    # Validation error (file too large, wrong extension)
    raise DomainException(f"Invalid file: {str(e)}")
except Exception as e:
    # Upload error
    raise InfrastructureException(f"Failed to upload file: {str(e)}")
```

## Local Storage (Development)

### Directory Structure

```
uploads/
└── company/
    └── {company_id}/
        └── candidates/
            └── {candidate_id}/
                └── resume/
                    └── john_doe_resume.pdf
```

### Accessing Files

Files are served at: `http://localhost:8000/uploads/{file_path}`

**Note**: You need to configure FastAPI to serve static files from the `uploads` directory.

## S3 Storage (Production)

### Bucket Structure

Same directory structure as local storage, but stored in S3:

```
s3://your-bucket/
└── company/
    └── {company_id}/
        └── candidates/
            └── {candidate_id}/
                └── resume/
                    └── john_doe_resume.pdf
```

### Accessing Files

Files are accessible via S3 URLs:
- Direct S3: `https://{bucket}.s3.{region}.amazonaws.com/{file_path}`
- CloudFront (if configured): `https://{cloudfront_domain}/{file_path}`

### S3 Presigned URLs

For temporary access to private files:

```python
# Only available in S3StorageService
from src.framework.infrastructure.storage.s3_storage_service import S3StorageService

if isinstance(self.storage_service, S3StorageService):
    presigned_url = self.storage_service.get_presigned_url(
        file_path=file_path,
        expiration=3600  # 1 hour
    )
```

## Registering in Container

The storage service is already registered in `core/container.py`:

```python
# Storage service - automatically selects Local or S3 based on settings
@staticmethod
def _get_storage_service():
    from src.framework.domain.infrastructure.storage_service_interface import StorageConfig

    allowed_extensions = [ext.strip() for ext in settings.ALLOWED_FILE_EXTENSIONS.split(',')]
    config = StorageConfig(
        max_file_size_mb=settings.MAX_FILE_SIZE_MB,
        allowed_extensions=allowed_extensions
    )

    return StorageFactory.create_storage_service(
        storage_type=settings.STORAGE_TYPE,
        config=config
    )

storage_service = providers.Singleton(_get_storage_service)
```

## Using in Command Handlers

To use storage service in a command handler, inject it via constructor:

```python
# In core/container.py
upload_candidate_resume_command_handler = providers.Factory(
    UploadCandidateResumeCommandHandler,
    storage_service=storage_service,  # Inject here
    repository=company_candidate_repository
)
```

## Testing

### Unit Tests

Mock the storage service interface:

```python
from unittest.mock import Mock

def test_upload_resume():
    # Mock storage service
    mock_storage = Mock(spec=StorageServiceInterface)
    mock_storage.upload_file.return_value = UploadedFile(
        file_path="company/123/candidates/456/resume/test.pdf",
        file_url="http://localhost:8000/uploads/...",
        file_size=1024,
        content_type="application/pdf",
        uploaded_at=datetime.utcnow()
    )

    # Test handler
    handler = UploadCandidateResumeCommandHandler(
        storage_service=mock_storage,
        repository=mock_repository
    )

    handler.handle(command)

    mock_storage.upload_file.assert_called_once()
```

### Integration Tests

Use local storage for integration tests:

```python
# In test environment
STORAGE_TYPE=local
LOCAL_STORAGE_PATH=test_uploads
```

## Best Practices

1. **Always store file_path in database** (not file_url)
   - file_path is consistent across environments
   - file_url can be regenerated using `get_file_url()`

2. **Use appropriate StorageType**
   - Helps with organization and path generation
   - Makes it easier to implement different retention policies

3. **Handle errors gracefully**
   - Validate files before upload
   - Catch and handle specific exceptions

4. **Clean up old files**
   - Implement deletion when entities are removed
   - Consider implementing retention policies

5. **Use presigned URLs for S3**
   - For private files that need temporary access
   - More secure than public URLs

## Migration from Direct File Storage

If you have existing code that writes files directly:

### Before (Direct filesystem access):
```python
with open(f"uploads/resume_{candidate_id}.pdf", "wb") as f:
    f.write(file_content)
```

### After (Using storage service):
```python
uploaded_file = self.storage_service.upload_file(
    file_content=file_content,
    filename="resume.pdf",
    content_type="application/pdf",
    storage_type=StorageType.CANDIDATE_RESUME,
    entity_id=str(candidate_id),
    company_id=str(company_id)
)
```

## Troubleshooting

### Local Storage

**Files not accessible via URL**:
- Ensure FastAPI is configured to serve static files from uploads directory
- Check that `LOCAL_STORAGE_URL` matches your API base URL

**Permission errors**:
- Ensure the `uploads` directory is writable
- Check Docker volume permissions if using Docker

### S3 Storage

**Access denied errors**:
- Verify AWS credentials are correct
- Check IAM permissions for the bucket
- Ensure bucket exists in the specified region

**Files not uploading**:
- Check bucket CORS configuration
- Verify bucket policy allows PutObject
- Check network connectivity to AWS

## Next Steps

1. Configure FastAPI to serve static files (for local storage)
2. Create S3 bucket and configure IAM permissions (for production)
3. Implement file cleanup when entities are deleted
4. Consider adding CloudFront for better S3 performance
5. Implement file scanning/virus checking for security
