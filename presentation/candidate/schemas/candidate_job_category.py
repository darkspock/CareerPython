from pydantic import BaseModel
from src.shared.domain.enums.job_category import JobCategoryEnum


class CandidateJobCategoryBase(BaseModel):
    candidate_id: str
    job_category: JobCategoryEnum
    is_primary: bool


class CandidateJobCategoryCreate(CandidateJobCategoryBase):
    id: str


class CandidateJobCategory(CandidateJobCategoryBase):
    id: str

    class Config:
        from_attributes = True


class CandidateJobCategoryResponse(CandidateJobCategoryBase):
    id: str

    class Config:
        from_attributes = True
