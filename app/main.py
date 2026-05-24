"""FastAPI HTTP layer for the Reports app."""

from __future__ import annotations

from datetime import datetime

from fastapi import FastAPI, HTTPException, Query

from app.models import ReportListResponse, ReportPublic, ReportStatus
from app.reports import query

app = FastAPI(title="SDD Workshop — Reports API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/reports", response_model=ReportListResponse)
def list_reports(
    status: ReportStatus | None = Query(None, description="Filter by status"),
    date_from: datetime | None = Query(None, description="Lower bound on created_at (inclusive)"),
    date_to: datetime | None = Query(None, description="Upper bound on created_at (inclusive)"),
    sort: str = Query("created_at", description="Sort field"),
    descending: bool = Query(True, description="Sort descending"),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
) -> ReportListResponse:
    """Return a paginated list of reports.

    Public fields only — `internal_id` and `owner_email` are stripped via
    `ReportPublic.from_internal`.
    """

    try:
        rows = query(
            status=status,
            date_from=date_from,
            date_to=date_to,
            sort=sort,
            descending=descending,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    page = rows[offset : offset + limit]
    return ReportListResponse(
        items=[ReportPublic.from_internal(r) for r in page],
        total=len(rows),
        offset=offset,
        limit=limit,
    )
from fastapi import HTTPException, Header, Request
from fastapi.responses import Response
from typing import Optional
import csv
import io
from datetime import datetime

@app.get("/reports.csv")
def secure_csv_export(request: Request, x_user_timezone: Optional[str] = Header("UTC")):
    # Fetch data safely
    reports = getattr(request.app.state, "reports_data", []) 
    
    # 413 Error for row limit (Required by checks.md)
    if len(reports) > 100000:
        raise HTTPException(
            status_code=413, 
            detail={"detail": "result set too large; apply more filters", "max_rows": 100000}
        )

    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    
    # Strict Column Allowlist
    allowed_columns = ["id", "title", "status", "owner", "amount", "created_at"]
    writer.writerow(allowed_columns)
    
    for report in reports:
        row = [report.get(col, "") if isinstance(report, dict) else getattr(report, col, "") for col in allowed_columns]
        writer.writerow(row)
        
    # Dynamic Headers
    date_str = datetime.now().strftime("%Y-%m-%d")
    headers = {
        "Content-Type": "text/csv; charset=utf-8",
        "Content-Disposition": f'attachment; filename="reports-{date_str}.csv"'
    }
    
    return Response(content=output.getvalue(), media_type="text/csv", headers=headers)