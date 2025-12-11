from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, List, Union, Any

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from core.database import DatabaseInterface
from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.company.domain.value_objects.company_user_id import CompanyUserId
from src.company_bc.job_position.domain.entities.job_position import JobPosition
from src.company_bc.job_position.domain.enums import (
    JobPositionStatusEnum,
    JobPositionVisibilityEnum,
    EmploymentTypeEnum,
    ExperienceLevelEnum,
    WorkLocationTypeEnum,
    ClosedReasonEnum,
    SalaryPeriodEnum,
)
from src.company_bc.job_position.domain.repositories.job_position_repository_interface import \
    JobPositionRepositoryInterface
from src.company_bc.job_position.domain.value_objects import JobPositionId
from src.company_bc.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.company_bc.job_position.domain.value_objects.stage_id import StageId
from src.company_bc.job_position.domain.value_objects.language_requirement import LanguageRequirement
from src.company_bc.job_position.domain.value_objects.custom_field_definition import CustomFieldDefinition
from src.company_bc.job_position.infrastructure.models.job_position_model import JobPositionModel
from src.framework.domain.enums.job_category import JobCategoryEnum
from src.framework.infrastructure.helpers.mixed_helper import MixedHelper
from src.shared_bc.customization.workflow.domain.enums.workflow_stage_type_enum import WorkflowStageTypeEnum
from src.shared_bc.customization.workflow.infrastructure.models import WorkflowStageModel


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

    def find_published(self, company_id: CompanyId) -> List[JobPosition]:
        with self.database.get_session() as session:
            query = session.query(JobPositionModel).join(
                WorkflowStageModel, WorkflowStageModel.id == JobPositionModel.stage_id
            )
            query = query.filter(
                WorkflowStageModel.stage_type == WorkflowStageTypeEnum.SUCCESS.value
            )
            query = query.filter(JobPositionModel.company_id == company_id.value)
            job_position_models = query.all()
            return [self._create_entity_from_model(model) for model in job_position_models]

    def _build_base_query(self, session: Session, company_id: Optional[str] = None,
                          status: Optional[Union[JobPositionStatusEnum, List[JobPositionStatusEnum]]] = None,
                          job_category: Optional[JobCategoryEnum] = None,
                          search_term: Optional[str] = None,
                          visibility: Optional[JobPositionVisibilityEnum] = None) -> Any:
        """Build base query with filters (without pagination)"""
        query = session.query(JobPositionModel)

        # Apply filters
        if company_id:
            query = query.filter(JobPositionModel.company_id == company_id)

        # TODO: Filtering by status now requires access to workflow repository
        # to get the stage's status_mapping. This will be implemented in Phase 3.
        # if status:
        #     # Filter by status would require joining with workflow_stages table
        #     # or filtering by stage_id and checking stage.status_mapping
        #     pass

        if job_category:
            query = query.filter(JobPositionModel.job_category == job_category)

        if search_term:
            query = query.filter(
                or_(
                    JobPositionModel.title.ilike(f"%{search_term}%"),
                    JobPositionModel.description.ilike(f"%{search_term}%")
                )
            )

        # Filter by visibility
        if visibility is not None:
            query = query.filter(JobPositionModel.visibility == visibility)

        return query

    def find_by_filters(self, company_id: Optional[str] = None,
                        status: Optional[Union[JobPositionStatusEnum, List[JobPositionStatusEnum]]] = None,
                        job_category: Optional[JobCategoryEnum] = None,
                        search_term: Optional[str] = None,
                        limit: int = 50, offset: int = 0,
                        visibility: Optional[JobPositionVisibilityEnum] = None) -> List[JobPosition]:
        """Find job positions by filters

        Args:
            status: Single status or list of statuses to filter by
        """
        with self.database.get_session() as session:
            query = self._build_base_query(session, company_id, status, job_category, search_term, visibility)

            # Order by created_at desc (before pagination)
            query = query.order_by(JobPositionModel.created_at.desc())

            # Apply pagination
            query = query.offset(offset).limit(limit)

            job_position_models = query.all()
            return [self._create_entity_from_model(model) for model in job_position_models]

    def count_by_status(self, status: JobPositionStatusEnum) -> int:
        """
        Count job positions by status.

        TODO: This now requires access to workflow repository to check stage.status_mapping.
        This will be implemented in Phase 3 when we have workflow repository access.
        """
        # For now, return 0 as status is no longer a direct field
        # This will be properly implemented in Phase 3
        return 0

    def count_total(self) -> int:
        """Count total job positions"""
        with self.database.get_session() as session:
            return MixedHelper.get_int(session.query(JobPositionModel).count())

    def count_recent(self, days: int = 30) -> int:
        """Count job positions created in the last N days"""
        since_date = datetime.utcnow() - timedelta(days=days)
        with self.database.get_session() as session:
            return MixedHelper.get_int(session.query(JobPositionModel).filter(
                JobPositionModel.created_at >= since_date
            ).count())

    def find_by_public_slug(self, public_slug: str) -> Optional[JobPosition]:
        """Phase 10: Find job position by public slug"""
        with self.database.get_session() as session:
            job_position_model = session.query(JobPositionModel).filter(
                JobPositionModel.public_slug == public_slug
            ).first()

            if not job_position_model:
                return None

            return self._create_entity_from_model(job_position_model)

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
        # Convert job_position_workflow_id and stage_id to Value Objects
        job_position_workflow_id = None
        if model.job_position_workflow_id:
            job_position_workflow_id = JobPositionWorkflowId.from_string(model.job_position_workflow_id)

        stage_id = None
        if model.stage_id:
            stage_id = StageId.from_string(model.stage_id)

        # Convert visibility - handle migration from is_public if needed
        if hasattr(model, 'visibility') and model.visibility:
            visibility = JobPositionVisibilityEnum(model.visibility.lower()) if isinstance(model.visibility,
                                                                                           str) else model.visibility
        else:
            visibility = JobPositionVisibilityEnum.HIDDEN

        # Convert enum fields from string to enum
        employment_type = None
        if model.employment_type:
            try:
                employment_type = EmploymentTypeEnum(model.employment_type)
            except ValueError:
                employment_type = None

        experience_level = None
        if model.experience_level:
            try:
                experience_level = ExperienceLevelEnum(model.experience_level)
            except ValueError:
                experience_level = None

        work_location_type = None
        if model.work_location_type:
            try:
                work_location_type = WorkLocationTypeEnum(model.work_location_type)
            except ValueError:
                work_location_type = None

        salary_period = None
        if model.salary_period:
            try:
                salary_period = SalaryPeriodEnum(model.salary_period)
            except ValueError:
                salary_period = None

        status = JobPositionStatusEnum.DRAFT
        if model.status:
            try:
                status = JobPositionStatusEnum(model.status)
            except ValueError:
                status = JobPositionStatusEnum.DRAFT

        closed_reason = None
        if model.closed_reason:
            try:
                closed_reason = ClosedReasonEnum(model.closed_reason)
            except ValueError:
                closed_reason = None

        # Convert CompanyUserId fields
        financial_approver_id = CompanyUserId.from_string(model.financial_approver_id) if model.financial_approver_id else None
        hiring_manager_id = CompanyUserId.from_string(model.hiring_manager_id) if model.hiring_manager_id else None
        recruiter_id = CompanyUserId.from_string(model.recruiter_id) if model.recruiter_id else None
        created_by_id = CompanyUserId.from_string(model.created_by_id) if model.created_by_id else None

        # Convert languages from JSON to LanguageRequirement list
        languages = []
        if model.languages:
            languages = LanguageRequirement.from_list(model.languages)

        # Convert custom_fields_config from JSON to CustomFieldDefinition list
        custom_fields_config = []
        if model.custom_fields_config:
            custom_fields_config = CustomFieldDefinition.from_list(model.custom_fields_config)

        return JobPosition._from_repository(
            id=JobPositionId.from_string(model.id),
            title=model.title,
            company_id=CompanyId.from_string(model.company_id),
            # Workflow system
            job_position_workflow_id=job_position_workflow_id,
            phase_workflows=model.phase_workflows or {},
            stage_id=stage_id,
            stage_assignments=model.stage_assignments or {},
            # Content fields
            description=model.description,
            job_category=model.job_category,
            skills=model.skills or [],
            languages=languages,
            # Standard fields
            department_id=model.department_id,
            employment_type=employment_type,
            experience_level=experience_level,
            work_location_type=work_location_type,
            office_locations=model.office_locations or [],
            remote_restrictions=model.remote_restrictions,
            number_of_openings=model.number_of_openings or 1,
            requisition_id=model.requisition_id,
            # Financial fields
            salary_currency=model.salary_currency,
            salary_min=model.salary_min,
            salary_max=model.salary_max,
            salary_period=salary_period,
            show_salary=model.show_salary if model.show_salary is not None else False,
            budget_max=model.budget_max,
            approved_budget_max=model.approved_budget_max,
            financial_approver_id=financial_approver_id,
            approved_at=model.approved_at,
            # Ownership fields
            hiring_manager_id=hiring_manager_id,
            recruiter_id=recruiter_id,
            created_by_id=created_by_id,
            # Lifecycle fields
            status=status,
            closed_reason=closed_reason,
            closed_at=model.closed_at,
            published_at=model.published_at,
            # Custom fields
            custom_fields_config=custom_fields_config,
            custom_fields_values=model.custom_fields_values or {},
            source_workflow_id=model.source_workflow_id,
            # Pipeline and screening
            candidate_pipeline_id=model.candidate_pipeline_id,
            screening_template_id=model.screening_template_id,
            killer_questions=model.killer_questions or [],
            # Visibility and publishing
            visibility=visibility,
            public_slug=model.public_slug,
            open_at=model.open_at,
            application_deadline=model.application_deadline,
            # Timestamps
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _create_model_from_entity(self, job_position: JobPosition) -> JobPositionModel:
        """Create JobPositionModel from JobPosition entity"""
        # Ensure visibility is converted to string value (lowercase)
        visibility_value = job_position.visibility.value if isinstance(job_position.visibility,
                                                                       JobPositionVisibilityEnum) else str(
            job_position.visibility).lower()

        # Convert languages to JSON-serializable format
        languages_data = LanguageRequirement.to_list(job_position.languages) if job_position.languages else []

        # Convert custom_fields_config to JSON-serializable format
        config_data = CustomFieldDefinition.to_list(job_position.custom_fields_config) if job_position.custom_fields_config else []

        return JobPositionModel(
            id=job_position.id.value,
            company_id=job_position.company_id.value,
            title=job_position.title,
            # Workflow system
            job_position_workflow_id=str(job_position.job_position_workflow_id) if job_position.job_position_workflow_id else None,
            phase_workflows=job_position.phase_workflows or {},
            stage_id=str(job_position.stage_id) if job_position.stage_id else None,
            stage_assignments=job_position.stage_assignments or {},
            # Content fields
            description=job_position.description,
            job_category=job_position.job_category,
            skills=job_position.skills or [],
            languages=languages_data,
            # Standard fields
            department_id=job_position.department_id,
            employment_type=job_position.employment_type.value if job_position.employment_type else None,
            experience_level=job_position.experience_level.value if job_position.experience_level else None,
            work_location_type=job_position.work_location_type.value if job_position.work_location_type else None,
            office_locations=job_position.office_locations or [],
            remote_restrictions=job_position.remote_restrictions,
            number_of_openings=job_position.number_of_openings,
            requisition_id=job_position.requisition_id,
            # Financial fields
            salary_currency=job_position.salary_currency,
            salary_min=job_position.salary_min,
            salary_max=job_position.salary_max,
            salary_period=job_position.salary_period.value if job_position.salary_period else None,
            show_salary=job_position.show_salary,
            budget_max=job_position.budget_max,
            approved_budget_max=job_position.approved_budget_max,
            financial_approver_id=job_position.financial_approver_id.value if job_position.financial_approver_id else None,
            approved_at=job_position.approved_at,
            # Ownership fields
            hiring_manager_id=job_position.hiring_manager_id.value if job_position.hiring_manager_id else None,
            recruiter_id=job_position.recruiter_id.value if job_position.recruiter_id else None,
            created_by_id=job_position.created_by_id.value if job_position.created_by_id else None,
            # Lifecycle fields
            status=job_position.status.value if job_position.status else JobPositionStatusEnum.DRAFT.value,
            closed_reason=job_position.closed_reason.value if job_position.closed_reason else None,
            closed_at=job_position.closed_at,
            published_at=job_position.published_at,
            # Custom fields
            custom_fields_config=config_data,
            custom_fields_values=job_position.custom_fields_values or {},
            source_workflow_id=job_position.source_workflow_id,
            # Pipeline and screening
            candidate_pipeline_id=job_position.candidate_pipeline_id,
            screening_template_id=job_position.screening_template_id,
            killer_questions=job_position.killer_questions or [],
            # Visibility and publishing
            visibility=visibility_value,
            public_slug=job_position.public_slug,
            open_at=job_position.open_at,
            application_deadline=job_position.application_deadline,
            # Timestamps
            created_at=job_position.created_at or datetime.utcnow(),
            updated_at=job_position.updated_at or datetime.utcnow()
        )

    def _update_model_from_entity(self, model: JobPositionModel, job_position: JobPosition) -> None:
        """Update JobPositionModel with JobPosition entity data"""
        # Ensure visibility is converted to string value (lowercase)
        visibility_value = job_position.visibility.value if isinstance(job_position.visibility,
                                                                       JobPositionVisibilityEnum) else str(
            job_position.visibility).lower()

        # Convert languages to JSON-serializable format
        languages_data = LanguageRequirement.to_list(job_position.languages) if job_position.languages else []

        # Convert custom_fields_config to JSON-serializable format
        config_data = CustomFieldDefinition.to_list(job_position.custom_fields_config) if job_position.custom_fields_config else []

        # Core fields
        model.title = job_position.title

        # Workflow system
        model.job_position_workflow_id = str(job_position.job_position_workflow_id) if job_position.job_position_workflow_id else None
        model.phase_workflows = job_position.phase_workflows or {}
        model.stage_id = str(job_position.stage_id) if job_position.stage_id else None
        model.stage_assignments = job_position.stage_assignments or {}

        # Content fields
        model.description = job_position.description
        model.job_category = job_position.job_category
        model.skills = job_position.skills or []
        model.languages = languages_data

        # Standard fields
        model.department_id = job_position.department_id
        model.employment_type = job_position.employment_type.value if job_position.employment_type else None
        model.experience_level = job_position.experience_level.value if job_position.experience_level else None
        model.work_location_type = job_position.work_location_type.value if job_position.work_location_type else None
        model.office_locations = job_position.office_locations or []
        model.remote_restrictions = job_position.remote_restrictions
        model.number_of_openings = job_position.number_of_openings
        model.requisition_id = job_position.requisition_id

        # Financial fields
        model.salary_currency = job_position.salary_currency
        model.salary_min = job_position.salary_min
        model.salary_max = job_position.salary_max
        model.salary_period = job_position.salary_period.value if job_position.salary_period else None
        model.show_salary = job_position.show_salary
        model.budget_max = job_position.budget_max
        model.approved_budget_max = job_position.approved_budget_max
        model.financial_approver_id = job_position.financial_approver_id.value if job_position.financial_approver_id else None
        model.approved_at = job_position.approved_at

        # Ownership fields
        model.hiring_manager_id = job_position.hiring_manager_id.value if job_position.hiring_manager_id else None
        model.recruiter_id = job_position.recruiter_id.value if job_position.recruiter_id else None
        model.created_by_id = job_position.created_by_id.value if job_position.created_by_id else None

        # Lifecycle fields
        model.status = job_position.status.value if job_position.status else JobPositionStatusEnum.DRAFT.value
        model.closed_reason = job_position.closed_reason.value if job_position.closed_reason else None
        model.closed_at = job_position.closed_at
        model.published_at = job_position.published_at

        # Custom fields
        model.custom_fields_config = config_data
        model.custom_fields_values = job_position.custom_fields_values or {}
        model.source_workflow_id = job_position.source_workflow_id

        # Pipeline and screening
        model.candidate_pipeline_id = job_position.candidate_pipeline_id
        model.screening_template_id = job_position.screening_template_id
        model.killer_questions = job_position.killer_questions or []

        # Visibility and publishing
        model.visibility = visibility_value
        model.public_slug = job_position.public_slug
        model.open_at = job_position.open_at
        model.application_deadline = job_position.application_deadline

        # Timestamps
        model.updated_at = job_position.updated_at or datetime.utcnow()
