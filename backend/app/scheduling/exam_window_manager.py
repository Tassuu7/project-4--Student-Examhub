"""
ExamHub - Global Examination Window & Timezone Manager
Manages flexible multi-timezone start windows and accommodates global distance learners.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone

class ExamWindowManager:
    """Calculates active testing windows and evaluates candidate entry eligibility."""

    @staticmethod
    def evaluate_candidate_entry(
        start_time_iso: str,
        end_time_iso: str,
        duration_minutes: int,
        floating_window_minutes: int = 120
    ) -> Dict[str, Any]:
        """
        Evaluates whether candidate is within valid examination attendance window.
        """
        try:
            start_dt = datetime.fromisoformat(start_time_iso)
            end_dt = datetime.fromisoformat(end_time_iso)
        except Exception:
            return {"can_enter": False, "reason": "Malformed window timestamps"}

        now_utc = datetime.utcnow()
        if start_dt.tzinfo:
            now_utc = datetime.now(timezone.utc)

        # Before start time
        if now_utc < start_dt:
            delta_sec = int((start_dt - now_utc).total_seconds())
            return {
                "can_enter": False,
                "status": "Upcoming",
                "seconds_until_start": delta_sec,
                "reason": f"Examination opens in {delta_sec // 60} minutes."
            }

        # After overall end window
        if now_utc > end_dt:
            return {
                "can_enter": False,
                "status": "Closed",
                "reason": "Examination testing window has concluded."
            }

        # Check remaining time for full duration
        remaining_in_window_minutes = (end_dt - now_utc).total_seconds() / 60.0
        has_full_duration = remaining_in_window_minutes >= duration_minutes

        return {
            "can_enter": True,
            "status": "Open",
            "has_full_duration_available": has_full_duration,
            "allocated_duration_minutes": min(duration_minutes, int(remaining_in_window_minutes)),
            "reason": "Candidate authorized to enter active assessment."
        }
