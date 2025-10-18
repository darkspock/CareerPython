"""Groq service for resume analysis."""

import json
import logging

import requests
from requests.exceptions import RequestException, Timeout

from core.config import settings
from src.shared.domain.interfaces.ai_service_interface import AIServiceInterface
from ....domain.value_objects.resume_analysis_result import ResumeAnalysisResult

logger = logging.getLogger(__name__)


class GroqResumeAnalysisService(AIServiceInterface):
    """Service for analyzing resumes using Groq."""

    def __init__(self) -> None:
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL
        self.max_tokens = settings.GROQ_MAX_TOKENS
        self.timeout = settings.GROQ_TIMEOUT
        self.api_url = f"{settings.GROQ_API_URL}/chat/completions"

        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")

    def analyze_resume_pdf(self, pdf_text: str) -> ResumeAnalysisResult:
        """Analyze resume PDF text with Groq."""
        try:
            logger.info("Starting resume analysis with Groq")

            # Create the analysis prompt
            prompt = self._create_analysis_prompt(pdf_text)

            # Call Groq API
            response = self._call_groq_api(prompt)

            # Parse the response
            analysis_result = self._parse_response(response)

            logger.info(f"Resume analysis completed with confidence: {analysis_result.confidence_score}")
            return analysis_result

        except Exception as e:
            logger.error(f"Resume analysis failed: {str(e)}")
            return ResumeAnalysisResult(
                candidate_info={},
                experiences=[],
                educations=[],
                projects=[],
                skills=[],
                confidence_score=0.0,
                success=False,
                error_message=str(e)
            )

    def _create_analysis_prompt(self, pdf_text: str) -> str:
        """Create the analysis prompt for Groq."""
        return f"""
Analyze this resume and extract the information in exact JSON format. It is critical that you respond ONLY with valid JSON, without additional text.

RESUME TEXT:
{pdf_text}

REQUIRED RESPONSE (JSON):
{{
  "candidate": {{
    "name": "string",
    "phone": "string",
    "city": "string",
    "country": "string",
    "email": "string",
    "linkedin_url": "string",
    "skills": ["skill1", "skill2"],
    "job_category": "TECHNOLOGY"
  }},
  "experiences": [{{
    "job_title": "string",
    "company": "string",
    "description": "string",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD"
  }}],
  "educations": [{{
    "degree": "string",
    "institution": "string",
    "description": "string",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD"
  }}],
  "projects": [{{
    "name": "string",
    "description": "string",
    "start_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD"
  }}],
  "confidence": 0.95
}}

INSTRUCTIONS:
- Extract only information that is clearly present in the resume
- If there is no information, use null or empty array []
- For dates, use YYYY-MM-DD format or null if not available
- job_category must be one of: TECHNOLOGY, OPERATIONS, SALES, MARKETING, ADMINISTRATION, HR, FINANCE, CUSTOMER_SERVICE, OTHER
- confidence must be a number between 0 and 1
- Respond ONLY with the JSON, without additional explanations
"""

    def _call_groq_api(self, prompt: str) -> str:
        """Call Groq API with the analysis prompt."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert resume analyzer. Respond only with valid JSON, without additional text."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": self.max_tokens,
            "temperature": 0.1  # Low temperature for consistent results
        }

        try:
            logger.info("Calling Groq API")
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=self.timeout
            )

            if response.status_code != 200:
                raise RequestException(f"Groq API returned status {response.status_code}: {response.text}")

            response_data = response.json()
            content: str = response_data["choices"][0]["message"]["content"]

            logger.info("Groq API call successful")
            return content

        except Timeout:
            raise Exception(f"Groq API call timed out after {self.timeout} seconds")
        except RequestException as e:
            raise Exception(f"Groq API request failed: {str(e)}")
        except KeyError as e:
            raise Exception(f"Unexpected Groq API response format: missing {str(e)}")
        except Exception as e:
            raise Exception(f"Groq API call failed: {str(e)}")

    def _parse_response(self, response_text: str) -> ResumeAnalysisResult:
        """Parse Groq response into structured data."""
        try:
            # Clean response text - remove any markdown formatting
            cleaned_text = response_text.strip()

            # Remove markdown code blocks (with or without language specifier)
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            elif cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:]

            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]

            cleaned_text = cleaned_text.strip()

            # Parse JSON
            data = json.loads(cleaned_text)

            # Extract data with defaults
            candidate_info = data.get("candidate", {})
            experiences = data.get("experiences", [])
            educations = data.get("educations", [])
            projects = data.get("projects", [])
            confidence = data.get("confidence", 0.5)

            # Extract skills from candidate info
            skills = candidate_info.get("skills", [])

            return ResumeAnalysisResult(
                candidate_info=candidate_info,
                experiences=experiences,
                educations=educations,
                projects=projects,
                skills=skills,
                confidence_score=confidence,
                success=True,
                raw_response=response_text
            )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Groq response as JSON: {e}")
            logger.error(f"Response text: {response_text}")

            # Try to extract partial information
            return self._fallback_parsing(response_text)

        except Exception as e:
            logger.error(f"Failed to parse Groq response: {e}")
            return ResumeAnalysisResult(
                candidate_info={},
                experiences=[],
                educations=[],
                projects=[],
                skills=[],
                confidence_score=0.0,
                success=False,
                error_message=f"Response parsing failed: {str(e)}",
                raw_response=response_text
            )

    def _fallback_parsing(self, response_text: str) -> ResumeAnalysisResult:
        """Fallback parsing when JSON parsing fails."""
        logger.warning("Using fallback parsing for Groq response")

        # This could implement basic text parsing as a fallback
        # For now, return a low-confidence failed result
        return ResumeAnalysisResult(
            candidate_info={},
            experiences=[],
            educations=[],
            projects=[],
            skills=[],
            confidence_score=0.1,
            success=False,
            error_message="Failed to parse structured data from AI response",
            raw_response=response_text
        )

    def validate_analysis_result(self, result: ResumeAnalysisResult) -> bool:
        """Validate the analysis result quality."""
        if not result.success:
            return False

        # Check if we got meaningful data
        has_candidate_info = bool(result.candidate_info.get("name") or result.candidate_info.get("email"))
        has_experience = len(result.experiences) > 0
        has_education = len(result.educations) > 0

        # Require at least candidate info and either experience or education
        return has_candidate_info and (has_experience or has_education)
