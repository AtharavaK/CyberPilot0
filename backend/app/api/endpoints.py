from fastapi import APIRouter, HTTPException
from typing import List
from app.models.schemas import ScanRequest, ScanResponse, ReportSummary
from app.services import master_agent
from app.db import crud

router = APIRouter()

@router.post("/scan/start", response_model=ScanResponse)
async def start_scan(request: ScanRequest):
    scan_id = master_agent.start_scan_workflow(request.target_url)
    return ScanResponse(
        scan_id=scan_id,
        status="ACCEPTED",
        message=f"Scan initiated for {request.target_url}"
    )

@router.get("/scan/{scan_id}/status")
async def get_scan_status(scan_id: str):
    result = master_agent.get_scan_result(scan_id)
    if result["status"] == "NOT_FOUND":
        raise HTTPException(status_code=404, detail="Scan ID not found")

    if result["status"] == "COMPLETED":
        return ReportSummary(
            scan_id=scan_id,
            target_url=result["target_url"],
            overall_score=result["overall_score"],
            findings=result.get("findings", [])
        )
    return {"scan_id": scan_id, "status": result["status"]}

@router.get("/scans")
async def list_all_scans():
    """Return all historical scans from the database."""
    return crud.get_all_scans()
