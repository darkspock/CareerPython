"""Value objects for resume analysis results."""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List


@dataclass
class ResumeAnalysisResult:
    """Result of resume analysis from AI service."""
    candidate_info: Dict[str, Any]
    experiences: List[Dict[str, Any]]
    educations: List[Dict[str, Any]]
    projects: List[Dict[str, Any]]
    skills: List[str]
    confidence_score: float
    success: bool
    raw_response: Optional[str] = None
    error_message: Optional[str] = None
