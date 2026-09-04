"""
ExamHub - Secure Browser Lockdown Policy Enforcement
Generates lockdown configurations, evaluates full-screen escape violations,
and verifies clipboard security constraints.
"""

from typing import Dict, Any, List

class BrowserLockdownPolicy:
    """Configures and validates secure candidate client environment constraints."""

    DEFAULT_POLICY = {
        "require_fullscreen": True,
        "block_clipboard_copy_paste": True,
        "block_right_click": True,
        "block_devtools_shortcuts": True,
        "warn_on_window_blur": True,
        "max_blur_events_allowed": 3,
        "max_tab_switches_allowed": 2,
        "auto_terminate_on_breach": False
    }

    @staticmethod
    def get_enforcement_manifest() -> Dict[str, Any]:
        return {
            "policy_version": "2.4-lockdown",
            "enforced_rules": BrowserLockdownPolicy.DEFAULT_POLICY,
            "blocked_key_combinations": [
                "Ctrl+C", "Ctrl+V", "Ctrl+X", "Ctrl+U", "Ctrl+Shift+I",
                "F12", "Alt+Tab", "Meta+Tab", "Ctrl+W", "Ctrl+T"
            ],
            "allowed_origins": ["http://localhost:3000", "http://127.0.0.1:3000"]
        }

    @staticmethod
    def validate_session_compliance(blur_count: int, tab_switch_count: int, devtools_opened: bool) -> Dict[str, Any]:
        breaches = []
        if devtools_opened:
            breaches.append("Critical: Developer Tools Inspection opened.")

        if tab_switch_count > BrowserLockdownPolicy.DEFAULT_POLICY["max_tab_switches_allowed"]:
            breaches.append(f"Exceeded tab switch tolerance ({tab_switch_count} > {BrowserLockdownPolicy.DEFAULT_POLICY['max_tab_switches_allowed']}).")

        if blur_count > BrowserLockdownPolicy.DEFAULT_POLICY["max_blur_events_allowed"]:
            breaches.append(f"Exceeded window blur limit ({blur_count} > {BrowserLockdownPolicy.DEFAULT_POLICY['max_blur_events_allowed']}).")

        is_compliant = (len(breaches) == 0)

        return {
            "is_compliant": is_compliant,
            "breaches": breaches,
            "action_required": "None" if is_compliant else "Proctor Manual Review Mandated"
        }
