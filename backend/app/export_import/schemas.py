"""
ExamHub - Data Exchange, Export, and Question Ingestion Schemas
Data contracts for CSV exports, JSON backups, Aiken/GIFT parsers, and batch dumps.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class AikenImportRequest(BaseModel):
    subject_id: str
    aiken_text: str
    default_difficulty: Optional[str] = "Medium"
    default_marks: Optional[float] = 1.0
    topic: Optional[str] = None

class AikenImportResult(BaseModel):
    total_parsed: int
    successful_imports: int
    failed_count: int
    errors: List[str]
    imported_question_ids: List[str]

class ExamArchiveExportResponse(BaseModel):
    export_id: str
    exam_id: str
    format: str  # csv, json, qti
    file_size_bytes: int
    generated_at: str
    download_url: str

class BackupSnapshotSummary(BaseModel):
    snapshot_id: str
    created_at: str
    total_tables: int
    total_records: int
    integrity_checksum: str
