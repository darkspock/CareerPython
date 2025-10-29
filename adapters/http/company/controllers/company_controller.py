from typing import List, Optional

import ulid
from fastapi import HTTPException, status

from adapters.http.company.mappers.company_mapper import CompanyResponseMapper
from adapters.http.company.schemas.company_request import (
    CreateCompanyRequest,
    UpdateCompanyRequest,
)
from adapters.http.company.schemas.company_response import CompanyResponse
from src.company.application.commands import (
    CreateCompanyCommand,
    UpdateCompanyCommand,
    UploadCompanyLogoCommand,
    SuspendCompanyCommand,
    ActivateCompanyCommand,
    DeleteCompanyCommand,
)
from src.company.application.dtos.company_dto import CompanyDto
from src.company.application.queries import (
    GetCompanyByIdQuery,
    GetCompanyByDomainQuery,
    GetCompanyBySlugQuery,
    ListCompaniesQuery,
)
from src.company.domain import CompanyId, CompanyStatusEnum
from src.company.domain.exceptions.company_exceptions import (
    CompanyNotFoundError,
    CompanyValidationError, CompanyDomainAlreadyExistsError,
)
from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus


class CompanyController:
    """Controller for Company operations"""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self.command_bus = command_bus
        self.query_bus = query_bus

    def create_company(self, request: CreateCompanyRequest) -> CompanyResponse:
        """Create a new company"""
        try:
            # Generate new ID
            company_id = str(ulid.new())

            # Execute command
            command = CreateCompanyCommand(
                id=company_id,
                name=request.name,
                domain=request.domain,
                logo_url=request.logo_url,
                settings=request.settings,
            )
            self.command_bus.dispatch(command)

            # Query to get created company
            query = GetCompanyByIdQuery(company_id=CompanyId.from_string(company_id))
            dto: Optional[CompanyDto] = self.query_bus.query(query)

            if not dto:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Company created but not found"
                )

            return CompanyResponseMapper.dto_to_response(dto)

        except CompanyValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except CompanyDomainAlreadyExistsError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create company: {str(e)}"
            )

    def get_company_by_id(self, company_id: str) -> CompanyResponse:
        """Get a company by ID"""
        try:
            query = GetCompanyByIdQuery(company_id=CompanyId.from_string(company_id))
            dto: Optional[CompanyDto] = self.query_bus.query(query)

            if not dto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Company with id {company_id} not found"
                )

            return CompanyResponseMapper.dto_to_response(dto)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve company: {str(e)}"
            )

    def get_company_by_domain(self, domain: str) -> CompanyResponse:
        """Get a company by domain"""
        try:
            query = GetCompanyByDomainQuery(domain=domain)
            dto: Optional[CompanyDto] = self.query_bus.query(query)

            if not dto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Company with domain {domain} not found"
                )

            return CompanyResponseMapper.dto_to_response(dto)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve company: {str(e)}"
            )

    def get_company_by_slug(self, slug: str) -> CompanyResponse:
        """Get a company by slug"""
        try:
            query = GetCompanyBySlugQuery(slug=slug)
            dto: Optional[CompanyDto] = self.query_bus.query(query)

            if not dto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Company with slug {slug} not found"
                )

            return CompanyResponseMapper.dto_to_response(dto)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve company: {str(e)}"
            )

    def list_companies(
            self,
            search_term: Optional[str] = None,
            status_filter: Optional[CompanyStatusEnum] = None,
            limit: int = 100,
            offset: int = 0
    ) -> List[CompanyResponse]:
        """List all companies"""
        try:
            query = ListCompaniesQuery(
                status=status_filter,
                search_term=search_term,
                limit=limit,
                offset=offset
            )
            dtos: List[CompanyDto] = self.query_bus.query(query)

            return [CompanyResponseMapper.dto_to_response(dto) for dto in dtos]

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to list companies: {str(e)}"
            )

    def update_company(self, company_id: str, request: UpdateCompanyRequest) -> CompanyResponse:
        """Update a company"""
        try:
            # Execute command
            command = UpdateCompanyCommand(
                id=company_id,
                name=request.name,
                domain=request.domain,
                slug=request.slug,
                logo_url=request.logo_url,
                settings=request.settings,
            )
            self.command_bus.dispatch(command)

            # Query to get updated company
            query = GetCompanyByIdQuery(company_id=CompanyId.from_string(company_id))
            dto: Optional[CompanyDto] = self.query_bus.query(query)

            if not dto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Company with id {company_id} not found"
                )

            return CompanyResponseMapper.dto_to_response(dto)

        except CompanyNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except CompanyValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except CompanyDomainAlreadyExistsError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update company: {str(e)}"
            )

    def suspend_company(self, company_id: str, reason: str) -> CompanyResponse:
        """Suspend a company"""
        try:
            # Execute command
            command = SuspendCompanyCommand(id=CompanyId.from_string(company_id), reason=reason)
            self.command_bus.dispatch(command)

            # Query to get updated company
            query = GetCompanyByIdQuery(company_id=CompanyId.from_string(company_id))
            dto: Optional[CompanyDto] = self.query_bus.query(query)

            if not dto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Company with id {company_id} not found"
                )

            return CompanyResponseMapper.dto_to_response(dto)

        except CompanyNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to suspend company: {str(e)}"
            )

    def activate_company(self, company_id: CompanyId) -> CompanyResponse:
        """Activate a company"""
        try:
            # Execute command
            command = ActivateCompanyCommand(id=company_id, activated_by='')
            self.command_bus.dispatch(command)

            # Query to get updated company
            query = GetCompanyByIdQuery(company_id=company_id)
            dto: Optional[CompanyDto] = self.query_bus.query(query)

            if not dto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Company with id {company_id} not found"
                )

            return CompanyResponseMapper.dto_to_response(dto)

        except CompanyNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to activate company: {str(e)}"
            )

    def delete_company(self, company_id: str) -> None:
        """Delete a company (soft delete)"""
        try:
            command = DeleteCompanyCommand(id=CompanyId(company_id))
            self.command_bus.dispatch(command)

        except CompanyNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete company: {str(e)}"
            )

    def upload_company_logo(
        self,
        company_id: str,
        file_content: bytes,
        filename: str,
        content_type: str
    ) -> CompanyResponse:
        """Upload a company logo"""
        try:
            # Execute command
            command = UploadCompanyLogoCommand(
                company_id=company_id,
                file_content=file_content,
                filename=filename,
                content_type=content_type
            )
            self.command_bus.dispatch(command)

            # Query to get updated company
            query = GetCompanyByIdQuery(company_id=CompanyId.from_string(company_id))
            dto: Optional[CompanyDto] = self.query_bus.query(query)

            if not dto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Company with id {company_id} not found"
                )

            return CompanyResponseMapper.dto_to_response(dto)

        except CompanyNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload logo: {str(e)}"
            )
