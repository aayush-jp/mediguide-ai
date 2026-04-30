# MediGuide AI

Advanced full-stack AI-powered healthcare assistant for a final-year AI/ML project.

## Stack

- Frontend: React + Vite
- Backend: FastAPI
- Auth: JWT + bcrypt
- Database: SQLAlchemy with PostgreSQL support via `DATABASE_URL`; local development falls back to SQLite
- OCR/AI: Production-ready API shape with modular AI agent, MCP server, and medical skills

## Local URLs

- Frontend: http://127.0.0.1:3000
- Backend API: http://127.0.0.1:8001
- API docs: http://127.0.0.1:8001/docs

## Environment

Copy `backend/.env.example` to `backend/.env` for production secrets.
