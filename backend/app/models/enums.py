"""
ScamTrap AI — Locked Behavioral & Infrastructure Taxonomy (§3.3)

These enums are the SINGLE SOURCE OF TRUTH for classification fields.
The Phase 4 LLM extractor classifies into these enums — it does NOT
generate free text for these fields. This makes Phase 7's "shared
social-engineering tactics" a deterministic set-intersection instead
of an LLM judgment call.

IMPORTANT: These enums are CLOSED-SET. New values require an explicit
schema migration and review. The LLM is never allowed to invent new
enum values at runtime.
"""

from enum import Enum


class ProvenanceType(str, Enum):
    """
    Provenance labels (§3.2).

    Every AI-derived field carries exactly one of these labels to distinguish
    ground truth from inference from prediction.
    """
    OBSERVED = "OBSERVED"      # Direct ground-truth fact extracted verbatim from raw incident data
    INFERRED = "INFERRED"      # Derived via heuristic, NLP extraction, or semantic embedding
    PREDICTED = "PREDICTED"    # Emitted by an ML model prior to deterministic verification


class SocialEngineeringTactic(str, Enum):
    """
    Locked taxonomy of social engineering tactics (§3.3).
    Used for deterministic set-intersection in campaign relationship detection.
    """
    URGENCY_PRESSURE = "urgency_pressure"
    AUTHORITY_IMPERSONATION = "authority_impersonation"
    FEAR_INDUCTION = "fear_induction"
    ARTIFICIAL_SCARCITY = "artificial_scarcity"
    TRUST_BUILDING = "trust_building"
    ISOLATION_TACTIC = "isolation_tactic"
    CREDENTIAL_HARVESTING = "credential_harvesting"
    PAYMENT_REDIRECTION = "payment_redirection"


class ImpersonationTarget(str, Enum):
    """
    Locked taxonomy of impersonation targets (§3.3).
    """
    BANK = "bank"
    GOVERNMENT_TAX = "government_tax"
    LAW_ENFORCEMENT = "law_enforcement"
    TELECOM = "telecom"
    DELIVERY_COURIER = "delivery_courier"
    FAMILY_MEMBER = "family_member"
    EMPLOYER = "employer"
    TECH_SUPPORT = "tech_support"
    OTHER = "other"  # escape hatch — pairs with impersonation_target_detail


class PaymentMethod(str, Enum):
    """
    Locked taxonomy of payment methods (§3.3).
    """
    UPI = "upi"
    BANK_TRANSFER = "bank_transfer"
    GIFT_CARD = "gift_card"
    CRYPTO = "crypto"
    CASH_PICKUP = "cash_pickup"
    WALLET_APP = "wallet_app"
    OTHER = "other"


class EntityType(str, Enum):
    """Types of extractable entities from incidents."""
    PHONE = "phone"
    UPI = "upi"
    EMAIL = "email"
    URL = "url"
    DOMAIN = "domain"


class IncidentChannel(str, Enum):
    """Communication channels for scam incidents."""
    SMS = "sms"
    WHATSAPP = "whatsapp"
    EMAIL = "email"
    VOICE = "voice"
    TELEGRAM = "telegram"
    OTHER = "other"


class IncidentStatus(str, Enum):
    """Processing status of an incident."""
    PENDING = "pending"
    PROCESSING = "processing"
    ANALYZED = "analyzed"
    FAILED = "failed"


class CampaignStatus(str, Enum):
    """Status of a detected campaign."""
    EMERGING = "emerging"
    ACTIVE = "active"
    CONFIRMED = "confirmed"
    ARCHIVED = "archived"


class RelationshipType(str, Enum):
    """Types of relationships between incidents."""
    SHARED_PHONE = "shared_phone"
    SHARED_UPI = "shared_upi"
    SHARED_URL = "shared_url"
    SHARED_DOMAIN = "shared_domain"
    SIMILAR_DNA = "similar_dna"
    SIMILAR_EMBEDDING = "similar_embedding"
    TEMPORAL_PROXIMITY = "temporal_proximity"
    SHARED_IMPERSONATION = "shared_impersonation"
    SHARED_TACTICS = "shared_tactics"


class RiskLevel(str, Enum):
    """Risk assessment levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
