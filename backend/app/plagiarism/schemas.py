"""
ExamHub Plagiarism & Collusion Detection - Schemas
Defines request and response structures for text fingerprinting,
cross-candidate similarity analysis, and source attribution.
"""

from typing import List, Dict, Optional, Tuple
from pydantic import BaseModel, Field


class PlagiarismScanRequest(BaseModel):
    exam_id: str
    question_id: str
    similarity_threshold: float = Field(default=0.40, ge=0.05, le=1.0)
    k_gram_length: int = Field(default=25, ge=5, le=100)
    window_size: int = Field(default=15, ge=3, le=50)


class PlagiarismMatchSpan(BaseModel):
    start_char_candidate: int
    end_char_candidate: int
    start_char_matched: int
    end_char_matched: int
    matched_text_sample: str


class PlagiarismMatchDetail(BaseModel):
    matched_candidate_id: str
    matched_submission_id: str
    similarity_score: float
    matched_spans: List[PlagiarismMatchSpan] = Field(default_factory=list)


class CandidateCollusionRecord(BaseModel):
    candidate_id_a: str
    candidate_id_b: str
    similarity_percentage: float
    shared_fingerprints_count: int
    total_fingerprints_a: int
    total_fingerprints_b: int
    temporal_proximity_seconds: Optional[float] = None
    ip_match: bool = False
    verdict: str


class PlagiarismReport(BaseModel):
    report_id: str
    exam_id: str
    question_id: str
    analyzed_submissions_count: int
    flagged_pairs_count: int
    collusion_records: List[CandidateCollusionRecord] = Field(default_factory=list)
    scanned_at: str
