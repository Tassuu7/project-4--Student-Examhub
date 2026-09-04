"""
ExamHub Keystroke Dynamics Engine
Analyzes typing cadence, dwell durations, and flight transitions to verify candidate identity.
"""

import math
from typing import List, Dict, Tuple
from backend.app.biometrics.schemas import KeystrokeEvent, TypingProfile


class KeystrokeDynamicsEngine:
    """
    Biometric behavioral analysis of typing patterns for continuous candidate authentication.
    """

    @classmethod
    def extract_dwell_times(cls, events: List[KeystrokeEvent]) -> List[float]:
        """
        Dwell Time (Hold Time): Duration key remained depressed (up_time - down_time).
        """
        dwells = []
        for ev in events:
            duration = ev.up_time_ms - ev.down_time_ms
            if 10.0 <= duration <= 1000.0:  # Reasonable typing bound
                dwells.append(duration)
        return dwells

    @classmethod
    def extract_flight_times(cls, events: List[KeystrokeEvent]) -> List[float]:
        """
        Flight Time: Duration between releasing key i and depressing key i+1.
        """
        flights = []
        for i in range(len(events) - 1):
            flight = events[i + 1].down_time_ms - events[i].up_time_ms
            if -200.0 <= flight <= 2000.0:  # Allow negative for rollover typing
                flights.append(flight)
        return flights

    @classmethod
    def extract_digraph_transitions(cls, events: List[KeystrokeEvent]) -> Dict[str, float]:
        """
        Calculates average transition duration (key1 down to key2 down) for character pairs.
        """
        digraph_times: Dict[str, List[float]] = {}
        for i in range(len(events) - 1):
            k1 = events[i].key.lower()
            k2 = events[i + 1].key.lower()
            if len(k1) == 1 and len(k2) == 1 and k1.isalnum() and k2.isalnum():
                pair = f"{k1}{k2}"
                time_diff = events[i + 1].down_time_ms - events[i].down_time_ms
                if 20.0 <= time_diff <= 1500.0:
                    if pair not in digraph_times:
                        digraph_times[pair] = []
                    digraph_times[pair].append(time_diff)

        return {pair: (sum(times) / len(times)) for pair, times in digraph_times.items()}

    @classmethod
    def build_profile(cls, candidate_id: str, events: List[KeystrokeEvent], sample_text: str = "") -> TypingProfile:
        """
        Build enrolled baseline typing signature from a reference session.
        """
        dwells = cls.extract_dwell_times(events)
        flights = cls.extract_flight_times(events)
        digraphs = cls.extract_digraph_transitions(events)

        mean_dwell = sum(dwells) / len(dwells) if dwells else 100.0
        mean_flight = sum(flights) / len(flights) if flights else 120.0

        # Calculate internal consistency (1.0 - CV)
        if len(dwells) > 1:
            var = sum((d - mean_dwell) ** 2 for d in dwells) / len(dwells)
            sd = math.sqrt(var)
            cv = sd / mean_dwell if mean_dwell > 0 else 1.0
            consistency = max(0.1, min(1.0, 1.0 - cv * 0.5))
        else:
            consistency = 0.8

        return TypingProfile(
            candidate_id=candidate_id,
            sample_text=sample_text,
            mean_dwell_ms=round(mean_dwell, 2),
            mean_flight_ms=round(mean_flight, 2),
            digraph_profiles=digraphs,
            consistency_score=round(consistency, 2)
        )

    @classmethod
    def compute_similarity(cls, enrolled: TypingProfile, session_events: List[KeystrokeEvent]) -> float:
        """
        Compute similarity score (0.0 to 1.0) between session typing telemetry and enrolled profile.
        """
        sess_digraphs = cls.extract_digraph_transitions(session_events)
        shared_keys = set(enrolled.digraph_profiles.keys()).intersection(set(sess_digraphs.keys()))

        if len(shared_keys) < 3:
            # Fallback to mean dwell and flight comparison
            dwells = cls.extract_dwell_times(session_events)
            flights = cls.extract_flight_times(session_events)
            cur_dwell = sum(dwells) / len(dwells) if dwells else 100.0
            cur_flight = sum(flights) / len(flights) if flights else 120.0

            dwell_diff = abs(cur_dwell - enrolled.mean_dwell_ms) / (enrolled.mean_dwell_ms + 1e-5)
            flight_diff = abs(cur_flight - enrolled.mean_flight_ms) / (enrolled.mean_flight_ms + 1e-5)
            avg_diff = (dwell_diff + flight_diff) / 2.0
            sim = max(0.0, 1.0 - avg_diff)
            return round(sim, 3)

        # Vector cosine similarity on shared digraph latencies
        vec_enrolled = [enrolled.digraph_profiles[k] for k in shared_keys]
        vec_session = [sess_digraphs[k] for k in shared_keys]

        dot_product = sum(a * b for a, b in zip(vec_enrolled, vec_session))
        norm_a = math.sqrt(sum(a * a for a in vec_enrolled))
        norm_b = math.sqrt(sum(b * b for b in vec_session))

        if norm_a == 0.0 or norm_b == 0.0:
            return 0.5

        cosine = dot_product / (norm_a * norm_b)
        # Normalize relative differences
        rel_diffs = [abs(a - b) / max(a, b) for a, b in zip(vec_enrolled, vec_session)]
        mean_rel_diff = sum(rel_diffs) / len(rel_diffs)

        score = cosine * (1.0 - min(0.5, mean_rel_diff))
        return round(max(0.0, min(1.0, score)), 3)
