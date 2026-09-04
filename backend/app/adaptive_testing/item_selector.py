"""
ExamHub Computerized Adaptive Testing - Item Selector & Exposure Controller
Implements Maximum Fisher Information (MFI), Sympson-Hetter exposure control,
and constrained content balancing.
"""

import random
from typing import List, Dict, Optional, Set
from backend.app.adaptive_testing.schemas import CATItemParameter
from backend.app.adaptive_testing.engine import CATEngine


class ItemSelector:
    """
    Selects the next optimal question from the item pool while honoring
    content constraints, item exposure ceilings, and psychometric information efficiency.
    """

    def __init__(self, item_pool: List[CATItemParameter]):
        self.item_pool: List[CATItemParameter] = item_pool
        self.item_map: Dict[str, CATItemParameter] = {it.item_id: it for it in item_pool}
        self.exposure_counts: Dict[str, int] = {it.item_id: 0 for it in item_pool}
        self.total_sessions: int = 0

    def select_next_item(
        self,
        current_theta: float,
        administered_ids: Set[str],
        content_target_percentages: Optional[Dict[str, float]] = None,
        administered_content_counts: Optional[Dict[str, int]] = None,
        exposure_control_rate: float = 0.30
    ) -> Optional[CATItemParameter]:
        """
        Selects the next best item using Maximum Fisher Information with
        content balancing and randomized exposure throttling.
        """
        candidate_items = [
            it for it in self.item_pool
            if it.item_id not in administered_ids
        ]

        if not candidate_items:
            return None

        # Determine if content balancing restricts domain selection
        targeted_domain = None
        if content_target_percentages and administered_content_counts:
            total_administered = sum(administered_content_counts.values())
            if total_administered > 0:
                deficits = {}
                for domain, target_pct in content_target_percentages.items():
                    current_pct = administered_content_counts.get(domain, 0) / total_administered
                    deficits[domain] = target_pct - current_pct
                
                # Pick domain with greatest negative deficit
                most_deficient = max(deficits.items(), key=lambda x: x[1])
                if most_deficient[1] > 0.05:  # Over 5% behind target
                    domain_items = [it for it in candidate_items if it.domain_content == most_deficient[0]]
                    if domain_items:
                        candidate_items = domain_items
                        targeted_domain = most_deficient[0]

        # Calculate Fisher Information for each eligible candidate item at current theta
        item_scores = []
        for item in candidate_items:
            info = CATEngine.fisher_information_3pl(
                theta=current_theta,
                a=item.discrimination_a,
                b=item.difficulty_b,
                c=item.guessing_c
            )
            item_scores.append((item, info))

        # Sort descending by information
        item_scores.sort(key=lambda x: x[1], reverse=True)

        # Sympson-Hetter style exposure throttle:
        # Instead of always taking item 0, select probabilistically from the top-k informative items
        top_k = min(5, len(item_scores))
        top_candidates = item_scores[:top_k]

        # Weight selection by information score
        weights = [max(0.01, score) for _, score in top_candidates]
        selected_item = random.choices(
            population=[item for item, _ in top_candidates],
            weights=weights,
            k=1
        )[0]

        # Update exposure stats
        self.exposure_counts[selected_item.item_id] += 1
        return selected_item

    def get_exposure_rate_report(self) -> Dict[str, float]:
        """
        Returns the observed exposure rate (administration count / total sessions)
        for every item in the pool.
        """
        if self.total_sessions == 0:
            return {item_id: 0.0 for item_id in self.exposure_counts}
        return {
            item_id: round(count / self.total_sessions, 3)
            for item_id, count in self.exposure_counts.items()
        }

    def generate_synthetic_pool(count: int = 100) -> List[CATItemParameter]:
        """
        Generates a balanced synthetic item pool across difficulty and discrimination spectrums.
        """
        pool = []
        domains = ["Mathematics", "Physics", "Computer Science", "Verbal Reasoning"]
        for i in range(1, count + 1):
            # Normal distribution for difficulty b around 0.0 (spread -2.5 to +2.5)
            b = round(random.gauss(0.0, 1.1), 2)
            b = max(-3.0, min(3.0, b))
            # Log-normal or truncated normal for discrimination a (0.7 to 2.2)
            a = round(random.uniform(0.7, 2.0), 2)
            c = 0.25  # 4-option multiple choice guessing
            domain = domains[i % len(domains)]
            pool.append(
                CATItemParameter(
                    item_id=f"CAT-ITEM-{i:04d}",
                    difficulty_b=b,
                    discrimination_a=a,
                    guessing_c=c,
                    domain_content=domain,
                    question_text=f"Adaptive Item #{i:04d} testing core principles of {domain} (Difficulty b={b:+.2f}).",
                    options=[
                        f"Option Alpha: Primary analytical formulation for item {i}",
                        f"Option Beta: Alternative empirical formulation for item {i}",
                        f"Option Gamma: Standard baseline formulation for item {i}",
                        f"Option Delta: Boundary condition formulation for item {i}"
                    ],
                    correct_option_index=i % 4
                )
            )
        return pool
