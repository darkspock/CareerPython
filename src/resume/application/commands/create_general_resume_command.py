from dataclasses import dataclass
from typing import Optional, Dict, Any, List

from src.candidate.application.queries.list_candidate_educations_by_candidate_id import \
    ListCandidateEducationsByCandidateIdQuery
from src.candidate.application.queries.list_candidate_experiences_by_candidate_id import \
    ListCandidateExperiencesByCandidateIdQuery
from src.candidate.application.queries.list_candidate_projects_by_candidate_id import \
    ListCandidateProjectsByCandidateIdQuery
from src.candidate.application.queries.shared.candidate_experience_dto import CandidateExperienceDto
from src.candidate.domain.entities import Candidate
from src.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.resume.application.services.resume_generation_service import ResumeGenerationService
from src.resume.domain.entities.resume import Resume
from src.resume.domain.repositories.resume_repository_interface import ResumeRepositoryInterface
from src.resume.domain.value_objects.resume_id import ResumeId
from src.shared.application.command_bus import Command, CommandHandler
from src.shared.application.query_bus import QueryBus


@dataclass
class CreateGeneralResumeCommand(Command):
    """Command to create a general resume"""
    candidate_id: CandidateId
    name: str
    include_ai_enhancement: bool = False
    general_data: Optional[Dict[str, Any]] = None


