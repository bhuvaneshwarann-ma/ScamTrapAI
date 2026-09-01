# ScamTrap AI — Architecture Decision Records

> Each decision is logged with context, rationale, and alternatives considered.

---

## ADR-001: FastAPI as Backend Framework

**Status:** Accepted
**Date:** Phase 1

**Context:** Need a Python web framework for the REST API that supports async, Pydantic integration, and OpenAPI documentation.

**Decision:** Use FastAPI with Pydantic v2.

**Rationale:**
- Native Pydantic v2 integration for request/response validation
- Async support for concurrent LLM/embedding calls
- Automatic OpenAPI documentation
- Middleware ecosystem (CORS, request IDs, etc.)
- Strong typing throughout

**Alternatives:** Flask (lacks native async, no built-in validation), Django (too heavy, ORM-coupled), Starlette (too low-level).

---

## ADR-002: HMAC-SHA256 for PII Hashing

**Status:** Accepted
**Date:** Phase 1

**Context:** PII (phone numbers, emails, UPI IDs) must never appear in logs but must be correlatable across log entries and incidents.

**Decision:** Use HMAC-SHA256 with a server-side secret key. Output is prefixed with a type tag (e.g., `PH:a3f8c2d1`) and truncated to 16 hex characters.

**Rationale:**
- Deterministic: same input always produces the same hash (enables correlation)
- Keyed: without the HMAC key, raw values cannot be recovered from hashes
- Type-prefixed: `PH:`, `EM:`, `UP:` make log analysis meaningful
- Truncated: 64 bits is sufficient for log correlation, minimizes log bloat

**Alternatives:** SHA-256 without HMAC (no key protection), random UUIDs (not deterministic), encryption (reversible — violates PII-safe principle for logs).

---

## ADR-003: structlog for Structured Logging

**Status:** Accepted
**Date:** Phase 1

**Context:** Need structured JSON logging with custom processors for automatic PII redaction.

**Decision:** Use `structlog` with a custom PII-redaction processor that scans all log values.

**Rationale:**
- Processor pipeline architecture allows inserting PII redaction before JSON serialization
- JSON output is machine-parseable for monitoring/alerting
- Context binding (request IDs, timestamps) propagates automatically
- Compatible with Python's stdlib `logging`

**Alternatives:** `python-json-logger` (less flexible processor pipeline), custom logging (reinventing the wheel).

---

## ADR-004: Input Sanitizer with Pattern-Based Injection Detection

**Status:** Accepted
**Date:** Phase 1

**Context:** Incident text fed to LLMs is untrusted and may contain prompt-injection attacks.

**Decision:** Regex-based detection of known injection patterns + delimiter stripping. Detection flags the input; the caller decides whether to reject or proceed with caution.

**Rationale:**
- Pattern-based detection covers known attack vectors (role override, system prompt extraction, delimiter injection, DAN/jailbreak)
- Delimiter stripping removes tokens that could confuse LLM instruction parsing
- Separation of detection and action: the sanitizer reports, the caller decides
- Extensible: new patterns can be added as threats evolve

**Trade-offs:** Regex patterns can't catch novel, zero-day injections. This is defense-in-depth — the LLM prompt architecture (Phase 4) adds another layer by structurally separating system instructions from user data.

---

## ADR-005: Vite + React + TypeScript for Frontend

**Status:** Accepted
**Date:** Phase 1

**Context:** Need a modern frontend framework for the investigator console with graph visualization capabilities.

**Decision:** Vite (build tool) + React 18 + TypeScript + Tailwind CSS.

**Rationale:**
- Vite: fast HMR, modern ESM-first build
- React 18: concurrent features, strong ecosystem (React Flow for graph viz)
- TypeScript: type safety matches backend's Pydantic discipline
- Tailwind CSS: rapid UI development with consistent design tokens

---

## ADR-006: Dark SOC/Cybersecurity Visual Design System

**Status:** Accepted
**Date:** Phase 1

**Context:** The investigator console must look professional and domain-appropriate — not like a generic SaaS dashboard.

**Decision:** Deep navy/charcoal backgrounds, electric blue/cyan accents, glassmorphism panels, mono-spaced fonts for data fields. Inspired by SOC/SIEM tools and cybersecurity dashboards.

**Rationale:**
- Dark themes reduce eye strain during extended investigation sessions
- High contrast for data-dense displays (graph nodes, evidence tables, confidence scores)
- Cyber-aesthetic establishes credibility and domain expertise
- Glassmorphism adds visual depth without distraction

---

## ADR-007: Offline-First with Mock Providers

**Status:** Accepted
**Date:** Phase 1

**Context:** The system must run with zero internet connectivity (§4.5). Live demos cannot depend on external API availability.

**Decision:** Every external dependency (LLM, embeddings, database) has a configurable provider abstraction with a deterministic mock fallback. The `LLM_PROVIDER=mock` and `EMBEDDING_PROVIDER=mock` settings activate offline mode.

**Rationale:**
- Hackathon demos must be 100% reliable
- Mock providers return deterministic, pre-computed results
- Same code paths are exercised in both modes (only the data source changes)
- Provider abstraction enables future swaps (Gemini → GPT, etc.)

---

## Threshold Calibration Records

> Reserved for Phase 9.5 — campaign detection threshold sweep results will be recorded here.
