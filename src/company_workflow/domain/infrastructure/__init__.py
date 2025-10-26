# Company workflow infrastructure interfaces
from .company_workflow_repository_interface import CompanyWorkflowRepositoryInterface
from .workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from .custom_field_repository_interface import CustomFieldRepositoryInterface
from .field_configuration_repository_interface import FieldConfigurationRepositoryInterface

__all__ = [
    "CompanyWorkflowRepositoryInterface",
    "WorkflowStageRepositoryInterface",
    "CustomFieldRepositoryInterface",
    "FieldConfigurationRepositoryInterface",
]