class CreateGeneralResumeCommandHandler(CommandHandler[CreateGeneralResumeCommand]):
    """Handler to create a general resume"""

    def __init__(
            self,
            resume_repository: ResumeRepositoryInterface,
            candidate_repository: CandidateRepositoryInterface,
            generation_service: ResumeGenerationService,
            query_bus: QueryBus
    ):
        self.resume_repository = resume_repository
        self.candidate_repository = candidate_repository
        self.generation_service = generation_service
        self.query_bus = query_bus

    def execute(self, command: CreateGeneralResumeCommand) -> None:
        """Handle the general resume creation command"""

        # 1. Verify that the candidate exists
        candidate = self.candidate_repository.get_by_id(command.candidate_id)
        if not candidate:
            raise ValueError(f"Candidate with id {command.candidate_id.value} not found")

        # 2. Create the resume in DRAFT state
        resume = Resume.create_general_resume(
            id=ResumeId.generate(),
            candidate_id=command.candidate_id,
            name=command.name,
            include_ai_enhancement=command.include_ai_enhancement,
            general_data=command.general_data
        )

        # 3. Save the initial resume
        created_resume = self.resume_repository.create(resume)

        # 4. Mark as completed immediately for simplicity
        # In a real scenario, this would be done in background
        try:
            created_resume.start_generation()

            # 5. Get candidate data for generation
            candidate_data = self._prepare_candidate_data(candidate, command.general_data)

            # 6. Generate content using the generation service
            from src.resume.domain.enums.resume_type import ResumeType

            # Generate basic content synchronously
            basic_content = self.generation_service.generate_basic_content(
                candidate_id=command.candidate_id,
                resume_type=ResumeType.GENERAL,
                candidate_data=candidate_data
            )

            # 7. Generate AI content if requested
            ai_content = None
            if command.include_ai_enhancement:
                try:
                    ai_content = self.generation_service.generate_ai_enhanced_content(
                        candidate_id=command.candidate_id,
                        resume_type=ResumeType.GENERAL,
                        basic_content=basic_content,
                        candidate_data=candidate_data
                    )
                except Exception:
                    # If AI fails, continue without AI content (will be handled in complete_generation)
                    pass

            # 8. Complete the generation (this handles both basic and AI content)
            created_resume.complete_generation(basic_content, ai_content)
            self.resume_repository.update(created_resume)

        except Exception as e:
            # In case of error, mark the resume as failed
            created_resume.fail_generation(str(e))
            self.resume_repository.update(created_resume)
            raise

    def _prepare_candidate_data(self, candidate: Candidate, general_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Prepare candidate data for generation"""
        candidate_data: Dict[str, Any] = {
            'name': candidate.name,
            'email': candidate.email,
            'phone': candidate.phone,
            'location': f"{candidate.city}, {candidate.country}",
            'city': candidate.city,
            'country': candidate.country,
            'job_category': candidate.job_category.value if candidate.job_category else 'Technology',
            'skills': candidate.skills or [],
            'current_roles': [role.value for role in candidate.current_roles] if candidate.current_roles else [],
            'expected_roles': [role.value for role in candidate.expected_roles] if candidate.expected_roles else [],
            'current_job_level': candidate.current_job_level.value if candidate.current_job_level else None,
            'expected_job_level': candidate.expected_job_level.value if candidate.expected_job_level else None,
            'linkedin_url': candidate.linkedin_url,
            'current_salary': candidate.current_annual_salary,
            'expected_salary': candidate.expected_annual_salary,
            'currency': candidate.currency,
            'languages': {lang.value: level.value for lang, level in
                          candidate.languages.items()} if candidate.languages else {},
            'work_modality': [modality.value for modality in
                              candidate.work_modality] if candidate.work_modality else [],
            'relocation': candidate.relocation,
            'candidate_notes': candidate.candidate_notes,
        }

        # Get candidate work experiences
        try:
            experiences_query = ListCandidateExperiencesByCandidateIdQuery(candidate.id)
            experiences_dtos: List[CandidateExperienceDto] = self.query_bus.query(experiences_query)

            # Convert experiences to a useful format for generation
            experiences_data = []
            for exp_dto in experiences_dtos:
                experience = {
                    'job_title': exp_dto.job_title,
                    'company': exp_dto.company,
                    'description': exp_dto.description or '',
                    'start_date': exp_dto.start_date.isoformat() if exp_dto.start_date else None,
                    'end_date': exp_dto.end_date.isoformat() if exp_dto.end_date else None,
                    'is_current': exp_dto.end_date is None  # If there's no end date, it's current job
                }
                experiences_data.append(experience)

            # Sort by start date (most recent first)
            experiences_data.sort(key=lambda x: x['start_date'] or '1900-01-01', reverse=True)
            candidate_data['experiences'] = experiences_data

        except Exception as e:
            print(f"Warning: Could not fetch candidate experiences: {e}")
            candidate_data['experiences'] = []

        # Get candidate education
        try:
            educations_query = ListCandidateEducationsByCandidateIdQuery(candidate.id)
            educations_dtos: List[Any] = self.query_bus.query(educations_query)

            # Convert educations to format for generation
            educations_data = []
            for edu_dto in educations_dtos:
                education = {
                    'institution': edu_dto.institution,
                    'degree': edu_dto.degree,
                    'field_of_study': '',  # Not available in current DTO
                    'start_date': edu_dto.start_date.isoformat() if edu_dto.start_date else None,
                    'end_date': edu_dto.end_date.isoformat() if edu_dto.end_date else None,
                    'description': edu_dto.description or ''
                }
                educations_data.append(education)

            candidate_data['educations'] = educations_data

        except Exception as e:
            print(f"Warning: Could not fetch candidate educations: {e}")
            candidate_data['educations'] = []

        # Get candidate projects
        try:
            projects_query = ListCandidateProjectsByCandidateIdQuery(candidate.id)
            projects_dtos: List[Any] = self.query_bus.query(projects_query)

            # Convert projects to format for generation
            projects_data = []
            for proj_dto in projects_dtos:
                project = {
                    'name': proj_dto.name,
                    'description': proj_dto.description or '',
                    'technologies': [],  # Not available in current DTO
                    'url': '',  # Not available in current DTO
                    'start_date': proj_dto.start_date.isoformat() if proj_dto.start_date else None,
                    'end_date': proj_dto.end_date.isoformat() if proj_dto.end_date else None
                }
                projects_data.append(project)

            candidate_data['projects'] = projects_data

        except Exception as e:
            print(f"Warning: Could not fetch candidate projects: {e}")
            candidate_data['projects'] = []

        # Add additional data if available
        if general_data:
            candidate_data.update(general_data)

        return candidate_data
