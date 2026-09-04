"""
ExamHub Notifications Engine - Schemas & Models
Supports multichannel notifications (Email, SMS, Webhook, In-App), localized templates, and delivery guarantees.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum


class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    WEBHOOK = "webhook"
    IN_APP = "in_app"


class NotificationPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class DeliveryStatus(str, Enum):
    QUEUED = "queued"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    DEAD_LETTER = "dead_letter"


class NotificationTemplate(BaseModel):
    template_id: str
    event_type: str  # e.g., "exam_reminder", "score_released", "proctor_flag"
    language_code: str = "en"
    subject: str
    body_text: str
    body_html: Optional[str] = None


class SendNotificationRequest(BaseModel):
    event_type: str
    recipient_id: str
    recipient_contact: str  # email or phone
    channel: NotificationChannel = NotificationChannel.EMAIL
    priority: NotificationPriority = NotificationPriority.NORMAL
    context_variables: Dict[str, Any] = Field(default_factory=dict)
    language_code: str = "en"


class NotificationRecord(BaseModel):
    notification_id: str
    recipient_id: str
    channel: NotificationChannel
    status: DeliveryStatus
    attempts: int = 0
    created_at: str
    sent_at: Optional[str] = None
    last_error: Optional[str] = None
    rendered_subject: str
    rendered_body: str


class WebhookEndpointConfig(BaseModel):
    webhook_id: str
    destination_url: str
    secret_token: str
    subscribed_events: List[str]
    is_active: bool = True
