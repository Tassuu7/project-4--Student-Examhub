"""
ExamHub Biometrics & Identity Verification - Schemas
Supports keystroke dynamics, typing rhythm signatures, and candidate head pose telemetry.
"""

from typing import List, Dict, Optional, Tuple
from pydantic import BaseModel, Field


class KeystrokeEvent(BaseModel):
    key: str
    down_time_ms: float
    up_time_ms: float


class DigraphFeature(BaseModel):
    digraph: str
    dwell_time_ms: float
    flight_time_ms: float


class TypingProfile(BaseModel):
    candidate_id: str
    sample_text: str
    mean_dwell_ms: float
    mean_flight_ms: float
    digraph_profiles: Dict[str, float]  # digraph -> mean transition time ms
    consistency_score: float = 1.0


class KeystrokeVerificationRequest(BaseModel):
    candidate_id: str
    session_id: str
    events: List[KeystrokeEvent]
    threshold_similarity: float = Field(default=0.70, ge=0.1, le=1.0)


class PoseTelemetryEvent(BaseModel):
    session_id: str
    candidate_id: str
    timestamp_ms: float
    yaw_degrees: float   # Left / Right turn (-90 to +90)
    pitch_degrees: float # Up / Down tilt (-90 to +90)
    roll_degrees: float  # Side tilt (-90 to +90)
    eyes_closed: bool = False
    face_detected: bool = True
    confidence: float = 0.95


class BiometricVerificationResult(BaseModel):
    session_id: str
    candidate_id: str
    keystroke_similarity: float
    is_keystroke_verified: bool
    pose_alert_flag: bool
    pose_alert_reason: Optional[str] = None
    overall_trust_index: float
