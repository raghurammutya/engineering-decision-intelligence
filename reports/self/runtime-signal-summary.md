# Runtime Signal Summary

Generated: `2026-05-23T04:35:15+00:00`

These records are inferred from repository artifacts. They are expected runtime-risk signals, not observed telemetry.

Runtime signal records: `4`
Runtime surface groups: `27`

## Environment Counts

- `dev`: 2
- `prod`: 2
- `test`: 2
- `staging`: 1
- `unknown`: 1

## Mutation Counts

- `ai_agent`: 3
- `broker_order`: 2
- `database`: 2
- `deployment`: 2
- `configuration`: 1
- `none_detected`: 1
- `queue_stream`: 1

## Evidence Counts

- `present`: 4

## Runtime Surface Groups

| Environment | Mutation Type | Evidence | Count | Risk | Top Paths |
| --- | --- | --- | --- | --- | --- |
| prod | ai_agent | present | 2 | critical:1, high:1 | `tools/acceptance_gates.py`<br>`tools/operational_state_scan.py` |
| prod | broker_order | present | 2 | critical:1, high:1 | `tools/acceptance_gates.py`<br>`tools/operational_state_scan.py` |
| prod | database | present | 2 | critical:1, high:1 | `tools/acceptance_gates.py`<br>`tools/operational_state_scan.py` |
| prod | deployment | present | 2 | critical:1, high:1 | `tools/acceptance_gates.py`<br>`tools/operational_state_scan.py` |
| dev | ai_agent | present | 1 | high:1 | `tools/operational_state_scan.py` |
| dev | broker_order | present | 1 | high:1 | `tools/operational_state_scan.py` |
| dev | configuration | present | 1 | high:1 | `tools/operational_state_scan.py` |
| dev | database | present | 1 | high:1 | `tools/operational_state_scan.py` |
| dev | deployment | present | 1 | high:1 | `tools/operational_state_scan.py` |
| dev | none_detected | present | 1 | low:1 | `.github/workflows/ci.yml` |
| dev | queue_stream | present | 1 | high:1 | `tools/operational_state_scan.py` |
| prod | configuration | present | 1 | high:1 | `tools/operational_state_scan.py` |
| prod | queue_stream | present | 1 | high:1 | `tools/operational_state_scan.py` |
| staging | ai_agent | present | 1 | high:1 | `tools/operational_state_scan.py` |
| staging | broker_order | present | 1 | high:1 | `tools/operational_state_scan.py` |
| staging | configuration | present | 1 | high:1 | `tools/operational_state_scan.py` |
| staging | database | present | 1 | high:1 | `tools/operational_state_scan.py` |
| staging | deployment | present | 1 | high:1 | `tools/operational_state_scan.py` |
| staging | queue_stream | present | 1 | high:1 | `tools/operational_state_scan.py` |
| test | ai_agent | present | 1 | high:1 | `tools/operational_state_scan.py` |
| test | broker_order | present | 1 | high:1 | `tools/operational_state_scan.py` |
| test | configuration | present | 1 | high:1 | `tools/operational_state_scan.py` |
| test | database | present | 1 | high:1 | `tools/operational_state_scan.py` |
| test | deployment | present | 1 | high:1 | `tools/operational_state_scan.py` |
| test | none_detected | present | 1 | low:1 | `.github/workflows/ci.yml` |
| test | queue_stream | present | 1 | high:1 | `tools/operational_state_scan.py` |
| unknown | ai_agent | present | 1 | medium:1 | `AGENTS.md` |
