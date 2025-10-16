import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional

from src.user.domain.enums.asset_enums import AssetTypeEnum, ProcessingStatusEnum
from src.user.domain.value_objects.UserId import UserId
from src.user.domain.value_objects.user_asset_id import UserAssetId


@dataclass
class UserAsset:
    """Entidad del dominio para assets de usuario"""
    id: UserAssetId
    user_id: UserId
    asset_type: AssetTypeEnum
    content: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    content_type: Optional[str] = None
    processing_status: ProcessingStatusEnum = ProcessingStatusEnum.PENDING
    processing_error: Optional[str] = None
    text_content: Optional[str] = None
    file_metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self) -> None:
        """Initialize defaults after construction"""
        if self.file_metadata is None:
            self.file_metadata = {}

    def update_content(self, content: Dict[str, Any]) -> None:
        """Actualizar contenido del asset"""
        self.content = content
        self.updated_at = datetime.utcnow()

    def set_processing_status(self, status: ProcessingStatusEnum, error: Optional[str] = None) -> None:
        """Actualizar estado de procesamiento"""
        self.processing_status = status
        self.processing_error = error
        self.updated_at = datetime.utcnow()

    def set_extracted_text(self, text: str) -> None:
        """Establecer texto extraído"""
        self.text_content = text
        self.set_processing_status(ProcessingStatusEnum.COMPLETED)

    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata entry"""
        if self.file_metadata is None:
            self.file_metadata = {}
        self.file_metadata[key] = value
        self.updated_at = datetime.utcnow()

    def extract_pdf_data(self) -> Optional[Dict[str, str]]:
        """Extraer nombre, teléfono y LinkedIn del texto usando regex mejorado"""
        if not self.text_content:
            return None

        result = {}

        # 1. Extract name with improved camelCase handling
        full_name = self._extract_name()
        if full_name:
            result.update(full_name)

        # 2. Extract phone number
        phone = self._extract_phone()
        if phone:
            result["phone"] = phone

        # 3. Extract LinkedIn URL
        linkedin = self._extract_linkedin()
        if linkedin:
            result["linkedin_url"] = linkedin

        return result if result else None

    def _extract_name(self) -> Optional[Dict[str, str]]:
        """Extract and clean name, handling camelCase like 'JuanMaciasjmacias'"""
        if not self.text_content:
            return None

        name_patterns = [
            # Pattern 1: "Name: John Doe" or "Nombre: Juan Pérez"
            r"(?:Name|Nombre|NOMBRE|NAME):\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)",
            # Pattern 2: First line with capital letters (often the name)
            r"^([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)",
            # Pattern 3: Before email patterns
            r"([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)\s*\n.*?@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            # Pattern 4: CamelCase pattern like "JuanMaciasjmacias"
            r"([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+[a-záéíóúñ]*)",
        ]

        for pattern in name_patterns:
            matches = re.search(pattern, self.text_content, re.MULTILINE | re.IGNORECASE)
            if matches:
                raw_name = matches.group(1).strip()

                # Handle camelCase names like "JuanMaciasjmacias"
                cleaned_name = self._split_camel_case_name(raw_name)

                if cleaned_name:
                    name_parts = cleaned_name.split()
                    if len(name_parts) >= 2:
                        first_name = name_parts[0]
                        last_name = " ".join(name_parts[1:])
                        return {
                            "first_name": first_name,
                            "last_name": last_name,
                            "full_name": cleaned_name
                        }
                    elif len(name_parts) == 1:
                        return {
                            "first_name": name_parts[0],
                            "last_name": "",
                            "full_name": name_parts[0]
                        }

        return None

    def _split_camel_case_name(self, name: str) -> str:
        """Split camelCase names like 'JuanMaciasjmacias' into 'Juan Macias jmacias'"""
        # If name contains spaces, return as-is
        if " " in name:
            return name

        # Split on capital letters but keep them
        # This regex finds capital letters that are followed by lowercase letters
        parts = re.findall(r'[A-ZÁÉÍÓÚÑ][a-záéíóúñ]*', name)

        if len(parts) >= 2:
            # Join with spaces
            return " ".join(parts)

        return name

    def _extract_phone(self) -> Optional[str]:
        """Extract phone number from text"""
        if not self.text_content:
            return None

        phone_patterns = [
            # Pattern 1: Spanish phone with country code on separate lines: "+34\n659203461"
            r"\+34\s*\n\s*([0-9]{9})",
            # Pattern 2: Spanish phone with country code: "+34 659203461" or "+34659203461"
            r"\+34\s*([0-9]{9})",
            # Pattern 3: General pattern with country code on separate lines: "+XX\nYYYYYYYYY"
            r"\+([0-9]{1,3})\s*\n\s*([0-9]{8,10})",
            # Pattern 4: Traditional patterns with labels
            r"(?:teléfono|telefono|phone|móvil|movil|tel\.?):\s*([+]?[0-9\s\-()]{9,15})",
            # Pattern 5: General international format
            r"([+]?[0-9]{2,3}\s?[0-9]{3}\s?[0-9]{3}\s?[0-9]{3})",
            # Pattern 6: Flexible pattern for various formats
            r"([+]?[0-9\s\-()]{9,15})",
        ]

        for i, pattern in enumerate(phone_patterns):
            matches = re.search(pattern, self.text_content, re.IGNORECASE | re.MULTILINE)
            if matches:
                if i == 0:  # Spanish pattern with separate lines
                    phone = f"+34{matches.group(1)}"
                elif i == 1:  # Spanish pattern together
                    phone = f"+34{matches.group(1)}"
                elif i == 2:  # General pattern with separate lines
                    phone = f"+{matches.group(1)}{matches.group(2)}"
                else:  # Other patterns
                    phone = matches.group(1).strip()

                # Clean phone number (remove spaces, dashes, parentheses but keep +)
                phone = re.sub(r'[^\d+]', '', phone)

                # Validate length (international numbers are typically 9-15 digits + country code)
                if len(phone) >= 9 and phone.startswith('+'):
                    return phone
                elif len(phone) >= 9:  # Domestic number without country code
                    return phone

        return None

    def _extract_linkedin(self) -> Optional[str]:
        """Extract LinkedIn URL from text"""
        if not self.text_content:
            return None

        linkedin_patterns = [
            # LinkedIn URL patterns
            r"(?:linkedin\.com/in/)([a-zA-Z0-9\-]+)",
            r"(?:www\.linkedin\.com/in/)([a-zA-Z0-9\-]+)",
            r"(?:https?://(?:www\.)?linkedin\.com/in/)([a-zA-Z0-9\-]+)",
        ]

        for pattern in linkedin_patterns:
            matches = re.search(pattern, self.text_content, re.IGNORECASE)
            if matches:
                username = matches.group(1)
                return f"linkedin.com/in/{username}"

        return None

    def is_resume_pdf(self) -> bool:
        """Verificar si es un PDF de CV"""
        return self.asset_type == AssetTypeEnum.PDF_RESUME

    def is_linkedin_profile(self) -> bool:
        """Verificar si es un perfil de LinkedIn"""
        return self.asset_type == AssetTypeEnum.LINKEDIN_PROFILE

    def get_extracted_text(self) -> Optional[str]:
        """Get extracted text"""
        if self.is_resume_pdf():
            return self.text_content or self.content.get("extracted_text")
        return None

    def get_file_size_mb(self) -> Optional[float]:
        """Get file size in MB"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return None

    def is_processing_complete(self) -> bool:
        """Verificar si el procesamiento está completo"""
        return self.processing_status == ProcessingStatusEnum.COMPLETED

    def is_processing_failed(self) -> bool:
        """Verificar si el procesamiento falló"""
        return self.processing_status == ProcessingStatusEnum.FAILED

    def validate_pdf_file(self) -> bool:
        """Validar si es un archivo PDF válido"""
        return (self.content_type == "application/pdf" and self.file_size is not None and self.file_size > 0)

    @staticmethod
    def create(
            id: UserAssetId,
            user_id: UserId,
            asset_type: AssetTypeEnum,
            content: Dict[str, Any],
            file_name: Optional[str] = None,
            file_size: Optional[int] = None,
            content_type: Optional[str] = None
    ) -> 'UserAsset':
        """Factory method para crear un nuevo asset"""
        return UserAsset(
            id=id,
            user_id=user_id,
            asset_type=asset_type,
            content=content,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            file_name=file_name,
            file_size=file_size,
            content_type=content_type,
            processing_status=ProcessingStatusEnum.PENDING,
            processing_error=None,
            text_content=None,
            file_metadata={}
        )
