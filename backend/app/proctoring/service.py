"""
ExamHub - Proctoring Application Service
Coordinates telemetry ingestion, real-time integrity evaluation,
flagging for manual review, and dashboard feeds.
"""

from typing import List, Dict, Any, Optional
from backend.app.proctoring.repository import ProctoringRepository
from backend.app.proctoring.integrity_scorer import IntegrityScorer
from backend.app.proctoring.schemas import (
    CandidateIntegrityProfile, ActiveSessionMonitoringItem,
    ProctoringLiveFeedResponse, ProctoringEventItem
)
from backend.app.database.connection import get_db_connection
from backend.app.core.exceptions import NotFoundException

class ProctoringService:
    """Service layer coordinating exam monitoring operations."""

    @staticmethod
    def ingest_event(attempt_id: str, event_type: str, details: Optional[str], severity: str = "low") -> str:
        return ProctoringRepository.log_event(attempt_id, event_type, details, severity)

    @staticmethod
    def get_candidate_integrity(attempt_id: str) -> CandidateIntegrityProfile:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ea.id as attempt_id, ea.student_id, ea.exam_id,
                   e.name as exam_name, u.full_name as student_name,
                   st.student_id_code as roll_number
            FROM exam_attempts ea
            JOIN exams e ON ea.exam_id = e.id
            JOIN students st ON ea.student_id = st.id
            JOIN users u ON st.user_id = u.id
            WHERE ea.id = ?
        """, (attempt_id,))
        row = cursor.fetchone()
        if not row:
            raise NotFoundException(f"Exam attempt '{attempt_id}' not found.")

        meta = dict(row)
        events_raw = ProctoringRepository.get_events_for_attempt(attempt_id)
        score, risk, counts = IntegrityScorer.calculate_integrity_score(events_raw)

        event_items = [
            ProctoringEventItem(
                id=e["id"],
                attempt_id=e["attempt_id"],
                event_type=e["event_type"],
                details=e["details"],
                timestamp=e["timestamp"],
                severity=e.get("severity", "low")
            ) for e in events_raw
        ]

        return CandidateIntegrityProfile(
            attempt_id=attempt_id,
            student_id=meta["student_id"],
            student_name=meta["student_name"],
            roll_number=meta["roll_number"],
            exam_id=meta["exam_id"],
            exam_name=meta["exam_name"],
            integrity_score=score,
            risk_level=risk,
            total_anomalies=len(events_raw),
            tab_switch_count=counts["tab_switch"],
            blur_count=counts["blur"],
            audio_spike_count=counts["audio_spike"],
            face_anomalies_count=counts["face_anomalies"],
            devtools_attempts_count=counts["devtools"],
            is_flagged_for_manual_review=(score < 70.0 or counts["devtools"] > 0),
            events=event_items
        )

    @staticmethod
    def get_live_monitoring_feed() -> ProctoringLiveFeedResponse:
        active_sessions = ProctoringRepository.get_active_proctored_sessions()
        recent_events_raw = ProctoringRepository.get_recent_system_events(30)

        candidates = []
        flagged_count = 0
        for s in active_sessions:
            att_id = s["attempt_id"]
            events_raw = ProctoringRepository.get_events_for_attempt(att_id)
            score, risk, _ = IntegrityScorer.calculate_integrity_score(events_raw)
            if score < 70.0:
                flagged_count += 1

            candidates.append(ActiveSessionMonitoringItem(
                attempt_id=att_id,
                student_name=s["student_name"],
                roll_number=s["roll_number"],
                exam_name=s["exam_name"],
                time_remaining_seconds=s["time_remaining_seconds"],
                current_status=s["status"],
                last_ping=s["last_ping"] or "",
                integrity_score=score,
                total_warnings=s["warning_count"]
            ))

        recent_events = [
            ProctoringEventItem(
                id=e["id"],
                attempt_id=e["attempt_id"],
                event_type=e["event_type"],
                details=e["details"],
                timestamp=e["timestamp"],
                severity=e.get("severity", "low")
            ) for e in recent_events_raw
        ]

        return ProctoringLiveFeedResponse(
            active_sessions_count=len(candidates),
            flagged_sessions_count=flagged_count,
            active_candidates=candidates,
            recent_events=recent_events
        )
