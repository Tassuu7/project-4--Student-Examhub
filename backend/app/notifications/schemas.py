"""
ExamHub - In-App Notifications & Alert Broadcast Schemas
Data models for student announcements, exam schedule alerts, and score release notices.
"""

from typing import Optional, List
from pydantic import BaseModel

class NotificationCreate(BaseModel):
    user_id: str
    title: str
    message: str
    type: str = "info"  # info, warning, success, alert
    link: Optional[str] = None

class NotificationItem(BaseModel):
    id: str
    user_id: str
    title: str
    message: str
    type: str
    is_read: bool
    link: Optional[str] = None
    created_at: str

class NotificationBroadcastRequest(BaseModel):
    role_target: Optional[str] = None  # all, student, teacher
    title: str
    message: str
    type: str = "announcement"
    link: Optional[str] = None
