from pydantic import BaseModel, Field
from typing import List, Optional

class ScanRequest(BaseModel):
    target_url: str = Field(..., example="https://example-ai-app.com")

class Finding(BaseModel):
    agent_name: str
    severity: str
    description: str
    remediation: Optional[str] = None

class ScanResponse(BaseModel):
    scan_id: str
    status: str
    message: str

class ReportSummary(BaseModel):
    scan_id: str
    target_url: str
    overall_score: int
    findings: List[Finding]
