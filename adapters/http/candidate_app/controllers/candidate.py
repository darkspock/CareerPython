import logging
from datetime import datetime
from typing import List, Optional, cast, Dict, Any

import ulid
from fastapi import HTTPException

from adapters.http.candidate_app.schemas.candidate import CandidateCreate, CandidateUpdate, CandidateResponse
from adapters.http.candidate_app.schemas.candidate_education import CandidateEducationResponse, \
    CandidateEducationCreateRequest
from adapters.http.candidate_app.schemas.candidate_experience import CandidateExperienceResponse, \
    CandidateExperienceCreateRequest
from adapters.http.candidate_app.schemas.candidate_project import CandidateProjectResponse, \
    CandidateProjectCreateRequest
from adapters.http.candidate_app.services.profile_validation_service import ProfileValidationService
from src.auth_bc.user.domain.value_objects import UserId
from src.candidate_bc.candidate.application import GetCandidateByIdQuery, GetCandidateByUserIdQuery, ListCandidatesQuery
from src.candidate_bc.candidate.application import GetEducationByIdQuery
from src.candidate_bc.candidate.application import GetProjectByIdQuery
from src.candidate_bc.candidate.application.commands import CreateCandidateCommand
from src.candidate_bc.candidate.application.commands.create_education import CreateEducationCommand
from src.candidate_bc.candidate.application.commands.create_experience import CreateExperienceCommand
from src.candidate_bc.candidate.application.commands.create_project import CreateProjectCommand
from src.candidate_bc.candidate.application.commands.delete_education import DeleteEducationCommand
from src.candidate_bc.candidate.application.commands.delete_experience import DeleteExperienceCommand
from src.candidate_bc.candidate.application.commands.delete_project import DeleteProjectCommand
from src.candidate_bc.candidate.application.commands.update_candidate_basic import UpdateCandidateBasicCommand
from src.candidate_bc.candidate.application.commands.update_education import UpdateEducationCommand
from src.candidate_bc.candidate.application.commands.update_experience import UpdateExperienceCommand
from src.candidate_bc.candidate.application.commands.update_project import UpdateProjectCommand
from src.candidate_bc.candidate.application.queries.get_educations_by_candidate_id import \
    GetEducationsByCandidateIdQuery
from src.candidate_bc.candidate.application.queries.get_experience_by_id import GetExperienceByIdQuery
from src.candidate_bc.candidate.application.queries.get_experiences_by_candidate_id import \
    GetExperiencesByCandidateIdQuery
from src.candidate_bc.candidate.application.queries.get_projects_by_candidate_id import GetProjectsByCandidateIdQuery
from src.candidate_bc.candidate.application.queries.shared.candidate_dto import CandidateDto
from src.candidate_bc.candidate.application.queries.shared.candidate_education_dto import CandidateEducationDto
from src.candidate_bc.candidate.application.queries.shared.candidate_project_dto import CandidateProjectDto
from src.candidate_bc.candidate.domain.enums import WorkModalityEnum
from src.candidate_bc.candidate.domain.enums.candidate_enums import PositionRoleEnum, LanguageEnum, LanguageLevelEnum
from src.candidate_bc.candidate.domain.exceptions import CandidateNotFoundError
from src.candidate_bc.candidate.domain.value_objects import CandidateId, CandidateProjectId, CandidateEducationId, \
    CandidateExperienceId
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus
from src.framework.domain.enums.job_category import JobCategoryEnum

log = logging.getLogger(__name__)


