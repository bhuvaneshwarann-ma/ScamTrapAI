# SCAMTRAP AI — CONSOLIDATED BUILD DIRECTIVE (spec.md, v3 merged)

You are the Principal Software Engineer, Senior AI/ML Engineer, Security Architect, Product Architect, and Technical Lead for this project. This is the single, standalone build directive — merging the phase-by-phase plan with the technical specification into one authoritative document. Hand this file to the engineering agent as-is.

---

## 1. MISSION & PARADIGM

ScamTrap AI is **not** a generic scam detector, chatbot, or thin RAG wrapper.

- **Generic detector paradigm:** *"Is this message a scam?"*
- **ScamTrap AI paradigm:** *"What infrastructure and behavioral campaign does this scam belong to?"*

The system converts suspicious, unverified multilingual conversations (SMS, WhatsApp, Email, Voice Transcripts) into structured behavioral intelligence (**Scam DNA**), normalizes and resolves entities, correlates incidents across shared infrastructure and tactics using a hybrid ML + deterministic verification engine, constructs a campaign graph, detects emerging campaigns, and provides evidence-bounded explanations.

The system must clearly distinguish **OBSERVED / INFERRED / PREDICTED** at every stage. The LLM must never independently declare someone criminal or make unsupported accusations.

**The project uses synthetic data only** for the hackathon.

### Intended pipeline

```
Conversation → AI Analysis → Scam DNA → Correlation → Campaign Alert
```

### Detailed data flow

```
Raw Incident
→ PII-safe normalization
→ multilingual LLM extraction (classifies into locked taxonomy)
→ Scam DNA
→ entity resolution
→ embedding generation
→ candidate relationship generation
→ ML similarity (relationship_probability)
→ temporal / infrastructure features
→ deterministic evidence verification (relationship_confidence)
→ campaign graph
→ community detection
→ campaign_confidence
→ investigator UI
→ feedback
→ evaluation / calibration
```

### System topology

```
[ Multilingual Incident: SMS / WhatsApp / Email / Voice ]
                    │
                    ▼
          [ FastAPI API Gateway ]
                    │
                    ▼
      [ Incident Ingestion Pipeline ]
                    │
                    ▼
   [ PII Tokenization & Normalization ]
                    │
                    ▼
   [ Multilingual LLM Extraction ]
   (classifies into locked taxonomy)
                    │
                    ▼
          [ Structured Scam DNA ]
          ├──► [ Semantic Embeddings ] ───────┐
          └──► [ Entity Resolution ] ─────────┼──► [ Candidate Relationship Engine ]
                                               │              │
                                               │    [ Temporal + Infra Features ]
                                               │              │
                                               │    [ Campaign Similarity Model ]
                                               │      (relationship_probability)
                                               │              │
                                               │    [ Graph Construction (NetworkX) ]
                                               │              │
                                               │    [ Community / Cluster Detection ]
                                               │              │
                            [ PostgreSQL / pgvector / Redis ]
                                               │
                            [ Deterministic Verification ]
                                               │
                            [ Canonical Evidence Engine ]
                               (relationship_confidence)
                                               │
                                [ Campaign Confidence ]
                                               │
                        ┌──────────────────────┴──────────────────────┐
                        ▼                                             ▼
          [ Emerging Campaign Alert ]                    [ Investigator Console ]
                                                       (React Flow Graph + Evidence)
                                                                      │
                                                       [ Evidence-Bounded Copilot ]
                                                        (strict zero-hallucination)
```

### Real-world precedents this design borrows from

| Pattern | Source system | Where it's used below |
|---|---|---|
| Typed evidence objects with confidence + provenance chains | MISP / STIX-TAXII (threat-intel exchange standards) | §3.1 Canonical Evidence Object |
| Entity-relationship graph, every edge carries explicit provenance | Palantir Gotham / Maltego | §3.1, Phase 8 |
| Heuristic + ML co-clustering with a *separate deterministic confirmation* before attribution is user-facing | Chainalysis Reactor (crypto wallet clustering) | Phase 7, §3.2 namespaced confidence |
| Behavior tagged with a fixed technique taxonomy, not free text | MITRE ATT&CK | §3.3 Taxonomy Lock |
| "ML proposes, rules/evidence layer verifies" — a single model score is never investigator-facing alone | Feedzai / Sift / Forter (production fraud platforms) | Phase 7 hybrid engine |
| Identifier normalization across noisy formats | Truecaller-style number/entity resolution | Phase 5 |

---

## 2. ENGINEERING PRINCIPLES

- Do NOT build a generic chatbot.
- Do NOT build a generic RAG application.
- Do NOT blindly trust LLM output.
- Do NOT let the LLM make final risk decisions.
- Do NOT create unnecessary microservices.
- Do NOT overengineer.
- Do NOT add features that don't improve the winning demo.
- Prefer deterministic systems for evidence and final decisions.
- Use AI for language understanding.
- Use ML for similarity/prediction.
- Use graph algorithms for campaign discovery.
- Keep every important conclusion explainable.
- Every AI-generated claim must have provenance.
- All critical AI outputs must use structured schemas.
- Design the system so the AI service can fail without destroying the application.
- Build everything incrementally. Test every phase before moving forward.

