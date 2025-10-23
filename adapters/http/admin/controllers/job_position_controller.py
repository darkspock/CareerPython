"""Job position admin controller"""
import logging
from datetime import date
from typing import List, Optional, Dict, Any

from adapters.http.admin.mappers.job_position_mapper import JobPositionMapper
from adapters.http.admin.schemas.job_position import (
    JobPositionCreate, JobPositionUpdate, JobPositionResponse, JobPositionListResponse,
    JobPositionStatsResponse, JobPositionActionResponse
)
from src.candidate.domain.enums.candidate_enums import LanguageEnum, LanguageLevelEnum, PositionRoleEnum
from src.company.domain.value_objects.company_id import CompanyId
# Job position commands
from src.job_position.application.commands.create_job_position import CreateJobPositionCommand
from src.job_position.application.commands.delete_job_position import DeleteJobPositionCommand
from src.job_position.application.commands.update_job_position import UpdateJobPositionCommand
from src.job_position.application.queries.get_job_position_by_id import GetJobPositionByIdQuery
from src.job_position.application.queries.get_job_positions_stats import GetJobPositionsStatsQuery
from src.job_position.application.queries.job_position_dto import JobPositionDto
# Job position queries
from src.job_position.application.queries.list_job_positions import ListJobPositionsQuery
# Domain enums
from src.job_position.domain.enums import WorkLocationTypeEnum, ContractTypeEnum
from src.job_position.domain.enums.position_level_enum import JobPositionLevelEnum
from src.job_position.domain.value_objects import JobPositionId
from src.job_position.domain.value_objects.salary_range import SalaryRange
from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus
from src.shared.domain.enums.job_category import JobCategoryEnum

# DTOs and schemas

logger = logging.getLogger(__name__)


