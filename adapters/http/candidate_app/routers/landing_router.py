import logging
from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from core.containers import Container
from src.auth_bc.user.application.queries.dtos.auth_dto import CurrentUserDto
from src.auth_bc.user.application.queries.get_current_user_from_token_query import GetCurrentUserFromTokenQuery
from src.framework.application.query_bus import QueryBus

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/candidate/onboarding", tags=["candidate-onboarding"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="candidate/auth/login")


@router.post("/subscribe")
async def subscribe_to_landing(name: str, email: str) -> JSONResponse:
    """Simple subscription endpoint for leads"""
    return JSONResponse(
        status_code=200,
        content={"message": "Suscripción exitosa", "name": name, "email": email}
    )


# Helper function to get current user
@inject
def get_current_user(
        query_bus: Annotated[QueryBus, Depends(Provide[Container.query_bus])],
        token: str = Security(oauth2_scheme),
) -> CurrentUserDto:
    """Get current user from JWT token"""
    try:
        query = GetCurrentUserFromTokenQuery(token=token)
        user_dto: CurrentUserDto = query_bus.query(query)
        if not user_dto:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_dto
    except Exception as e:
        logger.error(f"Error getting current user: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
