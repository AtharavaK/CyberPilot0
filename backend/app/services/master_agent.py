import uuid
import asyncio
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from app.services.graph_state import CyberPilotState, Finding
from app.db import crud

# ---------------------------------------------------------
# Node Functions (Simulating Agents) — now writing to SQLite
# ---------------------------------------------------------

async def recon_node(state: CyberPilotState) -> CyberPilotState:
    print(f"[{state['scan_id']}] Running Recon Agent...")
    await asyncio.sleep(1)
    state["status"] = "RECONNAISSANCE"
    state["recon_data"] = {"endpoints_found": 3, "auth_type": "OAuth 2.0"}
    crud.update_scan_status(state["scan_id"], state["status"])
    return state

async def security_analysis_node(state: CyberPilotState) -> CyberPilotState:
    print(f"[{state['scan_id']}] Running Security Analysis Agents...")
    await asyncio.sleep(1.5)
    state["status"] = "SECURITY_ANALYSIS"

    state["ai_vulnerabilities"] = [{
        "agent_name": "AI Security Agent",
        "severity": "HIGH",
        "description": "Mild susceptibility to role-play jailbreak.",
        "remediation": None
    }]
    state["api_vulnerabilities"] = [{
        "agent_name": "API Security Agent",
        "severity": "HIGH",
        "description": f"Rate limiting missing on {state['target_url']}/api/v1/chat endpoint.",
        "remediation": None
    }]
    state["code_vulnerabilities"] = [{
        "agent_name": "Code Review Agent",
        "severity": "MEDIUM",
        "description": "Outdated dependency (requests v2.25.0) detected.",
        "remediation": None
    }]
    state["infra_vulnerabilities"] = []

    state["all_findings"] = (
        state["ai_vulnerabilities"] +
        state["api_vulnerabilities"] +
        state["code_vulnerabilities"] +
        state["infra_vulnerabilities"]
    )
    crud.update_scan_status(state["scan_id"], state["status"])
    return state

async def risk_scoring_node(state: CyberPilotState) -> CyberPilotState:
    print(f"[{state['scan_id']}] Running Risk Analysis Agent...")
    await asyncio.sleep(0.5)
    state["status"] = "RISK_SCORING"
    state["overall_score"] = 78
    crud.update_scan_status(state["scan_id"], state["status"])
    return state

async def recommendation_node(state: CyberPilotState) -> CyberPilotState:
    print(f"[{state['scan_id']}] Running Recommendation Agent...")
    await asyncio.sleep(1)
    state["status"] = "RECOMMENDATIONS"

    for finding in state["all_findings"]:
        if finding["agent_name"] == "AI Security Agent":
            finding["remediation"] = "Implement input sanitization and strict system prompts."
        elif finding["agent_name"] == "API Security Agent":
            finding["remediation"] = "Use Redis-based rate limiting (e.g., 60 req/min per IP)."
        elif finding["agent_name"] == "Code Review Agent":
            finding["remediation"] = "Update 'requests' library to the latest secure version."

    crud.update_scan_status(state["scan_id"], state["status"])
    return state

async def report_node(state: CyberPilotState) -> CyberPilotState:
    print(f"[{state['scan_id']}] Running Report Agent...")
    await asyncio.sleep(0.5)
    state["status"] = "COMPLETED"
    state["final_report"] = {"summary_generated": True, "technical_report_generated": True}

    # ✅ Persist final results to SQLite
    crud.complete_scan(state["scan_id"], state["overall_score"], state["all_findings"])
    return state

# ---------------------------------------------------------
# Graph Construction
# ---------------------------------------------------------

def build_master_agent_graph() -> StateGraph:
    workflow = StateGraph(CyberPilotState)
    workflow.add_node("recon", recon_node)
    workflow.add_node("security_analysis", security_analysis_node)
    workflow.add_node("risk_scoring", risk_scoring_node)
    workflow.add_node("recommendations", recommendation_node)
    workflow.add_node("report", report_node)

    workflow.set_entry_point("recon")
    workflow.add_edge("recon", "security_analysis")
    workflow.add_edge("security_analysis", "risk_scoring")
    workflow.add_edge("risk_scoring", "recommendations")
    workflow.add_edge("recommendations", "report")
    workflow.add_edge("report", END)

    return workflow.compile()

master_agent_app = build_master_agent_graph()

# ---------------------------------------------------------
# API Integration Functions
# ---------------------------------------------------------

def start_scan_workflow(target_url: str) -> str:
    scan_id = str(uuid.uuid4())

    # ✅ Create initial record in SQLite
    crud.create_scan(scan_id, target_url)

    initial_state: CyberPilotState = {
        "scan_id": scan_id,
        "target_url": target_url,
        "status": "INITIALIZING",
        "recon_data": {},
        "ai_vulnerabilities": [],
        "api_vulnerabilities": [],
        "code_vulnerabilities": [],
        "infra_vulnerabilities": [],
        "all_findings": [],
        "overall_score": 100,
        "compliance_status": "PENDING",
        "final_report": {}
    }

    asyncio.create_task(master_agent_app.ainvoke(initial_state))
    return scan_id

def get_scan_result(scan_id: str) -> Dict[str, Any]:
    """Read directly from SQLite."""
    result = crud.get_scan(scan_id)
    if result is None:
        return {"status": "NOT_FOUND"}
    return result
