# Agent Semantic Classifier Summary

Generated: `2026-05-23T04:52:01+00:00`

This v2 classifier separates context prompts, command surfaces, policy surfaces, evaluations, and direct execution capability.

Semantic records: `97`

## Semantic Classes

- `agent_command`: 7
- `agent_policy`: 2
- `automation_with_agent_terms`: 17
- `context_prompt`: 64
- `evaluation_surface`: 2
- `high_risk_prompt_claim`: 5

## Capability Assertions

- `direct_execution_capability`: 24
- `governance_or_eval_surface`: 4
- `prompted_capability_claim`: 69

## Highest-Risk Semantic Records

| Path | Semantic Class | Capability Assertion | Capability Level | Risk | Evidence | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| `.claude/commands/assess-architecture.md` | agent_command | direct_execution_capability | financial_or_order_capable | critical | present | missing_or_unknown |
| `.claude/commands/assess-infrastructure.md` | agent_command | direct_execution_capability | financial_or_order_capable | critical | present | missing_or_unknown |
| `signal_service/AGENTS.md` | agent_policy | governance_or_eval_surface | financial_or_order_capable | critical | present | missing_or_unknown |
| `scripts/governance/run_live_entry_exit_basket_probe.sh` | automation_with_agent_terms | direct_execution_capability | financial_or_order_capable | critical | present | present |
| `scripts/governance/run_promotion_preflight.sh` | automation_with_agent_terms | direct_execution_capability | financial_or_order_capable | critical | present | present |
| `scripts/production_checklist.py` | automation_with_agent_terms | direct_execution_capability | runtime_mutating | critical | present | present |
| `scripts/rotate_encryption_key.sh` | automation_with_agent_terms | direct_execution_capability | runtime_mutating | critical | present | missing_or_unknown |
| `scripts/smoke/verify_gateway_critical_paths.sh` | automation_with_agent_terms | direct_execution_capability | runtime_mutating | critical | present | missing_or_unknown |
| `BACKEND_FIX_PROMPTS.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | missing_or_unknown |
| `BACKEND_TEAM_PROMPT_ACCOUNT_SELECTOR.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `BACKEND_TEAM_PROMPT_BROKER_ACCOUNTS.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `BACKEND_TEAM_PROMPT_PASSWORD_RESET_FIX.md` | context_prompt | prompted_capability_claim | runtime_mutating | critical | present | present |
| `NEXT_SESSION_PROMPT.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | missing_or_unknown |
| `backend_prompt.md` | context_prompt | prompted_capability_claim | runtime_mutating | critical | present | missing_or_unknown |
| `dev-prompt.txt` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | missing_or_unknown |
| `docs/prompts/CLAUDE_CLI_PROMPT_GREEKS_CACHE_IMPLEMENTATION.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | missing_or_unknown |
| `docs/prompts/CONFIG_SERVICE_GUIDE.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | missing_or_unknown |
| `docs/prompts/EXTENDED_CONFIG_SERVICE.md` | context_prompt | prompted_capability_claim | runtime_mutating | critical | present | missing_or_unknown |
| `docs/prompts/MULTI_SERVICE_REFACTOR_BATCH_PROMPT.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | missing_or_unknown |
| `docs/prompts/MY_STRATEGIES_SPRINT_PLAN.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | missing_or_unknown |
| `docs/prompts/README.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | missing_or_unknown |
| `docs/prompts/alert-service-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/prompts/algo-engine-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/prompts/api-gateway-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/prompts/backend-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/prompts/billing-service-context-old.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/prompts/billing-service-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/prompts/calendar-service-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | missing_or_unknown |
| `docs/prompts/comms-service-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | missing_or_unknown |
| `docs/prompts/config-service-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/prompts/data-relay-service-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/prompts/fix-verified-issues-prompt.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | missing_or_unknown |
| `docs/prompts/market-data-service-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/prompts/marketplace-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/prompts/message-service-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/prompts/news-service-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/prompts/order-service-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/prompts/payoff-service-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/prompts/rating-service-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | missing_or_unknown |
| `docs/prompts/screener-service-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/prompts/signal-service-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/prompts/support-service-context.md` | context_prompt | prompted_capability_claim | runtime_mutating | critical | present | missing_or_unknown |
| `docs/prompts/system-overview.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/prompts/ticker-service-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | missing_or_unknown |
| `docs/prompts/token-manager-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/prompts/user-service-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/prompts/ws-gateway-service-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/qa/prompts/aef_next_tracks/AEF_306_STRATEGY_SDK_CHANNEL_EXECUTION_HANDOFF_PROMPT.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | missing_or_unknown |
| `docs/qa/prompts/aef_next_tracks/AEF_DEFERRED_PRODUCTION_RESILIENCE_READINESS_PROMPT.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | missing_or_unknown |
| `docs/qa/prompts/aef_next_tracks/AEF_ORCHESTRATOR_PROMPT.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | missing_or_unknown |
| `docs/qa/prompts/aef_next_tracks/AEF_PARALLEL_ENTERPRISE_ARCHITECTURE_REVIEW_PROMPT.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | present |
| `docs/qa/prompts/aef_next_tracks/README.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | missing_or_unknown |
| `infra-prompt.txt` | context_prompt | prompted_capability_claim | financial_or_order_capable | critical | present | missing_or_unknown |
| `docs/prompts/CONFIG_SERVICE_IMPROVEMENTS.md` | high_risk_prompt_claim | prompted_capability_claim | financial_or_order_capable | critical | missing | missing_or_unknown |
| `.claude/commands/browser-test.md` | agent_command | direct_execution_capability | financial_or_order_capable | high | present | missing_or_unknown |
| `.claude/commands/debug-browser.md` | agent_command | direct_execution_capability | runtime_mutating | high | missing | missing_or_unknown |
| `.claude/commands/service-context.md` | agent_command | direct_execution_capability | financial_or_order_capable | high | present | missing_or_unknown |
| `.claude/commands/update-service-prompt.md` | agent_command | direct_execution_capability | runtime_mutating | high | present | missing_or_unknown |
| `AGENTS.md` | agent_policy | governance_or_eval_surface | financial_or_order_capable | high | present | missing_or_unknown |
| `.github/workflows/streaming-tracker-watch.yml` | automation_with_agent_terms | direct_execution_capability | runtime_mutating | high | missing | present |
| `scripts/autonomous-debug.sh` | automation_with_agent_terms | direct_execution_capability | runtime_mutating | high | present | missing_or_unknown |
| `scripts/decrypt_mf_xls.sh` | automation_with_agent_terms | direct_execution_capability | financial_or_order_capable | high | missing | missing_or_unknown |
| `scripts/governance/run_execution_manual_order_probe.py` | automation_with_agent_terms | direct_execution_capability | financial_or_order_capable | high | present | present |
| `scripts/governance/run_mcx_live_entry_exit_probe.sh` | automation_with_agent_terms | direct_execution_capability | financial_or_order_capable | high | present | present |
| `scripts/grant-claude-permissions.sh` | automation_with_agent_terms | direct_execution_capability | runtime_mutating | high | present | missing_or_unknown |
| `scripts/orchestrate_codex_claude.sh` | automation_with_agent_terms | direct_execution_capability | runtime_mutating | high | missing | missing_or_unknown |
| `scripts/qa/service_taxonomy_parity/adapters/algo_engine.py` | automation_with_agent_terms | direct_execution_capability | runtime_mutating | high | present | present |
| `scripts/qa/service_taxonomy_parity/adapters/signal_service.py` | automation_with_agent_terms | direct_execution_capability | runtime_mutating | high | present | present |
| `scripts/system-cleanup.sh` | automation_with_agent_terms | direct_execution_capability | runtime_mutating | high | missing | missing_or_unknown |
| `BACKEND_TEAM_PROMPT_LOGIN_AFTER_SIGNUP.md` | context_prompt | prompted_capability_claim | runtime_mutating | high | present | present |
| `BROWSER_DEBUGGING_PROMPT.md` | context_prompt | prompted_capability_claim | runtime_mutating | high | present | missing_or_unknown |
| `PHASE_2.5_DAY3_IMPLEMENTATION_PROMPT.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | high | present | missing_or_unknown |
| `SPRINT_1.5_MARKETPLACE_INFRASTRUCTURE_PROMPT.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | high | present | missing_or_unknown |
| `docs/prompts/ADV_ADVISORY_LAYER_IMPLEMENTATION.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | high | present | missing_or_unknown |
| `docs/prompts/API_GATEWAY_TESTING_CONTINUATION.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | high | present | present |
| `docs/prompts/FRONTEND_API_GATEWAY_MIGRATION.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | high | present | present |
| `docs/prompts/MESSAGING_SERVICE_SPRINT_PLAN.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | high | present | missing_or_unknown |
| `docs/prompts/algo-engine-advanced-intent-wiring-prompt.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | high | present | missing_or_unknown |
| `docs/prompts/new-broker-integration-master-prompt.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | high | present | missing_or_unknown |
| `docs/prompts/technical-writer-context.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | high | present | missing_or_unknown |
| `docs/qa/prompts/aef_next_tracks/AEF_DEFERRED_BROKER_ORDER_WRITE_SAFETY_PROMPT.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | high | present | missing_or_unknown |
| `docs/qa/prompts/aef_next_tracks/AEF_DEFERRED_COMMAND_CENTER_TRADING_DASHBOARD_ALIGNMENT_PROMPT.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | high | present | missing_or_unknown |
| `docs/qa/prompts/aef_next_tracks/AEF_DEFERRED_RATE_POLICY_RUNTIME_ADMISSION_PROMPT.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | high | present | present |
| `docs/qa/prompts/aef_next_tracks/AEF_PARALLEL_EXECUTION_METADATA_PROJECTION_REVIEW_PROMPT.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | high | present | missing_or_unknown |
| `docs/qa/prompts/aef_next_tracks/AEF_PARALLEL_GATEWAY_DATA_READ_PROJECTION_REVIEW_PROMPT.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | high | present | missing_or_unknown |
| `docs/qa/prompts/aef_next_tracks/AEF_PARALLEL_MANUAL_TRADING_SHARED_FOUNDATION_REVIEW_PROMPT.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | high | present | present |
| `docs/qa/prompts/aef_next_tracks/AEF_PARALLEL_SCRIPT_STRATEGY_EXECUTION_REVIEW_PROMPT.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | high | present | missing_or_unknown |
| `prompts_for_validation.md` | context_prompt | prompted_capability_claim | financial_or_order_capable | high | present | present |
| `alert_service/app/background/evaluation_worker.py` | evaluation_surface | governance_or_eval_surface | financial_or_order_capable | high | present | missing_or_unknown |
| `alert_service/test_evaluation.py` | evaluation_surface | governance_or_eval_surface | runtime_mutating | high | present | missing_or_unknown |
| `docs/prompts/API_GATEWAY_ARCHITECTURE.md` | high_risk_prompt_claim | prompted_capability_claim | financial_or_order_capable | high | missing | missing_or_unknown |
| `docs/prompts/MY_STRATEGIES_PAGE_REDESIGN.md` | high_risk_prompt_claim | prompted_capability_claim | financial_or_order_capable | high | missing | missing_or_unknown |
| `docs/prompts/dataflows.md` | high_risk_prompt_claim | prompted_capability_claim | financial_or_order_capable | high | missing | missing_or_unknown |
| `docs/prompts/domain-glossary.md` | high_risk_prompt_claim | prompted_capability_claim | financial_or_order_capable | high | missing | missing_or_unknown |
| `.claude/commands/watch-errors.md` | agent_command | direct_execution_capability | tool_using_or_prompted | medium | missing | missing_or_unknown |
| `scripts/governance/check_no_legacy_ticker_v2_strings.py` | automation_with_agent_terms | direct_execution_capability | tool_using_or_prompted | low | present | present |
| `scripts/qa/live_non_contra_probe_strategy.py` | automation_with_agent_terms | direct_execution_capability | financial_or_order_capable | low | missing | present |
