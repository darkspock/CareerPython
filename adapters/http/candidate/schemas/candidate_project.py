from datetime import date, datetime
from typing import Optional, Any

from pydantic import BaseModel, field_validator, ConfigDict


class CandidateProjectBase(BaseModel):
    name: str
    description: str
    start_date: date
    end_date: Optional[date]


class CandidateProjectCreate(CandidateProjectBase):
    id: str
    candidate_id: str
    created_at: datetime
    updated_at: datetime


class CandidateProject(CandidateProjectBase):
    id: str
    candidate_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CandidateProjectResponse(CandidateProjectBase):
    id: str
    candidate_id: str

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

    model_config = ConfigDict(from_attributes=True)


class CandidateProjectCreateRequest(BaseModel):
    name: str
    description: str
    start_date: str
    end_date: Optional[str]
