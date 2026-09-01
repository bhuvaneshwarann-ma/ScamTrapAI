"""
ScamTrap AI — PII Security Tests

Gate check (§4.2): PII hashing is deterministic, produces unique hashes,
and never exposes raw PII values.
"""

from backend.app.core.security import (
    hash_pii,
    hash_phone,
    hash_email,
    hash_upi,
    hash_url,
    hash_domain,
)


class TestHashPII:
    """Core HMAC-SHA256 hashing behavior."""

    def test_deterministic_hashing(self):
        """Same input always produces the same hash."""
        value = "+91 98765 43210"
        hash1 = hash_pii(value, "phone")
        hash2 = hash_pii(value, "phone")
        assert hash1 == hash2

    def test_different_inputs_different_hashes(self):
        """Different inputs produce different hashes."""
        hash1 = hash_pii("9876543210", "phone")
        hash2 = hash_pii("1234567890", "phone")
        assert hash1 != hash2

    def test_hash_not_raw_value(self):
        """Hash output must not contain the raw input."""
        raw = "victim@gmail.com"
        hashed = hash_pii(raw, "email")
        assert raw not in hashed

    def test_hash_has_type_prefix(self):
        """Hash output should be prefixed with the PII type tag."""
        assert hash_phone("9876543210").startswith("PH:")
        assert hash_email("test@test.com").startswith("EM:")
        assert hash_upi("user@ybl").startswith("UP:")
        assert hash_url("https://example.com").startswith("UR:")
        assert hash_domain("example.com").startswith("DM:")

    def test_empty_value_handling(self):
        """Empty values should produce a safe placeholder, not crash."""
        result = hash_pii("", "phone")
        assert result == "PH:EMPTY"

    def test_whitespace_stripping(self):
        """Leading/trailing whitespace should not affect the hash."""
        hash1 = hash_pii("  9876543210  ", "phone")
        hash2 = hash_pii("9876543210", "phone")
        assert hash1 == hash2

    def test_generic_type(self):
        """Generic PII type should use 'GN' prefix."""
        result = hash_pii("some_identifier")
        assert result.startswith("GN:")


class TestTypeSpecificHashers:
    """Convenience wrappers for specific PII types."""

    def test_hash_phone(self, sample_phone_numbers):
        """All phone number formats should hash successfully."""
        for phone in sample_phone_numbers:
            result = hash_phone(phone)
            assert result.startswith("PH:")
            assert len(result) > 5  # prefix + colon + hash chars

    def test_hash_email(self, sample_emails):
        """All email formats should hash successfully."""
        for email in sample_emails:
            result = hash_email(email)
            assert result.startswith("EM:")
            assert email not in result

    def test_hash_upi(self, sample_upi_ids):
        """All UPI ID formats should hash successfully."""
        for upi in sample_upi_ids:
            result = hash_upi(upi)
            assert result.startswith("UP:")
            assert upi not in result

    def test_hash_url(self, sample_urls):
        """All URL formats should hash successfully."""
        for url in sample_urls:
            result = hash_url(url)
            assert result.startswith("UR:")
            assert url not in result
