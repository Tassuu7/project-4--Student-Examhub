"""
ExamHub - Real-Time Behavioral Anomaly Detector
Analyzes streaming events to flag velocity outliers, rapid window alternating,
and collusion indicators during live assessments.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

class AnomalyDetector:
    """Heuristic rule engine for suspicious exam behavior patterns."""

    @staticmethod
    def evaluate_tab_burst(recent_events: List[Dict[str, Any]], window_seconds: int = 60) -> bool:
        """Flags if user switched tabs 3 or more times within a 60-second burst window."""
        tab_events = [e for e in recent_events if e.get("event_type") == "tab_switch"]
        if len(tab_events) < 3:
            return False

        timestamps = []
        for e in tab_events:
            try:
                dt = datetime.fromisoformat(e["timestamp"])
                timestamps.append(dt)
            except Exception:
                continue

        timestamps.sort()
        for i in range(len(timestamps) - 2):
            delta = (timestamps[i + 2] - timestamps[i]).total_seconds()
            if delta <= window_seconds:
                return True
        return False

    @staticmethod
    def evaluate_velocity(question_time_seconds: float, question_word_count: int) -> Dict[str, Any]:
        """Detects if response was recorded faster than human reading comprehension thresholds."""
        # Average adult reading speed: ~200-250 wpm -> ~3-4 words per second
        min_reading_time = max(3.0, (question_word_count / 4.0))
        is_suspicious_rapid = question_time_seconds < min_reading_time

        return {
            "is_suspiciously_fast": is_suspicious_rapid,
            "recorded_time": question_time_seconds,
            "min_expected_time": round(min_reading_time, 1),
            "flag": "Speed anomaly - potential prior question leakage" if is_suspicious_rapid else "Normal"
        }
