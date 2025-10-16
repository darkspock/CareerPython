"""Job position mapper for converting DTOs to response schemas"""
from typing import Optional

from src.job_position.application.queries.job_position_dto import JobPositionDto
from presentation.admin.schemas.job_position import JobPositionResponse


class JobPositionMapper:
    """Mapper for converting JobPosition DTOs to response schemas"""

    @staticmethod
    def dto_to_response(dto: JobPositionDto, company_name: Optional[str] = None) -> JobPositionResponse:
        """Convert JobPositionDto to JobPositionResponse"""
        # Convert salary_range
        salary_range_dict = None
        if dto.salary_range:
            salary_range_dict = {
                "min_amount": dto.salary_range.min_salary,
                "max_amount": dto.salary_range.max_salary,
                "currency": dto.salary_range.currency
            }

        # Convert languages_required
        languages_dict = {}
        if dto.languages_required:
            languages_dict = {
                lang.value: level.value
                for lang, level in dto.languages_required.items()
            }

        # Convert desired_roles
        desired_roles_list = None
        if dto.desired_roles:
            desired_roles_list = [role.value for role in dto.desired_roles]

        return JobPositionResponse(
            id=dto.id.value,
            company_id=dto.company_id.value,
            company_name=company_name,
            title=dto.title,
            description=dto.description,
            location=dto.location,
            employment_type=dto.employment_type,
            work_location_type=dto.work_location_type,
            salary_range=salary_range_dict,
            contract_type=dto.contract_type,
            requirements=dto.requirements,
            job_category=dto.job_category,
            position_level=dto.position_level,
            number_of_openings=dto.number_of_openings,
            application_instructions=dto.application_instructions,
            benefits=dto.benefits or [],
            working_hours=dto.working_hours,
            travel_required=dto.travel_required,
            languages_required=languages_dict,
            visa_sponsorship=dto.visa_sponsorship,
            contact_person=dto.contact_person,
            department=dto.department,
            reports_to=dto.reports_to,
            status=dto.status,
            desired_roles=desired_roles_list,
            open_at=dto.open_at,
            application_deadline=dto.application_deadline,
            skills=dto.skills or [],
            application_url=dto.application_url,
            application_email=dto.application_email,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    @staticmethod
    def _contract_type_to_employment_type(contract_type: str) -> str:
        """Map contract type to employment type"""
        mapping = {
            "full_time": "full_time",
            "part_time": "part_time",
            "contract": "contract",
            "internship": "internship"
        }
        return mapping.get(contract_type, "full_time")

    @staticmethod
    def _position_level_to_experience_level(position_level: Optional[str]) -> Optional[str]:
        """Map position level to experience level"""
        if not position_level:
            return None

        mapping = {
            "junior": "junior",
            "mid": "mid",
            "senior": "senior",
            "lead": "lead"
        }
        return mapping.get(position_level.lower())
