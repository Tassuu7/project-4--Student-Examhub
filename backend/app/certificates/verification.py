"""
ExamHub - Public Certificate Verification Subsystem
Allows third-party verification of student certificates using serial codes and cryptographic signatures.
"""

from typing import Dict, Any, Optional
from backend.app.certificates.repository import CertificateRepository
from backend.app.certificates.crypto_signer import CryptoSigner
from backend.app.certificates.schemas import CertificateVerificationResponse

class CertificateVerifier:
    """Verifies credential integrity, expiration, and cryptographic authenticity."""

    @staticmethod
    def verify_by_code(code: str) -> CertificateVerificationResponse:
        record = CertificateRepository.get_by_code(code.strip().upper())
        if not record:
            return CertificateVerificationResponse(
                is_valid=False,
                certificate_code=code,
                student_name="Unknown",
                roll_number="N/A",
                exam_name="Unknown",
                subject_code="N/A",
                subject_name="Unknown",
                percentage=0.0,
                grade="N/A",
                issue_date="",
                expiry_date=None,
                issuer="ExamHub Academic Authority",
                verification_hash="",
                status="not_found",
                tamper_status="invalid_signature"
            )

        sign_payload = {
            "student_id": record["student_id"],
            "exam_id": record["exam_id"],
            "attempt_id": record["attempt_id"],
            "percentage": float(record["percentage"]),
            "grade": record["grade"],
            "issue_date": record["issue_date"]
        }
        signature_matches = CryptoSigner.verify_signature(sign_payload, record["verification_hash"])
        is_active = record["status"] == "active"
        is_valid = is_active and signature_matches

        return CertificateVerificationResponse(
            is_valid=is_valid,
            certificate_code=record["certificate_code"],
            student_name=record["student_name"],
            roll_number=record["roll_number"],
            exam_name=record["exam_name"],
            subject_code=record["subject_code"],
            subject_name=record["subject_name"],
            percentage=float(record["percentage"]),
            grade=record["grade"],
            issue_date=record["issue_date"],
            expiry_date=record.get("expiry_date"),
            issuer="ExamHub Academic Authority",
            verification_hash=record["verification_hash"],
            status=record["status"],
            tamper_status="intact" if signature_matches else "invalid_signature"
        )
