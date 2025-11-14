from typing import Optional, List

from sqlalchemy.orm import Session

from core.database import DatabaseInterface
from src.auth_bc.user.domain.entities.user_asset import UserAsset
from src.auth_bc.user.domain.enums.asset_enums import AssetTypeEnum, ProcessingStatusEnum
from src.auth_bc.user.domain.repositories.user_asset_repository_interface import UserAssetRepositoryInterface
from src.auth_bc.user.domain.value_objects.UserId import UserId
from src.auth_bc.user.domain.value_objects.user_asset_id import UserAssetId
from src.auth_bc.user.infrastructure.models.user_asset_model import UserAssetModel
from src.framework.infrastructure.repositories.base import BaseRepository


class SQLAlchemyUserAssetRepository(UserAssetRepositoryInterface):
    """Implementación de repositorio de assets de usuario con SQLAlchemy"""

    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.base_repo = BaseRepository(database, UserAssetModel)

    def _to_domain(self, model: UserAssetModel) -> UserAsset:
        """Convierte modelo de SQLAlchemy a entidad de dominio"""
        return UserAsset(
            id=UserAssetId(model.id),
            user_id=UserId(model.user_id),
            asset_type=AssetTypeEnum(model.asset_type),
            content=model.content,
            created_at=model.created_at,
            updated_at=model.updated_at,
            file_name=model.file_name,
            file_size=model.file_size,
            content_type=model.content_type,
            processing_status=ProcessingStatusEnum(model.processing_status),
            processing_error=model.processing_error,
            text_content=model.text_content,
            file_metadata=model.file_metadata or {}
        )

    def _to_model(self, entity: UserAsset) -> UserAssetModel:
        """Convierte entidad de dominio a modelo de SQLAlchemy"""
        return UserAssetModel(
            id=entity.id.value,
            user_id=entity.user_id.value,
            asset_type=entity.asset_type,
            content=entity.content,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            file_name=entity.file_name,
            file_size=entity.file_size,
            content_type=entity.content_type,
            processing_status=entity.processing_status,
            processing_error=entity.processing_error,
            text_content=entity.text_content,
            file_metadata=entity.file_metadata or {}
        )

    def save(self, user_asset: UserAsset) -> None:
        """Guardar un asset de usuario"""
        session: Session = self.database.get_session()
        try:
            existing_model = session.query(UserAssetModel).filter_by(
                id=user_asset.id.value
            ).first()

            if existing_model:
                # Update existing
                existing_model.user_id = user_asset.user_id.value
                existing_model.asset_type = user_asset.asset_type
                existing_model.content = user_asset.content
                existing_model.updated_at = user_asset.updated_at
                existing_model.file_name = user_asset.file_name
                existing_model.file_size = user_asset.file_size
                existing_model.content_type = user_asset.content_type
                existing_model.processing_status = user_asset.processing_status
                existing_model.processing_error = user_asset.processing_error
                existing_model.text_content = user_asset.text_content
                existing_model.file_metadata = user_asset.file_metadata or {}
            else:
                # Create new
                model = self._to_model(user_asset)
                session.add(model)

            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_by_id(self, asset_id: UserAssetId) -> Optional[UserAsset]:
        """Obtener asset por ID"""
        model = self.base_repo.get_by_id(asset_id)
        return self._to_domain(model) if model else None

    def get_by_user_id(self, user_id: UserId) -> List[UserAsset]:
        """Obtener todos los assets de un usuario"""
        session: Session = self.database.get_session()
        try:
            models = session.query(UserAssetModel).filter_by(
                user_id=user_id.value
            ).all()
            return [self._to_domain(model) for model in models]
        finally:
            session.close()

    def get_by_user_and_type(self, user_id: UserId, asset_type: AssetTypeEnum) -> List[UserAsset]:
        """Obtener assets de un usuario por tipo"""
        session: Session = self.database.get_session()
        try:
            models = session.query(UserAssetModel).filter_by(
                user_id=user_id.value,
                asset_type=asset_type
            ).all()
            return [self._to_domain(model) for model in models]
        finally:
            session.close()

    def delete(self, asset_id: UserAssetId) -> None:
        """Eliminar asset"""
        session: Session = self.database.get_session()
        try:
            model = session.query(UserAssetModel).filter_by(
                id=asset_id.value
            ).first()
            if model:
                session.delete(model)
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
