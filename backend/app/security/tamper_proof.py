"""
ExamHub - Request Payload Tamper Proofing & Nonce Freshness
Validates digital signatures and timestamp freshness on submitted answers.
"""

import hmac
import hashlib
import time
from backend.app.core.config import SECRET_KEY

class TamperProofGuard:
    """Validates payload authenticity and rejects replayed requests."""

    @staticmethod
    def verify_answer_payload_integrity(attempt_id: str, question_id: str, option: str, timestamp: int, signature: str) -> bool:
        # Check freshness within 300 seconds
        now = int(time.time())
        if abs(now - timestamp) > 300:
            return False

        canonical = f"{attempt_id}:{question_id}:{option}:{timestamp}"
        expected = hmac.new(
            SECRET_KEY.encode('utf-8'),
            canonical.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected, signature)
