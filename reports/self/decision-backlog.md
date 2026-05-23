# Decision Backlog

Generated: `2026-05-23T03:55:41+00:00`

This backlog is generated from scanner findings. It is decision support, not source truth.

## Action Lanes

| Lane | Items | Highest Priority | Dominant Owner | First Decision |
| --- | --- | --- | --- | --- |
| Block or certify critical operational mutation | 1 | P0 | present | block or require controlled owner review before use |
| Review before autonomy expansion | 4 | P3 | missing_or_unknown | retain controlled execution with evidence |

## Decisions

| Priority | Lane | Path | Risk | Autonomy | Owner | Decision Needed |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | Block or certify critical operational mutation | `tools/acceptance_gates.py` | critical | blocked | present | block or require controlled owner review before use |
| P3 | Review before autonomy expansion | `tools/operational_state_scan.py` | high | controlled_execute | present | retain controlled execution with evidence |
| P4 | Review before autonomy expansion | `.github/workflows/ci.yml` | low | observe | missing_or_unknown | assign owner boundary |
| P4 | Review before autonomy expansion | `tools/autopilot_progress.py` | low | observe | missing_or_unknown | assign owner boundary |
| P4 | Review before autonomy expansion | `tools/check_report_drift.py` | low | observe | missing_or_unknown | assign owner boundary |