---

## 3. DOMAIN MODEL & CANONICAL SCHEMAS

These are defined **once**, in Phase 2. No later phase redefines them — Phase 7 (relationship engine), Phase 9 (campaign detection), and Phase 10 (explainability) all *consume and populate* these schemas.

### 3.1 Canonical Evidence Object

```python
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

class Evidence(BaseModel):
    claim: str
    type: Literal["OBSERVED", "INFERRED", "PREDICTED"]
    source: str                       # subsystem that produced this claim, e.g. "entity_resolver", "dna_extractor"
    confidence: float = Field(ge=0.0, le=1.0)
    supporting_incident_ids: list[str] = Field(default_factory=list)
    supporting_entity_ids: list[str] = Field(default_factory=list)
    scoring_factors: dict[str, float] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

A `Relationship` is: `{relationship_type, supporting_evidence: list[Evidence], relationship_probability, relationship_confidence}`.

### 3.2 Provenance Tagging & Namespaced Confidence

**Provenance labels**
- `OBSERVED` — direct ground-truth fact extracted verbatim from raw incident data (e.g. a normalized phone number, a verified timestamp).
- `INFERRED` — derived via heuristic, NLP extraction, or semantic embedding (e.g. an extracted `urgency_pressure` score, tactic classification).
- `PREDICTED` — emitted by an ML statistical model prior to deterministic verification (e.g. a candidate clustering hypothesis, a raw similarity ranking).

**Namespaced confidence fields** — no field is ever named bare `confidence` past Phase 2:

| Field | Meaning | Consumer / visibility |
|---|---|---|
| `extraction_confidence` | How sure the Scam DNA extractor is about the fields it pulled out | Backend / diagnostics |
| `resolution_confidence` | How sure the entity resolver is that two mentions are the same canonical entity | Entity engine / evidence |
| `relationship_probability` | Raw ML-predicted likelihood, pre-verification | **Internal ML only — never shown to an investigator on its own** |
| `relationship_confidence` | Confidence *after* the deterministic evidence engine verifies it | Investigator-facing UI |
| `campaign_confidence` | Confidence in the campaign grouping as a whole, aggregated from `relationship_confidence` values | Investigator-facing UI |

**Hard rule:** `relationship_probability` alone can never populate an investigator-visible field. Only `relationship_confidence` (which requires independent, deterministic evidence) can.

### 3.3 Locked Behavioral & Infrastructure Taxonomy

```python
from enum import Enum

class SocialEngineeringTactic(str, Enum):
    URGENCY_PRESSURE = "urgency_pressure"
    AUTHORITY_IMPERSONATION = "authority_impersonation"
    FEAR_INDUCTION = "fear_induction"
    ARTIFICIAL_SCARCITY = "artificial_scarcity"
    TRUST_BUILDING = "trust_building"
    ISOLATION_TACTIC = "isolation_tactic"          # e.g. "don't tell anyone / don't inform bank or family"
    CREDENTIAL_HARVESTING = "credential_harvesting"
    PAYMENT_REDIRECTION = "payment_redirection"
    # extend as the synthetic dataset (Phase 3) reveals real patterns

class ImpersonationTarget(str, Enum):
    BANK = "bank"
    GOVERNMENT_TAX = "government_tax"
    LAW_ENFORCEMENT = "law_enforcement"
    TELECOM = "telecom"
    DELIVERY_COURIER = "delivery_courier"
    FAMILY_MEMBER = "family_member"
    EMPLOYER = "employer"
    TECH_SUPPORT = "tech_support"
    OTHER = "other"          # escape hatch — pairs with a free-text note field

class PaymentMethod(str, Enum):
    UPI = "upi"
    BANK_TRANSFER = "bank_transfer"
    GIFT_CARD = "gift_card"
    CRYPTO = "crypto"
    CASH_PICKUP = "cash_pickup"
    WALLET_APP = "wallet_app"
    OTHER = "other"
```

The Phase 4 LLM extractor **classifies into these enums — it does not generate free text for these fields.** This is what makes Phase 7's "shared social-engineering tactics" a deterministic set-intersection instead of an LLM judgment call.

### 3.4 Full Scam DNA Schema

```python
from typing import List, Optional
from pydantic import BaseModel, Field

