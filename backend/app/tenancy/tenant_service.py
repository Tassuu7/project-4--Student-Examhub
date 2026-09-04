"""
ExamHub Multi-Tenancy Management Service
Handles tenant onboarding, isolated schema provisioning, domain routing, and quota enforcement.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from backend.app.tenancy.schemas import (
    TenantRecord,
    SubscriptionTier,
    TenantQuota,
    TenantBranding,
    SSOConfig,
    SSOProviderType,
)


class TenantService:
    """
    Core service for managing institutional tenants, resource allocation, and domain mapping.
    """

    def __init__(self):
        self._tenants: Dict[str, TenantRecord] = {}
        self._domain_lookup: Dict[str, str] = {}  # domain/subdomain -> tenant_id
        self._seed_default_tenants()

    def _seed_default_tenants(self):
        default_tenant = TenantRecord(
            tenant_id="tenant-apex-inst",
            slug="apex-polytechnic",
            organization_name="Apex Polytechnic Institute",
            custom_domain="exams.apex.edu",
            tier=SubscriptionTier.ENTERPRISE,
            quota=TenantQuota(
                max_active_students=10000,
                max_concurrent_exams=100,
                storage_limit_gigabytes=500.0,
                enable_live_proctoring=True,
                enable_biometric_auth=True,
                enable_adaptive_cat=True,
                custom_domain_allowed=True
            ),
            branding=TenantBranding(
                institution_display_name="Apex Institute of Technology & Management",
                primary_color_hex="#0f766e",
                secondary_color_hex="#115e59",
                accent_color_hex="#f97316",
                logo_url="/assets/apex-logo.svg",
                portal_welcome_message="Welcome to Apex Secure Testing Portal."
            ),
            sso_config=SSOConfig(
                provider_type=SSOProviderType.MICROSOFT_ENTRA,
                issuer_url="https://login.microsoftonline.com/tenant-guid/v2.0",
                client_id="azure-client-apex-01",
                is_enabled=True
            ),
            created_at=datetime.now(timezone.utc).isoformat(),
            is_active=True,
            admin_contact_email="provost@apex.edu"
        )
        self._tenants[default_tenant.tenant_id] = default_tenant
        self._domain_lookup[default_tenant.slug] = default_tenant.tenant_id
        if default_tenant.custom_domain:
            self._domain_lookup[default_tenant.custom_domain] = default_tenant.tenant_id

    def get_tenant_by_id(self, tenant_id: str) -> Optional[TenantRecord]:
        return self._tenants.get(tenant_id)

    def get_tenant_by_host(self, host: str) -> Optional[TenantRecord]:
        """Resolves tenant from HTTP Host header (subdomain or custom domain)."""
        clean_host = host.split(":")[0].lower()
        # Direct domain match
        if clean_host in self._domain_lookup:
            return self._tenants.get(self._domain_lookup[clean_host])

        # Subdomain match: apex.examhub.io -> apex
        subdomain = clean_host.split(".")[0]
        if subdomain in self._domain_lookup:
            return self._tenants.get(self._domain_lookup[subdomain])

        # Fallback to primary tenant
        return next(iter(self._tenants.values()), None)

    def list_all_tenants(self) -> List[TenantRecord]:
        return list(self._tenants.values())

    def create_tenant(
        self,
        slug: str,
        organization_name: str,
        admin_email: str,
        tier: SubscriptionTier = SubscriptionTier.CAMPUS,
        custom_domain: Optional[str] = None
    ) -> TenantRecord:
        if slug in self._domain_lookup:
            raise ValueError(f"Tenant slug '{slug}' is already taken.")

        tenant_id = f"tenant-{uuid.uuid4().hex[:10]}"
        quotas = {
            SubscriptionTier.STARTER: TenantQuota(max_active_students=100, max_concurrent_exams=2, storage_limit_gigabytes=5.0, enable_live_proctoring=False, enable_biometric_auth=False),
            SubscriptionTier.CAMPUS: TenantQuota(max_active_students=2500, max_concurrent_exams=25, storage_limit_gigabytes=100.0, enable_live_proctoring=True, enable_biometric_auth=False),
            SubscriptionTier.ENTERPRISE: TenantQuota(max_active_students=20000, max_concurrent_exams=200, storage_limit_gigabytes=1000.0, enable_live_proctoring=True, enable_biometric_auth=True, custom_domain_allowed=True),
            SubscriptionTier.GOVERNMENT: TenantQuota(max_active_students=100000, max_concurrent_exams=1000, storage_limit_gigabytes=5000.0, enable_live_proctoring=True, enable_biometric_auth=True, custom_domain_allowed=True),
        }

        branding = TenantBranding(institution_display_name=organization_name)
        record = TenantRecord(
            tenant_id=tenant_id,
            slug=slug,
            organization_name=organization_name,
            custom_domain=custom_domain,
            tier=tier,
            quota=quotas.get(tier, TenantQuota()),
            branding=branding,
            created_at=datetime.now(timezone.utc).isoformat(),
            is_active=True,
            admin_contact_email=admin_email
        )

        self._tenants[tenant_id] = record
        self._domain_lookup[slug] = tenant_id
        if custom_domain:
            self._domain_lookup[custom_domain] = tenant_id

        return record

    def update_branding(self, tenant_id: str, branding: TenantBranding) -> TenantRecord:
        tenant = self._tenants.get(tenant_id)
        if not tenant:
            raise KeyError("Tenant not found")
        tenant.branding = branding
        return tenant

    def update_sso_config(self, tenant_id: str, sso: SSOConfig) -> TenantRecord:
        tenant = self._tenants.get(tenant_id)
        if not tenant:
            raise KeyError("Tenant not found")
        tenant.sso_config = sso
        return tenant
