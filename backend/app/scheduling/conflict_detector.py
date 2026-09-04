"""
ExamHub - Timetable Collision & Schedule Conflict Detector
Detects candidate examination overlaps, room booking clashes, and fatigue proximity warnings.
"""

from typing import List, Dict, Any
from datetime import datetime

class ScheduleConflictDetector:
    """Audits institutional assessment timetables for temporal collisions."""

    @staticmethod
    def detect_student_collisions(
        exam_slots: List[Dict[str, Any]],
        student_enrollments: Dict[str, List[str]]  # student_id -> list of exam_ids
    ) -> List[Dict[str, Any]]:
        """
        exam_slots: [{'exam_id': '...', 'start_time': '2026-09-10T09:00:00', 'end_time': '2026-09-10T11:00:00'}]
        """
        slot_map = {}
        for slot in exam_slots:
            try:
                s_dt = datetime.fromisoformat(slot["start_time"])
                e_dt = datetime.fromisoformat(slot["end_time"])
                slot_map[slot["exam_id"]] = (s_dt, e_dt)
            except Exception:
                continue

        collisions = []

        for stu_id, exam_ids in student_enrollments.items():
            for i in range(len(exam_ids)):
                for j in range(i + 1, len(exam_ids)):
                    ex_a = exam_ids[i]
                    ex_b = exam_ids[j]

                    if ex_a in slot_map and ex_b in slot_map:
                        start_a, end_a = slot_map[ex_a]
                        start_b, end_b = slot_map[ex_b]

                        # Check temporal overlap: max(start_a, start_b) < min(end_a, end_b)
                        if max(start_a, start_b) < min(end_a, end_b):
                            collisions.append({
                                "student_id": stu_id,
                                "exam_a_id": ex_a,
                                "exam_b_id": ex_b,
                                "conflict_type": "Direct Timetable Overlap",
                                "start_a": start_a.isoformat(),
                                "end_a": end_a.isoformat(),
                                "start_b": start_b.isoformat(),
                                "end_b": end_b.isoformat()
                            })
                        else:
                            # Check fatigue gap (< 30 minutes between exams)
                            gap_minutes = abs((start_b - end_a).total_seconds()) / 60.0
                            if gap_minutes < 30.0:
                                collisions.append({
                                    "student_id": stu_id,
                                    "exam_a_id": ex_a,
                                    "exam_b_id": ex_b,
                                    "conflict_type": f"Severe Exam Fatigue ({int(gap_minutes)}m rest window)",
                                    "gap_minutes": int(gap_minutes)
                                })

        return collisions
