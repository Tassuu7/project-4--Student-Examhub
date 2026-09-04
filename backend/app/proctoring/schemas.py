"""
ExamHub - Proctoring & Examination Integrity Schemas
Defines telemetry ingestion contracts, anomaly indicators, and integrity risk scores.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ProctoringEventIngest(BaseModel):
    attempt_id: str
    event_type: str = Field(..., description="tab_switch, blur, key_combination, multiple_faces, face_loss, audio_spike, devtools_open")
    details: Optional[str] = None
    client_timestamp: Optional[str] = None
    severity: Optional[str] = "low"  # low, medium, high, critical

class ProctoringEventItem(BaseModel):
    id: str
    attempt_id: str
    event_type: str
    details: Optional[str] = None
    timestamp: str
    severity: str

class CandidateIntegrityProfile(BaseModel):
    attempt_id: str
    student_id: str
    student_name: str
    roll_number: str
    exam_id: str
    exam_name: str
    integrity_score: float  # 0 to 100 (100 = spotless, < 60 = suspicious)
    risk_level: str  # Normal, Moderate, High, Severe
    total_anomalies: int
    tab_switch_count: int
    blur_count: int
    audio_spike_count: int
    face_anomalies_count: int
    devtools_attempts_count: int
    is_flagged_for_manual_review: bool
    events: List[ProctoringEventItem]

class ActiveSessionMonitoringItem(BaseModel):
    attempt_id: str
    student_name: str
    roll_number: str
    exam_name: str
    time_remaining_seconds: int
    current_status: str
    last_ping: str
    integrity_score: float
    total_warnings: int

class ProctoringLiveFeedResponse(BaseModel):
    active_sessions_count: int
    flagged_sessions_count: int
    active_candidates: List[ActiveSessionMonitoringItem]
    recent_events: List[ProctoringEventItem]

class TeacherWarningRequest(BaseModel):
    attempt_id: str
    warning_message: str

class TerminateSessionRequest(BaseModel):
    attempt_id: str
    reason: str
