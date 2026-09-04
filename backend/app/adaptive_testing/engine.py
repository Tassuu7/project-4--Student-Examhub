"""
ExamHub Computerized Adaptive Testing (CAT) Engine
Implements Item Response Theory (IRT) probability functions, Fisher Information,
Expected A Posteriori (EAP) Bayesian estimation, and Maximum Likelihood (MLE).
"""

import math
from typing import List, Tuple, Optional
from backend.app.adaptive_testing.schemas import (
    CATItemParameter,
    CandidateResponseRecord,
    AbilityEstimationMethod,
)


class CATEngine:
    """
    Core psychometric mathematics engine for Computerized Adaptive Testing.
    Supports 1PL, 2PL, and 3PL logistic IRT models with quadrature-based
    EAP ability estimation and Newton-Raphson MLE.
    """

    QUADRATURE_POINTS: int = 61
    THETA_MIN: float = -4.0
    THETA_MAX: float = 4.0
    DEFAULT_SCALING_D: float = 1.702  # Logistic to normal metric scaling factor

    @classmethod
    def probability_3pl(
        cls,
        theta: float,
        a: float,
        b: float,
        c: float,
        d_scale: float = DEFAULT_SCALING_D
    ) -> float:
        """
        Calculate 3PL probability of correct response given candidate ability theta:
        P(theta) = c + (1 - c) / (1 + exp(-D * a * (theta - b)))
        """
        logit = d_scale * a * (theta - b)
        # Numerical stability clamp
        if logit > 35.0:
            return 1.0
        elif logit < -35.0:
            return c
        exp_val = math.exp(-logit)
        return c + (1.0 - c) / (1.0 + exp_val)

    @classmethod
    def fisher_information_3pl(
        cls,
        theta: float,
        a: float,
        b: float,
        c: float,
        d_scale: float = DEFAULT_SCALING_D
    ) -> float:
        """
        Calculate Fisher Information for an item at ability level theta:
        I(theta) = (D^2 * a^2 * (P(theta) - c)^2 * Q(theta)) / ((1 - c)^2 * P(theta))
        where Q(theta) = 1 - P(theta)
        """
        p = cls.probability_3pl(theta, a, b, c, d_scale)
        q = 1.0 - p

        if p <= c or p <= 0.0 or q <= 0.0:
            return 1e-6

        numerator = (d_scale ** 2) * (a ** 2) * ((p - c) ** 2) * q
        denominator = ((1.0 - c) ** 2) * p

        if denominator <= 0.0:
            return 1e-6

        return max(1e-6, numerator / denominator)

    @classmethod
    def test_information(
        cls,
        theta: float,
        administered_items: List[Tuple[float, float, float]]
    ) -> float:
        """
        Calculate total test information for a set of administered items (a, b, c).
        """
        info_sum = 0.0
        for a, b, c in administered_items:
            info_sum += cls.fisher_information_3pl(theta, a, b, c)
        return info_sum

    @classmethod
    def standard_error_of_measurement(
        cls,
        theta: float,
        administered_items: List[Tuple[float, float, float]]
    ) -> float:
        """
        Calculate SEM = 1 / sqrt(Test Information).
        """
        if not administered_items:
            return 1.0
        total_info = cls.test_information(theta, administered_items)
        if total_info <= 1e-5:
            return 2.5
        return 1.0 / math.sqrt(total_info)

    @classmethod
    def _generate_quadrature_grid(cls) -> List[Tuple[float, float]]:
        """
        Generate quadrature nodes and standard normal prior weights N(0, 1).
        Returns list of (node, weight) pairs.
        """
        step = (cls.THETA_MAX - cls.THETA_MIN) / (cls.QUADRATURE_POINTS - 1)
        grid = []
        weight_sum = 0.0

        for i in range(cls.QUADRATURE_POINTS):
            x = cls.THETA_MIN + i * step
            # Standard normal density: 1 / sqrt(2*pi) * exp(-x^2 / 2)
            density = (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * (x ** 2))
            grid.append((x, density))
            weight_sum += density

        # Normalize weights
        normalized = [(x, w / weight_sum) for x, w in grid]
        return normalized

    @classmethod
    def estimate_theta_eap(
        cls,
        responses: List[CandidateResponseRecord]
    ) -> Tuple[float, float]:
        """
        Estimate candidate ability theta using Bayesian Expected A Posteriori (EAP).
        Returns (theta_estimate, posterior_standard_deviation).
        """
        if not responses:
            return 0.0, 1.0

        grid = cls._generate_quadrature_grid()
        posterior_numerators = []
        posterior_denominators = []

        for x_k, w_k in grid:
            likelihood = 1.0
            for resp in responses:
                p_i = cls.probability_3pl(x_k, resp.discrimination_a, resp.difficulty_b, resp.guessing_c)
                if resp.is_correct:
                    likelihood *= max(1e-12, p_i)
                else:
                    likelihood *= max(1e-12, 1.0 - p_i)

            posterior_numerators.append(x_k * likelihood * w_k)
            posterior_denominators.append(likelihood * w_k)

        sum_denom = sum(posterior_denominators)
        if sum_denom <= 1e-15:
            # Fallback to mean difficulty of correct vs incorrect items
            correct_b = [r.difficulty_b for r in responses if r.is_correct]
            if correct_b:
                return min(cls.THETA_MAX, max(cls.THETA_MIN, sum(correct_b) / len(correct_b))), 0.5
            return 0.0, 1.0

        theta_eap = sum(posterior_numerators) / sum_denom

        # Compute posterior variance
        variance_numerator = sum(((x_k - theta_eap) ** 2) * denom for (x_k, _), denom in zip(grid, posterior_denominators))
        posterior_variance = variance_numerator / sum_denom
        posterior_sd = math.sqrt(max(1e-6, posterior_variance))

        theta_eap = max(cls.THETA_MIN, min(cls.THETA_MAX, theta_eap))
        return round(theta_eap, 4), round(posterior_sd, 4)

    @classmethod
    def estimate_theta_mle(
        cls,
        responses: List[CandidateResponseRecord],
        initial_theta: float = 0.0,
        max_iterations: int = 25,
        convergence_epsilon: float = 0.001
    ) -> Tuple[float, float]:
        """
        Estimate candidate ability using Newton-Raphson Maximum Likelihood Estimation (MLE).
        If all responses are correct or all incorrect, falls back to EAP.
        """
        num_correct = sum(1 for r in responses if r.is_correct)
        if num_correct == 0 or num_correct == len(responses):
            return cls.estimate_theta_eap(responses)

        theta = initial_theta
        items_tuple = [(r.discrimination_a, r.difficulty_b, r.guessing_c) for r in responses]

        for _ in range(max_iterations):
            first_derivative = 0.0
            second_derivative = 0.0

            for resp in responses:
                a = resp.discrimination_a
                b = resp.difficulty_b
                c = resp.guessing_c
                p = cls.probability_3pl(theta, a, b, c)
                q = 1.0 - p
                u = 1.0 if resp.is_correct else 0.0

                if p <= c or p >= 1.0:
                    continue

                d_logit = cls.DEFAULT_SCALING_D * a
                dp_dtheta = d_logit * ((p - c) / (1.0 - c)) * q

                # Score function
                score = (u - p) / (p * q) * dp_dtheta
                first_derivative += score

                # Expected information for Fisher scoring
                second_derivative -= cls.fisher_information_3pl(theta, a, b, c)

            if abs(second_derivative) < 1e-6:
                break

            delta = -first_derivative / second_derivative
            # Damped Newton step to prevent wild oscillation
            delta = max(-1.0, min(1.0, delta))
            theta += delta

            if abs(delta) < convergence_epsilon:
                break

        theta = max(cls.THETA_MIN, min(cls.THETA_MAX, theta))
        sem = cls.standard_error_of_measurement(theta, items_tuple)
        return round(theta, 4), round(sem, 4)

    @classmethod
    def normal_cdf(cls, x: float) -> float:
        """
        Standard normal cumulative distribution function (error function approximation).
        """
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

    @classmethod
    def theta_to_percentile(cls, theta: float) -> float:
        """
        Convert logit theta into percentile rank (0 to 100).
        """
        pct = cls.normal_cdf(theta) * 100.0
        return round(max(0.1, min(99.9, pct)), 1)
