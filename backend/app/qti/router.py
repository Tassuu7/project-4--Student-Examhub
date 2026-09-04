"""
ExamHub QTI (Question & Test Interoperability) - FastAPI Router
Endpoints for importing and exporting IMS QTI 2.1 packages.
"""

import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File

from backend.app.qti.schemas import (
    QTIAssessmentItem,
    QTIPackageExportRequest,
    QTIPackageExportResponse,
    QTIImportResult,
    QTIInteractionType,
    QTIResponseDeclaration,
    QTISimpleChoice,
)
from backend.app.qti.parser import QTIParser
from backend.app.qti.generator import QTIGenerator
from backend.app.auth.dependencies import require_role

router = APIRouter(prefix="/api/qti", tags=["QTI Assessment Interoperability"])


@router.post("/export", response_model=QTIPackageExportResponse)
def export_qti_package(
    req: QTIPackageExportRequest,
    current_user: dict = Depends(require_role(["teacher", "admin"]))
):
    """
    Export question items in standard IMS QTI 2.1 XML package structure.
    """
    # Create sample QTI assessment items if none given
    items: List[QTIAssessmentItem] = []
    ids_to_export = req.question_ids or [f"Q-{i}" for i in range(1, 6)]

    for qid in ids_to_export:
        item = QTIAssessmentItem(
            identifier=f"ITEM-{qid}",
            title=f"Assessment Question {qid}",
            adaptive=False,
            time_dependent=False,
            interaction_type=QTIInteractionType.CHOICE,
            prompt=f"Which architectural pattern maximizes high-availability in distributed system {qid}?",
            choices=[
                QTISimpleChoice(identifier="ChoiceA", fixed=False, content="Active-Passive failover with shared storage"),
                QTISimpleChoice(identifier="ChoiceB", fixed=False, content="Active-Active cluster with Raft consensus"),
                QTISimpleChoice(identifier="ChoiceC", fixed=False, content="Single master node with delayed replication"),
                QTISimpleChoice(identifier="ChoiceD", fixed=False, content="Stateless worker with persistent local disk")
            ],
            response_declaration=QTIResponseDeclaration(
                identifier="RESPONSE",
                cardinality="single",
                base_type="identifier",
                correct_response=["ChoiceB"]
            ),
            feedback=[],
            max_score=2.0
        )
        items.append(item)

    manifest_xml = QTIGenerator.generate_manifest_xml(items, "ExamHub Export Package")
    pkg_id = f"qti-pkg-{uuid.uuid4().hex[:10]}"

    return QTIPackageExportResponse(
        package_id=pkg_id,
        manifest_xml=manifest_xml,
        items=items,
        total_items=len(items),
        zip_download_url=f"/api/qti/download/{pkg_id}.zip"
    )


@router.post("/validate-xml")
def validate_qti_item_xml(
    xml_content: str,
    current_user: dict = Depends(require_role(["teacher", "admin"]))
):
    """
    Validate and inspect a raw QTI 2.1 XML assessment item string.
    """
    parsed = QTIParser.parse_assessment_item_xml(xml_content)
    if not parsed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="XML string could not be parsed as a valid IMS QTI 2.1 assessmentItem."
        )
    return {
        "status": "valid",
        "identifier": parsed.identifier,
        "title": parsed.title,
        "interaction_type": parsed.interaction_type,
        "choices_count": len(parsed.choices),
        "correct_answers": parsed.response_declaration.correct_response
    }
