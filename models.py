# Import models for Alembic migration detection
from src.interview.interview_template.infrastructure.models.interview_template import InterviewTemplateModel
from src.interview.interview_template.infrastructure.models.interview_template_question import InterviewTemplateQuestionModel
from src.interview.interview_template.infrastructure.models.interview_template_section import InterviewTemplateSectionModel
from src.job_position.infrastructure.models.job_position_model import JobPositionModel
from src.job_position.infrastructure.models.job_position_workflow_model import JobPositionWorkflowModel
from src.job_position.infrastructure.models.job_position_comment_model import JobPositionCommentModel
from src.job_position.infrastructure.models.job_position_activity_model import JobPositionActivityModel
from src.phase.infrastructure.models.phase_model import PhaseModel
from src.company.infrastructure.models.company_model import CompanyModel
from src.company.infrastructure.models.company_user_model import CompanyUserModel
from src.company.infrastructure.models.company_user_invitation_model import CompanyUserInvitationModel
from src.company_page.infrastructure.models.company_page_model import CompanyPageModel
from src.company_candidate.infrastructure.models.company_candidate_model import CompanyCandidateModel
from src.company_candidate.infrastructure.models.candidate_comment_model import CandidateCommentModel
from src.candidate_review.infrastructure.models.candidate_review_model import CandidateReviewModel
from src.workflow.infrastructure.models.workflow_model import WorkflowModel
from src.workflow.infrastructure.models.workflow_stage_model import WorkflowStageModel
from src.customization.infrastructure.models.custom_field_model import CustomFieldModel
from src.customization.infrastructure.models.field_configuration_model import FieldConfigurationModel
from src.customization.infrastructure.models.entity_customization_model import EntityCustomizationModel
from src.field_validation.infrastructure.models.validation_rule_model import ValidationRuleModel
from src.user.infrastructure.models.user_model import UserModel
from src.user.infrastructure.models.user_asset_model import UserAssetModel
from src.candidate.infrastructure.models.candidate_model import CandidateModel
from src.candidate.infrastructure.models.candidate_education import CandidateEducationModel
from src.candidate.infrastructure.models.candidate_experience import CandidateExperienceModel
from src.candidate.infrastructure.models.candidate_project import CandidateProjectModel
from src.candidate.infrastructure.models.file_attachment_model import FileAttachmentModel
from src.candidate_application.infrastructure.models.candidate_application_model import CandidateApplicationModel
from src.resume.infrastructure.models.resume_model import ResumeModel
from src.talent_pool.infrastructure.models.talent_pool_entry_model import TalentPoolEntryModel

# Make sure models are available for Alembic
__all__ = [
    "InterviewTemplateModel",
    "InterviewTemplateQuestionModel",
    "InterviewTemplateSectionModel",
    "JobPositionModel",
    "JobPositionWorkflowModel",
    "JobPositionCommentModel",
    "JobPositionActivityModel",
    "PhaseModel",
    "CompanyModel",
    "CompanyUserModel",
    "CompanyUserInvitationModel",
    "CompanyPageModel",
    "CompanyCandidateModel",
    "CandidateCommentModel",
    "CandidateReviewModel",
    "WorkflowModel",
    "WorkflowStageModel",
    "CustomFieldModel",
    "FieldConfigurationModel",
    "EntityCustomizationModel",
    "ValidationRuleModel",
    "UserModel",
    "UserAssetModel",
    "CandidateModel",
    "CandidateEducationModel",
    "CandidateExperienceModel",
    "CandidateProjectModel",
    "FileAttachmentModel",
    "CandidateApplicationModel",
    "ResumeModel",
    "TalentPoolEntryModel",
]