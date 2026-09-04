"""
ExamHub - Exam Orchestration Service
"""

import datetime
from typing import Dict, Any, List, Optional, Tuple, Union
from fastapi import HTTPException, status
from backend.app.core.constants import ExamStatus, AttemptStatus, UserRole
from backend.app.auth.schemas import TokenData
from backend.app.exams.repository import ExamRepository
from backend.app.exams.evaluator import ExamEvaluator
from backend.app.exams.generator import ExamGenerator
from backend.app.exams.schemas import (
    ExamCreateRequest, ExamUpdateRequest, ExamQuestionAssignmentRequest,
    ExamStudentAssignmentRequest, StudentAnswerSaveRequest, ExamAutoGenerateRequest
)

def get_user_meta(user: Union[TokenData, Dict[str, Any]]) -> Tuple[str, str, Optional[str], Optional[str]]:
    """Returns (user_id, role, teacher_id, student_id)"""
    if isinstance(user, TokenData):
        role_str = user.role.value if hasattr(user.role, "value") else str(user.role)
        return user.sub, role_str, user.teacher_id, user.student_id
    elif isinstance(user, dict):
        role_str = user.get("role")
        if hasattr(role_str, "value"):
            role_str = role_str.value
        t_id = user.get("teacher_id") or user.get("teacher_profile", {}).get("id")
        s_id = user.get("student_id") or user.get("student_profile", {}).get("id")
        return user.get("id") or user.get("sub", ""), str(role_str), t_id, s_id
    return "", "", None, None

