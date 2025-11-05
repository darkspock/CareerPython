from datetime import datetime, timedelta
from typing import Optional, List, Union

from sqlalchemy import and_, or_

from core.database import DatabaseInterface
from src.company.domain.value_objects.company_id import CompanyId
from src.job_position.domain.entities.job_position import JobPosition
from src.job_position.domain.enums import JobPositionStatusEnum, JobPositionVisibilityEnum
from src.job_position.domain.repositories.job_position_repository_interface import JobPositionRepositoryInterface
from src.job_position.domain.value_objects import JobPositionId
from src.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.job_position.domain.value_objects.stage_id import StageId
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
            return session.query(JobPositionModel).count()

    def count_recent(self, days: int = 30) -> int:
        """Count job positions created in the last N days"""
        since_date = datetime.utcnow() - timedelta(days=days)
        with self.database.get_session() as session:
            return session.query(JobPositionModel).filter(
                JobPositionModel.created_at >= since_date
            ).count()

    def count_active_by_company_id(self, company_id: str) -> int:
        """
        Count active job positions by company ID.
        
        TODO: This now requires access to workflow repository to check if stage.status_mapping is ACTIVE.
        This will be properly implemented in Phase 3.
        For now, we count positions that have a workflow and stage assigned.
        """
        with self.database.get_session() as session:
            return session.query(JobPositionModel).filter(
                and_(
                    JobPositionModel.company_id == company_id,
                    JobPositionModel.job_position_workflow_id.isnot(None),
                    JobPositionModel.stage_id.isnot(None)
                )
            ).count()

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
        # Visibility is stored as string value, convert to enum
        if hasattr(model, 'visibility') and model.visibility:
            visibility = JobPositionVisibilityEnum(model.visibility.lower()) if isinstance(model.visibility, str) else model.visibility
        else:
            visibility = JobPositionVisibilityEnum.HIDDEN
        # TODO: Migration logic - if visibility doesn't exist but is_public does, convert it
        # This will be handled in the migration

        return JobPosition._from_repository(
            id=JobPositionId.from_string(model.id),
            title=model.title,
            company_id=CompanyId.from_string(model.company_id),
            job_position_workflow_id=job_position_workflow_id,
            stage_id=stage_id,
            phase_workflows=model.phase_workflows or {},
            custom_fields_values=model.custom_fields_values or {},
            description=model.description,
            job_category=model.job_category,
            open_at=model.open_at,
            application_deadline=model.application_deadline,
            visibility=visibility,
            public_slug=model.public_slug,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _create_model_from_entity(self, job_position: JobPosition) -> JobPositionModel:
        """Create JobPositionModel from JobPosition entity"""
        # Ensure visibility is converted to string value (lowercase)
        visibility_value = job_position.visibility.value if isinstance(job_position.visibility, JobPositionVisibilityEnum) else str(job_position.visibility).lower()
        
        return JobPositionModel(
            id=job_position.id.value,
            company_id=job_position.company_id.value,
            job_position_workflow_id=str(job_position.job_position_workflow_id) if job_position.job_position_workflow_id else None,
            stage_id=str(job_position.stage_id) if job_position.stage_id else None,
            phase_workflows=job_position.phase_workflows or {},
            custom_fields_values=job_position.custom_fields_values or {},
            title=job_position.title,
            description=job_position.description,
            job_category=job_position.job_category,
            open_at=job_position.open_at,
            application_deadline=job_position.application_deadline,
            visibility=visibility_value,
            public_slug=job_position.public_slug,
            created_at=job_position.created_at or datetime.utcnow(),
            updated_at=job_position.updated_at or datetime.utcnow()
        )

    def _update_model_from_entity(self, model: JobPositionModel, job_position: JobPosition) -> None:
        """Update JobPositionModel with JobPosition entity data"""
        model.job_position_workflow_id = str(job_position.job_position_workflow_id) if job_position.job_position_workflow_id else None
        model.stage_id = str(job_position.stage_id) if job_position.stage_id else None
        model.phase_workflows = job_position.phase_workflows or {}
        model.custom_fields_values = job_position.custom_fields_values or {}
        model.title = job_position.title
        model.description = job_position.description
        model.job_category = job_position.job_category
        model.open_at = job_position.open_at
        model.application_deadline = job_position.application_deadline
        # Ensure visibility is converted to string value (lowercase)
        visibility_value = job_position.visibility.value if isinstance(job_position.visibility, JobPositionVisibilityEnum) else str(job_position.visibility).lower()
        model.visibility = visibility_value
        model.public_slug = job_position.public_slug
        model.updated_at = job_position.updated_at or datetime.utcnow()
