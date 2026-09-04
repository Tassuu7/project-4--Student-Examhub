"""
ExamHub Accreditation Engine - NBA & NAAC Attainment Computation
Calculates Course Outcome (CO) attainment and Program Outcome (PO) mapping matrices.
"""

from typing import List, Dict, Any, Tuple
from backend.app.accreditation.schemas import (
    CourseOutcome,
    CO_PO_Correlation,
    StudentAssessmentRecord,
    COAttainmentResult,
    POAttainmentMatrix,
    AccreditationStandard,
)


class NBAAttainmentEngine:
    """
    Computes direct assessment attainment metrics per National Board of Accreditation (NBA)
    and National Assessment and Accreditation Council (NAAC) Outcome-Based Education protocols.
    """

    @classmethod
    def calculate_co_attainment(
        cls,
        co: CourseOutcome,
        records: List[StudentAssessmentRecord]
    ) -> COAttainmentResult:
        """
        Evaluate student performance against target threshold for a Course Outcome.
        """
        co_records = [r for r in records if r.co_code == co.co_code]
        if not co_records:
            return COAttainmentResult(
                co_code=co.co_code,
                total_students=0,
                students_above_threshold=0,
                direct_attainment_percentage=0.0,
                attainment_level=0,
                target_met=False
            )

        # Aggregate student marks for this CO
        student_totals: Dict[str, Tuple[float, float]] = {}
        for r in co_records:
            cur_obt, cur_max = student_totals.get(r.student_id, (0.0, 0.0))
            student_totals[r.student_id] = (cur_obt + r.obtained_marks, cur_max + r.max_marks)

        total_students = len(student_totals)
        above_threshold_count = 0

        for sid, (obt, mx) in student_totals.items():
            if mx > 0:
                pct = (obt / mx) * 100.0
                if pct >= co.target_threshold_score:
                    above_threshold_count += 1

        attainment_pct = (above_threshold_count / total_students * 100.0) if total_students > 0 else 0.0

        # Assign attainment level (NBA 3-level rubric)
        if attainment_pct >= 80.0:
            level = 3
        elif attainment_pct >= 70.0:
            level = 2
        elif attainment_pct >= 60.0:
            level = 1
        else:
            level = 0

        target_met = attainment_pct >= co.target_percentage

        return COAttainmentResult(
            co_code=co.co_code,
            total_students=total_students,
            students_above_threshold=above_threshold_count,
            direct_attainment_percentage=round(attainment_pct, 2),
            attainment_level=level,
            target_met=target_met
        )

    @classmethod
    def compute_po_attainment(
        cls,
        course_id: str,
        co_results: List[COAttainmentResult],
        correlations: List[CO_PO_Correlation],
        standard: AccreditationStandard = AccreditationStandard.NBA
    ) -> POAttainmentMatrix:
        """
        Compute weighted PO attainment score across all CO mappings:
        PO_score = Sum(CO_level * Correlation) / Sum(Correlation)
        """
        co_level_map = {r.co_code: r.attainment_level for r in co_results}

        # Group correlations by PO
        po_map: Dict[str, List[CO_PO_Correlation]] = {}
        for c in correlations:
            if c.po_code not in po_map:
                po_map[c.po_code] = []
            po_map[c.po_code].append(c)

        po_scores: Dict[str, float] = {}
        for po_code, corr_list in po_map.items():
            weighted_sum = 0.0
            weight_total = 0

            for corr in corr_list:
                if corr.correlation_level > 0:
                    co_level = co_level_map.get(corr.co_code, 0)
                    weighted_sum += (co_level * corr.correlation_level)
                    weight_total += corr.correlation_level

            score = (weighted_sum / weight_total) if weight_total > 0 else 0.0
            po_scores[po_code] = round(score, 2)

        # Build display table matrix
        matrix_table = []
        for r in co_results:
            row: Dict[str, Any] = {
                "co_code": r.co_code,
                "direct_pct": r.direct_attainment_percentage,
                "level": r.attainment_level
            }
            for po_code in po_map:
                # Find correlation
                corr = next((c for c in correlations if c.co_code == r.co_code and c.po_code == po_code), None)
                row[po_code] = corr.correlation_level if corr else "-"
            matrix_table.append(row)

        recommendations = []
        unmet_cos = [r.co_code for r in co_results if not r.target_met]
        if unmet_cos:
            recommendations.append(
                f"Course outcomes {', '.join(unmet_cos)} failed to meet institutional target. Recommend remedial tutorial sessions."
            )
        else:
            recommendations.append("All course outcomes met institutional quality targets. Criteria verified for accreditation.")

        return POAttainmentMatrix(
            course_id=course_id,
            standard=standard,
            co_results=co_results,
            po_scores=po_scores,
            matrix_table=matrix_table,
            recommendations=recommendations
        )
