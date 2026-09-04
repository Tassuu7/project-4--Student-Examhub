"""
ExamHub - Gaze Tracking & Head Pose Telemetry Analyzer
Classifies candidate eye-gaze direction and flags sustained off-screen deviations.
"""

from typing import List, Dict, Any, Tuple

class GazeTracker:
    """Processes webcam head pose (pitch, yaw, roll) and eye gaze vectors."""

    YAW_THRESHOLD_DEGREES = 28.0    # Left/Right looking away
    PITCH_THRESHOLD_DOWN = 22.0    # Looking down at phone/cheat sheet
    PITCH_THRESHOLD_UP = 25.0      # Looking up at ceiling/helper

    @staticmethod
    def classify_gaze_point(pitch: float, yaw: float, roll: float) -> Tuple[str, bool]:
        """
        pitch: vertical rotation (+ down, - up)
        yaw: horizontal rotation (+ right, - left)
        roll: tilt (+ right shoulder, - left shoulder)
        Returns (direction_label, is_off_screen).
        """
        if abs(yaw) > GazeTracker.YAW_THRESHOLD_DEGREES:
            dir_str = "Looking Right" if yaw > 0 else "Looking Left"
            return dir_str, True
        elif pitch > GazeTracker.PITCH_THRESHOLD_DOWN:
            return "Looking Down (Notes/Phone)", True
        elif pitch < -GazeTracker.PITCH_THRESHOLD_UP:
            return "Looking Up", True
        else:
            return "Center (On-Screen)", False

    @staticmethod
    def audit_gaze_stream(
        telemetry_samples: List[Dict[str, float]],
        sample_interval_seconds: float = 1.0
    ) -> Dict[str, Any]:
        """
        telemetry_samples: [{'pitch': 5.2, 'yaw': -12.1, 'roll': 1.0}, ...]
        """
        total_samples = len(telemetry_samples)
        if total_samples == 0:
            return {"total_duration_seconds": 0, "off_screen_percentage": 0.0}

        off_screen_count = 0
        longest_continuous_off = 0
        current_streak = 0

        breakdown = {"Center": 0, "Left": 0, "Right": 0, "Down": 0, "Up": 0}

        for s in telemetry_samples:
            label, is_off = GazeTracker.classify_gaze_point(s["pitch"], s["yaw"], s.get("roll", 0.0))
            if is_off:
                off_screen_count += 1
                current_streak += 1
                longest_continuous_off = max(longest_continuous_off, current_streak)
            else:
                current_streak = 0

            if "Left" in label:
                breakdown["Left"] += 1
            elif "Right" in label:
                breakdown["Right"] += 1
            elif "Down" in label:
                breakdown["Down"] += 1
            elif "Up" in label:
                breakdown["Up"] += 1
            else:
                breakdown["Center"] += 1

        off_screen_pct = (off_screen_count / total_samples) * 100.0
        longest_streak_sec = longest_continuous_off * sample_interval_seconds

        is_flagged = (off_screen_pct > 25.0) or (longest_streak_sec >= 15.0)

        return {
            "total_samples": total_samples,
            "off_screen_seconds": round(off_screen_count * sample_interval_seconds, 1),
            "off_screen_percentage": round(off_screen_pct, 1),
            "longest_continuous_away_seconds": round(longest_streak_sec, 1),
            "gaze_breakdown": breakdown,
            "is_flagged_for_review": is_flagged,
            "warning": "Excessive off-screen gaze duration detected" if is_flagged else "Gaze within normal bounds"
        }
