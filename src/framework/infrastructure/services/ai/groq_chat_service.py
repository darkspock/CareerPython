"""Groq Chat Service for conversational AI capabilities."""

import logging
from typing import List, Optional

import requests
from requests.exceptions import RequestException, Timeout

from core.config import settings
from src.framework.domain.interfaces.ai_chat_service_interface import (
    AIChatServiceInterface,
    ChatMessage,
    ChatResponse,
)

logger = logging.getLogger(__name__)


class GroqChatService(AIChatServiceInterface):
    """Service for AI chat using Groq."""

    def __init__(self) -> None:
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL
        self.max_tokens = settings.GROQ_MAX_TOKENS
        self.timeout = settings.GROQ_TIMEOUT
        self.api_url = f"{settings.GROQ_API_URL}/chat/completions"

        if not self.api_key:
            logger.warning("GROQ_API_KEY not configured - AI features will be limited")

    def chat(
        self,
        messages: List[ChatMessage],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> ChatResponse:
        """Send a chat completion request to Groq."""
        if not self.api_key:
            return ChatResponse(
                content="AI service not configured",
                success=False,
                error_message="GROQ_API_KEY not configured"
            )

        try:
            # Build messages list
            api_messages = []

            if system_prompt:
                api_messages.append({
                    "role": "system",
                    "content": system_prompt
                })

            for msg in messages:
                api_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

            # Call Groq API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": api_messages,
                "max_tokens": max_tokens or self.max_tokens,
                "temperature": temperature
            }

            logger.info(f"Calling Groq Chat API with {len(api_messages)} messages")
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )

            if response.status_code != 200:
                logger.error(f"Groq API error: {response.status_code} - {response.text}")
                return ChatResponse(
                    content="",
                    success=False,
                    error_message=f"API returned status {response.status_code}"
                )

            response_data = response.json()
            content = response_data["choices"][0]["message"]["content"]
            tokens = response_data.get("usage", {}).get("total_tokens")

            logger.info("Groq Chat API call successful")
            return ChatResponse(
                content=content,
                success=True,
                model=self.model,
                tokens_used=tokens
            )

        except Timeout:
            logger.error(f"Groq API timeout after {self.timeout}s")
            return ChatResponse(
                content="",
                success=False,
                error_message=f"API call timed out after {self.timeout} seconds"
            )
        except RequestException as e:
            logger.error(f"Groq API request failed: {e}")
            return ChatResponse(
                content="",
                success=False,
                error_message=f"Request failed: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Groq Chat error: {e}")
            return ChatResponse(
                content="",
                success=False,
                error_message=str(e)
            )

    def generate_interview_followup(
        self,
        question: str,
        candidate_response: str,
        position_context: Optional[str] = None,
        previous_messages: Optional[List[ChatMessage]] = None
    ) -> ChatResponse:
        """Generate an interview follow-up question."""
        system_prompt = """You are an expert interviewer conducting a professional job interview.
Your role is to:
1. Acknowledge the candidate's response thoughtfully
2. Ask a relevant follow-up question that goes deeper into the topic
3. Keep questions professional and focused on skills/experience
4. Be encouraging but probe for specific examples and outcomes
5. Keep your response concise (2-3 sentences max)

Do not repeat questions already asked. Focus on understanding the candidate's actual experience and capabilities."""

        if position_context:
            system_prompt += f"\n\nPosition context: {position_context}"

        # Build conversation history
        messages = []

        if previous_messages:
            messages.extend(previous_messages)

        # Add current exchange
        messages.append(ChatMessage(
            role="assistant",
            content=f"Interview question: {question}"
        ))
        messages.append(ChatMessage(
            role="user",
            content=candidate_response
        ))

        return self.chat(
            messages=messages,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=300
        )

    def generate_candidate_report(
        self,
        candidate_name: str,
        comments: List[dict],
        interview_data: Optional[List[dict]] = None,
        position_info: Optional[dict] = None
    ) -> ChatResponse:
        """Generate a comprehensive candidate evaluation report."""
        system_prompt = """You are an expert HR analyst creating a comprehensive candidate evaluation report.
Generate a professional report in Markdown format that includes:
1. Executive Summary (2-3 sentences)
2. Strengths (bullet points based on feedback)
3. Areas for Development (bullet points)
4. Interview Insights (if interview data provided)
5. Final Recommendation

Be objective, professional, and base your analysis on the provided feedback.
If limited data is available, acknowledge this and provide what insights you can."""

        # Build context from comments
        feedback_text = ""
        if comments:
            feedback_text = "\n\nFeedback entries:\n"
            for i, comment in enumerate(comments, 1):
                content = comment.get('content', '')
                author = comment.get('author', 'Anonymous')
                created = comment.get('created_at', '')
                feedback_text += f"{i}. {author}: \"{content}\" ({created})\n"
        else:
            feedback_text = "\n\nNo feedback entries recorded yet."

        # Build interview context
        interview_text = ""
        if interview_data:
            interview_text = "\n\nInterview responses:\n"
            for i, item in enumerate(interview_data, 1):
                q = item.get('question', '')
                a = item.get('answer', '')
                interview_text += f"Q{i}: {q}\nA{i}: {a}\n\n"

        # Build position context
        position_text = ""
        if position_info:
            title = position_info.get('title', 'Unknown position')
            dept = position_info.get('department', '')
            position_text = f"\n\nPosition: {title}"
            if dept:
                position_text += f" ({dept})"

        user_prompt = f"""Generate a candidate evaluation report for: {candidate_name}
{position_text}
{feedback_text}
{interview_text}

Please provide a comprehensive analysis in Markdown format."""

        messages = [ChatMessage(role="user", content=user_prompt)]

        return self.chat(
            messages=messages,
            system_prompt=system_prompt,
            temperature=0.3,  # Lower temperature for more consistent reports
            max_tokens=2000
        )


def get_chat_service() -> AIChatServiceInterface:
    """Factory function to get the AI chat service based on configuration."""
    if settings.AI_AGENT.lower() == "groq":
        return GroqChatService()
    else:
        # For now, default to Groq for chat
        # XAI chat service could be added later
        return GroqChatService()
