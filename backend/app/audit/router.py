"""
ExamHub - System Audit API Router
Exposes administrative access to security audit trails and action histories.
"""

from fastapi import APIRouter, Depends, Query
from typing import Dict, Any, Optional

from backend.app.auth.rbac import require_role
from backend.app.audit.schemas import AuditLogsListResponse, AuditLogItem
from backend.app.audit.repository import AuditRepository

router = APIRouter(prefix="/audit", tags=["Audit & Security Logs"])

@router.get("/logs", response_model=AuditLogsListResponse)
def get_audit_logs(
    limit: int = Query(default=100, le=500),
    action: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(require_role(["admin"]))
):
    """Admin-only endpoint: Retrieve system audit logs with optional action filtering."""
    logs = AuditRepository.get_logs(limit=limit, action=action)
    items = [AuditLogItem(**l) for l in logs]
    return AuditLogsListResponse(total_records=len(items), items=items)
