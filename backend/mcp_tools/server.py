"""
MediGuide AI — MCP Server
Exposes medical tools via the Model Context Protocol (MCP) so that
Claude Code or other MCP clients can call them directly.

Run with: python -m backend.mcp_tools.server
"""

import asyncio
import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

from backend.mcp_tools.tools import (
    tool_check_emergency_flags,
    tool_analyze_symptoms,
    tool_calculate_risk,
    tool_interpret_lab_values,
    tool_get_medical_info,
    tool_doctor_referral_rule,
)

server = Server("mediguide-mcp")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="symptom_checker_tool",
            description="Analyze patient symptoms and return possible conditions with risk levels.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symptoms": {"type": "array", "items": {"type": "string"}},
                    "age": {"type": "integer"},
                    "gender": {"type": "string"},
                    "duration_days": {"type": "integer"},
                    "severity": {"type": "integer"},
                    "temperature_f": {"type": "number"},
                    "existing_conditions": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["symptoms"],
            },
        ),
        types.Tool(
            name="emergency_check_tool",
            description="Check if symptoms contain emergency red flags requiring immediate care.",
            inputSchema={
                "type": "object",
                "properties": {
                    "symptoms": {"type": "array", "items": {"type": "string"}},
                    "symptom_text": {"type": "string"},
                },
                "required": ["symptoms"],
            },
        ),
        types.Tool(
            name="risk_triage_tool",
            description="Calculate final risk level with patient profile modifiers.",
            inputSchema={
                "type": "object",
                "properties": {
                    "base_level": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH", "EMERGENCY"]},
                    "age": {"type": "integer"},
                    "temperature_f": {"type": "number"},
                    "duration_days": {"type": "integer"},
                    "severity": {"type": "integer"},
                    "existing_conditions": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["base_level"],
            },
        ),
        types.Tool(
            name="lab_values_tool",
            description="Interpret lab test values against standard reference ranges.",
            inputSchema={
                "type": "object",
                "properties": {
                    "values": {"type": "object", "additionalProperties": {"type": "number"}},
                    "gender": {"type": "string"},
                },
                "required": ["values"],
            },
        ),
        types.Tool(
            name="medical_knowledge_tool",
            description="Retrieve condition details from the medical knowledge base.",
            inputSchema={
                "type": "object",
                "properties": {
                    "condition_key": {"type": "string"},
                },
                "required": ["condition_key"],
            },
        ),
        types.Tool(
            name="doctor_referral_tool",
            description="Determine urgency and type of medical referral needed.",
            inputSchema={
                "type": "object",
                "properties": {
                    "risk_level": {"type": "string", "enum": ["LOW", "MEDIUM", "HIGH", "EMERGENCY"]},
                    "duration_days": {"type": "integer"},
                    "age": {"type": "integer"},
                    "existing_conditions": {"type": "array", "items": {"type": "string"}},
                    "symptom_text": {"type": "string"},
                },
                "required": ["risk_level"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    try:
        if name == "symptom_checker_tool":
            result = tool_analyze_symptoms(**arguments)
        elif name == "emergency_check_tool":
            result = tool_check_emergency_flags(**arguments)
        elif name == "risk_triage_tool":
            result = tool_calculate_risk(**arguments)
        elif name == "lab_values_tool":
            result = tool_interpret_lab_values(**arguments)
        elif name == "medical_knowledge_tool":
            result = tool_get_medical_info(**arguments)
        elif name == "doctor_referral_tool":
            result = tool_doctor_referral_rule(**arguments)
        else:
            result = {"error": f"Unknown tool: {name}"}
    except Exception as e:
        result = {"error": str(e)}

    return [types.TextContent(type="text", text=json.dumps(result, indent=2))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
