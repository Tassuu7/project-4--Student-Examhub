"""
ExamHub Multi-Tenancy - FastAPI Router
Provides administrative endpoints for institutional onboarding, branding, and SSO configuration.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel

from backend.app.tenancy.schemas import (
    TenantRecord,
    TenantBranding,
    SSOConfig,
    SubscriptionTier,
)
from backend.app.tenancy.tenant_service import TenantService
from backend.app.auth.dependencies import require_role

router = APIRouter(prefix="/api/tenancy", tags=["Multi-Tenancy & Institutional Settings"])
_TENANT_SERVICE = TenantService()


class CreateTenantRequest(BaseModel):
    slug: str
    organization_name: str
    admin_email: str
    tier: SubscriptionTier = SubscriptionTier.CAMPUS
    custom_domain: str = None


@router.get("/current", response_model=TenantRecord)
def get_current_tenant(request: Request):
    """
    Resolve and return the tenant context associated with the incoming request host.
    """
    host = request.headers.get("host", "localhost")
    tenant = _TENANT_SERVICE.get_tenant_by_host(host)
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant context could not be resolved.")
    return tenant


@router.get("/list", response_model=List[TenantRecord])
def list_tenants(current_user: dict = Depends(require_role(["admin"]))):
    """List all registered institutional tenants (Super-admin only)."""
    return _TENANT_SERVICE.list_all_tenants()


@router.post("/create", response_model=TenantRecord)
def create_new_tenant(
    req: CreateTenantRequest,
    current_user: dict = Depends(require_role(["admin"]))
):
    """Provision a new institutional tenant."""
    try:
        tenant = _TENANT_SERVICE.create_tenant(
            slug=req.slug,
            organization_name=req.organization_name,
            admin_email=req.admin_email,
            tier=req.tier,
            custom_domain=req.custom_domain
        )
        return tenant
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{tenant_id}/branding", response_model=TenantRecord)
def update_branding(
    tenant_id: str,
    branding: TenantBranding,
    current_user: dict = Depends(require_role(["admin"]))
):
    """Update institutional branding, themes, and logos."""
    try:
        return _TENANT_SERVICE.update_branding(tenant_id, branding)
    except KeyError:
        raise HTTPException(status_code=404, detail="Tenant not found")


@router.put("/{tenant_id}/sso", response_model=TenantRecord)
def configure_sso(
    tenant_id: str,
    sso: SSOConfig,
    current_user: dict = Depends(require_role(["admin"]))
):
    """Configure SAML 2.0 or OpenID Connect SSO settings."""
    try:
        return _TENANT_SERVICE.update_sso_config(tenant_id, sso)
    except KeyError:
        raise HTTPException(status_code=404, detail="Tenant not found")
