from src.candidate.application.queries.shared.candidate_experience_dto import CandidateExperienceDto
from src.candidate.domain.entities import CandidateExperience


class CandidateExperienceMapper:
    @staticmethod
    def to_dto(experience: CandidateExperience) -> CandidateExperienceDto:
        return CandidateExperienceDto(
            id=experience.id,
            candidate_id=experience.candidate_id,
            job_title=experience.job_title,
            company=experience.company,
            description=experience.description,
            start_date=experience.start_date,
            end_date=experience.end_date
        )
