# Agent Drift And Evaluation Summary

Generated: `2026-05-23T04:44:14+00:00`

This view highlights AI-agent surfaces with capability drift, missing owner boundaries, or missing evaluation evidence.

Drift/evaluation records: `59`

## Drift Status

- `capability_escalation_without_evidence`: 10
- `missing_eval_coverage`: 1
- `ownerless_agent_surface`: 48

## Evaluation Coverage

- `evaluation_artifact`: 2
- `missing`: 12
- `referenced_evidence`: 16
- `test_evidence`: 29

## Review Queue

| Path | Capability | Drift | Eval Coverage | Safety | Risk | Owner | Next Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `docs/prompts/CONFIG_SERVICE_IMPROVEMENTS.md` | financial_or_order_capable | capability_escalation_without_evidence | missing | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `.claude/commands/assess-architecture.md` | financial_or_order_capable | ownerless_agent_surface | referenced_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `.claude/commands/assess-infrastructure.md` | financial_or_order_capable | ownerless_agent_surface | referenced_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `BACKEND_FIX_PROMPTS.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `NEXT_SESSION_PROMPT.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `backend_prompt.md` | runtime_mutating | ownerless_agent_surface | test_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `dev-prompt.txt` | financial_or_order_capable | ownerless_agent_surface | test_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `docs/prompts/CLAUDE_CLI_PROMPT_GREEKS_CACHE_IMPLEMENTATION.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `docs/prompts/CONFIG_SERVICE_GUIDE.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `docs/prompts/EXTENDED_CONFIG_SERVICE.md` | runtime_mutating | ownerless_agent_surface | test_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `docs/prompts/MULTI_SERVICE_REFACTOR_BATCH_PROMPT.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `docs/prompts/MY_STRATEGIES_SPRINT_PLAN.md` | financial_or_order_capable | ownerless_agent_surface | referenced_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `docs/prompts/README.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `docs/prompts/calendar-service-context.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `docs/prompts/comms-service-context.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `docs/prompts/fix-verified-issues-prompt.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `docs/prompts/rating-service-context.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `docs/prompts/support-service-context.md` | runtime_mutating | ownerless_agent_surface | test_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `docs/prompts/ticker-service-context.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `docs/qa/prompts/aef_next_tracks/AEF_306_STRATEGY_SDK_CHANNEL_EXECUTION_HANDOFF_PROMPT.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `docs/qa/prompts/aef_next_tracks/AEF_DEFERRED_PRODUCTION_RESILIENCE_READINESS_PROMPT.md` | financial_or_order_capable | ownerless_agent_surface | referenced_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `docs/qa/prompts/aef_next_tracks/AEF_ORCHESTRATOR_PROMPT.md` | financial_or_order_capable | ownerless_agent_surface | referenced_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `docs/qa/prompts/aef_next_tracks/README.md` | financial_or_order_capable | ownerless_agent_surface | referenced_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `infra-prompt.txt` | financial_or_order_capable | ownerless_agent_surface | referenced_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `scripts/rotate_encryption_key.sh` | runtime_mutating | ownerless_agent_surface | referenced_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `scripts/smoke/verify_gateway_critical_paths.sh` | runtime_mutating | ownerless_agent_surface | test_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `signal_service/AGENTS.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | blocked | critical | missing_or_unknown | block or require controlled owner review before use |
| `.claude/commands/debug-browser.md` | runtime_mutating | capability_escalation_without_evidence | missing | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `.github/workflows/streaming-tracker-watch.yml` | runtime_mutating | capability_escalation_without_evidence | missing | approval_required | high | present | map to canonical automation or document exception |
| `docs/prompts/API_GATEWAY_ARCHITECTURE.md` | financial_or_order_capable | capability_escalation_without_evidence | missing | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `docs/prompts/MY_STRATEGIES_PAGE_REDESIGN.md` | financial_or_order_capable | capability_escalation_without_evidence | missing | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `docs/prompts/dataflows.md` | financial_or_order_capable | capability_escalation_without_evidence | missing | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `docs/prompts/domain-glossary.md` | financial_or_order_capable | capability_escalation_without_evidence | missing | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `scripts/decrypt_mf_xls.sh` | financial_or_order_capable | capability_escalation_without_evidence | missing | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `scripts/orchestrate_codex_claude.sh` | runtime_mutating | capability_escalation_without_evidence | missing | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `scripts/system-cleanup.sh` | runtime_mutating | capability_escalation_without_evidence | missing | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `.claude/commands/browser-test.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `.claude/commands/service-context.md` | financial_or_order_capable | ownerless_agent_surface | referenced_evidence | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `.claude/commands/update-service-prompt.md` | runtime_mutating | ownerless_agent_surface | referenced_evidence | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `AGENTS.md` | financial_or_order_capable | ownerless_agent_surface | referenced_evidence | approval_required | high | missing_or_unknown | assign owner boundary |
| `BROWSER_DEBUGGING_PROMPT.md` | runtime_mutating | ownerless_agent_surface | test_evidence | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `PHASE_2.5_DAY3_IMPLEMENTATION_PROMPT.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `SPRINT_1.5_MARKETPLACE_INFRASTRUCTURE_PROMPT.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `alert_service/app/background/evaluation_worker.py` | financial_or_order_capable | ownerless_agent_surface | evaluation_artifact | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `alert_service/test_evaluation.py` | runtime_mutating | ownerless_agent_surface | evaluation_artifact | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `docs/prompts/ADV_ADVISORY_LAYER_IMPLEMENTATION.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `docs/prompts/MESSAGING_SERVICE_SPRINT_PLAN.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `docs/prompts/algo-engine-advanced-intent-wiring-prompt.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `docs/prompts/new-broker-integration-master-prompt.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `docs/prompts/technical-writer-context.md` | financial_or_order_capable | ownerless_agent_surface | referenced_evidence | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `docs/qa/prompts/aef_next_tracks/AEF_DEFERRED_BROKER_ORDER_WRITE_SAFETY_PROMPT.md` | financial_or_order_capable | ownerless_agent_surface | referenced_evidence | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `docs/qa/prompts/aef_next_tracks/AEF_DEFERRED_COMMAND_CENTER_TRADING_DASHBOARD_ALIGNMENT_PROMPT.md` | financial_or_order_capable | ownerless_agent_surface | referenced_evidence | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `docs/qa/prompts/aef_next_tracks/AEF_PARALLEL_EXECUTION_METADATA_PROJECTION_REVIEW_PROMPT.md` | financial_or_order_capable | ownerless_agent_surface | referenced_evidence | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `docs/qa/prompts/aef_next_tracks/AEF_PARALLEL_GATEWAY_DATA_READ_PROJECTION_REVIEW_PROMPT.md` | financial_or_order_capable | ownerless_agent_surface | referenced_evidence | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `docs/qa/prompts/aef_next_tracks/AEF_PARALLEL_SCRIPT_STRATEGY_EXECUTION_REVIEW_PROMPT.md` | financial_or_order_capable | ownerless_agent_surface | test_evidence | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `scripts/autonomous-debug.sh` | runtime_mutating | ownerless_agent_surface | test_evidence | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `scripts/grant-claude-permissions.sh` | runtime_mutating | ownerless_agent_surface | test_evidence | approval_required | high | missing_or_unknown | map to canonical automation or document exception |
| `.claude/commands/watch-errors.md` | tool_using_or_prompted | ownerless_agent_surface | missing | observe | medium | missing_or_unknown | map to canonical automation or document exception |
| `scripts/qa/live_non_contra_probe_strategy.py` | financial_or_order_capable | missing_eval_coverage | missing | observe | low | qa-governance (quality evidence) | map to canonical automation or document exception |
