"""
ExamHub Compliance & Audit Integrity - Schemas
Supports GDPR/FERPA Data Subject Access Requests (DSAR), PII pseudonymization, and Merkle audit anchors.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum


class DSARType(str, Enum):
    EXPORT = "export"
    ERASURE = "erasure"
    RECTIFICATION = "rectification"


class MerkleAuditProof(BaseModel):
    record_id: str
    record_hash: str
    merkle_root: str
    proof_path: List[Dict[str, str]]  # list of {"position": "left"/"right", "hash": "..."}
    is_verified: bool


class CandidatePIIExport(BaseModel):
    candidate_id: str
    export_timestamp: str
    personal_data: Dict[str, Any]
    exam_history: List[Dict[str, Any]]
    proctoring_records_count: int
    data_retention_policy: str = "FERPA 5-Year Academic Record Retention"


class ComplianceVerificationResult(BaseModel):
    compliance_framework: str = "FERPA / GDPR"
    is_compliant: bool = True
    active_audit_records_count: int
    merkle_root_anchor: str
    tamper_detected: bool = False
    audit_notes: List[str] = Field(default_factory=list)
