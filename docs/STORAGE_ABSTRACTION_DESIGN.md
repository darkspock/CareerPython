# Storage Abstraction Layer - Diseño

## 🎯 Objetivo

Crear una abstracción que permita cambiar entre almacenamiento local (desarrollo) y S3 (producción) sin modificar el código de la aplicación.

---

## 🏗️ Arquitectura

### Patrón: Strategy + Dependency Injection

```
┌─────────────────────────────────────────────────────────┐
│                   Application Layer                      │
│         (Commands, Queries, Controllers)                 │
│                                                          │
│  UploadCandidateResumeCommand                           │
│       ↓ usa                                              │
│  StorageService (interface)                             │
└─────────────────────────────────────────────────────────┘
                          ↓ inyecta
┌─────────────────────────────────────────────────────────┐
│              Infrastructure Layer                        │
│                                                          │
│  ┌──────────────────┐      ┌──────────────────┐        │
│  │ LocalStorage     │      │  S3Storage       │        │
│  │ Implementation   │      │  Implementation  │        │
│  └──────────────────┘      └──────────────────┘        │
│         ↓                           ↓                    │
│  filesystem local            AWS S3 API                 │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura de Archivos

```
src/
  shared/
    domain/
      infrastructure/
        storage_service_interface.py  # Interface abstracta
    infrastructure/
      storage/
        __init__.py
        local_storage_service.py      # Implementación local
        s3_storage_service.py          # Implementación S3
        storage_factory.py             # Factory para crear instancia
```

---

## 🔧 Implementación

### 1. Interface (Domain Layer)

**Archivo**: `src/shared/domain/infrastructure/storage_service_interface.py`

```python
"""
Storage Service Interface - Domain Layer
NO debe tener dependencias de infraestructura (boto3, filesystem, etc.)
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class StorageType(Enum):
    """Tipos de archivos que se pueden almacenar"""
    CANDIDATE_RESUME = "candidate_resume"
    APPLICATION_RESUME = "application_resume"
    COMPANY_LOGO = "company_logo"
    ATTACHMENT = "attachment"


@dataclass(frozen=True)
class UploadedFile:
    """Resultado de una subida exitosa"""
    url: str  # URL completa del archivo (para acceso)
    path: str  # Path interno (para eliminación)
    size_bytes: int
    content_type: str
    uploaded_at: str  # ISO format


@dataclass(frozen=True)
class StorageConfig:
    """Configuración para el storage"""
    max_file_size_mb: int = 10
    allowed_content_types: tuple = ("application/pdf",)
    url_expiration_seconds: int = 3600  # 1 hora para presigned URLs


class StorageServiceInterface(ABC):
    """
    Interface para servicios de almacenamiento.

    Implementaciones:
    - LocalStorageService: Almacena en filesystem local
    - S3StorageService: Almacena en AWS S3
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
        """
        Sube un archivo al storage.

        Args:
            file_content: Contenido del archivo en bytes
            filename: Nombre original del archivo
            content_type: MIME type (ej: "application/pdf")
            storage_type: Tipo de archivo (candidate_resume, etc.)
            entity_id: ID de la entidad (candidate_id, application_id, etc.)
            company_id: ID de la empresa

        Returns:
            UploadedFile con la información del archivo subido

        Raises:
            ValueError: Si el archivo no cumple con las validaciones
            StorageError: Si falla la subida
        """
        pass

    @abstractmethod
    def get_file_url(self, file_path: str) -> str:
        """
        Obtiene la URL de acceso a un archivo.

        Para S3: Genera presigned URL temporal
        Para local: Retorna URL del servidor estático

        Args:
            file_path: Path interno del archivo

        Returns:
            URL de acceso al archivo
        """
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> bool:
        """
        Elimina un archivo del storage.

        Args:
            file_path: Path interno del archivo

        Returns:
            True si se eliminó correctamente, False si no existía

        Raises:
            StorageError: Si falla la eliminación
        """
        pass

    @abstractmethod
    def file_exists(self, file_path: str) -> bool:
        """
        Verifica si un archivo existe.

        Args:
            file_path: Path interno del archivo

        Returns:
            True si existe, False si no
        """
        pass

    @abstractmethod
    def get_file_size(self, file_path: str) -> Optional[int]:
        """
        Obtiene el tamaño de un archivo en bytes.

        Args:
            file_path: Path interno del archivo

        Returns:
            Tamaño en bytes o None si no existe
        """
        pass

    def validate_file(
        self,
        file_content: bytes,
        content_type: str,
        config: StorageConfig
    ) -> None:
        """
        Valida que un archivo cumpla con las restricciones.

        Args:
            file_content: Contenido del archivo
            content_type: MIME type
            config: Configuración con restricciones

        Raises:
            ValueError: Si el archivo no es válido
        """
        # Validar tamaño
        size_mb = len(file_content) / (1024 * 1024)
        if size_mb > config.max_file_size_mb:
            raise ValueError(
                f"File size ({size_mb:.2f}MB) exceeds maximum "
                f"allowed ({config.max_file_size_mb}MB)"
            )

        # Validar tipo de contenido
        if content_type not in config.allowed_content_types:
            raise ValueError(
                f"Content type '{content_type}' not allowed. "
                f"Allowed types: {config.allowed_content_types}"
            )


