from dataclasses import dataclass
from typing import Optional

from src.interview.interview_template.domain.enums import InterviewTemplateSectionEnum
from src.interview.interview_template.domain.enums.interview_template_section import InterviewTemplateSectionStatusEnum
from src.interview.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.interview.interview_template.domain.value_objects.interview_template_section_id import \
    InterviewTemplateSectionId


@dataclass
class InterviewTemplateSection:
    id: InterviewTemplateSectionId
    interview_template_id: InterviewTemplateId
    name: str
    intro: str  # short for interview
    prompt: str  # instructions for the interviewer
    goal: str  # what to achieve with this template
    section: Optional[InterviewTemplateSectionEnum]
    sort_order: int = 0  # order within the template (0 = first)
    status: InterviewTemplateSectionStatusEnum = InterviewTemplateSectionStatusEnum.DRAFT

    @staticmethod
    def create(id: InterviewTemplateSectionId, interview_template_id: InterviewTemplateId, name: str, intro: str,
               prompt: str, goal: str, section: Optional[InterviewTemplateSectionEnum] = None,
               sort_order: int = 0,
               status: InterviewTemplateSectionStatusEnum = InterviewTemplateSectionStatusEnum.DRAFT) -> 'InterviewTemplateSection':
        return InterviewTemplateSection(
            id=id,
            interview_template_id=interview_template_id,
            name=name,
            intro=intro,
            prompt=prompt,
            goal=goal,
            section=section,
            sort_order=sort_order,
            status=status
        )

    def update_details(self, name: str, intro: str,
                       prompt: str, goal: str,
                       section: Optional[InterviewTemplateSectionEnum]) -> None:
        self.name = name
        self.intro = intro
        self.prompt = prompt
        self.goal = goal
        self.section = section

    def enable(self) -> None:
        """Enable this interview template section"""
        self.status = InterviewTemplateSectionStatusEnum.ENABLED

    def disable(self) -> None:
        """Disable this interview template section"""
        self.status = InterviewTemplateSectionStatusEnum.DISABLED

    def publish(self) -> None:
        """Publish this interview template section"""
        self.status = InterviewTemplateSectionStatusEnum.ENABLED

    def draft(self) -> None:
        """Set this interview template section to draft status"""
        self.status = InterviewTemplateSectionStatusEnum.DRAFT

    def update_sort_order(self, new_order: int) -> None:
        """Update the sort order of this section"""
        self.sort_order = new_order
