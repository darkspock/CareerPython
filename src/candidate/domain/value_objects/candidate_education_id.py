from dataclasses import dataclass

from src.shared.domain.value_objects.base_id import BaseId


@dataclass(frozen=True)
class CandidateEducationId(BaseId):
    pass
