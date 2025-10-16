from src.candidate.application.queries.shared.candidate_education_dto import CandidateEducationDto
from src.candidate.domain.entities import CandidateEducation


class CandidateEducationMapper:
    @staticmethod
    def to_dto(education: CandidateEducation) -> CandidateEducationDto:
        return CandidateEducationDto(
            id=education.id,
            candidate_id=education.candidate_id,
            institution=education.institution,
            degree=education.degree,
            description=education.description,
            start_date=education.start_date,
            end_date=education.end_date,
            created_at=education.created_at,
            updated_at=education.updated_at
        )
