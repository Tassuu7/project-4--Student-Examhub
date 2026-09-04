"""
ExamHub - Candidate Integrity Scoring Algorithm
Computes an objective, multi-factor academic honesty score (0 to 100)
based on frequency, severity, and temporal density of anomalous telemetry events.
"""

from typing import List, Dict, Any, Tuple

class IntegrityScorer:
    """Mathematical penalization and risk classification engine for online tests."""

    PENALTY_WEIGHTS = {
        "tab_switch": 8.0,
        "blur": 4.0,
        "multiple_faces": 25.0,
        "face_loss": 12.0,
        "audio_spike": 6.0,
        "devtools_open": 30.0,
        "copy_paste_attempt": 15.0,
        "ip_change": 20.0,
        "fullscreen_exit": 7.0
    }

    @staticmethod
    def calculate_integrity_score(events: List[Dict[str, Any]]) -> Tuple[float, str, Dict[str, int]]:
        """
        Calculates integrity score from 100.0 (clean) downwards.
        Returns (score, risk_level, breakdown_counts).
        """
        base_score = 100.0
        counts = {
            "tab_switch": 0,
            "blur": 0,
            "audio_spike": 0,
            "face_anomalies": 0,
            "devtools": 0,
            "other": 0
        }

        total_penalty = 0.0

        for event in events:
            etype = event.get("event_type", "").lower()
            severity = event.get("severity", "low").lower()

            weight = IntegrityScorer.PENALTY_WEIGHTS.get(etype, 3.0)

            # Severity multiplier
            if severity == "critical":
                multiplier = 2.0
            elif severity == "high":
                multiplier = 1.5
            elif severity == "medium":
                multiplier = 1.2
            else:
                multiplier = 1.0

            total_penalty += weight * multiplier

            if etype == "tab_switch":
                counts["tab_switch"] += 1
            elif etype == "blur":
                counts["blur"] += 1
            elif etype == "audio_spike":
                counts["audio_spike"] += 1
            elif etype in ("multiple_faces", "face_loss"):
                counts["face_anomalies"] += 1
            elif etype == "devtools_open":
                counts["devtools"] += 1
            else:
                counts["other"] += 1

        final_score = max(0.0, min(100.0, round(base_score - total_penalty, 1)))

        if final_score >= 85.0:
            risk = "Normal"
        elif final_score >= 70.0:
            risk = "Moderate"
        elif final_score >= 50.0:
            risk = "High"
        else:
            risk = "Severe"

        return final_score, risk, counts
