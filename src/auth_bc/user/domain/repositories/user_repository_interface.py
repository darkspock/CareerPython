from abc import abstractmethod, ABC
from typing import Optional, List, Any

from src.auth_bc.user.domain.entities.user import User
from src.auth_bc.user.domain.value_objects.UserId import UserId


class UserRepositoryInterface(ABC):
    """Interfaz para repositorio de usuarios"""

    @abstractmethod
    def create(self, user: User) -> None:
        pass

    @abstractmethod
    def get_by_id(self, user_id: UserId) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_auth_data_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def update(self, user_id: UserId, user_data: dict[str, Any]) -> Optional[User]:
        pass

    @abstractmethod
    def update_entity(self, user: User) -> User:
        """Update user entity directly"""
        pass

    @abstractmethod
    def delete(self, user_id: UserId) -> bool:
        pass

    @abstractmethod
    def get_by_reset_token(self, reset_token: str) -> Optional[User]:
        pass
