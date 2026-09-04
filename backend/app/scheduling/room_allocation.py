"""
ExamHub - Examination Hall Seating & Venue Space Allocator
Assigns physical testing seats using alternating checkerboard anti-collusion patterns.
"""

from typing import List, Dict, Any, Tuple

class RoomAllocator:
    """Allocates hall seating layouts with anti-cheating spacing rules."""

    @staticmethod
    def generate_checkerboard_seating(
        room_name: str,
        rows: int,
        cols: int,
        students: List[Dict[str, str]]  # [{'id': '...', 'name': '...', 'roll': '...'}]
    ) -> Dict[str, Any]:
        """
        Alternating pattern: (row + col) % 2 == 0 is active seat.
        Leaves buffer seats empty adjacent to every active candidate.
        """
        total_desks = rows * cols
        usable_seats = []

        for r in range(rows):
            for c in range(cols):
                if (r + c) % 2 == 0:
                    usable_seats.append((r + 1, c + 1, f"Desk-R{r+1}C{c+1}"))

        seat_assignments = []
        unassigned_students = []

        for idx, s in enumerate(students):
            if idx < len(usable_seats):
                row_num, col_num, desk_id = usable_seats[idx]
                seat_assignments.append({
                    "desk_id": desk_id,
                    "row": row_num,
                    "col": col_num,
                    "student_id": s["id"],
                    "student_name": s["name"],
                    "roll_number": s["roll"]
                })
            else:
                unassigned_students.append(s)

        capacity = len(usable_seats)
        occupancy_pct = round((len(seat_assignments) / capacity * 100.0), 1) if capacity > 0 else 0.0

        return {
            "room_name": room_name,
            "total_physical_desks": total_desks,
            "anti_collusion_capacity": capacity,
            "assigned_students_count": len(seat_assignments),
            "unassigned_count": len(unassigned_students),
            "occupancy_percentage": occupancy_pct,
            "seating_chart": seat_assignments,
            "overflow_students": unassigned_students
        }
