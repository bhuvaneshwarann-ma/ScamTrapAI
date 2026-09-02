# 🛡️ ScamTrap AI

**Behavioral Intelligence Platform for Multilingual Scam Campaign Detection & Autonomous Investigation**

ScamTrap AI transforms suspicious multilingual communications into behavioral Scam DNA, correlates incidents using graph and semantic intelligence, and helps investigators uncover coordinated scam campaigns.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18.3-61DAFB.svg?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript 5.5](https://img.shields.io/badge/TypeScript-5.5-3178C6.svg?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vite 5.4](https://img.shields.io/badge/Vite-5.4-646CFF.svg?style=flat-square&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Tailwind CSS 3.4](https://img.shields.io/badge/Tailwind_CSS-3.4-06B6D4.svg?style=flat-square&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Tests](https://img.shields.io/badge/tests-90%20passed%20%7C%20100%25-brightgreen.svg?style=flat-square&logo=pytest&logoColor=white)]()
[![Vercel Deployment](https://img.shields.io/badge/Vercel-Serverless_Ready-000000.svg?style=flat-square&logo=vercel&logoColor=white)](https://vercel.com/)

[📖 Interactive OpenAPI Docs](http://localhost:8000/docs) • [💻 GitHub Repository](https://github.com/bhuvaneshwarann-ma/ScamTrapAI) • [📊 Architecture Specification](docs/architecture.md) • [🤝 ADR Decisions](docs/decisions.md)



## ⚡ Why ScamTrap AI?

Traditional Cyber Threat Intelligence (CTI) detects known indicators. **ScamTrap AI detects the recurring behavioral patterns behind scam campaigns.**

Modern cybercriminals rapidly rotate infrastructure across disposable payment handles (UPI IDs, temporary wallets), short-lived domains, and burner phone numbers while preserving underlying **psychological manipulation tactics, urgency pressure, script patterns, and social-engineering playbooks** across multilingual communication channels (SMS, WhatsApp, Email, Voice).

| Feature / Capability | Traditional CTI | ScamTrap AI |
|----------------------|-----------------|-------------|
| **Primary Vector** | Static IOCs (IPs, domains, single hashes) | Behavioral Scam DNA (`ScamDNA` v1.0) |
| **Correlation Scope** | Individual isolated incidents | Campaign-level graph & cluster correlation |
| **Matching Engine** | Exact string / IP matching | Semantic embedding + entity overlap similarity |
| **Threat Output** | Flat IOC lists & blacklists | Heterogeneous relationship graphs & attack timelines |
| **Investigation** | Manual query & investigation | Evidence-Grounded AI Investigator Copilot |

---

## 👥 Intended Users

- **SOC Analysts**: Triage incoming user-reported scam messages and identify emerging campaign threats in real time.
- **Cyber Threat Intelligence (CTI) Analysts**: Map campaign infrastructure, trace actor relationships, and export standardized STIX 2.1 bundles & MISP threat feeds.
- **Fraud Investigation Teams**: Perform deep-dive correlation across payment handles, domain clusters, and psychological tactics.
- **Security Researchers**: Analyze multilingual social-engineering playbooks and evaluate automated Honeypot dialogue engagement strategies.
- **Academic Cybersecurity Researchers**: Benchmark graph community detection and semantic vector retrieval over multilingual fraud datasets.

---

## 🛠️ Technology Stack

- **Frontend**: React 18 • TypeScript 5.5 • Vite 5.4 • Tailwind CSS 3.4 • React Flow
- **Backend**: Python 3.11+ • FastAPI 0.115.0 • Pydantic v2 • SQLAlchemy 2.0
- **AI & Retrieval**: LLM Provider Abstraction • Dense Vector Embeddings • RAG Engine • Cosine Vector Search
- **Graph Intelligence**: NetworkX 3.0 • Louvain Modularity Community Detection
- **Database Storage**: SQLite (Local Dev / Vercel Serverless `/tmp`) • PostgreSQL + `pgvector` (Production Enterprise)
- **Threat Intelligence**: STIX 2.1 • MISP JSON • MITRE ATT&CK / FiCF Taxonomy

---

## 🚦 Project Status Summary

| Component Module | Status | Source Code File | Description |
|------------------|--------|------------------|-------------|
| **Scam DNA Extractor** | ✅ Implemented | [`backend/app/models/scam_dna.py`](backend/app/models/scam_dna.py) | Pydantic v2 schema with `schema_version`, field confidence map, & language metadata |
| **Campaign Detection** | ✅ Implemented | [`backend/app/services/campaign_detector.py`](backend/app/services/campaign_detector.py) | Threshold detection (`min_incidents=3`), alerts, and temporal timeline sorting |
| **Graph Intelligence** | ✅ Implemented | [`backend/app/services/graph_engine.py`](backend/app/services/graph_engine.py) | NetworkX Louvain graph clustering & React Flow graph export |
| **Vector RAG Store** | ✅ Implemented | [`backend/app/services/rag_engine.py`](backend/app/services/rag_engine.py) | Incident embedding indexing & cosine vector search Q&A |
| **Multilingual Normalization** | ✅ Implemented | [`backend/app/services/llm_provider.py`](backend/app/services/llm_provider.py) | Tested on English, Tamil (`ta`), Hindi (`hi`) & Code-Switching (`ta-en`, `hi-en`) |
| **Investigator Copilot** | ✅ Implemented | [`backend/app/services/copilot_service.py`](backend/app/services/copilot_service.py) | Evidence-grounded Q&A with strict confidence threshold fallback |
| **STIX 2.1 / MISP Export** | ✅ Implemented | [`backend/app/api/cti.py`](backend/app/api/cti.py) | Validated STIX 2.1 JSON bundle & MISP feed exporter |
| **Audit & Evidence Integrity**| ✅ Implemented | [`backend/app/services/audit_service.py`](backend/app/services/audit_service.py) | Audit logging tracking actor, role, action, target_id, and operation details |
| **Accuracy Benchmarking** | ✅ Implemented | [`scripts/benchmark_accuracy.py`](scripts/benchmark_accuracy.py) | Reproducible evaluation script computing Precision, Recall, and F1 |
| **Trojan Victim Honeypot** | 🧪 Experimental | [`backend/app/services/trojan_victim_service.py`](backend/app/services/trojan_victim_service.py) | Controlled simulation mode with synthetic personas & stress tests |
| **Production DB (pgvector)** | 🚧 Production Ready | [`backend/app/db/engine.py`](backend/app/db/engine.py) | Dual-driver SQLAlchemy 2.0 supporting SQLite (local/Vercel) & PostgreSQL + `pgvector` |

---

## ✨ Key Features

- 🧬 **Scam DNA Extraction (v1.0)**: Decomposes raw multilingual text into structured behavioral fingerprints, tracking urgency indices, psychological tactics (`SocialEngineeringTactic`), impersonation targets (`ImpersonationTarget`), payment methods (`PaymentMethod`), and extracted IOCs with field-level namespaced confidence scores (`confidence_scores`).
- 🕸️ **Louvain Graph Campaign Clustering**: Graph community engine built on NetworkX (`GraphEngine.get_clusters()`) optimizing modularity to discover emerging scam campaigns.
- 🌐 **Multilingual Intelligence & Normalization**: Normalizes and correlates scam messages across English, Tamil (`ta`), Hindi (`hi`), and code-switching dialects (`ta-en`, `hi-en`) in `MockLLMProvider` ([`backend/app/services/llm_provider.py`](backend/app/services/llm_provider.py)).
- ⏱️ **Temporal Campaign Evolution**: Chronological attack timelines (`Campaign.timeline`) tracking incident progression over time.
- 🤖 **Evidence-Grounded Investigator Copilot**: Evidence-backed Q&A (`CopilotService.answer_query()`) returning cited evidence IDs with an explicit insufficient-evidence fallback (`"Insufficient evidence to determine this."`).
- 🎯 **Autonomous Trojan Victim Honeypot**: Dialogue agent (`TrojanVictimService`) engaging scammers in controlled simulation mode with synthetic personas, stress testing, and kill-switch safety boundaries.
- 🛡️ **Offline-First Execution & PII Protection**: Mandatory `HMAC-SHA256` deterministic PII redaction (`hash_pii()` in [`backend/app/core/security.py`](backend/app/core/security.py)) and multi-pass prompt injection defense (`sanitize_input()` in [`backend/app/core/sanitizer.py`](backend/app/core/sanitizer.py)).
- 🔐 **Investigator Audit Logging & Evidence Integrity**: Complete audit trail (`AuditService` in [`backend/app/services/audit_service.py`](backend/app/services/audit_service.py)) and canonical SHA-256 evidence hashing (`Evidence.compute_integrity_hash()` in [`backend/app/models/evidence.py`](backend/app/models/evidence.py)).

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python**: `3.11+`
- **Node.js**: `v20.x+` (`npm` `v10+`)
- **Docker** *(Optional)*: Docker Desktop `v24+` / Docker Compose `v2+`

### 1. Local Setup Commands

```bash
# Clone environment configuration template
cp .env.example .env

# Create Python 3.11 virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\activate

# Activate virtual environment (macOS / Linux)
# source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# Start FastAPI backend service (Terminal 1)
uvicorn backend.app.main:app --reload --port 8000
```

In a secondary terminal window:

```bash
# Start React + TypeScript + Vite frontend service (Terminal 2)
cd frontend
npm install
npm run dev
```

- 🌐 **Frontend App Deck**: `http://localhost:5173`
- ⚡ **Backend API**: `http://localhost:8000`
- 📖 **Interactive OpenAPI Docs**: `http://localhost:8000/docs`

---

## 🔄 End-to-End Investigation Pipeline Workflow

```
       Suspicious Multilingual Communication (SMS / WhatsApp / Email / Voice)
                                         │
                                         ▼
                   ┌───────────────────────────────────────────┐
                   │  Sanitization & PII Protection            │
                   │  - HMAC-SHA256 Deterministic PII Redaction│
                   │  - Multi-pass Prompt Injection Guardrail  │
                   └─────────────────────┬─────────────────────┘
                                         │
                                         ▼
                   ┌───────────────────────────────────────────┐
                   │  Scam DNA Extraction (v1.0)               │
                   │  - Urgency, Tactics, Impersonation Target │
                   │  - Namespaced Field Confidence Scores     │
                   └─────────────────────┬─────────────────────┘
                                         │
                                         ▼
                   ┌───────────────────────────────────────────┐
                   │  Entity Resolution & Disambiguation       │
                   │  - UPI, Domain, URL, Phone Canonicalization│
                   └─────────────────────┬─────────────────────┘
                                         │
                                         ▼
                   ┌───────────────────────────────────────────┐
                   │  Pairwise Similarity Analysis             │
                   │  - Composite Vector + Jaccard Scoring     │
                   │  - Sub-score Breakdown & Evidence Reasons │
                   └─────────────────────┬─────────────────────┘
                                         │
                                         ▼
                   ┌───────────────────────────────────────────┐
                   │  Graph Community Correlation (Louvain)    │
                   │  - NetworkX Graph Edge Weighting          │
                   │  - Cluster Discovery & Modularity Optimization
                   └─────────────────────┬─────────────────────┘
                                         │
                                         ▼
                   ┌───────────────────────────────────────────┐
                   │  Campaign Detection & Timeline Assembly   │
                   │  - Emerging Campaign Alerts               │
                   │  - Chronological Attack Progression Timeline│
                   └─────────────────────┬─────────────────────┘
                                         │
                  ┌──────────────────────┴──────────────────────┐
                  ▼                                             ▼
┌───────────────────────────────────┐         ┌───────────────────────────────────┐
│  Investigator Copilot Query       │         │  Cyber Threat Intelligence Export │
│  - Evidence-Grounded Q&A          │         │  - STIX 2.1 JSON Bundles          │
│  - Citation & Threshold Fallback  │         │  - MISP JSON Threat Feeds         │
└───────────────────────────────────┘         └───────────────────────────────────┘
```

---

## 🧬 Scam DNA Engine & Technical Specifications

A scammer can change their phone number, URL, or payment handle while keeping the same psychological script. **ScamTrap AI captures this recurring behavioral pattern as Scam DNA.**

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

Where $J(X, Y) = \frac{|X \cap Y|}{|X \cup Y|}$ represents Jaccard Similarity over entities ($E$) and tactics ($T$). Output `SimilarityResult` exposes `entity_overlap_score`, `tactic_similarity_score`, `semantic_similarity_score`, `urgency_similarity_score`, and `primary_evidence_reasons`.

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
| **Offline-First Execution** | [`backend/app/services/llm_provider.py`](backend/app/services/llm_provider.py) | Offline-first `MockLLMProvider` fallback for air-gapped execution |

---

## 💻 API Example & Gateway Reference

### Incident Analysis API Example

```bash
curl -X POST http://localhost:8000/api/v1/incidents/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "sms",
    "raw_text": "URGENT: SBI YONO account will be blocked today. Update your KYC immediately at http://sbi-kyc-update.com or pay Rs 1 to sbi.kyc@ybl"
  }'
```

#### Scam DNA Extracted Response

```json
{
  "incident_id": "inc-101",
  "status": "analyzed",
  "scam_dna": {
    "schema_version": "1.0",
    "language": "ta-en",
    "language_confidence": 0.96,
    "channel": "sms",
    "impersonation_target": "bank",
    "urgency": 0.9,
    "fear": 0.85,
    "authority_pressure": 0.8,
    "credential_request": true,
    "payment_request": true,
    "payment_method": "upi",
    "requested_action": "Update KYC / Pay pending bill or fee",
    "social_engineering_tactics": [
      "urgency_pressure",
      "authority_impersonation"
    ],
    "phone_numbers": [],
    "upi_ids": ["sbi.kyc@ybl"],
    "urls": ["http://sbi-kyc-update.com"],
    "domains": ["sbi-kyc-update.com"],
    "extraction_confidence": 0.92,
    "confidence_scores": {
      "impersonation_target": 0.94,
      "social_engineering_tactics": 0.92,
      "payment_method": 0.90,
      "urgency": 0.95
    }
  }
}
```

### API Endpoint Reference Summary

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

## 📊 Benchmark Results

| Benchmark Metric | Result Value |
|------------------|--------------|
| **Evaluation Dataset** | 3 Synthetic Incidents |
| **Pairwise Evaluations** | 3 Incident Pairs |
| **Execution Latency** | 0.00 ms |
| **Precision** | 33.3% |
| **Recall** | 100.0% |
| **F1-Score** | 50.0% |

Reproducible evaluation output from [`scripts/benchmark_accuracy.py`](scripts/benchmark_accuracy.py):

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

> *Note: This is an initial reproducible benchmark executed on a 3-incident synthetic evaluation dataset to verify mathematical pipeline stability. It should not be interpreted as real-world production accuracy.*

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
│   └── images/
│       └── dashboard.png     # Application Dashboard Screenshot Preview
├── scripts/                  # Calibration & Accuracy Benchmark Utilities
├── tests/                    # Pytest Test Suite (90 Unit & Integration Tests)
├── docker-compose.yml        # Docker Container Stack
├── vercel.json               # Vercel Deployment Specification
└── README.md
```

---

## 🤝 Architectural Decision Records (ADRs)

Key engineering design decisions documented in [`docs/decisions.md`](docs/decisions.md):

1. **ADR-001: Hybrid Graph & Vector Search**: Selected Louvain graph clustering for deterministic infrastructure links combined with dense cosine embeddings for semantic tactic matching.
2. **ADR-002: Deterministic HMAC PII Redaction**: Implemented HMAC-SHA256 with salt to prevent raw PII persistence while preserving exact match capability across incidents.
3. **ADR-003: SQLite / PostgreSQL Dual Driver**: Designed an abstraction layer in `backend/app/db/engine.py` allowing zero-config local SQLite development alongside production PostgreSQL + `pgvector` scaling.

---

## 🗺️ Roadmap

- [x] **Scam DNA Schema v1.0** with field-level namespaced confidence scores
- [x] **Graph Community Campaign Detection** using Louvain modularity optimization
- [x] **Multilingual Normalization** across English, Tamil (`ta`), Hindi (`hi`), and dialect code-switching
- [x] **Evidence-Grounded Copilot** with strict citation fallback (`"Insufficient evidence to determine this."`)
- [x] **Standardized CTI Exports** (STIX 2.1 JSON bundles, MISP feeds, & MITRE ATT&CK / FiCF taxonomy)
- [x] **Investigator Audit Logging** (`AuditService`) & canonical SHA-256 evidence checksums
- [x] **Reproducible Accuracy Benchmark Script** (`scripts/benchmark_accuracy.py`)
- [ ] **Expanded Multilingual Benchmark** over 10,000+ real-world multilingual incident samples
- [ ] **Real-World CTI Feed Ingestion** (Automated sync with CERT-In and MISP threat feeds)
- [ ] **Advanced Temporal Graph Analytics** with continuous sliding-window campaign clustering
- [ ] **Native PostgreSQL + pgvector Infrastructure** with automated Alembic migrations
- [ ] **Multi-Tenant Investigator Workspace** with Role-Based Access Control (RBAC)

---

## 🤝 Contributing

Contributions, bug reports, feature requests, and security improvements are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Make your changes and add tests
4. Run the automated test suite (`python -m pytest tests/ -v`)
5. Submit a Pull Request for review

---

## ⚠️ Limitations & Failure Modes

- **Demo Environment**: Demonstration data uses synthetic payloads for threat research safety.
- **Serverless Storage**: Serverless Vercel deployment uses ephemeral `/tmp` storage suitable for demonstration. Multi-tenant enterprise production requires PostgreSQL + `pgvector`.
- **Honeypot Boundaries**: Honeypot engagement operates strictly in simulated evaluation mode with synthetic identities and safety kill-switches.

---

## 🛡️ Responsible Use & Safety Guidelines

- ScamTrap AI is designed for cybersecurity research, SOC analysis, and threat intelligence.
- Campaign correlation provides decision support and does not constitute criminal attribution or legal proof.
- Honeypot tools must only be executed within controlled simulation boundaries.

---

## 📜 License

Distributed under the MIT License for cyber security research and threat intelligence analysis.
