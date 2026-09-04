"""
ExamHub - System Action Auditor Middleware & Decorator Helper
Dispatches administrative action records for security tracing.
"""

from typing import Optional, Dict, Any
import json
from backend.app.audit.repository import AuditRepository

class Auditor:
    """Convenience helper for recording system actions."""

    @staticmethod
    def log(user_id: Optional[str], action: str, entity_type: str, entity_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        details_str = json.dumps(details or {})
        return AuditRepository.record_action(user_id, action, entity_type, entity_id, details_str)
