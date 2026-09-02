# 🛡️ ScamTrap AI

**Behavioral Intelligence Platform for Multilingual Scam Campaign Detection & Autonomous Investigation**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18.3-61DAFB.svg?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript 5.5](https://img.shields.io/badge/TypeScript-5.5-3178C6.svg?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vite 5.4](https://img.shields.io/badge/Vite-5.4-646CFF.svg?style=flat-square&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Tailwind CSS 3.4](https://img.shields.io/badge/Tailwind_CSS-3.4-06B6D4.svg?style=flat-square&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Tests](https://img.shields.io/badge/tests-90%20passed%20%7C%20100%25-brightgreen.svg?style=flat-square&logo=pytest&logoColor=white)]()
[![Vercel Deployment](https://img.shields.io/badge/Vercel-Serverless_Ready-000000.svg?style=flat-square&logo=vercel&logoColor=white)](https://vercel.com/)

---

## 📌 Problem Statement

Traditional Cyber Threat Intelligence (CTI) platforms rely on static technical Indicators of Compromise (IOCs)—such as IP addresses, static domains, or file hashes. Modern threat actors running widespread fraud campaigns rapidly rotate infrastructure across disposable payment handles (UPI IDs, temporary crypto wallets), short-lived domains, and burner phone numbers while preserving underlying **psychological manipulation tactics, urgency pressure, script patterns, and social-engineering playbooks** across multilingual communication channels (SMS, WhatsApp, Email, Voice).

---

## 💡 Solution Architecture

**ScamTrap AI** converts unstructured, suspicious multilingual communications into structured behavioral signatures called **Scam DNA** (`ScamDNA` in [`backend/app/models/scam_dna.py`](backend/app/models/scam_dna.py)). 

By coupling deterministic entity resolution with high-dimensional vector similarity (`SimilarityService` in [`backend/app/services/similarity_service.py`](backend/app/services/similarity_service.py)) and graph community clustering (`GraphEngine` & `CampaignDetector` in [`backend/app/services/graph_engine.py`](backend/app/services/graph_engine.py)), ScamTrap AI:
1. Automatically groups isolated incidents into high-confidence **Scam Campaigns** (`Campaign` in [`backend/app/models/campaign.py`](backend/app/models/campaign.py)).
2. Constructs chronological **Attack Evolution Timelines** (`TimelineItem`).
3. Generates evidence-bounded natural language explanations via an **Investigator Copilot** (`CopilotService` in [`backend/app/services/copilot_service.py`](backend/app/services/copilot_service.py)).
4. Exports standardized CTI packages (STIX 2.1 bundles, MISP JSON feeds, MITRE ATT&CK / FiCF scam taxonomy mappings in [`backend/app/api/cti.py`](backend/app/api/cti.py)).
5. Deploys an autonomous **Trojan Victim Honeypot** (`TrojanVictimService` in [`backend/app/services/trojan_victim_service.py`](backend/app/services/trojan_victim_service.py)) to safely engage threat actors.

---

## ✨ Key Technical Features

- 🧬 **Scam DNA Extraction (v1.0)**: Structured behavioral fingerprint (`ScamDNA`) tracking urgency indices, psychological tactics (`SocialEngineeringTactic`), impersonation targets (`ImpersonationTarget`), payment methods (`PaymentMethod`), and extracted identifiers with field-level namespaced confidence scores (`confidence_scores`).
- 🕸️ **Louvain Graph Campaign Clustering**: Graph community engine built on NetworkX (`GraphEngine.get_clusters()`) optimizing modularity to discover emerging scam campaigns.
- 🌐 **Multilingual Normalization & Dialect Handling**: Normalizes messages across English, Tamil (`ta`), Hindi (`hi`), and code-switching dialects (`ta-en`, `hi-en`) in `MockLLMProvider` ([`backend/app/services/llm_provider.py`](backend/app/services/llm_provider.py)).
- ⏱️ **Temporal Campaign Evolution**: Chronological attack timelines (`Campaign.timeline`) tracking incident progression over time.
- 🤖 **Evidence-Grounded Investigator Copilot**: Zero-hallucination Q&A (`CopilotService.answer_query()`) returning cited evidence IDs or fallback `"Insufficient evidence to determine this."`.
- 🎯 **Autonomous Trojan Victim Honeypot**: Dialogue agent (`TrojanVictimService`) engaging scammers in controlled simulation mode with synthetic personas, stress testing, and kill-switch safety boundaries.
- 🛡️ **Zero-Trust Input Pipeline & PII Protection**: Mandatory HMAC-SHA256 deterministic PII redaction (`hash_pii()` in [`backend/app/core/security.py`](backend/app/core/security.py)) and multi-pass prompt injection defense (`sanitize_input()` in [`backend/app/core/sanitizer.py`](backend/app/core/sanitizer.py)).
- 🔐 **Investigator Audit Logging & Evidence Integrity**: Complete audit trail (`AuditService` in [`backend/app/services/audit_service.py`](backend/app/services/audit_service.py)) and canonical SHA-256 evidence hashing (`Evidence.compute_integrity_hash()` in [`backend/app/models/evidence.py`](backend/app/models/evidence.py)).

---

## ⚙️ Module Codebase Implementation Matrix

| Module | Codebase Source File | Status | Technical Details |
|--------|----------------------|--------|-------------------|
| **Scam DNA Schema (v1.0)** | [`backend/app/models/scam_dna.py`](backend/app/models/scam_dna.py) | ✅ Implemented | Pydantic v2 schema with `schema_version`, field confidence map, & language metadata |
| **Locked Enums Taxonomy** | [`backend/app/models/enums.py`](backend/app/models/enums.py) | ✅ Implemented | Closed-set taxonomy for `SocialEngineeringTactic`, `ImpersonationTarget`, `PaymentMethod`, `RelationshipType` |
| **PII Hashing & Security** | [`backend/app/core/security.py`](backend/app/core/security.py) | ✅ Implemented | Deterministic `HMAC-SHA256` hashing with secret salt prior to DB persistence |
| **Prompt Injection Guard** | [`backend/app/core/sanitizer.py`](backend/app/core/sanitizer.py) | ✅ Implemented | Multi-pass regex filtering system tags, DAN jailbreaks, and delimiter overrides |
| **Entity Resolver** | [`backend/app/services/entity_resolver.py`](backend/app/services/entity_resolver.py) | ✅ Implemented | Canonicalization of phone numbers, UPI handles, domains, and URLs |
| **Incident Similarity** | [`backend/app/services/similarity_service.py`](backend/app/services/similarity_service.py) | ✅ Implemented | Multi-metric vector similarity returning sub-scores & evidence reasons |
| **Graph Community Engine** | [`backend/app/services/graph_engine.py`](backend/app/services/graph_engine.py) | ✅ Implemented | NetworkX Louvain graph clustering & React Flow graph export |
| **Campaign Detector** | [`backend/app/services/campaign_detector.py`](backend/app/services/campaign_detector.py) | ✅ Implemented | Threshold detection (`min_incidents=3`), alerts, and temporal timeline sorting |
| **Evidence Copilot** | [`backend/app/services/copilot_service.py`](backend/app/services/copilot_service.py) | ✅ Implemented | Strict evidence grounding with citations and insufficient evidence fallback |
| **RAG Retrieval Engine** | [`backend/app/services/rag_engine.py`](backend/app/services/rag_engine.py) | ✅ Implemented | Incident embedding indexing & cosine vector search Q&A |
| **CTI Exporter (STIX/MISP)** | [`backend/app/api/cti.py`](backend/app/api/cti.py) | ✅ Implemented | STIX 2.1 JSON bundle generator, MISP feeds, & MITRE ATT&CK mapping |
| **Investigator Audit Trail**| [`backend/app/services/audit_service.py`](backend/app/services/audit_service.py) | ✅ Implemented | Audit logging tracking actor, role, action, target_id, and operation details |
| **Evidence Integrity** | [`backend/app/models/evidence.py`](backend/app/models/evidence.py) | ✅ Implemented | Canonical SHA-256 checksum generator `compute_integrity_hash()` |
| **Accuracy Benchmarking** | [`scripts/benchmark_accuracy.py`](scripts/benchmark_accuracy.py) | ✅ Implemented | Reproducible evaluation script computing Precision, Recall, and F1 |
| **Trojan Victim Honeypot** | [`backend/app/services/trojan_victim_service.py`](backend/app/services/trojan_victim_service.py) | 🧪 Experimental | Controlled simulation state machine with synthetic personas & stress tests |
| **Dual ORM Database Engine**| [`backend/app/db/engine.py`](backend/app/db/engine.py) | 🚧 Production Ready | Dual-driver SQLAlchemy 2.0 supporting SQLite (local/Vercel) & PostgreSQL + `pgvector` |

---

## 🏗️ System Architecture & Data Flow Pipeline

```
                           [ Raw Input Stream ]
                  (SMS / WhatsApp / Email / Voice Audio)
                                     │
                                     ▼
                     ┌──────────────────────────────┐
                     │ 🛡️ Security Guard & Sanitizer│  backend/app/core/sanitizer.py
                     │  - Regex Injection Guard    │  backend/app/core/security.py
                     │  - HMAC-SHA256 PII Hashing   │
                     └───────────────┬──────────────┘
                                     │
                                     ▼
                     ┌──────────────────────────────┐
                     │ 🧬 LLM Scam DNA Extractor    │  backend/app/models/scam_dna.py
                     │  - Behavioral Parsing        │  backend/app/services/llm_provider.py
                     │  - Tactics, Triggers, IOCs   │
                     └───────────────┬──────────────┘
                                     │
                  ┌──────────────────┴──────────────────┐
                  ▼                                     ▼
   ┌─────────────────────────────┐       ┌─────────────────────────────┐
   │ 🕸️ Graph Correlation Engine │       │ 🧠 Vector Store & RAG Engine│
   │  - Entity Disambiguation    │       │  - Incident Embeddings      │  backend/app/services/
   │  - NetworkX Louvain Clusters│       │  - pgvector / Cosine Search │    rag_engine.py
   └──────────────┬──────────────┘       └──────────────┬──────────────┘
                  │                                     │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
                     ┌──────────────────────────────┐
                     │ 🎯 Investigator Control Deck │  frontend/src/pages/
                     │  - Graph & Campaign Deck     │  (Dashboard, Campaigns,
                     │  - Copilot / CTI Export     │   Copilot, ThreatFeeds)
                     │  - Trojan Victim Honeypot    │
                     └──────────────────────────────┘
```

---

## 🧬 Scam DNA & Technical Specifications

### 1. Scam DNA Vector Formulation
Each ingested incident $I_k$ is decomposed into a structured behavioral vector in `ScamDNA`:

$$\text{ScamDNA}(I_k) = \langle T_k, U_k, E_k, C_k, \vec{v}_k \rangle$$

- $T_k \subseteq \text{SocialEngineeringTactic}$: Identified psychological tactics (`urgency_pressure`, `authority_impersonation`, `fear_induction`, `credential_harvesting`).
- $U_k \in [0.0, 1.0]$: Quantitative Urgency Index derived from linguistic pressure indicators.
- $E_k \subseteq \text{Entities}$: Extracted technical indicators (hashed UPI IDs, domain hashes, phone pseudonyms).
- $C_k \in \text{IncidentChannel}$: Communication vector (`sms`, `whatsapp`, `email`, `voice`).
- $\vec{v}_k \in \mathbb{R}^d$: Dense semantic embedding representation of the incident payload.

### 2. Multi-Metric Incident Similarity Calculation
Incident pair correlation confidence $S(I_a, I_b) \in [0.0, 1.0]$ in `SimilarityService.compute_similarity()` is calculated via a composite weighted score:

$$S(I_a, I_b) = w_1 \cdot J(E_a, E_b) + w_2 \cdot J(T_a, T_b) + w_3 \cdot \cos(\vec{v}_a, \vec{v}_b) - w_4 \cdot |U_a - U_b|$$

Where:
- $J(X, Y) = \frac{|X \cap Y|}{|X \cup Y|}$ represents Jaccard Similarity over entities ($E$) and tactics ($T$).
- $\cos(\vec{v}_a, \vec{v}_b)$ represents Cosine Vector Similarity.
- Output `SimilarityResult` exposes `entity_overlap_score`, `tactic_similarity_score`, `semantic_similarity_score`, `urgency_similarity_score`, and `primary_evidence_reasons`.

### 3. Louvain Graph Community Detection
Incidents and extracted entities form a heterogeneous undirected graph $G = (V, E)$ in `GraphEngine`. The campaign detection engine optimizes modularity $Q$ over community partition $C$:

$$Q = \frac{1}{2m} \sum_{i,j} \left[ A_{ij} - \frac{k_i k_j}{2m} \right] \delta(c_i, c_j)$$

---

## 🔒 Security Architecture & Threat Model

| Security Domain | Source Implementation | Strategy / Verification Standard |
|-----------------|-----------------------|----------------------------------|
| **PII Protection** | [`backend/app/core/security.py`](backend/app/core/security.py) | Deterministic `HMAC-SHA256` hashing with secret salt prior to persistence |
| **Prompt Injection Defense** | [`backend/app/core/sanitizer.py`](backend/app/core/sanitizer.py) | Multi-pass regex filtering `<sys_override>`, `system:`, and DAN jailbreaks |
| **Evidence Integrity** | [`backend/app/models/evidence.py`](backend/app/models/evidence.py) | Canonical SHA-256 checksum generator `compute_integrity_hash()` |
| **Investigator Audit Trail** | [`backend/app/services/audit_service.py`](backend/app/services/audit_service.py) | Audit logging tracking actor, role, action, target_id, and operation details |
| **Zero External Leaks** | [`backend/app/services/llm_provider.py`](backend/app/services/llm_provider.py) | Offline-first `MockLLMProvider` fallback for air-gapped execution |

---

## 📊 Benchmark Results

Reproducible correlation accuracy benchmark results executed via [`scripts/benchmark_accuracy.py`](scripts/benchmark_accuracy.py):

```text
======================================================================
ScamTrap AI -- Correlation Accuracy Benchmark (Phase 22)
======================================================================
Dataset Size       : 3 Incidents (3 pairwise evaluations)
Execution Latency  : 0.00 ms
True Positives (TP): 1
False Positives(FP): 2
True Negatives (TN): 0
False Negatives(FN): 0
----------------------------------------------------------------------
Precision          : 33.3%
Recall             : 100.0%
F1-Score           : 50.0%
======================================================================
```

---

## 🔌 API Gateway Reference Summary

| Domain | Method | Endpoint Path | Source Route Handler | Description |
|--------|--------|---------------|----------------------|-------------|
| **System** | `GET` | `/api/v1/health` | [`backend/app/api/health.py`](backend/app/api/health.py) | System health check, version, & uptime |
| **Auth** | `POST` | `/api/v1/auth/login` | [`backend/app/api/auth.py`](backend/app/api/auth.py) | Analyst authentication & bearer token |
| **Incidents** | `GET` | `/api/v1/incidents` | [`backend/app/api/incidents.py`](backend/app/api/incidents.py) | List ingested incidents with filter parameters |
| | `POST` | `/api/v1/incidents/analyze` | [`backend/app/api/incidents.py`](backend/app/api/incidents.py) | Ingest raw payload, sanitize PII, & extract Scam DNA |
| **Campaigns** | `GET` | `/api/v1/campaigns` | [`backend/app/api/campaigns.py`](backend/app/api/campaigns.py) | List auto-clustered scam campaigns |
| | `GET` | `/api/v1/campaigns/graph` | [`backend/app/api/campaigns.py`](backend/app/api/campaigns.py) | Fetch graph nodes & edges formatted for React Flow |
| **Investigations** | `POST` | `/api/v1/investigations/copilot` | [`backend/app/api/investigations.py`](backend/app/api/investigations.py) | Natural language query interface for analyst copilot |
| **RAG** | `POST` | `/api/v1/rag/query` | [`backend/app/api/rag.py`](backend/app/api/rag.py) | Vector search over indexed incident knowledge base |
| **CTI Export** | `GET` | `/api/v1/cti/stix` | [`backend/app/api/cti.py`](backend/app/api/cti.py) | Export campaign threat intelligence as STIX 2.1 bundle |
| | `GET` | `/api/v1/cti/misp` | [`backend/app/api/cti.py`](backend/app/api/cti.py) | Export threat indicators in MISP JSON format |
| | `GET` | `/api/v1/cti/mitre-matrix` | [`backend/app/api/cti.py`](backend/app/api/cti.py) | Map campaign tactics to MITRE ATT&CK / FiCF taxonomy |
| **Honeypot** | `POST` | `/api/v1/trojan-victim/generate` | [`backend/app/api/trojan_victim.py`](backend/app/api/trojan_victim.py) | Generate honeypot victim profile for active engagement |
| | `POST` | `/api/v1/trojan-victim/stress-test` | [`backend/app/api/trojan_victim.py`](backend/app/api/trojan_victim.py) | Run adversarial dialogue turn against scammer |

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python**: `3.11+`
- **Node.js**: `v20.x+` (`npm` `v10+`)
- **Docker** *(Optional)*: Docker Desktop `v24+` / Docker Compose `v2+`

### Local Development Setup

#### 1. Start Backend Service
```bash
# Clone environment configuration
cp .env.example .env

# Create Python virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt

# Run FastAPI dev server
uvicorn backend.app.main:app --reload --port 8000
```

#### 2. Start Frontend Application
In a secondary terminal window:
```bash
cd frontend
npm install
npm run dev
```
Frontend interface will be accessible at `http://localhost:5173`.

---

## 🐳 Docker Deployment

Run both Backend and Frontend containerized in a single command using [`docker-compose.yml`](docker-compose.yml):

```bash
cp .env.example .env
docker-compose up --build -d
```

- 🌐 **Frontend Application**: `http://localhost:3000`
- ⚡ **Backend API**: `http://localhost:8000`
- 📖 **API Documentation**: `http://localhost:8000/docs`

---

## 🌐 Production Serverless Deployment (Vercel)

ScamTrap AI is pre-configured for serverless deployment on **Vercel**:

- **Serverless API Entrypoint**: [`api/index.py`](api/index.py)
- **Vercel Configuration**: [`vercel.json`](vercel.json)

```bash
npm install -g vercel
vercel --prod
```

> 💡 **Serverless Storage Note**: In Vercel serverless environment, `api/index.py` initializes SQLite in `/tmp/scamtrap.db` and copies the seed database on cold start. Multi-tenant production deployments require persistent PostgreSQL + `pgvector`.

---

## 🧪 Testing & Verification

```bash
# Run pytest test suite (90 passed)
.\venv\Scripts\python.exe -m pytest tests/ -v

# Run accuracy benchmark script
.\venv\Scripts\python.exe scripts/benchmark_accuracy.py
```

---

## 📁 Repository Sitemap

```
ScamTrapAI/
├── api/                      # Vercel Serverless Entrypoint (api/index.py)
├── backend/                  # FastAPI Application Core
│   ├── app/
│   │   ├── api/              # Endpoint Handlers (Incidents, Campaigns, CTI, RAG)
│   │   ├── core/             # Config, Security Guardrails, PII Redactor
│   │   ├── db/               # SQLAlchemy ORM Models & CRUD Operations
│   │   ├── models/           # Pydantic Schemas & Scam DNA Definitions
│   │   └── services/         # DNA Extractor, Louvain Engine, Audit Service
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                 # React 18 + TypeScript + Vite Dashboard
│   ├── src/
│   │   ├── components/       # UI Components & React Flow Graphs
│   │   └── pages/            # Investigator Workspace Views
│   ├── Dockerfile
│   └── package.json
├── data/                     # Synthetic Multilingual Benchmark Datasets
├── docs/                     # Architecture & ADR Documentation
├── scripts/                  # Calibration & Accuracy Benchmark Utilities
├── tests/                    # Pytest Test Suite (90 Unit & Integration Tests)
├── docker-compose.yml        # Docker Container Stack
├── vercel.json               # Vercel Deployment Specification
└── README.md
```

---

## ⚠️ Limitations

- **Demo Environment**: Demonstration data uses synthetic payloads.
- **Serverless Storage**: Serverless Vercel deployment uses ephemeral `/tmp` storage suitable for demonstration. Multi-tenant production requires PostgreSQL + `pgvector`.
- **Honeypot Boundaries**: Honeypot engagement operates strictly in simulated evaluation mode with synthetic identities.

---

## 🛡️ Responsible Use Guidelines

- ScamTrap AI is designed for cybersecurity research, SOC analysis, and threat intelligence.
- Campaign correlation provides decision support and does not constitute criminal attribution or legal proof.
- Honeypot tools must only be executed within controlled simulation boundaries.

---

## 📜 License

Distributed under the MIT License for cyber security research and threat intelligence analysis.
