from dataclasses import dataclass
from typing import Optional

from src.candidate_bc.candidate.application.queries.shared.file_attachment_dto import FileAttachmentDto
from src.candidate_bc.candidate.domain.repositories.file_attachment_repository_interface import \
    FileAttachmentRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.file_attachment_id import FileAttachmentId
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetFileAttachmentByIdQuery(Query):
    file_id: FileAttachmentId


class GetFileAttachmentByIdQueryHandler(QueryHandler[GetFileAttachmentByIdQuery, Optional[FileAttachmentDto]]):
    def __init__(self, file_attachment_repository: FileAttachmentRepositoryInterface):
        self.file_attachment_repository = file_attachment_repository

    def handle(self, query: GetFileAttachmentByIdQuery) -> Optional[FileAttachmentDto]:
        file_attachment = self.file_attachment_repository.get_by_id(query.file_id)
        if file_attachment:
            return FileAttachmentDto.from_entity(file_attachment)
        return None
