# Owner Confidence Map

Generated: `2026-05-23T03:22:58+00:00`

Owner workflow records: `5`

## Assignment Types

- `missing_owner`: 3
- `embedded_hint`: 2

## Review Classes

- `missing-owner-assignment`: 3
- `owner-map-normalization`: 2

## Lowest-Confidence Owner Decisions

| Confidence | Review Class | Owner | Boundary | Path | Risk | Action |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `.github/workflows/ci.yml` | low | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `tools/autopilot_progress.py` | low | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `tools/check_report_drift.py` | low | assign accountable owner boundary |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `tools/operational_state_scan.py` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `tools/acceptance_gates.py` | medium | convert embedded owner hint into owner-map rule |
