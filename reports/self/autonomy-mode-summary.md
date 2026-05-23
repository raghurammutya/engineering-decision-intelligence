# Autonomy Mode Summary

Generated: `2026-05-23T04:11:49+00:00`

## Counts

- `observe`: 3
- `blocked`: 1
- `controlled_execute`: 1

## Mode Details

### `blocked`

- `tools/acceptance_gates.py`: critical, block or require controlled owner review before use

### `controlled_execute`

- `tools/operational_state_scan.py`: high, retain controlled execution with evidence

### `observe`

- `.github/workflows/ci.yml`: low, assign owner boundary
- `tools/autopilot_progress.py`: low, assign owner boundary
- `tools/check_report_drift.py`: low, assign owner boundary
