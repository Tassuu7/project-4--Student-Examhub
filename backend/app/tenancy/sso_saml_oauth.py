"""
ExamHub Single Sign-On (SSO) Integration Engine
Handles SAML 2.0 XML assertion parsing, JWT/OIDC ID token claims mapping, and user provisioning.
"""

import base64
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional
from backend.app.tenancy.schemas import SSOConfig, SSOProviderType


class SSOIntegrationEngine:
    """
    Translates identity claims from university IdPs (Okta, Azure AD, Shibboleth, Google)
    into standardized ExamHub candidate and instructor accounts.
    """

    @classmethod
    def parse_saml_response(cls, saml_response_b64: str, config: SSOConfig) -> Dict[str, Any]:
        """
        Parses SAML 2.0 Base64 response XML and extracts mapped attributes.
        """
        try:
            xml_bytes = base64.b64decode(saml_response_b64)
            root = ET.fromstring(xml_bytes)
        except Exception as e:
            raise ValueError(f"Invalid SAML response encoding: {str(e)}")

        # Extract attributes from Assertion
        extracted_attributes: Dict[str, str] = {}
        for elem in root.iter():
            tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
            if tag == "Attribute":
                attr_name = elem.attrib.get("Name", "")
                attr_val = ""
                for child in elem:
                    child_tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
                    if child_tag == "AttributeValue" and child.text:
                        attr_val = child.text.strip()
                        break
                if attr_name and attr_val:
                    extracted_attributes[attr_name] = attr_val

        # Map to canonical user profile
        mapped_user = {
            "email": extracted_attributes.get(config.attribute_mapping.get("email", "email"), "user@institution.edu"),
            "name": extracted_attributes.get(config.attribute_mapping.get("name", "name"), "Academic User"),
            "student_id": extracted_attributes.get(config.attribute_mapping.get("student_id", "student_id"), "ID-UNKNOWN"),
            "role": "student"
        }

        # Role mapping heuristic
        raw_role = extracted_attributes.get(config.attribute_mapping.get("role", "role"), "").lower()
        if any(keyword in raw_role for keyword in ["faculty", "professor", "instructor", "teacher"]):
            mapped_user["role"] = "teacher"
        elif any(keyword in raw_role for keyword in ["admin", "dean", "registrar"]):
            mapped_user["role"] = "admin"

        return mapped_user

    @classmethod
    def map_oidc_claims(cls, claims: Dict[str, Any], config: SSOConfig) -> Dict[str, Any]:
        """
        Maps OpenID Connect ID token JSON payload to ExamHub user model.
        """
        email_key = config.attribute_mapping.get("email", "email")
        name_key = config.attribute_mapping.get("name", "name")

        email = claims.get(email_key, claims.get("upn", "candidate@institution.edu"))
        name = claims.get(name_key, claims.get("preferred_username", "Student"))
        groups = claims.get("groups", claims.get("roles", []))

        role = "student"
        if isinstance(groups, list):
            for g in groups:
                g_lower = str(g).lower()
                if "faculty" in g_lower or "instructor" in g_lower:
                    role = "teacher"
                elif "admin" in g_lower:
                    role = "admin"

        return {
            "email": email,
            "name": name,
            "student_id": claims.get("sub", "SUB-001"),
            "role": role,
            "provider": config.provider_type
        }
