"""
ScamTrap AI — Phase 5 Entity Resolution Tests

Validates:
- Phone format normalization (+91 98765 43210, 9876543210, +91-98765-43210 → +919876543210)
- UPI casing and whitespace normalization
- URL and domain canonicalization
- Resolution confidence assignment
"""

import pytest
from backend.app.models.enums import EntityType
from backend.app.services.entity_resolver import EntityResolver


def test_phone_normalization_formats():
    resolver = EntityResolver()
    variations = [
        "+91 98765 43210",
        "9876543210",
        "+91-98765-43210",
        "91-9876543210",
    ]

    for var in variations:
        norm, conf = resolver.normalize_phone(var)
        assert norm == "+919876543210"
        assert conf >= 0.90


def test_upi_normalization():
    resolver = EntityResolver()
    norm, conf = resolver.normalize_upi("  SBI.KYC.UPDATE@YBL  ")
    assert norm == "sbi.kyc.update@ybl"
    assert conf == 0.99


def test_url_domain_canonicalization():
    resolver = EntityResolver()
    norm_url, _ = resolver.normalize_url("https://sbi-kyc-update-portal.xyz/verify?utm_source=sms.")
    assert norm_url.startswith("https://sbi-kyc-update-portal.xyz/verify")

    norm_domain, _ = resolver.normalize_domain("http://SBI-KYC-UPDATE-PORTAL.XYZ/login")
    assert norm_domain == "sbi-kyc-update-portal.xyz"


def test_resolve_mention():
    resolver = EntityResolver()
    mention, entity = resolver.resolve_mention("+91 98765 43210", EntityType.PHONE, "inc-101")

    assert mention.raw_value == "+91 98765 43210"
    assert entity.normalized_value == "+919876543210"
    assert entity.resolution_confidence >= 0.90
    assert mention.canonical_entity_id == entity.id