class ScamDNA(BaseModel):
    language: str
    channel: str
    impersonation_target: ImpersonationTarget
    impersonation_target_detail: Optional[str] = None
    urgency: float = Field(ge=0.0, le=1.0)
    fear: float = Field(ge=0.0, le=1.0)
    authority_pressure: float = Field(ge=0.0, le=1.0)
    credential_request: bool
    payment_request: bool
    payment_method: PaymentMethod
    requested_action: str
    social_engineering_tactics: List[SocialEngineeringTactic]
    target_type: str
    script_features: List[str] = Field(default_factory=list)
    infrastructure_indicators: List[str] = Field(default_factory=list)
    phone_numbers: List[str] = Field(default_factory=list)
    upi_ids: List[str] = Field(default_factory=list)
    urls: List[str] = Field(default_factory=list)
    domains: List[str] = Field(default_factory=list)
    emails: List[str] = Field(default_factory=list)
    extraction_confidence: float = Field(ge=0.0, le=1.0)
```

Not fixed — revise if engineering analysis during Phase 3/4 shows a better structure, but **keep the enum fields closed-set.**

---

## 4. CROSS-CUTTING CONSTRAINTS (apply from Phase 1 onward — never deferred)

These five constraints are active starting in Phase 1 and are non-negotiable architectural gates. A phase is **not done** if it violates any of these, even if its own local tests pass.

1. **Untrusted input defense.** Any phase feeding incident text to an LLM treats that text as adversarial data. It must never alter system instructions. A prompt-injection test harness exists from Phase 1, not Phase 15.
2. **PII-safe logging.** No raw identifier (phone, UPI, email, URL) may ever be logged, including in debug logs. All logging layers pass identifiers through HMAC-SHA256 hashing/tokenization. A hashing helper exists from Phase 1.
3. **Provenance tagging.** Every AI-derived field carries exactly one of `OBSERVED | INFERRED | PREDICTED`.
4. **Namespaced confidence.** No field is ever named bare `confidence` past Phase 2 (see §3.2). `relationship_probability` is never shown to investigators directly.
5. **100% offline fallback.** Every phase touching an external API (LLM, embeddings) is independently runnable in fallback/mock mode from the phase it's introduced in. The application must remain fully functional with zero internet connectivity via deterministic local mock providers.

---

## 5. CAMPAIGN DETECTION SIGNALS

1. Shared phone
2. Shared UPI
3. Shared URL/domain
4. Similar Scam DNA (enum overlap)
5. Semantic similarity (embeddings)
6. Temporal proximity
7. Shared impersonation target
8. Shared behavioral tactics

**Hybrid system:** ML ranking (produces `relationship_probability`) + deterministic evidence verification (produces `relationship_confidence`). No single model is responsible for the final decision. A shared keyword must never be sufficient on its own.

---

## 6. TARGET TECHNOLOGY STACK

- **Frontend:** React 18 + TypeScript, Tailwind CSS, React Flow (graph visualization), Recharts, Lucide Icons.
- **Backend:** Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0.
- **Storage & indexing:** PostgreSQL with pgvector extension (SQLite local-file fallback acceptable for MVP/test isolation), Redis for edge/query caching.
- **AI & NLP:** Gemini API (or configurable LLM provider) with a deterministic `MockLLMProvider` fallback; closed-taxonomy JSON schema enforcement.
- **ML & embeddings:** scikit-learn initially (cosine similarity, density clustering), sentence-transformers or a local embedding mock; PyTorch only if genuinely necessary.
- **Graph engine:** NetworkX initially — in-memory graph construction, Louvain community detection, topological centrality; a graph database only if required later.
- **Deployment & ops:** Docker, Docker Compose, structured JSON logging, Prometheus-compatible latency/cost tracking, request tracing, AI-call metrics.

---

## 7. CRITICAL DEMO REQUIREMENT (mandatory)

**TRUE CAMPAIGN:** three or more incidents that appear unrelated but actually belong to the same synthetic campaign.

**FALSE SIMILARITY:** at least one incident with similar words/intent that belongs to a *different* campaign. The system must correctly avoid over-clustering it.

### Primary demo story

Investigator sees Incident A, B, C — they appear unrelated. ScamTrap analyzes them: Scam DNA generated, entities normalized, similarity calculated, campaign graph appears. System announces **EMERGING CAMPAIGN DETECTED**. A deliberately similar but unrelated incident is introduced — system rejects it. Investigator asks "Why are these incidents connected?" — the Evidence-Bounded Investigator explains the exact evidence.

---

## 8. SUCCESS CRITERIA

1. User can ingest a scam incident.
2. Scam DNA is generated.
3. Entities are extracted and normalized.
4. Similar incidents can be discovered.
5. Campaign graph renders.
6. Campaign clusters are detected.
7. False similarity is rejected.
8. Evidence can be inspected.
9. Investigator explanation works.
10. Evaluation metrics can be displayed.
11. AI failure has graceful fallback.
12. Demo can run reliably without internet if fallback mode is enabled.

---

## 9. DEVELOPMENT METHOD & REPORTING FORMAT

Build in phases. **Do not jump ahead.** Complete one phase, run tests, validate architecture, then move to the next. Do not rewrite working components unnecessarily.

Execute sequentially, one phase at a time. After completing each phase, stop and output a status report in exactly this format:

```
### Phase [X] Completion Report
- Files Created: [list of new files with paths]
- Files Modified: [list of modified files]
- Architectural Changes: [summary of structural changes]
- Tests Executed & Results: [test output, coverage, verification metrics]
- Cross-Cutting Constraint Audit:
  - Untrusted Input Sanitization: [Pass/Fail]
  - PII-Safe Logging: [Pass/Fail]
  - Provenance Tagging: [Pass/Fail]
  - Namespaced Confidence: [Pass/Fail]
  - Offline Fallback Readiness: [Pass/Fail]
