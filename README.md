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

## 📌 Executive Summary

**ScamTrap AI** is an enterprise-grade behavioral intelligence and threat correlation platform engineered to solve the multi-billion dollar challenge of fragmented scam detection. Traditional threat intelligence platforms focus primarily on technical Indicators of Compromise (IOCs) such as static IPs or single domain names. Modern cybercriminals, however, rapidly rotate infrastructure across disposable payment handles, temporary domains, and burner phone numbers while preserving underlying **psychological manipulation tactics, urgency indices, and communication signatures**.

ScamTrap AI ingests raw, unstructured, multilingual communications—including SMS, WhatsApp conversations, phishing emails, and transcribed voice calls—and converts them into normalized behavioral vectors termed **Scam DNA**. By running graph community algorithms (NetworkX & Louvain clustering) and high-dimensional vector similarity matching over structured Scam DNA, ScamTrap AI automatically clusters isolated incidents into high-confidence scam campaigns, generates evidence-bounded natural language explanations for intelligence analysts, exports standardized CTI (STIX 2.1 / MISP), and deploys an autonomous Trojan Victim Honeypot to engage threat actors in real time.

> **⚠️ CONTROLLED DEMO & SECURITY RESEARCH ENVIRONMENT**  
> *This platform is built for cyber threat intelligence (CTI) analysts, SOC teams, and law enforcement agencies. All demonstration payloads use synthetic, anonymized, and sanitized data.*

---

## 🏗️ System Architecture & Data Pipeline

The system enforces a **Zero-Trust Input Pipeline** where no raw user communication reaches storage or third-party Large Language Models without first undergoing deterministic security sanitization and PII hashing.

```
                           [ Raw Input Stream ]
                  (SMS / WhatsApp / Email / Voice Audio)
                                     │
                                     ▼
                     ┌──────────────────────────────┐
                     │ 🛡️ Security Guard & Sanitizer│
                     │  - Regex Injection Guard    │
                     │  - HMAC-SHA256 PII Hashing   │
                     └───────────────┬──────────────┘
                                     │
                                     ▼
                     ┌──────────────────────────────┐
                     │ 🧬 LLM Scam DNA Extractor    │
                     │  - Behavioral Parsing        │
                     │  - Tactics, Triggers, IOCs   │
                     └───────────────┬──────────────┘
                                     │
                  ┌──────────────────┴──────────────────┐
                  ▼                                     ▼
   ┌─────────────────────────────┐       ┌─────────────────────────────┐
   │ 🕸️ Graph Correlation Engine │       │ 🧠 Vector Store & RAG Engine│
   │  - Entity Disambiguation    │       │  - Incident Embeddings      │
   │  - NetworkX Louvain Clusters│       │  - pgvector / Cosine Search │
   └──────────────┬──────────────┘       └──────────────┬──────────────┘
                  │                                     │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
                     ┌──────────────────────────────┐
                     │ 🎯 Investigator Control Deck │
                     │  - Graph & Campaign Deck     │
                     │  - Copilot / CTI Export     │
                     │  - Trojan Victim Honeypot    │
                     └──────────────────────────────┘
```

---

## 🔬 Core Algorithmic & Technical Specifications

### 1. Scam DNA Vector Formulation
Each ingested incident $I_k$ is decomposed into a structured behavioral vector:

$$\text{ScamDNA}(I_k) = \langle T_k, U_k, E_k, C_k, \vec{v}_k \rangle$$

- $T_k \subseteq \text{Tactics}$: Set of identified psychological tactics (e.g., `AUTHORITY_IMPERSONATION`, `FEAR_LEGAL_ACTION`, `KYC_EXPIRATION`).
- $U_k \in [0.0, 1.0]$: Quantitative Urgency Index derived from linguistic indicators.
- $E_k \subseteq \text{Entities}$: Extracted technical indicators (hashed UPI IDs, domain hashes, phone pseudonyms).
- $C_k \in \text{Channels}$: Communication vector (`SMS`, `WHATSAPP`, `EMAIL`, `VOICE`).
- $\vec{v}_k \in \mathbb{R}^d$: Dense semantic embedding representation of the incident text payload.

### 2. Multi-Metric Incident Similarity Calculation
Incident pair correlation confidence $S(I_a, I_b) \in [0.0, 1.0]$ is calculated via a composite weighted score combining deterministic entity overlaps, tactic Jaccard similarity, and semantic vector similarity:

$$S(I_a, I_b) = w_1 \cdot J(E_a, E_b) + w_2 \cdot J(T_a, T_b) + w_3 \cdot \cos(\vec{v}_a, \vec{v}_b) - w_4 \cdot |U_a - U_b|$$

