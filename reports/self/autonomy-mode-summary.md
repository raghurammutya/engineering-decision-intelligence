# Autonomy Mode Summary

Generated: `2026-05-23T03:22:58+00:00`

## Counts

- `observe`: 3
- `controlled_execute`: 1
- `recommend`: 1

## Mode Details

### `controlled_execute`

- `tools/operational_state_scan.py`: high, retain controlled execution with evidence

### `recommend`

- `tools/acceptance_gates.py`: medium, map to canonical automation or document exception

### `observe`

- `.github/workflows/ci.yml`: low, assign owner boundary
- `tools/autopilot_progress.py`: low, assign owner boundary
- `tools/check_report_drift.py`: low, assign owner boundary
