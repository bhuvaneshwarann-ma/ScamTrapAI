"""
ScamTrap AI — Phase 6 Similarity Service Tests

Validates:
- High behavioral similarity for same-campaign ScamDNA paraphrases
- Discrimination against false-similarity negative controls
- Feature contribution breakdown
"""

import pytest
from backend.app.models.enums import (
    IncidentChannel,
    ImpersonationTarget,
    PaymentMethod,
    SocialEngineeringTactic,
)
from backend.app.models.scam_dna import ScamDNA
from backend.app.services.similarity_service import SimilarityService


def test_same_campaign_high_similarity():
    service = SimilarityService()

    dna1 = ScamDNA(
        language="en",
        channel=IncidentChannel.SMS,
        impersonation_target=ImpersonationTarget.BANK,
        urgency=0.9,
        fear=0.8,
        authority_pressure=0.8,
        credential_request=True,
        payment_request=True,
        payment_method=PaymentMethod.UPI,
        requested_action="Update KYC",
        social_engineering_tactics=[
            SocialEngineeringTactic.URGENCY_PRESSURE,
            SocialEngineeringTactic.FEAR_INDUCTION,
        ],
        target_type="individual",
        extraction_confidence=0.95,
    )

    dna2 = ScamDNA(
        language="ta-en",
        channel=IncidentChannel.WHATSAPP,
        impersonation_target=ImpersonationTarget.BANK,
        urgency=0.85,
        fear=0.8,
        authority_pressure=0.75,
        credential_request=True,
        payment_request=True,
        payment_method=PaymentMethod.UPI,
        requested_action="Pay KYC fee",
        social_engineering_tactics=[
            SocialEngineeringTactic.URGENCY_PRESSURE,
            SocialEngineeringTactic.FEAR_INDUCTION,
        ],
        target_type="individual",
        extraction_confidence=0.92,
    )

    res = service.compute_similarity(dna1, dna2)
    assert res.similarity_score >= 0.85
    assert "shared_impersonation_target" in res.compared_features


def test_different_campaign_low_similarity():
    service = SimilarityService()

    dna_bank = ScamDNA(
        language="en",
        channel=IncidentChannel.SMS,
        impersonation_target=ImpersonationTarget.BANK,
        urgency=0.9,
        fear=0.8,
        authority_pressure=0.8,
        credential_request=True,
        payment_request=True,
        payment_method=PaymentMethod.UPI,
        requested_action="Update KYC",
        social_engineering_tactics=[SocialEngineeringTactic.URGENCY_PRESSURE],
        target_type="individual",
        extraction_confidence=0.95,
    )

    dna_traffic = ScamDNA(
        language="en",
        channel=IncidentChannel.SMS,
        impersonation_target=ImpersonationTarget.LAW_ENFORCEMENT,
        urgency=0.4,
        fear=0.3,
        authority_pressure=0.9,
        credential_request=False,
        payment_request=True,
        payment_method=PaymentMethod.CASH_PICKUP,
        requested_action="Pay traffic fine",
        social_engineering_tactics=[SocialEngineeringTactic.AUTHORITY_IMPERSONATION],
        target_type="individual",
        extraction_confidence=0.90,
    )

    res = service.compute_similarity(dna_bank, dna_traffic)
    assert res.similarity_score < 0.60
