from typing import List, Optional

from fastapi import HTTPException, status

from adapters.http.company.mappers.company_mapper import CompanyResponseMapper
from adapters.http.company.schemas.company_request import (
    CreateCompanyRequest,
    UpdateCompanyRequest,
)
from adapters.http.company.schemas.company_response import CompanyResponse
from adapters.http.company.schemas.company_registration_request import (
    CompanyRegistrationRequest,
    LinkUserRequest,
)
from adapters.http.company.schemas.company_registration_response import (
    CompanyRegistrationResponse,
    LinkUserResponse,
)
from src.company_bc.company.application import GetCompanyByIdQuery, GetCompanyBySlugQuery, GetCompanyByDomainQuery, \
    ListCompaniesQuery
from src.company_bc.company.application.commands import (
    CreateCompanyCommand,
    UpdateCompanyCommand,
    UploadCompanyLogoCommand,
    SuspendCompanyCommand,
    ActivateCompanyCommand,
    DeleteCompanyCommand,
)
from src.company_bc.company.application.commands.register_company_with_user_command import (
    RegisterCompanyWithUserCommand,
)
from src.company_bc.company.application.commands.link_user_to_company_command import (
    LinkUserToCompanyCommand,
)
from src.company_bc.company.application.dtos.company_dto import CompanyDto

from src.company_bc.company.domain import CompanyId, CompanyStatusEnum
from src.company_bc.company.domain.value_objects import CompanyId as CompanyIdVO
from src.auth_bc.user.domain.value_objects import UserId
from src.company_bc.company.domain.exceptions.company_exceptions import (
    CompanyNotFoundError,
    CompanyValidationError, CompanyDomainAlreadyExistsError,
)
from src.auth_bc.user.domain.exceptions.user_exceptions import EmailAlreadyExistException, UserNotFoundError
from src.framework.domain.exceptions import InvalidCredentialsException
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus
import ulid


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
                company_type=request.company_type,
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

    def check_domain_available(self, domain: str) -> dict:
        """Check if a domain is available for registration"""
        try:
            query = GetCompanyByDomainQuery(domain=domain)
            dto: Optional[CompanyDto] = self.query_bus.query(query)
            
            return {
                "available": dto is None,
                "domain": domain
            }
        except Exception as e:
            # On error, assume domain is available (let registration handle validation)
            return {
                "available": True,
                "domain": domain
            }

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
    
    def register_company_with_user(self, request: CompanyRegistrationRequest) -> CompanyRegistrationResponse:
        """Register a new company with a new user"""
        try:
            # Generate IDs
            user_id = UserId.from_string(str(ulid.new()))
            company_id = CompanyIdVO.from_string(str(ulid.new()))
            
            # Execute command
            command = RegisterCompanyWithUserCommand(
                user_id=user_id,
                user_email=request.email,
                user_password=request.password,
                user_full_name=request.full_name,
                company_id=company_id,
                company_name=request.company_name,
                company_domain=request.domain,
                company_logo_url=request.logo_url,
                company_contact_phone=request.contact_phone,
                company_address=request.address,
                company_type=request.company_type,
                initialize_workflows=request.initialize_workflows,
                include_example_data=request.include_example_data,
            )
            self.command_bus.dispatch(command)
            
            return CompanyRegistrationResponse(
                company_id=str(company_id.value),
                user_id=str(user_id.value),
                message="Company and user registered successfully",
                redirect_url="/company/dashboard"
            )
            
        except EmailAlreadyExistException as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Este email ya está registrado. ¿Ya tienes una cuenta?"
            )
        except CompanyDomainAlreadyExistsError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Este dominio ya está en uso. Por favor, elige otro."
            )
        except CompanyValidationError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al registrar la empresa: {str(e)}"
            )
    
    def link_user_to_company(self, request: LinkUserRequest) -> LinkUserResponse:
        """Link an existing user to a new company"""
        try:
            # Generate company ID
            company_id = CompanyIdVO.from_string(str(ulid.new()))
            
            # Execute command
            command = LinkUserToCompanyCommand(
                user_email=request.email,
                user_password=request.password,
                company_id=company_id,
                company_name=request.company_name,
                company_domain=request.domain,
                company_logo_url=request.logo_url,
                company_contact_phone=request.contact_phone,
                company_address=request.address,
                company_type=request.company_type,
                initialize_workflows=request.initialize_workflows,
                include_example_data=request.include_example_data,
            )
            self.command_bus.dispatch(command)
            
            # Get user ID using query
            from src.auth_bc.user.application import GetUserByEmailQuery
            from src.auth_bc.user.application.queries.dtos.auth_dto import CurrentUserDto
            user_dto: Optional[CurrentUserDto] = self.query_bus.query(GetUserByEmailQuery(email=request.email))
            
            if not user_dto:
                raise UserNotFoundError(user_id=request.email)
            
            return LinkUserResponse(
                company_id=str(company_id.value),
                user_id=user_dto.user_id,  # CurrentUserDto has user_id field
                message="Usuario vinculado a la empresa exitosamente",
                redirect_url="/company/dashboard"
            )
            
        except UserNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado."
            )
        except InvalidCredentialsException as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos."
            )
        except CompanyDomainAlreadyExistsError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Este dominio ya está en uso."
            )
        except CompanyValidationError as e:
            # This can include password validation errors
            error_msg = str(e)
            if "password" in error_msg.lower() or "invalid" in error_msg.lower():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Email o contraseña incorrectos."
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al vincular la cuenta: {str(e)}"
            )
