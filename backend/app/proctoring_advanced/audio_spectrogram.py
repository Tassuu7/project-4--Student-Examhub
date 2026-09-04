"""
ExamHub - Audio Telemetry & Voice Activity Detection (VAD) Analyzer
Monitors candidate microphone decibel energy, background speech events,
and whispering heuristics.
"""

from typing import List, Dict, Any, Tuple
import math

class AudioTelemetryAnalyzer:
    """Processes streaming audio amplitude and decibel metrics for exam security."""

    SPEECH_DB_THRESHOLD = 45.0      # dB threshold indicative of speech
    LOUD_NOISE_THRESHOLD = 70.0     # dB threshold for loud room disruptions

    @staticmethod
    def audit_audio_frames(decibel_frames: List[float], sample_rate_hz: float = 2.0) -> Dict[str, Any]:
        """
        decibel_frames: List of audio dB levels recorded (e.g., [25.0, 32.1, 58.4, 22.0, ...]).
        """
        total_frames = len(decibel_frames)
        if total_frames == 0:
            return {"total_duration_sec": 0, "speech_detected": False}

        speech_frames = [db for db in decibel_frames if db >= AudioTelemetryAnalyzer.SPEECH_DB_THRESHOLD]
        loud_frames = [db for db in decibel_frames if db >= AudioTelemetryAnalyzer.LOUD_NOISE_THRESHOLD]

        mean_db = sum(decibel_frames) / total_frames
        speech_pct = (len(speech_frames) / total_frames) * 100.0

        # Burst detection: continuous speech >= 3 seconds
        frame_interval_sec = 1.0 / sample_rate_hz
        max_speech_burst = 0
        cur_burst = 0
        for db in decibel_frames:
            if db >= AudioTelemetryAnalyzer.SPEECH_DB_THRESHOLD:
                cur_burst += 1
                max_speech_burst = max(max_speech_burst, cur_burst)
            else:
                cur_burst = 0

        max_burst_sec = max_speech_burst * frame_interval_sec

        is_suspicious = (speech_pct > 15.0) or (max_burst_sec >= 4.0)

        return {
            "total_frames_sampled": total_frames,
            "ambient_baseline_db": round(mean_db, 1),
            "speech_events_count": len(speech_frames),
            "speech_duration_seconds": round(len(speech_frames) * frame_interval_sec, 1),
            "speech_percentage": round(speech_pct, 1),
            "longest_continuous_speech_seconds": round(max_burst_sec, 1),
            "loud_audio_spikes_count": len(loud_frames),
            "is_flagged_for_voice": is_suspicious,
            "security_status": "Flagged - Voice Conversation Detected" if is_suspicious else "Quiet Testing Room"
        }
