# Telemetry Correlation Summary

Generated: `2026-05-23T04:00:57+00:00`

These correlations currently join inferred runtime signals with CI/CD, owner, and evidence dimensions. Observed telemetry is not ingested yet.

Correlation records: `3`

## Telemetry State

- `inferred_only`: 3

## CI/CD Surface Class

- `not_workflow`: 2
- `workflow_governance`: 1

## Owner Assignment Type

- `embedded_hint`: 2
- `missing_owner`: 1

## Evidence Status

- `present`: 3

## Highest-Risk Telemetry Gaps

| Path | Risk | CI/CD Surface | Owner Assignment | Evidence | Environments | Mutations |
| --- | --- | --- | --- | --- | --- | --- |
| `tools/acceptance_gates.py` | critical | not_workflow | embedded_hint | present | prod | deployment, database |
| `tools/operational_state_scan.py` | high | not_workflow | embedded_hint | present | prod, staging, test, dev | deployment, database, configuration, broker_order, queue_stream, ai_agent |
| `.github/workflows/ci.yml` | low | workflow_governance | missing_owner | present | test, dev | none_detected |
