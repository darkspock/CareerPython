"""
Interview Template Section Repository
"""
from typing import List, Optional

from sqlalchemy.exc import IntegrityError

from core.database import DatabaseInterface
from src.interview.interview_template.domain.entities.interview_template_section import InterviewTemplateSection
from src.interview.interview_template.domain.exceptions.interview_exceptions import (
    InterviewTemplateNotFoundException,
    InterviewTemplateValidationException
)
from src.interview.interview_template.domain.infrastructure.interview_template_section_repository_interface import \
    InterviewTemplateSectionRepositoryInterface
from src.interview.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.interview.interview_template.domain.value_objects.interview_template_section_id import \
    InterviewTemplateSectionId
from src.interview.interview_template.infrastructure.models.interview_template_section import \
    InterviewTemplateSectionModel


class InterviewTemplateSectionRepository(InterviewTemplateSectionRepositoryInterface):
    """Repository for interview template sections"""

    def __init__(self, database: DatabaseInterface):
        self.database = database

    def create(self, section: InterviewTemplateSection) -> InterviewTemplateSection:
        """Create a new section"""
        with self.database.get_session() as session:
            try:
                db_section = InterviewTemplateSectionModel(
                    id=section.id.value,
                    interview_template_id=section.interview_template_id.value,
                    name=section.name,
                    intro=section.intro,
                    prompt=section.prompt,
                    goal=section.goal,
                    section=section.section,
                    sort_order=section.sort_order,
                    status=section.status
                )

                session.add(db_section)
                session.commit()
                session.refresh(db_section)

                return self._to_domain(db_section)

            except IntegrityError as e:
                session.rollback()
                raise InterviewTemplateValidationException(
                    section.id.value,
                    [f"Section creation failed: {str(e)}"]
                )
            except Exception as e:
                session.rollback()
                raise InterviewTemplateValidationException(
                    section.id.value,
                    [f"Unexpected error during section creation: {str(e)}"]
                )

    def get_by_id(self, section_id: InterviewTemplateSectionId) -> Optional[InterviewTemplateSection]:
        """Get section by ID"""
        with self.database.get_session() as session:
            db_section = session.query(InterviewTemplateSectionModel).filter(
                InterviewTemplateSectionModel.id == section_id.value
            ).first()
            return self._to_domain(db_section) if db_section else None

    def get_by_template_id(self, template_id: InterviewTemplateId) -> List[InterviewTemplateSection]:
        """Get all sections for a template, ordered by sort_order"""
        with self.database.get_session() as session:
            db_sections = session.query(InterviewTemplateSectionModel).filter(
                InterviewTemplateSectionModel.interview_template_id == template_id.value
            ).order_by(InterviewTemplateSectionModel.sort_order.asc()).all()
            return [self._to_domain(section) for section in db_sections]

    def update(self, section: InterviewTemplateSection) -> InterviewTemplateSection:
        """Update an existing section"""
        with self.database.get_session() as session:
            db_section = session.query(InterviewTemplateSectionModel).filter(
                InterviewTemplateSectionModel.id == section.id.value
            ).first()

            if not db_section:
                raise InterviewTemplateNotFoundException(f"Section {section.id.value} not found")

            # Update fields
            db_section.name = section.name
            db_section.intro = section.intro
            db_section.prompt = section.prompt
            db_section.goal = section.goal
            db_section.section = section.section
            db_section.sort_order = section.sort_order
            db_section.status = section.status

            session.commit()
            session.refresh(db_section)

            return self._to_domain(db_section)

    def delete(self, section_id: InterviewTemplateSectionId) -> bool:
        """Delete a section"""
        with self.database.get_session() as session:
            result = session.query(InterviewTemplateSectionModel).filter(
                InterviewTemplateSectionModel.id == section_id.value
            ).delete()

            session.commit()
            return result > 0

    def _to_domain(self, db_section: InterviewTemplateSectionModel) -> InterviewTemplateSection:
        """Convert database model to domain entity"""
        from src.interview.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
        from src.interview.interview_template.domain.value_objects.interview_template_section_id import \
            InterviewTemplateSectionId

        return InterviewTemplateSection(
            id=InterviewTemplateSectionId.from_string(db_section.id),
            interview_template_id=InterviewTemplateId.from_string(db_section.interview_template_id),
            name=db_section.name,
            intro=db_section.intro,
            prompt=db_section.prompt,
            goal=db_section.goal,
            section=db_section.section,
            sort_order=db_section.sort_order,
            status=db_section.status
        )