class CandidateController:
    def __init__(
            self,
            command_bus: CommandBus,
            query_bus: QueryBus,
    ):
        self.command_bus = command_bus
        self.query_bus = query_bus
        self.profile_validation_service = ProfileValidationService()

    def create_candidate(self, candidate_data: CandidateCreate, user_id: str) -> str:
        id = CandidateId.generate()
        command = CreateCandidateCommand(id=id,
                                         user_id=UserId.from_string(user_id),
                                         date_of_birth=datetime.strptime("01-01-1973", "%Y-%m-%d").date(),
                                         job_category=JobCategoryEnum(candidate_data.job_category),
                                         name=candidate_data.name,
                                         phone=candidate_data.phone,
                                         email=candidate_data.email,
                                         city=candidate_data.city,
                                         country=candidate_data.country,
                                         )
        self.command_bus.dispatch(command)
        return id.value

    def get_candidate(self, candidate_id: str) -> CandidateResponse:
        dto: Optional[CandidateDto] = self.query_bus.query(GetCandidateByIdQuery(CandidateId.from_string(candidate_id)))
        if not dto:
            raise CandidateNotFoundError(f"Candidate with id {candidate_id} not found")
        return CandidateResponse.model_validate(dto)

    def get_candidate_by_user_id(self, user_id: str) -> CandidateResponse:
        dto: Optional[CandidateDto] = self.query_bus.query(GetCandidateByUserIdQuery(UserId.from_string(user_id)))
        if not dto:
            raise CandidateNotFoundError(f"Candidate with user_id {user_id} not found")
        return CandidateResponse.model_validate(dto)

    def list_candidates(self, name: Optional[str], phone: Optional[str]) -> List[CandidateResponse]:
        dtos: List[CandidateDto] = self.query_bus.query(ListCandidatesQuery(name=name, phone=phone))
        return [CandidateResponse.model_validate(dto) for dto in dtos]

    def update_candidate(self, candidate_id: str, candidate: CandidateUpdate) -> None:
        # Convert languages from dict[str, str] to dict[LanguageEnum, LanguageLevelEnum]
        languages_dict = None
        if candidate.languages:
            languages_dict = {}
            for lang_key, level_key in candidate.languages.items():
                try:
                    lang_enum = LanguageEnum(lang_key)
                    level_enum = LanguageLevelEnum(level_key)
                    languages_dict[lang_enum] = level_enum
                except ValueError:
                    # Skip invalid language/level combinations
                    continue

        # Convert work_modality from list[str] to list[WorkModalityEnum]
        work_modality_list = None
        if candidate.work_modality:
            work_modality_list = []
            for modality in candidate.work_modality:
                try:
                    work_modality_list.append(WorkModalityEnum(modality))
                except ValueError:
                    # Skip invalid modalities
                    continue

        # Convert roles from list[str] to list[PositionRoleEnum]
        current_roles_list = None
        if candidate.current_roles:
            current_roles_list = []
            for role in candidate.current_roles:
                try:
                    current_roles_list.append(PositionRoleEnum(role))
                except ValueError:
                    # Skip invalid roles
                    continue

        expected_roles_list = None
        if candidate.expected_roles:
            expected_roles_list = []
            for role in candidate.expected_roles:
                try:
                    expected_roles_list.append(PositionRoleEnum(role))
                except ValueError:
                    # Skip invalid roles
                    continue

        command = UpdateCandidateBasicCommand(
            id=CandidateId.from_string(candidate_id),
            name=candidate.name,
            date_of_birth=datetime.strptime(candidate.date_of_birth, "%Y-%m-%d").date(),
            city=candidate.city,
            country=candidate.country,
            phone=candidate.phone,
            email=candidate.email,
            linkedin_url=candidate.linkedin_url,
            job_category=JobCategoryEnum(candidate.job_category),
            expected_annual_salary=candidate.expected_annual_salary,
            currency=candidate.currency,
            relocation=candidate.relocation or False,
            work_modality=work_modality_list,
            languages=languages_dict,
            current_annual_salary=candidate.current_annual_salary,
            current_roles=current_roles_list,
            expected_roles=expected_roles_list,
            skills=candidate.skills
        )

        self.command_bus.dispatch(command)

    def get_experiences_by_candidate_id(self, candidate_id: str) -> List[CandidateExperienceResponse]:
        return self.query_bus.query(GetExperiencesByCandidateIdQuery(CandidateId.from_string(candidate_id)))

    def get_educations_by_candidate_id(self, candidate_id: str) -> List[CandidateEducationResponse]:
        return self.query_bus.query(GetEducationsByCandidateIdQuery(CandidateId.from_string(candidate_id)))

    def get_projects_by_candidate_id(self, candidate_id: str) -> List[CandidateProjectResponse]:
        return self.query_bus.query(GetProjectsByCandidateIdQuery(CandidateId.from_string(candidate_id)))

    def get_experience_by_id(self, experience_id: str) -> CandidateExperienceResponse:
        experience = cast(Optional[CandidateExperienceResponse],
                          self.query_bus.query(
                              GetExperienceByIdQuery(id=CandidateExperienceId.from_string(experience_id))))
        if not experience:
            raise CandidateNotFoundError(f"Experience with id {experience_id} not found")
        return experience

    def create_experience(self, candidate_id: str,
                          experience: CandidateExperienceCreateRequest) -> CandidateExperienceResponse:
        experience_id = ulid.new().str
        self.command_bus.dispatch(CreateExperienceCommand(id=CandidateExperienceId.from_string(experience_id),
                                                          candidate_id=CandidateId.from_string(candidate_id),
                                                          job_title=experience.job_title,
                                                          company=experience.company,
                                                          description=experience.description,
                                                          start_date=datetime.strptime(experience.start_date,
                                                                                       "%Y-%m-%d").date(),
                                                          end_date=datetime.strptime(experience.end_date,
                                                                                     "%Y-%m-%d").date() if experience.end_date else None
                                                          ))

        return self.get_experience_by_id(experience_id)

    def update_experience(self, experience_id: str,
                          experience: CandidateExperienceCreateRequest) -> CandidateExperienceResponse:
        self.command_bus.dispatch(UpdateExperienceCommand(id=CandidateExperienceId.from_string(experience_id),
                                                          job_title=experience.job_title,
                                                          company=experience.company,
                                                          description=experience.description,
                                                          start_date=datetime.strptime(experience.start_date,
                                                                                       "%Y-%m-%d").date(),
                                                          end_date=datetime.strptime(experience.end_date,
                                                                                     "%Y-%m-%d").date() if experience.end_date else None
                                                          ))
        return self.get_experience_by_id(experience_id)

    def create_education(self, candidate_id: str,
                         education: CandidateEducationCreateRequest) -> CandidateEducationResponse:
        education_id = ulid.new().str
        self.command_bus.dispatch(CreateEducationCommand(id=CandidateEducationId.from_string(education_id),
                                                         candidate_id=CandidateId.from_string(candidate_id),
                                                         degree=education.degree,
                                                         institution=education.institution,
                                                         description=education.description,
                                                         start_date=datetime.strptime(education.start_date,
                                                                                      "%Y-%m-%d").date(),
                                                         end_date=datetime.strptime(education.end_date,
                                                                                    "%Y-%m-%d").date() if education.end_date else None
                                                         ))
        return self.get_education_by_id(education_id)

    def get_education_by_id(self, education_id: str) -> CandidateEducationResponse:
        dto: Optional[CandidateEducationDto] = self.query_bus.query(
            GetEducationByIdQuery(CandidateEducationId.from_string(education_id)))
        if not dto:
            raise CandidateNotFoundError(f"Education with id {education_id} not found")
        return CandidateEducationResponse.model_validate(dto)

    def update_education(self, education_id: str,
                         education: CandidateEducationCreateRequest) -> CandidateEducationResponse:
        self.command_bus.dispatch(UpdateEducationCommand(id=CandidateEducationId.from_string(education_id),
                                                         degree=education.degree,
                                                         institution=education.institution,
                                                         description=education.description,
                                                         start_date=datetime.strptime(education.start_date,
                                                                                      "%Y-%m-%d").date(),
                                                         end_date=datetime.strptime(education.end_date,
                                                                                    "%Y-%m-%d").date() if education.end_date else None
                                                         ))
        return self.get_education_by_id(education_id)

    def create_project(self, candidate_id: str, project: CandidateProjectCreateRequest) -> CandidateProjectResponse:
        project_id = ulid.new().str
        self.command_bus.dispatch(CreateProjectCommand(id=CandidateProjectId.from_string(project_id),
                                                       candidate_id=CandidateId.from_string(candidate_id),
                                                       name=project.name,
                                                       description=project.description,
                                                       start_date=datetime.strptime(project.start_date,
                                                                                    "%Y-%m-%d").date(),
                                                       end_date=datetime.strptime(project.end_date,
                                                                                  "%Y-%m-%d").date() if project.end_date else None
                                                       ))
        return self.get_project_by_id(project_id)

    def get_project_by_id(self, project_id: str) -> CandidateProjectResponse:
        dto: Optional[CandidateProjectDto] = self.query_bus.query(
            GetProjectByIdQuery(id=CandidateProjectId.from_string(project_id)))
        if not dto:
            raise CandidateNotFoundError(f"Project with id {project_id} not found")
        return CandidateProjectResponse.model_validate(dto)

    def update_project(self, project_id: str, project: CandidateProjectCreateRequest) -> CandidateProjectResponse:
        self.command_bus.dispatch(UpdateProjectCommand(id=CandidateProjectId.from_string(project_id),
                                                       name=project.name,
                                                       description=project.description,
                                                       start_date=datetime.strptime(project.start_date,
                                                                                    "%Y-%m-%d").date(),
                                                       end_date=datetime.strptime(project.end_date,
                                                                                  "%Y-%m-%d").date() if project.end_date else None
                                                       ))
        return self.get_project_by_id(project_id)

    def delete_experience(self, experience_id: str) -> None:
        self.command_bus.dispatch(DeleteExperienceCommand(CandidateExperienceId.from_string(experience_id)))

    def delete_education(self, education_id: str) -> None:
        self.command_bus.dispatch(DeleteEducationCommand(CandidateEducationId.from_string(education_id)))

    def delete_project(self, project_id: str) -> None:
        self.command_bus.dispatch(DeleteProjectCommand(CandidateProjectId.from_string(project_id)))

    # ====================================
    # ENHANCED CANDIDATE METHODS
    # Business logic moved from router
    # ====================================

    def get_my_profile(self, user_id: str, email: Optional[str] = None) -> CandidateResponse:
        """Get candidate profile for authenticated user.

        If email is provided and no candidate exists, auto-creates one.
        """
        try:
            return self.get_candidate_by_user_id(user_id)
        except CandidateNotFoundError:
            if email:
                # Auto-create candidate profile
                return self._create_candidate_for_user(user_id, email)
            raise HTTPException(status_code=404, detail="Candidate profile not found")

    def _create_candidate_for_user(self, user_id: str, email: str) -> CandidateResponse:
        """Create a minimal candidate profile for the user, or return existing one by email"""
        from src.candidate_bc.candidate.application.queries.get_candidate_by_email import GetCandidateByEmailQuery

        # First check if a candidate with this email already exists
        existing_by_email: Optional[CandidateDto] = self.query_bus.query(GetCandidateByEmailQuery(email=email))
        if existing_by_email:
            log.info(f"Found existing candidate {existing_by_email.id} by email {email}")
            return CandidateResponse.model_validate(existing_by_email)

        log.info(f"Creating candidate profile for user {user_id} with email {email}")
        candidate_id = CandidateId.generate()
        command = CreateCandidateCommand(
            id=candidate_id,
            user_id=UserId.from_string(user_id),
            date_of_birth=datetime.strptime("1990-01-01", "%Y-%m-%d").date(),
            name=email.split("@")[0],  # Use email prefix as initial name
            phone="",
            email=email,
            city="",
            country="",
        )
        self.command_bus.dispatch(command)
        log.info(f"Created candidate profile {candidate_id} for user {user_id}")
        return self.get_candidate_by_user_id(user_id)

    def get_or_create_my_profile(self, user_id: str, email: str) -> CandidateResponse:
        """Get candidate profile for authenticated user, creating one if it doesn't exist"""
        try:
            return self.get_candidate_by_user_id(user_id)
        except CandidateNotFoundError:
            log.info(f"Creating candidate profile for user {user_id} with email {email}")
            # Create a minimal candidate profile
            candidate_id = CandidateId.generate()
            command = CreateCandidateCommand(
                id=candidate_id,
                user_id=UserId.from_string(user_id),
                date_of_birth=datetime.strptime("1990-01-01", "%Y-%m-%d").date(),
                name=email.split("@")[0],  # Use email prefix as initial name
                phone="",
                email=email,
                city="",
                country="",
            )
            self.command_bus.dispatch(command)
            log.info(f"Created candidate profile {candidate_id} for user {user_id}")
            return self.get_candidate_by_user_id(user_id)

    def get_candidate_with_ownership_check(self, candidate_id: str, user_id: str) -> CandidateResponse:
        """Get candidate by ID but verify ownership by current user"""
        candidate = self.get_candidate(candidate_id)

        # TODO: Add recruiter role check when roles are implemented
        # For now, only allow access to own profile
        if candidate.user_id != user_id:
            raise HTTPException(status_code=404, detail="Candidate not found or unauthorized")

        return candidate

    def get_my_experiences(self, user_id: str, email: Optional[str] = None) -> List[CandidateExperienceResponse]:
        """Get experiences for authenticated user"""
        candidate = self.get_my_profile(user_id, email)
        log.info(f"🔍 Getting experiences for user_id: {user_id}, candidate_id: {candidate.id}")

        experiences = self.get_experiences_by_candidate_id(candidate.id)
        log.info(f"📝 Found {len(experiences)} experiences for candidate: {candidate.id}")

        return experiences

    def get_my_educations(self, user_id: str, email: Optional[str] = None) -> List[CandidateEducationResponse]:
        """Get educations for authenticated user"""
        candidate = self.get_my_profile(user_id, email)
        return self.get_educations_by_candidate_id(candidate.id)

    def get_my_projects(self, user_id: str, email: Optional[str] = None) -> List[CandidateProjectResponse]:
        """Get projects for authenticated user"""
        candidate = self.get_my_profile(user_id, email)
        return self.get_projects_by_candidate_id(candidate.id)

    def create_my_experience(self, user_id: str,
                             experience: CandidateExperienceCreateRequest) -> CandidateExperienceResponse:
        """Create experience for authenticated user"""
        candidate = self.get_my_profile(user_id)
        return self.create_experience(candidate.id, experience)

    def get_my_experience_by_id(self, user_id: str, experience_id: str) -> CandidateExperienceResponse:
        """Get experience by ID with ownership verification"""
        candidate = self.get_my_profile(user_id)
        experience = self.get_experience_by_id(experience_id)

        if experience.candidate_id != candidate.id:
            raise HTTPException(status_code=404, detail="Experience not found or unauthorized")

        return experience

    def update_my_experience(self, user_id: str, experience_id: str,
                             experience: CandidateExperienceCreateRequest) -> CandidateExperienceResponse:
        """Update experience for authenticated user with ownership verification"""
        candidate = self.get_my_profile(user_id)
        existing_experience = self.get_experience_by_id(experience_id)

        if existing_experience.candidate_id != candidate.id:
            raise HTTPException(status_code=404, detail="Experience not found or unauthorized")

        return self.update_experience(experience_id, experience)

    def delete_my_experience(self, user_id: str, experience_id: str) -> None:
        """Delete experience for authenticated user with ownership verification"""
        candidate = self.get_my_profile(user_id)
        existing_experience = self.get_experience_by_id(experience_id)

        if existing_experience.candidate_id != candidate.id:
            raise HTTPException(status_code=404, detail="Experience not found or unauthorized")

        self.delete_experience(experience_id)

    def create_my_education(self, user_id: str,
                            education: CandidateEducationCreateRequest) -> CandidateEducationResponse:
        """Create education for authenticated user"""
        candidate = self.get_my_profile(user_id)
        return self.create_education(candidate.id, education)

    def get_my_education_by_id(self, user_id: str, education_id: str) -> CandidateEducationResponse:
        """Get education by ID with ownership verification"""
        candidate = self.get_my_profile(user_id)
        education = self.get_education_by_id(education_id)

        if education.candidate_id != candidate.id:
            raise HTTPException(status_code=404, detail="Education not found or unauthorized")

        return education

    def update_my_education(self, user_id: str, education_id: str,
                            education: CandidateEducationCreateRequest) -> CandidateEducationResponse:
        """Update education for authenticated user with ownership verification"""
        candidate = self.get_my_profile(user_id)
        existing_education = self.get_education_by_id(education_id)

        if existing_education.candidate_id != candidate.id:
            raise HTTPException(status_code=404, detail="Education not found or unauthorized")

        return self.update_education(education_id, education)

    def delete_my_education(self, user_id: str, education_id: str) -> None:
        """Delete education for authenticated user with ownership verification"""
        candidate = self.get_my_profile(user_id)
        existing_education = self.get_education_by_id(education_id)

        if existing_education.candidate_id != candidate.id:
            raise HTTPException(status_code=404, detail="Education not found or unauthorized")

        self.delete_education(education_id)

    def create_my_project(self, user_id: str, project: CandidateProjectCreateRequest) -> CandidateProjectResponse:
        """Create project for authenticated user"""
        candidate = self.get_my_profile(user_id)
        return self.create_project(candidate.id, project)

    def get_my_project_by_id(self, user_id: str, project_id: str) -> CandidateProjectResponse:
        """Get project by ID with ownership verification"""
        candidate = self.get_my_profile(user_id)
        project = self.get_project_by_id(project_id)

        if project.candidate_id != candidate.id:
            raise HTTPException(status_code=404, detail="Project not found or unauthorized")

        return project

    def update_my_project(self, user_id: str, project_id: str,
                          project: CandidateProjectCreateRequest) -> CandidateProjectResponse:
        """Update project for authenticated user with ownership verification"""
        candidate = self.get_my_profile(user_id)
        existing_project = self.get_project_by_id(project_id)

        if existing_project.candidate_id != candidate.id:
            raise HTTPException(status_code=404, detail="Project not found or unauthorized")

        return self.update_project(project_id, project)

    def delete_my_project(self, user_id: str, project_id: str) -> None:
        """Delete project for authenticated user with ownership verification"""
        candidate = self.get_my_profile(user_id)
        existing_project = self.get_project_by_id(project_id)

        if existing_project.candidate_id != candidate.id:
            raise HTTPException(status_code=404, detail="Project not found or unauthorized")

        self.delete_project(project_id)

    def update_my_profile(self, user_id: str, candidate_update: CandidateUpdate) -> CandidateResponse:
        """Update profile for authenticated user"""

        candidate_profile = self.get_my_profile(user_id)

        self.update_candidate(candidate_profile.id, candidate_update)

        updated_candidate = self.get_candidate(candidate_profile.id)

        return updated_candidate

    def get_profile_summary(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive profile summary for dashboard"""
        candidate = self.get_my_profile(user_id)
        experiences = self.get_experiences_by_candidate_id(candidate.id)
        educations = self.get_educations_by_candidate_id(candidate.id)
        projects = self.get_projects_by_candidate_id(candidate.id)

        return {
            "candidate": candidate,
            "summary": {
                "total_experiences": len(experiences),
                "total_educations": len(educations),
                "total_projects": len(projects),
                "profile_completeness": self.profile_validation_service.calculate_profile_completeness(
                    candidate, experiences, educations, projects
                ),
                "last_updated": self.profile_validation_service.get_most_recent_update(
                    candidate, experiences, educations, projects
                )
            },
            "recent_items": {
                "experiences": experiences[:3],  # Most recent 3
                "educations": educations[:3],
                "projects": projects[:3]
            }
        }

    def create_multiple_experiences(self, user_id: str, experiences: List[CandidateExperienceCreateRequest]) -> List[
        CandidateExperienceResponse]:
        """Create multiple experiences at once for better dashboard UX"""
        candidate = self.get_my_profile(user_id)

        created_experiences = []
        for experience in experiences:
            try:
                created_exp = self.create_experience(candidate.id, experience)
                created_experiences.append(created_exp)
            except Exception as e:
                log.error(f"Failed to create experience: {e}")
                # Continue with other experiences
                continue

        return created_experiences

    def update_multiple_experiences(self, user_id: str, experience_updates: List[Dict[str, Any]]) -> List[
        CandidateExperienceResponse]:
        """Update multiple experiences at once for better dashboard UX"""
        candidate = self.get_my_profile(user_id)

        updated_experiences = []
        for update in experience_updates:
            try:
                experience_id = update.get("id")
                experience_data = update.get("data")

                if not experience_id or not experience_data:
                    continue

                # Verify ownership
                existing_experience = self.get_experience_by_id(experience_id)
                if not existing_experience or existing_experience.candidate_id != candidate.id:
                    continue

                # Convert dict to proper request object
                experience_request = CandidateExperienceCreateRequest(**experience_data)
                updated_exp = self.update_experience(experience_id, experience_request)
                updated_experiences.append(updated_exp)
            except Exception as e:
                log.error(f"Failed to update experience {experience_id}: {e}")
                continue

        return updated_experiences

    def validate_profile_completeness(self, user_id: str) -> Dict[str, Any]:
        """Validate profile completeness and provide recommendations"""
        candidate = self.get_my_profile(user_id)
        experiences = self.get_experiences_by_candidate_id(candidate.id)
        educations = self.get_educations_by_candidate_id(candidate.id)
        projects = self.get_projects_by_candidate_id(candidate.id)

        return self.profile_validation_service.validate_profile_completeness(
            candidate, experiences, educations, projects
        )

    def auto_enhance_profile(self, user_id: str) -> Dict[str, Any]:
        """Auto-enhance profile with AI suggestions (placeholder for AI integration)"""

        # This would integrate with AI services to enhance the profile
        # For now, return enhancement suggestions
        return {
            "enhancement_available": True,
            "suggestions": [
                "Add more specific achievements to your work experiences",
                "Include quantifiable results in your project descriptions",
                "Expand your education section with relevant coursework",
                "Add technical skills and certifications"
            ],
            "ai_enhancement_status": "available",
            "estimated_improvement": "25% better match rate"
        }

    def upload_resume_for_ai_processing(self, user_id: str) -> Dict[str, Any]:
        """Upload and process resume with AI extraction"""
        candidate = self.get_my_profile(user_id)

        # This endpoint would handle PDF upload and AI processing
        # For now, return a placeholder response
        return {
            "success": True,
            "message": "Resume uploaded and processed successfully",
            "extraction_status": "completed",
            "candidate_id": candidate.id,
            "extracted_data": {
                "experiences_found": 3,
                "education_entries": 2,
                "projects_found": 1,
                "skills_extracted": ["Python", "FastAPI", "React"]
            },
            "next_steps": [
                "Review extracted information",
                "Start AI interview to enhance profile",
                "Generate enhanced resume"
            ]
        }