class ExamService:
    @staticmethod
    def create_exam(data: ExamCreateRequest, current_user: Union[TokenData, Dict[str, Any]]) -> str:
        user_id, role, teacher_id, _ = get_user_meta(current_user)

        if role == UserRole.ADMIN.value and not teacher_id:
            from backend.app.database.connection import get_db_connection
            c = get_db_connection().cursor()
            c.execute("SELECT id FROM teachers LIMIT 1;")
            t_row = c.fetchone()
            if t_row:
                teacher_id = t_row[0]

        if not teacher_id:
            raise HTTPException(status_code=400, detail="Valid teacher profile required to create exam.")

        status_val = ExamStatus.ACTIVE.value
        if data.status:
            status_val = data.status.value if hasattr(data.status, "value") else str(data.status)

        exam_payload = {
            "name": data.name,
            "subject_id": data.subject_id,
            "teacher_id": teacher_id,
            "description": data.description,
            "duration_minutes": data.duration_minutes,
            "passing_percentage": data.passing_percentage,
            "start_date": data.start_date,
            "end_date": data.end_date,
            "instructions": data.instructions,
            "status": status_val
        }

        exam_id = ExamRepository.create_exam(exam_payload)

        if data.question_ids:
            allocations = [{"question_id": qid, "marks_allocated": 1.0} for qid in data.question_ids]
            ExamRepository.set_exam_questions(exam_id, allocations)

        if data.student_ids:
            ExamRepository.set_exam_students(exam_id, data.student_ids)
        else:
            all_stus = ExamRepository.get_all_student_ids()
            if all_stus:
                ExamRepository.set_exam_students(exam_id, all_stus)

        return exam_id

    @staticmethod
    def auto_generate_exam(data: ExamAutoGenerateRequest, current_user: Union[TokenData, Dict[str, Any]]) -> str:
        selected_questions = ExamGenerator.generate_questions(
            subject_id=data.subject_id,
            easy_count=data.easy_count,
            medium_count=data.medium_count,
            hard_count=data.hard_count,
            topic=data.topic_filter
        )

        create_req = ExamCreateRequest(
            name=data.name,
            subject_id=data.subject_id,
            description=f"Auto-generated exam with {len(selected_questions)} questions.",
            duration_minutes=data.duration_minutes,
            passing_percentage=data.passing_percentage,
            start_date=data.start_date,
            end_date=data.end_date,
            instructions=data.instructions or "Please read all questions carefully before submitting.",
            question_ids=[q["id"] for q in selected_questions]
        )

        return ExamService.create_exam(create_req, current_user)

    @staticmethod
    def update_exam(exam_id: str, data: ExamUpdateRequest, current_user: Union[TokenData, Dict[str, Any]]) -> Dict[str, Any]:
        exam = ExamRepository.get_by_id(exam_id)
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")

        _, role, teacher_id, _ = get_user_meta(current_user)
        if role == UserRole.TEACHER.value and exam["teacher_id"] != teacher_id:
            raise HTTPException(status_code=403, detail="Not authorized to edit this exam")

        update_dict = {k: v for k, v in data.model_dump(exclude={"question_ids", "student_ids"}).items() if v is not None}
        if "status" in update_dict and hasattr(update_dict["status"], "value"):
            update_dict["status"] = update_dict["status"].value

        ExamRepository.update_exam(exam_id, update_dict)

        if data.question_ids is not None:
            allocations = [{"question_id": qid, "marks_allocated": 1.0} for qid in data.question_ids]
            ExamRepository.set_exam_questions(exam_id, allocations)

        if data.student_ids is not None:
            ExamRepository.set_exam_students(exam_id, data.student_ids)

        return ExamRepository.get_by_id(exam_id)

    @staticmethod
    def delete_exam(exam_id: str, current_user: Union[TokenData, Dict[str, Any]]) -> bool:
        exam = ExamRepository.get_by_id(exam_id)
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")

        _, role, teacher_id, _ = get_user_meta(current_user)
        if role == UserRole.TEACHER.value and exam["teacher_id"] != teacher_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this exam")

        return ExamRepository.delete_exam(exam_id)

    @staticmethod
    def get_exam_details(exam_id: str) -> Dict[str, Any]:
        exam = ExamRepository.get_by_id(exam_id)
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")
        exam["questions"] = ExamRepository.get_exam_questions(exam_id)
        exam["assigned_students"] = ExamRepository.get_exam_assigned_students(exam_id)
        return exam

    @staticmethod
    def assign_questions(exam_id: str, req: ExamQuestionAssignmentRequest) -> Dict[str, Any]:
        allocations = [{"question_id": item.question_id, "marks_allocated": item.marks_allocated} for item in req.questions]
        total_marks = ExamRepository.set_exam_questions(exam_id, allocations)
        return {"exam_id": exam_id, "questions_count": len(allocations), "total_marks": total_marks}

    @staticmethod
    def assign_students(exam_id: str, req: ExamStudentAssignmentRequest) -> Dict[str, Any]:
        count = ExamRepository.set_exam_students(exam_id, req.student_ids)
        return {"exam_id": exam_id, "assigned_count": count}

    # Student Taking Flow
    @staticmethod
    def start_exam_attempt(exam_id: str, current_user: Union[TokenData, Dict[str, Any]]) -> Dict[str, Any]:
        _, role, _, student_id = get_user_meta(current_user)

        if role != UserRole.STUDENT.value:
            raise HTTPException(status_code=403, detail="Only students can attempt exams")

        if not student_id:
            raise HTTPException(status_code=400, detail="Student profile required")

        exam = ExamRepository.get_by_id(exam_id)
        if not exam:
            raise HTTPException(status_code=404, detail="Exam not found")

        if exam["status"] not in [ExamStatus.ACTIVE.value, ExamStatus.SCHEDULED.value]:
            raise HTTPException(status_code=400, detail=f"Exam is not open for attempts (Status: {exam['status']})")

        existing_attempt = ExamRepository.get_student_attempt_for_exam(exam_id, student_id)
        if existing_attempt:
            if existing_attempt["status"] in [AttemptStatus.SUBMITTED.value, AttemptStatus.AUTO_SUBMITTED.value, AttemptStatus.EVALUATED.value]:
                raise HTTPException(status_code=400, detail="Exam already submitted")
            attempt_id = existing_attempt["id"]
            time_remaining = existing_attempt["time_remaining_seconds"]
            start_time = existing_attempt["start_time"]
            status_val = existing_attempt["status"]
        else:
            attempt_id = ExamRepository.create_attempt(exam_id, student_id, exam["duration_minutes"])
            time_remaining = exam["duration_minutes"] * 60
            start_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
            status_val = AttemptStatus.IN_PROGRESS.value

        questions = ExamRepository.get_exam_questions(exam_id)
        saved_answers = ExamRepository.get_student_answers(attempt_id)

        public_questions = []
        for q in questions:
            qid = q["question_id"]
            ans_info = saved_answers.get(qid, {})
            public_questions.append({
                "id": q["exam_question_id"],
                "question_id": qid,
                "order_index": q["order_index"],
                "question_text": q["question_text"],
                "option_a": q["option_a"],
                "option_b": q["option_b"],
                "option_c": q["option_c"],
                "option_d": q["option_d"],
                "marks_allocated": q["marks_allocated"],
                "difficulty": q["difficulty"],
                "topic": q.get("topic"),
                "selected_option": ans_info.get("selected_option"),
                "is_marked_for_review": bool(ans_info.get("is_marked_for_review", False))
            })

        return {
            "attempt_id": attempt_id,
            "exam_id": exam["id"],
            "exam_name": exam["name"],
            "subject_code": exam["subject_code"],
            "subject_name": exam["subject_name"],
            "duration_minutes": exam["duration_minutes"],
            "time_remaining_seconds": time_remaining,
            "start_time": start_time,
            "status": status_val,
            "questions": public_questions,
            "instructions": exam.get("instructions"),
            "require_camera_proctoring": bool(exam.get("require_camera_proctoring", 1))
        }

    @staticmethod
    def save_answer(attempt_id: str, req: StudentAnswerSaveRequest, current_user: Union[TokenData, Dict[str, Any]]) -> Dict[str, Any]:
        attempt = ExamRepository.get_attempt_by_id(attempt_id)
        if not attempt:
            raise HTTPException(status_code=404, detail="Exam attempt not found")

        _, role, _, student_id = get_user_meta(current_user)
        if attempt["student_id"] != student_id and role != UserRole.ADMIN.value:
            raise HTTPException(status_code=403, detail="Unauthorized")

        if attempt["status"] != AttemptStatus.IN_PROGRESS.value:
            raise HTTPException(status_code=400, detail="Attempt is already closed")

        ExamRepository.upsert_student_answer(
            attempt_id=attempt_id,
            question_id=req.question_id,
            selected_option=req.selected_option,
            is_marked_for_review=req.is_marked_for_review
        )
        return {
            "question_id": req.question_id,
            "selected_option": req.selected_option,
            "is_marked_for_review": req.is_marked_for_review,
            "saved": True
        }

    @staticmethod
    def update_time_remaining(attempt_id: str, seconds_left: int, current_user: Union[TokenData, Dict[str, Any]]):
        attempt = ExamRepository.get_attempt_by_id(attempt_id)
        if not attempt:
            raise HTTPException(status_code=404, detail="Attempt not found")
        ExamRepository.update_attempt_time(attempt_id, seconds_left)

    @staticmethod
    def submit_exam_attempt(attempt_id: str, auto_submitted: bool = False) -> Dict[str, Any]:
        attempt = ExamRepository.get_attempt_by_id(attempt_id)
        if not attempt:
            raise HTTPException(status_code=404, detail="Exam attempt not found")

        if attempt["status"] in [AttemptStatus.SUBMITTED.value, AttemptStatus.AUTO_SUBMITTED.value, AttemptStatus.EVALUATED.value]:
            existing_result = ExamRepository.get_result_by_attempt_id(attempt_id)
            if existing_result:
                return ExamService.build_result_response(existing_result, attempt["exam_id"], attempt_id)

        exam_id = attempt["exam_id"]
        exam = ExamRepository.get_by_id(exam_id)
        questions = ExamRepository.get_exam_questions(exam_id)
        answers_by_qid = ExamRepository.get_student_answers(attempt_id)

        summary, item_evaluations = ExamEvaluator.evaluate_attempt(exam, questions, answers_by_qid)

        for it in item_evaluations:
            ExamRepository.update_student_answer_evaluation(
                attempt_id,
                it["question_id"],
                it["is_correct"],
                it["marks_obtained"]
            )

        final_status = AttemptStatus.AUTO_SUBMITTED.value if auto_submitted else AttemptStatus.SUBMITTED.value
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        ExamRepository.update_attempt_status(attempt_id, final_status, now_iso)

        result_payload = {
            "attempt_id": attempt_id,
            "exam_id": exam_id,
            "student_id": attempt["student_id"],
            "total_questions": summary["total_questions"],
            "correct_count": summary["correct_count"],
            "wrong_count": summary["wrong_count"],
            "unanswered_count": summary["unanswered_count"],
            "total_marks": summary["total_marks"],
            "obtained_marks": summary["obtained_marks"],
            "percentage": summary["percentage"],
            "grade": summary["grade"],
            "pass_fail": summary["pass_fail"],
            "rank": None
        }
        ExamRepository.save_result(result_payload)
        ExamRepository.recalculate_exam_ranks(exam_id)

        result = ExamRepository.get_result_by_attempt_id(attempt_id)
        return ExamService.build_result_response(result, exam_id, attempt_id)

    @staticmethod
    def get_result(attempt_id: str, current_user: Union[TokenData, Dict[str, Any]]) -> Dict[str, Any]:
        result = ExamRepository.get_result_by_attempt_id(attempt_id)
        if not result:
            raise HTTPException(status_code=404, detail="Result not found for this attempt")

        _, role, _, student_id = get_user_meta(current_user)
        if role == UserRole.STUDENT.value and result["student_id"] != student_id:
            raise HTTPException(status_code=403, detail="Unauthorized to view this result")

        return ExamService.build_result_response(result, result["exam_id"], attempt_id)

    @staticmethod
    def build_result_response(result: Dict[str, Any], exam_id: str, attempt_id: str) -> Dict[str, Any]:
        exam = ExamRepository.get_by_id(exam_id)
        questions = ExamRepository.get_exam_questions(exam_id)
        answers_by_qid = ExamRepository.get_student_answers(attempt_id)
        _, item_evaluations = ExamEvaluator.evaluate_attempt(exam, questions, answers_by_qid)

        all_results = ExamRepository.list_exam_results(exam_id)

        return {
            "result_id": result["id"],
            "attempt_id": attempt_id,
            "exam_id": exam_id,
            "exam_name": result["exam_name"],
            "subject_code": result["subject_code"],
            "subject_name": result["subject_name"],
            "student_id": result["student_id"],
            "student_name": result["student_name"],
            "student_roll_number": result["student_roll_number"],
            "total_questions": result["total_questions"],
            "correct_count": result["correct_count"],
            "wrong_count": result["wrong_count"],
            "unanswered_count": result["unanswered_count"],
            "total_marks": result["total_marks"],
            "obtained_marks": result["obtained_marks"],
            "percentage": result["percentage"],
            "grade": result["grade"],
            "pass_fail": result["pass_fail"],
            "rank": result["rank"],
            "total_candidates": len(all_results),
            "start_time": result["start_time"],
            "end_time": result["end_time"],
            "generated_at": result["generated_at"],
            "review_items": item_evaluations
        }
