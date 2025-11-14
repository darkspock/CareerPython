"""
Dashboard queries - Simplified for Interview Templates focus.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional

from src.framework.application.query_bus import Query, QueryHandler


# Dashboard Overview Queries
@dataclass
class GetDashboardOverviewQuery(Query):
    """Query to get dashboard overview - focused on Interview Templates."""
    user_id: str


# Query Handlers
class GetDashboardOverviewQueryHandler(QueryHandler[GetDashboardOverviewQuery, Dict[str, Any]]):
    """Handler for getting dashboard overview - simplified for Interview Templates."""

    def __init__(self, interview_template_repository: Optional[Any] = None) -> None:
        """Initialize with optional interview template repository."""
        self.interview_template_repository = interview_template_repository

    def handle(self, query: GetDashboardOverviewQuery) -> Dict[str, Any]:
        """Handle dashboard overview query - returns basic structure with interview templates."""
        # TODO: Replace with actual interview template listing when ready
        # For now, return empty structure to pass mypy
        return {
            'user_id': query.user_id,
            'interview_templates': [],  # Empty array as requested
            'generated_at': datetime.utcnow()
        }
