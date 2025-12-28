"""
In-App Notification Router - For company users to manage their notifications.

Company-scoped routes for in-app notifications.
URL Pattern: /{company_slug}/admin/notifications/*
"""
import logging
from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query, status

from adapters.http.company_app.notification.controllers.notification_controller import NotificationController
from adapters.http.company_app.notification.schemas.notification_schemas import (
    NotificationListResponse,
    UnreadCountResponse
)
from adapters.http.shared.dependencies.company_context import AdminCompanyContext, CurrentCompanyUser
from core.containers import Container

log = logging.getLogger(__name__)

router = APIRouter(prefix="/{company_slug}/admin/notifications", tags=["In-App Notifications"])


@router.get(
    "",
    response_model=NotificationListResponse,
    summary="List notifications for the current user"
)
@inject
def list_notifications(
    company: AdminCompanyContext,
    current_user: CurrentCompanyUser,
    controller: Annotated[NotificationController, Depends(Provide[Container.notification_controller])],
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    unread_only: bool = Query(default=False)
) -> NotificationListResponse:
    """List in-app notifications for the current user"""
    try:
        return controller.list_notifications(
            user_id=current_user.id,
            company_id=company.id,
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
def get_unread_count(
    company: AdminCompanyContext,
    current_user: CurrentCompanyUser
) -> UnreadCountResponse:
    """Get the count of unread notifications for the current user.

    TODO: Implement full notification system. Currently returns 0.
    """
    # Stub implementation - returns 0 until notification system is fully implemented
    return UnreadCountResponse(unread_count=0)


@router.post(
    "/{notification_id}/read",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Mark a notification as read"
)
@inject
def mark_as_read(
    notification_id: str,
    company: AdminCompanyContext,
    current_user: CurrentCompanyUser,
    controller: Annotated[NotificationController, Depends(Provide[Container.notification_controller])]
) -> None:
    """Mark a specific notification as read"""
    try:
        controller.mark_as_read(
            notification_id=notification_id,
            user_id=current_user.id,
            company_id=company.id
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
    company: AdminCompanyContext,
    current_user: CurrentCompanyUser,
    controller: Annotated[NotificationController, Depends(Provide[Container.notification_controller])]
) -> None:
    """Mark all notifications as read for the current user"""
    try:
        controller.mark_all_as_read(user_id=current_user.id, company_id=company.id)
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
    company: AdminCompanyContext,
    current_user: CurrentCompanyUser,
    controller: Annotated[NotificationController, Depends(Provide[Container.notification_controller])]
) -> None:
    """Delete a specific notification"""
    try:
        controller.delete_notification(
            notification_id=notification_id,
            user_id=current_user.id,
            company_id=company.id
        )
    except Exception as e:
        log.error(f"Error deleting notification: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
