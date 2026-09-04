"""
ExamHub - Keystroke Dynamics & Typing Biometrics Analyzer
Analyzes dwell time, flight time, and detects robotic paste or macro injection events.
"""

from typing import List, Dict, Any, Tuple
import math

class KeystrokeBiometricsAnalyzer:
    """Evaluates candidate typing rhythm and identifies automated text injection."""

    @staticmethod
    def audit_keystroke_stream(
        keystrokes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        keystrokes: List of dicts with:
        {'key': 'a', 'down_time_ms': 1000, 'up_time_ms': 1080}
        """
        n = len(keystrokes)
        if n < 2:
            return {"total_keystrokes": n, "status": "Insufficient typing samples"}

        dwell_times = []
        flight_times = []
        macro_bursts_count = 0

        for i in range(n):
            down = float(keystrokes[i].get("down_time_ms", 0.0))
            up = float(keystrokes[i].get("up_time_ms", down + 80.0))
            dwell = max(0.0, up - down)
            dwell_times.append(dwell)

            if i > 0:
                prev_up = float(keystrokes[i - 1].get("up_time_ms", down))
                flight = down - prev_up
                flight_times.append(flight)

                # Flag robotic macro burst: flight time < 5ms for multiple consecutive keys
                if flight < 5.0 and dwell < 15.0:
                    macro_bursts_count += 1

        mean_dwell = sum(dwell_times) / n
        mean_flight = sum(flight_times) / len(flight_times) if flight_times else 0.0

        # Variance of flight time
        var_flight = sum((x - mean_flight) ** 2 for x in flight_times) / len(flight_times) if flight_times else 0.0
        std_flight = math.sqrt(var_flight)

        is_bot_like = (macro_bursts_count > 5) or (std_flight < 2.0 and n > 20)

        return {
            "total_keystrokes": n,
            "average_dwell_time_ms": round(mean_dwell, 1),
            "average_flight_time_ms": round(mean_flight, 1),
            "flight_time_std_dev": round(std_flight, 1),
            "macro_burst_injections": macro_bursts_count,
            "is_human_rhythm": not is_bot_like,
            "integrity_flag": "Suspicious Automated Typing Detected" if is_bot_like else "Natural Human Cadence"
        }
