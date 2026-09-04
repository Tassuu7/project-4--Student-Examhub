"""
ExamHub - Digital Certificate & Academic Credential Schemas
Defines data structures for issuance, cryptographic verification,
revocation, and student transcript badges.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class CertificateIssueRequest(BaseModel):
    attempt_id: Optional[str] = None
    student_id: Optional[str] = None
    exam_id: Optional[str] = None
    custom_title: Optional[str] = None
    expiry_months: Optional[int] = Field(default=24, ge=1, le=120)

class CertificateVerificationResponse(BaseModel):
    is_valid: bool
    certificate_code: str
    student_name: str
    roll_number: str
    exam_name: str
    subject_code: str
    subject_name: str
    percentage: float
    grade: str
    issue_date: str
    expiry_date: Optional[str] = None
    issuer: str
    verification_hash: str
    status: str  # active, expired, revoked
    tamper_status: str  # intact, invalid_signature

class CertificateRecord(BaseModel):
    id: str
    certificate_code: str
    attempt_id: str
    exam_id: str
    student_id: str
    student_name: str
    roll_number: str
    exam_name: str
    subject_code: str
    subject_name: str
    percentage: float
    grade: str
    issue_date: str
    expiry_date: Optional[str] = None
    verification_hash: str
    status: str
    download_url: str

class CertificateRevocationRequest(BaseModel):
    reason: str
    revoked_by: Optional[str] = None

class StudentCertificatesListResponse(BaseModel):
    student_id: str
    total_certificates: int
    items: List[CertificateRecord]
