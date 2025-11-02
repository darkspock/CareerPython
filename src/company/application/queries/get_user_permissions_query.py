from dataclasses import dataclass
from typing import Optional, Dict, Any

from src.company.domain.value_objects import CompanyId
from src.company.domain.infrastructure.company_user_repository_interface import (
    CompanyUserRepositoryInterface
)
from src.company.domain.exceptions.company_exceptions import CompanyNotFoundError
from src.shared.application.query_bus import Query, QueryHandler
from src.user.domain.value_objects.UserId import UserId


@dataclass
class GetUserPermissionsQuery(Query):
    """Query to get permissions for a company user"""
    company_id: str
    user_id: str


class GetUserPermissionsQueryHandler(QueryHandler[GetUserPermissionsQuery, Optional[Dict[str, Any]]]):
    """Handler for getting user permissions - returns dict with role and permissions"""

    def __init__(self, company_user_repository: CompanyUserRepositoryInterface):
        self.company_user_repository = company_user_repository

    def handle(self, query: GetUserPermissionsQuery) -> Optional[Dict[str, Any]]:
        """Execute the query - returns dict with permissions or None"""
        company_id = CompanyId.from_string(query.company_id)
        user_id = UserId.from_string(query.user_id)

        company_user = self.company_user_repository.get_by_company_and_user(company_id, user_id)

        if not company_user:
            return None

        return {
            "role": company_user.role.value,
            "permissions": company_user.permissions.to_dict(),
            "status": company_user.status.value,
        }