class StorageError(Exception):
    """Excepción base para errores de storage"""
    pass
```

---

### 2. Implementación Local (Infrastructure Layer)

**Archivo**: `src/shared/infrastructure/storage/local_storage_service.py`

```python
"""
Local Storage Service - Para desarrollo
Almacena archivos en el filesystem local
"""
import os
from pathlib import Path
from datetime import datetime
from typing import Optional
import logging

from src.shared.domain.infrastructure.storage_service_interface import (
    StorageServiceInterface,
    StorageType,
    UploadedFile,
    StorageConfig,
    StorageError,
)

logger = logging.getLogger(__name__)


class LocalStorageService(StorageServiceInterface):
    """
    Implementación de storage local para desarrollo.

    Estructura de directorios:
    uploads/
      company/{company_id}/
        candidates/{candidate_id}/
          resume.pdf
        applications/{application_id}/
          resume.pdf
        logos/
          logo.png
    """

    def __init__(
        self,
        base_path: str = "uploads",
        base_url: str = "http://localhost:8000/uploads",
        config: Optional[StorageConfig] = None
    ):
        """
        Args:
            base_path: Directorio base para almacenar archivos
            base_url: URL base para acceder a los archivos
            config: Configuración de storage
        """
        self.base_path = Path(base_path)
        self.base_url = base_url.rstrip('/')
        self.config = config or StorageConfig()

        # Crear directorio base si no existe
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"LocalStorageService initialized with base_path: {self.base_path}")

    def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str,
        storage_type: StorageType,
        entity_id: str,
        company_id: str,
    ) -> UploadedFile:
        """Sube archivo al filesystem local"""
        # Validar archivo
        self.validate_file(file_content, content_type, self.config)

        # Construir path
        file_path = self._build_file_path(
            storage_type, entity_id, company_id, filename
        )

        # Crear directorios si no existen
        file_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Escribir archivo
            with open(file_path, 'wb') as f:
                f.write(file_content)

            logger.info(f"File uploaded successfully: {file_path}")

            # Construir URL de acceso
            relative_path = file_path.relative_to(self.base_path)
            url = f"{self.base_url}/{relative_path.as_posix()}"

            return UploadedFile(
                url=url,
                path=str(relative_path),  # Path relativo para eliminación
                size_bytes=len(file_content),
                content_type=content_type,
                uploaded_at=datetime.utcnow().isoformat(),
            )

        except Exception as e:
            logger.error(f"Failed to upload file: {e}")
            raise StorageError(f"Failed to upload file: {str(e)}")

    def get_file_url(self, file_path: str) -> str:
        """Retorna URL del archivo en servidor local"""
        return f"{self.base_url}/{file_path}"

    def delete_file(self, file_path: str) -> bool:
        """Elimina archivo del filesystem"""
        full_path = self.base_path / file_path

        if not full_path.exists():
            logger.warning(f"File not found for deletion: {full_path}")
            return False

        try:
            full_path.unlink()
            logger.info(f"File deleted successfully: {full_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete file: {e}")
            raise StorageError(f"Failed to delete file: {str(e)}")

    def file_exists(self, file_path: str) -> bool:
        """Verifica si archivo existe"""
        full_path = self.base_path / file_path
        return full_path.exists() and full_path.is_file()

    def get_file_size(self, file_path: str) -> Optional[int]:
        """Obtiene tamaño del archivo"""
        full_path = self.base_path / file_path

        if not full_path.exists():
            return None

        try:
            return full_path.stat().st_size
        except Exception as e:
            logger.error(f"Failed to get file size: {e}")
            return None

    def _build_file_path(
        self,
        storage_type: StorageType,
        entity_id: str,
        company_id: str,
        filename: str
    ) -> Path:
        """
        Construye el path del archivo según el tipo.

        Ejemplos:
        - candidate_resume: company/123/candidates/456/resume.pdf
        - application_resume: company/123/applications/789/resume.pdf
        """
        # Sanitizar filename (remover caracteres peligrosos)
        safe_filename = self._sanitize_filename(filename)

        if storage_type == StorageType.CANDIDATE_RESUME:
            return self.base_path / "company" / company_id / "candidates" / entity_id / safe_filename

        elif storage_type == StorageType.APPLICATION_RESUME:
            return self.base_path / "company" / company_id / "applications" / entity_id / safe_filename

        elif storage_type == StorageType.COMPANY_LOGO:
            return self.base_path / "company" / company_id / "logos" / safe_filename

        elif storage_type == StorageType.ATTACHMENT:
            return self.base_path / "company" / company_id / "attachments" / entity_id / safe_filename

        else:
            raise ValueError(f"Unknown storage type: {storage_type}")

    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """Sanitiza el nombre del archivo"""
        # Remover caracteres peligrosos
        dangerous_chars = ['/', '\\', '..', '\0', '\n', '\r']
        safe = filename
        for char in dangerous_chars:
            safe = safe.replace(char, '_')

        # Limitar longitud
        if len(safe) > 255:
            name, ext = os.path.splitext(safe)
            safe = name[:250] + ext

        return safe
