from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Optional, List, Any

from sqlalchemy.exc import IntegrityError

from core.database import DatabaseInterface
from src.shared.domain.exceptions import ValidationException
from src.shared.domain.value_objects.base_id import BaseId

# Tipo genérico para entidades
T = TypeVar('T')


class RepositoryInterface(ABC, Generic[T]):
    """Interfaz genérica para repositorios"""

    @abstractmethod
    def create(self, entity: T) -> T:
        """Crea una nueva entidad"""
        pass

    @abstractmethod
    def get_by_id(self, entity_id: BaseId) -> Optional[T]:
        """Obtiene una entidad por ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """Obtiene todas las entidades"""
        pass

    @abstractmethod
    def update(self, entity_id: BaseId, entity_data: dict[str, Any]) -> Optional[T]:
        """Actualiza una entidad"""
        pass

    @abstractmethod
    def delete(self, entity_id: BaseId) -> bool:
        """Elimina una entidad"""
        pass


class BaseRepository(RepositoryInterface[T]):
    """Implementación base de repositorio"""

    def __init__(self, database: DatabaseInterface, model: Type[T]):
        self.database = database
        self.model = model

    def create(self, entity: T) -> T:
        with self.database.get_session() as session:
            try:
                session.add(entity)
                session.commit()
                session.refresh(entity)
                return entity
            except IntegrityError as e:
                session.rollback()
                # Check if it's a unique constraint violation for email
                if "email" in str(e.orig).lower() and (
                        "unique" in str(e.orig).lower() or "duplicate" in str(e.orig).lower()):
                    raise ValidationException(
                        "Este email ya está registrado. ¿Ya tienes una cuenta? Puedes iniciar sesión.")
                # Re-raise other integrity errors
                raise ValidationException(f"Error de integridad de datos: {str(e.orig)}")
            except Exception:
                session.rollback()
                raise

    def get_by_id(self, id: BaseId) -> Optional[T]:
        with self.database.get_session() as session:
            return session.query(self.model).filter(self.model.id == id.value).first()  # type: ignore

    def get_all(self) -> List[T]:
        with self.database.get_session() as session:
            return session.query(self.model).all()

    def update(self, entity_id: BaseId, entity_data: dict[str, Any]) -> Optional[T]:
        with self.database.get_session() as session:
            db_entity = session.query(self.model).filter(self.model.id == entity_id.value).first()  # type: ignore
            if db_entity:
                for key, value in entity_data.items():
                    setattr(db_entity, key, value)
                session.commit()
                session.refresh(db_entity)
                return db_entity
            return None

    def delete(self, id: BaseId) -> bool:
        with self.database.get_session() as session:
            entity = session.query(self.model).filter(self.model.id == id.value).first()  # type: ignore
            if entity:
                session.delete(entity)
                session.commit()
                return True
            return False
