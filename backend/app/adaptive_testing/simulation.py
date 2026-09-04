"""
ExamHub Computerized Adaptive Testing - Monte Carlo Simulator
Simulates adaptive examination administration across synthetic populations
to evaluate stopping rules, measurement precision, test length efficiency, and bias.
"""

import math
import random
from typing import List, Dict
from backend.app.adaptive_testing.schemas import (
    CATSessionConfig,
    CATSimulationResult,
    CandidateResponseRecord,
    StoppingRuleType,
    AbilityEstimationMethod,
)
from backend.app.adaptive_testing.engine import CATEngine
from backend.app.adaptive_testing.item_selector import ItemSelector


class CATSimulator:
    """
    Runs multi-trial Monte Carlo simulations to assess CAT psychometric integrity
    prior to live candidate deployment.
    """

    @classmethod
    def run_simulation(
        cls,
        true_theta: float,
        trials_count: int = 100,
        pool_size: int = 120,
        config: Optional[CATSessionConfig] = None
    ) -> CATSimulationResult:
        if config is None:
            config = CATSessionConfig()

        pool = ItemSelector.generate_synthetic_pool(pool_size)
        selector = ItemSelector(pool)

        estimated_thetas = []
        test_lengths = []
        final_sems = []

        for trial in range(trials_count):
            current_theta = config.initial_theta
            current_sem = 1.0
            administered_ids = set()
            responses: List[CandidateResponseRecord] = []

            for step in range(1, config.max_items + 1):
                item = selector.select_next_item(
                    current_theta=current_theta,
                    administered_ids=administered_ids,
                    exposure_control_rate=config.exposure_control_rate
                )
                if not item:
                    break

                administered_ids.add(item.item_id)

                # Simulate true response probability
                p_success = CATEngine.probability_3pl(
                    theta=true_theta,
                    a=item.discrimination_a,
                    b=item.difficulty_b,
                    c=item.guessing_c
                )
                is_correct = random.random() < p_success

                # Prior ability
                theta_prior = current_theta

                # Create record
                record = CandidateResponseRecord(
                    step_number=step,
                    item_id=item.item_id,
                    selected_option_index=item.correct_option_index if is_correct else (item.correct_option_index + 1) % 4,
                    is_correct=is_correct,
                    response_time_seconds=round(random.uniform(20.0, 90.0), 1),
                    difficulty_b=item.difficulty_b,
                    discrimination_a=item.discrimination_a,
                    guessing_c=item.guessing_c,
                    theta_prior=theta_prior,
                    theta_post=0.0,
                    sem_post=0.0
                )
                responses.append(record)

                # Re-estimate ability
                if config.estimation_method == AbilityEstimationMethod.EAP:
                    new_theta, new_sem = CATEngine.estimate_theta_eap(responses)
                else:
                    new_theta, new_sem = CATEngine.estimate_theta_mle(responses, initial_theta=current_theta)

                current_theta = new_theta
                current_sem = new_sem
                record.theta_post = new_theta
                record.sem_post = new_sem

                # Check stopping rules
                should_stop = False
                if step >= config.min_items:
                    if config.stopping_rule == StoppingRuleType.SEM_THRESHOLD:
                        if current_sem <= config.target_sem:
                            should_stop = True
                    elif config.stopping_rule == StoppingRuleType.COMBINED:
                        if current_sem <= config.target_sem or step >= config.max_items:
                            should_stop = True

                if should_stop or step >= config.max_items:
                    break

            estimated_thetas.append(current_theta)
            test_lengths.append(len(responses))
            final_sems.append(current_sem)

        mean_est = sum(estimated_thetas) / len(estimated_thetas)
        bias = mean_est - true_theta
        squared_errors = [(est - true_theta) ** 2 for est in estimated_thetas]
        rmse = math.sqrt(sum(squared_errors) / len(squared_errors))
        mean_len = sum(test_lengths) / len(test_lengths)
        mean_sem = sum(final_sems) / len(final_sems)

        return CATSimulationResult(
            simulations_count=trials_count,
            true_theta=true_theta,
            mean_estimated_theta=round(mean_est, 3),
            bias=round(bias, 3),
            root_mean_squared_error=round(rmse, 3),
            mean_test_length=round(mean_len, 1),
            mean_sem=round(mean_sem, 3)
        )
