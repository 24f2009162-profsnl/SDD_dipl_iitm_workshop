# Proposal: CSV Export for Reports

**Why:** Users need to export report data for offline analysis.
**What Changes:** Add a CSV export capability to the `/reports` endpoint via a `.csv` route.
**Capabilities:** Export reports as CSV
**Impact:** High value for reporting teams. Architecture strictly enforces a 100,000 row limit and masks sensitive fields like internal_id.
