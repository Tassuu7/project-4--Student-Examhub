"""
ExamHub Secure Lockdown Enforcer
Evaluates client-side lockdown heartbeats, multi-display violations, and blacklisted software.
"""

from typing import Tuple, Optional
from backend.app.exam_delivery.schemas import (
    LockdownHeartbeatRequest,
    LockdownStatusResponse,
)


class LockdownEnforcer:
    """
    Enforces secure testing browser lockdown policies.
    """

    MAX_TOLERATED_VIOLATIONS: int = 3

    @classmethod
    def evaluate_heartbeat(
        cls,
        req: LockdownHeartbeatRequest,
        current_violations: int = 0
    ) -> Tuple[bool, bool, Optional[str], int]:
        """
        Returns: (allowed_to_continue, warning_issued, warning_message, new_violation_count)
        """
        violations = []

        if not req.is_fullscreen:
            violations.append("Candidate exited fullscreen lockdown mode.")

        if not req.window_focused:
            violations.append("Candidate switched application window / focus lost.")

        if req.screen_count > 1:
            violations.append(f"Multiple display monitors detected ({req.screen_count} connected screens).")

        if req.detected_blacklisted_apps:
            apps_str = ", ".join(req.detected_blacklisted_apps)
            violations.append(f"Prohibited software processes detected: {apps_str}")

        if not violations:
            return True, False, None, current_violations

        new_count = current_violations + len(violations)
        warning_msg = " • ".join(violations)

        if new_count >= cls.MAX_TOLERATED_VIOLATIONS:
            return False, True, f"EXAM TERMINATED: Repeated security violations ({new_count}): {warning_msg}", new_count

        return True, True, f"SECURITY WARNING ({new_count}/{cls.MAX_TOLERATED_VIOLATIONS}): {warning_msg}", new_count
