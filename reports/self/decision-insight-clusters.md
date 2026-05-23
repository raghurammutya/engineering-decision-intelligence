# Decision Insight Clusters

Generated: `2026-05-23T03:19:45+00:00`

Findings grouped: `5`
Decision clusters: `3`
Likely scanner tuning candidates: `0`
Likely operational blockers: `4`

## Top Decision Clusters

| Rank | Cluster | Findings | Risk Reduction Score | Scanner Tuning | Operational Blockers | Top Action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `config_secret_scripts::review-before-autonomy-expansion` | 1 | 70 | 0 | 1 | retain controlled execution with evidence |
| 2 | `other_scripts::review-before-autonomy-expansion` | 3 | 61 | 0 | 2 | assign owner boundary |
| 3 | `other_workflows::review-before-autonomy-expansion` | 1 | 22 | 0 | 1 | assign owner boundary |

## Scanner Tuning Candidates

| Path | Risk | Family | Reason | Suggested Action |
| --- | --- | --- | --- | --- |

## Operational Blockers

| Path | Risk | Autonomy | Family | Next Action |
| --- | --- | --- | --- | --- |
| `tools/operational_state_scan.py` | high | controlled_execute | config_secret_scripts | retain controlled execution with evidence |
| `tools/check_report_drift.py` | low | observe | other_scripts | assign owner boundary |
| `.github/workflows/ci.yml` | low | observe | other_workflows | assign owner boundary |
| `tools/autopilot_progress.py` | low | observe | other_scripts | assign owner boundary |
