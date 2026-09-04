"""
ExamHub Tabular Analytics and Institutional Data Export
Builds RFC 4180 compliant CSV and tab-delimited exports for cohort analysis and external SIS integration.
"""

import io
import csv
from typing import List, Dict, Any


class TabularAnalyticsExporter:
    """
    Generates tabular datasets for statistical packages (SPSS, R, Python Pandas).
    """

    @classmethod
    def export_cohort_responses_matrix_csv(
        cls,
        candidate_ids: List[str],
        question_ids: List[str],
        response_matrix: Dict[str, Dict[str, int]]  # candidate_id -> {qid: 0/1}
    ) -> str:
        """
        Creates candidate-by-item response matrix CSV with UTF-8 BOM.
        """
        output = io.StringIO()
        output.write("\ufeff")  # BOM
        writer = csv.writer(output, lineterminator="\n")

        # Header row
        header = ["Candidate_ID"] + question_ids + ["Total_Raw_Score", "Percentage"]
        writer.writerow(header)

        for cid in candidate_ids:
            cand_scores = response_matrix.get(cid, {})
            row = [cid]
            total = 0
            for qid in question_ids:
                sc = cand_scores.get(qid, 0)
                total += sc
                row.append(sc)
            pct = (total / len(question_ids) * 100.0) if question_ids else 0.0
            row.append(total)
            row.append(f"{pct:.2f}%")
            writer.writerow(row)

        return output.getvalue()

    @classmethod
    def export_item_psychometric_csv(cls, items_data: List[Dict[str, Any]]) -> str:
        """
        Exports classical test theory (P-value, Kelley's D, Point-Biserial) table to CSV.
        """
        output = io.StringIO()
        output.write("\ufeff")
        writer = csv.writer(output, lineterminator="\n")

        headers = [
            "Item_ID",
            "Question_Text",
            "Difficulty_P",
            "Discrimination_D",
            "Point_Biserial_R",
            "Domain_Topic",
            "Psychometric_Status"
        ]
        writer.writerow(headers)

        for it in items_data:
            writer.writerow([
                it.get("item_id", ""),
                it.get("question_text", "").replace("\n", " "),
                f"{it.get('difficulty_p', 0.0):.3f}",
                f"{it.get('discrimination_d', 0.0):.3f}",
                f"{it.get('point_biserial', 0.0):.3f}",
                it.get("domain", "General"),
                it.get("status", "VALID")
            ])

        return output.getvalue()
