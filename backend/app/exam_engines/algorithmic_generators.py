"""
ExamHub Algorithmic Question Generator Engine
Generates randomized STEM questions with parametric variable constraints,
exact analytical solutions, and LaTeX mathematical stems.
"""

import math
import random
from typing import List, Dict, Any, Tuple
from pydantic import BaseModel


class GeneratedParametricQuestion(BaseModel):
    problem_id: str
    subject_domain: str
    problem_title: str
    latex_stem: str
    parameters: Dict[str, Any]
    numerical_answer: float
    tolerance: float = 0.02
    unit: str
    step_by_step_solution_latex: str


class STEMAlgorithmicGenerators:
    """
    Parametric problem generators for STEM examinations.
    Ensures every candidate receives mathematically distinct problem variants with identical difficulty.
    """

    @classmethod
    def generate_linear_circuit_thevenin(cls, seed: Optional[int] = None) -> GeneratedParametricQuestion:
        """
        Generates Thevenin Equivalent Voltage and Resistance for a DC circuit.
        """
        rng = random.Random(seed)
        v_source = rng.choice([12, 18, 24, 36, 48])
        r1 = rng.choice([2, 4, 6, 8, 10])
        r2 = rng.choice([3, 5, 6, 12, 15])
        r_load = rng.choice([4, 8, 10, 12])

        # Voltage divider: V_th = V_s * (R2 / (R1 + R2))
        v_th = v_source * (r2 / (r1 + r2))
        # Parallel resistance: R_th = (R1 * R2) / (R1 + R2)
        r_th = (r1 * r2) / (r1 + r2)

        latex_stem = (
            f"Consider a DC resistive network powered by independent DC source $V_s = {v_source}\\,\\text{{V}}$ "
            f"in series with resistor $R_1 = {r1}\\,\\Omega$ and shunt resistor $R_2 = {r2}\\,\\Omega$. "
            f"Determine the open-circuit Thevenin equivalent voltage $V_{{th}}$ observed across the output terminals."
        )

        solution = (
            f"By application of the voltage divider rule across the open terminals:\n"
            f"$$V_{{th}} = V_s \\left( \\frac{{R_2}}{{R_1 + R_2}} \\right) = {v_source} \\left( \\frac{{{r2}}}{{{r1} + {r2}}} \\right) = {v_th:.2f}\\,\\text{{V}}$$"
        )

        return GeneratedParametricQuestion(
            problem_id=f"CIRC-THV-{rng.randint(1000, 9999)}",
            subject_domain="Electrical Engineering",
            problem_title="Thevenin Equivalent Voltage Calculation",
            latex_stem=latex_stem,
            parameters={"Vs": v_source, "R1": r1, "R2": r2, "R_load": r_load},
            numerical_answer=round(v_th, 2),
            tolerance=0.02,
            unit="V",
            step_by_step_solution_latex=solution
        )

    @classmethod
    def generate_calculus_definite_integral(cls, seed: Optional[int] = None) -> GeneratedParametricQuestion:
        """
        Generates polynomial definite integral: Integral from 0 to B of (a*x^2 + b*x + c) dx
        """
        rng = random.Random(seed)
        a = rng.randint(1, 6) * 3  # Multiple of 3 for integer integration
        b = rng.randint(1, 6) * 2  # Multiple of 2 for integer integration
        c = rng.randint(1, 10)
        upper_bound = rng.randint(1, 4)

        # Integral = [ (a/3)*x^3 + (b/2)*x^2 + c*x ] from 0 to upper_bound
        val = (a / 3) * (upper_bound ** 3) + (b / 2) * (upper_bound ** 2) + c * upper_bound

        latex_stem = (
            f"Evaluate the definite integral:\n"
            f"$$\\int_{{0}}^{{{upper_bound}}} ({a}x^2 + {b}x + {c}) \\, dx$$"
        )

        solution = (
            f"Integrating term-by-term using the power rule:\n"
            f"$$\\left[ \\frac{{{a}}}{{3}}x^3 + \\frac{{{b}}}{{2}}x^2 + {c}x \\right]_0^{{{upper_bound}}} = "
            f"\\left( {int(a/3)}({upper_bound})^3 + {int(b/2)}({upper_bound})^2 + {c}({upper_bound}) \\right) = {val:.1f}$$"
        )

        return GeneratedParametricQuestion(
            problem_id=f"CALC-INT-{rng.randint(1000, 9999)}",
            subject_domain="Mathematics",
            problem_title="Definite Integral Evaluation",
            latex_stem=latex_stem,
            parameters={"a": a, "b": b, "c": c, "upper_limit": upper_bound},
            numerical_answer=round(val, 2),
            tolerance=0.01,
            unit="",
            step_by_step_solution_latex=solution
        )

    @classmethod
    def generate_network_bandwidth_delay_product(cls, seed: Optional[int] = None) -> GeneratedParametricQuestion:
        """
        Generates Bandwidth-Delay Product (BDP) problem for TCP buffer sizing.
        """
        rng = random.Random(seed)
        bandwidth_mbps = rng.choice([100, 250, 500, 1000])  # Mbps
        rtt_ms = rng.choice([20, 40, 60, 80, 120])           # ms

        # BDP bits = Bandwidth (bps) * RTT (sec)
        # BDP bytes = (bandwidth_mbps * 1e6 * (rtt_ms / 1000)) / 8
        bdp_bytes = (bandwidth_mbps * 1_000_000 * (rtt_ms / 1000.0)) / 8.0
        bdp_kb = bdp_bytes / 1000.0

        latex_stem = (
            f"A high-speed WAN connection provides a bottleneck bandwidth of $C = {bandwidth_mbps}\\,\\text{{Mbps}}$ "
            f"with a two-way round-trip propagation time of $\\text{{RTT}} = {rtt_ms}\\,\\text{{ms}}$. "
            f"Calculate the Bandwidth-Delay Product (BDP) in kilobytes (KB) required to fully saturate the link."
        )

        solution = (
            f"$$\\text{{BDP}} = \\frac{{\\text{{Bandwidth}} \\times \\text{{RTT}}}}{{8}} = "
            f"\\frac{{{bandwidth_mbps} \\times 10^6 \\times ({rtt_ms} \\times 10^{{-3}})}}{{8}} = {bdp_bytes:,.0f}\\,\\text{{bytes}} = {bdp_kb:.1f}\\,\\text{{KB}}$$"
        )

        return GeneratedParametricQuestion(
            problem_id=f"NET-BDP-{rng.randint(1000, 9999)}",
            subject_domain="Computer Networks",
            problem_title="Bandwidth-Delay Product (BDP) Sizing",
            latex_stem=latex_stem,
            parameters={"bandwidth_mbps": bandwidth_mbps, "rtt_ms": rtt_ms},
            numerical_answer=round(bdp_kb, 1),
            tolerance=0.03,
            unit="KB",
            step_by_step_solution_latex=solution
        )

    @classmethod
    def generate_harmonic_oscillator_frequency(cls, seed: Optional[int] = None) -> GeneratedParametricQuestion:
        """
        Physics harmonic oscillator: f = (1 / 2pi) * sqrt(k / m)
        """
        rng = random.Random(seed)
        mass_kg = rng.choice([0.5, 1.0, 2.0, 4.0, 5.0])
        k_spring = rng.choice([50, 100, 200, 400, 500])  # N/m

        omega = math.sqrt(k_spring / mass_kg)
        freq_hz = omega / (2.0 * math.pi)

        latex_stem = (
            f"An undamped linear spring-mass system consists of mass $m = {mass_kg}\\,\\text{{kg}}$ attached "
            f"to an ideal spring of stiffness $k = {k_spring}\\,\\text{{N/m}}$. "
            f"Determine the natural cyclic frequency of oscillation $f$ in Hertz (Hz)."
        )

        solution = (
            f"The angular natural frequency is given by $\\omega_n = \\sqrt{{k / m}} = \\sqrt{{{k_spring} / {mass_kg}}} = {omega:.2f}\\,\\text{{rad/s}}$.\n"
            f"The cyclic frequency is:\n"
            f"$$f = \\frac{{\\omega_n}}{{2\\pi}} = \\frac{{{omega:.2f}}}{{2\\pi}} = {freq_hz:.2f}\\,\\text{{Hz}}$$"
        )

        return GeneratedParametricQuestion(
            problem_id=f"PHYS-OSC-{rng.randint(1000, 9999)}",
            subject_domain="Applied Physics",
            problem_title="Natural Frequency of Harmonic Oscillator",
            latex_stem=latex_stem,
            parameters={"mass_kg": mass_kg, "k_spring": k_spring},
            numerical_answer=round(freq_hz, 2),
            tolerance=0.02,
            unit="Hz",
            step_by_step_solution_latex=solution
        )
