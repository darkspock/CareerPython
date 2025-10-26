from datetime import datetime, timedelta
from typing import Optional, List

from sqlalchemy import and_, or_

from core.database import DatabaseInterface
from src.candidate.domain.enums.candidate_enums import LanguageEnum, LanguageLevelEnum, PositionRoleEnum
from src.company.domain.value_objects.company_id import CompanyId
from src.job_position.domain.entities.job_position import JobPosition
from src.job_position.domain.enums import JobPositionStatusEnum, WorkLocationTypeEnum, ContractTypeEnum
from src.job_position.domain.repositories.job_position_repository_interface import JobPositionRepositoryInterface
from src.job_position.domain.value_objects import JobPositionId
from src.job_position.domain.value_objects.salary_range import SalaryRange
from src.job_position.infrastructure.models.job_position_model import JobPositionModel
from src.shared.domain.enums.job_category import JobCategoryEnum


class JobPositionRepository(JobPositionRepositoryInterface):
    def __init__(self, database: DatabaseInterface):
        self.database = database

    def save(self, job_position: JobPosition) -> JobPosition:
        """Save or update job position"""
        with self.database.get_session() as session:
            job_position_model = session.query(JobPositionModel).filter(
                JobPositionModel.id == job_position.id.value
            ).first()

            if job_position_model:
                # Update existing
                self._update_model_from_entity(job_position_model, job_position)
            else:
                # Create new
                job_position_model = self._create_model_from_entity(job_position)
                session.add(job_position_model)

            session.commit()
            session.refresh(job_position_model)

            return self._create_entity_from_model(job_position_model)

    def get_by_id(self, id: JobPositionId) -> Optional[JobPosition]:
        """Get job position by ID"""
        with self.database.get_session() as session:
            job_position_model = session.query(JobPositionModel).filter(
                JobPositionModel.id == id.value
            ).first()

            if not job_position_model:
                return None

            return self._create_entity_from_model(job_position_model)

    def find_by_filters(self, company_id: Optional[str] = None,
                        status: Optional[JobPositionStatusEnum] = None,
                        job_category: Optional[JobCategoryEnum] = None,
                        work_location_type: Optional[WorkLocationTypeEnum] = None,
                        contract_type: Optional[ContractTypeEnum] = None,
                        location: Optional[str] = None,
                        search_term: Optional[str] = None,
                        limit: int = 50, offset: int = 0) -> List[JobPosition]:
        """Find job positions by filters"""
        with self.database.get_session() as session:
            query = session.query(JobPositionModel)

            # Apply filters
            if company_id:
                query = query.filter(JobPositionModel.company_id == company_id)

            if status:
                query = query.filter(JobPositionModel.status == status)

            if job_category:
                query = query.filter(JobPositionModel.job_category == job_category)

            if work_location_type:
                query = query.filter(JobPositionModel.work_location_type == work_location_type)

            if contract_type:
                query = query.filter(JobPositionModel.contract_type == contract_type)

            if location:
                query = query.filter(JobPositionModel.location.ilike(f"%{location}%"))

            if search_term:
                query = query.filter(
                    or_(
                        JobPositionModel.title.ilike(f"%{search_term}%"),
                        JobPositionModel.description.ilike(f"%{search_term}%"),
                        JobPositionModel.location.ilike(f"%{search_term}%")
                    )
                )

            # Order by created_at desc (before pagination)
            query = query.order_by(JobPositionModel.created_at.desc())

            # Apply pagination
            query = query.offset(offset).limit(limit)

            job_position_models = query.all()
            return [self._create_entity_from_model(model) for model in job_position_models]

    def count_by_status(self, status: JobPositionStatusEnum) -> int:
        """Count job positions by status"""
        with self.database.get_session() as session:
            return session.query(JobPositionModel).filter(
                JobPositionModel.status == status
            ).count()

    def count_total(self) -> int:
        """Count total job positions"""
        with self.database.get_session() as session:
            return session.query(JobPositionModel).count()

    def count_recent(self, days: int = 30) -> int:
        """Count job positions created in the last N days"""
        since_date = datetime.utcnow() - timedelta(days=days)
        with self.database.get_session() as session:
            return session.query(JobPositionModel).filter(
                JobPositionModel.created_at >= since_date
            ).count()

    def count_active_by_company_id(self, company_id: str) -> int:
        """Count active job positions by company ID"""
        active_statuses = [JobPositionStatusEnum.OPEN, JobPositionStatusEnum.APPROVED]
        with self.database.get_session() as session:
            return session.query(JobPositionModel).filter(
                and_(
                    JobPositionModel.company_id == company_id,
                    JobPositionModel.status.in_(active_statuses)
                )
            ).count()

    def delete(self, id: JobPositionId) -> bool:
        """Delete job position"""
        with self.database.get_session() as session:
            job_position_model = session.query(JobPositionModel).filter(
                JobPositionModel.id == id.value
            ).first()

            if not job_position_model:
                return False

            session.delete(job_position_model)
            session.commit()
            return True

    def _create_entity_from_model(self, model: JobPositionModel) -> JobPosition:
        """Convert JobPositionModel to JobPosition entity"""
        # Convert salary_range JSON to SalaryRange object
        salary_range = None
        if model.salary_range:
            salary_range = SalaryRange(
                min_salary=model.salary_range.get('min_salary'),
                max_salary=model.salary_range.get('max_salary'),
                currency=model.salary_range.get('currency', 'USD')
            )

        # Convert languages_required JSON to proper dict
        languages_required = {}
        if model.languages_required:
            # Convert string keys to LanguageEnum and string values to LanguageLevelEnum
            for lang_str, level_str in model.languages_required.items():
                try:
                    lang_enum = LanguageEnum(lang_str)
                    level_enum = LanguageLevelEnum(level_str)
                    languages_required[lang_enum] = level_enum
                except ValueError:
                    # Skip invalid enum values
                    continue

        # Convert desired_roles JSON to proper list
        desired_roles = None
        if model.desired_roles:
            desired_roles = []
            for role_str in model.desired_roles:
                try:
                    role_enum = PositionRoleEnum(role_str)
                    desired_roles.append(role_enum)
                except ValueError:
                    # Skip invalid enum values
                    continue

        return JobPosition._from_repository(
            id=JobPositionId.from_string(model.id),
            title=model.title,
            company_id=CompanyId.from_string(model.company_id),
            workflow_id=model.workflow_id,
            description=model.description,
            location=model.location,
            employment_type=model.employment_type,
            work_location_type=model.work_location_type,
            salary_range=salary_range,
            contract_type=model.contract_type,
            requirements=model.requirements or {},
            job_category=model.job_category,
            position_level=model.position_level,
            number_of_openings=model.number_of_openings,
            application_instructions=model.application_instructions,
            benefits=model.benefits or [],
            working_hours=model.working_hours,
            travel_required=model.travel_required,
            languages_required=languages_required,
            visa_sponsorship=model.visa_sponsorship,
            contact_person=model.contact_person,
            department=model.department,
            reports_to=model.reports_to,
            status=model.status,
            desired_roles=desired_roles,
            open_at=model.open_at,
            application_deadline=model.application_deadline,
            skills=model.skills or [],
            application_url=model.application_url,
            application_email=model.application_email,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _create_model_from_entity(self, job_position: JobPosition) -> JobPositionModel:
        """Create JobPositionModel from JobPosition entity"""
        # Convert SalaryRange to JSON
        salary_range_json = None
        if job_position.salary_range:
            salary_range_json = {
                'min_salary': job_position.salary_range.min_salary,
                'max_salary': job_position.salary_range.max_salary,
                'currency': job_position.salary_range.currency
            }

        # Convert languages_required to JSON-serializable dict
        languages_required_json = None
        if job_position.languages_required:
            languages_required_json = {
                lang.value: level.value
                for lang, level in job_position.languages_required.items()
            }

        # Convert desired_roles to JSON-serializable list
        desired_roles_json = None
        if job_position.desired_roles:
            desired_roles_json = [role.value for role in job_position.desired_roles]

        return JobPositionModel(
            id=job_position.id.value,
            company_id=job_position.company_id.value,
            workflow_id=job_position.workflow_id,
            title=job_position.title,
            description=job_position.description,
            location=job_position.location,
            employment_type=job_position.employment_type,
            work_location_type=job_position.work_location_type,
            salary_range=salary_range_json,
            contract_type=job_position.contract_type,
            requirements=job_position.requirements,
            job_category=job_position.job_category,
            position_level=job_position.position_level,
            number_of_openings=job_position.number_of_openings,
            application_instructions=job_position.application_instructions,
            benefits=job_position.benefits,
            working_hours=job_position.working_hours,
            travel_required=job_position.travel_required,
            languages_required=languages_required_json,
            visa_sponsorship=job_position.visa_sponsorship,
            contact_person=job_position.contact_person,
            department=job_position.department,
            reports_to=job_position.reports_to,
            desired_roles=desired_roles_json,
            open_at=job_position.open_at,
            application_deadline=job_position.application_deadline,
            skills=job_position.skills,
            application_url=job_position.application_url,
            application_email=job_position.application_email,
            status=job_position.status,
            created_at=job_position.created_at or datetime.utcnow(),
            updated_at=job_position.updated_at or datetime.utcnow()
        )

    def _update_model_from_entity(self, model: JobPositionModel, job_position: JobPosition) -> None:
        """Update JobPositionModel with JobPosition entity data"""
        # Convert SalaryRange to JSON
        salary_range_json = None
        if job_position.salary_range:
            salary_range_json = {
                'min_salary': job_position.salary_range.min_salary,
                'max_salary': job_position.salary_range.max_salary,
                'currency': job_position.salary_range.currency
            }

        # Convert languages_required to JSON-serializable dict
        languages_required_json = None
        if job_position.languages_required:
            languages_required_json = {
                lang.value: level.value
                for lang, level in job_position.languages_required.items()
            }

        # Convert desired_roles to JSON-serializable list
        desired_roles_json = None
        if job_position.desired_roles:
            desired_roles_json = [role.value for role in job_position.desired_roles]

        model.workflow_id = job_position.workflow_id
        model.title = job_position.title
        model.description = job_position.description
        model.location = job_position.location
        model.employment_type = job_position.employment_type
        model.work_location_type = job_position.work_location_type
        model.salary_range = salary_range_json
        model.contract_type = job_position.contract_type
        model.requirements = job_position.requirements
        model.job_category = job_position.job_category
        model.position_level = job_position.position_level
        model.number_of_openings = job_position.number_of_openings
        model.application_instructions = job_position.application_instructions
        model.benefits = job_position.benefits
        model.working_hours = job_position.working_hours
        model.travel_required = job_position.travel_required
        model.languages_required = languages_required_json
        model.visa_sponsorship = job_position.visa_sponsorship
        model.contact_person = job_position.contact_person
        model.department = job_position.department
        model.reports_to = job_position.reports_to
        model.desired_roles = desired_roles_json
        model.open_at = job_position.open_at
        model.application_deadline = job_position.application_deadline
        model.skills = job_position.skills
        model.application_url = job_position.application_url
        model.application_email = job_position.application_email
        model.status = job_position.status
        model.updated_at = job_position.updated_at or datetime.utcnow()
