"""
ExamHub - In-App Notifications API Router
Exposes endpoints for retrieving user alerts and marking notifications read.
"""

from fastapi import APIRouter, Depends
from typing import List, Dict, Any

from backend.app.auth.dependencies import get_current_user
from backend.app.notifications.schemas import NotificationItem
from backend.app.notifications.service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications & Alerts"])

@router.get("/my", response_model=List[NotificationItem])
def get_my_notifications(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Retrieve in-app notifications for the authenticated user."""
    return NotificationService.get_user_notifications(current_user["id"])

@router.post("/read/{notification_id}")
def mark_read(
    notification_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Mark a specific notification as read."""
    success = NotificationService.mark_as_read(notification_id, current_user["id"])
    return {"status": "ok", "marked_read": success}
