# Import models for Alembic migration detection
from src.interview_bc.interview_template.infrastructure.models.interview_template import InterviewTemplateModel
from src.interview_bc.interview_template.infrastructure.models.interview_template_question import InterviewTemplateQuestionModel
from src.interview_bc.interview_template.infrastructure.models.interview_template_section import InterviewTemplateSectionModel
from src.company_bc.job_position.infrastructure.models.job_position_model import JobPositionModel
from src.company_bc.job_position.infrastructure.models.job_position_comment_model import JobPositionCommentModel
from src.company_bc.job_position.infrastructure.models.job_position_stage_model import JobPositionStageModel
from src.shared_bc.customization.phase.infrastructure.models.phase_model import PhaseModel
from src.company_bc.company.infrastructure.models.company_model import CompanyModel
from src.company_bc.company.infrastructure.models.company_user_model import CompanyUserModel
from src.company_bc.company.infrastructure.models.company_user_invitation_model import CompanyUserInvitationModel
from src.company_bc.company_page.infrastructure.models.company_page_model import CompanyPageModel
from src.company_bc.company_candidate.infrastructure.models.company_candidate_model import CompanyCandidateModel
from src.company_bc.company_candidate.infrastructure.models.candidate_comment_model import CandidateCommentModel
from src.company_bc.candidate_review.infrastructure.models.candidate_review_model import CandidateReviewModel
from src.shared_bc.customization.workflow.infrastructure.models.workflow_model import WorkflowModel
from src.shared_bc.customization.workflow.infrastructure.models.workflow_stage_model import WorkflowStageModel
from src.shared_bc.customization.entity_customization.infrastructure.models.custom_field_model import CustomFieldModel
from src.shared_bc.customization.entity_customization.infrastructure.models.field_configuration_model import FieldConfigurationModel
from src.shared_bc.customization.entity_customization.infrastructure.models.entity_customization_model import EntityCustomizationModel
from src.shared_bc.customization.field_validation.infrastructure.models.validation_rule_model import ValidationRuleModel
from src.auth_bc.user.infrastructure.models.user_model import UserModel
from src.auth_bc.user.infrastructure.models.user_asset_model import UserAssetModel
from src.auth_bc.user_registration.infrastructure.models.user_registration_model import UserRegistrationModel
from src.candidate_bc.candidate.infrastructure.models.candidate_model import CandidateModel
from src.candidate_bc.candidate.infrastructure.models.candidate_education import CandidateEducationModel
from src.candidate_bc.candidate.infrastructure.models.candidate_experience import CandidateExperienceModel
from src.candidate_bc.candidate.infrastructure.models.candidate_project import CandidateProjectModel
from src.candidate_bc.candidate.infrastructure.models.file_attachment_model import FileAttachmentModel
from src.company_bc.candidate_application.infrastructure.models.candidate_application_model import CandidateApplicationModel
from src.candidate_bc.resume.infrastructure.models.resume_model import ResumeModel
from src.company_bc.talent_pool.infrastructure.models.talent_pool_entry_model import TalentPoolEntryModel

# Make sure models are available for Alembic
__all__ = [
    "InterviewTemplateModel",
    "InterviewTemplateQuestionModel",
    "InterviewTemplateSectionModel",
    "JobPositionModel",
    "JobPositionCommentModel",
    "JobPositionStageModel",
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
    "UserRegistrationModel",
    "CandidateModel",
    "CandidateEducationModel",
    "CandidateExperienceModel",
    "CandidateProjectModel",
    "FileAttachmentModel",
    "CandidateApplicationModel",
    "ResumeModel",
    "TalentPoolEntryModel",
]