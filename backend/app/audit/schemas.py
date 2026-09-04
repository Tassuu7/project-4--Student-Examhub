"""
ExamHub - System Audit & Compliance Logging Schemas
Data contracts for administrative activity tracking and FERPA/GDPR compliance logs.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class AuditLogItem(BaseModel):
    id: str
    user_id: Optional[str] = None
    username: Optional[str] = None
    action: str
    entity_type: str
    entity_id: Optional[str] = None
    details_json: Optional[str] = None
    created_at: str

class AuditLogsListResponse(BaseModel):
    total_records: int
    items: List[AuditLogItem]
