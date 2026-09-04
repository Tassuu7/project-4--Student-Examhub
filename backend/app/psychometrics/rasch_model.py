"""
ExamHub - Rasch Measurement Model (1PL IRT Engine)
Implements Georg Rasch's simple logistic model for invariant measurement,
Joint Maximum Likelihood Estimation (JMLE), person ability scoring,
and item outfit/infit mean-square statistics.
"""

import math
from typing import List, Dict, Any, Tuple, Optional

class RaschModel:
    """
    Rasch 1-Parameter Logistic (1PL) Model Engine.
    Formula:
    P(X_ni = 1 | theta_n, beta_i) = exp(theta_n - beta_i) / (1 + exp(theta_n - beta_i))
    """

    @staticmethod
    def probability_correct(theta: float, beta: float) -> float:
        """Calculates probability of correct response given person ability theta and item difficulty beta."""
        diff = theta - beta
        # Clamp to avoid numerical overflow in exp
        clamped_diff = max(-35.0, min(35.0, diff))
        return 1.0 / (1.0 + math.exp(-clamped_diff))

    @staticmethod
    def log_odds(theta: float, beta: float) -> float:
        """Log-odds of success (logit): ln(P / (1 - P)) = theta - beta"""
        return theta - beta

    @staticmethod
    def item_information(theta: float, beta: float) -> float:
        """Rasch Item Information Function: I_i(theta) = P_i(theta) * (1 - P_i(theta))"""
        p = RaschModel.probability_correct(theta, beta)
        return p * (1.0 - p)

    @staticmethod
    def test_information(theta: float, item_difficulties: List[float]) -> float:
        """Test Information Function: Sum of item information across all test items."""
        return sum(RaschModel.item_information(theta, b) for b in item_difficulties)

    @staticmethod
    def standard_error_of_measurement(theta: float, item_difficulties: List[float]) -> float:
        """SEM(theta) = 1 / sqrt(Test_Information(theta))"""
        info = RaschModel.test_information(theta, item_difficulties)
        if info <= 0.0001:
            return 9.99
        return 1.0 / math.sqrt(info)

    @staticmethod
    def estimate_person_ability(
        response_vector: List[int],
        item_difficulties: List[float],
        max_iterations: int = 50,
        convergence_threshold: float = 0.001
    ) -> Tuple[float, float, int]:
        """
        Estimates person ability (theta) using Newton-Raphson maximum likelihood iteration.
        Returns (theta_estimate, standard_error, iterations_count).
        """
        n_items = len(item_difficulties)
        raw_score = sum(response_vector)

        # Extreme score adjustments (score of 0 or perfect score)
        if raw_score == 0:
            adjusted_score = 0.5
        elif raw_score == n_items:
            adjusted_score = n_items - 0.5
        else:
            adjusted_score = float(raw_score)

        # Initial ability estimate based on raw score log-odds
        p_initial = adjusted_score / n_items
        theta = math.log(p_initial / (1.0 - p_initial))

        iterations = 0
        for it in range(max_iterations):
            iterations += 1
            # Expected score: E(theta) = sum(P_i(theta))
            expected_score = 0.0
            variance_sum = 0.0

            for b in item_difficulties:
                p = RaschModel.probability_correct(theta, b)
                expected_score += p
                variance_sum += p * (1.0 - p)

            delta = (adjusted_score - expected_score) / (variance_sum if variance_sum > 0.0001 else 0.0001)
            # Damping delta to avoid divergence
            damped_delta = max(-1.5, min(1.5, delta))
            theta += damped_delta

            if abs(delta) < convergence_threshold:
                break

        sem = RaschModel.standard_error_of_measurement(theta, item_difficulties)
        return round(theta, 3), round(sem, 3), iterations

    @staticmethod
    def estimate_item_difficulties_jmle(
        response_matrix: List[List[int]],
        max_iterations: int = 100,
        tolerance: float = 0.01
    ) -> Tuple[List[float], List[float]]:
        """
        Joint Maximum Likelihood Estimation (JMLE) for item difficulties (beta)
        and person abilities (theta).
        response_matrix is shape (N_persons, M_items) with values 0 or 1.
        Returns (item_difficulties, person_abilities).
        """
        n_persons = len(response_matrix)
        if n_persons == 0:
            return [], []

        n_items = len(response_matrix[0])
        if n_items == 0:
            return [], []

        # Center constraint: Sum of item difficulties = 0.0
        betas = [0.0] * n_items
        thetas = [0.0] * n_persons

        for iteration in range(max_iterations):
            max_change = 0.0

            # 1. Update Person Abilities
            for p_idx in range(n_persons):
                resp = response_matrix[p_idx]
                r_score = sum(resp)
                if r_score == 0:
                    r_score = 0.3
                elif r_score == n_items:
                    r_score = n_items - 0.3

                exp_score = sum(RaschModel.probability_correct(thetas[p_idx], betas[i]) for i in range(n_items))
                var_score = sum(RaschModel.item_information(thetas[p_idx], betas[i]) for i in range(n_items))

                if var_score > 0.001:
                    d = (r_score - exp_score) / var_score
                    d_clamped = max(-1.0, min(1.0, d))
                    thetas[p_idx] += d_clamped
                    max_change = max(max_change, abs(d_clamped))

            # 2. Update Item Difficulties
            for i_idx in range(n_items):
                item_score = sum(response_matrix[p][i_idx] for p in range(n_persons))
                if item_score == 0:
                    item_score = 0.3
                elif item_score == n_persons:
                    item_score = n_persons - 0.3

                exp_item_score = sum(RaschModel.probability_correct(thetas[p], betas[i_idx]) for p in range(n_persons))
                var_item_score = sum(RaschModel.item_information(thetas[p], betas[i_idx]) for p in range(n_persons))

                if var_item_score > 0.001:
                    d_b = (exp_item_score - item_score) / var_item_score
                    d_b_clamped = max(-1.0, min(1.0, d_b))
                    betas[i_idx] += d_b_clamped
                    max_change = max(max_change, abs(d_b_clamped))

            # Center betas to maintain origin at 0.0 logits
            mean_beta = sum(betas) / n_items
            betas = [b - mean_beta for b in betas]

            if max_change < tolerance:
                break

        rounded_betas = [round(b, 3) for b in betas]
        rounded_thetas = [round(t, 3) for t in thetas]
        return rounded_betas, rounded_thetas

    @staticmethod
    def calculate_item_fit_statistics(
        response_matrix: List[List[int]],
        thetas: List[float],
        betas: List[float]
    ) -> List[Dict[str, Any]]:
        """
        Computes Outfit and Infit Mean Square (MNSQ) statistics per item.
        Expected MNSQ is 1.0. Values > 1.4 indicate noise/unidimensionality violation.
        Values < 0.6 indicate item redundancy.
        """
        n_persons = len(response_matrix)
        n_items = len(betas)

        fit_results = []

        for i in range(n_items):
            b = betas[i]
            sum_std_residual_sq = 0.0
            sum_variance = 0.0
            sum_raw_residual_sq = 0.0

            for p in range(n_persons):
                observed = float(response_matrix[p][i])
                expected = RaschModel.probability_correct(thetas[p], b)
                variance = expected * (1.0 - expected)

                residual = observed - expected
                sum_raw_residual_sq += residual ** 2

                if variance > 0.0001:
                    std_res_sq = (residual ** 2) / variance
                    sum_std_residual_sq += std_res_sq
                    sum_variance += variance

            # Outfit MNSQ: Unweighted average of standardized residuals squared
            outfit_mnsq = (sum_std_residual_sq / n_persons) if n_persons > 0 else 1.0

            # Infit MNSQ: Information-weighted average of standardized residuals squared
            infit_mnsq = (sum_raw_residual_sq / sum_variance) if sum_variance > 0 else 1.0

            if 0.7 <= infit_mnsq <= 1.3:
                fit_category = "Productive for Measurement"
            elif 0.5 <= infit_mnsq < 0.7 or 1.3 < infit_mnsq <= 1.5:
                fit_category = "Acceptable"
            elif infit_mnsq > 1.5:
                fit_category = "Distorting / Misfit"
            else:
                fit_category = "Overfit / Redundant"

            fit_results.append({
                "item_index": i + 1,
                "difficulty_beta": b,
                "outfit_mnsq": round(outfit_mnsq, 3),
                "infit_mnsq": round(infit_mnsq, 3),
                "fit_status": fit_category
            })

        return fit_results

    @staticmethod
    def generate_icc_curve_points(beta: float, points_count: int = 50) -> List[Dict[str, float]]:
        """Generates coordinate points for rendering Item Characteristic Curve from -4 to +4 logits."""
        points = []
        step = 8.0 / (points_count - 1)
        for i in range(points_count):
            theta = -4.0 + (i * step)
            prob = RaschModel.probability_correct(theta, beta)
            points.append({
                "theta": round(theta, 2),
                "probability": round(prob, 4)
            })
        return points
