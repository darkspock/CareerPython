"""AI Chat Service Interface for conversational AI capabilities."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ChatMessage:
    """Represents a single message in a conversation."""
    role: str  # "system", "user", or "assistant"
    content: str


@dataclass
class ChatResponse:
    """Response from the AI chat service."""
    content: str
    success: bool
    error_message: Optional[str] = None
    model: Optional[str] = None
    tokens_used: Optional[int] = None


class AIChatServiceInterface(ABC):
    """Abstract interface for AI chat services."""

    @abstractmethod
    def chat(
        self,
        messages: List[ChatMessage],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> ChatResponse:
        """
        Send a chat completion request.

        Args:
            messages: List of conversation messages
            system_prompt: Optional system prompt to prepend
            temperature: Creativity level (0.0-1.0)
            max_tokens: Maximum tokens in response

        Returns:
            ChatResponse containing the AI response
        """
        pass

    @abstractmethod
    def generate_interview_followup(
        self,
        question: str,
        candidate_response: str,
        position_context: Optional[str] = None,
        previous_messages: Optional[List[ChatMessage]] = None
    ) -> ChatResponse:
        """
        Generate a follow-up question for an interview.

        Args:
            question: The original interview question
            candidate_response: The candidate's answer
            position_context: Optional context about the position
            previous_messages: Optional conversation history

        Returns:
            ChatResponse containing the follow-up question
        """
        pass

    @abstractmethod
    def generate_candidate_report(
        self,
        candidate_name: str,
        comments: List[dict],
        interview_data: Optional[List[dict]] = None,
        position_info: Optional[dict] = None
    ) -> ChatResponse:
        """
        Generate a comprehensive candidate evaluation report.

        Args:
            candidate_name: Name of the candidate
            comments: List of feedback comments
            interview_data: Optional interview responses
            position_info: Optional position details

        Returns:
            ChatResponse containing the report in markdown
        """
        pass
