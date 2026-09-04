"""
ExamHub - Historical Performance & Longitudinal Trend Analyzer
Tracks student learning trajectories, semester-over-semester score growth,
learning retention indices, and early academic intervention warnings.
"""

from typing import List, Dict, Any, Optional, Tuple
import math
from backend.app.database.connection import get_db_connection

class TrendAnalyzer:
    """Longitudinal statistical trend modeling for examination scores."""

    @staticmethod
    def get_student_trend(student_id: str) -> Dict[str, Any]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, r.exam_id, r.percentage, r.obtained_marks, r.total_marks,
                   r.grade, r.pass_fail, r.generated_at, e.name as exam_name,
                   s.code as subject_code, s.name as subject_name
            FROM results r
            JOIN exams e ON r.exam_id = e.id
            JOIN subjects s ON e.subject_id = s.id
            WHERE r.student_id = ?
            ORDER BY r.generated_at ASC
        """, (student_id,))
        records = [dict(row) for row in cursor.fetchall()]

        if not records:
            return {
                "student_id": student_id,
                "record_count": 0,
                "trajectory": "Insufficient Data",
                "slope": 0.0,
                "average_score": 0.0,
                "history": []
            }

        scores = [float(r["percentage"]) for r in records]
        n = len(scores)
        avg = sum(scores) / n

        # Ordinary Least Squares (OLS) Linear Regression slope over time
        if n >= 2:
            x_vals = list(range(n))
            mean_x = sum(x_vals) / n
            numerator = sum((x_vals[i] - mean_x) * (scores[i] - avg) for i in range(n))
            denominator = sum((x_vals[i] - mean_x) ** 2 for i in range(n))
            slope = (numerator / denominator) if denominator != 0 else 0.0
        else:
            slope = 0.0

        if slope > 2.0:
            trajectory = "Accelerating Growth"
        elif slope > 0.5:
            trajectory = "Steady Improvement"
        elif slope > -0.5:
            trajectory = "Consistent Performance"
        elif slope > -2.0:
            trajectory = "Slight Decline"
        else:
            trajectory = "Significant Drop - Intervention Needed"

        return {
            "student_id": student_id,
            "record_count": n,
            "trajectory": trajectory,
            "slope": round(slope, 3),
            "average_score": round(avg, 2),
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "history": records
        }

    @staticmethod
    def get_subject_longitudinal_trend(subject_id: str) -> Dict[str, Any]:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT e.id as exam_id, e.name as exam_name, e.created_at,
                   AVG(r.percentage) as mean_percentage,
                   COUNT(r.id) as candidate_count,
                   SUM(CASE WHEN r.pass_fail = 'PASS' THEN 1 ELSE 0 END) as pass_count
            FROM exams e
            JOIN results r ON e.id = r.exam_id
            WHERE e.subject_id = ?
            GROUP BY e.id
            ORDER BY e.created_at ASC
        """, (subject_id,))
        exam_points = [dict(row) for row in cursor.fetchall()]

        if not exam_points:
            return {
                "subject_id": subject_id,
                "exam_count": 0,
                "trend_status": "No Historical Data",
                "timeline": []
            }

        percentages = [float(ep["mean_percentage"]) for ep in exam_points]
        n = len(percentages)

        if n >= 2:
            first_half_avg = sum(percentages[:n // 2]) / (n // 2)
            second_half_avg = sum(percentages[n // 2:]) / (n - n // 2)
            diff = second_half_avg - first_half_avg
            if diff > 5.0:
                trend = "Curriculum Mastery Improving"
            elif diff < -5.0:
                trend = "Curriculum Difficulty Spike Detected"
            else:
                trend = "Curriculum Balance Normal"
        else:
            trend = "Baseline Assessment"

        return {
            "subject_id": subject_id,
            "exam_count": n,
            "trend_status": trend,
            "timeline": exam_points
        }
