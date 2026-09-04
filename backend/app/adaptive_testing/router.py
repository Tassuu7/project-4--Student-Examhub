"""
ExamHub Computerized Adaptive Testing - FastAPI Router
Provides REST API endpoints for initiating CAT sessions, fetching next items,
recording responses, dynamically tracking candidate theta and stopping tests.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.adaptive_testing.schemas import (
    CATSessionConfig,
    CATSessionState,
    NextItemRequest,
    NextItemResponse,
    SubmitCATAnswerRequest,
    SubmitCATAnswerResponse,
    CATSimulationRequest,
    CATSimulationResult,
    CandidateResponseRecord,
    StoppingRuleType,
    AbilityEstimationMethod,
)
from backend.app.adaptive_testing.engine import CATEngine
from backend.app.adaptive_testing.item_selector import ItemSelector
from backend.app.auth.dependencies import get_current_user, require_role

router = APIRouter(prefix="/api/cat", tags=["Adaptive Testing"])

# In-memory session store & item selector
_GLOBAL_POOL = ItemSelector.generate_synthetic_pool(120)
_SELECTOR = ItemSelector(_GLOBAL_POOL)
_SESSIONS: Dict[str, CATSessionState] = {}


@router.post("/start", response_model=CATSessionState)
def start_cat_session(
    exam_id: str,
    config: Optional[CATSessionConfig] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Initialize a new Computerized Adaptive Testing session for the current candidate.
    """
    session_config = config or CATSessionConfig()
    session_id = f"cat-sess-{uuid.uuid4().hex[:12]}"
    now_str = datetime.now(timezone.utc).isoformat()

    state = CATSessionState(
        session_id=session_id,
        candidate_id=str(current_user.get("id", "guest")),
        exam_id=exam_id,
        config=session_config,
        current_step=0,
        current_theta=session_config.initial_theta,
        current_sem=1.0,
        responses=[],
        administered_item_ids=[],
        is_completed=False,
        started_at=now_str
    )
    _SESSIONS[session_id] = state
    _SELECTOR.total_sessions += 1
    return state


