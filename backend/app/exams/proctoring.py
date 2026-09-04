"""
ExamHub - Proctoring and Examination Integrity Service
"""

from typing import Dict, Any, List, Optional
from backend.app.exams.repository import ExamRepository

class ProctoringService:
    @staticmethod
    def record_event(attempt_id: str, event_type: str, details: Optional[str] = None):
        """Records student integrity event such as tab switch, blur, fullscreen exit."""
        ExamRepository.log_proctoring_event(attempt_id, event_type, details)

    @staticmethod
    def get_integrity_summary(attempt_id: str) -> Dict[str, Any]:
        """Summarizes suspicious activities and proctoring warnings."""
        logs = ExamRepository.get_proctoring_logs(attempt_id)
        counts: Dict[str, int] = {}
        for l in logs:
            etype = l.get("event_type", "unknown")
            counts[etype] = counts.get(etype, 0) + 1

        total_violations = len(logs)
        severity = "Normal"
        if total_violations >= 5:
            severity = "High"
        elif total_violations >= 2:
            severity = "Moderate"

        return {
            "total_events": total_violations,
            "event_breakdown": counts,
            "severity": severity,
            "logs": logs
        }
