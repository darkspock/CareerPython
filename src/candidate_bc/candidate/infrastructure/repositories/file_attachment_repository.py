from typing import List, Optional
from src.candidate_bc.candidate.infrastructure.models.file_attachment_model import FileAttachmentModel
from core.database import database


class FileAttachmentRepository:
    """Repository for file attachment operations"""

    def __init__(self) -> None:
        self._database = database

    def save(self, file_attachment: FileAttachmentModel) -> FileAttachmentModel:
        """Save a file attachment to the database"""
        with self._database.get_session() as session:
            session.add(file_attachment)
            session.commit()
            session.refresh(file_attachment)
            return file_attachment

    def get_by_id(self, file_id: str) -> Optional[FileAttachmentModel]:
        """Get a file attachment by ID"""
        with self._database.get_session() as session:
            return session.query(FileAttachmentModel).filter(
                FileAttachmentModel.id == file_id
            ).first()

    def get_by_candidate_id(self, candidate_id: str) -> List[FileAttachmentModel]:
        """Get all file attachments for a candidate"""
        with self._database.get_session() as session:
            return session.query(FileAttachmentModel).filter(
                FileAttachmentModel.candidate_id == candidate_id
            ).order_by(FileAttachmentModel.uploaded_at.desc()).all()

    def delete(self, file_id: str) -> bool:
        """Delete a file attachment"""
        with self._database.get_session() as session:
            file_attachment = session.query(FileAttachmentModel).filter(
                FileAttachmentModel.id == file_id
            ).first()
            if file_attachment:
                session.delete(file_attachment)
                session.commit()
                return True
            return False

    def delete_by_candidate_id(self, candidate_id: str) -> int:
        """Delete all file attachments for a candidate"""
        with self._database.get_session() as session:
            deleted_count = session.query(FileAttachmentModel).filter(
                FileAttachmentModel.candidate_id == candidate_id
            ).delete()
            session.commit()
            return deleted_count
