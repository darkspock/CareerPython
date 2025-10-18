"""Factory for AI services to avoid circular imports."""

from core.config import settings
from src.shared.domain.interfaces.ai_service_interface import AIServiceInterface


def get_ai_service() -> AIServiceInterface:
    """
    Factory function to get the appropriate AI service based on configuration.

    Returns:
        AIServiceInterface: Either XAI or Groq service based on AI_AGENT setting
    """
    if settings.AI_AGENT.lower() == "groq":
        from .groq_service import GroqResumeAnalysisService
        return GroqResumeAnalysisService()
    else:
        from .xai_service import XAIResumeAnalysisService
        return XAIResumeAnalysisService()
