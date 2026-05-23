# Decision Insight Clusters

Generated: `2026-05-23T05:06:12+00:00`

Findings grouped: `6`
Decision clusters: `5`
Likely scanner tuning candidates: `0`
Likely operational blockers: `5`

## Top Decision Clusters

| Rank | Cluster | Findings | Risk Reduction Score | Scanner Tuning | Operational Blockers | Top Action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `db_migration_scripts::block-or-certify-critical-operational-mutation` | 1 | 190 | 0 | 1 | block or require controlled owner review before use |
| 2 | `config_secret_scripts::review-before-autonomy-expansion` | 1 | 70 | 0 | 1 | retain controlled execution with evidence |
| 3 | `other_scripts::review-before-autonomy-expansion` | 2 | 59 | 0 | 2 | assign owner boundary |
| 4 | `other_workflows::review-before-autonomy-expansion` | 1 | 22 | 0 | 1 | assign owner boundary |
| 5 | `ai_agent_tooling::canonicalize-or-document-exception` | 1 | 22 | 0 | 0 | map to canonical automation or document exception |

## Scanner Tuning Candidates

| Path | Risk | Family | Reason | Suggested Action |
| --- | --- | --- | --- | --- |

## Operational Blockers

| Path | Risk | Autonomy | Family | Next Action |
| --- | --- | --- | --- | --- |
| `tools/acceptance_gates.py` | critical | blocked | db_migration_scripts | block or require controlled owner review before use |
| `tools/operational_state_scan.py` | high | controlled_execute | config_secret_scripts | retain controlled execution with evidence |
| `tools/check_report_drift.py` | low | observe | other_scripts | assign owner boundary |
| `.github/workflows/ci.yml` | low | observe | other_workflows | assign owner boundary |
| `tools/autopilot_progress.py` | low | observe | other_scripts | assign owner boundary |
