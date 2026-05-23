# Operational State Mutation Registry

Generated: `2026-05-23T05:26:49+00:00`
Pilot repository: `/home/stocksadmin/workspace/engineering-decision-intelligence`

This is a generated materialized view from local repository evidence.
It is not an authoritative source of truth.

## Local Git State

- Branch: `main`
- Remote: `git@github.com:raghurammutya/engineering-decision-intelligence.git`
- Dirty file count: `0`
- Ahead/behind: `0	1`

## Summary

- Artifacts scanned: `6`
- High or critical risk artifacts: `2`
- Blocked autonomy artifacts: `1`

### Risk Counts

- `low`: 3
- `critical`: 1
- `high`: 1
- `medium`: 1

### Autonomy Mode Counts

- `observe`: 3
- `blocked`: 1
- `controlled_execute`: 1
- `recommend`: 1

### Mutation Type Counts

- `ai_agent`: 3
- `none_detected`: 3
- `broker_order`: 2
- `database`: 2
- `deployment`: 2
- `configuration`: 1
- `queue_stream`: 1

## Highest-Risk Blocked Paths

| Path | Type | Environments | Mutation | Blocked Claims | Next Action |
| --- | --- | --- | --- | --- | --- |
| `tools/acceptance_gates.py` | tool | prod | deployment, database, broker_order, ai_agent | cannot claim canonical operating path<br>cannot claim autonomous execution readiness | block or require controlled owner review before use |

## Registry

| Path | Type | Risk | Autonomy | Canonical | Owner | Evidence | Exception | Next Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `tools/acceptance_gates.py` | tool | critical / high | blocked / operational_mutation | non_canonical_or_unknown | present | present | none | block or require controlled owner review before use |
| `tools/operational_state_scan.py` | tool | high / high | controlled_execute / operational_mutation | uses_canonical_command | present | present | none | retain controlled execution with evidence |
| `AGENTS.md` | agent_policy | medium / high | recommend / state_mutation_candidate | non_canonical_or_unknown | present | present | none | map to canonical automation or document exception |
| `.github/workflows/ci.yml` | workflow | low / low | observe / no_mutation_detected | not_mutation_capable | missing_or_unknown | present | none | assign owner boundary |
| `tools/autopilot_progress.py` | tool | low / low | observe / no_mutation_detected | not_mutation_capable | missing_or_unknown | present | none | assign owner boundary |
| `tools/check_report_drift.py` | tool | low / low | observe / no_mutation_detected | not_mutation_capable | missing_or_unknown | missing | none | assign owner boundary |
