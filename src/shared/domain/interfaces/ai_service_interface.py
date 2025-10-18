"""AI Service Interface for resume analysis."""

from abc import ABC, abstractmethod

from src.shared.domain.value_objects.resume_analysis_result import ResumeAnalysisResult


class AIServiceInterface(ABC):
    """Abstract interface for AI resume analysis services."""

    @abstractmethod
    def analyze_resume_pdf(self, pdf_text: str) -> ResumeAnalysisResult:
        """
        Analyze resume PDF text and extract structured information.

        Args:
            pdf_text: The extracted text from a resume PDF

        Returns:
            ResumeAnalysisResult containing extracted candidate information
        """
        pass

    @abstractmethod
    def validate_analysis_result(self, result: ResumeAnalysisResult) -> bool:
        """
        Validate the quality of an analysis result.

        Args:
            result: The analysis result to validate

        Returns:
            True if the result is valid and contains meaningful data
        """
        pass
