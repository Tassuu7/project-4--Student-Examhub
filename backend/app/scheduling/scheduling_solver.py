"""
ExamHub Institutional Examination Scheduling Solver
Implements a Constraint Satisfaction Problem (CSP) solver using backtracking search
with Minimum Remaining Values (MRV) heuristic and forward checking to schedule exam sessions,
rooms, invigilators, and candidate cohorts without time, room, or proctor conflicts.
"""

from typing import List, Dict, Set, Optional, Tuple, Any
from pydantic import BaseModel, Field
from datetime import datetime, timedelta


class TimeSlot(BaseModel):
    slot_id: str
    date_str: str          # YYYY-MM-DD
    start_time: str        # HH:MM
    end_time: str          # HH:MM
    duration_minutes: int = 120


class ExamRoom(BaseModel):
    room_id: str
    room_number: str
    building: str
    capacity: int
    is_computer_lab: bool = False
    has_proctoring_station: bool = True
    wheelchair_accessible: bool = True


class InvigilatorFaculty(BaseModel):
    faculty_id: str
    name: str
    department: str
    max_daily_slots: int = 2
    max_weekly_slots: int = 8
    unavailable_slot_ids: Set[str] = Field(default_factory=set)


class CourseExamSession(BaseModel):
    session_id: str
    course_code: str
    course_title: str
    enrolled_student_ids: List[str]
    requires_computer_lab: bool = False
    required_invigilators: int = 1
    duration_minutes: int = 120


class ScheduleAssignment(BaseModel):
    assignment_id: str
    session_id: str
    course_code: str
    slot_id: str
    room_id: str
    invigilator_ids: List[str]
    assigned_student_count: int


class ExamSchedulingSolver:
    """
    Solves complex multi-facility institutional exam timetabling constraints:
    1. No student has overlapping exams in the same time slot.
    2. Room capacity is not exceeded.
    3. Computer lab requirements are satisfied.
    4. Invigilators are not double-booked or assigned beyond daily limits.
    5. Invigilator department neutrality (optional: professors don't invigilate their own courses).
    """

    def __init__(
        self,
        slots: List[TimeSlot],
        rooms: List[ExamRoom],
        invigilators: List[InvigilatorFaculty],
        exams: List[CourseExamSession]
    ):
        self.slots = slots
        self.rooms = rooms
        self.invigilators = invigilators
        self.exams = exams

        # Student lookup for rapid collision checking
        self.exam_student_map: Dict[str, Set[str]] = {
            e.session_id: set(e.enrolled_student_ids) for e in exams
        }

        # Precompute student overlap graph between exams
        self.exam_conflicts: Dict[str, Set[str]] = {e.session_id: set() for e in exams}
        for i in range(len(exams)):
            for j in range(i + 1, len(exams)):
                e1 = exams[i]
                e2 = exams[j]
                shared = self.exam_student_map[e1.session_id].intersection(self.exam_student_map[e2.session_id])
                if shared:
                    self.exam_conflicts[e1.session_id].add(e2.session_id)
                    self.exam_conflicts[e2.session_id].add(e1.session_id)

    def is_assignment_valid(
        self,
        exam: CourseExamSession,
        slot: TimeSlot,
        room: ExamRoom,
        chosen_invigilators: List[InvigilatorFaculty],
        current_assignments: List[ScheduleAssignment]
    ) -> bool:
        # Check lab requirement
        if exam.requires_computer_lab and not room.is_computer_lab:
            return False

        # Check capacity
        if len(exam.enrolled_student_ids) > room.capacity:
            return False

        # Check slot duration
        if exam.duration_minutes > slot.duration_minutes:
            return False

        # Check room and student conflicts in same slot
        for asgn in current_assignments:
            if asgn.slot_id == slot.slot_id:
                # Room double-booked
                if asgn.room_id == room.room_id:
                    return False
                # Student conflict
                if asgn.session_id in self.exam_conflicts.get(exam.session_id, set()):
                    return False
                # Invigilator conflict
                for inv in chosen_invigilators:
                    if inv.faculty_id in asgn.invigilator_ids:
                        return False

        # Check invigilator daily load
        for inv in chosen_invigilators:
            if slot.slot_id in inv.unavailable_slot_ids:
                return False
            daily_count = sum(
                1 for asgn in current_assignments
                if inv.faculty_id in asgn.invigilator_ids and any(
                    s.slot_id == asgn.slot_id and s.date_str == slot.date_str for s in self.slots
                )
            )
            if daily_count >= inv.max_daily_slots:
                return False

        return True

    def solve(self) -> Optional[List[ScheduleAssignment]]:
        """
        Backtracking search with forward checking.
        """
        # Sort exams by number of conflicts and size (Most Constrained First heuristic)
        sorted_exams = sorted(
            self.exams,
            key=lambda e: (len(self.exam_conflicts[e.session_id]), len(e.enrolled_student_ids)),
            reverse=True
        )

        assignments: List[ScheduleAssignment] = []

        def backtrack(exam_idx: int) -> bool:
            if exam_idx >= len(sorted_exams):
                return True

            exam = sorted_exams[exam_idx]

            # Try slots
            for slot in self.slots:
                # Try rooms
                for room in self.rooms:
                    if exam.requires_computer_lab and not room.is_computer_lab:
                        continue
                    if len(exam.enrolled_student_ids) > room.capacity:
                        continue

                    # Find eligible invigilators
                    eligible_invs = [
                        inv for inv in self.invigilators
                        if slot.slot_id not in inv.unavailable_slot_ids
                    ]

                    # Filter out already busy invigilators in this slot
                    busy_inv_ids = {
                        inv_id for asgn in assignments if asgn.slot_id == slot.slot_id
                        for inv_id in asgn.invigilator_ids
                    }
                    available_invs = [inv for inv in eligible_invs if inv.faculty_id not in busy_inv_ids]

                    if len(available_invs) < exam.required_invigilators:
                        continue

                    chosen_invs = available_invs[:exam.required_invigilators]

                    if self.is_assignment_valid(exam, slot, room, chosen_invs, assignments):
                        asgn = ScheduleAssignment(
                            assignment_id=f"asgn-{exam.session_id}-{slot.slot_id}",
                            session_id=exam.session_id,
                            course_code=exam.course_code,
                            slot_id=slot.slot_id,
                            room_id=room.room_id,
                            invigilator_ids=[inv.faculty_id for inv in chosen_invs],
                            assigned_student_count=len(exam.enrolled_student_ids)
                        )
                        assignments.append(asgn)

                        if backtrack(exam_idx + 1):
                            return True

                        assignments.pop()

            return False

        success = backtrack(0)
        return assignments if success else None
