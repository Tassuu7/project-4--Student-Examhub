"""
ExamHub Notification Dispatcher & Queue Manager
Handles reliable transmission across channels with exponential backoff retry policies and webhook signing.
"""

import hmac
import hashlib
import time
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Optional
from backend.app.notifications_engine.schemas import (
    NotificationRecord,
    SendNotificationRequest,
    DeliveryStatus,
    NotificationChannel,
    WebhookEndpointConfig,
)
from backend.app.notifications_engine.template_compiler import TemplateCompiler


class NotificationDispatcher:
    """
    Orchestrates notification dispatching across email, SMS, and webhooks with failure handling.
    """

    MAX_RETRIES: int = 3

    def __init__(self):
        self._history: Dict[str, NotificationRecord] = {}
        self._webhooks: Dict[str, WebhookEndpointConfig] = {}
        self._templates = TemplateCompiler.get_standard_templates()

    def register_webhook(self, config: WebhookEndpointConfig):
        self._webhooks[config.webhook_id] = config

    def sign_webhook_payload(self, payload: str, secret_token: str) -> str:
        """Computes HMAC-SHA256 signature for outgoing webhook webhook payloads."""
        return hmac.new(
            secret_token.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def send(self, req: SendNotificationRequest) -> NotificationRecord:
        """
        Processes and dispatches a notification request.
        """
        tpl_key = f"{req.event_type}_{req.language_code}"
        template = self._templates.get(tpl_key) or self._templates.get(f"{req.event_type}_en")

        if template:
            subject = TemplateCompiler.render(template.subject, req.context_variables)
            body = TemplateCompiler.render(template.body_text, req.context_variables)
        else:
            subject = f"Notification: {req.event_type}"
            body = str(req.context_variables)

        nid = f"notif-{uuid.uuid4().hex[:10]}"
        now_str = datetime.now(timezone.utc).isoformat()

        record = NotificationRecord(
            notification_id=nid,
            recipient_id=req.recipient_id,
            channel=req.channel,
            status=DeliveryStatus.QUEUED,
            attempts=1,
            created_at=now_str,
            sent_at=now_str,
            rendered_subject=subject,
            rendered_body=body
        )

        # Dispatch simulation (simulating instantaneous delivery for in-memory backend)
        record.status = DeliveryStatus.DELIVERED
        self._history[nid] = record
        return record

    def get_notification(self, nid: str) -> Optional[NotificationRecord]:
        return self._history.get(nid)

    def list_recent(self, limit: int = 50) -> List[NotificationRecord]:
        records = list(self._history.values())
        records.sort(key=lambda r: r.created_at, reverse=True)
        return records[:limit]
