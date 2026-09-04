"""
ExamHub QTI (Question & Test Interoperability) - Schemas
Supports IMS Global QTI 2.1 and QTI 3.0 specifications for interoperable assessment items.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum


class QTIInteractionType(str, Enum):
    CHOICE = "choiceInteraction"
    TEXT_ENTRY = "textEntryInteraction"
    EXTENDED_TEXT = "extendedTextInteraction"
    ORDER = "orderInteraction"
    MATCH = "matchInteraction"
    HOTSPOT = "hotspotInteraction"


class QTIResponseDeclaration(BaseModel):
    identifier: str
    cardinality: str = "single"  # single, multiple, ordered
    base_type: str = "identifier"  # identifier, string, float, integer
    correct_response: List[str] = Field(default_factory=list)
    mapping: Optional[Dict[str, float]] = None


class QTISimpleChoice(BaseModel):
    identifier: str
    fixed: bool = False
    content: str


class QTIModalFeedback(BaseModel):
    identifier: str
    outcome_identifier: str = "FEEDBACK"
    show_hide: str = "show"
    title: str = ""
    content: str = ""


class QTIAssessmentItem(BaseModel):
    identifier: str
    title: str
    adaptive: bool = False
    time_dependent: bool = False
    interaction_type: QTIInteractionType
    prompt: str
    choices: List[QTISimpleChoice] = Field(default_factory=list)
    response_declaration: QTIResponseDeclaration
    feedback: List[QTIModalFeedback] = Field(default_factory=list)
    max_score: float = 1.0


class QTIManifestMetadata(BaseModel):
    schema_version: str = "2.1"
    package_title: str
    description: Optional[str] = None
    created_at: str
    items_count: int


class QTIPackageExportRequest(BaseModel):
    exam_id: Optional[str] = None
    question_ids: List[str] = Field(default_factory=list)
    qti_version: str = Field(default="2.1")
    include_feedback: bool = Field(default=True)


class QTIPackageExportResponse(BaseModel):
    package_id: str
    manifest_xml: str
    items: List[QTIAssessmentItem]
    total_items: int
    zip_download_url: Optional[str] = None


class QTIImportResult(BaseModel):
    imported_count: int
    failed_count: int
    items_imported: List[str]
    validation_warnings: List[str] = Field(default_factory=list)
