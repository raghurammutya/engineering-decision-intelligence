# Agent Semantic Classifier Summary

Generated: `2026-05-23T05:26:49+00:00`

This v2 classifier separates context prompts, command surfaces, policy surfaces, evaluations, and direct execution capability.

Semantic records: `3`

## Semantic Classes

- `agent_policy`: 1
- `automation_with_agent_terms`: 2

## Capability Assertions

- `direct_execution_capability`: 2
- `governance_or_eval_surface`: 1

## Highest-Risk Semantic Records

| Path | Semantic Class | Capability Assertion | Capability Level | Risk | Evidence | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| `tools/acceptance_gates.py` | automation_with_agent_terms | direct_execution_capability | financial_or_order_capable | critical | present | present |
| `tools/operational_state_scan.py` | automation_with_agent_terms | direct_execution_capability | financial_or_order_capable | high | present | present |
| `AGENTS.md` | agent_policy | governance_or_eval_surface | tool_using_or_prompted | medium | present | present |
