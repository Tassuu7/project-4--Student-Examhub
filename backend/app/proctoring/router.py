"""
ExamHub - Proctoring & Exam Integrity API Router
Exposes endpoints for telemetry logging, active candidate feeds,
and candidate integrity score inspections.
"""

from fastapi import APIRouter, Depends
from typing import Dict, Any

from backend.app.auth.dependencies import get_current_user
from backend.app.auth.rbac import require_role
from backend.app.proctoring.schemas import (
    ProctoringEventIngest, CandidateIntegrityProfile, ProctoringLiveFeedResponse,
    TeacherWarningRequest, TerminateSessionRequest
)
from backend.app.proctoring.service import ProctoringService

router = APIRouter(prefix="/proctoring", tags=["Proctoring & Exam Integrity"])

@router.post("/events")
def ingest_proctoring_event(
    payload: ProctoringEventIngest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Candidate endpoint: Ingest client-side telemetry (tab switch, window blur, audio)."""
    event_id = ProctoringService.ingest_event(
        attempt_id=payload.attempt_id,
        event_type=payload.event_type,
        details=payload.details,
        severity=payload.severity or "low"
    )
    return {"status": "logged", "event_id": event_id}

@router.get("/candidate/{attempt_id}", response_model=CandidateIntegrityProfile)
def get_candidate_integrity(
    attempt_id: str,
    current_user: Dict[str, Any] = Depends(require_role(["admin", "teacher"]))
):
    """Teacher/Admin endpoint: Retrieve integrity score, risk level, and telemetry timeline."""
    return ProctoringService.get_candidate_integrity(attempt_id)

@router.get("/feed", response_model=ProctoringLiveFeedResponse)
def get_live_monitoring_feed(
    current_user: Dict[str, Any] = Depends(require_role(["admin", "teacher"]))
):
    """Teacher/Admin endpoint: Real-time dashboard feed of all active test-takers and alerts."""
    return ProctoringService.get_live_monitoring_feed()

@router.post("/warning")
def send_candidate_warning(
    payload: TeacherWarningRequest,
    current_user: Dict[str, Any] = Depends(require_role(["admin", "teacher"]))
):
    """Teacher/Admin endpoint: Broadcast a warning message directly to candidate session."""
    event_id = ProctoringService.send_warning(payload.attempt_id, payload.warning_message)
    return {"status": "warning_sent", "event_id": event_id}

@router.post("/terminate")
def terminate_candidate_session(
    payload: TerminateSessionRequest,
    current_user: Dict[str, Any] = Depends(require_role(["admin", "teacher"]))
):
    """Teacher/Admin endpoint: Terminate an active exam attempt for academic dishonesty."""
    ProctoringService.terminate_session(payload.attempt_id, payload.reason)
    return {"status": "session_terminated", "attempt_id": payload.attempt_id}

@router.post("/clear-flags/{attempt_id}")
def clear_candidate_flags(
    attempt_id: str,
    current_user: Dict[str, Any] = Depends(require_role(["admin", "teacher"]))
):
    """Teacher/Admin endpoint: Clear anomalous integrity flags after proctor audit."""
    ProctoringService.clear_flags(attempt_id)
    return {"status": "flags_cleared", "attempt_id": attempt_id}
