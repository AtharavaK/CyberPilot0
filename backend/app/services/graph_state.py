from typing import TypedDict, List, Dict, Any, Optional

class Finding(TypedDict):
    agent_name: str
    severity: str
    description: str
    remediation: Optional[str]

class CyberPilotState(TypedDict):
    scan_id: str
    target_url: str
    status: str
    
    # Internal agent states
    recon_data: Dict[str, Any]
    ai_vulnerabilities: List[Finding]
    api_vulnerabilities: List[Finding]
    code_vulnerabilities: List[Finding]
    infra_vulnerabilities: List[Finding]
    
    # Aggregated results
    all_findings: List[Finding]
    overall_score: int
    compliance_status: str
    
    # Final output
    final_report: Dict[str, Any]
