"""
ExamHub - Competency Mastery Matrix & Skill Prerequisites Graph
Constructs student competency mastery vectors and models skill prerequisite dependencies.
"""

from typing import List, Dict, Any, Set
from collections import defaultdict

class CompetencyMatrixEngine:
    """Evaluates student competency progression along curriculum learning graphs."""

    @staticmethod
    def evaluate_competency_mastery(
        student_results: List[Dict[str, Any]],
        competency_skills: List[str]
    ) -> Dict[str, Any]:
        """
        student_results: List of {'skill': '...', 'is_correct': 1, 'marks': 2.0}
        """
        skill_totals = defaultdict(lambda: {"attempts": 0, "correct": 0, "marks_earned": 0.0})

        for r in student_results:
            s = r.get("skill")
            if s:
                skill_totals[s]["attempts"] += 1
                if r.get("is_correct") == 1:
                    skill_totals[s]["correct"] += 1
                    skill_totals[s]["marks_earned"] += float(r.get("marks", 1.0))

        mastery_levels = {}
        for skill in competency_skills:
            data = skill_totals[skill]
            att = data["attempts"]
            accuracy = (data["correct"] / att * 100.0) if att > 0 else 0.0

            if att == 0:
                tier = "Unassessed"
            elif accuracy >= 85.0:
                tier = "Advanced Mastery"
            elif accuracy >= 65.0:
                tier = "Proficient"
            elif accuracy >= 40.0:
                tier = "Basic Competence"
            else:
                tier = "Needs Remediation"

            mastery_levels[skill] = {
                "attempts": att,
                "accuracy_pct": round(accuracy, 1),
                "proficiency_tier": tier
            }

        proficient_count = sum(
            1 for v in mastery_levels.values()
            if v["proficiency_tier"] in ("Advanced Mastery", "Proficient")
        )

        return {
            "total_competencies": len(competency_skills),
            "proficient_count": proficient_count,
            "overall_competency_index": round((proficient_count / len(competency_skills) * 100.0), 1) if competency_skills else 0.0,
            "competency_breakdown": mastery_levels
        }
