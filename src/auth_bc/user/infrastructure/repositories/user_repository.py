from datetime import date
from typing import Optional, List, Any, Dict

from sqlalchemy import and_, func, extract

from core.database import DatabaseInterface
from src.framework.infrastructure.repositories.base import BaseRepository
from src.auth_bc.user.domain.entities.user import User
from src.auth_bc.user.domain.repositories.user_repository_interface import UserRepositoryInterface
from src.auth_bc.user.domain.value_objects.UserId import UserId
from src.auth_bc.user.infrastructure.models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepositoryInterface):
    """Implementación de repositorio de usuarios con SQLAlchemy"""

    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.base_repo = BaseRepository(database, UserModel)

    @staticmethod
    def _to_domain(model: UserModel) -> User:
        """Convierte modelo de SQLAlchemy a entidad de dominio"""
        return User(
            id=UserId.from_string(model.id),
            email=model.email,
            hashed_password=model.hashed_password,
            is_active=model.is_active,
            subscription_tier=model.subscription_tier,
            subscription_expires_at=model.subscription_expires_at,
            password_reset_token=model.password_reset_token,
            password_reset_expires_at=model.password_reset_expires_at,
            preferred_language=model.preferred_language
        )

    @staticmethod
    def _to_model(domain: User) -> UserModel:
        """Convierte entidad de dominio a modelo de SQLAlchemy"""
        return UserModel(
            id=domain.id.value,
            email=domain.email,
            hashed_password=domain.hashed_password,
            is_active=domain.is_active,
            subscription_tier=domain.subscription_tier,
            subscription_expires_at=domain.subscription_expires_at,
            password_reset_token=domain.password_reset_token,
            password_reset_expires_at=domain.password_reset_expires_at,
            preferred_language=domain.preferred_language
        )

    def create(self, user: User) -> None:
        model = self._to_model(user)
        self.base_repo.create(model)

    def get_by_id(self, id: UserId) -> Optional[User]:
        model = self.base_repo.get_by_id(id)
        if model:
            return self._to_domain(model)
        return None

    def get_by_email(self, email: str) -> Optional[User]:
        session = self.database.get_session()
        model = session.query(UserModel).filter(UserModel.email == email).first()
        if model:
            return self._to_domain(model)
        return None

    def get_user_auth_data_by_email(self, email: str) -> Optional[User]:
        session = self.database.get_session()
        print(f"[SQLAlchemyUserRepository] get_user_auth_data_by_email - Session ID: {id(session)}")
        model = session.query(UserModel).filter(UserModel.email == email).first()
        print(f"[SQLAlchemyUserRepository] Query result for email {email}: {model}")
        if model:
            return self._to_domain(model)
        return None

    def get_all(self) -> List[User]:
        session = self.database.get_session()
        models = session.query(UserModel).all()
        return [self._to_domain(model) for model in models]

    def update(self, user_id: UserId, user_data: dict[str, Any]) -> Optional[User]:
        updated_model = self.base_repo.update(user_id, user_data)
        if updated_model:
            return self._to_domain(updated_model)
        return None

    def update_entity(self, user: User) -> User:
        """Update user entity directly"""
        session = self.database.get_session()
        model = session.query(UserModel).filter(UserModel.id == user.id.value).first()
        if model:
            model.email = user.email
            model.hashed_password = user.hashed_password
            model.is_active = user.is_active
            model.subscription_tier = user.subscription_tier
            model.subscription_expires_at = user.subscription_expires_at
            model.password_reset_token = user.password_reset_token
            model.password_reset_expires_at = user.password_reset_expires_at
            model.preferred_language = user.preferred_language
            session.commit()
            session.refresh(model)
            return self._to_domain(model)
        raise ValueError(f"User with id {user.id.value} not found")

    def delete(self, user_id: UserId) -> bool:
        return self.base_repo.delete(user_id)

    def get_by_reset_token(self, reset_token: str) -> Optional[User]:
        """Get user by password reset token"""
        session = self.database.get_session()
        model = session.query(UserModel).filter(
            UserModel.password_reset_token == reset_token
        ).first()
        if model:
            return self._to_domain(model)
        return None

    def list_with_filters(self, filters: Dict[str, Any], limit: int = 50, offset: int = 0,
                          sort_by: str = "created_at", sort_order: str = "desc") -> List[User]:
        """List users with advanced filtering"""
        session = self.database.get_session()
        query = session.query(UserModel)

        # Apply filters
        conditions = []

        if 'email' in filters:
            conditions.append(UserModel.email.ilike(f"%{filters['email']}%"))

        if 'is_active' in filters:
            conditions.append(UserModel.is_active == filters['is_active'])

        if 'created_after' in filters:
            conditions.append(func.date(UserModel.created_at) >= filters['created_after'])

        if 'created_before' in filters:
            conditions.append(func.date(UserModel.created_at) <= filters['created_before'])

        if 'last_login_after' in filters and hasattr(UserModel, 'last_login'):
            conditions.append(func.date(UserModel.last_login) >= filters['last_login_after'])

        if 'last_login_before' in filters and hasattr(UserModel, 'last_login'):
            conditions.append(func.date(UserModel.last_login) <= filters['last_login_before'])

        if 'search_term' in filters:
            search_term = f"%{filters['search_term']}%"
            conditions.append(UserModel.email.ilike(search_term))

        if conditions:
            query = query.filter(and_(*conditions))

        # Apply sorting
        from sqlalchemy.orm import InstrumentedAttribute
        from typing import Any
        sort_column: InstrumentedAttribute[Any]

        if sort_by == "email":
            sort_column = UserModel.email
        elif sort_by == "last_login" and hasattr(UserModel, 'last_login'):
            sort_column = UserModel.last_login
        else:
            sort_column = UserModel.created_at

        if sort_order.lower() == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        # Apply pagination
        query = query.offset(offset).limit(limit)

        models = query.all()
        return [self._to_domain(model) for model in models]

    def count_all(self) -> int:
        """Count total number of users"""
        session = self.database.get_session()
        return session.query(UserModel).count()

    def count_by_status(self, is_active: bool) -> int:
        """Count users by active status"""
        session = self.database.get_session()
        return session.query(UserModel).filter(UserModel.is_active == is_active).count()

    def count_created_after(self, date_threshold: date) -> int:
        """Count users created after specific date"""
        session = self.database.get_session()
        return session.query(UserModel).filter(
            func.date(UserModel.created_at) >= date_threshold
        ).count()

    def count_with_login_after(self, date_threshold: date) -> int:
        """Count users with login after specific date"""
        session = self.database.get_session()
        if hasattr(UserModel, 'last_login'):
            return session.query(UserModel).filter(
                func.date(UserModel.last_login) >= date_threshold
            ).count()
        return 0

    def count_never_logged_in(self) -> int:
        """Count users who never logged in"""
        session = self.database.get_session()
        if hasattr(UserModel, 'last_login'):
            return session.query(UserModel).filter(UserModel.last_login.is_(None)).count()
        return 0

    def get_monthly_registration_trend(self, months: int = 12) -> List[Dict[str, Any]]:
        """Get monthly registration trend for the last N months"""
        session = self.database.get_session()

        # Get monthly counts
        monthly_data = session.query(
            extract('year', UserModel.created_at).label('year'),
            extract('month', UserModel.created_at).label('month'),
            func.count(UserModel.id).label('count')
        ).group_by(
            extract('year', UserModel.created_at),
            extract('month', UserModel.created_at)
        ).order_by(
            extract('year', UserModel.created_at).desc(),
            extract('month', UserModel.created_at).desc()
        ).limit(months).all()

        return [
            {
                'year': int(row.year),
                'month': int(row.month),
                'count': row.count,
                'period': f"{int(row.year)}-{int(row.month):02d}"
            }
            for row in monthly_data
        ]
