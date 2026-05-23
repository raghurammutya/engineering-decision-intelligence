# Finding Family Summary

Generated: `2026-05-23T03:01:31+00:00`

| Family | Count | Critical | High | Blocked | Representative Next Action |
| --- | --- | --- | --- | --- | --- |
| `config_secret_scripts` | 1 | 0 | 1 | 0 | retain controlled execution with evidence |
| `other_scripts` | 3 | 0 | 0 | 0 | observe |
| `other_workflows` | 1 | 0 | 0 | 0 | assign owner boundary |

## Highest-Risk Examples By Family

### `config_secret_scripts`

- `tools/operational_state_scan.py`: high, controlled_execute

### `other_scripts`

- `tools/acceptance_gates.py`: low, observe
- `tools/autopilot_progress.py`: low, observe
- `tools/check_report_drift.py`: low, observe

### `other_workflows`

- `.github/workflows/ci.yml`: low, observe
