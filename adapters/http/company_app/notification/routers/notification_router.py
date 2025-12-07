"""In-App Notification Router - For company users to manage their notifications"""
import base64
import json
import logging
from typing import Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query, Security, status
from fastapi.security import OAuth2PasswordBearer

from adapters.http.company_app.notification.controllers.notification_controller import NotificationController
from adapters.http.company_app.notification.schemas.notification_schemas import (
    NotificationListResponse,
    UnreadCountResponse
)
from core.containers import Container

log = logging.getLogger(__name__)

router = APIRouter(prefix="/api/company/notifications", tags=["In-App Notifications"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/companies/auth/login")


def get_company_id_from_token(token: str = Security(oauth2_scheme)) -> str:
    """Extract company_id from JWT token"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            raise HTTPException(status_code=401, detail="Invalid token format")

        payload = parts[1]
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding

        decoded = base64.urlsafe_b64decode(payload)
        data = json.loads(decoded)
        company_id = data.get('company_id')

        if not company_id or not isinstance(company_id, str):
            raise HTTPException(status_code=401, detail="company_id not found in token")

        return str(company_id)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error extracting company_id from token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


def get_user_id_from_token(token: str = Security(oauth2_scheme)) -> str:
    """Extract user_id (company_user_id) from JWT token"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            raise HTTPException(status_code=401, detail="Invalid token format")

        payload = parts[1]
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding

        decoded = base64.urlsafe_b64decode(payload)
        data = json.loads(decoded)
        user_id = data.get('company_user_id') or data.get('user_id')

        if not user_id or not isinstance(user_id, str):
            raise HTTPException(status_code=401, detail="user_id not found in token")

        return str(user_id)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error extracting user_id from token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get(
    "/",
    response_model=NotificationListResponse,
    summary="List notifications for the current user"
)
@inject
def list_notifications(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    unread_only: bool = Query(default=False),
    controller: NotificationController = Depends(Provide[Container.notification_controller]),
    company_id: str = Depends(get_company_id_from_token),
    user_id: str = Depends(get_user_id_from_token)
) -> NotificationListResponse:
    """List in-app notifications for the current user"""
    try:
        return controller.list_notifications(
            user_id=user_id,
            company_id=company_id,
            limit=limit,
            offset=offset,
            unread_only=unread_only
        )
    except Exception as e:
        log.error(f"Error listing notifications: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/unread-count",
    response_model=UnreadCountResponse,
    summary="Get unread notification count"
)
@inject
def get_unread_count(
    controller: NotificationController = Depends(Provide[Container.notification_controller]),
    company_id: str = Depends(get_company_id_from_token),
    user_id: str = Depends(get_user_id_from_token)
) -> UnreadCountResponse:
    """Get the count of unread notifications for the current user"""
    try:
        return controller.get_unread_count(user_id=user_id, company_id=company_id)
    except Exception as e:
        log.error(f"Error getting unread count: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post(
    "/{notification_id}/read",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Mark a notification as read"
)
@inject
def mark_as_read(
    notification_id: str,
    controller: NotificationController = Depends(Provide[Container.notification_controller]),
    company_id: str = Depends(get_company_id_from_token),
    user_id: str = Depends(get_user_id_from_token)
) -> None:
    """Mark a specific notification as read"""
    try:
        controller.mark_as_read(
            notification_id=notification_id,
            user_id=user_id,
            company_id=company_id
        )
    except Exception as e:
        log.error(f"Error marking notification as read: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post(
    "/read-all",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Mark all notifications as read"
)
@inject
def mark_all_as_read(
    controller: NotificationController = Depends(Provide[Container.notification_controller]),
    company_id: str = Depends(get_company_id_from_token),
    user_id: str = Depends(get_user_id_from_token)
) -> None:
    """Mark all notifications as read for the current user"""
    try:
        controller.mark_all_as_read(user_id=user_id, company_id=company_id)
    except Exception as e:
        log.error(f"Error marking all notifications as read: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a notification"
)
@inject
def delete_notification(
    notification_id: str,
    controller: NotificationController = Depends(Provide[Container.notification_controller]),
    company_id: str = Depends(get_company_id_from_token),
    user_id: str = Depends(get_user_id_from_token)
) -> None:
    """Delete a specific notification"""
    try:
        controller.delete_notification(
            notification_id=notification_id,
            user_id=user_id,
            company_id=company_id
        )
    except Exception as e:
        log.error(f"Error deleting notification: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
