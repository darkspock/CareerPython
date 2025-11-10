from enum import Enum


class WorkflowTypeEnum(str, Enum):
    JOB_POSITION_OPENING = "PO"  # Workflow is being configured
    CANDIDATE_APPLICATION = "CA"  # Workflow is active and can be used
    CANDIDATE_ONBOARDING = "CO"  # Workflow is archived
