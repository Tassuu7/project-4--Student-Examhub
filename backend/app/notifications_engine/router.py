"""
ExamHub Notifications Engine - FastAPI Router
Endpoints for dispatching transactional alerts, managing webhook endpoints, and auditing delivery logs.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.notifications_engine.schemas import (
    SendNotificationRequest,
    NotificationRecord,
    WebhookEndpointConfig,
)
from backend.app.notifications_engine.dispatcher import NotificationDispatcher
from backend.app.auth.dependencies import require_role

router = APIRouter(prefix="/api/notifications-engine", tags=["Multichannel Notifications Engine"])
_DISPATCHER = NotificationDispatcher()


@router.post("/send", response_model=NotificationRecord)
def send_notification(
    req: SendNotificationRequest,
    current_user: dict = Depends(require_role(["teacher", "admin"]))
):
    """
    Dispatch an event notification via Email, SMS, or Webhook.
    """
    return _DISPATCHER.send(req)


@router.get("/logs", response_model=List[NotificationRecord])
def get_notification_logs(
    limit: int = 50,
    current_user: dict = Depends(require_role(["teacher", "admin"]))
):
    """
    Audit recent notification deliveries and transmission status.
    """
    return _DISPATCHER.list_recent(limit)


@router.post("/webhooks", response_model=WebhookEndpointConfig)
def register_webhook_endpoint(
    config: WebhookEndpointConfig,
    current_user: dict = Depends(require_role(["admin"]))
):
    """
    Register an external endpoint to receive automated HMAC-signed event webhooks.
    """
    _DISPATCHER.register_webhook(config)
    return config
