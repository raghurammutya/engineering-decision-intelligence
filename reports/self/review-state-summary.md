# Review State Summary

Generated: `2026-05-23T05:14:09+00:00`

This model gives each finding a deterministic review state. It is a workflow input, not an approval.

Review state records: `6`

## Review States

- `blocked_owner_review`: 1
- `controlled_execution_ready`: 1
- `observe`: 1
- `owner_assignment_required`: 3

## Highest-Priority Reviews

| Priority | State | Path | Risk | Owner | Evidence | Action |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | blocked_owner_review | `tools/acceptance_gates.py` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P3 | controlled_execution_ready | `tools/operational_state_scan.py` | high | embedded_owner_hint | present | retain controlled execution with evidence |
| P4 | observe | `AGENTS.md` | medium | embedded_owner_hint | present | observe |
| P4 | owner_assignment_required | `.github/workflows/ci.yml` | low | unassigned | present | assign accountable owner boundary |
| P4 | owner_assignment_required | `tools/autopilot_progress.py` | low | unassigned | present | assign accountable owner boundary |
| P4 | owner_assignment_required | `tools/check_report_drift.py` | low | unassigned | missing | assign accountable owner boundary |