Where:
- $J(X, Y) = \frac{|X \cap Y|}{|X \cup Y|}$ represents Jaccard Similarity.
- $\cos(\vec{v}_a, \vec{v}_b)$ represents Cosine Vector Similarity.
- If $E_a \cap E_b \neq \emptyset$ (shared payment handle, domain, or phone number), deterministic edge weight amplification is triggered automatically.

### 3. Louvain Graph Community Detection
Incidents and extracted entities form a heterogeneous undirected graph $G = (V, E)$. The campaign detection engine optimizes modularity $Q$ over community partition $C$:

$$Q = \frac{1}{2m} \sum_{i,j} \left[ A_{ij} - \frac{k_i k_j}{2m} \right] \delta(c_i, c_j)$$

Discovered communities with modularity thresholds meeting calibrated baseline confidence scores are elevated into actionable **Scam Campaigns** with automated evidence linking.

---

## 🔒 Security Architecture & Threat Model

ScamTrap AI is designed with strict adherence to privacy compliance and LLM security standards:

| Security Domain | Strategy / Implementation | Verification Standard |
|-----------------|---------------------------|-----------------------|
| **PII Protection** | Deterministic `HMAC-SHA256` hashing with secret salt prior to persistence | Zero raw phone numbers, emails, or payment IDs stored in DB |
| **Prompt Injection Defense** | Multi-stage regex guardrails filtering `<sys_override>`, `system:`, and DAN jailbreaks | Tested against 15+ adversarial injection payloads |
| **Data Integrity** | Cryptographic evidence hashes (`SHA-256`) per incident payload | Tamper-evident evidence chain for law enforcement export |
| **Zero External Leaks** | Offline-first mock fallback for LLM and Vector Embeddings | Fully functional in air-gapped environments |

---

## 🚀 Deployment Options

### Prerequisites
- **Python**: `3.11+`
- **Node.js**: `v20.x+` (`npm` `v10+`)
- **Docker** *(Optional)*: Docker Desktop `v24+` / Docker Compose `v2+`

---

### Option 1: Vercel Production Serverless Deployment

ScamTrap AI is pre-configured for seamless serverless deployment on **Vercel** with zero backend infrastructure overhead:

