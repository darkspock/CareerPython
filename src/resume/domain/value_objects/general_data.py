from dataclasses import dataclass


@dataclass
class GeneralData:
    """Value Object for fixed general data section"""
    cv_title: str = ""
    name: str = ""
    email: str = ""
    phone: str = ""

    def __post_init__(self) -> None:
        """Validate general data fields"""
        if self.email and '@' not in self.email:
            raise ValueError("Invalid email format")

        # Basic phone validation (allow various formats)
        if self.phone and len(self.phone.replace(' ', '').replace('-', '').replace('+', '')) < 7:
            raise ValueError("Phone number too short")

    def is_complete(self) -> bool:
        """Check if all required fields are filled"""
        return bool(self.cv_title and self.name and self.email)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'cv_title': self.cv_title,
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'GeneralData':
        """Create from dictionary"""
        return cls(
            cv_title=data.get('cv_title', ''),
            name=data.get('name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', '')
        )
