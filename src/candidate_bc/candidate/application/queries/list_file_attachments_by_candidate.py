from dataclasses import dataclass
from typing import List

from src.candidate_bc.candidate.application.queries.shared.file_attachment_dto import FileAttachmentDto
from src.candidate_bc.candidate.domain.repositories.file_attachment_repository_interface import \
    FileAttachmentRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class ListFileAttachmentsByCandidateQuery(Query):
    candidate_id: CandidateId


class ListFileAttachmentsByCandidateQueryHandler(
    QueryHandler[ListFileAttachmentsByCandidateQuery, List[FileAttachmentDto]]
):
    def __init__(self, file_attachment_repository: FileAttachmentRepositoryInterface):
        self.file_attachment_repository = file_attachment_repository

    def handle(self, query: ListFileAttachmentsByCandidateQuery) -> List[FileAttachmentDto]:
        file_attachments = self.file_attachment_repository.get_by_candidate_id(query.candidate_id)
        return [FileAttachmentDto.from_entity(fa) for fa in file_attachments]
