"""
ExamHub Multi-Tenancy Quota & Feature Gating Manager
Validates resource consumption limits against tenant licensing tiers.
"""

from typing import Dict, Tuple
from backend.app.tenancy.schemas import TenantRecord, SubscriptionTier


class QuotaManager:
    """
    Enforces subscription quotas, concurrent examination limits, and feature toggles.
    """

    def __init__(self):
        # Current utilization counters: tenant_id -> count
        self._active_exams_count: Dict[str, int] = {}
        self._active_candidates_count: Dict[str, int] = {}
        self._storage_usage_gb: Dict[str, float] = {}

    def check_exam_concurrency_allowed(self, tenant: TenantRecord) -> Tuple[bool, str]:
        """Verify if tenant can launch an additional concurrent exam session."""
        current = self._active_exams_count.get(tenant.tenant_id, 0)
        max_allowed = tenant.quota.max_concurrent_exams

        if current >= max_allowed:
            return False, f"Concurrent exam limit reached ({current}/{max_allowed}). Upgrade tier to increase capacity."
        return True, "OK"

    def increment_active_exam(self, tenant_id: str):
        self._active_exams_count[tenant_id] = self._active_exams_count.get(tenant_id, 0) + 1

    def decrement_active_exam(self, tenant_id: str):
        current = self._active_exams_count.get(tenant_id, 1)
        self._active_exams_count[tenant_id] = max(0, current - 1)

    def check_candidate_seat_allowed(self, tenant: TenantRecord, additional_seats: int = 1) -> Tuple[bool, str]:
        """Verify candidate enrolment does not breach active student license quota."""
        current = self._active_candidates_count.get(tenant.tenant_id, 0)
        max_allowed = tenant.quota.max_active_students

        if current + additional_seats > max_allowed:
            return False, f"Active student seat limit exceeded ({current + additional_seats}/{max_allowed})."
        return True, "OK"

    def check_feature_entitlement(self, tenant: TenantRecord, feature_name: str) -> bool:
        """Check whether specific enterprise feature is unlocked for tenant."""
        q = tenant.quota
        if feature_name == "live_proctoring":
            return q.enable_live_proctoring
        elif feature_name == "biometric_auth":
            return q.enable_biometric_auth
        elif feature_name == "adaptive_cat":
            return q.enable_adaptive_cat
        elif feature_name == "custom_domain":
            return q.custom_domain_allowed
        return True
