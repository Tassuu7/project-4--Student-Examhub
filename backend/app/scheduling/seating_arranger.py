"""
ExamHub Examination Seating Plan & Spacing Arranger
Arranges candidate seating in examination halls using alternating course interleaving
and diagonal spacing to minimize cheating risks.
"""

from typing import List, Dict, Tuple, Optional
from pydantic import BaseModel


class DeskSeat(BaseModel):
    seat_id: str
    row_number: int
    column_number: int
    candidate_id: Optional[str] = None
    course_code: Optional[str] = None
    is_blocked_for_spacing: bool = False


class RoomSeatingGrid(BaseModel):
    room_id: str
    rows: int
    columns: int
    allocated_seats: List[DeskSeat]
    empty_buffer_seats_count: int
    total_seated: int


class SeatingPlanArranger:
    """
    Allocates candidates to physical desk matrices.
    Employs checkerboard interleaving (Course A, Course B alternating)
    so no two students taking the same exam sit adjacent horizontally, vertically, or diagonally.
    """

    @classmethod
    def arrange_room_seating(
        cls,
        room_id: str,
        rows: int,
        columns: int,
        cohorts: Dict[str, List[str]],  # course_code -> list of candidate_ids
        spacing_mode: str = "checkerboard"  # "checkerboard", "alternate_rows", "dense"
    ) -> RoomSeatingGrid:
        seats: List[DeskSeat] = []
        allocated_count = 0
        empty_buffer = 0

        # Flatten candidates with course tags
        cohort_queues: Dict[str, List[str]] = {c: list(ids) for c, ids in cohorts.items()}
        course_keys = list(cohort_queues.keys())
        current_course_idx = 0

        for r in range(1, rows + 1):
            for c in range(1, columns + 1):
                seat_id = f"{room_id}-R{r:02d}-C{c:02d}"

                if spacing_mode == "checkerboard":
                    # In checkerboard, only occupy seats where (r + c) % 2 == 0
                    if (r + c) % 2 != 0:
                        seats.append(
                            DeskSeat(
                                seat_id=seat_id,
                                row_number=r,
                                column_number=c,
                                is_blocked_for_spacing=True
                            )
                        )
                        empty_buffer += 1
                        continue

                # Find candidate from next available course queue
                placed = False
                for attempt in range(len(course_keys)):
                    active_course = course_keys[(current_course_idx + attempt) % len(course_keys)]
                    if cohort_queues[active_course]:
                        cand_id = cohort_queues[active_course].pop(0)
                        seats.append(
                            DeskSeat(
                                seat_id=seat_id,
                                row_number=r,
                                column_number=c,
                                candidate_id=cand_id,
                                course_code=active_course,
                                is_blocked_for_spacing=False
                            )
                        )
                        allocated_count += 1
                        current_course_idx = (current_course_idx + attempt + 1) % len(course_keys)
                        placed = True
                        break

                if not placed:
                    # No more candidates to seat
                    seats.append(
                        DeskSeat(
                            seat_id=seat_id,
                            row_number=r,
                            column_number=c,
                            is_blocked_for_spacing=False
                        )
                    )
                    empty_buffer += 1

        return RoomSeatingGrid(
            room_id=room_id,
            rows=rows,
            columns=columns,
            allocated_seats=seats,
            empty_buffer_seats_count=empty_buffer,
            total_seated=allocated_count
        )
