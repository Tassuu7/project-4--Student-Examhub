"""
ExamHub - Cryptographic Certificate Signing and Tamper Proofing
Generates HMAC-SHA256 signatures, verifiable digital checksums,
and deterministic verification codes for certificates.
"""

import hmac
import hashlib
import uuid
from typing import Dict, Any, Tuple
from backend.app.core.config import SECRET_KEY

class CryptoSigner:
    """Cryptographic signing and verification utilities for digital credentials."""

    @staticmethod
    def generate_certificate_code(exam_id: str, student_id: str) -> str:
        """Generates a human-readable verification serial: e.g., EXAM-A7B2-9F1C-2026"""
        raw = f"{exam_id}:{student_id}:{uuid.uuid4().hex[:8]}"
        digest = hashlib.sha256(raw.encode('utf-8')).hexdigest().upper()
        return f"EXAM-{digest[:4]}-{digest[4:8]}-{digest[8:12]}"

    @staticmethod
    def compute_verification_hash(payload: Dict[str, Any]) -> str:
        """Computes HMAC-SHA256 signature over standardized payload string."""
        canonical_str = (
            f"student={payload.get('student_id')}|"
            f"exam={payload.get('exam_id')}|"
            f"attempt={payload.get('attempt_id')}|"
            f"score={payload.get('percentage')}|"
            f"grade={payload.get('grade')}|"
            f"issue_date={payload.get('issue_date')}"
        )
        signature = hmac.new(
            SECRET_KEY.encode('utf-8'),
            canonical_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    @staticmethod
    def verify_signature(payload: Dict[str, Any], expected_hash: str) -> bool:
        computed = CryptoSigner.compute_verification_hash(payload)
        return hmac.compare_digest(computed, expected_hash)