- **Serverless API Entrypoint**: [`api/index.py`](file:///c:/Users/GUNALAN/Downloads/ScamTrapAI/api/index.py)
- **Vercel Configuration**: [`vercel.json`](file:///c:/Users/GUNALAN/Downloads/ScamTrapAI/vercel.json)

```bash
# Install Vercel CLI (if not already installed)
npm install -g vercel

# Deploy directly from workspace root
vercel --prod
```

> 💡 **Serverless DB Storage**: In Vercel environments, `api/index.py` automatically initializes SQLite in `/tmp/scamtrap.db` and copies the pre-populated seed dataset on cold start.

---

### Option 2: Docker Multi-Container Stack

To run the complete isolated microservices stack locally:

```bash
# 1. Clone environment configuration
cp .env.example .env

# 2. Build and launch container stack
docker-compose up --build -d

# 3. Verify running services
docker-compose ps
```

- 🌐 **Frontend Application Deck**: `http://localhost:3000`
- ⚡ **Backend FastAPI Gateway**: `http://localhost:8000`
- 📖 **Interactive OpenAPI Docs**: `http://localhost:8000/docs`

---

### Option 3: Local Developer Setup

#### 1. Backend Service Setup
```bash
# Navigate to project root and set up environment
cp .env.example .env

# Create Python 3.11 virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\activate

# Activate virtual environment (macOS / Linux)
# source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# Launch FastAPI development server with hot reload
uvicorn backend.app.main:app --reload --port 8000
```

#### 2. Frontend Application Setup
In a secondary terminal window:
```bash
cd frontend

# Install Node modules
npm install

# Start Vite dev server
npm run dev
```
Frontend interface will be live at `http://localhost:5173`.

---

## 🧪 Comprehensive Verification & Benchmarks

The platform includes a 100% passing automated test suite covering security sanitization, ORM operations, graph clustering, RAG retrieval, and API gateway routing.

```bash
# Run complete unit and integration test suite
.\venv\Scripts\python.exe -m pytest tests/ -v

# Generate test coverage report
.\venv\Scripts\python.exe -m pytest --cov=backend tests/
```

### Automated Similarity Threshold Calibration
To calibrate Jaccard and vector correlation thresholds against custom incident datasets:

```bash
.\venv\Scripts\python.exe scripts/calibrate_thresholds.py
```

---

## 🔌 API Gateway Reference

Below is a summary of core REST API endpoints provided by the FastAPI backend:

| Domain | Method | Endpoint Path | Description |
|--------|--------|---------------|-------------|
| **System** | `GET` | `/api/v1/health` | System health check, version, & uptime |
| **Auth** | `POST` | `/api/v1/auth/login` | Analyst authentication & bearer token |
| **Incidents** | `GET` | `/api/v1/incidents` | List ingested incidents with filter parameters |
| | `POST` | `/api/v1/incidents/analyze` | Ingest raw payload, sanitize PII, & extract Scam DNA |
| **Campaigns** | `GET` | `/api/v1/campaigns` | List auto-clustered scam campaigns |
| | `GET` | `/api/v1/campaigns/graph` | Fetch graph nodes & edges formatted for React Flow |
| **Investigations** | `POST` | `/api/v1/investigations/copilot` | Natural language query interface for analyst copilot |
| **RAG** | `POST` | `/api/v1/rag/query` | Vector search over indexed incident knowledge base |
| **CTI Export** | `GET` | `/api/v1/cti/stix` | Export campaign threat intelligence as STIX 2.1 bundle |
| | `GET` | `/api/v1/cti/misp` | Export threat indicators in MISP JSON format |
| | `GET` | `/api/v1/cti/mitre-matrix` | Map campaign tactics to MITRE ATT&CK / FiCF taxonomy |
| **Honeypot** | `POST` | `/api/v1/trojan-victim/generate` | Generate honeypot victim profile for active engagement |
| | `POST` | `/api/v1/trojan-victim/stress-test` | Run adversarial dialogue turn against scammer |

---

## 📁 Repository Sitemap

```
ScamTrapAI/
├── api/                      # Vercel Serverless Function Entrypoint
│   └── index.py              # Serverless app factory & dynamic /tmp SQLite initializer
├── backend/                  # FastAPI Application Core
│   ├── app/
│   │   ├── api/              # Endpoint Handlers (Incidents, Campaigns, CTI, RAG, Honeypot)
│   │   ├── core/             # Config, Logging, Security Guardrails, PII Redactor
│   │   ├── db/               # SQLAlchemy 2.0 ORM Models, Engine, & CRUD Operations
│   │   ├── models/           # Pydantic Schemas, Scam DNA Vectors, & Enum Definitions
│   │   ├── services/         # DNA Extractor, Louvain Graph Engine, RAG, Copilot
│   │   └── main.py           # Application Factory & Middleware Pipeline
│   ├── Dockerfile            # Production Python Container Build File
│   └── requirements.txt      # Backend Python Dependencies
├── frontend/                 # React 18 + TypeScript + Vite Dashboard
│   ├── src/
│   │   ├── components/       # Reusable UI Cards, Navigation, & React Flow Graphs
│   │   ├── pages/            # 15 Interactive Investigator Workspace Views
│   │   ├── App.tsx           # Main App Routing & Layout Shell
│   │   └── index.css         # Tailwind CSS Tokens & Glassmorphism Styling
│   ├── Dockerfile            # Nginx Production Frontend Container
│   └── package.json          # Node.js Project Manifest
├── data/                     # Synthetic Multilingual Benchmark Datasets
├── docs/                     # Architectural Documentation
│   ├── architecture.md       # Technical Pipeline Architecture & Specifications
│   └── decisions.md          # Architectural Decision Records (ADRs)
├── scripts/                  # Machine Learning & Graph Calibration Utilities
│   └── calibrate_thresholds.py # Modularity & Jaccard Threshold Calibration Script
├── tests/                    # Pytest Suite (90 Unit & Integration Tests)
├── docker-compose.yml        # Multi-Container Deployment Orchestration
├── vercel.json               # Vercel Serverless Build & Rewrite Specification
├── .env.example              # Environment Variable Template
└── README.md                 # Project Technical Documentation
```

---

## 🤝 Architectural Decision Records (ADRs)

Key engineering design decisions documented in [`docs/decisions.md`](file:///c:/Users/GUNALAN/Downloads/ScamTrapAI/docs/decisions.md):

1. **ADR-001: Hybrid Graph & Vector Search**: Selected Louvain graph clustering for deterministic infrastructure links combined with dense cosine embeddings for semantic tactic matching.
2. **ADR-002: Deterministic HMAC PII Redaction**: Implemented HMAC-SHA256 with salt to prevent raw PII persistence while preserving exact match capability across incidents.
3. **ADR-003: SQLite / PostgreSQL Dual Driver**: Designed an abstraction layer in `backend/app/db/engine.py` allowing zero-config local SQLite development alongside production PostgreSQL + `pgvector` scaling.

---

## 📜 License

Distributed under the MIT License for cyber security research and threat intelligence analysis. See `LICENSE` for details.
