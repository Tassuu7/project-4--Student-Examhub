"""
ExamHub Curriculum Competency Framework
Defines comprehensive hierarchical competency taxonomies, Bloom's revised cognitive levels,
and prerequisite dependency graphs for multi-disciplinary accreditation.
"""

from typing import List, Dict, Set, Optional
from pydantic import BaseModel, Field
from enum import Enum


class CognitiveDomain(str, Enum):
    REMEMBER = "REMEMBER"
    UNDERSTAND = "UNDERSTAND"
    APPLY = "APPLY"
    ANALYZE = "ANALYZE"
    EVALUATE = "EVALUATE"
    CREATE = "CREATE"


class DifficultyLogitBand(str, Enum):
    FOUNDATIONAL = "FOUNDATIONAL"   # -3.0 to -1.0
    INTERMEDIATE = "INTERMEDIATE"   # -1.0 to +0.5
    PROFICIENT = "PROFICIENT"       # +0.5 to +1.8
    MASTERY = "MASTERY"             # +1.8 to +3.0


class PerformanceIndicator(BaseModel):
    indicator_id: str
    code: str
    description: str
    cognitive_level: CognitiveDomain
    target_rubric_level: str = "Proficient"
    passing_threshold_score: float = 65.0


class LearningCompetency(BaseModel):
    competency_id: str
    code: str
    title: str
    description: str
    cognitive_level: CognitiveDomain
    difficulty_band: DifficultyLogitBand
    prerequisite_competency_ids: List[str] = Field(default_factory=list)
    performance_indicators: List[PerformanceIndicator] = Field(default_factory=list)
    mapped_accreditation_outcomes: List[str] = Field(default_factory=list)


class CurriculumDomainModule(BaseModel):
    module_id: str
    module_code: str
    module_name: str
    credits: float
    competencies: List[LearningCompetency] = Field(default_factory=list)


