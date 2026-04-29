#!/bin/bash
# Start MediGuide AI backend
cd "$(dirname "$0")/.."

# Install dependencies if needed
pip install -r backend/requirements.txt

# Run FastAPI server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
