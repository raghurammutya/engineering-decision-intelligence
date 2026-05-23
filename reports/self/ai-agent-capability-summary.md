# AI Agent Capability Summary

Generated: `2026-05-23T05:06:12+00:00`

These records are inferred from repository artifacts. They identify agent, prompt, command, evaluation, and AI-tooling surfaces.

AI-agent records: `3`

## Capability Levels

- `financial_or_order_capable`: 2
- `tool_using_or_prompted`: 1

## Safety Status

- `approval_required`: 1
- `blocked`: 1
- `observe`: 1

## Highest-Risk Agent Surfaces

| Path | Type | Capability | Safety | Risk | Owner | Eval Coverage | Next Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `tools/acceptance_gates.py` | tool | financial_or_order_capable | blocked | critical | present | referenced_evidence | block or require controlled owner review before use |
| `tools/operational_state_scan.py` | tool | financial_or_order_capable | approval_required | high | present | referenced_evidence | retain controlled execution with evidence |
| `AGENTS.md` | agent_policy | tool_using_or_prompted | observe | medium | present | referenced_evidence | map to canonical automation or document exception |
