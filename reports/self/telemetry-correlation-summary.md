# Telemetry Correlation Summary

Generated: `2026-05-23T05:00:14+00:00`

These correlations currently join inferred runtime signals with CI/CD, owner, and evidence dimensions. Observed telemetry is not ingested yet.

Correlation records: `4`

## Telemetry State

- `inferred_only`: 4

## CI/CD Surface Class

- `not_workflow`: 3
- `workflow_governance`: 1

## Owner Assignment Type

- `embedded_hint`: 3
- `missing_owner`: 1

## Evidence Status

- `present`: 4

## Highest-Risk Telemetry Gaps

| Path | Risk | CI/CD Surface | Owner Assignment | Evidence | Environments | Mutations |
| --- | --- | --- | --- | --- | --- | --- |
| `tools/acceptance_gates.py` | critical | not_workflow | embedded_hint | present | prod | deployment, database, broker_order, ai_agent |
| `tools/operational_state_scan.py` | high | not_workflow | embedded_hint | present | prod, staging, test, dev | deployment, database, configuration, broker_order, queue_stream, ai_agent |
| `AGENTS.md` | medium | not_workflow | embedded_hint | present | unknown | ai_agent |
| `.github/workflows/ci.yml` | low | workflow_governance | missing_owner | present | test, dev | none_detected |
