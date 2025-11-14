from enum import Enum
from typing import TypeVar, List, Type, Any, Dict

T = TypeVar('T', bound=Enum)


class MixedHelper:
    """Helper class for type conversions and mixed data operations"""

    @staticmethod
    def get_string(value: Any) -> str:
        """Convert any value to string, handling enums specially"""
        if isinstance(value, Enum):
            return str(value.value)
        return str(value)

    @staticmethod
    def get_int(value: Any) -> int:
        """Convert any value to integer"""
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                raise ValueError(f"Cannot convert '{value}' to integer")
        if value is None:
            raise ValueError("Cannot convert None to integer")
        return int(value)
    
    @staticmethod
    def get_boolean(value: Any) -> bool:
        """Convert any value to boolean"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        if isinstance(value, (int, float)):
            return bool(value)
        return bool(value)

    @staticmethod
    def enum_list_to_string_list(enum_list: List[Any]) -> List[str]:
        """Convert list of enums to list of strings"""
        return [MixedHelper.get_string(enum_item) for enum_item in enum_list]

    @staticmethod
    def enum_list_to_string_list_or_null(enum_list: List[Any] | None) -> List[str] | None:
        """Convert list of enums to list of strings or return None if input is None"""
        if enum_list is None:
            return None
        return [MixedHelper.get_string(enum_item) for enum_item in enum_list]

    @staticmethod
    def string_list_to_enum_list(string_list: List[str], enum_class: Type[T]) -> List[T]:
        """Convert list of strings to list of enums"""
        return [enum_class(string_item) for string_item in string_list]

    @staticmethod
    def string_list_to_enum_list_or_null(string_list: Any, enum_class: Type[T]) -> List[T] | None:
        """Convert list of strings to list of enums or return None if input is None"""
        if string_list is None:
            return None
        return [enum_class(string_item) for string_item in string_list]

    @staticmethod
    def get_string_list(value: Any) -> List[str]:
        """Convert any value to list of strings"""
        if value is None:
            return []
        if isinstance(value, list):
            return [MixedHelper.get_string(item) for item in value]
        # If it's a single value, convert to string and return as single-item list
        return [MixedHelper.get_string(value)]
    
    @staticmethod
    def get_optional_string(value: Any) -> str | None:
        """Convert any value to optional string"""
        if value is None:
            return None
        return MixedHelper.get_string(value)
    
    @classmethod
    def dict_to_list(cls, value: Dict[str, Any]) -> List[Any]:
        """Convert dict values to list"""
        if not isinstance(value, dict):
            raise ValueError("Input must be a dictionary")
        return list(value.values())
