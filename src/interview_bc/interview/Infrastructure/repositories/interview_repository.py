"""Interview repository implementation"""
import logging
from datetime import datetime, timedelta
from typing import Optional, List

from sqlalchemy import or_, func
from sqlalchemy.dialects import postgresql

from core.database import DatabaseInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.company_bc.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.company_bc.company.domain import CompanyId
from src.company_bc.company_role.domain.value_objects.company_role_id import CompanyRoleId
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.company_bc.job_position.infrastructure.models import JobPositionModel
from src.framework.infrastructure.helpers.mixed_helper import MixedHelper
from src.framework.infrastructure.repositories.base import BaseRepository
from src.interview_bc.interview.Infrastructure.models.interview_model import InterviewModel
from src.interview_bc.interview.domain.entities.interview import Interview
from src.interview_bc.interview.domain.enums.interview_enums import (
    InterviewStatusEnum,
    InterviewTypeEnum,
    InterviewModeEnum,
    InterviewProcessTypeEnum
)
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface
from src.interview_bc.interview.domain.read_models.interview_list_read_model import InterviewListReadModel
from src.interview_bc.interview.domain.value_objects.interview_id import InterviewId
from src.interview_bc.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId

logger = logging.getLogger(__name__)


class SQLAlchemyInterviewRepository(InterviewRepositoryInterface):
    """SQLAlchemy implementation of Interview repository"""

    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.base_repo = BaseRepository(database, InterviewModel)

    def _to_domain(self, model: InterviewModel) -> Interview:
        """Convert model to domain entity"""
        job_position_id = JobPositionId.from_string(model.job_position_id)

        application_id = None
        if model.application_id:
            application_id = CandidateApplicationId.from_string(model.application_id)

        interview_template_id = None
        if model.interview_template_id:
            interview_template_id = InterviewTemplateId.from_string(model.interview_template_id)

        workflow_stage_id = WorkflowStageId.from_string(model.workflow_stage_id)

        interviewers_list = model.interviewers or []

        # Convert required_roles from List[str] to List[CompanyRoleId]
        required_roles_list = []
        if model.required_roles:
            required_roles_list = [CompanyRoleId.from_string(role_id) for role_id in model.required_roles]
        # Note: required_roles is obligatory, so it should never be None, but we handle empty list

        # Convert string enums to enum objects
        process_type_enum = None
        if model.process_type:
            try:
                process_type_enum = InterviewProcessTypeEnum(model.process_type)
            except ValueError:
                # Handle invalid enum values gracefully
                process_type_enum = None

        interview_type_enum = InterviewTypeEnum.CUSTOM
        if model.interview_type:
            try:
                interview_type_enum = InterviewTypeEnum(model.interview_type)
            except ValueError:
                interview_type_enum = InterviewTypeEnum.CUSTOM

        interview_mode_enum = None
        if model.interview_mode:
            try:
                interview_mode_enum = InterviewModeEnum(model.interview_mode)
            except ValueError:
                interview_mode_enum = None

        # Handle status enum conversion
        # Note: InterviewStatusEnum.ENABLED has value "PENDING", so we need to handle both cases
        status_enum = InterviewStatusEnum.PENDING  # Default
        if model.status:
            status_upper = model.status.upper()
            try:
                # Try direct conversion first (works for "PENDING", "IN_PROGRESS", etc.)
                status_enum = InterviewStatusEnum(model.status)
            except ValueError:
                # Handle legacy or mismatched values
                # Map "ENABLED" to ENABLED enum (which has value "PENDING")
                if status_upper == "ENABLED":
                    status_enum = InterviewStatusEnum.PENDING
                elif status_upper == "DISABLED":
                    status_enum = InterviewStatusEnum.DISCARDED
                elif status_upper == "PENDING":
                    status_enum = InterviewStatusEnum.PENDING  # PENDING maps to ENABLED enum
                else:
                    # Try to find enum member by name
                    try:
                        status_enum = InterviewStatusEnum[status_upper]
                    except (KeyError, ValueError):
                        status_enum = InterviewStatusEnum.PENDING  # Default fallback

        return Interview(
            id=InterviewId.from_string(model.id),
            candidate_id=CandidateId.from_string(model.candidate_id),
            required_roles=required_roles_list,
            process_type=process_type_enum,
            job_position_id=job_position_id,
            application_id=application_id,
            interview_template_id=interview_template_id,
            workflow_stage_id=workflow_stage_id,
            interview_type=interview_type_enum,
            interview_mode=interview_mode_enum,
            status=status_enum,
            title=model.title,
            description=model.description,
            scheduled_at=model.scheduled_at,
            deadline_date=model.deadline_date,
            started_at=model.started_at,
            finished_at=model.finished_at,
            duration_minutes=model.duration_minutes,
            interviewers=interviewers_list,
            interviewer_notes=model.interviewer_notes,
            candidate_notes=model.candidate_notes,
            score=model.score,
            feedback=model.feedback,
            free_answers=model.free_answers,
            link_token=model.link_token,
            link_expires_at=model.link_expires_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, domain: Interview) -> InterviewModel:
        """Convert domain entity to model"""
        job_position_id = domain.job_position_id.value

        application_id = None
        if domain.application_id:
            application_id = domain.application_id.value

        interview_template_id = None
        if domain.interview_template_id:
            interview_template_id = domain.interview_template_id.value

        workflow_stage_id = str(domain.workflow_stage_id)

        # Convert required_roles from List[CompanyRoleId] to List[str]
        # required_roles is obligatory, so it should always have at least one element
        required_roles_list = [role_id.value for role_id in domain.required_roles] if domain.required_roles else []

        # Convert enum objects to strings for storage
        process_type_str = domain.process_type.value if domain.process_type else None
        interview_type_str = domain.interview_type.value if domain.interview_type else InterviewTypeEnum.CUSTOM.value
        interview_mode_str = domain.interview_mode.value if domain.interview_mode else None
        status_str = domain.status.value if domain.status else InterviewStatusEnum.PENDING.value

        return InterviewModel(
            id=domain.id.value,
            candidate_id=domain.candidate_id.value,
            required_roles=required_roles_list,
            process_type=process_type_str,
            job_position_id=job_position_id,
            application_id=application_id,
            interview_template_id=interview_template_id,
            workflow_stage_id=workflow_stage_id,
            interview_type=interview_type_str,
            interview_mode=interview_mode_str,
            status=status_str,
            title=domain.title,
            description=domain.description,
            scheduled_at=domain.scheduled_at,
            deadline_date=domain.deadline_date,
            started_at=domain.started_at,
            finished_at=domain.finished_at,
            duration_minutes=domain.duration_minutes,
            interviewers=domain.interviewers,
            interviewer_notes=domain.interviewer_notes,
            candidate_notes=domain.candidate_notes,
            score=domain.score,
            feedback=domain.feedback,
            free_answers=domain.free_answers,
            link_token=domain.link_token,
            link_expires_at=domain.link_expires_at,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
        )

    def create(self, interview: Interview) -> Interview:
        """Create a new interview"""
        model = self._to_model(interview)
        created_model = self.base_repo.create(model)
        return self._to_domain(created_model)

    def get_by_id(self, interview_id: str) -> Optional[Interview]:
        """Get interview by ID"""
        with self.database.get_session() as session:
            model = session.query(InterviewModel).filter(InterviewModel.id == interview_id).first()
            if model:
                return self._to_domain(model)
            return None

    def update(self, interview: Interview) -> Interview:
        """Update an existing interview"""
        import logging
        logger = logging.getLogger(__name__)

        with self.database.get_session() as session:
            model = session.query(InterviewModel).filter(InterviewModel.id == interview.id.value).first()
            if model:
                logger.debug(
                    f"Updating interview {interview.id.value}. Link token before: {model.link_token}, after: {interview.link_token}")

                # Update all fields from the entity
                model.candidate_id = interview.candidate_id.value
                model.required_roles = [role_id.value for role_id in
                                        interview.required_roles] if interview.required_roles else []
                model.process_type = interview.process_type.value if interview.process_type else None
                model.job_position_id = interview.job_position_id.value
                model.application_id = interview.application_id.value if interview.application_id else None
                model.interview_template_id = interview.interview_template_id.value if interview.interview_template_id else None
                model.workflow_stage_id = interview.workflow_stage_id.value
                model.interview_type = interview.interview_type.value if interview.interview_type else InterviewTypeEnum.CUSTOM.value
                model.interview_mode = interview.interview_mode.value if interview.interview_mode else None
                model.status = interview.status.value if interview.status else InterviewStatusEnum.PENDING.value
                model.title = interview.title
                model.description = interview.description
                model.scheduled_at = interview.scheduled_at
                model.deadline_date = interview.deadline_date
                model.started_at = interview.started_at
                model.finished_at = interview.finished_at
                model.duration_minutes = interview.duration_minutes
                model.interviewers = interview.interviewers
                model.interviewer_notes = interview.interviewer_notes
                model.candidate_notes = interview.candidate_notes
                model.score = interview.score
                model.feedback = interview.feedback
                model.free_answers = interview.free_answers
                model.link_token = interview.link_token
                model.link_expires_at = interview.link_expires_at
                model.updated_at = interview.updated_at or datetime.now()
                # Handle updated_by safely - it may not exist in the entity
                if hasattr(interview, 'updated_by'):
                    model.updated_by = interview.updated_by
                # Keep existing updated_by if entity doesn't have it
                # (don't overwrite with None)

                session.commit()
                session.refresh(model)
                logger.debug(f"Interview {interview.id.value} updated. Link token in DB: {model.link_token}")
                return self._to_domain(model)
            raise ValueError(f"Interview with id {interview.id.value} not found")

    def delete(self, id: InterviewId) -> bool:
        """Delete an interview"""
        return self.base_repo.delete(id)

    def get_by_candidate_id(self, candidate_id: str) -> List[Interview]:
        """Get all interviews for a candidate"""
        with self.database.get_session() as session:
            models = session.query(InterviewModel).filter(
                InterviewModel.candidate_id == candidate_id
            ).order_by(InterviewModel.created_at.desc()).all()
            return [self._to_domain(model) for model in models]

    def get_by_job_position_id(self, job_position_id: str) -> List[Interview]:
        """Get all interviews for a job position"""
        with self.database.get_session() as session:
            models = session.query(InterviewModel).filter(
                InterviewModel.job_position_id == job_position_id
            ).order_by(InterviewModel.created_at.desc()).all()
            return [self._to_domain(model) for model in models]

    def get_by_application_id(self, application_id: str) -> List[Interview]:
        """Get all interviews for a candidate application"""
        with self.database.get_session() as session:
            models = session.query(InterviewModel).filter(
                InterviewModel.application_id == application_id
            ).order_by(InterviewModel.created_at.desc()).all()
            return [self._to_domain(model) for model in models]

    def get_by_status(self, status: InterviewStatusEnum) -> List[Interview]:
        """Get interviews by status"""
        with self.database.get_session() as session:
            models = session.query(InterviewModel).filter(
                InterviewModel.status == status
            ).order_by(InterviewModel.created_at.desc()).all()
            return [self._to_domain(model) for model in models]

    def get_by_interview_type(self, interview_type: InterviewTypeEnum) -> List[Interview]:
        """Get interviews by type"""
        with self.database.get_session() as session:
            models = session.query(InterviewModel).filter(
                InterviewModel.interview_type == interview_type
            ).order_by(InterviewModel.created_at.desc()).all()
            return [self._to_domain(model) for model in models]

    def get_scheduled_interviews(self, from_date: datetime, to_date: datetime) -> List[Interview]:
        """Get scheduled interviews within date range"""
        with self.database.get_session() as session:
            models = session.query(InterviewModel).filter(
                InterviewModel.scheduled_at.between(from_date, to_date)
            ).order_by(InterviewModel.scheduled_at).all()
            return [self._to_domain(model) for model in models]

    def get_interviews_by_candidate_and_job_position(
            self,
            candidate_id: str,
            job_position_id: str
    ) -> List[Interview]:
        """Get interviews for specific candidate and job position"""
        with self.database.get_session() as session:
            models = session.query(InterviewModel).filter(
                InterviewModel.candidate_id == candidate_id,
                InterviewModel.job_position_id == job_position_id
            ).order_by(InterviewModel.created_at.desc()).all()
            return [self._to_domain(model) for model in models]

    def find_finished_recent(self, days: int, company_id: CompanyId) -> List[Interview]:
        now = datetime.utcnow()
        from_date = now - timedelta(days=days)
        statuses = MixedHelper.enum_list_to_string_list(InterviewStatusEnum.finished())
        with self.database.get_session() as session:
            query = session.query(InterviewModel)
            query = query.join(JobPositionModel, InterviewModel.job_position_id == JobPositionModel.id)
            query = query.filter(InterviewModel.status.in_(statuses))
            query = query.order_by(InterviewModel.created_at.desc())
            query = query.filter(InterviewModel.created_at >= from_date)
            query= query.filter(JobPositionModel.company_id == company_id)
            models = query.all()
        return [self._to_domain(model) for model in models]

    def find_not_finished(self, company_id: CompanyId) -> List[Interview]:
        statuses = MixedHelper.enum_list_to_string_list(InterviewStatusEnum.not_finished())

        with self.database.get_session() as session:
            query = session.query(InterviewModel)
            query = query.join(JobPositionModel, InterviewModel.job_position_id == JobPositionModel.id)
            query = query.filter(InterviewModel.status.in_(statuses))
            query = query.order_by(InterviewModel.created_at.desc())
            query = query.filter(JobPositionModel.company_id == company_id)
            models = query.all()
        return [self._to_domain(model) for model in models]

    def find_by_filters(
            self,
            candidate_id: Optional[str] = None,
            candidate_name: Optional[str] = None,
            job_position_id: Optional[str] = None,
            interview_type: Optional[InterviewTypeEnum] = None,
            process_type: Optional[InterviewProcessTypeEnum] = None,
            status: Optional[InterviewStatusEnum] = None,
            required_role_id: Optional[str] = None,
            interviewer_user_id: Optional[str] = None,
            created_by: Optional[str] = None,
            from_date: Optional[datetime] = None,
            to_date: Optional[datetime] = None,
            filter_by: Optional[str] = None,  # 'scheduled', 'deadline', or 'unscheduled'
            has_scheduled_at_and_interviewers: bool = False,  # Special filter for "SCHEDULED" status
            limit: int = 50,
            offset: int = 0
    ) -> List[Interview]:
        """Find interviews by multiple filters"""

        with self.database.get_session() as session:
            query = session.query(InterviewModel)

            if candidate_id:
                query = query.filter(InterviewModel.candidate_id == candidate_id)

            # Filter by candidate_name using JOIN with candidates table
            if candidate_name:
                from src.candidate_bc.candidate.infrastructure.models.candidate_model import CandidateModel
                query = query.join(
                    CandidateModel,
                    InterviewModel.candidate_id == CandidateModel.id
                ).filter(
                    func.lower(CandidateModel.name).contains(func.lower(candidate_name))
                )

            if job_position_id:
                query = query.filter(InterviewModel.job_position_id == job_position_id)

            if interview_type:
                # Convert enum to string for comparison
                interview_type_str = interview_type.value if hasattr(interview_type, 'value') else str(interview_type)
                query = query.filter(InterviewModel.interview_type == interview_type_str)

            if process_type:
                process_type_str = process_type.value if hasattr(process_type, 'value') else str(process_type)
                query = query.filter(InterviewModel.process_type == process_type_str)

            if status:
                status_str = status.value if hasattr(status, 'value') else str(status)
                query = query.filter(InterviewModel.status == status_str)

            # Special filter for "SCHEDULED" status: must have scheduled_at and interviewers
            if has_scheduled_at_and_interviewers:
                # interviewers is JSON (not JSONB), so we need to cast it to JSONB for jsonb_array_length
                # Or use a simpler check: verify it's not null and not an empty array
                query = query.filter(
                    InterviewModel.scheduled_at.isnot(None),
                    InterviewModel.interviewers.isnot(None),
                    func.jsonb_array_length(func.cast(InterviewModel.interviewers, postgresql.JSONB)) > 0
                )

            if required_role_id:
                # Filter using JSONB operator: check if required_roles contains the role_id
                query = query.filter(
                    InterviewModel.required_roles.contains([required_role_id])
                )

            if interviewer_user_id:
                # Filter by interviewer user_id in the interviewers list
                # Note: interviewers is currently a list of names, not user_ids
                # TODO: Update when interviewers becomes a list of CompanyUserId
                query = query.filter(
                    InterviewModel.interviewers.contains([interviewer_user_id])
                )

            if created_by:
                query = query.filter(InterviewModel.created_by == created_by)

            # Date filtering - support both scheduled_at and deadline_date
            # If filter_by is 'deadline', always exclude null deadline_date
            if filter_by == 'deadline':
                query = query.filter(InterviewModel.deadline_date.isnot(None))
                if from_date:
                    query = query.filter(InterviewModel.deadline_date >= from_date)
                if to_date:
                    query = query.filter(InterviewModel.deadline_date <= to_date)
            elif filter_by == 'unscheduled':
                # Filter for interviews without scheduled_at or without interviewers
                # This is for "pending_to_plan" - interviews that need to be scheduled
                query = query.filter(
                    or_(
                        InterviewModel.scheduled_at.is_(None),
                        InterviewModel.interviewers.is_(None),
                        func.jsonb_array_length(func.cast(InterviewModel.interviewers, postgresql.JSONB)) == 0
                    )
                )
            elif from_date or to_date:
                # Default to scheduled_at when filter_by is not 'deadline' or 'unscheduled'
                if from_date:
                    query = query.filter(InterviewModel.scheduled_at >= from_date)
                if to_date:
                    query = query.filter(InterviewModel.scheduled_at <= to_date)
            else:
                # If no filter_by specified, use created_at as fallback
                if from_date:
                    query = query.filter(InterviewModel.created_at >= from_date)
                if to_date:
                    query = query.filter(InterviewModel.created_at <= to_date)

            query = query.order_by(InterviewModel.created_at.desc())
            query = query.offset(offset).limit(limit)

            models = query.all()
            return [self._to_domain(model) for model in models]

    def count_by_filters(
            self,
            candidate_id: Optional[str] = None,
            candidate_name: Optional[str] = None,
            job_position_id: Optional[str] = None,
            interview_type: Optional[InterviewTypeEnum] = None,
            process_type: Optional[InterviewProcessTypeEnum] = None,
            status: Optional[InterviewStatusEnum] = None,
            required_role_id: Optional[str] = None,
            interviewer_user_id: Optional[str] = None,
            created_by: Optional[str] = None,
            from_date: Optional[datetime] = None,
            to_date: Optional[datetime] = None,
            filter_by: Optional[str] = None,  # 'scheduled', 'deadline', or 'unscheduled'
            has_scheduled_at_and_interviewers: bool = False  # Special filter for "SCHEDULED" status
    ) -> int:
        """Count interviews matching the filters (for pagination)"""

        with self.database.get_session() as session:
            query = session.query(InterviewModel)

            if candidate_id:
                query = query.filter(InterviewModel.candidate_id == candidate_id)

            # Filter by candidate_name using JOIN with candidates table
            if candidate_name:
                from src.candidate_bc.candidate.infrastructure.models.candidate_model import CandidateModel
                query = query.join(
                    CandidateModel,
                    InterviewModel.candidate_id == CandidateModel.id
                ).filter(
                    func.lower(CandidateModel.name).contains(func.lower(candidate_name))
                )

            if job_position_id:
                query = query.filter(InterviewModel.job_position_id == job_position_id)

            if interview_type:
                interview_type_str = interview_type.value if hasattr(interview_type, 'value') else str(interview_type)
                query = query.filter(InterviewModel.interview_type == interview_type_str)

            if process_type:
                process_type_str = process_type.value if hasattr(process_type, 'value') else str(process_type)
                query = query.filter(InterviewModel.process_type == process_type_str)

            if status:
                status_str = status.value if hasattr(status, 'value') else str(status)
                query = query.filter(InterviewModel.status == status_str)

            # Special filter for "SCHEDULED" status: must have scheduled_at and interviewers
            if has_scheduled_at_and_interviewers:
                # interviewers is JSON (not JSONB), so we need to cast it to JSONB for jsonb_array_length
                # Or use a simpler check: verify it's not null and not an empty array
                query = query.filter(
                    InterviewModel.scheduled_at.isnot(None),
                    InterviewModel.interviewers.isnot(None),
                    func.jsonb_array_length(func.cast(InterviewModel.interviewers, postgresql.JSONB)) > 0
                )

            if required_role_id:
                query = query.filter(
                    InterviewModel.required_roles.contains([required_role_id])
                )

            if interviewer_user_id:
                query = query.filter(
                    InterviewModel.interviewers.contains([interviewer_user_id])
                )

            if created_by:
                query = query.filter(InterviewModel.created_by == created_by)

            # Date filtering - support both scheduled_at and deadline_date
            # If filter_by is 'deadline', always exclude null deadline_date
            if filter_by == 'deadline':
                query = query.filter(InterviewModel.deadline_date.isnot(None))
                if from_date:
                    query = query.filter(InterviewModel.deadline_date >= from_date)
                if to_date:
                    query = query.filter(InterviewModel.deadline_date <= to_date)
            elif filter_by == 'unscheduled':
                # Filter for interviews without scheduled_at or without interviewers
                # This is for "pending_to_plan" - interviews that need to be scheduled
                query = query.filter(
                    or_(
                        InterviewModel.scheduled_at.is_(None),
                        InterviewModel.interviewers.is_(None),
                        func.jsonb_array_length(func.cast(InterviewModel.interviewers, postgresql.JSONB)) == 0
                    )
                )
            elif from_date or to_date:
                # Default to scheduled_at when filter_by is not 'deadline' or 'unscheduled'
                if from_date:
                    query = query.filter(InterviewModel.scheduled_at >= from_date)
                if to_date:
                    query = query.filter(InterviewModel.scheduled_at <= to_date)
            else:
                # If no filter_by specified, use created_at as fallback
                if from_date:
                    query = query.filter(InterviewModel.created_at >= from_date)
                if to_date:
                    query = query.filter(InterviewModel.created_at <= to_date)

            return query.count()

    def count_by_status(self, status: InterviewStatusEnum) -> int:
        """Count interviews by status"""
        with self.database.get_session() as session:
            return session.query(InterviewModel).filter(InterviewModel.status == status).count()

    def count_by_candidate(self, candidate_id: str) -> int:
        """Count interviews for a candidate"""
        with self.database.get_session() as session:
            return session.query(InterviewModel).filter(InterviewModel.candidate_id == candidate_id).count()

    def get_pending_interviews_by_candidate_and_stage(
            self,
            candidate_id: str,
            workflow_stage_id: str
    ) -> List[Interview]:
        """Get pending interviews for a candidate in a specific workflow stage"""
        with self.database.get_session() as session:
            models = session.query(InterviewModel).filter(
                InterviewModel.candidate_id == candidate_id,
                InterviewModel.workflow_stage_id == workflow_stage_id,
                InterviewModel.status == InterviewStatusEnum.PENDING  # ENABLED = "PENDING" (see enum definition)
            ).order_by(InterviewModel.created_at.desc()).all()
            return [self._to_domain(model) for model in models]

    def get_by_token(self, interview_id: str, token: str) -> Optional[Interview]:
        """Get interview by ID and token for secure link access"""
        import logging
        logger = logging.getLogger(__name__)

        with self.database.get_session() as session:
            # First check if interview exists
            model = session.query(InterviewModel).filter(
                InterviewModel.id == interview_id
            ).first()

            if not model:
                logger.warning(f"Interview {interview_id} not found")
                return None

            # Check if token matches
            if model.link_token != token:
                logger.warning(
                    f"Token mismatch for interview {interview_id}. Expected: {model.link_token}, Got: {token}")
                return None

            interview = self._to_domain(model)

            # Validate that the link is still valid
            if not interview.is_link_valid():
                logger.warning(f"Link expired for interview {interview_id}. Expires at: {interview.link_expires_at}")
                return None

            return interview

    def find_by_filters_with_joins(
            self,
            candidate_id: Optional[str] = None,
            candidate_name: Optional[str] = None,
            job_position_id: Optional[str] = None,
            interview_type: Optional[InterviewTypeEnum] = None,
            process_type: Optional[InterviewProcessTypeEnum] = None,
            status: Optional[InterviewStatusEnum] = None,
            required_role_id: Optional[str] = None,
            interviewer_user_id: Optional[str] = None,
            created_by: Optional[str] = None,
            from_date: Optional[datetime] = None,
            to_date: Optional[datetime] = None,
            filter_by: Optional[str] = None,  # 'scheduled', 'deadline', or 'unscheduled'
            has_scheduled_at_and_interviewers: bool = False,  # Special filter for "SCHEDULED" status
            limit: int = 50,
            offset: int = 0
    ) -> List[InterviewListReadModel]:
        """Find interviews by multiple filters with JOINs to get all related information (ReadModel)"""
        from src.candidate_bc.candidate.infrastructure.models.candidate_model import CandidateModel
        from src.company_bc.job_position.infrastructure.models.job_position_model import JobPositionModel
        from src.interview_bc.interview_template.infrastructure.models.interview_template import InterviewTemplateModel
        from src.shared_bc.customization.workflow.infrastructure.models.workflow_stage_model import WorkflowStageModel
        from src.company_bc.company_role.infrastructure.models.company_role_model import CompanyRoleModel
        from src.company_bc.company.infrastructure.models.company_user_model import CompanyUserModel
        from src.auth_bc.user.infrastructure.models.user_model import UserModel

        with self.database.get_session() as session:
            # Base query with JOINs
            query = session.query(
                InterviewModel,
                CandidateModel.name.label('candidate_name'),
                CandidateModel.email.label('candidate_email'),
                JobPositionModel.title.label('job_position_title'),
                InterviewTemplateModel.name.label('interview_template_name'),
                WorkflowStageModel.name.label('workflow_stage_name')
            ).outerjoin(
                CandidateModel,
                InterviewModel.candidate_id == CandidateModel.id
            ).outerjoin(
                JobPositionModel,
                InterviewModel.job_position_id == JobPositionModel.id
            ).outerjoin(
                InterviewTemplateModel,
                InterviewModel.interview_template_id == InterviewTemplateModel.id
            ).outerjoin(
                WorkflowStageModel,
                InterviewModel.workflow_stage_id == WorkflowStageModel.id
            )

            # Apply filters (same logic as find_by_filters)
            if candidate_id:
                query = query.filter(InterviewModel.candidate_id == candidate_id)

            if candidate_name:
                query = query.filter(func.lower(CandidateModel.name).contains(func.lower(candidate_name)))

            if job_position_id:
                query = query.filter(InterviewModel.job_position_id == job_position_id)

            if interview_type:
                interview_type_str = interview_type.value if hasattr(interview_type, 'value') else str(interview_type)
                query = query.filter(InterviewModel.interview_type == interview_type_str)

            if process_type:
                process_type_str = process_type.value if hasattr(process_type, 'value') else str(process_type)
                query = query.filter(InterviewModel.process_type == process_type_str)

            if status:
                status_str = status.value if hasattr(status, 'value') else str(status)
                query = query.filter(InterviewModel.status == status_str)

            if has_scheduled_at_and_interviewers:
                query = query.filter(
                    InterviewModel.scheduled_at.isnot(None),
                    InterviewModel.interviewers.isnot(None),
                    func.jsonb_array_length(func.cast(InterviewModel.interviewers, postgresql.JSONB)) > 0
                )

            if required_role_id:
                query = query.filter(InterviewModel.required_roles.contains([required_role_id]))

            if interviewer_user_id:
                query = query.filter(InterviewModel.interviewers.contains([interviewer_user_id]))

            if created_by:
                query = query.filter(InterviewModel.created_by == created_by)

            # Date filtering
            if filter_by == 'deadline':
                query = query.filter(InterviewModel.deadline_date.isnot(None))
                if from_date:
                    query = query.filter(InterviewModel.deadline_date >= from_date)
                if to_date:
                    query = query.filter(InterviewModel.deadline_date <= to_date)
            elif filter_by == 'unscheduled':
                query = query.filter(
                    or_(
                        InterviewModel.scheduled_at.is_(None),
                        InterviewModel.interviewers.is_(None),
                        func.jsonb_array_length(func.cast(InterviewModel.interviewers, postgresql.JSONB)) == 0
                    )
                )
            elif from_date or to_date:
                if from_date:
                    query = query.filter(InterviewModel.scheduled_at >= from_date)
                if to_date:
                    query = query.filter(InterviewModel.scheduled_at <= to_date)
            else:
                if from_date:
                    query = query.filter(InterviewModel.created_at >= from_date)
                if to_date:
                    query = query.filter(InterviewModel.created_at <= to_date)

            query = query.order_by(InterviewModel.created_at.desc())
            query = query.offset(offset).limit(limit)

            results = query.all()

            # Collect all unique interviewer IDs and role IDs to fetch in batch
            all_interviewer_ids = set()
            all_role_ids = set()
            interview_interviewers_map = {}  # interview_id -> list of interviewer_ids
            interview_roles_map = {}  # interview_id -> list of role_ids

            for result in results:
                interview_model = result[0]
                interview_id = interview_model.id

                if interview_model.interviewers:
                    interview_interviewers_map[interview_id] = interview_model.interviewers
                    all_interviewer_ids.update(interview_model.interviewers)

                if interview_model.required_roles:
                    interview_roles_map[interview_id] = interview_model.required_roles
                    all_role_ids.update(interview_model.required_roles)

            # Batch fetch all CompanyUsers and Users
            interviewer_name_map = {}  # interviewer_id -> name/email
            if all_interviewer_ids:
                company_users = session.query(CompanyUserModel, UserModel).join(
                    UserModel,
                    CompanyUserModel.user_id == UserModel.id
                ).filter(CompanyUserModel.id.in_(list(all_interviewer_ids))).all()

                for company_user, user in company_users:
                    interviewer_name_map[company_user.id] = user.email or user.name or company_user.id

            # Batch fetch all CompanyRoles
            role_name_map = {}  # role_id -> name
            if all_role_ids:
                roles = session.query(CompanyRoleModel).filter(
                    CompanyRoleModel.id.in_(list(all_role_ids))
                ).all()
                for role in roles:
                    role_name_map[role.id] = role.name

            # Convert to ReadModels
            read_models = []
            for result in results:
                interview_model = result[0]
                interview_id = interview_model.id
                candidate_name = result[1]
                candidate_email = result[2]
                job_position_title = result[3]
                interview_template_name = result[4]
                workflow_stage_name = result[5]

                # Get interviewer names from batch-fetched map
                interviewer_names = []
                if interview_id in interview_interviewers_map:
                    for interviewer_id in interview_interviewers_map[interview_id]:
                        interviewer_names.append(interviewer_name_map.get(interviewer_id, interviewer_id))

                # Get required role names from batch-fetched map
                required_role_names = []
                if interview_id in interview_roles_map:
                    for role_id in interview_roles_map[interview_id]:
                        required_role_names.append(role_name_map.get(role_id, role_id))

                # Calculate is_incomplete
                is_incomplete = (
                        interview_model.scheduled_at is not None and
                        (not interview_model.required_roles or not interview_model.interviewers)
                )

                read_model = InterviewListReadModel(
                    id=interview_model.id,
                    candidate_id=interview_model.candidate_id,
                    required_roles=interview_model.required_roles or [],
                    interview_type=interview_model.interview_type or '',
                    status=interview_model.status or '',
                    interviewers=interview_model.interviewers or [],
                    job_position_id=interview_model.job_position_id,
                    application_id=interview_model.application_id,
                    interview_template_id=interview_model.interview_template_id,
                    workflow_stage_id=interview_model.workflow_stage_id,
                    process_type=interview_model.process_type,
                    interview_mode=interview_model.interview_mode,
                    title=interview_model.title,
                    description=interview_model.description,
                    scheduled_at=interview_model.scheduled_at,
                    deadline_date=interview_model.deadline_date,
                    started_at=interview_model.started_at,
                    finished_at=interview_model.finished_at,
                    duration_minutes=interview_model.duration_minutes,
                    interviewer_notes=interview_model.interviewer_notes,
                    candidate_notes=interview_model.candidate_notes,
                    score=interview_model.score,
                    feedback=interview_model.feedback,
                    free_answers=interview_model.free_answers,
                    link_token=interview_model.link_token,
                    link_expires_at=interview_model.link_expires_at,
                    created_at=interview_model.created_at,
                    updated_at=interview_model.updated_at,
                    created_by=interview_model.created_by,
                    updated_by=interview_model.updated_by,
                    candidate_name=candidate_name,
                    candidate_email=candidate_email,
                    job_position_title=job_position_title,
                    interview_template_name=interview_template_name,
                    workflow_stage_name=workflow_stage_name,
                    interviewer_names=interviewer_names,
                    required_role_names=required_role_names,
                    is_incomplete=is_incomplete
                )
                read_models.append(read_model)

            return read_models
