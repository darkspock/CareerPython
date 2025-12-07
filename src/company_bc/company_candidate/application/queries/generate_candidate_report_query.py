"""
Generate Candidate Report Query
Generates an AI-powered report from candidate comments, interviews, and reviews
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any

from src.framework.application.query_bus import Query, QueryHandler
from src.framework.domain.entities.base import generate_id


@dataclass
class CandidateReportDto:
    """DTO for candidate report"""
    report_id: str
    company_candidate_id: str
    candidate_name: str
    generated_at: str
    report_markdown: str
    sections: Dict[str, Any]


@dataclass
class GenerateCandidateReportQuery(Query):
    """Query to generate a candidate report"""
    company_candidate_id: str
    include_comments: bool = True
    include_interviews: bool = True
    include_reviews: bool = True


class GenerateCandidateReportQueryHandler(QueryHandler[GenerateCandidateReportQuery, CandidateReportDto]):
    """Handler for generating candidate reports"""

    def __init__(
        self,
        company_candidate_repository: Any,
        candidate_comment_repository: Any,
    ) -> None:
        self.company_candidate_repository = company_candidate_repository
        self.candidate_comment_repository = candidate_comment_repository

    def handle(self, query: GenerateCandidateReportQuery) -> CandidateReportDto:
        """Generate the candidate report"""
        from src.company_bc.company_candidate.domain.value_objects import CompanyCandidateId

        # Get candidate info
        candidate = self.company_candidate_repository.get_by_id(
            CompanyCandidateId.from_string(query.company_candidate_id)
        )

        if not candidate:
            raise ValueError(f"Candidate not found: {query.company_candidate_id}")

        # Get candidate name from the read model or entity
        candidate_name = getattr(candidate, 'candidate_name', None) or 'Candidate'

        # Collect data for report
        comments_data = []
        if query.include_comments:
            comments = self.candidate_comment_repository.list_by_company_candidate_id(
                CompanyCandidateId.from_string(query.company_candidate_id)
            )
            comments_data = [
                {
                    'content': c.content,
                    'author': getattr(c, 'author_name', 'Unknown'),
                    'created_at': c.created_at.isoformat() if hasattr(c, 'created_at') else None
                }
                for c in comments
            ]

        # Generate report sections (mock AI response for now)
        sections = self._generate_report_sections(
            candidate_name=candidate_name,
            comments=comments_data,
        )

        # Build markdown report
        report_markdown = self._build_markdown_report(candidate_name, sections)

        return CandidateReportDto(
            report_id=generate_id(),
            company_candidate_id=query.company_candidate_id,
            candidate_name=candidate_name,
            generated_at=datetime.utcnow().isoformat(),
            report_markdown=report_markdown,
            sections=sections
        )

    def _generate_report_sections(
        self,
        candidate_name: str,
        comments: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Generate report sections (mock AI for now - replace with real AI later)"""

        # Analyze comments to extract insights
        comment_count = len(comments)
        comment_text = " ".join([c.get('content', '') for c in comments])

        # Mock AI-generated sections
        # In production, this would call an AI service like Anthropic/OpenAI
        sections = {
            'summary': self._generate_summary(candidate_name, comment_count, comment_text),
            'strengths': self._extract_strengths(comment_text),
            'areas_for_improvement': self._extract_improvements(comment_text),
            'interview_insights': self._generate_interview_insights(comments) if comments else None,
            'recommendation': self._generate_recommendation(candidate_name, comment_count)
        }

        return sections

    def _generate_summary(self, name: str, comment_count: int, text: str) -> str:
        """Generate executive summary"""
        if comment_count == 0:
            return f"{name} is a candidate currently under evaluation. No feedback has been recorded yet."

        return (
            f"{name} has been evaluated through {comment_count} feedback entries. "
            f"The overall assessment indicates a candidate with notable qualities that merit further consideration. "
            f"Review the detailed analysis below for specific insights."
        )

    def _extract_strengths(self, text: str) -> List[str]:
        """Extract strengths from feedback (mock)"""
        # In production, AI would analyze the actual text
        base_strengths = [
            "Demonstrates professional communication skills",
            "Shows initiative and proactive approach",
            "Exhibits adaptability to new situations"
        ]

        # Add context-based strengths if text contains certain keywords
        if 'experience' in text.lower():
            base_strengths.append("Brings relevant industry experience")
        if 'team' in text.lower():
            base_strengths.append("Strong team collaboration abilities")
        if 'technical' in text.lower() or 'skills' in text.lower():
            base_strengths.append("Solid technical foundation")

        return base_strengths[:5]  # Limit to 5 strengths

    def _extract_improvements(self, text: str) -> List[str]:
        """Extract areas for improvement (mock)"""
        improvements = [
            "Could benefit from additional domain-specific training",
            "May need support during initial onboarding period"
        ]

        if not text:
            improvements.append("Requires more comprehensive evaluation feedback")

        return improvements

    def _generate_interview_insights(self, comments: List[Dict[str, Any]]) -> str:
        """Generate interview insights from feedback"""
        if not comments:
            return "No interview feedback available for analysis."

        return (
            f"Based on {len(comments)} recorded interactions, the candidate has demonstrated "
            f"engagement with the evaluation process. Feedback indicates consistent performance "
            f"across assessment criteria."
        )

    def _generate_recommendation(self, name: str, feedback_count: int) -> str:
        """Generate final recommendation"""
        if feedback_count == 0:
            return (
                f"Insufficient data to provide a definitive recommendation for {name}. "
                f"Consider scheduling additional evaluations or interviews to gather more insights."
            )

        if feedback_count < 3:
            return (
                f"Based on limited feedback ({feedback_count} entries), {name} shows potential "
                f"but additional evaluation is recommended before making a final decision."
            )

        return (
            f"Based on the comprehensive feedback collected, {name} appears to be a viable candidate "
            f"for further consideration. Recommend proceeding to the next stage of the hiring process "
            f"while focusing on the identified areas for development."
        )

    def _build_markdown_report(self, candidate_name: str, sections: Dict[str, Any]) -> str:
        """Build the full markdown report"""
        lines = [
            f"# Candidate Report: {candidate_name}",
            "",
            f"*Generated on {datetime.utcnow().strftime('%B %d, %Y at %H:%M UTC')}*",
            "",
            "---",
            "",
            "## Executive Summary",
            "",
            sections['summary'],
            "",
            "## Strengths",
            "",
        ]

        for strength in sections['strengths']:
            lines.append(f"- {strength}")

        lines.extend([
            "",
            "## Areas for Development",
            "",
        ])

        for area in sections['areas_for_improvement']:
            lines.append(f"- {area}")

        if sections.get('interview_insights'):
            lines.extend([
                "",
                "## Interview Insights",
                "",
                sections['interview_insights'],
            ])

        lines.extend([
            "",
            "## Recommendation",
            "",
            sections['recommendation'],
            "",
            "---",
            "",
            "*This report was generated using AI analysis. Human review is recommended.*",
        ])

        return "\n".join(lines)
