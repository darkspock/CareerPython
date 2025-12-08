from typing import List, Optional

from core.database import DatabaseInterface
from src.candidate_bc.candidate.domain.entities.file_attachment import FileAttachment
from src.candidate_bc.candidate.domain.repositories.file_attachment_repository_interface import \
    FileAttachmentRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.file_attachment_id import FileAttachmentId
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_bc.candidate.infrastructure.models.file_attachment_model import FileAttachmentModel


class SQLAlchemyFileAttachmentRepository(FileAttachmentRepositoryInterface):
    """SQLAlchemy implementation of file attachment repository"""

    def __init__(self, database: DatabaseInterface) -> None:
        self._database = database

    def _to_domain(self, model: FileAttachmentModel) -> FileAttachment:
        """Convert a database model to a domain entity"""
        return FileAttachment(
            id=FileAttachmentId.from_string(model.id),
            candidate_id=CandidateId.from_string(model.candidate_id),
            filename=model.filename,
            original_name=model.original_name,
            file_path=model.file_path,
            file_url=model.file_url,
            content_type=model.content_type,
            file_size=model.file_size,
            description=model.description,
            uploaded_at=model.uploaded_at,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: FileAttachment) -> FileAttachmentModel:
        """Convert a domain entity to a database model"""
        return FileAttachmentModel(
            id=entity.id.value,
            candidate_id=entity.candidate_id.value,
            filename=entity.filename,
            original_name=entity.original_name,
            file_path=entity.file_path,
            file_url=entity.file_url,
            content_type=entity.content_type,
            file_size=entity.file_size,
            description=entity.description,
            uploaded_at=entity.uploaded_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def save(self, file_attachment: FileAttachment) -> FileAttachment:
        """Save a file attachment to the database"""
        with self._database.get_session() as session:
            model = self._to_model(file_attachment)
            session.add(model)
            session.commit()
            session.refresh(model)
            return self._to_domain(model)

    def get_by_id(self, file_id: FileAttachmentId) -> Optional[FileAttachment]:
        """Get a file attachment by ID"""
        with self._database.get_session() as session:
            model = session.query(FileAttachmentModel).filter(
                FileAttachmentModel.id == file_id.value
            ).first()
            if model:
                return self._to_domain(model)
            return None

    def get_by_candidate_id(self, candidate_id: CandidateId) -> List[FileAttachment]:
        """Get all file attachments for a candidate"""
        with self._database.get_session() as session:
            models = session.query(FileAttachmentModel).filter(
                FileAttachmentModel.candidate_id == candidate_id.value
            ).order_by(FileAttachmentModel.uploaded_at.desc()).all()
            return [self._to_domain(model) for model in models]

    def delete(self, file_id: FileAttachmentId) -> bool:
        """Delete a file attachment"""
        with self._database.get_session() as session:
            model = session.query(FileAttachmentModel).filter(
                FileAttachmentModel.id == file_id.value
            ).first()
            if model:
                session.delete(model)
                session.commit()
                return True
            return False

    def delete_by_candidate_id(self, candidate_id: CandidateId) -> int:
        """Delete all file attachments for a candidate"""
        with self._database.get_session() as session:
            deleted_count: int = session.query(FileAttachmentModel).filter(
                FileAttachmentModel.candidate_id == candidate_id.value
            ).delete()
            session.commit()
            return deleted_count
