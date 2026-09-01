# 🛡️ ScamTrap AI

**Behavioral Intelligence Platform for Scam Campaign Detection & Investigation**

ScamTrap AI converts suspicious multilingual conversations (SMS, WhatsApp, Email, Voice Transcripts) into structured behavioral intelligence (**Scam DNA**), correlates incidents across shared infrastructure and tactics, discovers emerging scam campaigns, and provides evidence-bounded explanations to investigators.

> **⚠️ DEMO / CONTROLLED ENVIRONMENT — SYNTHETIC DATA ONLY**

---

## 🏗️ Architecture

```
Conversation → AI Analysis → Scam DNA → Correlation → Campaign Alert
```

- **Backend:** Python 3.11+, FastAPI, Pydantic v2
- **Frontend:** React 18 + TypeScript, Tailwind CSS, React Flow
- **Storage:** PostgreSQL + pgvector (SQLite fallback for dev)
- **AI/NLP:** Configurable LLM provider with deterministic mock fallback
- **Graph:** NetworkX (in-memory campaign graph)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- (Optional) Docker & Docker Compose

### Backend Setup

```bash
# Create and activate virtual environment
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Copy environment config
cp ../.env.example ../.env
# Edit .env with your settings (at minimum, change PII_HMAC_KEY)

# Run the backend
cd ..
uvicorn backend.app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Docker (both services)

```bash
cp .env.example .env
docker-compose up --build
```

### Run Tests

```bash
# From project root
pytest tests/ -v
```

## 🧪 API Endpoints (Phase 1)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/api/v1/health` | Health check (versioned) |

## 📁 Project Structure

```
ScamTrapAI/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Config, security, logging, sanitizer
│   │   └── main.py       # FastAPI application factory
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/             # React + TypeScript + Vite
├── tests/                # pytest test suite
├── data/                 # Synthetic datasets (Phase 3+)
├── docs/                 # Architecture & decision docs
├── scripts/              # Utility scripts
├── docker-compose.yml
├── .env.example
└── spec.md               # Build directive
```

## 🔒 Security

- **PII Protection:** All identifiers (phone, email, UPI, URL) are HMAC-SHA256 hashed before logging
- **Prompt Injection Defense:** Input sanitizer detects and neutralizes LLM injection patterns
- **Structured Logging:** JSON logs with automatic PII redaction

## 📄 License

Hackathon project — internal use only.
