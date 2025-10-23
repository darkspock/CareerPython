"""Company admin controller"""
import logging
from typing import List, Optional, Dict, Any

from adapters.http.admin.schemas.company import (
    CompanyCreate, CompanyUpdate, CompanyResponse, CompanyListResponse,
    CompanyStatsResponse, CompanyActionResponse
)
from src.company.application.commands import CreateCompanyCommand, UpdateCompanyCommand, ActivateCompanyCommand, \
    SuspendCompanyCommand, DeleteCompanyCommand
# DTOs and schemas
from src.company.application.queries.dtos.company_dto import CompanyDto
from src.company.application.queries.get_companies_stats import GetCompaniesStatsQuery
from src.company.application.queries.get_company_by_id import GetCompanyByIdQuery
# Company queries
from src.company.application.queries.list_companies import ListCompaniesQuery
from src.company.domain import Company, CompanyId
# Domain enums
from src.company.domain.enums.company_status import CompanyStatusEnum
from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus
from src.user.domain.value_objects.UserId import UserId

logger = logging.getLogger(__name__)


class CompanyController:
    """Controller for company admin operations"""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self.command_bus = command_bus
        self.query_bus = query_bus

    def list_companies(
            self,
            search_term: Optional[str] = None,
            status: Optional[str] = None,
            page: Optional[int] = None,
            page_size: Optional[int] = None
    ) -> CompanyListResponse:
        """List companies with filtering options"""
        try:
            # Set defaults
            page = page or 1
            page_size = min(page_size or 10, 100)  # Limit max page size
            offset = (page - 1) * page_size

            # Convert status string to enum if provided
            status_enum = None
            if status and status != "":
                try:
                    status_enum = CompanyStatusEnum(status.upper())
                except ValueError:
                    logger.warning(f"Invalid status filter: {status}")

            # Execute query
            query = ListCompaniesQuery(
                status=status_enum,
                search_term=search_term,
                limit=page_size,
                offset=offset
            )

            company_dtos: List[CompanyDto] = self.query_bus.query(query)

            # Convert DTOs to response models
            company_responses = [self._dto_to_response(dto) for dto in company_dtos]

            # Get total count (for now, we'll use the returned count)
            total = len(company_dtos)  # This should ideally come from a separate count query
            total_pages = (total + page_size - 1) // page_size

            return CompanyListResponse(
                companies=company_responses,
                total=total,
                page=page,
                page_size=page_size,
                total_pages=total_pages
            )

        except Exception as e:
            logger.error(f"Error listing companies: {str(e)}")
            raise

    def get_company_stats(self) -> CompanyStatsResponse:
        """Get company statistics"""
        try:
            query = GetCompaniesStatsQuery()
            stats: Dict[str, Any] = self.query_bus.query(query)

            return CompanyStatsResponse(
                total_companies=stats.get("total_count", 0),
                pending_approval=stats.get("pending_count", 0),
                approved_companies=stats.get("approved_count", 0),
                active_companies=stats.get("active_count", 0),
                rejected_companies=stats.get("rejected_count", 0)
            )

        except Exception as e:
            logger.error(f"Error getting company stats: {str(e)}")
            raise

    def get_company_by_id(self, company_id: CompanyId) -> CompanyResponse:
        """Get a specific company by ID"""
        try:
            query = GetCompanyByIdQuery(company_id=company_id)
            company: Optional[Company] = self.query_bus.query(query)

            if not company:
                raise ValueError(f"Company with ID {company_id} not found")

            company_dto = CompanyDto.from_entity(company)
            return self._dto_to_response(company_dto)

        except Exception as e:
            logger.error(f"Error getting company {company_id}: {str(e)}")
            raise

    def create_company(self, company_data: CompanyCreate, current_admin_id: str) -> CompanyResponse:
        """Create a new company"""
        try:
            # Import CompanyId here to avoid circular imports
            from src.company.domain.value_objects.company_id import CompanyId

            # Generate a new company ID
            company_id = CompanyId.generate()

            command = CreateCompanyCommand(
                id=str(company_id),
                name=company_data.name,
                domain=company_data.domain,
                logo_url=company_data.logo_url,
                settings=company_data.settings
            )

            self.command_bus.dispatch(command)

            # Get the created company
            return self.get_company_by_id(company_id)

        except Exception as e:
            logger.error(f"Error creating company: {str(e)}")
            raise

    def update_company(
            self,
            company_id: CompanyId,
            company_data: CompanyUpdate,
            current_admin_id: str
    ) -> CompanyResponse:
        """Update an existing company"""
        try:
            command = UpdateCompanyCommand(
                id=str(company_id),
                name=company_data.name,
                domain=company_data.domain,
                logo_url=company_data.logo_url,
                settings=company_data.settings or {}
            )

            self.command_bus.dispatch(command)

            # Get the updated company
            return self.get_company_by_id(company_id)

        except Exception as e:
            logger.error(f"Error updating company {company_id}: {str(e)}")
            raise

    def approve_company(self, company_id: CompanyId, current_admin_id: str) -> CompanyActionResponse:
        """Approve a pending company"""
        try:
            command = ActivateCompanyCommand(id=company_id, activated_by=current_admin_id)
            self.command_bus.dispatch(command)

            # Get the updated company to return in response
            updated_company = self.get_company_by_id(company_id)

            return CompanyActionResponse(
                message="Company approved successfully",
                affected_count=1,
                company=updated_company
            )

        except Exception as e:
            logger.error(f"Error approving company {company_id}: {str(e)}")
            raise

    def reject_company(
            self,
            company_id: CompanyId,
            reason: Optional[str] = None
    ) -> CompanyActionResponse:
        """Reject a pending company"""
        try:
            command = SuspendCompanyCommand(
                id=company_id,
                reason=reason or "No reason provided"
            )
            self.command_bus.dispatch(command)

            # Get the updated company to return in response
            updated_company = self.get_company_by_id(company_id)

            return CompanyActionResponse(
                message="Company rejected successfully",
                affected_count=1,
                company=updated_company
            )

        except Exception as e:
            logger.error(f"Error rejecting company {company_id}: {str(e)}")
            raise

    def activate_company(self, company_id: CompanyId) -> CompanyActionResponse:
        """Activate an inactive company"""
        try:
            command = SuspendCompanyCommand(id=company_id)
            self.command_bus.dispatch(command)

            # Get the updated company to return in response
            updated_company = self.get_company_by_id(company_id)

            return CompanyActionResponse(
                message="Company activated successfully",
                affected_count=1,
                company=updated_company
            )

        except Exception as e:
            logger.error(f"Error activating company {company_id}: {str(e)}")
            raise

    def deactivate_company(self, company_id: CompanyId, current_admin_id: str) -> CompanyActionResponse:
        """Deactivate an active company"""
        try:
            command = SuspendCompanyCommand(id=company_id)
            self.command_bus.dispatch(command)

            # Get the updated company to return in response
            updated_company = self.get_company_by_id(company_id)

            return CompanyActionResponse(
                message="Company deactivated successfully",
                affected_count=1,
                company=updated_company
            )

        except Exception as e:
            logger.error(f"Error deactivating company {company_id}: {str(e)}")
            raise

    def delete_company(self, company_id: CompanyId, current_admin_id: str) -> CompanyActionResponse:
        """Delete a company"""
        try:
            command = DeleteCompanyCommand(id=company_id)
            self.command_bus.dispatch(command)

            return CompanyActionResponse(
                message="Company deleted successfully",
                affected_count=1,
                company=None  # Company is deleted, so no company data to return
            )

        except Exception as e:
            logger.error(f"Error deleting company {company_id}: {str(e)}")
            raise

    def _dto_to_response(self, dto: CompanyDto) -> CompanyResponse:
        """Convert CompanyDto to CompanyResponse"""
        return CompanyResponse(**dto.__dict__)
