"""
ExamHub - Proctoring Repository Layer
Handles high-throughput ingestion of telemetry events, candidate timelines,
and proctoring audit storage.
"""

from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime
from backend.app.database.connection import get_db_connection

class ProctoringRepository:
    """Telemetry persistence and query layer for exam session events."""

    @staticmethod
    def ensure_columns():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(proctoring_logs)")
        cols = [c[1] for c in cursor.fetchall()]
        if "severity" not in cols:
            cursor.execute("ALTER TABLE proctoring_logs ADD COLUMN severity TEXT DEFAULT 'low'")
            conn.commit()

    @staticmethod
    def log_event(attempt_id: str, event_type: str, details: Optional[str], severity: str = "low") -> str:
        ProctoringRepository.ensure_columns()
        conn = get_db_connection()
        cursor = conn.cursor()
        event_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        cursor.execute("""
            INSERT INTO proctoring_logs (id, attempt_id, event_type, details, timestamp, severity)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (event_id, attempt_id, event_type, details or "", timestamp, severity))
        conn.commit()
        return event_id

    @staticmethod
    def get_events_for_attempt(attempt_id: str) -> List[Dict[str, Any]]:
        ProctoringRepository.ensure_columns()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, attempt_id, event_type, details, timestamp, severity
            FROM proctoring_logs
            WHERE attempt_id = ?
            ORDER BY timestamp ASC
        """, (attempt_id,))
        return [dict(r) for r in cursor.fetchall()]

    @staticmethod
    def get_recent_system_events(limit: int = 50) -> List[Dict[str, Any]]:
        ProctoringRepository.ensure_columns()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, attempt_id, event_type, details, timestamp, severity
            FROM proctoring_logs
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        return [dict(r) for r in cursor.fetchall()]

    @staticmethod
    def get_active_proctored_sessions() -> List[Dict[str, Any]]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ea.id as attempt_id, ea.time_remaining_seconds, ea.status,
                   ea.updated_at as last_ping, e.name as exam_name,
                   u.full_name as student_name, st.student_id_code as roll_number,
                   (SELECT COUNT(*) FROM proctoring_logs pl WHERE pl.attempt_id = ea.id) as warning_count
            FROM exam_attempts ea
            JOIN exams e ON ea.exam_id = e.id
            JOIN students st ON ea.student_id = st.id
            JOIN users u ON st.user_id = u.id
            WHERE ea.status = 'in_progress'
            ORDER BY ea.updated_at DESC
        """)
        return [dict(r) for r in cursor.fetchall()]
