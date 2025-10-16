"""Command to populate candidate data from PDF analysis results."""

import logging
from dataclasses import dataclass
from datetime import datetime, date
from typing import Dict, Any, List, Optional

from src.candidate.application.commands.create_education import CreateEducationCommand
from src.candidate.application.commands.create_experience import CreateExperienceCommand
from src.candidate.application.commands.create_project import CreateProjectCommand
from src.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.candidate.domain.value_objects.candidate_education_id import CandidateEducationId
from src.candidate.domain.value_objects.candidate_experience_id import CandidateExperienceId
from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate.domain.value_objects.candidate_project_id import CandidateProjectId
from src.shared.application.command_bus import Command, CommandHandler, CommandBus
from src.shared.domain.entities.base import generate_id


@dataclass
class PopulateCandidateFromPdfAnalysisCommand(Command):
    """Command to populate candidate profile from PDF analysis results."""
    candidate_id: str
    analysis_results: Dict[str, Any]


class PopulateCandidateFromPdfAnalysisCommandHandler(CommandHandler[PopulateCandidateFromPdfAnalysisCommand]):
    """Handler for populating candidate data from PDF analysis results."""

    def __init__(
            self,
            candidate_repository: CandidateRepositoryInterface,
            command_bus: CommandBus
    ):
        self.candidate_repository = candidate_repository
        self.command_bus = command_bus
        self.logger = logging.getLogger(__name__)

    def execute(self, command: PopulateCandidateFromPdfAnalysisCommand) -> None:
        """Execute the command to populate candidate data."""
        try:
            candidate_id = CandidateId.from_string(command.candidate_id)
            results = command.analysis_results

            # Validate analysis results
            if not results.get("analysis_successful", False):
                self.logger.warning(f"Analysis was not successful for candidate {candidate_id}")
                return

            # 1. DISABLED: Update candidate basic information (per spec: only experiences and education)
            # self._update_candidate_basic_info(candidate_id, results.get("candidate_info", {}))

            # 2. Create experiences - ENABLED per specification
            self._create_candidate_experiences(candidate_id, results.get("experiences", []))

            # 3. Create educations - ENABLED per specification
            self._create_candidate_educations(candidate_id, results.get("educations", []))

            # 4. Create projects - DISABLED (not mentioned in spec)
            # self._create_candidate_projects(candidate_id, results.get("projects", []))

            self.logger.info(f"Successfully populated candidate {candidate_id} from PDF analysis with all data")

        except Exception as e:
            self.logger.error(f"Error populating candidate from PDF analysis: {str(e)}")
            raise

    def _update_candidate_basic_info(self, candidate_id: CandidateId, candidate_info: Dict[str, Any]) -> None:
        """Update candidate basic information."""
        try:
            if not candidate_info:
                self.logger.warning(f"No candidate info provided for {candidate_id}")
                return

            # Get the existing candidate
            existing_candidate = self.candidate_repository.get_by_id(candidate_id)
            if not existing_candidate:
                self.logger.warning(f"Candidate {candidate_id} not found")
                return

            # Extract all available info with defaults - handle None values
            name = (candidate_info.get("name") or "").strip()
            phone = (candidate_info.get("phone") or "").strip()
            city = (candidate_info.get("city") or "").strip()
            country = (candidate_info.get("country") or "").strip()
            email = (candidate_info.get("email") or "").strip()
            linkedin_url = (candidate_info.get("linkedin_url") or "").strip()
            skills = candidate_info.get("skills", [])
            job_category = (candidate_info.get("job_category") or "").strip()

            # Update candidate fields directly - be VERY aggressive about updating with xAI data
            updated = False

            # Always update name if we have a clean name from xAI (not just regex extraction)
            if name and name != "Nuevo Candidato":
                self.logger.info(f"Updating candidate name from '{existing_candidate.name}' to '{name}'")
                existing_candidate.name = name
                updated = True

            # Always update phone if we have one from xAI
            if phone:
                self.logger.info(f"Updating candidate phone from '{existing_candidate.phone}' to '{phone}'")
                existing_candidate.phone = phone
                updated = True

            # Always update city if we have one from xAI
            if city:
                self.logger.info(f"Updating candidate city from '{existing_candidate.city}' to '{city}'")
                existing_candidate.city = city
                updated = True

            # Always update country if we have one from xAI
            if country:
                self.logger.info(f"Updating candidate country from '{existing_candidate.country}' to '{country}'")
                existing_candidate.country = country
                updated = True

            # Always update email if we have one from xAI (but be careful about duplicates)
            if email and email != existing_candidate.email:
                self.logger.info(f"Updating candidate email from '{existing_candidate.email}' to '{email}'")
                existing_candidate.email = email
                updated = True

            # Always update LinkedIn if we have one from xAI
            if linkedin_url:
                self.logger.info(
                    f"Updating candidate LinkedIn from '{existing_candidate.linkedin_url}' to '{linkedin_url}'")
                existing_candidate.linkedin_url = linkedin_url
                updated = True

            # Always update skills if we have them from xAI
            if skills and len(skills) > 0:
                self.logger.info(
                    f"Updating candidate skills: {len(skills)} skills found (replacing {len(existing_candidate.skills or [])} existing)")
                existing_candidate.skills = skills
                updated = True

            # Handle job category if provided
            if job_category:
                from src.shared.domain.enums.job_category import JobCategoryEnum
                try:
                    # Try to match job category case-insensitively
                    job_cat_enum = None
                    job_category_upper = job_category.upper()

                    # Map common variations to correct enum values
                    category_mapping = {
                        "TECHNOLOGY": JobCategoryEnum.TECHNOLOGY,
                        "TECH": JobCategoryEnum.TECHNOLOGY,
                        "OPERATIONS": JobCategoryEnum.OPERATIONS,
                        "SALES": JobCategoryEnum.SALES,
                        "MARKETING": JobCategoryEnum.MARKETING,
                        "ADMINISTRATION": JobCategoryEnum.ADMINISTRATION,
                        "ADMIN": JobCategoryEnum.ADMINISTRATION,
                        "HR": JobCategoryEnum.HR,
                        "HUMAN RESOURCES": JobCategoryEnum.HR,
                        "FINANCE": JobCategoryEnum.FINANCE,
                        "CUSTOMER SERVICE": JobCategoryEnum.CUSTOMER_SERVICE,
                        "OTHER": JobCategoryEnum.OTHER
                    }

                    job_cat_enum = category_mapping.get(job_category_upper)

                    if job_cat_enum and job_cat_enum != existing_candidate.job_category:
                        self.logger.info(
                            f"Updating job category from '{existing_candidate.job_category}' to '{job_cat_enum.value}'")
                        existing_candidate.job_category = job_cat_enum
                        updated = True
                    elif not job_cat_enum:
                        self.logger.warning(f"Unknown job category: {job_category}, using OTHER")
                        existing_candidate.job_category = JobCategoryEnum.OTHER
                        updated = True
                except (ValueError, AttributeError) as e:
                    self.logger.warning(f"Error processing job category '{job_category}': {str(e)}")

            # Save if we made any updates
            if updated:
                try:
                    self.candidate_repository.update(existing_candidate)
                    self.logger.info(f"✅ Successfully updated candidate basic info for {candidate_id}")
                except Exception as db_error:
                    # Handle database constraint violations gracefully
                    if "duplicate key value violates unique constraint" in str(db_error):
                        self.logger.warning(
                            f"⚠️ Database constraint violation when updating candidate {candidate_id}: {str(db_error)}")
                        self.logger.info("Continuing with experience/education/project creation...")
                    else:
                        self.logger.error(f"❌ Database error updating candidate basic info: {str(db_error)}")
                        raise
            else:
                self.logger.info(f"No updates needed for candidate {candidate_id}")

        except Exception as e:
            self.logger.error(f"❌ Error updating candidate basic info: {str(e)}")
            # Don't raise - continue with other data

    def _create_candidate_experiences(self, candidate_id: CandidateId, experiences: List[Dict[str, Any]]) -> None:
        """Create candidate experiences from analysis results."""
        try:
            if not experiences:
                self.logger.info(f"No experiences to create for candidate {candidate_id}")
                return

            self.logger.info(f"Creating {len(experiences)} experiences for candidate {candidate_id}")

            for exp_data in experiences:
                if not exp_data:
                    continue

                job_title = exp_data.get("job_title", "").strip()
                company = exp_data.get("company", "").strip()
                description = exp_data.get("description", "").strip()

                if not job_title or not company:
                    self.logger.warning(f"Skipping experience with missing job_title or company: {exp_data}")
                    continue

                # Parse dates
                start_date = self._parse_date(exp_data.get("start_date"))
                end_date = self._parse_date(exp_data.get("end_date"))

                experience_command = CreateExperienceCommand(
                    id=CandidateExperienceId(generate_id()),
                    candidate_id=candidate_id,
                    job_title=job_title,
                    company=company,
                    description=description,
                    start_date=start_date or date(2020, 1, 1),  # Default fallback
                    end_date=end_date
                )

                self.command_bus.execute(experience_command)
                self.logger.info(f"✅ Created experience: {job_title} at {company}")

        except Exception as e:
            self.logger.error(f"❌ Error creating candidate experiences: {str(e)}")
            import traceback
            self.logger.error(traceback.format_exc())
            # Don't raise - continue with other data

    def _create_candidate_educations(self, candidate_id: CandidateId, educations: List[Dict[str, Any]]) -> None:
        """Create candidate educations from analysis results."""
        try:
            if not educations:
                self.logger.info(f"No educations to create for candidate {candidate_id}")
                return

            self.logger.info(f"Creating {len(educations)} educations for candidate {candidate_id}")

            for edu_data in educations:
                if not edu_data:
                    continue

                institution = edu_data.get("institution", "").strip()
                degree = edu_data.get("degree", "").strip()

                if not institution or not degree:
                    self.logger.warning(f"Skipping education with missing institution or degree: {edu_data}")
                    continue

                # Parse dates
                start_date = self._parse_date(edu_data.get("start_date"))
                end_date = self._parse_date(edu_data.get("end_date"))

                education_command = CreateEducationCommand(
                    id=CandidateEducationId(generate_id()),
                    candidate_id=candidate_id,
                    institution=institution,
                    degree=degree,
                    start_date=start_date or date(2020, 1, 1),  # Default fallback
                    end_date=end_date,
                    description=edu_data.get("description", "")
                )

                self.command_bus.execute(education_command)
                self.logger.info(f"✅ Created education: {degree} at {institution}")

        except Exception as e:
            self.logger.error(f"❌ Error creating candidate educations: {str(e)}")
            import traceback
            self.logger.error(traceback.format_exc())
            # Don't raise - continue with other data

    def _create_candidate_projects(self, candidate_id: CandidateId, projects: List[Dict[str, Any]]) -> None:
        """Create candidate projects from analysis results."""
        try:
            if not projects:
                self.logger.info(f"No projects to create for candidate {candidate_id}")
                return

            self.logger.info(f"Creating {len(projects)} projects for candidate {candidate_id}")

            for project_data in projects:
                if not project_data:
                    continue

                name = project_data.get("name", "").strip()
                description = project_data.get("description", "").strip()

                if not name:
                    self.logger.warning(f"Skipping project with missing name: {project_data}")
                    continue

                # Parse dates
                start_date = self._parse_date(project_data.get("start_date"))
                end_date = self._parse_date(project_data.get("end_date"))

                project_command = CreateProjectCommand(
                    id=CandidateProjectId(generate_id()),
                    candidate_id=candidate_id,
                    name=name,
                    description=description,
                    start_date=start_date or date(2020, 1, 1),  # Default fallback
                    end_date=end_date
                )

                self.command_bus.execute(project_command)
                self.logger.info(f"✅ Created project: {name}")

        except Exception as e:
            self.logger.error(f"❌ Error creating candidate projects: {str(e)}")
            import traceback
            self.logger.error(traceback.format_exc())
            # Don't raise - continue with other data

    def _parse_date(self, date_str: Optional[str]) -> Optional[date]:
        """Parse date string to date object."""
        if not date_str or date_str.lower() in ["present", "current", ""]:
            return None

        try:
            # Try common date formats
            for fmt in ["%Y-%m-%d", "%Y-%m", "%Y", "%d/%m/%Y", "%d-%m-%Y"]:
                try:
                    parsed_date = datetime.strptime(date_str, fmt).date()
                    return parsed_date
                except ValueError:
                    continue

            # If no format worked, try to extract just the year
            if len(date_str) == 4 and date_str.isdigit():
                return date(int(date_str), 1, 1)

            return None

        except Exception as e:
            self.logger.warning(f"Could not parse date '{date_str}': {str(e)}")
            return None
