"""
ExamHub - Analytics Application Service
Orchestrates raw student data extraction, psychometric model computation,
mastery level categorization, and cohort insights.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from collections import defaultdict

from backend.app.analytics.repository import AnalyticsRepository
from backend.app.analytics.metrics_engine import MetricsEngine
from backend.app.analytics.schemas import (
    ExamAnalyticsResponse, CandidateRankItem, TopicPerformance,
    SystemOverviewAnalytics, SubjectComparativeMetrics
)
from backend.app.core.exceptions import NotFoundException

class AnalyticsService:
    """Business logic coordinator for educational analytics and psychometrics."""

    @staticmethod
    def get_exam_analytics(exam_id: str) -> ExamAnalyticsResponse:
        meta = AnalyticsRepository.get_exam_metadata(exam_id)
        if not meta:
            raise NotFoundException(f"Examination with ID '{exam_id}' not found.")

        student_scores = AnalyticsRepository.get_exam_student_scores(exam_id)
        raw_scores = [float(s["obtained_marks"]) for s in student_scores]
        raw_percentages = [float(s["percentage"]) for s in student_scores]
        total_marks = float(meta["total_marks"])
        passing_pct = float(meta["passing_percentage"])

        # 1. Classical Statistical Summary
        summary = MetricsEngine.calculate_score_summary(raw_scores, total_marks)

        # 2. Pass/Fail Breakdown
        pass_fail = MetricsEngine.calculate_pass_fail(raw_scores, passing_pct, total_marks)

        # 3. Grade Distributions
        grades = MetricsEngine.calculate_grade_distribution(raw_percentages)

        # 4. Deciles
        deciles = MetricsEngine.calculate_deciles(raw_scores, total_marks)

        # 5. Question Item Psychometrics (IRT & CTT)
        question_rows = AnalyticsRepository.get_exam_questions_with_answers(exam_id)
        grouped_questions = defaultdict(list)
        q_meta_map = {}
        for r in question_rows:
            qid = r["question_id"]
            grouped_questions[qid].append(r)
            if qid not in q_meta_map:
                q_meta_map[qid] = {
                    "order_index": r["order_index"],
                    "question_text": r["question_text"],
                    "difficulty": r["difficulty"],
                    "topic": r["topic"],
                    "marks_allocated": r["marks_allocated"]
                }

        question_metrics = []
        for qid, q_meta in sorted(q_meta_map.items(), key=lambda x: x[1]["order_index"]):
            responses = grouped_questions[qid]
            qm = MetricsEngine.calculate_item_psychometrics(qid, q_meta, responses)
            question_metrics.append(qm)

        # 6. Topic Performance Aggregation
        topic_groups = defaultdict(lambda: {"count": 0, "marks": 0.0, "correct": 0, "total_attempts": 0})
        for qm in question_metrics:
            t = qm.topic or "General"
            topic_groups[t]["count"] += 1
            topic_groups[t]["marks"] += qm.marks_allocated
            topic_groups[t]["correct"] += qm.correct_attempts
            topic_groups[t]["total_attempts"] += qm.total_attempts

        topic_performance = []
        for topic_name, t_data in topic_groups.items():
            attempts = t_data["total_attempts"]
            acc = (t_data["correct"] / attempts * 100.0) if attempts > 0 else 0.0
            if acc >= 80.0:
                mastery = "Mastered"
            elif acc >= 60.0:
                mastery = "Proficient"
            elif acc >= 40.0:
                mastery = "Developing"
            else:
                mastery = "Novice"

            topic_performance.append(TopicPerformance(
                topic=topic_name,
                question_count=t_data["count"],
                total_marks=round(t_data["marks"], 1),
                average_accuracy_percentage=round(acc, 1),
                mastery_level=mastery,
                weak_student_count=sum(1 for s in student_scores if s["percentage"] < 50.0),
                strong_student_count=sum(1 for s in student_scores if s["percentage"] >= 75.0)
            ))

        # 7. Candidate Ranking & At-Risk Identification
        candidates = []
        n_total = len(student_scores)
        for idx, row in enumerate(student_scores):
            # Compute time taken
            try:
                start_dt = datetime.fromisoformat(row["start_time"])
                end_dt = datetime.fromisoformat(row["end_time"]) if row.get("end_time") else start_dt
                duration_sec = max(0, int((end_dt - start_dt).total_seconds()))
            except Exception:
                duration_sec = 0

            m = duration_sec // 60
            s = duration_sec % 60
            formatted_time = f"{m}m {s}s"

            percentile = round(((n_total - idx) / n_total) * 100.0, 1) if n_total > 0 else 100.0

            candidates.append(CandidateRankItem(
                rank=idx + 1,
                student_id=row["student_id"],
                user_id=row["user_id"],
                full_name=row["full_name"],
                roll_number=row["roll_number"],
                obtained_marks=float(row["obtained_marks"]),
                total_marks=float(row["total_marks"]),
                percentage=float(row["percentage"]),
                grade=row["grade"],
                pass_fail=row["pass_fail"],
                percentile=percentile,
                completion_time_seconds=duration_sec,
                time_taken_formatted=formatted_time,
                submitted_at=row.get("end_time") or ""
            ))

        top_performers = candidates[:5]
        at_risk = [c for c in candidates if c.pass_fail == "FAIL" or c.percentage < passing_pct]

        return ExamAnalyticsResponse(
            exam_id=exam_id,
            exam_name=meta["name"],
            subject_code=meta["subject_code"],
            subject_name=meta["subject_name"],
            duration_minutes=int(meta["duration_minutes"]),
            total_marks=total_marks,
            passing_percentage=passing_pct,
            score_summary=summary,
            pass_fail=pass_fail,
            grade_distribution=grades,
            deciles=deciles,
            question_metrics=question_metrics,
            topic_performance=topic_performance,
            top_performers=top_performers,
            at_risk_candidates=at_risk,
            generated_at=datetime.utcnow().isoformat()
        )

    @staticmethod
    def get_system_overview() -> SystemOverviewAnalytics:
        counts = AnalyticsRepository.get_system_overview_counts()
        subject_summaries = AnalyticsRepository.get_subject_performance_summaries()

        return SystemOverviewAnalytics(
            total_users=counts["total_users"],
            total_students=counts["total_students"],
            total_teachers=counts["total_teachers"],
            total_subjects=counts["total_subjects"],
            total_questions=counts["total_questions"],
            total_exams=counts["total_exams"],
            total_attempts_completed=counts["total_attempts_completed"],
            global_average_score_pct=counts["global_average_score_pct"],
            global_pass_rate_pct=counts["global_pass_rate_pct"],
            active_exams_count=counts["active_exams_count"],
            proctoring_alerts_today=counts["proctoring_alerts_today"],
            recent_performance=[
                SubjectComparativeMetrics(**s) for s in subject_summaries
            ]
        )
