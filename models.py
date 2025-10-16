# Import models for Alembic migration detection
from src.interview.interview_template.infrastructure.models.interview_template import InterviewTemplateModel
from src.interview.interview_template.infrastructure.models.interview_template_question import InterviewTemplateQuestionModel
from src.interview.interview_template.infrastructure.models.interview_template_section import InterviewTemplateSectionModel
from src.job_position.infrastructure.models.job_position_model import JobPositionModel
from src.company.infrastructure.models.company_model import CompanyModel

# Make sure models are available for Alembic
__all__ = [
    "InterviewTemplateModel",
    "InterviewTemplateQuestionModel",
    "InterviewTemplateSectionModel",
    "JobPositionModel",
    "CompanyModel"
]