"""
ScamTrap AI — Entity Resolution Service (Phase 5)

Normalizes repeated identifiers into canonical Entities:
- Phone: E.164 format (+919876543210)
- UPI ID: Lowercase, trimmed
- URL: Stripped tracking parameters, normalized scheme & path
- Domain: Lowercase host without port/subpath
- Email: Lowercase, trimmed

Outputs:
- Canonical entity ID
- Entity type
- Normalized value
- Source mentions
- resolution_confidence (namespaced confidence §3.2)
"""

import re
from typing import List, Tuple
from urllib.parse import urlparse

from backend.app.core.security import hash_pii
from backend.app.models.enums import EntityType
from backend.app.models.entity import Entity, EntityMention


class EntityResolver:
    """Canonical Entity Resolver."""

    @staticmethod
    def normalize_phone(phone: str) -> Tuple[str, float]:
        """
        Normalize phone numbers into canonical E.164 format.
        Returns (normalized_value, confidence).
        """
        digits = re.sub(r"\D", "", phone)
        if not digits:
            return "", 0.0

        # India +91 default fallback if 10 digits
        if len(digits) == 10:
            return f"+91{digits}", 0.95
        elif len(digits) == 12 and digits.startswith("91"):
            return f"+{digits}", 0.99
        elif len(digits) >= 11:
            return f"+{digits}", 0.90

        return f"+{digits}", 0.80

    @staticmethod
    def normalize_upi(upi: str) -> Tuple[str, float]:
        """Normalize UPI ID to lowercase trimmed string."""
        clean = upi.strip().lower()
        if "@" in clean:
            return clean, 0.99
        return clean, 0.80

    @staticmethod
    def normalize_url(url: str) -> Tuple[str, float]:
        """Normalize URL by stripping tracking queries, subpaths when appropriate."""
        clean = url.strip().rstrip(".,;")
        if not clean.startswith(("http://", "https://")):
            clean = "https://" + clean
        parsed = urlparse(clean)
        domain = parsed.netloc.lower()
        path = parsed.path.rstrip("/")
        normalized = f"{parsed.scheme}://{domain}{path}"
        return normalized, 0.95

    @staticmethod
    def normalize_domain(domain_or_url: str) -> Tuple[str, float]:
        """Extract canonical lowercased domain host."""
        clean = domain_or_url.strip().lower()
        if clean.startswith(("http://", "https://")):
            clean = urlparse(clean).netloc
        domain = clean.split("/")[0].split(":")[0]
        return domain, 0.99

    @staticmethod
    def normalize_email(email: str) -> Tuple[str, float]:
        """Normalize email address to lowercase."""
        return email.strip().lower(), 0.99

    def resolve_mention(self, raw_value: str, entity_type: EntityType, incident_id: str) -> Tuple[EntityMention, Entity]:
        """Resolve a single raw mention into an EntityMention and canonical Entity."""
        if entity_type == EntityType.PHONE:
            norm_val, conf = self.normalize_phone(raw_value)
        elif entity_type == EntityType.UPI:
            norm_val, conf = self.normalize_upi(raw_value)
        elif entity_type == EntityType.URL:
            norm_val, conf = self.normalize_url(raw_value)
        elif entity_type == EntityType.DOMAIN:
            norm_val, conf = self.normalize_domain(raw_value)
        elif entity_type == EntityType.EMAIL:
            norm_val, conf = self.normalize_email(raw_value)
        else:
            norm_val, conf = raw_value.strip().lower(), 0.80

        entity = Entity(
            entity_type=entity_type,
            normalized_value=norm_val,
            resolution_confidence=conf,
            incident_ids=[incident_id],
        )

        mention = EntityMention(
            incident_id=incident_id,
            entity_type=entity_type,
            raw_value=raw_value,
            canonical_entity_id=entity.id,
        )

        entity.mention_ids.append(mention.id)
        return mention, entity
