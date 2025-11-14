from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Dict, Optional

from src.auth_bc.user.application.queries.dtos.auth_dto import TokenDto
from src.auth_bc.user.domain.services.token_service import TokenService
from src.framework.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class CreateAccessTokenQuery(Query):
    """Query to create an access token"""
    data: Dict[str, Any]
    expires_delta: Optional[timedelta] = None


class CreateAccessTokenQueryHandler(QueryHandler[CreateAccessTokenQuery, TokenDto]):
    """Handler for creating access tokens"""

    def handle(self, query: CreateAccessTokenQuery) -> TokenDto:
        """
        Handle access token creation

        Returns:
            TokenDto with token information
        """
        access_token = TokenService.create_access_token(
            data=query.data,
            expires_delta=query.expires_delta
        )

        # Calculate expires_in based on expires_delta or default
        expires_delta = query.expires_delta or timedelta(
            minutes=TokenService.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        expires_in = int(expires_delta.total_seconds())

        return TokenDto(
            access_token=access_token,
            token_type="bearer",
            expires_in=expires_in
        )
