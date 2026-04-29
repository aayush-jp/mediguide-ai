# MediGuide AI — Project Notes

## Project
Clinical support assistant combining symptom checker, medical chatbot, and report analysis.
NOT a doctor replacement — outputs "Possible conditions + risk level + next safe step."

## Architecture

### Backend (FastAPI + Python)
- Entry: `backend/main.py` → `uvicorn backend.main:app --reload --port 8000`
- Routes: `backend/routes/` — symptom.py, chat.py, report.py
- Agent: `backend/agents/medical_agent.py` — Claude claude-sonnet-4-6 with tool_use loop
- MCP Server: `backend/mcp_tools/server.py` — run with `python -m backend.mcp_tools.server`
- Tools: `backend/mcp_tools/tools.py` — Python implementations
- Knowledge base: `backend/utils/medical_kb.py` — 22 conditions + lab ranges
- Triage: `backend/utils/triage.py` — emergency detection + risk scoring

### Frontend (Next.js 15)
- Entry: `frontend/` → `npm run dev` (port 3000)
- Pages: `src/app/` — page.tsx, chat/, symptom-checker/, report/
- Components: `src/components/` — Navbar, ChatInterface, SymptomForm, ReportUpload, RiskMeter, EmergencyBanner, ConditionCard

## Environment
Copy `.env.example` to `.env` and set:
- `ANTHROPIC_API_KEY` — required for all AI features
- `NEXT_PUBLIC_API_URL` — frontend points to backend (default: http://localhost:8000)

## Running Locally
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

## Key Safety Rules
1. Agent never prescribes medications or dosages
2. Agent never makes a final diagnosis
3. Emergency keywords trigger immediate escalation
4. Every response ends with medical disclaimer
5. Report analysis is informational only