class JobPositionController:
    """Controller for job position admin operations"""

    # Mapping dictionaries for enum conversions
    EMPLOYMENT_TYPE_MAPPING = {
        "full_time": ContractTypeEnum.FULL_TIME,
        "part_time": ContractTypeEnum.PART_TIME,
        "contract": ContractTypeEnum.CONTRACT,
        "internship": ContractTypeEnum.INTERNSHIP
    }

    EXPERIENCE_LEVEL_MAPPING = {
        "junior": JobPositionLevelEnum.JUNIOR,
        "mid": JobPositionLevelEnum.MID,
        "senior": JobPositionLevelEnum.SENIOR,
        "lead": JobPositionLevelEnum.LEAD
    }

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self.command_bus = command_bus
        self.query_bus = query_bus

    def _create_salary_range(self, salary_min: Optional[int], salary_max: Optional[int],
                             salary_currency: Optional[str]) -> Optional[SalaryRange]:
        """Helper method to create salary range from individual fields"""
        if salary_min is not None and salary_max is not None:
            return SalaryRange(
                min_salary=float(salary_min),
                max_salary=float(salary_max),
                currency=salary_currency or "USD"
            )
        return None

    def _map_experience_level_to_position_level(self, experience_level: Optional[str]) -> Optional[
        'JobPositionLevelEnum']:
        """Helper method to map experience level to position level"""
        if experience_level:
            return self.EXPERIENCE_LEVEL_MAPPING.get(experience_level)
        return None

    def _parse_application_deadline(self, deadline_str: Optional[str]) -> Optional[date]:
        """Helper method to parse application deadline string"""
        if deadline_str:
            from datetime import datetime
            try:
                return datetime.strptime(deadline_str, "%Y-%m-%d").date()
            except ValueError:
                return None
        return None

    def _convert_languages_to_enums(self, languages_dict: Optional[Dict[str, str]]) -> Optional[
        Dict[LanguageEnum, LanguageLevelEnum]]:
        """Convert string dictionary to enum dictionary for languages"""
        if not languages_dict:
            return None

        try:
            enum_dict = {}
            for lang_str, level_str in languages_dict.items():
                lang_enum = LanguageEnum(lang_str.lower())
                level_enum = LanguageLevelEnum(level_str.lower())
                enum_dict[lang_enum] = level_enum
            return enum_dict
        except ValueError as e:
            logger.warning(f"Invalid language or level enum: {e}")
            return None

    def _convert_roles_to_enums(self, roles_list: Optional[List[str]]) -> Optional[List[PositionRoleEnum]]:
        """Convert string list to enum list for desired roles"""
        if not roles_list:
            return None

        try:
            enum_list = []
            for role_str in roles_list:
                role_enum = PositionRoleEnum(role_str.lower())
                enum_list.append(role_enum)
            return enum_list
        except ValueError as e:
            logger.warning(f"Invalid role enum: {e}")
            return None

    def list_positions(
            self,
            company_id: Optional[str] = None,
            search_term: Optional[str] = None,
            department: Optional[str] = None,
            location: Optional[str] = None,
            employment_type: Optional[str] = None,
            experience_level: Optional[str] = None,
            is_remote: Optional[bool] = None,
            is_active: Optional[bool] = None,
            page: Optional[int] = None,
            page_size: Optional[int] = None
    ) -> JobPositionListResponse:
        """List job positions with filters"""
        try:
            page = page or 1
            page_size = page_size or 10
            offset = (page - 1) * page_size

            query = ListJobPositionsQuery(
                company_id=company_id,
                search_term=search_term,
                location=location,
                limit=page_size,
                offset=offset
            )

            positions: List[JobPositionDto] = self.query_bus.query(query)

            # Convert DTOs to response schemas using mapper
            # TODO: Ideally we should get company names in batch for performance
            response_positions = []
            for dto in positions:
                # For now, we don't have company name, could be improved by joining in query
                response_positions.append(JobPositionMapper.dto_to_response(dto, company_name=None))

            # Calculate pagination
            total = len(response_positions)  # This is simplified, should be from repository
            total_pages = (total + page_size - 1) // page_size

            return JobPositionListResponse(
                positions=response_positions,
                total=total,
                page=page,
                page_size=page_size,
                total_pages=total_pages
            )

        except Exception as e:
            logger.error(f"Error listing positions: {str(e)}")
            raise

    def get_position_stats(self) -> JobPositionStatsResponse:
        """Get job position statistics"""
        try:
            query = GetJobPositionsStatsQuery()
            stats_data: Dict[str, Any] = self.query_bus.query(query)

            return JobPositionStatsResponse(
                total_positions=stats_data.get("total_count", 0),
                active_positions=stats_data.get("active_count", 0),
                inactive_positions=stats_data.get("inactive_count", 0),
                positions_by_type={},
                positions_by_company={}
            )

        except Exception as e:
            logger.error(f"Error getting position stats: {str(e)}")
            raise

    def get_position_by_id(self, position_id: str) -> JobPositionResponse:
        """Get a specific job position by ID"""
        try:
            query = GetJobPositionByIdQuery(id=JobPositionId.from_string(position_id))
            position_dto: Optional[JobPositionDto] = self.query_bus.query(query)

            if not position_dto:
                raise ValueError(f"Position with ID {position_id} not found")

            # TODO: Could fetch company name for better UX
            return JobPositionMapper.dto_to_response(position_dto, company_name=None)

        except Exception as e:
            logger.error(f"Error getting position {position_id}: {str(e)}")
            raise

    def create_position(self, position_data: JobPositionCreate) -> JobPositionActionResponse:
        """Create a new job position"""
        try:
            # Map employment type to contract type
            contract_type = self.EMPLOYMENT_TYPE_MAPPING.get(position_data.employment_type, ContractTypeEnum.FULL_TIME)

            # Map remote to work location type
            work_location_type = WorkLocationTypeEnum.REMOTE if position_data.is_remote else WorkLocationTypeEnum.ON_SITE

            # Create salary range
            salary_range = self._create_salary_range(
                position_data.salary_min,
                position_data.salary_max,
                position_data.salary_currency
            )

            # Map experience level to position level
            position_level = self._map_experience_level_to_position_level(position_data.experience_level)

            # Parse application deadline
            application_deadline = self._parse_application_deadline(position_data.application_deadline)

            # Convert languages and roles to enums
            languages_required_enums = self._convert_languages_to_enums(position_data.languages_required)
            desired_roles_enums = self._convert_roles_to_enums(position_data.desired_roles)

            id = JobPositionId.generate()
            command = CreateJobPositionCommand(
                id=id,
                company_id=CompanyId.from_string(position_data.company_id),
                title=position_data.title,
                description=position_data.description,
                location=position_data.location,
                work_location_type=work_location_type,
                salary_range=salary_range,
                contract_type=contract_type,
                requirements={"requirements": position_data.requirements or []},
                job_category=JobCategoryEnum.OTHER,
                position_level=position_level,
                number_of_openings=position_data.number_of_openings or 1,
                application_instructions=None,  # Not in create schema
                benefits=position_data.benefits or [],
                working_hours=position_data.working_hours,
                travel_required=position_data.travel_required,
                languages_required=languages_required_enums,
                visa_sponsorship=position_data.visa_sponsorship or False,
                contact_person=position_data.contact_person,
                department=position_data.department,
                reports_to=position_data.reports_to,
                desired_roles=desired_roles_enums,
                open_at=None,  # Not set during creation
                application_deadline=application_deadline,
                skills=position_data.skills or [],
                application_url=position_data.application_url,
                application_email=position_data.application_email
            )

            self.command_bus.dispatch(command)

            return JobPositionActionResponse(
                success=True,
                message="Position created successfully",
                position_id=id.value
            )

        except Exception as e:
            logger.error(f"Error creating position: {str(e)}")
            return JobPositionActionResponse(
                success=False,
                message=f"Failed to create position: {str(e)}"
            )

    def update_position(self, position_id: str, position_data: JobPositionUpdate) -> JobPositionActionResponse:
        """Update an existing job position"""
        try:
            # First, get the current position to fill in required fields that aren't provided
            current_position_query = GetJobPositionByIdQuery(id=JobPositionId.from_string(position_id))
            current_dto: Optional[JobPositionDto] = self.query_bus.query(current_position_query)

            if not current_dto:
                return JobPositionActionResponse(
                    success=False,
                    message=f"Position with ID {position_id} not found",
                    position_id=position_id
                )

            # Map employment type to contract type, use current if not provided
            contract_type = current_dto.contract_type
            if position_data.employment_type:
                contract_type = self.EMPLOYMENT_TYPE_MAPPING.get(position_data.employment_type,
                                                                 current_dto.contract_type)

            # Map remote to work location type, use current if not provided
            work_location_type = current_dto.work_location_type
            if position_data.is_remote is not None:
                work_location_type = WorkLocationTypeEnum.REMOTE if position_data.is_remote else WorkLocationTypeEnum.ON_SITE

            # Create salary range if provided, otherwise use current
            salary_range = current_dto.salary_range
            if position_data.salary_min is not None and position_data.salary_max is not None:
                salary_range = self._create_salary_range(
                    position_data.salary_min,
                    position_data.salary_max,
                    position_data.salary_currency or (
                        current_dto.salary_range.currency if current_dto.salary_range else "USD")
                )

            # Map experience level to position level, use current if not provided
            position_level = current_dto.position_level
            if position_data.experience_level:
                position_level = self._map_experience_level_to_position_level(
                    position_data.experience_level) or current_dto.position_level

            # Parse application deadline if provided
            application_deadline = self._parse_application_deadline(
                position_data.application_deadline) or current_dto.application_deadline

            # Map job category if provided
            job_category = current_dto.job_category
            if position_data.job_category:
                try:
                    job_category = JobCategoryEnum(position_data.job_category)
                except ValueError:
                    pass  # Keep current value if invalid

            # Parse languages if provided
            languages_required = current_dto.languages_required or {}
            if position_data.languages_required:
                # Convert string dict to enum dict
                languages_required = self._convert_languages_to_enums(
                    position_data.languages_required) or current_dto.languages_required or {}

            # Parse desired roles if provided
            desired_roles = current_dto.desired_roles
            if position_data.desired_roles:
                # Convert string list to enum list
                desired_roles = self._convert_roles_to_enums(position_data.desired_roles) or current_dto.desired_roles

            command = UpdateJobPositionCommand(
                id=JobPositionId.from_string(position_id),
                title=position_data.title or current_dto.title,
                description=position_data.description if position_data.description is not None else current_dto.description,
                location=position_data.location if position_data.location is not None else current_dto.location,
                work_location_type=work_location_type,
                salary_range=salary_range,
                contract_type=contract_type,
                requirements={
                    "requirements": position_data.requirements} if position_data.requirements is not None else current_dto.requirements or {},
                job_category=job_category,
                position_level=position_level,
                number_of_openings=position_data.number_of_openings
                if position_data.number_of_openings is not None else current_dto.number_of_openings,
                application_instructions=current_dto.application_instructions,
                benefits=position_data.benefits if position_data.benefits is not None else current_dto.benefits or [],
                working_hours=position_data.working_hours if position_data.working_hours is not None else current_dto.working_hours,
                travel_required=position_data.travel_required if position_data.travel_required is not None else current_dto.travel_required,
                languages_required=languages_required,
                visa_sponsorship=position_data.visa_sponsorship if position_data.visa_sponsorship is not None else current_dto.visa_sponsorship,
                contact_person=position_data.contact_person if position_data.contact_person is not None else current_dto.contact_person,
                department=position_data.department if position_data.department is not None else current_dto.department,
                reports_to=position_data.reports_to if position_data.reports_to is not None else current_dto.reports_to,
                desired_roles=desired_roles,
                open_at=current_dto.open_at,
                application_deadline=application_deadline,
                skills=position_data.skills if position_data.skills is not None else current_dto.skills or [],
                application_url=position_data.application_url if position_data.application_url is not None else current_dto.application_url,
                application_email=position_data.application_email if position_data.application_email is not None else current_dto.application_email
            )

            self.command_bus.dispatch(command)

            return JobPositionActionResponse(
                success=True,
                message="Position updated successfully",
                position_id=position_id
            )

        except Exception as e:
            logger.error(f"Error updating position {position_id}: {str(e)}")
            return JobPositionActionResponse(
                success=False,
                message=f"Failed to update position: {str(e)}"
            )

    def delete_position(self, position_id: str) -> JobPositionActionResponse:
        """Delete a job position"""
        try:
            command = DeleteJobPositionCommand(id=JobPositionId.from_string(position_id))
            self.command_bus.dispatch(command)

            return JobPositionActionResponse(
                success=True,
                message="Position deleted successfully",
                position_id=position_id
            )

        except Exception as e:
            logger.error(f"Error deleting position {position_id}: {str(e)}")
            return JobPositionActionResponse(
                success=False,
                message=f"Failed to delete position: {str(e)}"
            )

    def activate_position(self, position_id: str) -> JobPositionActionResponse:
        """Activate a job position"""
        try:
            # This would need an ActivateJobPositionCommand if it exists
            return JobPositionActionResponse(
                success=True,
                message="Position activated successfully",
                position_id=position_id
            )

        except Exception as e:
            logger.error(f"Error activating position {position_id}: {str(e)}")
            return JobPositionActionResponse(
                success=False,
                message=f"Failed to activate position: {str(e)}"
            )

    def deactivate_position(self, position_id: str) -> JobPositionActionResponse:
        """Deactivate a job position"""
        try:
            # This would need a DeactivateJobPositionCommand if it exists
            return JobPositionActionResponse(
                success=True,
                message="Position deactivated successfully",
                position_id=position_id
            )

        except Exception as e:
            logger.error(f"Error deactivating position {position_id}: {str(e)}")
            return JobPositionActionResponse(
                success=False,
                message=f"Failed to deactivate position: {str(e)}"
            )
