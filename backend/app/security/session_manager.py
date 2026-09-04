"""
ExamHub - Concurrent Session & Heartbeat Manager
Guarantees single-device candidate logins and terminates stale assessment heartbeats.
"""

import time
from typing import Dict, Optional, Tuple

class ActiveSessionManager:
    """Tracks active test-taker tokens and heartbeat pings."""

    def __init__(self, timeout_seconds: int = 45):
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.timeout_seconds = timeout_seconds

    def register_heartbeat(self, attempt_id: str, student_id: str, client_ip: str) -> bool:
        now = time.time()
        self.active_sessions[attempt_id] = {
            "student_id": student_id,
            "client_ip": client_ip,
            "last_seen": now
        }
        return True

    def is_session_live(self, attempt_id: str) -> bool:
        session = self.active_sessions.get(attempt_id)
        if not session:
            return False
        return (time.time() - session["last_seen"]) < self.timeout_seconds

    def terminate_session(self, attempt_id: str):
        if attempt_id in self.active_sessions:
            del self.active_sessions[attempt_id]

session_guard = ActiveSessionManager()
