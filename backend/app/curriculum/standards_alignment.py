"""
ExamHub - Educational Standards & Accreditation Mapping Engine
Tracks alignment to Course Learning Outcomes (CLOs) and Program Educational Objectives (PEOs).
"""

from typing import List, Dict, Any, Set
from collections import defaultdict

class StandardsAlignmentEngine:
    """Audits curriculum coverage against institutional standards."""

    @staticmethod
    def audit_outcome_coverage(
        course_outcomes: List[Dict[str, str]],  # [{'code': 'CLO1', 'description': '...'}]
        exam_questions: List[Dict[str, Any]]    # [{'id': '...', 'clo_code': 'CLO1', 'marks': 2.0}]
    ) -> Dict[str, Any]:
        outcome_map = {o["code"]: o["description"] for o in course_outcomes}
        coverage_counts = defaultdict(int)
        coverage_marks = defaultdict(float)

        for q in exam_questions:
            clo = q.get("clo_code")
            if clo and clo in outcome_map:
                coverage_counts[clo] += 1
                coverage_marks[clo] += float(q.get("marks", 1.0))

        total_marks = sum(coverage_marks.values()) or 1.0

        aligned = []
        uncovered = []

        for code, desc in outcome_map.items():
            count = coverage_counts.get(code, 0)
            marks = coverage_marks.get(code, 0.0)
            weight_pct = round((marks / total_marks) * 100.0, 1)

            entry = {
                "outcome_code": code,
                "description": desc,
                "question_count": count,
                "marks_allocated": marks,
                "weight_percentage": weight_pct
            }

            if count > 0:
                aligned.append(entry)
            else:
                uncovered.append(entry)

        compliance_rate = (len(aligned) / len(course_outcomes) * 100.0) if course_outcomes else 100.0

        return {
            "total_outcomes": len(course_outcomes),
            "covered_outcomes_count": len(aligned),
            "uncovered_outcomes_count": len(uncovered),
            "outcome_coverage_rate": round(compliance_rate, 1),
            "covered_outcomes": aligned,
            "uncovered_gaps": uncovered,
            "accreditation_readiness": "Ready for ABET/AACSB Audit" if compliance_rate >= 85.0 else "Coverage Deficiencies Detected"
        }
