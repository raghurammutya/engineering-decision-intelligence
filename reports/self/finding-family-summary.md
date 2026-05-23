# Finding Family Summary

Generated: `2026-05-23T03:55:41+00:00`

| Family | Count | Critical | High | Blocked | Representative Next Action |
| --- | --- | --- | --- | --- | --- |
| `config_secret_scripts` | 1 | 0 | 1 | 0 | retain controlled execution with evidence |
| `db_migration_scripts` | 1 | 1 | 0 | 1 | block or require controlled owner review before use |
| `other_scripts` | 2 | 0 | 0 | 0 | assign owner boundary |
| `other_workflows` | 1 | 0 | 0 | 0 | assign owner boundary |

## Highest-Risk Examples By Family

### `config_secret_scripts`

- `tools/operational_state_scan.py`: high, controlled_execute

### `db_migration_scripts`

- `tools/acceptance_gates.py`: critical, blocked

### `other_scripts`

- `tools/autopilot_progress.py`: low, observe
- `tools/check_report_drift.py`: low, observe

### `other_workflows`

- `.github/workflows/ci.yml`: low, observe
