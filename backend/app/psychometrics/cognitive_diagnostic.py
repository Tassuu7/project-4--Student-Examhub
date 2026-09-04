"""
ExamHub - Cognitive Diagnostic Modeling (CDM) Engine
Implements the Deterministic Input, Noisy "And" (DINA) model to infer student skill mastery
vectors across multi-attribute curriculum Q-matrices.
"""

from typing import List, Dict, Any, Tuple
import math

class CognitiveDiagnosticEngine:
    """Evaluates multi-attribute skill profiles using Q-matrix DINA models."""

    @staticmethod
    def calculate_dina_probability(
        skill_vector: List[int],  # e.g., [1, 1, 0] for student's possession of skills 1, 2, 3
        q_item_vector: List[int], # e.g., [1, 0, 0] skills required for item j
        slipping_s: float = 0.10,
        guessing_g: float = 0.20
    ) -> float:
        """
        DINA ideal response: eta_ij = prod_{k=1}^K (alpha_{ik} ^ q_{jk})
        If student has ALL required skills for item j: eta_ij = 1, P = 1 - s_j
        If student lacks ANY required skill:          eta_ij = 0, P = g_j
        """
        has_all_required = True
        for k in range(len(q_item_vector)):
            if q_item_vector[k] == 1 and skill_vector[k] == 0:
                has_all_required = False
                break

        if has_all_required:
            return 1.0 - slipping_s
        else:
            return guessing_g

    @staticmethod
    def estimate_skill_profile(
        student_responses: List[int],
        q_matrix: List[List[int]],
        skill_names: List[str]
    ) -> Dict[str, Any]:
        """
        Finds the most likely latent skill mastery profile alpha in {0, 1}^K
        maximizing likelihood: L(Y | alpha) = prod_j P_j(alpha)^Y_j * (1 - P_j(alpha))^(1 - Y_j)
        """
        k_skills = len(skill_names)
        num_profiles = 1 << k_skills  # 2^K profiles

        best_profile = [0] * k_skills
        max_log_likelihood = -1e12

        for p_idx in range(num_profiles):
            profile = [(p_idx >> bit) & 1 for bit in range(k_skills)]

            log_like = 0.0
            for j in range(len(student_responses)):
                p_correct = CognitiveDiagnosticEngine.calculate_dina_probability(
                    skill_vector=profile,
                    q_item_vector=q_matrix[j]
                )
                y_j = student_responses[j]
                if y_j == 1:
                    log_like += math.log(max(1e-10, p_correct))
                else:
                    log_like += math.log(max(1e-10, 1.0 - p_correct))

            if log_like > max_log_likelihood:
                max_log_likelihood = log_like
                best_profile = profile

        mastered_skills = [skill_names[idx] for idx, v in enumerate(best_profile) if v == 1]
        deficient_skills = [skill_names[idx] for idx, v in enumerate(best_profile) if v == 0]

        return {
            "mastered_skills": mastered_skills,
            "deficient_skills": deficient_skills,
            "mastery_rate": round(len(mastered_skills) / k_skills * 100.0, 1),
            "log_likelihood": round(max_log_likelihood, 3),
            "skill_vector": best_profile
        }
