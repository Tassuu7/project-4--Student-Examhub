"""
ExamHub - Digital Certificate API Router
Exposes endpoints for issuing certificates, public verification,
student transcript retrieval, and HTML certificate rendering.
"""

from fastapi import APIRouter, Depends, Response
from fastapi.responses import HTMLResponse
from typing import Dict, Any

from backend.app.auth.dependencies import get_current_user
from backend.app.auth.rbac import require_role
from backend.app.certificates.schemas import (
    CertificateIssueRequest, CertificateVerificationResponse,
    CertificateRecord, StudentCertificatesListResponse, CertificateRevocationRequest
)
from backend.app.certificates.service import CertificateService
from backend.app.certificates.verification import CertificateVerifier
from backend.app.certificates.generator import CertificateGenerator
from backend.app.certificates.repository import CertificateRepository
from backend.app.core.exceptions import NotFoundException

router = APIRouter(prefix="/certificates", tags=["Certificates & Credentials"])

@router.post("/issue", response_model=CertificateRecord)
def issue_certificate(
    payload: CertificateIssueRequest,
    current_user: Dict[str, Any] = Depends(require_role(["admin", "teacher"]))
):
    """Issue a verified digital certificate for a completed and passed exam attempt."""
    return CertificateService.issue_certificate_for_attempt(
        attempt_id=payload.attempt_id,
        custom_title=payload.custom_title,
        expiry_months=payload.expiry_months or 24,
        student_id=payload.student_id,
        exam_id=payload.exam_id
    )

@router.get("/verify/{certificate_code}", response_model=CertificateVerificationResponse)
def verify_certificate(certificate_code: str):
    """Public endpoint: Verify the cryptographic authenticity and validity of a certificate."""
    return CertificateVerifier.verify_by_code(certificate_code)

@router.get("", response_model=StudentCertificatesListResponse)
def list_all_certificates(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Retrieve all issued academic certificates across the institution."""
    return CertificateService.list_all_certificates()

@router.get("/student/{student_id}", response_model=StudentCertificatesListResponse)
def get_student_certificates(
    student_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Retrieve all issued academic certificates and credentials for a student."""
    return CertificateService.get_student_certificates(student_id)

@router.get("/render/{certificate_code}", response_class=HTMLResponse)
def render_certificate_html(certificate_code: str):
    """Renders the printable, official visual certificate layout in HTML format."""
    record = CertificateRepository.get_by_code(certificate_code)
    if not record:
        raise NotFoundException(f"Certificate '{certificate_code}' not found.")
    html_content = CertificateGenerator.render_html_certificate(record)
    return HTMLResponse(content=html_content, status_code=200)

@router.post("/revoke/{certificate_code}")
def revoke_certificate(
    certificate_code: str,
    payload: CertificateRevocationRequest,
    current_user: Dict[str, Any] = Depends(require_role(["admin", "teacher"]))
):
    """Admin and Teacher endpoint: Revoke an issued certificate with justification."""
    success = CertificateRepository.revoke_certificate(certificate_code, payload.reason)
    if not success:
        raise NotFoundException(f"Certificate '{certificate_code}' not found.")
    return {"status": "revoked", "certificate_code": certificate_code}
