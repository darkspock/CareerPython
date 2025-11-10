from src.framework.domain.value_objects.base_id import BaseId


class ResumeId(BaseId):
    """Value Object para ID de Resume"""

    @classmethod
    def create(cls) -> 'ResumeId':
        """Crea un nuevo ResumeId"""
        return cls.generate()

    @classmethod
    def from_string(cls, value: str) -> 'ResumeId':
        """Crea ResumeId desde string"""
        return cls(value)
