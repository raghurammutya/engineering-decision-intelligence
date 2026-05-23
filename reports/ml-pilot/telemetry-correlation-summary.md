# Telemetry Correlation Summary

Generated: `2026-05-23T04:33:14+00:00`

These correlations currently join inferred runtime signals with CI/CD, owner, and evidence dimensions. Observed telemetry is not ingested yet.

Correlation records: `538`

## Telemetry State

- `inferred_only`: 538

## CI/CD Surface Class

- `deployment_capable`: 18
- `not_workflow`: 515
- `validation_only`: 5

## Owner Assignment Type

- `declared_owner_map`: 225
- `embedded_hint`: 53
- `inferred_suggestion`: 244
- `missing_owner`: 16

## Evidence Status

- `missing`: 163
- `present`: 375

## Highest-Risk Telemetry Gaps

| Path | Risk | CI/CD Surface | Owner Assignment | Evidence | Environments | Mutations |
| --- | --- | --- | --- | --- | --- | --- |
| `.github/workflows/backend-production-promotion-diagnose.yml` | critical | deployment_capable | inferred_suggestion | present | prod, test, dev | deployment, database, infrastructure, configuration, runtime_shell |
| `.github/workflows/ci.yml` | critical | deployment_capable | inferred_suggestion | present | prod, staging, test | deployment, infrastructure, configuration, queue_stream |
| `.github/workflows/config-service-production-pipeline.yml` | critical | deployment_capable | inferred_suggestion | present | prod, staging, test, dev | deployment, database, infrastructure, configuration, queue_stream, runtime_shell |
| `.github/workflows/deploy-backend-production.yml` | critical | deployment_capable | embedded_hint | present | prod, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `.github/workflows/deploy-backend-staging.yml` | critical | deployment_capable | inferred_suggestion | present | prod, staging, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `.github/workflows/deploy-frontend-production.yml` | critical | deployment_capable | inferred_suggestion | present | prod, staging, test, dev | deployment, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `.github/workflows/deploy-production.yml` | critical | deployment_capable | embedded_hint | present | prod, test, dev | deployment, database, infrastructure, configuration, broker_order, runtime_shell |
| `.github/workflows/deploy-staging.yml` | critical | deployment_capable | inferred_suggestion | present | prod, staging, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `.github/workflows/environment-baseline-sync.yml` | critical | deployment_capable | inferred_suggestion | present | prod, staging, test, dev | configuration |
| `.github/workflows/integration-tests.yml` | critical | deployment_capable | embedded_hint | present | prod, staging, test, dev | deployment, database, infrastructure, configuration, queue_stream |
| `.github/workflows/port-consistency-check.yml` | critical | deployment_capable | embedded_hint | missing | prod | deployment, database, infrastructure, configuration |
| `.claude/commands/assess-architecture.md` | critical | not_workflow | inferred_suggestion | present | prod, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell, ai_agent |
| `.claude/commands/assess-infrastructure.md` | critical | not_workflow | inferred_suggestion | present | prod, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell, ai_agent |
| `BACKEND_FIX_PROMPTS.md` | critical | not_workflow | inferred_suggestion | present | prod, test, dev | database, infrastructure, configuration, broker_order, queue_stream, runtime_shell, ai_agent |
| `BACKEND_TEAM_PROMPT_ACCOUNT_SELECTOR.md` | critical | not_workflow | embedded_hint | present | prod, test, dev | deployment, database, broker_order, queue_stream |
| `BACKEND_TEAM_PROMPT_BROKER_ACCOUNTS.md` | critical | not_workflow | embedded_hint | present | prod, test | deployment, database, infrastructure, configuration, broker_order, queue_stream, ai_agent |
| `BACKEND_TEAM_PROMPT_PASSWORD_RESET_FIX.md` | critical | not_workflow | embedded_hint | present | prod, test | database, infrastructure, configuration, queue_stream, runtime_shell |
| `NEXT_SESSION_PROMPT.md` | critical | not_workflow | inferred_suggestion | present | prod, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, ai_agent |
| `backend_prompt.md` | critical | not_workflow | inferred_suggestion | present | prod, test | deployment, database, infrastructure, configuration, queue_stream |
| `dev-prompt.txt` | critical | not_workflow | inferred_suggestion | present | prod, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell, ai_agent |
| `docs/prompts/CLAUDE_CLI_PROMPT_GREEKS_CACHE_IMPLEMENTATION.md` | critical | not_workflow | inferred_suggestion | present | prod, test, dev | deployment, database, broker_order, queue_stream, ai_agent |
| `docs/prompts/CONFIG_SERVICE_GUIDE.md` | critical | not_workflow | inferred_suggestion | present | prod, staging, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `docs/prompts/CONFIG_SERVICE_IMPROVEMENTS.md` | critical | not_workflow | inferred_suggestion | missing | prod, staging | deployment, database, infrastructure, configuration, broker_order |
| `docs/prompts/EXTENDED_CONFIG_SERVICE.md` | critical | not_workflow | inferred_suggestion | present | prod | database, infrastructure, configuration, queue_stream |
| `docs/prompts/MULTI_SERVICE_REFACTOR_BATCH_PROMPT.md` | critical | not_workflow | inferred_suggestion | present | prod, test | deployment, database, configuration, broker_order, queue_stream, ai_agent |
| `docs/prompts/MY_STRATEGIES_SPRINT_PLAN.md` | critical | not_workflow | inferred_suggestion | present | prod, test, dev | deployment, database, infrastructure, broker_order, runtime_shell, ai_agent |
| `docs/prompts/README.md` | critical | not_workflow | inferred_suggestion | present | prod | deployment, database, infrastructure, configuration, broker_order, queue_stream, ai_agent |
| `docs/prompts/alert-service-context.md` | critical | not_workflow | embedded_hint | present | prod, test | deployment, database, infrastructure, configuration, broker_order, queue_stream |
| `docs/prompts/algo-engine-context.md` | critical | not_workflow | embedded_hint | present | prod, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `docs/prompts/api-gateway-context.md` | critical | not_workflow | embedded_hint | present | prod, test | database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `docs/prompts/backend-context.md` | critical | not_workflow | embedded_hint | present | prod, test | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `docs/prompts/billing-service-context-old.md` | critical | not_workflow | embedded_hint | present | prod, test | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `docs/prompts/billing-service-context.md` | critical | not_workflow | embedded_hint | present | prod, test | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `docs/prompts/calendar-service-context.md` | critical | not_workflow | inferred_suggestion | present | prod, test | deployment, database, infrastructure, configuration, broker_order, queue_stream |
| `docs/prompts/comms-service-context.md` | critical | not_workflow | inferred_suggestion | present | prod, staging, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, ai_agent |
| `docs/prompts/config-service-context.md` | critical | not_workflow | embedded_hint | present | prod, staging, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `docs/prompts/data-relay-service-context.md` | critical | not_workflow | embedded_hint | present | prod, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `docs/prompts/fix-verified-issues-prompt.md` | critical | not_workflow | inferred_suggestion | present | prod, test | database, infrastructure, configuration, broker_order, runtime_shell, ai_agent |
| `docs/prompts/market-data-service-context.md` | critical | not_workflow | embedded_hint | present | prod, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell, ai_agent |
| `docs/prompts/marketplace-context.md` | critical | not_workflow | embedded_hint | present | prod, test, dev | database, infrastructure, configuration, broker_order, queue_stream, runtime_shell, ai_agent |
| `docs/prompts/message-service-context.md` | critical | not_workflow | embedded_hint | present | prod, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, ai_agent |
| `docs/prompts/news-service-context.md` | critical | not_workflow | embedded_hint | present | prod, staging, test, dev | database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `docs/prompts/order-service-context.md` | critical | not_workflow | embedded_hint | present | prod, test | database, infrastructure, configuration, broker_order, queue_stream |
| `docs/prompts/payoff-service-context.md` | critical | not_workflow | embedded_hint | present | prod, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `docs/prompts/rating-service-context.md` | critical | not_workflow | inferred_suggestion | present | prod, test | database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `docs/prompts/screener-service-context.md` | critical | not_workflow | embedded_hint | present | prod, staging, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, ai_agent |
| `docs/prompts/signal-service-context.md` | critical | not_workflow | embedded_hint | present | prod, staging, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `docs/prompts/support-service-context.md` | critical | not_workflow | inferred_suggestion | present | prod, test | deployment, database, infrastructure, configuration, queue_stream, ai_agent |
| `docs/prompts/system-overview.md` | critical | not_workflow | embedded_hint | present | prod, staging, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, ai_agent |
| `docs/prompts/ticker-service-context.md` | critical | not_workflow | inferred_suggestion | present | prod, test | database, infrastructure, configuration, broker_order, queue_stream |
| `docs/prompts/token-manager-context.md` | critical | not_workflow | embedded_hint | present | prod, test | database, infrastructure, configuration, broker_order, queue_stream |
| `docs/prompts/user-service-context.md` | critical | not_workflow | embedded_hint | present | prod, test, dev | database, infrastructure, configuration, broker_order, queue_stream |
| `docs/prompts/ws-gateway-service-context.md` | critical | not_workflow | embedded_hint | present | prod, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `docs/qa/prompts/aef_next_tracks/AEF_306_STRATEGY_SDK_CHANNEL_EXECUTION_HANDOFF_PROMPT.md` | critical | not_workflow | inferred_suggestion | present | prod, staging | database, configuration, broker_order, queue_stream, ai_agent |
| `docs/qa/prompts/aef_next_tracks/AEF_DEFERRED_PRODUCTION_RESILIENCE_READINESS_PROMPT.md` | critical | not_workflow | inferred_suggestion | present | prod, staging, test | deployment, database, broker_order, queue_stream, ai_agent |
| `docs/qa/prompts/aef_next_tracks/AEF_ORCHESTRATOR_PROMPT.md` | critical | not_workflow | inferred_suggestion | present | prod, staging | database, configuration, broker_order, queue_stream, ai_agent |
| `docs/qa/prompts/aef_next_tracks/AEF_PARALLEL_ENTERPRISE_ARCHITECTURE_REVIEW_PROMPT.md` | critical | not_workflow | embedded_hint | present | prod | database, broker_order, queue_stream, ai_agent |
| `docs/qa/prompts/aef_next_tracks/README.md` | critical | not_workflow | inferred_suggestion | present | prod | broker_order, ai_agent |
| `infra-prompt.txt` | critical | not_workflow | inferred_suggestion | present | prod, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell, ai_agent |
| `scripts/apply_algo_engine_sql_migrations.sh` | critical | not_workflow | inferred_suggestion | missing | prod, dev | database |
| `scripts/apply_instrument_registry_migrations.sh` | critical | not_workflow | inferred_suggestion | missing | prod, dev | database |
| `scripts/apply_payoff_live_mode_config.sh` | critical | not_workflow | inferred_suggestion | present | prod, staging, test, dev | database, configuration |
| `scripts/apply_service_sql_migrations.sh` | critical | not_workflow | inferred_suggestion | present | prod, dev | database, broker_order |
| `scripts/backfill_today_via_ticker_service.py` | critical | not_workflow | inferred_suggestion | missing | prod, dev | database, broker_order |
| `scripts/backup/backup-service.py` | critical | not_workflow | declared_owner_map | missing | prod | database, infrastructure, configuration, queue_stream |
| `scripts/bootstrap-dev-api-gateway-prereqs.py` | critical | not_workflow | inferred_suggestion | present | prod, staging, test, dev | database, configuration, broker_order |
| `scripts/bootstrap-dev-owner-service-prereqs.py` | critical | not_workflow | embedded_hint | present | prod, staging, test, dev | database, infrastructure, configuration, broker_order, queue_stream |
| `scripts/bootstrap_broker_rate_limit_profiles.py` | critical | not_workflow | embedded_hint | present | prod, staging, test, dev | configuration, broker_order |
| `scripts/bootstrap_nonprod_config_from_prod.py` | critical | not_workflow | inferred_suggestion | present | prod, staging, test, dev | database, configuration, broker_order, queue_stream |
| `scripts/code-quality-scan.sh` | critical | not_workflow | inferred_suggestion | present | prod, test, dev | database, infrastructure, configuration, queue_stream |
| `scripts/config.sh` | critical | not_workflow | inferred_suggestion | missing | prod, dev | deployment, configuration |
| `scripts/copy_market_data.py` | critical | not_workflow | inferred_suggestion | missing | prod, staging, dev | database, broker_order |
| `scripts/copy_market_data.sh` | critical | not_workflow | inferred_suggestion | missing | prod, dev | database, configuration, broker_order |
| `scripts/data-migration.py` | critical | not_workflow | inferred_suggestion | missing | prod, staging, dev | database, configuration, broker_order, queue_stream |
| `scripts/deploy-phase1.sh` | critical | not_workflow | inferred_suggestion | present | prod, staging, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `scripts/deploy-staging.sh` | critical | not_workflow | embedded_hint | present | prod, staging, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream |
| `scripts/deploy.sh` | critical | not_workflow | inferred_suggestion | present | prod, test, dev | deployment, database, infrastructure, configuration, queue_stream |
| `scripts/deployment-gate.sh` | critical | not_workflow | inferred_suggestion | present | prod, staging, test, dev | deployment, infrastructure, configuration, broker_order |
| `scripts/detect_migration_regressions.sh` | critical | not_workflow | inferred_suggestion | present | prod, test, dev | database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `scripts/fetch_today_options_data.py` | critical | not_workflow | inferred_suggestion | missing | prod | database, configuration, broker_order |
| `scripts/fix_config_service_encryption.sh` | critical | not_workflow | inferred_suggestion | missing | prod | database, infrastructure, configuration, runtime_shell |
| `scripts/fix_timezone_data.py` | critical | not_workflow | embedded_hint | missing | prod, staging, dev | database, configuration, broker_order |
| `scripts/fix_timezone_data_all_tables.py` | critical | not_workflow | inferred_suggestion | missing | prod | database, configuration, broker_order |
| `scripts/governance/apply_prod_schema_to_envs.sh` | critical | not_workflow | declared_owner_map | missing | prod, dev | database |
| `scripts/governance/backfill_news_impacts_recent.sh` | critical | not_workflow | declared_owner_map | missing | prod, dev | database, infrastructure, configuration, broker_order, runtime_shell |
| `scripts/governance/bootstrap_algo_engine_sdk_contracts_config.py` | critical | not_workflow | declared_owner_map | present | prod, staging, test, dev | database, configuration |
| `scripts/governance/bootstrap_env_roles_and_grants.sh` | critical | not_workflow | declared_owner_map | missing | prod | database |
| `scripts/governance/bootstrap_instrument_universe_config.py` | critical | not_workflow | declared_owner_map | present | prod, staging, test, dev | database, configuration |
| `scripts/governance/bootstrap_internal_order_route_signing.py` | critical | not_workflow | declared_owner_map | missing | prod | database, configuration, broker_order |
| `scripts/governance/bootstrap_internal_service_identity_config.py` | critical | not_workflow | declared_owner_map | missing | prod | database, configuration |
| `scripts/governance/bootstrap_model_inference_config.py` | critical | not_workflow | declared_owner_map | present | prod, staging, test, dev | database, configuration |
| `scripts/governance/bootstrap_model_inference_config.sh` | critical | not_workflow | declared_owner_map | present | prod, staging, test | configuration |
| `scripts/governance/bootstrap_order_service_trading_safety_config.py` | critical | not_workflow | declared_owner_map | missing | prod | database, configuration, broker_order |
| `scripts/governance/bootstrap_support_service_config.py` | critical | not_workflow | declared_owner_map | present | prod, staging, test, dev | database, configuration |
| `scripts/governance/check_config_parameter_seeds.py` | critical | not_workflow | declared_owner_map | missing | prod, staging, dev | database, configuration |
| `scripts/governance/check_runtime_public_schema_usage.py` | critical | not_workflow | declared_owner_map | present | prod, test | database, infrastructure |
| `scripts/governance/generate_trading_safety_dashboard_snapshot.py` | critical | not_workflow | declared_owner_map | present | prod | database, configuration, broker_order |
| `scripts/governance/mirror_prod_images_to_lower_envs.sh` | critical | not_workflow | declared_owner_map | present | prod, staging, test, dev | deployment, infrastructure, configuration, broker_order |
| `scripts/governance/run_backend_promotion_contract_preflight.sh` | critical | not_workflow | declared_owner_map | present | prod, staging, dev | deployment, database, configuration |
| `scripts/governance/run_channel_services_pilot_beta.py` | critical | not_workflow | declared_owner_map | present | prod, staging, test | database, infrastructure, configuration, runtime_shell |
