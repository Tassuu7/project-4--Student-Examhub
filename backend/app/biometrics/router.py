"""
ExamHub Biometrics - FastAPI Router
Endpoints for enrolling keystroke profiles and verifying identity during exams.
"""

from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.biometrics.schemas import (
    KeystrokeVerificationRequest,
    PoseTelemetryEvent,
    BiometricVerificationResult,
    TypingProfile,
    KeystrokeEvent,
)
from backend.app.biometrics.keystroke_dynamics import KeystrokeDynamicsEngine
from backend.app.biometrics.pose_tracker import PoseTracker
from backend.app.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/biometrics", tags=["Biometrics & Continuous Authentication"])

_ENROLLED_PROFILES: Dict[str, TypingProfile] = {}


def _seed_profile():
    # Enrolled default profile for student
    sample_events = [
        KeystrokeEvent(key="h", down_time_ms=100.0, up_time_ms=180.0),
        KeystrokeEvent(key="e", down_time_ms=220.0, up_time_ms=310.0),
        KeystrokeEvent(key="l", down_time_ms=360.0, up_time_ms=440.0),
        KeystrokeEvent(key="l", down_time_ms=490.0, up_time_ms=570.0),
        KeystrokeEvent(key="o", down_time_ms=630.0, up_time_ms=710.0),
    ]
    prof = KeystrokeDynamicsEngine.build_profile("user_student_1", sample_events, "hello")
    _ENROLLED_PROFILES["user_student_1"] = prof

_seed_profile()


@router.post("/enroll", response_model=TypingProfile)
def enroll_keystroke_profile(
    events: List[KeystrokeEvent],
    sample_text: str = "",
    current_user: dict = Depends(get_current_user)
):
    """
    Enrolls candidate's typing signature baseline.
    """
    cid = str(current_user.get("id", "unknown_user"))
    profile = KeystrokeDynamicsEngine.build_profile(cid, events, sample_text)
    _ENROLLED_PROFILES[cid] = profile
    return profile


@router.post("/verify-keystrokes", response_model=BiometricVerificationResult)
def verify_keystrokes(
    req: KeystrokeVerificationRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Verifies live keystroke telemetry against enrolled typing signature.
    """
    profile = _ENROLLED_PROFILES.get(req.candidate_id)
    if not profile:
        # Auto enroll if not yet available
        profile = KeystrokeDynamicsEngine.build_profile(req.candidate_id, req.events)
        _ENROLLED_PROFILES[req.candidate_id] = profile

    sim = KeystrokeDynamicsEngine.compute_similarity(profile, req.events)
    is_verified = sim >= req.threshold_similarity

    return BiometricVerificationResult(
        session_id=req.session_id,
        candidate_id=req.candidate_id,
        keystroke_similarity=sim,
        is_keystroke_verified=is_verified,
        pose_alert_flag=False,
        pose_alert_reason=None,
        overall_trust_index=round(sim * 100.0, 1)
    )


@router.post("/telemetry-pose")
def ingest_pose_telemetry(
    event: PoseTelemetryEvent,
    current_user: dict = Depends(get_current_user)
):
    """
    Continuous webcam head angle and gaze telemetry ingestion.
    """
    is_suspicious, reason = PoseTracker.evaluate_pose(event)
    return {
        "received": True,
        "flagged": is_suspicious,
        "reason": reason,
        "session_id": event.session_id
    }