```

---

### 3. Implementación S3 (Infrastructure Layer)

**Archivo**: `src/shared/infrastructure/storage/s3_storage_service.py`

```python
"""
S3 Storage Service - Para producción
Almacena archivos en AWS S3
"""
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from typing import Optional
import logging

from src.shared.domain.infrastructure.storage_service_interface import (
    StorageServiceInterface,
    StorageType,
    UploadedFile,
    StorageConfig,
    StorageError,
)

logger = logging.getLogger(__name__)


class S3StorageService(StorageServiceInterface):
    """
    Implementación de storage en AWS S3 para producción.

    Estructura de paths en S3:
    bucket/
      company/{company_id}/
        candidates/{candidate_id}/
          resume.pdf
        applications/{application_id}/
          resume.pdf
    """

    def __init__(
        self,
        bucket_name: str,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        region_name: str = "us-east-1",
        config: Optional[StorageConfig] = None
    ):
        """
        Args:
            bucket_name: Nombre del bucket S3
            aws_access_key_id: AWS Access Key (opcional, usa env vars)
            aws_secret_access_key: AWS Secret Key (opcional, usa env vars)
            region_name: Región de AWS
            config: Configuración de storage
        """
        self.bucket_name = bucket_name
        self.config = config or StorageConfig()

        # Inicializar cliente S3
        session_kwargs = {"region_name": region_name}
        if aws_access_key_id and aws_secret_access_key:
            session_kwargs["aws_access_key_id"] = aws_access_key_id
            session_kwargs["aws_secret_access_key"] = aws_secret_access_key

        self.s3_client = boto3.client('s3', **session_kwargs)
        logger.info(f"S3StorageService initialized with bucket: {bucket_name}")

    def upload_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str,
        storage_type: StorageType,
        entity_id: str,
        company_id: str,
    ) -> UploadedFile:
        """Sube archivo a S3"""
        # Validar archivo
        self.validate_file(file_content, content_type, self.config)

        # Construir S3 key
        s3_key = self._build_s3_key(
            storage_type, entity_id, company_id, filename
        )

        try:
            # Subir a S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content,
                ContentType=content_type,
                # Metadata adicional
                Metadata={
                    'original-filename': filename,
                    'storage-type': storage_type.value,
                    'entity-id': entity_id,
                    'company-id': company_id,
                }
            )

            logger.info(f"File uploaded to S3: s3://{self.bucket_name}/{s3_key}")

            # Generar URL de acceso
            url = self.get_file_url(s3_key)

            return UploadedFile(
                url=url,
                path=s3_key,  # S3 key para eliminación
                size_bytes=len(file_content),
                content_type=content_type,
                uploaded_at=datetime.utcnow().isoformat(),
            )

        except ClientError as e:
            logger.error(f"Failed to upload file to S3: {e}")
            raise StorageError(f"Failed to upload file to S3: {str(e)}")

    def get_file_url(self, file_path: str) -> str:
        """Genera presigned URL temporal para S3"""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': file_path
                },
                ExpiresIn=self.config.url_expiration_seconds
            )
            return url
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            raise StorageError(f"Failed to generate presigned URL: {str(e)}")

    def delete_file(self, file_path: str) -> bool:
        """Elimina archivo de S3"""
        try:
            # Verificar si existe
            if not self.file_exists(file_path):
                logger.warning(f"File not found in S3: {file_path}")
                return False

            # Eliminar
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_path
            )

            logger.info(f"File deleted from S3: s3://{self.bucket_name}/{file_path}")
            return True

        except ClientError as e:
            logger.error(f"Failed to delete file from S3: {e}")
            raise StorageError(f"Failed to delete file from S3: {str(e)}")

    def file_exists(self, file_path: str) -> bool:
        """Verifica si archivo existe en S3"""
        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                logger.error(f"Error checking file existence: {e}")
                raise StorageError(f"Error checking file existence: {str(e)}")

    def get_file_size(self, file_path: str) -> Optional[int]:
        """Obtiene tamaño del archivo en S3"""
        try:
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=file_path
            )
            return response['ContentLength']
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return None
            else:
                logger.error(f"Error getting file size: {e}")
                return None

    def _build_s3_key(
        self,
        storage_type: StorageType,
        entity_id: str,
        company_id: str,
        filename: str
    ) -> str:
        """
        Construye el S3 key según el tipo.

        Ejemplos:
        - candidate_resume: company/123/candidates/456/resume.pdf
        - application_resume: company/123/applications/789/resume.pdf
        """
        # Usar mismo formato que local storage
        if storage_type == StorageType.CANDIDATE_RESUME:
            return f"company/{company_id}/candidates/{entity_id}/{filename}"

        elif storage_type == StorageType.APPLICATION_RESUME:
            return f"company/{company_id}/applications/{entity_id}/{filename}"

        elif storage_type == StorageType.COMPANY_LOGO:
            return f"company/{company_id}/logos/{filename}"

        elif storage_type == StorageType.ATTACHMENT:
            return f"company/{company_id}/attachments/{entity_id}/{filename}"

        else:
            raise ValueError(f"Unknown storage type: {storage_type}")
