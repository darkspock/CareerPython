from enum import Enum


class EntityCustomizationTypeEnum(str, Enum):
    JOB_POSITION = "JobPosition"
    CANDIDATE_APPLICATION = "CandidateApplication"
    CANDIDATE = "Candidate"
    WORKFLOW = "Workflow"