- Remaining Risks: [identified technical debt or edge cases]
- Next Phase: [explicit next phase target]
```

---

## 10. PHASES

**Phase 1 — Repository & architecture foundation**
Scaffold `backend/`, `frontend/`, `data/`, `tests/`, `docs/`, `scripts/`.
Backend: FastAPI application factory, structured error handling, CORS, configuration system, env var handling, health endpoint, structured JSON logging.
- `backend/app/core/security.py` — HMAC-SHA256 PII hashing utility.
- `backend/app/core/sanitizer.py` — input guardrail and prompt-injection test harness.
- `backend/app/core/logging.py` — structured JSON logger enforcing automatic identifier redaction.
Frontend: React + TypeScript + Vite, Tailwind, routing, application shell, dashboard placeholder, dark cybersecurity/SOC visual design system.
Infrastructure: Docker config, docker-compose, `.env.example`, README, dev instructions.
**Also implement here (pulled forward per §4):** prompt-injection test harness, PII-hashing helper — available to every later phase.
Docs: `docs/architecture.md` (system architecture, data flow, AI/ML boundaries, security boundaries, future production architecture), `docs/decisions.md` (architecture decisions + reasons).
Gate check: pytest suite passes; health endpoint returns 200 OK; frontend starts; Docker config syntactically valid; PII sanitizer and injection harness verified.
Do NOT build yet: LLM, embeddings, graph, Scam DNA, campaign detection, copilot, complex database models.
**STOP after Phase 1.**

**Phase 2 — Domain model & database**
Strongly typed models for: Incident, ScamDNA, Entity, EntityMention, Relationship, Campaign, Evidence, RiskAssessment, Investigation.
**Define here, canonically (per §3):** the `Evidence` object, namespaced confidence fields, and the closed-enum taxonomies (`SocialEngineeringTactic`, `ImpersonationTarget`, `PaymentMethod`). No later phase redefines these.
Every AI-derived field distinguishable via `OBSERVED | INFERRED | PREDICTED`.
Database: PostgreSQL if configured, else SQLite locally without changing domain logic. SQLAlchemy 2.0, migrations if appropriate.
Indexes: incident timestamp, phone number, UPI, URL, domain, campaign ID, relationship, embedding reference.
Gate check: CRUD tests pass; relationship tests pass; invalid enums fail validation; provenance tests pass; evidence schema cannot be mutated downstream; campaign membership tests pass.
**STOP after Phase 2.**

**Phase 3 — Synthetic dataset & ground truth**
10–20 synthetic scam campaigns, each with multiple incidents. Include Tamil-English code-switching, Hindi-English code-switching, English, paraphrased messages, different scam scripts, shared phones/UPIs/URLs/domains, temporal patterns, different victims/wording.
**Required negative examples:** incidents using similar words/tactics (KYC mentions, bank-blocking threats, payment requests) that belong to *different* campaigns — false-similarity cases. Mandatory, not optional.
Ground truth: every incident carries hidden `campaign_id` metadata, never shown to the normal investigator UI.
Dataset size: 200–500 incidents. Deterministic generator (fixed random seed).
Output: `data/generator.py`, `data/seed/`, documentation on campaign generation, entity reuse, language generation, ground truth, negative cases.
Gate check: validation script confirms campaign count, incident count, shared-entity ratios, true-relationship count, false-relationship (negative control) balance. Run it.
**STOP after Phase 3.**

**Phase 4 — Multilingual Scam DNA extraction**
Architecture: Incident → LLM → structured Pydantic ScamDNA. Provider abstraction `LLMProvider` supporting a `GeminiProvider` and a `MockLLMProvider` — never hardcode Gemini throughout the app.
Extraction: all ScamDNA fields (§3.4), **classified into the Phase 2 taxonomy enums, not emitted as free text.**
LLM output validated through Pydantic with schema repair; invalid output rejected/repaired.
Reliability: retry safely, log failure, fall back to mock mode, never crash the app.
Prompt injection: incident text is untrusted data (per §4), never allowed to modify system instructions.
**Fallback/offline mode is a first-class test target starting here**, not retrofitted later.
Gate check: extraction tests pass on English, Tamil-English, and Hindi-English samples; malformed LLM output handled; missing fields handled; malicious prompt injection blocked; provider failure triggers seamless mock fallback.
**STOP after Phase 4.**

**Phase 5 — Entity extraction & resolution**
Normalize repeated identifiers for phone, UPI, URL, domain, email — e.g. `+91 98765 43210`, `9876543210`, `91-98765-43210` → one canonical PHONE entity (E.164: `+919876543210`). UPI: handle parsing and casing normalization. URL/domain: subpath and query-string stripping, canonical domain extraction.
`EntityResolver` produces: canonical entity ID, entity type, normalized value, source mentions, `resolution_confidence`.
Security: don't expose raw sensitive-looking values unnecessarily in logs; hash/tokenize per §4.
Gate check: formatting differences resolve correctly, duplicate identifiers deduplicate, invalid identifiers rejected, near-matches and international formats handled, false matches avoided, zero raw PII leaks to logs.
**STOP after Phase 5.**

**Phase 6 — Semantic embeddings & ML similarity**
No keyword matching. Embed Scam DNA + normalized behavioral features (tactics, target, script traits), not raw message text.
`EmbeddingService`, `SimilarityService` — configurable embedding provider, local/mock fallback, cosine similarity, top-K candidate retrieval. Use pgvector if available, else a clean abstraction that can adopt it later.
Similarity output includes: similarity score, compared features, model version, timestamp.
Evaluation tests: same-campaign paraphrases, same-words-different-campaigns, different languages, different tactics. Optimize for useful discrimination, not just high similarity.
Metrics: precision, recall, F1 for relationship prediction on the ground-truth dataset.
Gate check: embeddings show high similarity for same-campaign paraphrases and low similarity for negative controls.
**STOP after Phase 6.**

**Phase 7 — Hybrid campaign relationship engine**
Candidate features: shared phone, shared UPI, shared URL, shared domain, Scam DNA similarity (enum overlap), semantic embedding similarity, temporal proximity, shared impersonation target, shared social-engineering tactics.
Architecture:
- **Candidate generation (ML):** compute `relationship_probability` via behavioral embeddings, temporal proximity, and tactic overlaps.
- **Deterministic verification:** corroborate candidates using exact infrastructure matches (shared UPI/phone) and taxonomy set-intersections to produce `relationship_confidence` + populate `Evidence` records (per §3). **ML alone can never create an investigator-visible high-confidence relationship.**
Output relationship contains: `relationship_probability`, `relationship_confidence`, supporting `Evidence` list, feature contributions, explanation.
False-positive protection: high-confidence relationships require independent evidence; a shared keyword is never enough.
Evaluation: precision, recall, F1, false relationship rate, false campaign rate. Generate an evaluation report.
Gate check: verify that high ML probability alone cannot produce an investigator-visible relationship without deterministic evidence.
**STOP after Phase 7.**

**Phase 8 — Campaign graph engine**
Nodes: Incident, Phone, UPI, URL, Domain, Scam DNA, Campaign.
Edges: `USES_PHONE`, `USES_UPI`, `USES_URL`, `USES_DOMAIN`, `SIMILAR_TO`, `RELATED_TO`, `MEMBER_OF`, `TEMPORALLY_NEAR`.
NetworkX-based `GraphBuilder`, `GraphQueryService`, `GraphAnalyticsService`. Analytics: connected components, community detection (Louvain), node degree, relationship strength, campaign density.
The graph is computationally generated from the relationship engine — visualization is not the innovation by itself.
API-ready output: graph JSON for React Flow, with evidence metadata on edges.
Gate check: graph creation/update tests pass, relationship insertion works, campaign clusters form correctly, false similarity rejected, subgraph queries return complete node-edge collections with intact evidence chains.
**STOP after Phase 8.**

**Phase 9 — Campaign detection & early warning**
Detect emerging campaigns from: number of related incidents, relationship confidence, shared infrastructure, semantic similarity, temporal density, graph density.
Configurable threshold system (e.g. 3+ related incidents + strong relationship evidence → `EMERGING_CAMPAIGN_DETECTED`) — **do not hardcode numbers throughout the code; treat these as provisional until Phase 9.5 calibrates them.**
Campaign object: campaign ID, incident count, entity count, `campaign_confidence`, first seen, latest seen, risk, evidence, status.
UI-ready alert payload with structured evidence.
Evaluation: time-to-detection, campaign precision, campaign recall, false campaign rate.
Gate check: automated alerts trigger correctly on multi-incident synthetic campaigns.
**STOP after Phase 9.**

**Phase 9.5 — Threshold calibration** *(inserted per real-world precedent: no production fraud system ships an unvalidated threshold)*
Run the Phase 9 detection logic against the full Phase 3 ground-truth dataset. Grid-sweep the incident-count threshold (N ∈ [2, 5]) and the evidence/confidence threshold (C ∈ [0.60, 0.95]) together. For each combination compute campaign precision, recall, F1, and false-campaign rate. Select the combination maximizing F1 while keeping false-campaign rate near zero. Record the chosen thresholds **and the sweep results that justify them** in `docs/decisions.md`.
Do not hardcode any detection threshold anywhere in the codebase before this phase has run.
Gate check: zero hardcoded, unvalidated magic numbers remain in detection logic.
**STOP after Phase 9.5.**

**Phase 10 — Evidence & explainability engine**
`EvidenceService` answers "why are these incidents connected?" using the canonical `Evidence` object from Phase 2 — **this phase populates and queries it; it does not redefine the schema.**
Example output: Observed — same UPI ID, same phone number, 42-minute temporal proximity. Inferred — Scam DNA similarity = 0.91. Predicted — campaign probability = 0.94.
Never convert inferred information into observed information. Never claim criminal identity. Never claim certainty when only probability exists.
UI payload per claim: claim, type, source, confidence, supporting records, timestamp.
Gate check: verification test confirms inferred attributes are never returned as observed facts; provenance cannot be accidentally changed.
**STOP after Phase 10.**

**Phase 11 — Evidence-Bounded Investigator Copilot**
Not a generic chatbot. Answers investigator questions using only stored evidence (incident data, graph relationships, `Evidence` records, scoring factors), then generates a concise explanation.
Hard restrictions: must not invent evidence, create new entities, accuse individuals, claim criminal guilt, fabricate relationships, or use information outside the investigation. If evidence is insufficient: reply "Insufficient evidence."
Every important claim cites an incident ID, entity ID, or relationship ID.
Gate check: supported questions answer correctly; unsupported/insufficient-evidence questions return "Insufficient evidence"; adversarial and prompt-injection queries are rejected safely.
**STOP after Phase 11.**

**Phase 12 — FastAPI application (production-ready gateway)**
Endpoints:
- `POST /api/v1/incidents` — ingest incident transcript
- `GET /api/v1/incidents`
- `GET /api/v1/incidents/{id}`
- `GET /api/v1/incidents/{id}/dna`
- `GET /api/v1/incidents/{id}/relationships`
- `GET /api/v1/campaigns`
- `GET /api/v1/campaigns/{id}`
- `GET /api/v1/campaigns/{id}/graph`
- `POST /api/v1/investigations/explain`
- `GET /api/v1/metrics`
- `POST /api/v1/evaluation/run`
Pydantic request/response validation, structured errors, request IDs, logging, pagination. **Implement the authentication & authorization architecture in full per §10a — this is not deferred to Phase 15.**
Security: input validation, rate-limiting abstraction, CORS config, secrets via env vars, no secrets in logs.
Gate check: full API test suite passes with complete request/response validation.
**STOP after Phase 12.**

### §10a — Authentication & Authorization Architecture (implemented in Phase 12, audited in Phase 15)

This is a SOC/investigator-facing system handling scam intelligence — treat auth as a first-class subsystem, not a stub. "Authentication-ready" is not an acceptable deliverable; the following must be implemented.

**Threat model this design targets:** credential stuffing / brute force, token theft & replay, session fixation, privilege escalation (investigator → admin), insider misuse without an audit trail, and long-lived tokens surviving a compromised device.

**1. Identity & credential storage**
- `User` model: `id`, `email`, `password_hash`, `role`, `mfa_secret` (nullable, encrypted at rest), `mfa_enabled`, `failed_login_count`, `locked_until`, `last_login_at`, `is_active`, `created_at`.
- Passwords hashed with **Argon2id** (`passlib[argon2]` or `argon2-cffi`) — never bcrypt-only, never SHA-family. Minimum password policy enforced server-side (length ≥ 12, checked against a breached-password list such as HaveIBeenPwned's k-anonymity API or a local Pwned-Passwords dataset offline).
- No plaintext secrets in the database or logs — `mfa_secret` encrypted with a KMS-managed key or, for the hackathon build, a locally-held Fernet key sourced from env, never committed.

**2. Token architecture**
- **Short-lived JWT access tokens** (RS256 or EdDSA, asymmetric — never HS256 with a shared secret across services), 10–15 minute expiry, containing `sub`, `role`, `jti`, `iat`, `exp` only — no PII, no incident data in the token payload.
- **Rotating refresh tokens**, opaque (not JWT), stored server-side hashed (never store raw refresh tokens), 7–14 day expiry, **single-use with rotation-on-refresh**: each refresh call issues a new refresh token and invalidates the old one. Reuse of an already-rotated refresh token is treated as a compromise signal — invalidate the entire token family and force re-authentication.
- Access tokens delivered via `httpOnly`, `Secure`, `SameSite=Strict` cookies for the investigator console (not `localStorage`/`sessionStorage`, which are XSS-readable); a bearer-token mode is available separately for service-to-service and CI use only.
- `jti` (token ID) checked against a Redis-backed revocation list on every request, so logout / admin-forced revocation takes effect immediately rather than waiting for expiry.

**3. Role-based access control (RBAC)**
- Closed enum, not free text:
  ```python
  class Role(str, Enum):
      INVESTIGATOR = "investigator"   # read incidents/campaigns/evidence, query the copilot
      SUPERVISOR = "supervisor"       # investigator rights + campaign status changes, evaluation runs
      ADMIN = "admin"                 # user management, threshold calibration, system config
      AUDITOR = "auditor"             # read-only across everything, including audit logs
  ```
- Enforced via a FastAPI dependency (`require_role(Role.SUPERVISOR)`), not scattered `if` checks in route bodies. Every endpoint in Phase 12's list is explicitly annotated with its minimum required role — none are "implicitly open."
- `POST /api/v1/evaluation/run`, `POST /api/v1/investigations/explain` on another investigator's case, and any user-management or threshold-calibration endpoint require `SUPERVISOR` or `ADMIN` at minimum — never `INVESTIGATOR`.
- Deny-by-default: an endpoint with no explicit role dependency fails closed (403), not open.

**4. MFA**
- TOTP-based MFA (RFC 6238, e.g. `pyotp`), **mandatory for `ADMIN` and `SUPERVISOR` roles**, optional-but-encouraged for `INVESTIGATOR`. Backup codes issued at enrollment, hashed at rest, single-use.

**5. Brute-force & abuse protection**
- Per-account lockout after 5 failed attempts (exponential backoff, then a 15-minute lock), independent of per-IP rate limiting on `/auth/login` (e.g. 10 req/min/IP via the Phase 1 rate-limiting abstraction, backed by Redis).
- Every login attempt (success or failure), lockout event, MFA challenge, token refresh, and token-family revocation is written to an **immutable audit log** (`AuditEvent`: actor, action, target, ip_hash, user_agent_hash, timestamp, result) — IPs and user agents hashed per the §4 PII-safe logging rule, never stored raw.

**6. Session & lifecycle management**
- `POST /auth/login` (email + password → MFA challenge if enabled → token pair), `POST /auth/refresh` (rotate), `POST /auth/logout` (revoke current token family), `POST /auth/logout-all` (revoke all sessions for the user — exposed to the user themselves and to `ADMIN` for incident response), `GET /auth/sessions` (list active token families with device/IP metadata for user self-service).
- Idle timeout at the access-token layer (15 min) plus an absolute session ceiling at the refresh-token layer (14 days) enforced independent of activity.

**7. Service-to-service / offline-mode auth**
- Internal calls between the API gateway and worker processes (embedding service, LLM provider calls) use short-lived scoped service tokens, not the user's token, and never call out with investigator-level credentials.
- The Phase 4/6 `MockLLMProvider` and other offline fallbacks run under the same auth boundary — offline mode changes the AI backend, never the auth requirements.

**8. Adversarial test matrix (required before Phase 12 gate check passes, re-run in Phase 15)**
- Expired / malformed / tampered JWT rejected.
- Rotated refresh token replay triggers full family revocation.
- Role-escalation attempt (investigator token calling an admin-only route) returns 403 and is audit-logged.
- Lockout cannot be bypassed by varying case/whitespace in the email field or by distributing attempts across IPs against a single account.
- Session-fixation: a pre-login session/token cannot be "upgraded" to an authenticated one without a fresh login.
- Logout / logout-all actually revokes tokens server-side, verified by replaying a logged-out access token.

**Phase 13 — Investigator console (SOC-grade UI)**
Pages/components:
- **Dashboard** — incidents analyzed, active/emerging campaigns, high-confidence relationships, false-positive evaluation, system health.
- **Incident Analysis** — transcript viewer, language, Scam DNA breakdown, entity tokens, risk, evidence.
- **Campaign Graph** — interactive React Flow canvas with custom nodes; clicking an edge opens an evidence drawer.
- **Campaign Details** — confidence, incidents, entities, timeline, evidence, risk.
- **Copilot Console** — chat-style Evidence-Bounded Investigator Q&A with interactive citation badges.
- **Auth screens** — login (with MFA challenge step where enabled), session/device list with per-session revoke, and role-appropriate navigation (e.g. `INVESTIGATOR` never sees user-management or threshold-calibration screens, not just role-blocked but hidden).
Visual requirements: professional dark SOC/cybersecurity aesthetic — not a generic AI chatbot look. Prioritize clarity, hierarchy, graph visualization, evidence, confidence, timeline.
Demo requirement: graph animates smoothly; campaign alert is visually obvious.
Gate check: smooth rendering, interactive graph navigation, complete evidence-drawer integration.
**STOP after Phase 13.**

**Phase 14 — Comprehensive evaluation system**
Critical for winning. Using Phase 3's hidden ground truth, calculate precision/recall/F1 for: extraction, entity resolution, relationship detection, campaign detection. Safety metrics: false relationship rate, false campaign rate. Performance: average latency, P50/P95/P99 latency, LLM cost estimate. Business impact simulation: investigator triage time, manual vs. automated comparison, percentage reduction — **clearly labeled as simulated.**
Evaluation Dashboard UI: confusion matrix, precision/recall, campaign detection, false-similarity test, latency, cost.
Gate check: evaluation pipeline generates a structured scorecard across all test campaigns.
**STOP after Phase 14.**

**Phase 15 — Security, privacy & reliability (audit + hardening pass)**
Since §4's cross-cutting constraints already enforce prompt-injection defense, PII-safe logging, and provenance from Phase 1, **this phase audits and hardens rather than implementing from scratch.**
Confirm/complete: the §10a authentication & authorization system (token rotation, lockout, MFA enforcement for privileged roles), input validation, secure headers, CORS, rate limiting, secret management, audit logs, database access controls, LLM output validation. Run the full §10a adversarial test matrix (token replay, privilege escalation, lockout bypass, session fixation) as part of this phase's gate check.
AI safety audit: no unsupported accusations, evidence provenance intact everywhere, uncertainty preserved, no hallucinated relationships, fallback works when the model fails.
Reliability: retries, timeouts, circuit-breaker abstraction, fallback provider, deterministic demo mode.
Observability: API latency, LLM latency, LLM failures, embedding latency, relationship-calculation time, campaign-detection time, errors.
Synthetic-data boundary: display `DEMO / CONTROLLED ENVIRONMENT — SYNTHETIC DATA ONLY` prominently and persistently across the UI; make it impossible to imply hackathon data is real.
Gate check: system passes simulated network-failure and malicious-payload injection tests.
**STOP after Phase 15.**

**Phase 16 — Production architecture review**
High-value hardening only — do not overengineer. Review database indexing, query performance, caching, concurrency, async processing, model latency, embedding storage, graph performance, API scalability.
Document a production architecture in `docs/production-architecture.md`: API Gateway → ingestion → event queue (e.g. Kafka) → worker services (Celery/async) → PostgreSQL → pgvector → Redis → graph analytics → AI services → observability — without necessarily implementing every component. Document what's implemented vs. architecture-only, and why.
Gate check: performance benchmark verifies high throughput on concurrent incident ingestion.
**STOP after Phase 16.**

**Phase 17 — Deterministic live presentation engine (hackathon killer demo mode)**
Deterministic scenario for a 3-minute live presentation: Incidents A/B/C appear unrelated but share one UPI, related phone infrastructure, similar Scam DNA, temporal proximity. Incident D has similar language/tactics but different infrastructure and different ground-truth campaign.
Demo sequence:
1. Display three incidents.
2. Analyze — show Scam DNA generation.
3. Click "Discover Campaign."
4. Animate graph construction.
5. Show "Emerging Campaign Detected."
6. Show 3 incidents / 2 shared infrastructure indicators / high campaign confidence.
7. Introduce Incident D → "Not Connected" with explanation.
8. Ask "Why are these incidents connected?" → Evidence-Bounded Investigator responds with citation-backed explanation.
Must be fully deterministic — no dependency on unpredictable LLM responses — with a fallback mode, and must never depend on internet connectivity live.
Gate check: complete demo executes deterministically from cold container boot with network access disabled.
**STOP after Phase 17.**

**Phase 18 — Final validation, dual-mode regression & polish**
No new major functionality after this phase unless explicitly requested. Run unit, integration, API, frontend, evaluation, security, and performance tests.
Test scenarios: normal scam, Tamil-English scam, Hindi-English scam, same campaign, different campaign, false similarity, missing LLM, invalid LLM output, prompt injection, database failure, slow model, empty incident.
**Dual-mode regression (per §4):** run the full Phase 3–17 test suite twice — once against the live LLM provider, once against the fallback/mock provider. Campaign membership on the ground-truth set must not diverge between the two runs.
Performance: end-to-end latency, P95 latency, graph rendering, database query performance.
Demo reliability: verify the complete 3-minute demo from clean startup, repeatably.
UX polish: remove unnecessary screens/buttons/placeholder text/broken states/developer UI/irrelevant metrics; polish typography, spacing, graph, evidence panel, campaign alert, loading/error states, citation badges, loading skeletons.
Final docs: `README.md`, `docs/architecture.md`, `docs/decisions.md`, `docs/demo-script.md`, `docs/evaluation-report.md` (or `docs/evaluation.md`), `docs/security.md`, `docs/technical-deep-dive.md`.
Final report covers: architecture, features, AI/ML pipeline, evaluation metrics, security, scalability, known limitations, demo instructions, exact commands to run, recommended presentation sequence.
Gate check: complete test suite passes with zero warnings.
**Do not add new features after this phase unless explicitly requested.**

---

## 11. IMPORTANT — EXECUTION INSTRUCTION

Do not implement all phases now. Start ONLY with **Phase 1**, using §4's cross-cutting constraints as acceptance criteria in addition to Phase 1's own requirements. After completing Phase 1, report using the format in §9 and stop — wait for the instruction to proceed to Phase 2.