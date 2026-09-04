"""
ExamHub Exam Delivery & Secure Client - Schemas
Supports browser lockdown enforcement, offline synchronization, and deterministic candidate randomization.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class LockdownHeartbeatRequest(BaseModel):
    session_id: str
    candidate_id: str
    timestamp_ms: float
    is_fullscreen: bool
    window_focused: bool
    screen_count: int = 1
    detected_blacklisted_apps: List[str] = Field(default_factory=list)
    clipboard_content_length: int = 0


class LockdownStatusResponse(BaseModel):
    session_id: str
    allowed_to_continue: bool
    warning_issued: bool
    warning_message: Optional[str] = None
    violation_count: int = 0


class OfflineAnswerSubmission(BaseModel):
    submission_id: str
    question_id: str
    selected_option_index: Optional[int] = None
    text_answer: Optional[str] = None
    client_timestamp_ms: float
    vector_clock_counter: int
    client_signature: str


class OfflineSyncBatchRequest(BaseModel):
    session_id: str
    candidate_id: str
    batch_submissions: List[OfflineAnswerSubmission]


class OfflineSyncBatchResponse(BaseModel):
    session_id: str
    accepted_count: int
    conflict_count: int
    latest_synced_counter: int
    server_time_iso: str


class ShuffledQuestionItem(BaseModel):
    original_question_id: str
    display_index: int
    question_text: str
    shuffled_options: List[Dict[str, Any]]  # [{"option_key": "opt_A", "text": "...", "original_index": 2}]
    points: float
