"""
ExamHub Exam Delivery - FastAPI Router
Endpoints for secure candidate delivery sessions, lockdown heartbeats, and offline sync.
"""

from datetime import datetime, timezone
from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.exam_delivery.schemas import (
    LockdownHeartbeatRequest,
    LockdownStatusResponse,
    OfflineSyncBatchRequest,
    OfflineSyncBatchResponse,
    ShuffledQuestionItem,
)
from backend.app.exam_delivery.lockdown_enforcer import LockdownEnforcer
from backend.app.exam_delivery.randomizer_engine import RandomizerEngine
from backend.app.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/delivery", tags=["Secure Candidate Exam Delivery"])
_VIOLATIONS_STORE: Dict[str, int] = {}  # session_id -> count


@router.post("/heartbeat", response_model=LockdownStatusResponse)
def submit_lockdown_heartbeat(
    req: LockdownHeartbeatRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Submits periodic client telemetry verifying fullscreen lockdown and single display focus.
    """
    current_v = _VIOLATIONS_STORE.get(req.session_id, 0)
    allowed, issued, msg, new_v = LockdownEnforcer.evaluate_heartbeat(req, current_v)
    _VIOLATIONS_STORE[req.session_id] = new_v

    return LockdownStatusResponse(
        session_id=req.session_id,
        allowed_to_continue=allowed,
        warning_issued=issued,
        warning_message=msg,
        violation_count=new_v
    )


@router.get("/exam/{exam_id}/shuffled-package", response_model=List[ShuffledQuestionItem])
def get_shuffled_exam_package(
    exam_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Fetches deterministically randomized question sequence and option permutations for candidate.
    """
    candidate_id = str(current_user.get("id", "cand_default"))

    raw_sample_questions = [
        {"id": "q1", "prompt": "What is the time complexity of lookup in a balanced red-black tree?", "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"], "points": 2.0},
        {"id": "q2", "prompt": "Which HTTP status code signifies that a resource has been permanently moved?", "options": ["301 Moved Permanently", "302 Found", "307 Temporary Redirect", "308 Permanent Redirect"], "points": 1.0},
        {"id": "q3", "prompt": "Which isolation level prevents phantom reads in SQL databases?", "options": ["Read Uncommitted", "Read Committed", "Repeatable Read", "Serializable"], "points": 2.0},
        {"id": "q4", "prompt": "In public-key cryptography, what encrypts data for confidential reception?", "options": ["Sender's Private Key", "Recipient's Public Key", "Sender's Public Key", "Certificate Authority Key"], "points": 2.0},
    ]

    return RandomizerEngine.generate_candidate_package(candidate_id, exam_id, raw_sample_questions)


@router.post("/offline-sync", response_model=OfflineSyncBatchResponse)
def sync_offline_answers(
    req: OfflineSyncBatchRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Accepts client-side cached answers saved during temporary network disconnection.
    """
    return OfflineSyncBatchResponse(
        session_id=req.session_id,
        accepted_count=len(req.batch_submissions),
        conflict_count=0,
        latest_synced_counter=max([s.vector_clock_counter for s in req.batch_submissions], default=1),
        server_time_iso=datetime.now(timezone.utc).isoformat()
    )
