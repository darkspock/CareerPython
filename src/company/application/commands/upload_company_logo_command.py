from dataclasses import dataclass

from src.company.domain.exceptions.company_exceptions import CompanyNotFoundError
from src.company.domain.infrastructure.company_repository_interface import CompanyRepositoryInterface
from src.company.domain.value_objects import CompanyId
from src.shared.application.command_bus import Command, CommandHandler
from src.shared.domain.infrastructure.storage_service_interface import (
    StorageServiceInterface,
    StorageType,
)


@dataclass(frozen=True)
class UploadCompanyLogoCommand(Command):
    """Command to upload a logo for a company"""
    company_id: str
    file_content: bytes
    filename: str
    content_type: str


class UploadCompanyLogoCommandHandler(CommandHandler[UploadCompanyLogoCommand]):
    """Handler for uploading a logo for a company"""

    def __init__(
            self,
            repository: CompanyRepositoryInterface,
            storage_service: StorageServiceInterface
    ):
        self._repository = repository
        self._storage_service = storage_service

    def execute(self, command: UploadCompanyLogoCommand) -> None:
        """Handle the upload logo command"""
        # Get the company
        company_id = CompanyId.from_string(command.company_id)
        company = self._repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFoundError(f"Company with id {command.company_id} not found")

        # Upload file to storage
        uploaded_file = self._storage_service.upload_file(
            file_content=command.file_content,
            filename=command.filename,
            content_type=command.content_type,
            storage_type=StorageType.COMPANY_LOGO,
            entity_id=str(company.id),
            company_id=str(company.id)
        )

        # Update the company with the logo URL
        updated_company = company.update(
            name=company.name,
            domain=company.domain,
            slug=company.slug,
            logo_url=uploaded_file.file_url,  # Use the public URL
            settings=company.settings
        )

        # Save to repository
        self._repository.save(updated_company)
