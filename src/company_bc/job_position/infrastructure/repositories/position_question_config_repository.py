from typing import Optional, List, Any

from src.company_bc.job_position.domain.entities.position_question_config import (
    PositionQuestionConfig
)
from src.company_bc.job_position.domain.repositories.position_question_config_repository_interface import (
    PositionQuestionConfigRepositoryInterface
)
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.company_bc.job_position.domain.value_objects.position_question_config_id import (
    PositionQuestionConfigId
)
from src.company_bc.job_position.infrastructure.models.position_question_config_model import (
    PositionQuestionConfigModel
)
from src.shared_bc.customization.workflow.domain.value_objects.application_question_id import (
    ApplicationQuestionId
)


class PositionQuestionConfigRepository(PositionQuestionConfigRepositoryInterface):
    """Repository implementation for PositionQuestionConfig entity."""

    def __init__(self, database: Any) -> None:
        self._database = database

    def get_by_id(self, config_id: PositionQuestionConfigId) -> Optional[PositionQuestionConfig]:
        """Get a position question config by ID."""
        with self._database.get_session() as session:
            model = session.query(PositionQuestionConfigModel).filter_by(
                id=str(config_id)
            ).first()
            if model:
                return self._to_domain(model)
            return None

    def get_by_position_and_question(
        self,
        position_id: JobPositionId,
        question_id: ApplicationQuestionId
    ) -> Optional[PositionQuestionConfig]:
        """Get config for a specific position and question combination."""
        with self._database.get_session() as session:
            model = session.query(PositionQuestionConfigModel).filter_by(
                position_id=str(position_id),
                question_id=str(question_id)
            ).first()
            if model:
                return self._to_domain(model)
            return None

    def list_by_position(
        self,
        position_id: JobPositionId,
        enabled_only: bool = False
    ) -> List[PositionQuestionConfig]:
        """List all question configs for a position."""
        with self._database.get_session() as session:
            query = session.query(PositionQuestionConfigModel).filter_by(
                position_id=str(position_id)
            )
            if enabled_only:
                query = query.filter_by(enabled=True)
            models = query.all()
            return [self._to_domain(model) for model in models]

    def save(self, config: PositionQuestionConfig) -> None:
        """Save a position question config (insert or update)."""
        model = self._to_model(config)
        with self._database.get_session() as session:
            existing = session.query(PositionQuestionConfigModel).filter_by(
                id=str(config.id)
            ).first()
            if existing:
                session.merge(model)
            else:
                session.add(model)
            session.commit()

    def delete(self, config_id: PositionQuestionConfigId) -> None:
        """Delete a position question config."""
        with self._database.get_session() as session:
            session.query(PositionQuestionConfigModel).filter_by(
                id=str(config_id)
            ).delete()
            session.commit()

    def delete_by_position(self, position_id: JobPositionId) -> int:
        """Delete all configs for a position. Returns count of deleted records."""
        with self._database.get_session() as session:
            count: int = session.query(PositionQuestionConfigModel).filter_by(
                position_id=str(position_id)
            ).delete()
            session.commit()
            return count

    def delete_by_question(self, question_id: ApplicationQuestionId) -> int:
        """Delete all configs for a question. Returns count of deleted records."""
        with self._database.get_session() as session:
            count: int = session.query(PositionQuestionConfigModel).filter_by(
                question_id=str(question_id)
            ).delete()
            session.commit()
            return count

    def _to_domain(self, model: PositionQuestionConfigModel) -> PositionQuestionConfig:
        """Convert model to domain entity."""
        return PositionQuestionConfig(
            id=PositionQuestionConfigId.from_string(str(model.id)),
            position_id=JobPositionId.from_string(str(model.position_id)),
            question_id=ApplicationQuestionId.from_string(str(model.question_id)),
            enabled=bool(model.enabled),
            is_required_override=model.is_required_override,
            sort_order_override=model.sort_order_override,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: PositionQuestionConfig) -> PositionQuestionConfigModel:
        """Convert domain entity to model."""
        return PositionQuestionConfigModel(
            id=str(entity.id.value),
            position_id=str(entity.position_id.value),
            question_id=str(entity.question_id.value),
            enabled=entity.enabled,
            is_required_override=entity.is_required_override,
            sort_order_override=entity.sort_order_override,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
