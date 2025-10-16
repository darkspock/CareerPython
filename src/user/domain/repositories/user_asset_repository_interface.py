from abc import ABC, abstractmethod
from typing import Optional, List

from src.user.domain.entities.user_asset import UserAsset
from src.user.domain.enums.asset_enums import AssetTypeEnum
from src.user.domain.value_objects.UserId import UserId
from src.user.domain.value_objects.user_asset_id import UserAssetId


class UserAssetRepositoryInterface(ABC):
    """Interface para el repositorio de assets de usuario"""

    @abstractmethod
    def save(self, user_asset: UserAsset) -> None:
        """Guardar un asset de usuario"""
        pass

    @abstractmethod
    def get_by_id(self, asset_id: UserAssetId) -> Optional[UserAsset]:
        """Obtener asset por ID"""
        pass

    @abstractmethod
    def get_by_user_id(self, user_id: UserId) -> List[UserAsset]:
        """Obtener todos los assets de un usuario"""
        pass

    @abstractmethod
    def get_by_user_and_type(self, user_id: UserId, asset_type: AssetTypeEnum) -> List[UserAsset]:
        """Obtener assets de un usuario por tipo"""
        pass

    @abstractmethod
    def delete(self, asset_id: UserAssetId) -> None:
        """Eliminar asset"""
        pass
