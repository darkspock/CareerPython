from abc import abstractmethod, ABC
from typing import Optional, List

from src.candidate_bc.candidate.domain.entities.file_attachment import FileAttachment
from src.candidate_bc.candidate.domain.value_objects.file_attachment_id import FileAttachmentId
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId


class FileAttachmentRepositoryInterface(ABC):
    """Interface for file attachment repository"""

    @abstractmethod
    def save(self, file_attachment: FileAttachment) -> FileAttachment:
        """Save a file attachment to the database"""
        pass

    @abstractmethod
    def get_by_id(self, file_id: FileAttachmentId) -> Optional[FileAttachment]:
        """Get a file attachment by ID"""
        pass

    @abstractmethod
    def get_by_candidate_id(self, candidate_id: CandidateId) -> List[FileAttachment]:
        """Get all file attachments for a candidate"""
        pass

    @abstractmethod
    def delete(self, file_id: FileAttachmentId) -> bool:
        """Delete a file attachment"""
        pass

    @abstractmethod
    def delete_by_candidate_id(self, candidate_id: CandidateId) -> int:
        """Delete all file attachments for a candidate"""
        pass
