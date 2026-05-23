# Review State Summary

Generated: `2026-05-23T04:52:01+00:00`

This model gives each finding a deterministic review state. It is a workflow input, not an approval.

Review state records: `567`

## Review States

- `accepted_exception_renewal`: 3
- `blocked_owner_review`: 169
- `controlled_execution_ready`: 5
- `evidence_required`: 30
- `observe`: 121
- `owner_assignment_required`: 179
- `scanner_tuning_review`: 60

## Highest-Priority Reviews

| Priority | State | Path | Risk | Owner | Evidence | Action |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | blocked_owner_review | `.claude/commands/assess-architecture.md` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `.claude/commands/assess-infrastructure.md` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `.github/workflows/backend-production-promotion-diagnose.yml` | critical | platform-governance | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `.github/workflows/ci.yml` | critical | platform-governance | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `.github/workflows/config-service-production-pipeline.yml` | critical | platform-governance | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `.github/workflows/deploy-backend-production.yml` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `.github/workflows/deploy-backend-staging.yml` | critical | platform-governance | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `.github/workflows/deploy-frontend-production.yml` | critical | platform-governance | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `.github/workflows/deploy-production.yml` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `.github/workflows/deploy-staging.yml` | critical | platform-governance | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `.github/workflows/environment-baseline-sync.yml` | critical | platform-governance | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `.github/workflows/integration-tests.yml` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `.github/workflows/port-consistency-check.yml` | critical | embedded_owner_hint | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `BACKEND_FIX_PROMPTS.md` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `BACKEND_TEAM_PROMPT_ACCOUNT_SELECTOR.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `BACKEND_TEAM_PROMPT_BROKER_ACCOUNTS.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `BACKEND_TEAM_PROMPT_PASSWORD_RESET_FIX.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `NEXT_SESSION_PROMPT.md` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `backend_prompt.md` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `dev-prompt.txt` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/CLAUDE_CLI_PROMPT_GREEKS_CACHE_IMPLEMENTATION.md` | critical | data-platform | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/CONFIG_SERVICE_GUIDE.md` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/CONFIG_SERVICE_IMPROVEMENTS.md` | critical | platform-security | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/EXTENDED_CONFIG_SERVICE.md` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/MULTI_SERVICE_REFACTOR_BATCH_PROMPT.md` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/MY_STRATEGIES_SPRINT_PLAN.md` | critical | data-platform | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/README.md` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/alert-service-context.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/algo-engine-context.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/api-gateway-context.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/backend-context.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/billing-service-context-old.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/billing-service-context.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/calendar-service-context.md` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/comms-service-context.md` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/config-service-context.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/data-relay-service-context.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/fix-verified-issues-prompt.md` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/market-data-service-context.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/marketplace-context.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/message-service-context.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/news-service-context.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/order-service-context.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/payoff-service-context.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/rating-service-context.md` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/screener-service-context.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/signal-service-context.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/support-service-context.md` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/system-overview.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/ticker-service-context.md` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/token-manager-context.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/user-service-context.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/prompts/ws-gateway-service-context.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/qa/prompts/aef_next_tracks/AEF_306_STRATEGY_SDK_CHANNEL_EXECUTION_HANDOFF_PROMPT.md` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/qa/prompts/aef_next_tracks/AEF_DEFERRED_PRODUCTION_RESILIENCE_READINESS_PROMPT.md` | critical | data-platform | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/qa/prompts/aef_next_tracks/AEF_ORCHESTRATOR_PROMPT.md` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/qa/prompts/aef_next_tracks/AEF_PARALLEL_ENTERPRISE_ARCHITECTURE_REVIEW_PROMPT.md` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `docs/qa/prompts/aef_next_tracks/README.md` | critical | trading-platform | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `infra-prompt.txt` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/apply_algo_engine_sql_migrations.sh` | critical | data-platform | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/apply_instrument_registry_migrations.sh` | critical | data-platform | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/apply_payoff_live_mode_config.sh` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/apply_service_sql_migrations.sh` | critical | data-platform | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/backfill_today_via_ticker_service.py` | critical | data-platform | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/backup/backup-service.py` | critical | platform-operations | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/bootstrap-dev-api-gateway-prereqs.py` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/bootstrap-dev-owner-service-prereqs.py` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/bootstrap_broker_rate_limit_profiles.py` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/bootstrap_nonprod_config_from_prod.py` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/code-quality-scan.sh` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/config.sh` | critical | platform-security | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/copy_market_data.py` | critical | data-platform | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/copy_market_data.sh` | critical | platform-security | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/data-migration.py` | critical | platform-security | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/deploy-phase1.sh` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/deploy-staging.sh` | critical | embedded_owner_hint | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/deploy.sh` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/deployment-gate.sh` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/detect_migration_regressions.sh` | critical | platform-security | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/fetch_today_options_data.py` | critical | platform-security | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/fix_config_service_encryption.sh` | critical | platform-security | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/fix_timezone_data.py` | critical | embedded_owner_hint | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/fix_timezone_data_all_tables.py` | critical | platform-security | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/governance/apply_prod_schema_to_envs.sh` | critical | platform-governance | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/governance/backfill_news_impacts_recent.sh` | critical | platform-governance | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/governance/bootstrap_algo_engine_sdk_contracts_config.py` | critical | platform-governance | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/governance/bootstrap_env_roles_and_grants.sh` | critical | platform-governance | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/governance/bootstrap_instrument_universe_config.py` | critical | platform-governance | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/governance/bootstrap_internal_order_route_signing.py` | critical | platform-governance | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/governance/bootstrap_internal_service_identity_config.py` | critical | platform-governance | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/governance/bootstrap_model_inference_config.py` | critical | platform-governance | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/governance/bootstrap_model_inference_config.sh` | critical | platform-governance | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/governance/bootstrap_order_service_trading_safety_config.py` | critical | platform-governance | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/governance/bootstrap_support_service_config.py` | critical | platform-governance | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/governance/check_config_parameter_seeds.py` | critical | platform-governance | missing | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/governance/check_runtime_public_schema_usage.py` | critical | platform-governance | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/governance/generate_trading_safety_dashboard_snapshot.py` | critical | platform-governance | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/governance/mirror_prod_images_to_lower_envs.sh` | critical | platform-governance | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/governance/run_backend_promotion_contract_preflight.sh` | critical | platform-governance | present | assign owner, confirm canonical path, attach evidence before execution |
| P0 | blocked_owner_review | `scripts/governance/run_channel_services_pilot_beta.py` | critical | platform-governance | present | assign owner, confirm canonical path, attach evidence before execution |
