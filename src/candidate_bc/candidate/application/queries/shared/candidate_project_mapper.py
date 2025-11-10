from src.candidate_bc.candidate.application.queries.shared.candidate_project_dto import CandidateProjectDto
from src.candidate_bc.candidate.domain.entities.candidate_project import CandidateProject


class CandidateProjectMapper:
    @staticmethod
    def to_dto(project: CandidateProject) -> CandidateProjectDto:
        return CandidateProjectDto(
            id=project.id,
            candidate_id=project.candidate_id,
            name=project.name,
            description=project.description,
            start_date=project.start_date,
            end_date=project.end_date
        )