@router.post("/next-item", response_model=NextItemResponse)
def get_next_item(
    req: NextItemRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Fetch the next optimal test item based on candidate's current theta estimate.
    """
    state = _SESSIONS.get(req.session_id)
    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CAT session {req.session_id} not found."
        )

    if state.is_completed:
        return NextItemResponse(
            session_id=state.session_id,
            step_number=state.current_step,
            is_completed=True,
            current_theta=state.current_theta,
            current_sem=state.current_sem,
            total_administered=len(state.responses),
            termination_reason=state.termination_reason
        )

    # Content counts
    content_counts: Dict[str, int] = {}
    for it_id in state.administered_item_ids:
        it = _SELECTOR.item_map.get(it_id)
        if it:
            content_counts[it.domain_content] = content_counts.get(it.domain_content, 0) + 1

    item = _SELECTOR.select_next_item(
        current_theta=state.current_theta,
        administered_ids=set(state.administered_item_ids),
        administered_content_counts=content_counts if state.config.content_balancing else None,
        exposure_control_rate=state.config.exposure_control_rate
    )

    if not item:
        # Pool exhausted
        state.is_completed = True
        state.termination_reason = "Item pool exhausted"
        state.completed_at = datetime.now(timezone.utc).isoformat()
        state.percentile_rank = CATEngine.theta_to_percentile(state.current_theta)
        return NextItemResponse(
            session_id=state.session_id,
            step_number=state.current_step,
            is_completed=True,
            current_theta=state.current_theta,
            current_sem=state.current_sem,
            total_administered=len(state.responses),
            termination_reason=state.termination_reason
        )

    state.current_step += 1
    state.administered_item_ids.append(item.item_id)

    return NextItemResponse(
        session_id=state.session_id,
        step_number=state.current_step,
        is_completed=False,
        item_id=item.item_id,
        question_text=item.question_text,
        options=item.options,
        current_theta=state.current_theta,
        current_sem=state.current_sem,
        total_administered=len(state.responses)
    )


@router.post("/submit-answer", response_model=SubmitCATAnswerResponse)
def submit_cat_answer(
    req: SubmitCATAnswerRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Score the candidate's answer to the current item and update their theta estimate and SEM.
    """
    state = _SESSIONS.get(req.session_id)
    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CAT session {req.session_id} not found."
        )

    if state.is_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session already completed."
        )

    item = _SELECTOR.item_map.get(req.item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {req.item_id} not found in pool."
        )

    is_correct = (req.selected_option_index == item.correct_option_index)
    theta_prior = state.current_theta

    record = CandidateResponseRecord(
        step_number=state.current_step,
        item_id=item.item_id,
        selected_option_index=req.selected_option_index,
        is_correct=is_correct,
        response_time_seconds=req.response_time_seconds,
        difficulty_b=item.difficulty_b,
        discrimination_a=item.discrimination_a,
        guessing_c=item.guessing_c,
        theta_prior=theta_prior,
        theta_post=theta_prior,
        sem_post=state.current_sem
    )
    state.responses.append(record)

    # Recompute ability
    if state.config.estimation_method == AbilityEstimationMethod.EAP:
        new_theta, new_sem = CATEngine.estimate_theta_eap(state.responses)
    else:
        new_theta, new_sem = CATEngine.estimate_theta_mle(state.responses, initial_theta=state.current_theta)

    state.current_theta = new_theta
    state.current_sem = new_sem
    record.theta_post = new_theta
    record.sem_post = new_sem

    # Check stopping rule
    num_responses = len(state.responses)
    if num_responses >= state.config.min_items:
        if state.config.stopping_rule == StoppingRuleType.SEM_THRESHOLD:
            if new_sem <= state.config.target_sem:
                state.is_completed = True
                state.termination_reason = f"Target SEM precision reached ({new_sem:.3f} <= {state.config.target_sem:.3f})"
        elif state.config.stopping_rule == StoppingRuleType.FIXED_LENGTH:
            if num_responses >= state.config.max_items:
                state.is_completed = True
                state.termination_reason = f"Fixed length reached ({num_responses} items)"
        elif state.config.stopping_rule == StoppingRuleType.COMBINED:
            if new_sem <= state.config.target_sem:
                state.is_completed = True
                state.termination_reason = f"Target SEM precision reached ({new_sem:.3f} <= {state.config.target_sem:.3f})"
            elif num_responses >= state.config.max_items:
                state.is_completed = True
                state.termination_reason = f"Maximum test length reached ({state.config.max_items} items)"

    if state.is_completed:
        state.completed_at = datetime.now(timezone.utc).isoformat()
        state.percentile_rank = CATEngine.theta_to_percentile(state.current_theta)

    return SubmitCATAnswerResponse(
        session_id=state.session_id,
        step_number=state.current_step,
        is_correct=is_correct,
        updated_theta=state.current_theta,
        updated_sem=state.current_sem,
        is_completed=state.is_completed,
        termination_reason=state.termination_reason
    )


@router.get("/session/{session_id}", response_model=CATSessionState)
def get_session_details(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve full session trajectory, responses, and final ability score.
    """
    state = _SESSIONS.get(session_id)
    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CAT session {session_id} not found."
        )
    return state


@router.post("/simulate", response_model=List[CATSimulationResult])
def run_cat_simulation(
    req: CATSimulationRequest,
    current_user: dict = Depends(require_role(["teacher", "admin"]))
):
    """
    Execute Monte Carlo simulation across true ability points to evaluate CAT properties.
    """
    from backend.app.adaptive_testing.simulation import CATSimulator

    results = []
    for th in req.true_thetas:
        sim_res = CATSimulator.run_simulation(
            true_theta=th,
            trials_count=40,
            pool_size=req.pool_size,
            config=req.config
        )
        results.append(sim_res)
    return results
