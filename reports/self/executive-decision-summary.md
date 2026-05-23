# Executive Decision Summary

Generated: `2026-05-23T04:04:06+00:00`

## Priority Counts

- `P0`: 1
- `P3`: 1
- `P4`: 3

## Top Decisions

| Priority | Path | Reason | Owner | Decision |
| --- | --- | --- | --- | --- |
| P0 | `tools/acceptance_gates.py` | blocked production mutation | present | block or require controlled owner review before use |
| P3 | `tools/operational_state_scan.py` | retain controlled execution with evidence | present | retain controlled execution with evidence |
| P4 | `.github/workflows/ci.yml` | assign owner boundary | missing_or_unknown | assign owner boundary |
| P4 | `tools/autopilot_progress.py` | assign owner boundary | missing_or_unknown | assign owner boundary |
| P4 | `tools/check_report_drift.py` | assign owner boundary | missing_or_unknown | assign owner boundary |
