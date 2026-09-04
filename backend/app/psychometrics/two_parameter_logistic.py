"""
ExamHub - 2-Parameter Logistic (2PL) IRT Engine
Implements Birnbaum's 2PL model incorporating item discrimination (a)
and item difficulty (b) with Fisher information functions.
"""

import math
from typing import List, Dict, Any, Tuple, Optional

class TwoParameterLogisticModel:
    """
    Birnbaum 2PL IRT Model:
    P(theta) = 1 / (1 + exp(-D * a * (theta - b)))
    D = 1.702 scaling factor matching normal ogive metric.
    """

    SCALING_D = 1.702

    @staticmethod
    def probability(theta: float, a: float, b: float) -> float:
        """
        Probability of correct response.
        a: discrimination parameter (typically 0.5 to 2.5)
        b: difficulty parameter (typically -3.0 to +3.0)
        """
        exponent = -TwoParameterLogisticModel.SCALING_D * a * (theta - b)
        exponent_clamped = max(-35.0, min(35.0, exponent))
        return 1.0 / (1.0 + math.exp(exponent_clamped))

    @staticmethod
    def item_information(theta: float, a: float, b: float) -> float:
        """
        Fisher Item Information function for 2PL:
        I(theta) = D^2 * a^2 * P(theta) * (1 - P(theta))
        Higher discrimination produces sharp, concentrated measurement precision near theta = b.
        """
        p = TwoParameterLogisticModel.probability(theta, a, b)
        q = 1.0 - p
        d = TwoParameterLogisticModel.SCALING_D
        return (d ** 2) * (a ** 2) * p * q

    @staticmethod
    def test_information_profile(
        thetas: List[float],
        items: List[Tuple[float, float]]  # List of (a, b) tuples
    ) -> List[Dict[str, float]]:
        """Calculates test information across ability grid."""
        profile = []
        for theta in thetas:
            total_info = sum(
                TwoParameterLogisticModel.item_information(theta, a, b)
                for a, b in items
            )
            sem = 1.0 / math.sqrt(total_info) if total_info > 0.001 else 9.99
            profile.append({
                "theta": round(theta, 2),
                "information": round(total_info, 3),
                "sem": round(sem, 3)
            })
        return profile

    @staticmethod
    def estimate_person_ability_eap(
        response_vector: List[int],
        items: List[Tuple[float, float]],
        prior_mean: float = 0.0,
        prior_std: float = 1.0,
        quadrature_points: int = 41
    ) -> Tuple[float, float]:
        """
        Expected A Posteriori (EAP) Bayesian ability estimation.
        EAP is robust against non-convergence and extreme scores.
        """
        # Quadrature grid from -4 to +4
        step = 8.0 / (quadrature_points - 1)
        grid_thetas = [-4.0 + (i * step) for i in range(quadrature_points)]

        # Normal prior weights
        prior_weights = []
        for th in grid_thetas:
            w = (1.0 / (prior_std * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((th - prior_mean) / prior_std) ** 2)
            prior_weights.append(w)

        # Compute likelihood for each quadrature point
        posteriors = []
        for idx, th in enumerate(grid_thetas):
            likelihood = 1.0
            for item_idx, (a, b) in enumerate(items):
                p = TwoParameterLogisticModel.probability(th, a, b)
                resp = response_vector[item_idx]
                p_item = p if resp == 1 else (1.0 - p)
                likelihood *= max(1e-12, p_item)

            posterior = likelihood * prior_weights[idx]
            posteriors.append(posterior)

        total_posterior = sum(posteriors)
        if total_posterior <= 0.0:
            return 0.0, 1.0

        # EAP Mean: sum(theta * posterior) / sum(posterior)
        eap_mean = sum(grid_thetas[i] * posteriors[i] for i in range(quadrature_points)) / total_posterior

        # EAP Variance: sum((theta - mean)^2 * posterior) / sum(posterior)
        eap_var = sum(((grid_thetas[i] - eap_mean) ** 2) * posteriors[i] for i in range(quadrature_points)) / total_posterior
        eap_sem = math.sqrt(max(0.001, eap_var))

        return round(eap_mean, 3), round(eap_sem, 3)
