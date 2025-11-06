"""
Profile validation service for candidate profiles
"""
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, cast, Union

from adapters.http.candidate.schemas.candidate import CandidateResponse
from adapters.http.candidate.schemas.candidate_education import CandidateEducationResponse
from adapters.http.candidate.schemas.candidate_experience import CandidateExperienceResponse
from adapters.http.candidate.schemas.candidate_project import CandidateProjectResponse

log = logging.getLogger(__name__)


class ProfileValidationService:
    """Service for validating and analyzing candidate profiles"""

    def calculate_profile_completeness(
            self,
            candidate: CandidateResponse,
            experiences: List[CandidateExperienceResponse],
            educations: List[CandidateEducationResponse],
            projects: List[CandidateProjectResponse]
    ) -> float:
        """Calculate profile completeness percentage"""
        score = 0
        total_points = 10

        # Basic info (3 points)
        if candidate.name:
            score += 1
        if candidate.email:
            score += 1
        if candidate.phone:
            score += 1

        # Experience (3 points)
        if experiences:
            score += min(len(experiences), 3)

        # Education (2 points)
        if educations:
            score += min(len(educations), 2)

        # Projects (2 points)
        if projects:
            score += min(len(projects), 2)

        return (score / total_points) * 100

    def get_most_recent_update(
            self,
            candidate: CandidateResponse,
            experiences: List[CandidateExperienceResponse],
            educations: List[CandidateEducationResponse],
            projects: List[CandidateProjectResponse]
    ) -> Optional[str]:
        """Get the most recent update timestamp"""
        timestamps: List[Union[str, datetime, None]] = []

        if hasattr(candidate, 'updated_at') and candidate.updated_at:
            timestamps.append(candidate.updated_at)

        # Handle the lists that might be returned as Any from controller
        all_items = [experiences, educations, projects]
        for items in all_items:
            if items and hasattr(items, '__iter__'):  # Check if it's iterable
                try:
                    for item in items:
                        if hasattr(item, 'updated_at') and item.updated_at:
                            timestamps.append(item.updated_at)
                except (TypeError, AttributeError):
                    # Skip if items is not iterable or doesn't have the expected attributes
                    continue

        if not timestamps:
            return None

        # Convert all timestamps to datetime objects for proper comparison
        datetime_objects: List[datetime] = []

        for timestamp in timestamps:
            if timestamp is None:
                continue

            try:
                # Handle datetime objects directly
                if isinstance(timestamp, datetime):
                    datetime_objects.append(timestamp)
                else:
                    # Convert everything else to string and parse
                    timestamp_str = str(timestamp)
                    if timestamp_str:
                        datetime_objects.append(datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')))
            except (ValueError, TypeError):
                # Skip invalid timestamps
                continue

        if not datetime_objects:
            return None

        # Get the most recent datetime and convert back to ISO string
        most_recent = max(datetime_objects)
        return most_recent.isoformat()

    def validate_profile_completeness(
            self,
            candidate: CandidateResponse,
            experiences: List[CandidateExperienceResponse],
            educations: List[CandidateEducationResponse],
            projects: List[CandidateProjectResponse]
    ) -> Dict[str, Any]:
        """Validate profile completeness and provide recommendations"""
        validation_results = {
            "is_complete": True,
            "completeness_score": 0,
            "missing_fields": [],
            "recommendations": [],
            "sections": {
                "basic_info": self._validate_basic_info(candidate),
                "experiences": self._validate_experiences(experiences),
                "educations": self._validate_educations(educations),
                "projects": self._validate_projects(projects)
            }
        }

        # Calculate overall completeness
        sections: Dict[str, Dict[str, Any]] = cast(Dict[str, Dict[str, Any]], validation_results["sections"])
        section_scores = [section["score"] for section in sections.values()]
        completeness_score = sum(section_scores) / len(section_scores) if section_scores else 0
        validation_results["completeness_score"] = completeness_score
        validation_results["is_complete"] = completeness_score >= 80

        # Collect missing fields and recommendations
        missing_fields_list: List[str] = cast(List[str], validation_results["missing_fields"])
        recommendations_list: List[str] = cast(List[str], validation_results["recommendations"])

        for section_name, section_data in sections.items():
            missing_fields_list.extend(section_data.get("missing_fields", []))
            recommendations_list.extend(section_data.get("recommendations", []))

        return validation_results

    def _validate_basic_info(self, candidate: CandidateResponse) -> Dict[str, Any]:
        """Validate basic candidate information"""
        missing_fields = []
        recommendations = []

        if not candidate.name:
            missing_fields.append("name")
        if not candidate.email:
            missing_fields.append("email")
        if not candidate.phone:
            missing_fields.append("phone")
        if not candidate.city:
            missing_fields.append("city")
            recommendations.append("Add your location to help with local job opportunities")

        score = ((4 - len(missing_fields)) / 4) * 100

        return {
            "score": score,
            "missing_fields": missing_fields,
            "recommendations": recommendations,
            "is_complete": len(missing_fields) == 0
        }

    def _validate_experiences(self, experiences: List[CandidateExperienceResponse]) -> Dict[str, Any]:
        """Validate work experiences"""
        missing_fields = []
        recommendations = []

        if not experiences:
            missing_fields.append("work_experience")
            recommendations.append("Add at least one work experience")
            return {
                "score": 0,
                "missing_fields": missing_fields,
                "recommendations": recommendations,
                "is_complete": False
            }

        # Check for detailed descriptions
        incomplete_experiences = [exp for exp in experiences if not exp.description or len(exp.description) < 50]
        if incomplete_experiences:
            recommendations.append(f"Add more detailed descriptions to {len(incomplete_experiences)} experiences")

        score: float = min(len(experiences) * 25, 100)  # Up to 4 experiences for full score
        if incomplete_experiences:
            score *= 0.8  # Reduce score for incomplete descriptions

        return {
            "score": score,
            "missing_fields": missing_fields,
            "recommendations": recommendations,
            "is_complete": len(incomplete_experiences) == 0
        }

    def _validate_educations(self, educations: List[CandidateEducationResponse]) -> Dict[str, Any]:
        """Validate education entries"""
        missing_fields = []
        recommendations = []

        if not educations:
            missing_fields.append("education")
            recommendations.append("Add your educational background")
            return {
                "score": 0,
                "missing_fields": missing_fields,
                "recommendations": recommendations,
                "is_complete": False
            }

        score = min(len(educations) * 50, 100)  # Up to 2 education entries for full score

        return {
            "score": score,
            "missing_fields": missing_fields,
            "recommendations": recommendations,
            "is_complete": True
        }

    def _validate_projects(self, projects: List[CandidateProjectResponse]) -> Dict[str, Any]:
        """Validate project entries"""
        recommendations = []

        if not projects:
            recommendations.append("Add projects to showcase your practical skills")
            return {
                "score": 50,  # Projects are optional but recommended
                "missing_fields": [],
                "recommendations": recommendations,
                "is_complete": True
            }

        score = min(len(projects) * 25, 100)  # Up to 4 projects for full score

        return {
            "score": score,
            "missing_fields": [],
            "recommendations": recommendations,
            "is_complete": True
        }
