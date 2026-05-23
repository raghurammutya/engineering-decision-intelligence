# Owner Review Queue

Generated: `2026-05-23T04:35:15+00:00`

| Review Class | Confidence | Owner | Boundary | Path | Risk | Autonomy | Blocked Claims | Next Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| missing-owner-assignment | 0.0 | unassigned | missing owner boundary | `.github/workflows/ci.yml` | low | observe | cannot claim owner-approved | assign owner boundary |
| missing-owner-assignment | 0.0 | unassigned | missing owner boundary | `tools/autopilot_progress.py` | low | observe | cannot claim owner-approved | assign owner boundary |
| missing-owner-assignment | 0.0 | unassigned | missing owner boundary | `tools/check_report_drift.py` | low | observe | cannot claim owner-approved<br>cannot claim evidence-backed safety | assign owner boundary |
| owner-map-normalization | 0.45 | embedded_owner_hint | owner text present without policy owner-map entry | `tools/acceptance_gates.py` | critical | blocked | cannot claim canonical operating path<br>cannot claim autonomous execution readiness | block or require controlled owner review before use |
| owner-map-normalization | 0.45 | embedded_owner_hint | owner text present without policy owner-map entry | `tools/operational_state_scan.py` | high | controlled_execute | cannot claim autonomous execution readiness | retain controlled execution with evidence |
| owner-map-normalization | 0.45 | embedded_owner_hint | owner text present without policy owner-map entry | `AGENTS.md` | medium | recommend | cannot claim canonical operating path | map to canonical automation or document exception |