class CompetencyFrameworkRegistry:
    """
    Standardized curriculum blueprints for Computer Science, Electrical Engineering,
    Data Science, and Cyber Security degrees aligned with IEEE / ACM curricula.
    """

    @classmethod
    def get_computer_science_blueprint(cls) -> List[CurriculumDomainModule]:
        return [
            CurriculumDomainModule(
                module_id="mod-cs-alg",
                module_code="CS201",
                module_name="Algorithms and Data Structures",
                credits=4.0,
                competencies=[
                    LearningCompetency(
                        competency_id="comp-cs-alg-01",
                        code="CS-ALG-1.1",
                        title="Asymptotic Complexity Analysis",
                        description="Formulate Big-O, Big-Omega, and Big-Theta bounds for iterative and recursive procedures using recurrence relations and the Master Theorem.",
                        cognitive_level=CognitiveDomain.ANALYZE,
                        difficulty_band=DifficultyLogitBand.INTERMEDIATE,
                        mapped_accreditation_outcomes=["PO1", "PO2"],
                        performance_indicators=[
                            PerformanceIndicator(
                                indicator_id="pi-cs-alg-1.1.1",
                                code="PI-1.1.1",
                                description="Solves divide-and-conquer recurrences T(n) = aT(n/b) + f(n) correctly.",
                                cognitive_level=CognitiveDomain.APPLY
                            ),
                            PerformanceIndicator(
                                indicator_id="pi-cs-alg-1.1.2",
                                code="PI-1.1.2",
                                description="Identifies tight asymptotic lower bounds for comparison-based sorting.",
                                cognitive_level=CognitiveDomain.ANALYZE
                            )
                        ]
                    ),
                    LearningCompetency(
                        competency_id="comp-cs-alg-02",
                        code="CS-ALG-1.2",
                        title="Self-Balancing Binary Search Trees",
                        description="Implement and verify invariant preservation in Red-Black Trees, AVL Trees, and B-Trees under dynamic mutations.",
                        cognitive_level=CognitiveDomain.APPLY,
                        difficulty_band=DifficultyLogitBand.PROFICIENT,
                        prerequisite_competency_ids=["comp-cs-alg-01"],
                        mapped_accreditation_outcomes=["PO2", "PO3"],
                        performance_indicators=[
                            PerformanceIndicator(
                                indicator_id="pi-cs-alg-1.2.1",
                                code="PI-1.2.1",
                                description="Performs single and double tree rotations to restore AVL height balance.",
                                cognitive_level=CognitiveDomain.APPLY
                            ),
                            PerformanceIndicator(
                                indicator_id="pi-cs-alg-1.2.2",
                                code="PI-1.2.2",
                                description="Traces B-tree node splitting and merging during order-m disk page allocations.",
                                cognitive_level=CognitiveDomain.ANALYZE
                            )
                        ]
                    ),
                    LearningCompetency(
                        competency_id="comp-cs-alg-03",
                        code="CS-ALG-1.3",
                        title="Graph Traversal & Shortest Path Synthesis",
                        description="Construct optimal traversal schemes using Dijkstra, Bellman-Ford, and Floyd-Warshall with negative cycle detection.",
                        cognitive_level=CognitiveDomain.EVALUATE,
                        difficulty_band=DifficultyLogitBand.PROFICIENT,
                        prerequisite_competency_ids=["comp-cs-alg-02"],
                        mapped_accreditation_outcomes=["PO2", "PO3"]
                    ),
                    LearningCompetency(
                        competency_id="comp-cs-alg-04",
                        code="CS-ALG-1.4",
                        title="Dynamic Programming & Memoization",
                        description="Decompose complex optimization problems into overlapping subproblems exhibiting optimal substructure.",
                        cognitive_level=CognitiveDomain.CREATE,
                        difficulty_band=DifficultyLogitBand.MASTERY,
                        prerequisite_competency_ids=["comp-cs-alg-01"],
                        mapped_accreditation_outcomes=["PO2", "PO3", "PO4"]
                    )
                ]
            ),
            CurriculumDomainModule(
                module_id="mod-cs-dist",
                module_code="CS301",
                module_name="Distributed Cloud Computing & Fault Tolerance",
                credits=4.0,
                competencies=[
                    LearningCompetency(
                        competency_id="comp-cs-dist-01",
                        code="CS-DIST-2.1",
                        title="CAP Theorem & Consistency Models",
                        description="Evaluate latency-consistency trade-offs across strict serializability, linearizability, sequential, and eventual consistency.",
                        cognitive_level=CognitiveDomain.ANALYZE,
                        difficulty_band=DifficultyLogitBand.INTERMEDIATE,
                        mapped_accreditation_outcomes=["PO1", "PO2"]
                    ),
                    LearningCompetency(
                        competency_id="comp-cs-dist-02",
                        code="CS-DIST-2.2",
                        title="Distributed Consensus (Raft & Multi-Paxos)",
                        description="Formalize state machine replication, leader election quorums, log compaction, and term transitions.",
                        cognitive_level=CognitiveDomain.EVALUATE,
                        difficulty_band=DifficultyLogitBand.MASTERY,
                        prerequisite_competency_ids=["comp-cs-dist-01"],
                        mapped_accreditation_outcomes=["PO2", "PO3", "PO4"]
                    ),
                    LearningCompetency(
                        competency_id="comp-cs-dist-03",
                        code="CS-DIST-2.3",
                        title="Atomic Commitment & Distributed Transactions",
                        description="Design resilient 2-Phase Commit (2PC) and 3-Phase Commit (3PC) coordinator failure recovery routines.",
                        cognitive_level=CognitiveDomain.CREATE,
                        difficulty_band=DifficultyLogitBand.PROFICIENT,
                        prerequisite_competency_ids=["comp-cs-dist-02"],
                        mapped_accreditation_outcomes=["PO3", "PO4"]
                    )
                ]
            ),
            CurriculumDomainModule(
                module_id="mod-cs-sec",
                module_code="CS401",
                module_name="Applied Cryptography & Network Security",
                credits=4.0,
                competencies=[
                    LearningCompetency(
                        competency_id="comp-cs-sec-01",
                        code="CS-SEC-3.1",
                        title="Symmetric Ciphers & Block Modes",
                        description="Analyze security proofs for AES-GCM authenticated encryption, initialization vector reuse hazards, and padding oracle attacks.",
                        cognitive_level=CognitiveDomain.ANALYZE,
                        difficulty_band=DifficultyLogitBand.PROFICIENT,
                        mapped_accreditation_outcomes=["PO1", "PO2"]
                    ),
                    LearningCompetency(
                        competency_id="comp-cs-sec-02",
                        code="CS-SEC-3.2",
                        title="Asymmetric Cryptography & Discrete Logarithms",
                        description="Verify RSA modular arithmetic, Diffie-Hellman ephemeral key exchanges, and Elliptic Curve Cryptography (Ed25519/ECDSA).",
                        cognitive_level=CognitiveDomain.EVALUATE,
                        difficulty_band=DifficultyLogitBand.MASTERY,
                        prerequisite_competency_ids=["comp-cs-sec-01"],
                        mapped_accreditation_outcomes=["PO2", "PO3"]
                    ),
                    LearningCompetency(
                        competency_id="comp-cs-sec-03",
                        code="CS-SEC-3.3",
                        title="Public Key Infrastructure & TLS Handshake",
                        description="Audit X.509 certificate trust chains, OCSP stapling, Certificate Transparency logs, and TLS 1.3 key derivation.",
                        cognitive_level=CognitiveDomain.APPLY,
                        difficulty_band=DifficultyLogitBand.INTERMEDIATE,
                        prerequisite_competency_ids=["comp-cs-sec-02"],
                        mapped_accreditation_outcomes=["PO3", "PO4"]
                    )
                ]
            )
        ]

    @classmethod
    def calculate_curriculum_coverage(
        cls,
        administered_competency_ids: Set[str],
        modules: List[CurriculumDomainModule]
    ) -> Dict[str, float]:
        """
        Calculates percentage coverage of competencies across academic modules.
        """
        coverage: Dict[str, float] = {}
        for mod in modules:
            total = len(mod.competencies)
            if total == 0:
                coverage[mod.module_code] = 100.0
                continue
            covered = sum(1 for c in mod.competencies if c.competency_id in administered_competency_ids)
            coverage[mod.module_code] = round((covered / total) * 100.0, 1)
        return coverage
