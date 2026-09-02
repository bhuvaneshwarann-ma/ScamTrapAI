# 🛡️ ScamTrap AI

**Behavioral Intelligence Platform for Multilingual Scam Campaign Detection & Autonomous Investigation**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18.3-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.5-blue.svg)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5.4-646CFF.svg)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-38BDF8.svg)](https://tailwindcss.com/)
[![Tests](https://img.shields.io/badge/tests-90%20passed-brightgreen.svg)]()

---

## 📌 Executive Summary

**ScamTrap AI** transforms unstructured, suspicious multilingual communications (SMS, WhatsApp messages, phishing emails, and voice call transcripts) into structured behavioral signatures called **Scam DNA**. 

By correlating tactics, psychological triggers, and technical indicators across incidents using graph community algorithms, ScamTrap AI automatically discovers emerging scam campaigns, generates evidence-bounded explanations for analysts, exports threat intelligence (STIX 2.1 / MISP), and emulates honeypot victim dialogues to trap active scammers.

> **⚠️ CONTROLLED DEMO ENVIRONMENT**  
> *This platform is built for security research and threat intelligence analysis using synthetic and sanitized incident data.*

---

## ✨ Key Features & Capabilities

- 🧬 **Scam DNA Extraction**: Parses raw multilingual text into structured behavioral signatures, extracting urgency indices, psychological manipulation tactics, financial targets, and technical IOCs (URLs, phone numbers, UPI IDs, bank details).
- 🕸️ **Graph-Based Campaign Discovery**: In-memory NetworkX & community detection engines link isolated incidents into high-confidence campaign clusters based on shared infrastructure and behavioral overlap.
- 🤖 **Analyst Copilot & RAG Investigation Engine**: Interactive AI assistant powered by vector embeddings (`sentence-transformers` / `pgvector`) for natural language querying over incident archives and campaign history.
- 🎯 **Autonomous Trojan / Victim Honeypot**: Interactive dialogue agent designed to safely engage scammers, draw out infrastructure details (payment handles, domains), and log telemetry.
- 🌐 **Cyber Threat Intelligence (CTI) Export**: One-click generation of standard STIX 2.1 JSON packages, MISP threat feeds, and MITRE ATT&CK / FiCF scam taxonomy mappings.
- 🛡️ **Privacy & Prompt Injection Defense**: Mandatory HMAC-SHA256 deterministic PII redaction and multi-stage LLM prompt injection sanitizer before any LLM processing.
- 📊 **Evaluation & Calibration Benchmarks**: Automated accuracy matrix (Precision, Recall, F1) and automated similarity threshold calibration script for tuning correlation confidence.

---

## 🏗️ System Architecture

```
                                  [ Raw Input ]
                         (SMS / WhatsApp / Email / Voice)
                                       │
                                       ▼
                       ┌───────────────────────────────┐
                       │  Security Guard & Sanitizer  │
                       │ (PII Redaction & Injection Check) │
                       └───────────────┬───────────────┘
                                       │
                                       ▼
                       ┌───────────────────────────────┐
                       │   LLM Scam DNA Extractor      │
                       │ (Tactics, Triggers, IOCs)     │
                       └───────────────┬───────────────┘
                                       │
                    ┌──────────────────┴──────────────────┐
                    ▼                                     ▼
     ┌─────────────────────────────┐       ┌─────────────────────────────┐
     │  Graph Correlation Engine   │       │   Vector Store & RAG Engine │
     │  (NetworkX / Louvain Graph) │       │ (pgvector / Embeddings)     │
     └──────────────┬──────────────┘       └──────────────┬──────────────┘
                    │                                     │
                    └──────────────────┬──────────────────┘
                                       │
                                       ▼
                       ┌───────────────────────────────┐
                       │   Investigator Control Deck   │
                       │ (Dashboard, Copilot, CTI Export) │
                       └───────────────────────────────┘
```

### Technology Stack

| Layer | Component | Description |
|-------|-----------|-------------|
| **Backend** | Python 3.11+, FastAPI | High-performance async REST API gateway |
| **Frontend** | React 18, TypeScript, Vite | Modern responsive UI with Tailwind CSS & Lucide icons |
| **Graph Visualization** | React Flow, NetworkX | Interactive campaign graph rendering & community clustering |
| **Storage & Vectors** | PostgreSQL + pgvector (SQLite fallback) | Relational incident storage & vector similarity search |
| **Security** | HMAC-SHA256, Regex Guardrails | Zero-PII leak guarantees & prompt injection defense |

---

## 🚀 Quick Start Guide

### Prerequisites

- **Python**: 3.11 or higher
- **Node.js**: v20.x or higher (`npm` v10+)
- **Docker** *(Optional)*: Docker Desktop / Docker Compose

---

### Option 1: Standard Local Setup

#### 1. Clone & Configure Environment

```bash
cp .env.example .env
```

> 🔑 **Important Security Note**: Open `.env` and set `PII_HMAC_KEY` to a secure random string (at least 32 characters).

#### 2. Start Backend Service

```bash
# Create and activate virtual environment
cd backend
python -m venv venv

# Windows (PowerShell / CMD)
venv\Scripts\activate

# macOS / Linux
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI dev server (from project root)
cd ..
uvicorn backend.app.main:app --reload --port 8000
```
Backend API interactive documentation will be live at `http://localhost:8000/docs`.

#### 3. Start Frontend Service

Open a new terminal window:

```bash
cd frontend
npm install
npm run dev
```
Frontend application will be accessible at `http://localhost:5173`.

---

### Option 2: Docker Setup

Run both Backend and Frontend containerized in a single command:

```bash
cp .env.example .env
docker-compose up --build
```

- **Frontend App**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`

---

## 🧪 Testing & Verification

### Run Backend Test Suite

The backend features full test coverage across API routes, DNA extraction, graph correlation, security sanitization, and RAG pipelines:

```bash
# Run pytest with verbose output
pytest tests/ -v

# Run with coverage report
pytest --cov=backend tests/
```

### Run Frontend Build & Linting

```bash
cd frontend
npm run build
```

---

## 🔌 API Reference Summary

Below is an overview of key endpoint categories exposed by the FastAPI backend:

| Group | Method | Path | Description |
|-------|--------|------|-------------|
| **Health** | `GET` | `/api/v1/health` | System health check and status |
| **Auth** | `POST` | `/api/v1/auth/login` | Investigator authentication & session token |
| **Incidents** | `GET` | `/api/v1/incidents` | List all ingested scam incidents |
| | `POST` | `/api/v1/incidents/analyze` | Ingest raw conversation & extract Scam DNA |
| **Campaigns** | `GET` | `/api/v1/campaigns` | Retrieve auto-detected scam campaigns |
| | `GET` | `/api/v1/campaigns/graph` | Fetch graph nodes & edges for React Flow |
| **Investigations**| `POST` | `/api/v1/investigations/copilot` | Natural language investigator copilot query |
| **RAG** | `POST` | `/api/v1/rag/query` | Vector search over indexed incident knowledge base |
| **CTI** | `GET` | `/api/v1/cti/stix` | Export campaign intelligence as STIX 2.1 bundle |
| | `GET` | `/api/v1/cti/misp` | Export threat indicators in MISP JSON format |
| **Honeypot** | `POST` | `/api/v1/trojan-victim/chat` | Send dialogue turn to autonomous victim emulator |

---

## ⚙️ Environment Configuration (`.env`)

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `APP_NAME` | `ScamTrap AI` | Platform application title |
| `DEBUG` | `true` | Enables FastAPI interactive `/docs` and debug logs |
| `LOG_LEVEL` | `INFO` | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `PII_HMAC_KEY` | *(Required)* | Secret key for deterministic PII hashing (min 32 chars) |
| `DATABASE_URL` | `sqlite:///./scamtrap.db` | Database connection URI (SQLite or PostgreSQL) |
| `LLM_PROVIDER` | `mock` | LLM engine (`mock` for offline dev, `gemini` for live API) |
| `GEMINI_API_KEY` | `""` | Google Gemini API Key (if `LLM_PROVIDER=gemini`) |
| `EMBEDDING_PROVIDER`| `mock` | Vector provider (`mock` or `sentence-transformers`) |

---

## 📁 Project Structure

```
ScamTrapAI/
├── backend/                  # FastAPI Application Core
│   ├── app/
│   │   ├── api/              # API Route Handlers (Incidents, Campaigns, CTI, RAG)
│   │   ├── core/             # Config, Security, PII Redactor, Input Sanitizer
│   │   ├── db/               # Database Models & SQLAlchemy Sessions
│   │   ├── models/           # Pydantic Schemas & Scam DNA Definitions
│   │   ├── services/         # DNA Extractor, Graph Engine, Copilot, Honeypot
│   │   └── main.py           # FastAPI Application Entry Point
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                 # React 18 + TypeScript + Vite Dashboard
│   ├── src/
│   │   ├── components/       # UI Components (Navigation, Graphs, Cards, Tables)
│   │   ├── pages/            # 15 Interactive Investigator Workspace Views
│   │   ├── App.tsx           # App Router & Layout Wrapper
│   │   └── index.css         # Tailwind & Custom Styling
│   ├── Dockerfile
│   └── package.json
├── data/                     # Synthetic incident datasets & test payloads
├── docs/                     # Architectural decisions & design documentation
│   ├── architecture.md       # Full Technical Architecture & Pipeline Specification
│   └── decisions.md          # Key Engineering & Design Trade-off Decisions
├── scripts/                  # Utility & Threshold Calibration Scripts
│   └── calibrate_thresholds.py # Graph similarity threshold calibration
├── tests/                    # Pytest Test Suite (90 unit & integration tests)
├── docker-compose.yml        # Docker Multi-Container Configuration
├── .env.example              # Environment Configuration Template
└── spec.md                   # Full Specification Directive
```

---

## 🔒 Security & Data Privacy Safeguards

- **Strict PII Redaction**: Before raw payload persistence or LLM invocation, sensitive personal data (phone numbers, email addresses, payment handles, URLs) are deterministically hashed via HMAC-SHA256.
- **Prompt Injection Defense**: Multi-layered regex and structural input sanitization filters prevent malicious prompt overrides or extraction attempts.
- **Zero Raw PII Storage**: Database tables store only hashed pseudonyms and anonymized tokens to remain compliant with privacy standards.

---

## 📜 License

Internal / Hackathon Demonstration Project. All rights reserved.

