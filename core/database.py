from contextvars import ContextVar
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Optional, List, Generator, Any
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy import create_engine, text  # type: ignore
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, DisconnectionError
import logging

from core.config import settings
from core.base import Base

# Configuración robusta de la base de datos
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=30,
    pool_timeout=30,  # Segundos para esperar por una conexión
    pool_recycle=3600,  # Reciclar conexiones cada hora
    pool_pre_ping=True,  # Verificar conexiones antes de usarlas
    echo=False  # No logging SQL en producción
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Context variable to store the session
db_session: ContextVar[Session] = ContextVar("db_session")  # type: ignore

# Tipo genérico para entidades
T = TypeVar('T')


def get_db() -> Generator[Session, None, None]: # type: ignore
    db = SessionLocal()
    db_session.set(db)
    try:
        yield db
    finally:
        db.close()


class DatabaseInterface(ABC):
    """Interfaz para operaciones de base de datos"""

    @abstractmethod
    def get_session(self) -> Session:  # type: ignore
        """Obtiene una sesión de base de datos"""
        pass


class SQLAlchemyDatabase(DatabaseInterface):
    """Implementación concreta usando SQLAlchemy con manejo robusto de errores"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_session(self) -> Session:  # type: ignore
        try:
            return db_session.get()
        except LookupError:
            # This will happen if the context is not set,
            # for example when running outside of a request.
            # In this case, we return a new session.
            return self._create_session()

    def _create_session(self) -> Session:  # type: ignore
        """Create a new session with error handling"""
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                session = SessionLocal()
                # Test the connection
                session.execute(text("SELECT 1"))
                return session
            except (OperationalError, DisconnectionError) as e:
                retry_count += 1
                self.logger.warning(f"Database connection attempt {retry_count} failed: {str(e)}")

                if retry_count >= max_retries:
                    self.logger.error("Max database connection retries exceeded")
                    raise

                # Dispose engine to force new connections
                engine.dispose()

        # This should never be reached, but just in case
        return SessionLocal()

    @property
    def engine(self):
        """Expose engine for middleware access"""
        return engine


class RepositoryInterface(ABC, Generic[T]):
    """Interfaz genérica para repositorios"""

    @abstractmethod
    def create(self, entity: T) -> T:
        """Crea una nueva entidad"""
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """Obtiene una entidad por ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """Obtiene todas las entidades"""
        pass

    @abstractmethod
    def update(self, entity_id: str, entity_data: dict[str,Any]) -> Optional[T]:
        """Actualiza una entidad"""
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Elimina una entidad"""
        pass


class BaseRepository(RepositoryInterface[T]):
    """Implementación base de repositorio"""

    def __init__(self, database: DatabaseInterface, model: Type[T]):
        self.database = database
        self.model = model

    def create(self, entity: T) -> T:
        with self.database.get_session() as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    def get_by_id(self, entity_id: str) -> Optional[T]:
        with self.database.get_session() as session:
            return session.query(self.model).filter(self.model.id == entity_id).first()  # type: ignore

    def get_all(self) -> List[T]:
        with self.database.get_session() as session:
            return session.query(self.model).all()  # type: ignore

    def update(self, entity_id: str, entity_data: dict[str,Any]) -> Optional[T]:
        with self.database.get_session() as session:
            entity = session.query(self.model).filter(self.model.id == entity_id).first()  # type: ignore
            if entity:
                for key, value in entity_data.items():
                    setattr(entity, key, value)
                session.commit()
                session.refresh(entity)
                return entity # type: ignore
            return None

    def delete(self, entity_id: str) -> bool:
        with self.database.get_session() as session:
            entity = session.query(self.model).filter(self.model.id == entity_id).first() # type: ignore
            if entity:
                session.delete(entity)
                session.commit()
                return True
            return False


# Instancia global de la base de datos
database = SQLAlchemyDatabase()