```

---

### 4. Factory (Infrastructure Layer)

**Archivo**: `src/shared/infrastructure/storage/storage_factory.py`

```python
"""
Storage Factory - Crea la instancia correcta según configuración
"""
import os
from typing import Optional

from src.shared.domain.infrastructure.storage_service_interface import (
    StorageServiceInterface,
    StorageConfig,
)
from src.shared.infrastructure.storage.local_storage_service import LocalStorageService
from src.shared.infrastructure.storage.s3_storage_service import S3StorageService


class StorageFactory:
    """Factory para crear instancias de StorageService"""

    @staticmethod
    def create_storage_service(
        storage_type: Optional[str] = None,
        config: Optional[StorageConfig] = None
    ) -> StorageServiceInterface:
        """
        Crea instancia de StorageService según configuración.

        Args:
            storage_type: 'local' o 's3' (opcional, usa env var STORAGE_TYPE)
            config: Configuración de storage

        Returns:
            Instancia de StorageServiceInterface

        Raises:
            ValueError: Si storage_type no es válido
        """
        storage_type = storage_type or os.getenv("STORAGE_TYPE", "local")

        if storage_type == "local":
            return LocalStorageService(
                base_path=os.getenv("LOCAL_STORAGE_PATH", "uploads"),
                base_url=os.getenv("LOCAL_STORAGE_URL", "http://localhost:8000/uploads"),
                config=config
            )

        elif storage_type == "s3":
            bucket_name = os.getenv("AWS_S3_BUCKET")
            if not bucket_name:
                raise ValueError("AWS_S3_BUCKET environment variable is required for S3 storage")

            return S3StorageService(
                bucket_name=bucket_name,
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_REGION", "us-east-1"),
                config=config
            )

        else:
            raise ValueError(f"Invalid storage type: {storage_type}. Use 'local' or 's3'")
```

---

### 5. Registrar en Container (Dependency Injection)

**Archivo**: `core/container.py`

```python
from dependency_injector import containers, providers

from src.shared.domain.infrastructure.storage_service_interface import StorageConfig
from src.shared.infrastructure.storage.storage_factory import StorageFactory


class Container(containers.DeclarativeContainer):
    # ... otros providers

    # Storage Service
    storage_config = providers.Singleton(
        StorageConfig,
        max_file_size_mb=10,
        allowed_content_types=("application/pdf",),
        url_expiration_seconds=3600,
    )

    storage_service = providers.Singleton(
        StorageFactory.create_storage_service,
        storage_type=None,  # Usa env var STORAGE_TYPE
        config=storage_config,
    )

    # Ejemplo de uso en command handler
    upload_candidate_resume_handler = providers.Factory(
        UploadCandidateResumeCommandHandler,
        storage_service=storage_service,
        repository=company_candidate_repository,
    )
