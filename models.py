# Import models for Alembic migration detection
from src.interview.interview_template.infrastructure.models.interview_template import InterviewTemplateModel
from src.interview.interview_template.infrastructure.models.interview_template_question import InterviewTemplateQuestionModel
from src.interview.interview_template.infrastructure.models.interview_template_section import InterviewTemplateSectionModel
from src.job_position.infrastructure.models.job_position_model import JobPositionModel
from src.company.infrastructure.models.company_model import CompanyModel
from src.company.infrastructure.models.company_user_model import CompanyUserModel
from src.company_candidate.infrastructure.models.company_candidate_model import CompanyCandidateModel
from src.company_candidate.infrastructure.models.candidate_comment_model import CandidateCommentModel
from src.company_workflow.infrastructure.models.company_workflow_model import CompanyWorkflowModel
from src.company_workflow.infrastructure.models.workflow_stage_model import WorkflowStageModel
from src.company_workflow.infrastructure.models.custom_field_model import CustomFieldModel
from src.company_workflow.infrastructure.models.field_configuration_model import FieldConfigurationModel
from src.field_validation.infrastructure.models.validation_rule_model import ValidationRuleModel
from src.user.infrastructure.models.user_model import UserModel
from src.user.infrastructure.models.user_asset_model import UserAssetModel
from src.candidate.infrastructure.models.candidate_model import CandidateModel
from src.candidate.infrastructure.models.candidate_education import CandidateEducationModel
from src.candidate.infrastructure.models.candidate_experience import CandidateExperienceModel
from src.candidate.infrastructure.models.candidate_project import CandidateProjectModel
from src.candidate_application.infrastructure.models.candidate_application_model import CandidateApplicationModel
from src.resume.infrastructure.models.resume_model import ResumeModel

# Make sure models are available for Alembic
__all__ = [
    "InterviewTemplateModel",
    "InterviewTemplateQuestionModel",
    "InterviewTemplateSectionModel",
    "JobPositionModel",
    "CompanyModel",
    "CompanyUserModel",
    "CompanyCandidateModel",
    "CandidateCommentModel",
    "CompanyWorkflowModel",
    "WorkflowStageModel",
    "CustomFieldModel",
    "FieldConfigurationModel",
    "ValidationRuleModel",
    "UserModel",
    "UserAssetModel",
    "CandidateModel",
    "CandidateEducationModel",
    "CandidateExperienceModel",
    "CandidateProjectModel",
    "CandidateApplicationModel",
    "ResumeModel",
]