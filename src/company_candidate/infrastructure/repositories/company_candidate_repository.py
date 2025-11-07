from typing import Optional, List

from sqlalchemy.orm import Session

from src.company_candidate.domain.entities.company_candidate import CompanyCandidate
from src.company_candidate.domain.enums import (
    CompanyCandidateStatus,
    OwnershipStatus,
    CandidatePriority,
)
from src.company_candidate.domain.value_objects import (
    CompanyCandidateId,
    VisibilitySettings,
)
from src.company_candidate.domain.read_models.company_candidate_with_candidate_read_model import (
    CompanyCandidateWithCandidateReadModel
)
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import (
    CompanyCandidateRepositoryInterface
)
from src.company_candidate.infrastructure.models.company_candidate_model import CompanyCandidateModel
from src.candidate.infrastructure.models.candidate_model import CandidateModel
from src.candidate_application.infrastructure.models.candidate_application_model import CandidateApplicationModel
from src.job_position.infrastructure.models.job_position_model import JobPositionModel
from src.company.domain.value_objects import CompanyId
from src.company.domain.value_objects.company_user_id import CompanyUserId
from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from core.database import SQLAlchemyDatabase


class CompanyCandidateRepository(CompanyCandidateRepositoryInterface):
    """SQLAlchemy implementation of CompanyCandidateRepositoryInterface"""

    def __init__(self, database: SQLAlchemyDatabase):
        self.database = database

    def _get_session(self) -> Session:
        """Get database session"""
        return self.database.get_session()

    def _to_domain(self, model: CompanyCandidateModel) -> CompanyCandidate:
        """Convert model to domain entity"""
        return CompanyCandidate(
            id=CompanyCandidateId.from_string(model.id),
            company_id=CompanyId.from_string(model.company_id),
            candidate_id=CandidateId.from_string(model.candidate_id),
            status=CompanyCandidateStatus(model.status),
            ownership_status=OwnershipStatus(model.ownership_status),
            created_by_user_id=CompanyUserId.from_string(model.created_by_user_id),
            workflow_id=WorkflowId.from_string(model.workflow_id) if model.workflow_id else None,
            current_stage_id=WorkflowStageId.from_string(model.current_stage_id) if model.current_stage_id else None,
            phase_id=model.phase_id,
            invited_at=model.invited_at,
            confirmed_at=model.confirmed_at,
            rejected_at=model.rejected_at,
            archived_at=model.archived_at,
            visibility_settings=VisibilitySettings.from_dict(model.visibility_settings or {}),
            tags=model.tags or [],
            internal_notes=model.internal_notes or "",
            position=model.position,
            department=model.department,
            priority=CandidatePriority(model.priority),
            lead_id=model.lead_id,
            source=model.source,
            resume_url=model.resume_url,
            resume_uploaded_by=CompanyUserId.from_string(model.resume_uploaded_by) if model.resume_uploaded_by else None,
            resume_uploaded_at=model.resume_uploaded_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: CompanyCandidate) -> CompanyCandidateModel:
        """Convert domain entity to model"""
        return CompanyCandidateModel(
            id=str(entity.id),
            company_id=str(entity.company_id),
            candidate_id=str(entity.candidate_id),
            status=entity.status.value,
            ownership_status=entity.ownership_status.value,
            created_by_user_id=str(entity.created_by_user_id),
            workflow_id=str(entity.workflow_id) if entity.workflow_id else None,
            current_stage_id=str(entity.current_stage_id) if entity.current_stage_id else None,
            phase_id=entity.phase_id,
            invited_at=entity.invited_at,
            confirmed_at=entity.confirmed_at,
            rejected_at=entity.rejected_at,
            archived_at=entity.archived_at,
            visibility_settings=entity.visibility_settings.to_dict(),
            tags=entity.tags,
            internal_notes=entity.internal_notes,
            position=entity.position,
            department=entity.department,
            priority=entity.priority.value,
            lead_id=entity.lead_id,
            source=entity.source,
            resume_url=entity.resume_url,
            resume_uploaded_by=str(entity.resume_uploaded_by) if entity.resume_uploaded_by else None,
            resume_uploaded_at=entity.resume_uploaded_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def save(self, company_candidate: CompanyCandidate) -> None:
        """Save or update a company candidate relationship"""
        session = self._get_session()
        model = session.query(CompanyCandidateModel).filter_by(id=str(company_candidate.id)).first()

        if model:
            # Update existing
            model.company_id = str(company_candidate.company_id)
            model.candidate_id = str(company_candidate.candidate_id)
            model.status = company_candidate.status.value
            model.ownership_status = company_candidate.ownership_status.value
            model.created_by_user_id = str(company_candidate.created_by_user_id)
            model.workflow_id = str(company_candidate.workflow_id) if company_candidate.workflow_id else None
            model.current_stage_id = str(company_candidate.current_stage_id) if company_candidate.current_stage_id else None
            model.invited_at = company_candidate.invited_at
            model.confirmed_at = company_candidate.confirmed_at
            model.rejected_at = company_candidate.rejected_at
            model.archived_at = company_candidate.archived_at
            model.visibility_settings = company_candidate.visibility_settings.to_dict()
            model.tags = company_candidate.tags
            model.internal_notes = company_candidate.internal_notes
            model.position = company_candidate.position
            model.department = company_candidate.department
            model.priority = company_candidate.priority.value
            model.lead_id = company_candidate.lead_id
            model.source = company_candidate.source
            model.resume_url = company_candidate.resume_url
            model.resume_uploaded_by = str(company_candidate.resume_uploaded_by) if company_candidate.resume_uploaded_by else None
            model.resume_uploaded_at = company_candidate.resume_uploaded_at
            model.updated_at = company_candidate.updated_at
        else:
            # Create new
            model = self._to_model(company_candidate)
            session.add(model)

        session.commit()

    def get_by_id(self, company_candidate_id: CompanyCandidateId) -> Optional[CompanyCandidate]:
        """Get a company candidate by ID"""
        session = self._get_session()
        model = session.query(CompanyCandidateModel).filter_by(id=str(company_candidate_id)).first()
        return self._to_domain(model) if model else None

    def get_by_id_with_candidate_info(self, company_candidate_id: CompanyCandidateId) -> Optional[CompanyCandidateWithCandidateReadModel]:
        """
        Get a single company candidate by ID with candidate basic info and position.
        Uses SQL JOIN for efficient data retrieval.
        """
        session = self._get_session()

        # Import models for JOIN
        from src.workflow.infrastructure.models.workflow_model import WorkflowModel
        from src.workflow.infrastructure.models.workflow_stage_model import WorkflowStageModel
        # from src.phase.infrastructure.models.phase_model import PhaseModel  # Temporarily disabled
        
        # Perform JOINs between company_candidates, candidates, candidate_applications, job_positions, workflows, and stages
        result = session.query(
            CompanyCandidateModel,
            CandidateModel.name,
            CandidateModel.email,
            CandidateModel.phone,
            CandidateApplicationModel.job_position_id,
            CandidateApplicationModel.application_status,
            JobPositionModel.title,
            WorkflowModel.name.label('workflow_name'),
            WorkflowStageModel.name.label('stage_name')
        ).join(
            CandidateModel,
            CompanyCandidateModel.candidate_id == CandidateModel.id
        ).outerjoin(
            CandidateApplicationModel,
            CompanyCandidateModel.candidate_id == CandidateApplicationModel.candidate_id
        ).outerjoin(
            JobPositionModel,
            CandidateApplicationModel.job_position_id == JobPositionModel.id
        ).outerjoin(
            WorkflowModel,
            CompanyCandidateModel.workflow_id == WorkflowModel.id
        ).outerjoin(
            WorkflowStageModel,
            CompanyCandidateModel.current_stage_id == WorkflowStageModel.id
        ).filter(
            CompanyCandidateModel.id == str(company_candidate_id)
        ).first()

        if not result:
            return None

        cc_model, candidate_name, candidate_email, candidate_phone, job_position_id, application_status, job_position_title, workflow_name, stage_name = result
        
        return CompanyCandidateWithCandidateReadModel(
            id=cc_model.id,
            company_id=cc_model.company_id,
            candidate_id=cc_model.candidate_id,
            status=cc_model.status,
            ownership_status=cc_model.ownership_status,
            created_by_user_id=cc_model.created_by_user_id,
            workflow_id=cc_model.workflow_id,
            current_stage_id=cc_model.current_stage_id,
            phase_id=cc_model.phase_id,
            invited_at=cc_model.invited_at,
            confirmed_at=cc_model.confirmed_at,
            rejected_at=cc_model.rejected_at,
            archived_at=cc_model.archived_at,
            visibility_settings=cc_model.visibility_settings or {},
            tags=cc_model.tags or [],
            internal_notes=cc_model.internal_notes or '',
            position=cc_model.position,
            department=cc_model.department,
            priority=cc_model.priority,
            lead_id=cc_model.lead_id,
            source=cc_model.source,
            resume_url=cc_model.resume_url,
            resume_uploaded_by=cc_model.resume_uploaded_by,
            resume_uploaded_at=cc_model.resume_uploaded_at,
            created_at=cc_model.created_at,
            updated_at=cc_model.updated_at,
            # Candidate info from JOIN
            candidate_name=candidate_name,
            candidate_email=candidate_email,
            candidate_phone=candidate_phone,
            # Job position info from candidate_application JOIN
            job_position_id=job_position_id,
            job_position_title=job_position_title,
            application_status=application_status,
            # Workflow and stage info from JOINs
            workflow_name=workflow_name,
            stage_name=stage_name,
            # Phase info from JOIN (temporarily disabled)
            phase_name=None,
        )

    def get_by_company_and_candidate(
        self,
        company_id: CompanyId,
        candidate_id: CandidateId
    ) -> Optional[CompanyCandidate]:
        """Get a company candidate by company and candidate IDs"""
        session = self._get_session()
        model = session.query(CompanyCandidateModel).filter_by(
            company_id=str(company_id),
            candidate_id=str(candidate_id)
        ).first()
        return self._to_domain(model) if model else None

    def list_by_company(self, company_id: CompanyId) -> List[CompanyCandidate]:
        """List all company candidates for a company"""
        session = self._get_session()
        models = session.query(CompanyCandidateModel).filter_by(
            company_id=str(company_id)
        ).all()
        return [self._to_domain(model) for model in models]

    def list_by_candidate(self, candidate_id: CandidateId) -> List[CompanyCandidate]:
        """List all company candidates for a candidate"""
        session = self._get_session()
        models = session.query(CompanyCandidateModel).filter_by(
            candidate_id=str(candidate_id)
        ).all()
        return [self._to_domain(model) for model in models]

    def list_active_by_company(self, company_id: CompanyId) -> List[CompanyCandidate]:
        """List all active company candidates for a company"""
        session = self._get_session()
        models = session.query(CompanyCandidateModel).filter_by(
            company_id=str(company_id),
            status=CompanyCandidateStatus.ACTIVE.value
        ).all()
        return [self._to_domain(model) for model in models]

    def delete(self, company_candidate_id: CompanyCandidateId) -> None:
        """Delete a company candidate relationship"""
        session = self._get_session()
        session.query(CompanyCandidateModel).filter_by(id=str(company_candidate_id)).delete()
        session.commit()

    def list_by_company_with_candidate_info(self, company_id: CompanyId) -> List[CompanyCandidateWithCandidateReadModel]:
        """
        List all company candidates for a company with candidate basic info and position.
        Uses SQL JOIN for efficient data retrieval.
        """
        session = self._get_session()

        # Import models for JOIN
        from src.workflow.infrastructure.models.workflow_model import WorkflowModel
        from src.workflow.infrastructure.models.workflow_stage_model import WorkflowStageModel
        from src.company_candidate.infrastructure.models.candidate_comment_model import CandidateCommentModel
        from src.company_candidate.domain.enums.comment_review_status import CommentReviewStatus
        from sqlalchemy import func
        # from src.phase.infrastructure.models.phase_model import PhaseModel  # Temporarily disabled
        
        # Subquery to count pending comments per company candidate
        pending_comments_subquery = session.query(
            CandidateCommentModel.company_candidate_id,
            func.count(CandidateCommentModel.id).label('pending_count')
        ).filter(
            CandidateCommentModel.review_status == CommentReviewStatus.PENDING.value
        ).group_by(CandidateCommentModel.company_candidate_id).subquery()
        
        # Perform JOINs between company_candidates, candidates, candidate_applications, job_positions, workflows, and stages
        results = session.query(
            CompanyCandidateModel,
            CandidateModel.name,
            CandidateModel.email,
            CandidateModel.phone,
            CandidateApplicationModel.job_position_id,
            CandidateApplicationModel.application_status,
            JobPositionModel.title,
            WorkflowModel.name.label('workflow_name'),
            WorkflowStageModel.name.label('stage_name'),
            func.coalesce(pending_comments_subquery.c.pending_count, 0).label('pending_comments_count')
        ).join(
            CandidateModel,
            CompanyCandidateModel.candidate_id == CandidateModel.id
        ).outerjoin(
            CandidateApplicationModel,
            CompanyCandidateModel.candidate_id == CandidateApplicationModel.candidate_id
        ).outerjoin(
            JobPositionModel,
            CandidateApplicationModel.job_position_id == JobPositionModel.id
        ).outerjoin(
            WorkflowModel,
            CompanyCandidateModel.workflow_id == WorkflowModel.id
        ).outerjoin(
            WorkflowStageModel,
            CompanyCandidateModel.current_stage_id == WorkflowStageModel.id
        ).outerjoin(
            pending_comments_subquery,
            CompanyCandidateModel.id == pending_comments_subquery.c.company_candidate_id
        ).filter(
            CompanyCandidateModel.company_id == str(company_id)
        ).all()

        # Convert to read models
        read_models = []
        for cc_model, candidate_name, candidate_email, candidate_phone, job_position_id, application_status, job_position_title, workflow_name, stage_name, pending_comments_count in results:
            read_model = CompanyCandidateWithCandidateReadModel(
                id=cc_model.id,
                company_id=cc_model.company_id,
                candidate_id=cc_model.candidate_id,
                status=cc_model.status,
                ownership_status=cc_model.ownership_status,
                created_by_user_id=cc_model.created_by_user_id,
                workflow_id=cc_model.workflow_id,
                current_stage_id=cc_model.current_stage_id,
                phase_id=cc_model.phase_id,  # Get phase_id from model
                invited_at=cc_model.invited_at,
                confirmed_at=cc_model.confirmed_at,
                rejected_at=cc_model.rejected_at,
                archived_at=cc_model.archived_at,
                visibility_settings=cc_model.visibility_settings or {},
                tags=cc_model.tags or [],
                internal_notes=cc_model.internal_notes or '',
                position=cc_model.position,
                department=cc_model.department,
                priority=cc_model.priority,
                lead_id=cc_model.lead_id,
                source=cc_model.source,
                resume_url=cc_model.resume_url,
                resume_uploaded_by=cc_model.resume_uploaded_by,
                resume_uploaded_at=cc_model.resume_uploaded_at,
                created_at=cc_model.created_at,
                updated_at=cc_model.updated_at,
                # Candidate info from JOIN
                candidate_name=candidate_name,
                candidate_email=candidate_email,
                candidate_phone=candidate_phone,
                # Job position info from candidate_application JOIN
                job_position_id=job_position_id,
                job_position_title=job_position_title,
                application_status=application_status,
                # Workflow and stage info from JOINs
                workflow_name=workflow_name,
                stage_name=stage_name,
                # Phase info from JOIN (temporarily disabled)
                phase_name=None,
                # Comment counts
                pending_comments_count=int(pending_comments_count) if pending_comments_count else 0,
            )
            read_models.append(read_model)

        return read_models