```

---

## 🔧 Variables de Entorno

**Archivo**: `.env`

```bash
# Storage Configuration
STORAGE_TYPE=local  # 'local' para desarrollo, 's3' para producción

# Local Storage (desarrollo)
LOCAL_STORAGE_PATH=uploads
LOCAL_STORAGE_URL=http://localhost:8000/uploads

# S3 Storage (producción)
AWS_S3_BUCKET=company-resumes-prod
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_REGION=us-east-1

# File Upload Limits
MAX_RESUME_SIZE_MB=10
ALLOWED_RESUME_TYPES=application/pdf
```

---

## 📝 Uso en Command Handler

**Ejemplo**: `UploadCandidateResumeCommandHandler`

```python
from dataclasses import dataclass
from src.shared.application.command_bus import Command, CommandHandler
from src.shared.domain.infrastructure.storage_service_interface import (
    StorageServiceInterface,
    StorageType,
)


@dataclass(frozen=True)
class UploadCandidateResumeCommand(Command):
    candidate_id: str
    company_id: str
    file_content: bytes
    filename: str
    content_type: str


class UploadCandidateResumeCommandHandler(CommandHandler[UploadCandidateResumeCommand]):
    def __init__(
        self,
        storage_service: StorageServiceInterface,
        repository: CompanyCandidateRepositoryInterface
    ):
        self.storage_service = storage_service
        self.repository = repository

    def execute(self, command: UploadCandidateResumeCommand) -> None:
        # Buscar candidato
        candidate = self.repository.get_by_id(command.candidate_id)
        if not candidate:
            raise ValueError(f"Candidate {command.candidate_id} not found")

        # Eliminar CV anterior si existe
        if candidate.resume_url:
            # Extraer path del URL
            old_path = self._extract_path_from_url(candidate.resume_url)
            self.storage_service.delete_file(old_path)

        # Subir nuevo CV
        uploaded_file = self.storage_service.upload_file(
            file_content=command.file_content,
            filename=command.filename,
            content_type=command.content_type,
            storage_type=StorageType.CANDIDATE_RESUME,
            entity_id=command.candidate_id,
            company_id=command.company_id,
        )

        # Actualizar candidato
        updated_candidate = candidate.upload_resume(
            resume_url=uploaded_file.url,
            uploaded_by="company",
        )

        # Guardar
        self.repository.save(updated_candidate)
```

---

## 🧪 Testing

### Unit Test para Local Storage

```python
import pytest
from pathlib import Path
from src.shared.infrastructure.storage.local_storage_service import LocalStorageService
from src.shared.domain.infrastructure.storage_service_interface import StorageType


def test_upload_candidate_resume():
    # Arrange
    storage = LocalStorageService(base_path="test_uploads")
    file_content = b"PDF content here"

    # Act
    result = storage.upload_file(
        file_content=file_content,
        filename="resume.pdf",
        content_type="application/pdf",
        storage_type=StorageType.CANDIDATE_RESUME,
        entity_id="candidate-123",
        company_id="company-456",
    )

    # Assert
    assert result.size_bytes == len(file_content)
    assert "candidate-123" in result.path
    assert result.url.endswith("resume.pdf")

    # Cleanup
    storage.delete_file(result.path)
    Path("test_uploads").rmdir()
```

---

## ✅ Ventajas de esta Arquitectura

1. ✅ **Desacoplamiento**: Application layer no conoce S3 ni filesystem
2. ✅ **Testeable**: Fácil mockear StorageServiceInterface en tests
3. ✅ **Flexible**: Cambiar entre local/S3 con variable de entorno
4. ✅ **SOLID**: Cumple con Dependency Inversion Principle
5. ✅ **Extensible**: Fácil añadir Azure Blob, Google Cloud Storage, etc.
6. ✅ **Consistente**: Misma estructura de paths en local y S3
7. ✅ **Validaciones centralizadas**: validate_file() reutilizable

---

## 🚀 Próximos Pasos

1. Crear archivos en estructura propuesta
2. Registrar en container.py
3. Configurar variables de entorno
4. Crear endpoint de servir archivos estáticos (para local)
5. Usar en UploadCandidateResumeCommand
6. Tests unitarios

**¿Procedemos con la implementación?**
