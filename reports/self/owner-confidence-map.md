# Owner Confidence Map

Generated: `2026-05-23T05:00:14+00:00`

Owner workflow records: `6`

## Assignment Types

- `embedded_hint`: 3
- `missing_owner`: 3

## Review Classes

- `missing-owner-assignment`: 3
- `owner-map-normalization`: 3

## Lowest-Confidence Owner Decisions

| Confidence | Review Class | Owner | Boundary | Path | Risk | Action |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `.github/workflows/ci.yml` | low | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `tools/autopilot_progress.py` | low | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `tools/check_report_drift.py` | low | assign accountable owner boundary |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `tools/acceptance_gates.py` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `tools/operational_state_scan.py` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `AGENTS.md` | medium | convert embedded owner hint into owner-map rule |
