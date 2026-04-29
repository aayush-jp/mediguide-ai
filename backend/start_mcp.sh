#!/bin/bash
# Start MediGuide AI MCP server (for Claude Code / MCP clients)
cd "$(dirname "$0")/.."
python -m backend.mcp_tools.server
