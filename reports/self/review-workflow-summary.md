# Review Workflow Summary

Generated: `2026-05-23T05:14:09+00:00`

This export turns review states into queueable workflow lanes.

Workflow records: `5`

## Workflow Lanes

- `Block or certify critical operational mutation`: 1
- `Review before autonomy expansion`: 4

## Review Queue

| Lane | State | Path | Priority | Owner | Transition | Action |
| --- | --- | --- | --- | --- | --- | --- |
| Block or certify critical operational mutation | blocked_owner_review | `tools/acceptance_gates.py` | P0 | embedded_owner_hint | open -> reviewed -> remediated_or_accepted | assign owner, confirm canonical path, attach evidence before execution |
| Review before autonomy expansion | controlled_execution_ready | `tools/operational_state_scan.py` | P3 | embedded_owner_hint | open -> reviewed -> remediated_or_accepted | retain controlled execution with evidence |
| Review before autonomy expansion | owner_assignment_required | `.github/workflows/ci.yml` | P4 | unassigned | open -> reviewed -> remediated_or_accepted | assign accountable owner boundary |
| Review before autonomy expansion | owner_assignment_required | `tools/autopilot_progress.py` | P4 | unassigned | open -> reviewed -> remediated_or_accepted | assign accountable owner boundary |
| Review before autonomy expansion | owner_assignment_required | `tools/check_report_drift.py` | P4 | unassigned | open -> reviewed -> remediated_or_accepted | assign accountable owner boundary |
