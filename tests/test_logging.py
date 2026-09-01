"""
ScamTrap AI — Structured Logging PII Redaction Tests

Gate check (§4.2): PII patterns in log messages and values are automatically
redacted with HMAC hashes before emission. Non-PII text passes unchanged.
"""

from backend.app.core.logging import _redact_pii_in_value


class TestPIIRedactionInValues:
    """The redaction processor must catch PII patterns in log values."""

    def test_redacts_phone_number(self):
        """Phone numbers in strings should be replaced with hashes."""
        result = _redact_pii_in_value("Called from +91 98765 43210")
        assert "+91 98765 43210" not in result
        assert "PH:" in result

    def test_redacts_email(self):
        """Email addresses should be replaced with hashes."""
        result = _redact_pii_in_value("Contact: victim@gmail.com")
        assert "victim@gmail.com" not in result
        assert "EM:" in result

    def test_redacts_upi_id(self):
        """UPI IDs should be replaced with hashes."""
        result = _redact_pii_in_value("UPI transfer to fraud@ybl")
        assert "fraud@ybl" not in result
        assert "UP:" in result

    def test_redacts_url(self):
        """URLs should be replaced with hashes."""
        result = _redact_pii_in_value("Visit https://fake-bank.com/login")
        assert "https://fake-bank.com/login" not in result
        assert "UR:" in result

    def test_preserves_non_pii_text(self):
        """Text without PII patterns should pass through unchanged."""
        text = "Processing incident with urgency score 0.85"
        result = _redact_pii_in_value(text)
        assert result == text

    def test_redacts_in_dict_values(self):
        """PII in dict values should be redacted."""
        data = {"phone": "+91 98765 43210", "status": "active"}
        result = _redact_pii_in_value(data)
        assert "+91 98765 43210" not in str(result)
        assert result["status"] == "active"

    def test_redacts_in_list_values(self):
        """PII in list items should be redacted."""
        data = ["+91 98765 43210", "clean text"]
        result = _redact_pii_in_value(data)
        assert "+91 98765 43210" not in str(result)
        assert "clean text" in result

    def test_multiple_pii_in_one_string(self):
        """Multiple PII patterns in one string should all be redacted."""
        text = "Phone: +91 98765 43210, Email: test@example.com"
        result = _redact_pii_in_value(text)
        assert "+91 98765 43210" not in result
        assert "test@example.com" not in result

    def test_handles_non_string_types(self):
        """Non-string types (int, float, None) should pass through."""
        assert _redact_pii_in_value(42) == 42
        assert _redact_pii_in_value(3.14) == 3.14
        assert _redact_pii_in_value(None) is None
        assert _redact_pii_in_value(True) is True
