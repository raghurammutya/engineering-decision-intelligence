# AI Agent Capability Summary

Generated: `2026-05-23T04:44:14+00:00`

These records are inferred from repository artifacts. They identify agent, prompt, command, evaluation, and AI-tooling surfaces.

AI-agent records: `97`

## Capability Levels

- `financial_or_order_capable`: 76
- `runtime_mutating`: 19
- `tool_using_or_prompted`: 2

## Safety Status

- `approval_required`: 40
- `blocked`: 54
- `observe`: 3

## Highest-Risk Agent Surfaces

| Path | Type | Capability | Safety | Risk | Owner | Eval Coverage | Next Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `.claude/commands/assess-architecture.md` | agent_command | financial_or_order_capable | blocked | critical | missing_or_unknown | referenced_evidence | block or require controlled owner review before use |
| `.claude/commands/assess-infrastructure.md` | agent_command | financial_or_order_capable | blocked | critical | missing_or_unknown | referenced_evidence | block or require controlled owner review before use |
| `BACKEND_FIX_PROMPTS.md` | agent_prompt | financial_or_order_capable | blocked | critical | missing_or_unknown | test_evidence | block or require controlled owner review before use |
| `BACKEND_TEAM_PROMPT_ACCOUNT_SELECTOR.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `BACKEND_TEAM_PROMPT_BROKER_ACCOUNTS.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `NEXT_SESSION_PROMPT.md` | agent_prompt | financial_or_order_capable | blocked | critical | missing_or_unknown | test_evidence | block or require controlled owner review before use |
| `dev-prompt.txt` | agent_prompt | financial_or_order_capable | blocked | critical | missing_or_unknown | test_evidence | block or require controlled owner review before use |
| `docs/prompts/CLAUDE_CLI_PROMPT_GREEKS_CACHE_IMPLEMENTATION.md` | agent_prompt | financial_or_order_capable | blocked | critical | missing_or_unknown | test_evidence | block or require controlled owner review before use |
| `docs/prompts/CONFIG_SERVICE_GUIDE.md` | agent_prompt | financial_or_order_capable | blocked | critical | missing_or_unknown | test_evidence | block or require controlled owner review before use |
| `docs/prompts/CONFIG_SERVICE_IMPROVEMENTS.md` | agent_prompt | financial_or_order_capable | blocked | critical | missing_or_unknown | missing | block or require controlled owner review before use |
| `docs/prompts/MULTI_SERVICE_REFACTOR_BATCH_PROMPT.md` | agent_prompt | financial_or_order_capable | blocked | critical | missing_or_unknown | test_evidence | block or require controlled owner review before use |
| `docs/prompts/MY_STRATEGIES_SPRINT_PLAN.md` | agent_prompt | financial_or_order_capable | blocked | critical | missing_or_unknown | referenced_evidence | block or require controlled owner review before use |
| `docs/prompts/README.md` | agent_prompt | financial_or_order_capable | blocked | critical | missing_or_unknown | test_evidence | block or require controlled owner review before use |
| `docs/prompts/alert-service-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `docs/prompts/algo-engine-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | referenced_evidence | block or require controlled owner review before use |
| `docs/prompts/api-gateway-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `docs/prompts/backend-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `docs/prompts/billing-service-context-old.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `docs/prompts/billing-service-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `docs/prompts/calendar-service-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | missing_or_unknown | test_evidence | block or require controlled owner review before use |
| `docs/prompts/comms-service-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | missing_or_unknown | test_evidence | block or require controlled owner review before use |
| `docs/prompts/config-service-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `docs/prompts/data-relay-service-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `docs/prompts/fix-verified-issues-prompt.md` | agent_prompt | financial_or_order_capable | blocked | critical | missing_or_unknown | test_evidence | block or require controlled owner review before use |
| `docs/prompts/market-data-service-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `docs/prompts/marketplace-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | referenced_evidence | block or require controlled owner review before use |
| `docs/prompts/message-service-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `docs/prompts/news-service-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `docs/prompts/order-service-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `docs/prompts/payoff-service-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `docs/prompts/rating-service-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | missing_or_unknown | test_evidence | block or require controlled owner review before use |
| `docs/prompts/screener-service-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | referenced_evidence | block or require controlled owner review before use |
| `docs/prompts/signal-service-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `docs/prompts/system-overview.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `docs/prompts/ticker-service-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | missing_or_unknown | test_evidence | block or require controlled owner review before use |
| `docs/prompts/token-manager-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `docs/prompts/user-service-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `docs/prompts/ws-gateway-service-context.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `docs/qa/prompts/aef_next_tracks/AEF_306_STRATEGY_SDK_CHANNEL_EXECUTION_HANDOFF_PROMPT.md` | agent_prompt | financial_or_order_capable | blocked | critical | missing_or_unknown | test_evidence | block or require controlled owner review before use |
| `docs/qa/prompts/aef_next_tracks/AEF_DEFERRED_PRODUCTION_RESILIENCE_READINESS_PROMPT.md` | agent_prompt | financial_or_order_capable | blocked | critical | missing_or_unknown | referenced_evidence | block or require controlled owner review before use |
| `docs/qa/prompts/aef_next_tracks/AEF_ORCHESTRATOR_PROMPT.md` | agent_prompt | financial_or_order_capable | blocked | critical | missing_or_unknown | referenced_evidence | block or require controlled owner review before use |
| `docs/qa/prompts/aef_next_tracks/AEF_PARALLEL_ENTERPRISE_ARCHITECTURE_REVIEW_PROMPT.md` | agent_prompt | financial_or_order_capable | blocked | critical | present | referenced_evidence | block or require controlled owner review before use |
| `docs/qa/prompts/aef_next_tracks/README.md` | agent_prompt | financial_or_order_capable | blocked | critical | missing_or_unknown | referenced_evidence | block or require controlled owner review before use |
| `infra-prompt.txt` | agent_prompt | financial_or_order_capable | blocked | critical | missing_or_unknown | referenced_evidence | block or require controlled owner review before use |
| `scripts/governance/run_live_entry_exit_basket_probe.sh` | script | financial_or_order_capable | blocked | critical | platform-governance (governance automation) | test_evidence | block or require controlled owner review before use |
| `scripts/governance/run_promotion_preflight.sh` | script | financial_or_order_capable | blocked | critical | platform-governance (governance automation) | referenced_evidence | block or require controlled owner review before use |
| `signal_service/AGENTS.md` | agent_policy | financial_or_order_capable | blocked | critical | missing_or_unknown | test_evidence | block or require controlled owner review before use |
| `BACKEND_TEAM_PROMPT_PASSWORD_RESET_FIX.md` | agent_prompt | runtime_mutating | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `backend_prompt.md` | agent_prompt | runtime_mutating | blocked | critical | missing_or_unknown | test_evidence | block or require controlled owner review before use |
| `docs/prompts/EXTENDED_CONFIG_SERVICE.md` | agent_prompt | runtime_mutating | blocked | critical | missing_or_unknown | test_evidence | block or require controlled owner review before use |
| `docs/prompts/support-service-context.md` | agent_prompt | runtime_mutating | blocked | critical | missing_or_unknown | test_evidence | block or require controlled owner review before use |
| `scripts/production_checklist.py` | script | runtime_mutating | blocked | critical | present | test_evidence | block or require controlled owner review before use |
| `scripts/rotate_encryption_key.sh` | script | runtime_mutating | blocked | critical | missing_or_unknown | referenced_evidence | block or require controlled owner review before use |
| `scripts/smoke/verify_gateway_critical_paths.sh` | script | runtime_mutating | blocked | critical | missing_or_unknown | test_evidence | block or require controlled owner review before use |
| `.claude/commands/browser-test.md` | agent_command | financial_or_order_capable | approval_required | high | missing_or_unknown | test_evidence | map to canonical automation or document exception |
| `.claude/commands/service-context.md` | agent_command | financial_or_order_capable | approval_required | high | missing_or_unknown | referenced_evidence | map to canonical automation or document exception |
| `AGENTS.md` | agent_policy | financial_or_order_capable | approval_required | high | missing_or_unknown | referenced_evidence | assign owner boundary |
| `PHASE_2.5_DAY3_IMPLEMENTATION_PROMPT.md` | agent_prompt | financial_or_order_capable | approval_required | high | missing_or_unknown | test_evidence | map to canonical automation or document exception |
| `SPRINT_1.5_MARKETPLACE_INFRASTRUCTURE_PROMPT.md` | agent_prompt | financial_or_order_capable | approval_required | high | missing_or_unknown | test_evidence | map to canonical automation or document exception |
| `alert_service/app/background/evaluation_worker.py` | agent_evaluation | financial_or_order_capable | approval_required | high | missing_or_unknown | evaluation_artifact | map to canonical automation or document exception |
| `docs/prompts/ADV_ADVISORY_LAYER_IMPLEMENTATION.md` | agent_prompt | financial_or_order_capable | approval_required | high | missing_or_unknown | test_evidence | map to canonical automation or document exception |
| `docs/prompts/API_GATEWAY_ARCHITECTURE.md` | agent_prompt | financial_or_order_capable | approval_required | high | missing_or_unknown | missing | map to canonical automation or document exception |
| `docs/prompts/API_GATEWAY_TESTING_CONTINUATION.md` | agent_prompt | financial_or_order_capable | approval_required | high | present | test_evidence | map to canonical automation or document exception |
| `docs/prompts/FRONTEND_API_GATEWAY_MIGRATION.md` | agent_prompt | financial_or_order_capable | approval_required | high | present | referenced_evidence | map to canonical automation or document exception |
| `docs/prompts/MESSAGING_SERVICE_SPRINT_PLAN.md` | agent_prompt | financial_or_order_capable | approval_required | high | missing_or_unknown | test_evidence | map to canonical automation or document exception |
| `docs/prompts/MY_STRATEGIES_PAGE_REDESIGN.md` | agent_prompt | financial_or_order_capable | approval_required | high | missing_or_unknown | missing | map to canonical automation or document exception |
| `docs/prompts/algo-engine-advanced-intent-wiring-prompt.md` | agent_prompt | financial_or_order_capable | approval_required | high | missing_or_unknown | test_evidence | map to canonical automation or document exception |
| `docs/prompts/dataflows.md` | agent_prompt | financial_or_order_capable | approval_required | high | missing_or_unknown | missing | map to canonical automation or document exception |
| `docs/prompts/domain-glossary.md` | agent_prompt | financial_or_order_capable | approval_required | high | missing_or_unknown | missing | map to canonical automation or document exception |
| `docs/prompts/new-broker-integration-master-prompt.md` | agent_prompt | financial_or_order_capable | approval_required | high | missing_or_unknown | test_evidence | map to canonical automation or document exception |
| `docs/prompts/technical-writer-context.md` | agent_prompt | financial_or_order_capable | approval_required | high | missing_or_unknown | referenced_evidence | map to canonical automation or document exception |
| `docs/qa/prompts/aef_next_tracks/AEF_DEFERRED_BROKER_ORDER_WRITE_SAFETY_PROMPT.md` | agent_prompt | financial_or_order_capable | approval_required | high | missing_or_unknown | referenced_evidence | map to canonical automation or document exception |
| `docs/qa/prompts/aef_next_tracks/AEF_DEFERRED_COMMAND_CENTER_TRADING_DASHBOARD_ALIGNMENT_PROMPT.md` | agent_prompt | financial_or_order_capable | approval_required | high | missing_or_unknown | referenced_evidence | map to canonical automation or document exception |
| `docs/qa/prompts/aef_next_tracks/AEF_DEFERRED_RATE_POLICY_RUNTIME_ADMISSION_PROMPT.md` | agent_prompt | financial_or_order_capable | approval_required | high | present | referenced_evidence | map to canonical automation or document exception |
| `docs/qa/prompts/aef_next_tracks/AEF_PARALLEL_EXECUTION_METADATA_PROJECTION_REVIEW_PROMPT.md` | agent_prompt | financial_or_order_capable | approval_required | high | missing_or_unknown | referenced_evidence | map to canonical automation or document exception |
| `docs/qa/prompts/aef_next_tracks/AEF_PARALLEL_GATEWAY_DATA_READ_PROJECTION_REVIEW_PROMPT.md` | agent_prompt | financial_or_order_capable | approval_required | high | missing_or_unknown | referenced_evidence | map to canonical automation or document exception |
| `docs/qa/prompts/aef_next_tracks/AEF_PARALLEL_MANUAL_TRADING_SHARED_FOUNDATION_REVIEW_PROMPT.md` | agent_prompt | financial_or_order_capable | approval_required | high | present | referenced_evidence | map to canonical automation or document exception |
| `docs/qa/prompts/aef_next_tracks/AEF_PARALLEL_SCRIPT_STRATEGY_EXECUTION_REVIEW_PROMPT.md` | agent_prompt | financial_or_order_capable | approval_required | high | missing_or_unknown | test_evidence | map to canonical automation or document exception |
| `prompts_for_validation.md` | agent_prompt | financial_or_order_capable | approval_required | high | present | test_evidence | map to canonical automation or document exception |
| `scripts/decrypt_mf_xls.sh` | script | financial_or_order_capable | approval_required | high | missing_or_unknown | missing | map to canonical automation or document exception |
| `scripts/governance/run_execution_manual_order_probe.py` | script | financial_or_order_capable | approval_required | high | platform-governance (governance automation) | referenced_evidence | map to canonical automation or document exception |
| `scripts/governance/run_mcx_live_entry_exit_probe.sh` | script | financial_or_order_capable | approval_required | high | platform-governance (governance automation) | referenced_evidence | map to canonical automation or document exception |
| `.claude/commands/debug-browser.md` | agent_command | runtime_mutating | approval_required | high | missing_or_unknown | missing | map to canonical automation or document exception |
| `.claude/commands/update-service-prompt.md` | agent_command | runtime_mutating | approval_required | high | missing_or_unknown | referenced_evidence | map to canonical automation or document exception |
| `.github/workflows/streaming-tracker-watch.yml` | workflow | runtime_mutating | approval_required | high | present | missing | map to canonical automation or document exception |
| `BACKEND_TEAM_PROMPT_LOGIN_AFTER_SIGNUP.md` | agent_prompt | runtime_mutating | approval_required | high | present | test_evidence | map to canonical automation or document exception |
| `BROWSER_DEBUGGING_PROMPT.md` | agent_prompt | runtime_mutating | approval_required | high | missing_or_unknown | test_evidence | map to canonical automation or document exception |
| `alert_service/test_evaluation.py` | agent_evaluation | runtime_mutating | approval_required | high | missing_or_unknown | evaluation_artifact | map to canonical automation or document exception |
| `scripts/autonomous-debug.sh` | script | runtime_mutating | approval_required | high | missing_or_unknown | test_evidence | map to canonical automation or document exception |
| `scripts/grant-claude-permissions.sh` | script | runtime_mutating | approval_required | high | missing_or_unknown | test_evidence | map to canonical automation or document exception |
| `scripts/orchestrate_codex_claude.sh` | script | runtime_mutating | approval_required | high | missing_or_unknown | missing | map to canonical automation or document exception |
| `scripts/qa/service_taxonomy_parity/adapters/algo_engine.py` | script | runtime_mutating | approval_required | high | qa-governance (quality evidence) | test_evidence | map to canonical automation or document exception |
| `scripts/qa/service_taxonomy_parity/adapters/signal_service.py` | script | runtime_mutating | approval_required | high | qa-governance (quality evidence) | test_evidence | map to canonical automation or document exception |
| `scripts/system-cleanup.sh` | script | runtime_mutating | approval_required | high | missing_or_unknown | missing | map to canonical automation or document exception |
| `.claude/commands/watch-errors.md` | agent_command | tool_using_or_prompted | observe | medium | missing_or_unknown | missing | map to canonical automation or document exception |
| `scripts/qa/live_non_contra_probe_strategy.py` | script | financial_or_order_capable | observe | low | qa-governance (quality evidence) | missing | map to canonical automation or document exception |
| `scripts/governance/check_no_legacy_ticker_v2_strings.py` | script | tool_using_or_prompted | observe | low | platform-governance (governance automation) | test_evidence | map to canonical automation or document exception |
