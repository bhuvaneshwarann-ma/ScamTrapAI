# ScamTrap AI — System Architecture

> **Phase 1 — Foundation Document**
> This document is maintained incrementally. It reflects the current state of implementation.

---

## 1. System Overview

ScamTrap AI is a behavioral intelligence platform that converts suspicious multilingual conversations into structured **Scam DNA**, correlates incidents across shared infrastructure and tactics, and discovers emerging scam campaigns with evidence-bounded explanations.

### Core Pipeline

```
Raw Incident
  → PII-safe normalization
  → Multilingual LLM extraction (classifies into locked taxonomy)
  → Scam DNA
  → Entity resolution
  → Embedding generation
  → Candidate relationship generation
  → ML similarity (relationship_probability)
  → Temporal / infrastructure features
  → Deterministic evidence verification (relationship_confidence)
  → Campaign graph
  → Community detection
  → campaign_confidence
  → Investigator UI
```

---

## 2. Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| API Gateway | FastAPI (Python 3.11+) | REST API, request routing, middleware |
| Data Validation | Pydantic v2 | Schema enforcement, serialization |
| Configuration | pydantic-settings | Env-driven config management |
| Logging | structlog | Structured JSON logging with PII redaction |
| Frontend | React 18 + TypeScript + Vite | Investigator console |
| Styling | Tailwind CSS | SOC/cybersecurity dark theme |
| Graph Viz | React Flow (Phase 8+) | Campaign graph visualization |
| Database | PostgreSQL + pgvector / SQLite | Incident & entity storage |
| Cache | Redis | Token revocation, query caching |
| AI/NLP | Gemini API + Mock fallback | Scam DNA extraction |
| ML | scikit-learn, sentence-transformers | Similarity, clustering |
| Graph Engine | NetworkX | Campaign graph, community detection |
| Containerization | Docker, Docker Compose | Deployment |

---

## 3. Security Boundaries

### Cross-Cutting Constraints (Active from Phase 1)

1. **Untrusted Input Defense** — All incident text is treated as adversarial. Prompt-injection patterns are detected and neutralized before LLM processing. (`core/sanitizer.py`)

2. **PII-Safe Logging** — No raw identifier (phone, UPI, email, URL) appears in any log output. All identifiers are HMAC-SHA256 hashed before logging. (`core/security.py`, `core/logging.py`)

3. **Provenance Tagging** — Every AI-derived field carries `OBSERVED | INFERRED | PREDICTED`. (Phase 2+)

4. **Namespaced Confidence** — No bare `confidence` field exists. All confidence scores are prefixed: `extraction_confidence`, `resolution_confidence`, `relationship_probability`, `relationship_confidence`, `campaign_confidence`. (Phase 2+)

5. **100% Offline Fallback** — Every external API dependency has a deterministic mock provider. The system runs fully offline.

### Data Flow Security

```
User Input (untrusted)
  → Input Sanitizer (injection detection + delimiter stripping)
  → PII Hashing (HMAC-SHA256 for all identifiers in logs)
  → LLM Processing (input isolated from system instructions)
  → Structured Output (Pydantic validation)
  → Evidence-tagged Storage
```

---

## 4. AI/ML Boundaries

The system uses a **"ML proposes, rules verify"** architecture:

- **LLM** is used for language understanding (Scam DNA extraction, multilingual parsing). Its output is always validated against Pydantic schemas and locked taxonomies.
- **ML models** produce `relationship_probability` — a statistical score that is never shown to investigators alone.
- **Deterministic verification** converts ML proposals into `relationship_confidence` using exact infrastructure matches and taxonomy set-intersections.
- **The LLM never makes final risk decisions.** It extracts and classifies — humans and deterministic systems decide.

---

## 5. Current Implementation (Phase 1)

### Backend Components
- `app/main.py` — FastAPI application factory with CORS, request ID middleware, error handling
- `app/core/config.py` — Pydantic Settings (env-driven)
- `app/core/security.py` — HMAC-SHA256 PII hashing
- `app/core/sanitizer.py` — Prompt-injection detection & input sanitization
- `app/core/logging.py` — Structured JSON logger with automatic PII redaction
- `app/api/health.py` — Health check endpoint

### Frontend Components
- React 18 + TypeScript + Vite application shell
- Dark SOC/cybersecurity design system
- Dashboard placeholder with system health indicators

### Not Yet Implemented
- Database models (Phase 2)
- Scam DNA extraction (Phase 4)
- Entity resolution (Phase 5)
- Embeddings & similarity (Phase 6)
- Campaign relationship engine (Phase 7)
- Campaign graph (Phase 8)
- Campaign detection (Phase 9)
- Investigator copilot (Phase 11)
- Full API surface (Phase 12)
- Authentication & authorization (Phase 12)

---

## 6. Future Production Architecture

```
                    ┌─────────────────┐
                    │   API Gateway   │
                    │    (FastAPI)    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Event Queue    │
                    │   (Kafka)       │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼──────┐  ┌───▼──────┐  ┌───▼──────────┐
     │  Ingestion    │  │ AI/ML    │  │  Graph       │
     │  Workers      │  │ Workers  │  │  Analytics   │
     │  (Celery)     │  │ (Celery) │  │  (NetworkX)  │
     └────────┬──────┘  └───┬──────┘  └───┬──────────┘
              │              │              │
     ┌────────▼──────────────▼──────────────▼──────────┐
     │              PostgreSQL + pgvector               │
     └──────────────────────┬──────────────────────────┘
                            │
                    ┌───────▼───────┐
                    │    Redis      │
                    │  (Cache/Auth) │
                    └───────────────┘
```

This architecture is documented, not fully implemented — see `docs/decisions.md` for rationale.
