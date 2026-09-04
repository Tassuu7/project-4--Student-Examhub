"""
ExamHub Pose & Gaze Telemetry Tracker
Evaluates candidate head orientation angles (yaw, pitch, roll) and gaze attention.
"""

from typing import Tuple, Optional
from backend.app.biometrics.schemas import PoseTelemetryEvent


class PoseTracker:
    """
    Validates candidate attentiveness and flags potential side-glancing,
    second screen usage, or leaving the examination frame.
    """

    YAW_THRESHOLD: float = 30.0    # degrees left/right
    PITCH_THRESHOLD: float = 25.0  # degrees up/down
    ROLL_THRESHOLD: float = 20.0   # degrees tilt

    @classmethod
    def evaluate_pose(cls, event: PoseTelemetryEvent) -> Tuple[bool, Optional[str]]:
        """
        Returns (is_suspicious, anomaly_reason)
        """
        if not event.face_detected:
            return True, "No face detected in webcam frame"

        if abs(event.yaw_degrees) > cls.YAW_THRESHOLD:
            direction = "right" if event.yaw_degrees > 0 else "left"
            return True, f"Excessive head yaw ({event.yaw_degrees:.1f}°) turned {direction} (possible second screen/notes)"

        if abs(event.pitch_degrees) > cls.PITCH_THRESHOLD:
            direction = "down" if event.pitch_degrees > 0 else "up"
            return True, f"Excessive head pitch ({event.pitch_degrees:.1f}°) looking {direction} (possible phone/notes on desk)"

        if abs(event.roll_degrees) > cls.ROLL_THRESHOLD:
            return True, f"Excessive head roll tilt ({event.roll_degrees:.1f}°)"

        if event.eyes_closed:
            return True, "Prolonged eyes closed / averted"

        return False, None
