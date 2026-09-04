"""
ExamHub - Invigilator & Proctor Duty Rostering Engine
Assigns academic invigilators to exam halls ensuring fairness and conflict-of-interest prevention.
"""

from typing import List, Dict, Any

class InvigilatorRosterEngine:
    """Manages proctor duty assignments and verifies impartiality."""

    @staticmethod
    def assign_proctors(
        exam_sessions: List[Dict[str, Any]],
        available_teachers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Prevents instructors from invigilating courses they authored/instruct.
        """
        assignments = []
        unassigned_sessions = []
        teacher_duty_counts = {t["id"]: 0 for t in available_teachers}

        for session in exam_sessions:
            exam_subject_id = session.get("subject_id")
            hall_name = session.get("hall_name", "Hall 1")
            assigned = False

            # Sort available teachers by least duties assigned
            sorted_teachers = sorted(available_teachers, key=lambda t: teacher_duty_counts[t["id"]])

            for t in sorted_teachers:
                # Conflict of interest check: teacher's own subject
                if exam_subject_id in t.get("taught_subject_ids", []):
                    continue

                assignments.append({
                    "session_id": session.get("id"),
                    "exam_name": session.get("exam_name"),
                    "hall_name": hall_name,
                    "proctor_id": t["id"],
                    "proctor_name": t["name"],
                    "duty_date": session.get("date")
                })
                teacher_duty_counts[t["id"]] += 1
                assigned = True
                break

            if not assigned:
                unassigned_sessions.append(session)

        return {
            "total_sessions": len(exam_sessions),
            "assigned_sessions": len(assignments),
            "unassigned_sessions": unassigned_sessions,
            "roster": assignments,
            "duty_distribution": teacher_duty_counts
        }
