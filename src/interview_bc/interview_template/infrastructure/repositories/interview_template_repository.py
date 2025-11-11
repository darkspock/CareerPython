from datetime import datetime
from typing import Any, List, Optional

from sqlalchemy import desc, asc, or_
from sqlalchemy.exc import IntegrityError

from core.database import DatabaseInterface
from src.interview_bc.interview_template.domain.entities.interview_template import InterviewTemplate
from src.interview_bc.interview_template.domain.enums import (
    InterviewTemplateStatusEnum, InterviewTemplateTypeEnum
)
from src.interview_bc.interview_template.domain.exceptions.interview_exceptions import (
    InterviewTemplateNotFoundException,
    InterviewTemplateValidationException
)
from src.interview_bc.interview_template.domain.infrastructure.interview_template_repository_interface import \
    InterviewTemplateRepositoryInterface
from src.interview_bc.interview_template.domain.value_objects import InterviewTemplateId
from src.interview_bc.interview_template.infrastructure.models.interview_template import InterviewTemplateModel
from src.framework.domain.enums.job_category import JobCategoryEnum


class InterviewTemplateRepository(InterviewTemplateRepositoryInterface):

    def __init__(self, database: DatabaseInterface):
        self.database = database

    # Basic CRUD Operations

    def create(self, template: InterviewTemplate) -> InterviewTemplate:
        with self.database.get_session() as session:
            try:
                db_template = InterviewTemplateModel(
                    id=template.id.value,
                    name=template.name,
                    intro=template.intro,
                    prompt=template.prompt,
                    goal=template.goal,
                    status=template.status,
                    type=template.template_type,
                    job_category=template.job_category,
                    allow_ai_questions=template.allow_ai_questions,
                    legal_notice=template.legal_notice,
                    company_id=template.company_id.value if template.company_id else None,
                    created_by=getattr(template, 'created_by', None),
                    tags=template.tags or [],
                    template_metadata=template.metadata or {},
                )

                session.add(db_template)
                session.commit()
                session.refresh(db_template)

                return self._to_domain(db_template)

            except IntegrityError as e:
                session.rollback()
                raise InterviewTemplateValidationException(
                    template.id.value,
                    [f"Template creation failed: {str(e)}"]
                )
            except Exception as e:
                # Ensure rollback for any other database errors
                session.rollback()
                # Re-raise as a more specific exception
                raise InterviewTemplateValidationException(
                    template.id.value,
                    [f"Unexpected error during template creation: {str(e)}"]
                )

    def get_by_id(self, template_id: InterviewTemplateId) -> Optional[InterviewTemplate]:
        with self.database.get_session() as session:
            query = session.query(InterviewTemplateModel).filter(
                InterviewTemplateModel.id == template_id.value
            )

            db_template = query.first()
            return self._to_domain(db_template) if db_template else None

    def update(self, template: InterviewTemplate) -> None:
        with self.database.get_session() as session:
            db_template = session.query(InterviewTemplateModel).filter(
                InterviewTemplateModel.id == template.id.value,
            ).first()

            if not db_template:
                raise InterviewTemplateNotFoundException(f"Template {template.id.value} not found")

            # Update fields
            db_template.name = template.name
            db_template.intro = template.intro
            db_template.prompt = template.prompt
            db_template.goal = template.goal
            db_template.status = template.status
            db_template.type = template.template_type
            db_template.job_category = template.job_category
            db_template.allow_ai_questions = template.allow_ai_questions
            db_template.legal_notice = template.legal_notice
            db_template.company_id = template.company_id.value if template.company_id else None
            db_template.tags = template.tags or []
            db_template.template_metadata = template.metadata or {}
            db_template.updated_at = datetime.utcnow()

            session.commit()

    def delete(self, template_id: str, soft_delete: bool = True) -> bool:
        """Delete template (soft delete by default)"""
        with self.database.get_session() as session:
            if soft_delete:
                # Mark as deleted instead of physical deletion
                result = session.query(InterviewTemplateModel).filter(
                    InterviewTemplateModel.id == template_id,
                ).update({
                    'status': InterviewTemplateStatusEnum.DISABLED,
                    'updated_at': datetime.utcnow()
                })
            else:
                result = session.query(InterviewTemplateModel).filter(
                    InterviewTemplateModel.id == template_id
                ).delete()

            session.commit()
            return result > 0

    # Search and Filtering

    def search(self, **criteria: Any) -> List[InterviewTemplate]:
        """Advanced template search with multiple criteria"""
        with self.database.get_session() as session:
            query = session.query(InterviewTemplateModel)
            # Apply filters
            if 'name' in criteria and criteria['name']:
                query = query.filter(InterviewTemplateModel.name.ilike(f"%{criteria['name']}%"))

            if 'status' in criteria and criteria['status']:
                if isinstance(criteria['status'], list):
                    query = query.filter(InterviewTemplateModel.status.in_(criteria['status']))
                else:
                    query = query.filter(InterviewTemplateModel.status == criteria['status'])

            if 'type' in criteria and criteria['type']:
                if isinstance(criteria['type'], list):
                    query = query.filter(InterviewTemplateModel.type.in_(criteria['type']))
                else:
                    query = query.filter(InterviewTemplateModel.type == criteria['type'])

            if 'job_category' in criteria and criteria['job_category']:
                if isinstance(criteria['job_category'], list):
                    query = query.filter(InterviewTemplateModel.job_category.in_(criteria['job_category']))
                else:
                    query = query.filter(InterviewTemplateModel.job_category == criteria['job_category'])

            if 'tags' in criteria and criteria['tags']:
                for tag in criteria['tags']:
                    query = query.filter(InterviewTemplateModel.tags.contains([tag]))

            if 'created_by' in criteria and criteria['created_by']:
                query = query.filter(InterviewTemplateModel.created_by == criteria['created_by'])

            if 'company_id' in criteria and criteria['company_id']:
                query = query.filter(InterviewTemplateModel.company_id == criteria['company_id'])

            if 'created_after' in criteria and criteria['created_after']:
                query = query.filter(InterviewTemplateModel.created_at >= criteria['created_after'])

            if 'created_before' in criteria and criteria['created_before']:
                query = query.filter(InterviewTemplateModel.created_at <= criteria['created_before'])

            if 'text_search' in criteria and criteria['text_search']:
                search_term = f"%{criteria['text_search']}%"
                query = query.filter(or_(
                    InterviewTemplateModel.name.ilike(search_term),
                    InterviewTemplateModel.intro.ilike(search_term),
                    InterviewTemplateModel.prompt.ilike(search_term),
                    InterviewTemplateModel.goal.ilike(search_term)
                ))

            # Apply sorting
            sort_by = criteria.get('sort_by', 'created_at')
            sort_order = criteria.get('sort_order', 'desc')

            if hasattr(InterviewTemplateModel, sort_by):
                if sort_order.lower() == 'asc':
                    query = query.order_by(asc(getattr(InterviewTemplateModel, sort_by)))
                else:
                    query = query.order_by(desc(getattr(InterviewTemplateModel, sort_by)))

            # Apply pagination
            if 'limit' in criteria:
                query = query.limit(criteria['limit'])

            if 'offset' in criteria:
                query = query.offset(criteria['offset'])

            db_templates = query.all()
            return [self._to_domain(template) for template in db_templates]

    def get_by_type(self, template_type: InterviewTemplateTypeEnum, include_disabled: bool = False) -> List[InterviewTemplate]:
        """Get templates by type"""
        with self.database.get_session() as session:
            query = session.query(InterviewTemplateModel).filter(
                InterviewTemplateModel.type == template_type,
            )

            if not include_disabled:
                query = query.filter(InterviewTemplateModel.status != InterviewTemplateStatusEnum.DISABLED)

            db_templates = query.all()
            return [self._to_domain(template) for template in db_templates]

    def get_by_job_category(self, job_category: Optional[JobCategoryEnum]) -> List[InterviewTemplate]:
        """Get templates by job category"""
        with self.database.get_session() as session:
            query = session.query(InterviewTemplateModel).filter(
                InterviewTemplateModel.status == InterviewTemplateStatusEnum.ENABLED
            )

            if job_category:
                query = query.filter(or_(
                    InterviewTemplateModel.job_category == job_category,
                    InterviewTemplateModel.job_category.is_(None)  # Generic templates
                ))
            else:
                query = query.filter(InterviewTemplateModel.job_category.is_(None))

            db_templates = query.all()
            return [self._to_domain(template) for template in db_templates]

    # Helper Methods

    def _to_domain(self, db_template: InterviewTemplateModel) -> InterviewTemplate:
        """Convert database model to domain entity"""
        from src.interview_bc.interview_template.domain.value_objects import InterviewTemplateId
        from src.company_bc.company.domain.value_objects import CompanyId

        return InterviewTemplate(
            id=InterviewTemplateId.from_string(db_template.id),
            company_id=CompanyId.from_string(db_template.company_id) if db_template.company_id else None,
            name=db_template.name,
            intro=db_template.intro,
            prompt=db_template.prompt,
            goal=db_template.goal,
            status=db_template.status,
            template_type=db_template.type,
            job_category=db_template.job_category,
            allow_ai_questions=db_template.allow_ai_questions,
            legal_notice=db_template.legal_notice,
            tags=db_template.tags or [],
            metadata=db_template.template_metadata or {},
        )

    def clone_template(self, template_id: str, new_name: str, created_by: Optional[str] = None) -> InterviewTemplate:
        """Clone existing template with new ID"""
        from src.interview_bc.interview_template.domain.value_objects import InterviewTemplateId

        original = self.get_by_id(InterviewTemplateId.from_string(template_id))
        if not original:
            raise InterviewTemplateNotFoundException(f"Template {template_id} not found")

        from src.framework.domain.entities.base import generate_id

        cloned = InterviewTemplate(
            id=InterviewTemplateId.from_string(generate_id()),
            company_id=original.company_id,
            name=new_name,
            intro=original.intro,
            prompt=original.prompt,
            goal=original.goal,
            status=InterviewTemplateStatusEnum.DRAFT,  # Clones start as draft
            template_type=original.template_type,
            job_category=original.job_category,
            allow_ai_questions=original.allow_ai_questions,
            legal_notice=original.legal_notice,
            tags=(original.tags or []) + ['cloned'],
            metadata={
                'cloned_from': template_id,
                'cloned_at': datetime.utcnow().isoformat(),
                'created_by': created_by
            }
        )

        return self.create(cloned)
