"""
ExamHub Advanced Question Engines - FastAPI Router
Endpoints for specialized question evaluation: numerical, cloze, ordering, and hotspot items.
"""

from fastapi import APIRouter, Depends
from backend.app.question_engines.schemas import (
    NumericalGradingRequest,
    NumericalGradingResponse,
    ClozeGradingRequest,
    ClozeGradingResponse,
    OrderingGradingRequest,
    OrderingGradingResponse,
    HotspotGradingRequest,
    HotspotGradingResponse,
)
from backend.app.question_engines.numerical_engine import NumericalEngine
from backend.app.question_engines.cloze_engine import ClozeEngine
from backend.app.question_engines.ordering_engine import OrderingEngine
from backend.app.question_engines.hotspot_engine import HotspotEngine
from backend.app.auth.dependencies import get_current_user

router = APIRouter(prefix="/api/question-engines", tags=["Specialized Item Engines"])


@router.post("/grade/numerical", response_model=NumericalGradingResponse)
def grade_numerical(req: NumericalGradingRequest, current_user: dict = Depends(get_current_user)):
    """Evaluate STEM numerical response with units and tolerance."""
    return NumericalEngine.evaluate(req)


@router.post("/grade/cloze", response_model=ClozeGradingResponse)
def grade_cloze(req: ClozeGradingRequest, current_user: dict = Depends(get_current_user)):
    """Evaluate fill-in-the-blanks with typo distance tolerance."""
    return ClozeEngine.evaluate(req)


@router.post("/grade/ordering", response_model=OrderingGradingResponse)
def grade_ordering(req: OrderingGradingRequest, current_user: dict = Depends(get_current_user)):
    """Evaluate ordered sequences with Kendall's Tau / Spearman correlation partial credit."""
    return OrderingEngine.evaluate(req)


@router.post("/grade/hotspot", response_model=HotspotGradingResponse)
def grade_hotspot(req: HotspotGradingRequest, current_user: dict = Depends(get_current_user)):
    """Evaluate candidate click point inside target polygon."""
    return HotspotEngine.evaluate(req)
