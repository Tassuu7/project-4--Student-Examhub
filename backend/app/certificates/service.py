"""
ExamHub - Certificate Issuance & Lifecycle Service
Validates passing criteria, generates cryptographically signed credentials,
and manages student transcript collections.
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

from backend.app.certificates.repository import CertificateRepository
from backend.app.certificates.crypto_signer import CryptoSigner
from backend.app.certificates.schemas import (
    CertificateRecord, CertificateVerificationResponse, StudentCertificatesListResponse
)
from backend.app.database.connection import get_db_connection
from backend.app.core.exceptions import ValidationException, NotFoundException

class CertificateService:
    """Business operations for digital certificate lifecycle."""

    @staticmethod
    def issue_certificate_for_attempt(attempt_id: str, custom_title: Optional[str] = None, expiry_months: int = 24) -> CertificateRecord:
        # Check if already issued
        existing = CertificateRepository.get_by_attempt_id(attempt_id)
        if existing:
            return CertificateService._map_record(existing)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id as result_id, r.exam_id, r.student_id, r.pass_fail,
                   r.percentage, r.grade, r.total_marks, r.obtained_marks,
                   e.name as exam_name, s.code as subject_code, s.name as subject_name,
                   u.full_name as student_name, st.student_id_code as roll_number
            FROM results r
            JOIN exams e ON r.exam_id = e.id
            JOIN subjects s ON e.subject_id = s.id
            JOIN students st ON r.student_id = st.id
            JOIN users u ON st.user_id = u.id
            WHERE r.attempt_id = ?
        """, (attempt_id,))
        res_row = cursor.fetchone()

        if not res_row:
            raise NotFoundException("Evaluation result not found for this attempt.")

        data = dict(res_row)
        if data["pass_fail"] != "PASS":
            raise ValidationException("Certificates can only be issued for examinations with PASS outcome.")

        cert_id = str(uuid.uuid4())
        cert_code = CryptoSigner.generate_certificate_code(data["exam_id"], data["student_id"])
        now = datetime.utcnow()
        issue_date_str = now.isoformat()
        expiry_date_str = (now + timedelta(days=expiry_months * 30)).isoformat() if expiry_months else None

        sign_payload = {
            "student_id": data["student_id"],
            "exam_id": data["exam_id"],
            "attempt_id": attempt_id,
            "percentage": data["percentage"],
            "grade": data["grade"],
            "issue_date": issue_date_str
        }
        verif_hash = CryptoSigner.compute_verification_hash(sign_payload)

        title = custom_title or f"Certificate of Competence in {data['exam_name']}"

        CertificateRepository.create_certificate({
            "id": cert_id,
            "certificate_code": cert_code,
            "attempt_id": attempt_id,
            "exam_id": data["exam_id"],
            "student_id": data["student_id"],
            "title": title,
            "issue_date": issue_date_str,
            "expiry_date": expiry_date_str,
            "verification_hash": verif_hash,
            "status": "active",
            "created_at": issue_date_str
        })

        new_record = CertificateRepository.get_by_code(cert_code)
        return CertificateService._map_record(new_record)

    @staticmethod
    def get_student_certificates(student_id: str) -> StudentCertificatesListResponse:
        records = CertificateRepository.get_student_certificates(student_id)
        items = [CertificateService._map_record(r) for r in records]
        return StudentCertificatesListResponse(
            student_id=student_id,
            total_certificates=len(items),
            items=items
        )

    @staticmethod
    def list_all_certificates() -> StudentCertificatesListResponse:
        records = CertificateRepository.list_all_certificates()
        items = [CertificateService._map_record(r) for r in records]
        return StudentCertificatesListResponse(
            student_id="all",
            total_certificates=len(items),
            items=items
        )

    @staticmethod
    def _map_record(row: Dict[str, Any]) -> CertificateRecord:
        return CertificateRecord(
            id=row["id"],
            certificate_code=row["certificate_code"],
            attempt_id=row["attempt_id"],
            exam_id=row["exam_id"],
            student_id=row["student_id"],
            student_name=row["student_name"],
            roll_number=row["roll_number"],
            exam_name=row["exam_name"],
            subject_code=row["subject_code"],
            subject_name=row["subject_name"],
            percentage=float(row["percentage"]),
            grade=row["grade"],
            issue_date=row["issue_date"],
            expiry_date=row.get("expiry_date"),
            verification_hash=row["verification_hash"],
            status=row["status"],
            download_url=f"/api/v1/certificates/render/{row['certificate_code']}"
        )
