"""
ScamTrap AI — Input Sanitizer & Prompt-Injection Defense

Cross-cutting constraint (§4.1): any incident text fed to an LLM is treated as
adversarial, untrusted data. It must never alter system instructions.

This module provides:
1. ``detect_injection`` — checks text against known prompt-injection patterns.
2. ``sanitize_input`` — strips/escapes dangerous patterns while preserving content.
3. ``SanitizationResult`` — structured output with detection metadata.

The test harness (in tests/) validates these against a curated set of known
injection payloads, ensuring the guardrails are effective from Phase 1 onward.
"""

import re
from typing import List

from pydantic import BaseModel


# ── Known prompt-injection patterns ──────────────────────────────────────
# These are regex patterns that match common LLM prompt injection attempts.
# They cover role-override, instruction-delimiter, system-prompt extraction,
# and jailbreak patterns. Case-insensitive matching.

_INJECTION_PATTERNS: List[re.Pattern] = [
    # Role override / persona hijacking
    re.compile(
        r"(ignore\s+(all\s+)?(previous|prior|above|earlier)\s+(instructions?|prompts?|rules?))",
        re.IGNORECASE,
    ),
    re.compile(
        r"(you\s+are\s+now\s+(a|an|the)\s+\w+)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(forget\s+(all\s+)?(previous|prior|your)\s+(instructions?|rules?|context))",
        re.IGNORECASE,
    ),
    re.compile(
        r"(disregard\s+(all\s+)?(previous|prior|above)\s+(instructions?|prompts?))",
        re.IGNORECASE,
    ),
    re.compile(
        r"(override\s+(system|safety|all)\s+(instructions?|prompts?|rules?))",
        re.IGNORECASE,
    ),
    # System prompt extraction
    re.compile(
        r"(repeat|show|display|reveal|print|output)\s+(your\s+)?(system\s+)?(prompt|instructions?|rules?)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(what\s+(are|is)\s+your\s+(system\s+)?(prompt|instructions?|rules?))",
        re.IGNORECASE,
    ),
    # Instruction delimiters that try to inject new system context
    re.compile(
        r"(\[SYSTEM\]|\[INST\]|\[\/INST\]|<\|system\|>|<\|user\|>|<\|assistant\|>)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(###\s*(system|instruction|new\s+instruction))",
        re.IGNORECASE,
    ),
    # DAN / jailbreak patterns
    re.compile(
        r"(do\s+anything\s+now|DAN\s+mode|jailbreak|act\s+as\s+if\s+you\s+have\s+no\s+restrictions)",
        re.IGNORECASE,
    ),
    # Delimiter injection (trying to close the user message and start a new one)
    re.compile(
        r"(```\s*system|<system>|</system>|<\|im_start\|>|<\|im_end\|>)",
        re.IGNORECASE,
    ),
]

# Maximum input length (characters) — defense against resource exhaustion
MAX_INPUT_LENGTH = 50_000


class SanitizationResult(BaseModel):
    """Structured result of input sanitization."""

    is_safe: bool
    original_length: int
    sanitized_text: str
    detected_patterns: List[str]
    was_truncated: bool = False


def detect_injection(text: str) -> List[str]:
    """
    Check text for known prompt-injection patterns.

    Args:
        text: The raw input text to scan.

    Returns:
        A list of matched pattern descriptions. Empty list means no injections detected.
    """
    if not text:
        return []

    detected: List[str] = []
    for pattern in _INJECTION_PATTERNS:
        match = pattern.search(text)
        if match:
            detected.append(f"Pattern matched: '{match.group()}'")

    return detected


def sanitize_input(text: str) -> SanitizationResult:
    """
    Sanitize untrusted input text for safe use with LLMs.

    This function:
    1. Truncates excessively long input.
    2. Detects known injection patterns (logged, flagged, but text is still processed —
       the caller decides whether to reject or proceed with caution).
    3. Strips dangerous instruction delimiters that could confuse LLM parsing.

    The original meaning of the text is preserved as much as possible — we are
    sanitizing for LLM safety, not for HTML/SQL injection.

    Args:
        text: The raw, untrusted input text.

    Returns:
        A SanitizationResult with the sanitized text and detection metadata.
    """
    if not text:
        return SanitizationResult(
            is_safe=True,
            original_length=0,
            sanitized_text="",
            detected_patterns=[],
        )

    original_length = len(text)
    was_truncated = False

    # Step 1: Truncate excessively long input
    if len(text) > MAX_INPUT_LENGTH:
        text = text[:MAX_INPUT_LENGTH]
        was_truncated = True

    # Step 2: Detect injection patterns
    detected_patterns = detect_injection(text)

    # Step 3: Strip dangerous instruction delimiters
    # We replace these with harmless equivalents so the text content is preserved
    # but the delimiters can't confuse the LLM's instruction parsing.
    sanitized = text
    sanitized = re.sub(
        r"(\[SYSTEM\]|\[INST\]|\[\/INST\])",
        "[REDACTED_DELIMITER]",
        sanitized,
        flags=re.IGNORECASE,
    )
    sanitized = re.sub(
        r"(<\|system\|>|<\|user\|>|<\|assistant\|>|<\|im_start\|>|<\|im_end\|>)",
        "[REDACTED_DELIMITER]",
        sanitized,
        flags=re.IGNORECASE,
    )
    sanitized = re.sub(
        r"(<system>|</system>)",
        "[REDACTED_DELIMITER]",
        sanitized,
        flags=re.IGNORECASE,
    )

    return SanitizationResult(
        is_safe=len(detected_patterns) == 0,
        original_length=original_length,
        sanitized_text=sanitized,
        detected_patterns=detected_patterns,
        was_truncated=was_truncated,
    )
