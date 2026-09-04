"""
ExamHub Multi-Tenancy Architecture - Schemas & Models
Defines isolation models, subscription tiers, resource quotas, and single sign-on (SSO) configurations.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum


class SubscriptionTier(str, Enum):
    STARTER = "starter"
    CAMPUS = "campus"
    ENTERPRISE = "enterprise"
    GOVERNMENT = "government"


class SSOProviderType(str, Enum):
    SAML_2 = "saml2"
    OAUTH2_OIDC = "oauth2_oidc"
    MICROSOFT_ENTRA = "azure_ad"
    GOOGLE_WORKSPACE = "google_workspace"
    LDAP = "ldap"


class TenantQuota(BaseModel):
    max_active_students: int = 500
    max_concurrent_exams: int = 10
    storage_limit_gigabytes: float = 25.0
    enable_live_proctoring: bool = True
    enable_biometric_auth: bool = False
    enable_adaptive_cat: bool = True
    custom_domain_allowed: bool = False


class TenantBranding(BaseModel):
    institution_display_name: str
    primary_color_hex: str = "#2563eb"
    secondary_color_hex: str = "#1e40af"
    accent_color_hex: str = "#f59e0b"
    logo_url: Optional[str] = None
    favicon_url: Optional[str] = None
    custom_css: Optional[str] = None
    portal_welcome_message: str = "Welcome to the Institutional Examination Portal."


class SSOConfig(BaseModel):
    provider_type: SSOProviderType = SSOProviderType.OAUTH2_OIDC
    issuer_url: str
    client_id: str
    client_secret_masked: str = "********"
    metadata_url: Optional[str] = None
    attribute_mapping: Dict[str, str] = Field(
        default_factory=lambda: {
            "email": "email",
            "name": "displayName",
            "student_id": "urn:oid:0.9.2342.19200300.100.1.1",
            "role": "department"
        }
    )
    is_enabled: bool = False


class TenantRecord(BaseModel):
    tenant_id: str
    slug: str
    organization_name: str
    custom_domain: Optional[str] = None
    tier: SubscriptionTier = SubscriptionTier.CAMPUS
    quota: TenantQuota = Field(default_factory=TenantQuota)
    branding: TenantBranding
    sso_config: Optional[SSOConfig] = None
    created_at: str
    is_active: bool = True
    admin_contact_email: str
