from pydantic import BaseModel, field_validator
from datetime import date, datetime
from typing import Optional, Any


class CandidateEducationBase(BaseModel):
    degree: str
    institution: str
    description: str
    start_date: date
    end_date: Optional[date]


class CandidateEducationCreate(CandidateEducationBase):
    id: str
    candidate_id: str
    created_at: datetime
    updated_at: datetime


class CandidateEducation(CandidateEducationBase):
    id: str
    candidate_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CandidateEducationResponse(CandidateEducationBase):
    id: str
    candidate_id: str
    created_at: datetime
    updated_at: datetime

    @field_validator('id', mode='before')
    @classmethod
    def format_id(cls, v: Any) -> str:
        if hasattr(v, 'value'):
            return str(v.value)
        return str(v)

    @field_validator('candidate_id', mode='before')
    @classmethod
    def format_candidate_id(cls, v: Any) -> str:
        if hasattr(v, 'value'):
            return str(v.value)
        return str(v)

    class Config:
        from_attributes = True


class CandidateEducationCreateRequest(BaseModel):
    degree: str
    institution: str
    description: str
    start_date: str
    end_date: Optional[str]
