import json
from typing import Any, Dict, List, Optional
from app.db.database import get_connection


def create_scan(scan_id: str, target_url: str) -> None:
    """Insert a new scan record."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO scans (scan_id, target_url, status) VALUES (?, ?, 'INITIALIZING')",
            (scan_id, target_url),
        )
        conn.commit()


def update_scan_status(scan_id: str, status: str) -> None:
    """Update the status of an in-progress scan."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE scans SET status = ?, updated_at = datetime('now') WHERE scan_id = ?",
            (status, scan_id),
        )
        conn.commit()


def complete_scan(scan_id: str, overall_score: int, findings: List[Dict[str, Any]]) -> None:
    """Persist the final score and findings when a scan completes."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE scans SET status = 'COMPLETED', overall_score = ?, updated_at = datetime('now') WHERE scan_id = ?",
            (overall_score, scan_id),
        )
        for f in findings:
            conn.execute(
                """INSERT INTO findings (scan_id, agent_name, severity, description, remediation)
                   VALUES (?, ?, ?, ?, ?)""",
                (scan_id, f["agent_name"], f["severity"], f["description"], f.get("remediation")),
            )
        conn.commit()


def get_scan(scan_id: str) -> Optional[Dict[str, Any]]:
    """Fetch a single scan with its findings."""
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM scans WHERE scan_id = ?", (scan_id,)).fetchone()
        if row is None:
            return None
        scan = dict(row)
        findings_rows = conn.execute(
            "SELECT agent_name, severity, description, remediation FROM findings WHERE scan_id = ?",
            (scan_id,),
        ).fetchall()
        scan["findings"] = [dict(f) for f in findings_rows]
        return scan


def get_all_scans() -> List[Dict[str, Any]]:
    """Fetch all scans ordered by most recent first."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT scan_id, target_url, status, overall_score, created_at FROM scans ORDER BY created_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]
