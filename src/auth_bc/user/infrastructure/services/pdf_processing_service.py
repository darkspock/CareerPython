import io
import logging
from typing import Dict, Any

try:
    import pypdf

    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

from src.auth_bc.user.domain.enums.asset_enums import ProcessingStatusEnum


class PDFProcessingService:
    """Servicio para procesar archivos PDF"""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def extract_text_from_pdf(self, pdf_bytes: bytes) -> Dict[str, Any]:
        """Extraer texto de un archivo PDF"""
        result: Dict[str, Any] = {
            "text": "",
            "status": ProcessingStatusEnum.FAILED,
            "error": None,
            "metadata": {}
        }

        if not PYPDF_AVAILABLE:
            error_msg = "pypdf is not installed. Install with: pip install pypdf"
            self.logger.error(error_msg)
            result["error"] = error_msg
            return result

        try:
            # Create a file-like object from bytes
            pdf_file = io.BytesIO(pdf_bytes)

            # Create PDF reader
            pdf_reader = pypdf.PdfReader(pdf_file)

            # Get metadata
            metadata = {
                "num_pages": len(pdf_reader.pages),
                "metadata": {}
            }

            if pdf_reader.metadata:
                metadata["metadata"] = {
                    "title": pdf_reader.metadata.get("/Title", ""),
                    "author": pdf_reader.metadata.get("/Author", ""),
                    "subject": pdf_reader.metadata.get("/Subject", ""),
                    "creator": pdf_reader.metadata.get("/Creator", ""),
                    "producer": pdf_reader.metadata.get("/Producer", ""),
                    "creation_date": str(pdf_reader.metadata.get("/CreationDate", "")),
                    "modification_date": str(pdf_reader.metadata.get("/ModDate", ""))
                }

            # Extract text from all pages
            extracted_text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        extracted_text += f"\n--- Page {page_num + 1} ---\n"
                        extracted_text += page_text
                        extracted_text += "\n"
                except Exception as page_error:
                    self.logger.warning(f"Failed to extract text from page {page_num + 1}: {str(page_error)}")
                    continue

            # Clean up the text
            cleaned_text = self._clean_extracted_text(extracted_text)

            result.update({
                "text": cleaned_text,
                "status": ProcessingStatusEnum.COMPLETED,
                "error": None,
                "metadata": metadata
            })

            self.logger.info(
                f"Successfully extracted {len(cleaned_text)} characters from PDF with {metadata['num_pages']} pages"
            )

        except Exception as e:
            error_msg = f"Failed to process PDF: {str(e)}"
            self.logger.error(error_msg)
            result["error"] = error_msg
            result["status"] = ProcessingStatusEnum.FAILED

        return result

    def _clean_extracted_text(self, text: str) -> str:
        """Limpiar el texto extraído"""
        if not text:
            return ""

        # Remove excessive whitespace and normalize line breaks
        lines = []
        for line in text.split('\n'):
            line = line.strip()
            if line:  # Skip empty lines
                lines.append(line)

        # Join lines with single line breaks
        cleaned_text = '\n'.join(lines)

        # Remove multiple consecutive line breaks
        while '\n\n\n' in cleaned_text:
            cleaned_text = cleaned_text.replace('\n\n\n', '\n\n')

        return cleaned_text

    def validate_pdf_file(self, pdf_bytes: bytes) -> bool:
        """Validar si el archivo es un PDF válido"""
        if not PYPDF_AVAILABLE:
            self.logger.warning("pypdf not available, skipping PDF validation")
            return True  # Assume valid if we can't validate

        try:
            pdf_file = io.BytesIO(pdf_bytes)
            pdf_reader = pypdf.PdfReader(pdf_file)

            # Try to read metadata and first page to ensure it's valid
            _ = len(pdf_reader.pages)
            if pdf_reader.pages:
                _ = pdf_reader.pages[0]

            return True
        except Exception as e:
            self.logger.error(f"PDF validation failed: {str(e)}")
            return False
