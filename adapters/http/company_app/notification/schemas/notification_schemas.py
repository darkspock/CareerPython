from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class InAppNotificationResponse(BaseModel):
    """Response schema for in-app notification"""
    id: str
    user_id: str
    company_id: str
    notification_type: str
    title: str
    message: str
    priority: str
    is_read: bool
    created_at: str
    read_at: Optional[str] = None
    link: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class NotificationListResponse(BaseModel):
    """Response schema for notification list with pagination"""
    notifications: List[InAppNotificationResponse]
    total_count: int
    unread_count: int


class UnreadCountResponse(BaseModel):
    """Response schema for unread notification count"""
    unread_count: int
