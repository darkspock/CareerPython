from src.candidate_bc.candidate.application.queries.shared.candidate_dto import CandidateDto
from src.candidate_bc.candidate.domain.entities import Candidate


class CandidateDtoMapper:
    @staticmethod
    def from_model(candidate: Candidate) -> CandidateDto:
        return CandidateDto(
            id=candidate.id,
            name=candidate.name,
            date_of_birth=candidate.date_of_birth,
            city=candidate.city,
            country=candidate.country,
            phone=candidate.phone,
            email=candidate.email,
            user_id=candidate.user_id,
            status=candidate.status,
            job_category=candidate.job_category,
            linkedin_url=candidate.linkedin_url,
            created_at=candidate.created_on,
            updated_at=candidate.updated_on,
            expected_annual_salary=candidate.expected_annual_salary,
            current_annual_salary=candidate.current_annual_salary,
            currency=candidate.currency,
            relocation=candidate.relocation,
            work_modality=candidate.work_modality,
            languages=candidate.languages,
            skills=candidate.skills,
            current_roles=candidate.current_roles,
            expected_roles=candidate.expected_roles,
            type=candidate.candidate_type
        )
