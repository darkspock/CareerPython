import io
from typing import Dict, Any

from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError


class PDFProcessingService:
    """Service for processing PDF files with validation and text extraction"""

    # Configuration constants
    MAX_FILE_SIZE_MB = 10  # 10MB limit
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
    ALLOWED_CONTENT_TYPES = ["application/pdf"]

    @classmethod
    def validate_pdf_file(cls, content: bytes, content_type: str, filename: str) -> Dict[str, Any]:
        """
        Validate PDF file and return validation result
        Returns:
            Dict with 'is_valid', 'error_message', and 'metadata' keys
        """
        result: Dict[str, Any] = {
            "is_valid": True,
            "error_message": None,
            "metadata": {
                "file_size": len(content),
                "file_size_mb": round(len(content) / (1024 * 1024), 2),
                "content_type": content_type,
                "filename": filename
            }
        }

        # Check file size
        if len(content) > cls.MAX_FILE_SIZE_BYTES:
            result["is_valid"] = False
            result[
                "error_message"] = f"File size ({result['metadata']['file_size_mb']}MB) exceeds maximum allowed size ({cls.MAX_FILE_SIZE_MB}MB)"
            return result

        # Check content type
        if content_type not in cls.ALLOWED_CONTENT_TYPES:
            result["is_valid"] = False
            result["error_message"] = f"Invalid file type. Only PDF files are allowed. Received: {content_type}"
            return result

        # Check if file is empty
        if len(content) == 0:
            result["is_valid"] = False
            result["error_message"] = "File is empty"
            return result

        # Try to read PDF to validate it's a valid PDF
        try:
            pdf_reader = PdfReader(io.BytesIO(content))
            result["metadata"]["page_count"] = len(pdf_reader.pages)

            # Check if PDF has pages
            if len(pdf_reader.pages) == 0:
                result["is_valid"] = False
                result["error_message"] = "PDF file contains no pages"
                return result

        except PdfReadError as e:
            result["is_valid"] = False
            result["error_message"] = f"Invalid PDF file: {str(e)}"
            return result
        except Exception as e:
            result["is_valid"] = False
            result["error_message"] = f"Error reading PDF file: {str(e)}"
            return result

        return result

    @classmethod
    def extract_text_from_pdf(cls, content: bytes) -> Dict[str, Any]:
        """
        Extract text from PDF content
        Returns:
            Dict with 'success', 'text', 'error_message', and 'metadata' keys
        """
        result: Dict[str, Any] = {
            "success": True,
            "text": "",
            "error_message": None,
            "metadata": {
                "page_count": 0,
                "extraction_method": "PyPDF2"
            }
        }

        try:
            pdf_reader = PdfReader(io.BytesIO(content))
            result["metadata"]["page_count"] = len(pdf_reader.pages)

            extracted_text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text.strip():
                        extracted_text += f"--- Page {page_num + 1} ---\n"
                        extracted_text += page_text + "\n\n"
                except Exception as e:
                    # Continue with other pages if one page fails
                    result["metadata"][f"page_{page_num + 1}_error"] = str(e)
                    continue

            result["text"] = extracted_text.strip()

            # Check if any text was extracted
            if not result["text"]:
                result["success"] = False
                result[
                    "error_message"] = "No text could be extracted from the PDF. The file might be image-based or corrupted."

        except PdfReadError as e:
            result["success"] = False
            result["error_message"] = f"PDF read error: {str(e)}"
        except Exception as e:
            result["success"] = False
            result["error_message"] = f"Unexpected error during text extraction: {str(e)}"

        return result

    @classmethod
    def get_pdf_metadata(cls, content: bytes) -> Dict[str, Any]:
        """
        Extract metadata from PDF
        Returns:
            Dict with PDF metadata information
        """
        metadata: Dict[str, Any] = {
            "title": None,
            "author": None,
            "subject": None,
            "creator": None,
            "producer": None,
            "creation_date": None,
            "modification_date": None,
            "page_count": 0,
            "encrypted": False,
            "extraction_error": None
        }

        try:
            pdf_reader = PdfReader(io.BytesIO(content))
            metadata["page_count"] = len(pdf_reader.pages)
            metadata["encrypted"] = pdf_reader.is_encrypted

            if pdf_reader.metadata:
                pdf_metadata = pdf_reader.metadata
                metadata.update({
                    "title": pdf_metadata.get("/Title"),
                    "author": pdf_metadata.get("/Author"),
                    "subject": pdf_metadata.get("/Subject"),
                    "creator": pdf_metadata.get("/Creator"),
                    "producer": pdf_metadata.get("/Producer"),
                    "creation_date": str(pdf_metadata.get("/CreationDate")) if pdf_metadata.get(
                        "/CreationDate") else None,
                    "modification_date": str(pdf_metadata.get("/ModDate")) if pdf_metadata.get("/ModDate") else None,
                })

        except Exception as e:
            metadata["extraction_error"] = str(e)

        return metadata
