"""
ExamHub Multidimensional Item Response Theory (MIRT) Engine
Implements compensatory and non-compensatory multidimensional logistic models (M2PL / M3PL),
multidimensional Fisher information matrices, and vector theta EAP estimation.
"""

import math
from typing import List, Tuple, Dict, Optional
from pydantic import BaseModel, Field


class MIRTItemParameter(BaseModel):
    item_id: str
    dimensions_count: int = 2
    a_vector: List[float] = Field(..., description="Vector of discrimination parameters [a_1, a_2, ...]")
    intercept_d: float = Field(..., description="Scalar intercept parameter d = -sum(a_k * b_k)")
    guessing_c: float = Field(default=0.0, ge=0.0, le=0.5)


class MIRTCandidateResponse(BaseModel):
    item_id: str
    is_correct: bool
    a_vector: List[float]
    intercept_d: float
    guessing_c: float


class MIRTEstimateResult(BaseModel):
    candidate_id: str
    estimated_theta_vector: List[float]
    standard_errors: List[float]
    covariance_matrix: List[List[float]]
    generalized_variance: float


class MIRTEngine:
    """
    Evaluates tests measuring multiple correlated latent traits simultaneously
    (e.g., Quantitative Ability + Spatial Reasoning + Verbal Logic).
    """

    @classmethod
    def probability_compensatory(
        cls,
        theta_vector: List[float],
        a_vector: List[float],
        intercept_d: float,
        guessing_c: float = 0.0
    ) -> float:
        """
        Multidimensional compensatory logistic model:
        P(theta) = c + (1 - c) / (1 + exp(-(a^T * theta + d)))
        """
        linear_combination = sum(a * th for a, th in zip(a_vector, theta_vector)) + intercept_d

        if linear_combination > 35.0:
            return 1.0
        elif linear_combination < -35.0:
            return guessing_c

        exp_val = math.exp(-linear_combination)
        return guessing_c + (1.0 - guessing_c) / (1.0 + exp_val)

    @classmethod
    def probability_non_compensatory(
        cls,
        theta_vector: List[float],
        a_vector: List[float],
        b_vector: List[float],
        guessing_c: float = 0.0
    ) -> float:
        """
        Partially compensatory (multiplicative) model where high ability in one trait
        cannot compensate for deficit in another.
        P(theta) = c + (1 - c) * Prod_k [ 1 / (1 + exp(-a_k * (theta_k - b_k))) ]
        """
        prod = 1.0
        for th, a, b in zip(theta_vector, a_vector, b_vector):
            logit = a * (th - b)
            if logit < -35.0:
                p_k = 0.0
            elif logit > 35.0:
                p_k = 1.0
            else:
                p_k = 1.0 / (1.0 + math.exp(-logit))
            prod *= p_k

        return guessing_c + (1.0 - guessing_c) * prod

    @classmethod
    def fisher_information_matrix(
        cls,
        theta_vector: List[float],
        a_vector: List[float],
        intercept_d: float,
        guessing_c: float = 0.0
    ) -> List[List[float]]:
        """
        Computes K x K information matrix for item i at theta vector:
        I(theta) = a * a^T * [ (P - c)^2 * Q / ((1 - c)^2 * P) ]
        """
        K = len(theta_vector)
        p = cls.probability_compensatory(theta_vector, a_vector, intercept_d, guessing_c)
        q = 1.0 - p

        if p <= guessing_c or p <= 0.0 or q <= 0.0:
            scalar = 1e-6
        else:
            num = ((p - guessing_c) ** 2) * q
            den = ((1.0 - guessing_c) ** 2) * p
            scalar = max(1e-6, num / max(1e-9, den))

        matrix = [[0.0 for _ in range(K)] for _ in range(K)]
        for i in range(K):
            for j in range(K):
                matrix[i][j] = a_vector[i] * a_vector[j] * scalar

        return matrix

    @classmethod
    def estimate_vector_eap_2d(
        cls,
        responses: List[MIRTCandidateResponse],
        grid_points_per_dim: int = 21,
        theta_range: Tuple[float, float] = (-3.0, 3.0)
    ) -> Tuple[List[float], List[float]]:
        """
        2-Dimensional quadrature grid integration for bivariate EAP estimation.
        Returns: (estimated_theta_vector, standard_error_vector)
        """
        step = (theta_range[1] - theta_range[0]) / (grid_points_per_dim - 1)
        nodes = [theta_range[0] + i * step for i in range(grid_points_per_dim)]

        # Bivariate standard normal prior density: (1/(2*pi)) * exp(-(x^2 + y^2)/2)
        total_likelihood_sum = 0.0
        weighted_theta1_sum = 0.0
        weighted_theta2_sum = 0.0
        weighted_theta1_sq_sum = 0.0
        weighted_theta2_sq_sum = 0.0

        for x in nodes:
            for y in nodes:
                prior_density = (1.0 / (2.0 * math.pi)) * math.exp(-0.5 * (x * x + y * y))

                # Compute likelihood
                likelihood = 1.0
                for resp in responses:
                    p = cls.probability_compensatory([x, y], resp.a_vector, resp.intercept_d, resp.guessing_c)
                    if resp.is_correct:
                        likelihood *= max(1e-12, p)
                    else:
                        likelihood *= max(1e-12, 1.0 - p)

                joint = likelihood * prior_density
                total_likelihood_sum += joint
                weighted_theta1_sum += x * joint
                weighted_theta2_sum += y * joint
                weighted_theta1_sq_sum += (x * x) * joint
                weighted_theta2_sq_sum += (y * y) * joint

        if total_likelihood_sum <= 1e-15:
            return [0.0, 0.0], [1.0, 1.0]

        eap_th1 = weighted_theta1_sum / total_likelihood_sum
        eap_th2 = weighted_theta2_sum / total_likelihood_sum

        var_th1 = max(1e-6, (weighted_theta1_sq_sum / total_likelihood_sum) - (eap_th1 ** 2))
        var_th2 = max(1e-6, (weighted_theta2_sq_sum / total_likelihood_sum) - (eap_th2 ** 2))

        sem_th1 = math.sqrt(var_th1)
        sem_th2 = math.sqrt(var_th2)

        return [round(eap_th1, 3), round(eap_th2, 3)], [round(sem_th1, 3), round(sem_th2, 3)]
