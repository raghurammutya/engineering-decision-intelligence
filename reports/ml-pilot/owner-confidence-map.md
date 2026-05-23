# Owner Confidence Map

Generated: `2026-05-23T04:44:14+00:00`

Owner workflow records: `567`

## Assignment Types

- `declared_owner_map`: 250
- `inferred_suggestion`: 244
- `embedded_hint`: 53
- `missing_owner`: 20

## Review Classes

- `inferred-owner-review`: 244
- `owner-confirmation`: 134
- `owner-approved-risk-review`: 116
- `owner-map-normalization`: 53
- `missing-owner-assignment`: 20

## Lowest-Confidence Owner Decisions

| Confidence | Review Class | Owner | Boundary | Path | Risk | Action |
| --- | --- | --- | --- | --- | --- | --- |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/switch-env.sh` | critical | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/ingest_mf_disclosure_file.sh` | high | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/retired/compare_v1_v2.sh` | high | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/retired/deploy_v2.sh` | high | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/retired/rollback_to_v1.sh` | high | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/service_health_summary.sh` | high | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/gh_repo.sh` | medium | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/setup_acl_test_env.sh` | medium | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/__init__.py` | low | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/apply_sim_fixes.py` | low | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/audit_scan_synthetic_mock_fallback.py` | low | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/continuous_demo_traffic.sh` | low | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/enforce_instrument_key_contract.py` | low | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/generate_test_traffic.sh` | low | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/health_check_v2.sh` | low | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/internal_api_key_audit.py` | low | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/monitor-production.sh` | low | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/perf/run_baseline_profiles.sh` | low | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/prove_health_compliance.sh` | low | assign accountable owner boundary |
| 0.0 | missing-owner-assignment | unassigned | missing owner boundary | `scripts/verify-service-cleanup.sh` | low | assign accountable owner boundary |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `.github/workflows/deploy-backend-production.yml` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `.github/workflows/deploy-production.yml` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `.github/workflows/integration-tests.yml` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `.github/workflows/port-consistency-check.yml` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `BACKEND_TEAM_PROMPT_ACCOUNT_SELECTOR.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `BACKEND_TEAM_PROMPT_BROKER_ACCOUNTS.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `BACKEND_TEAM_PROMPT_PASSWORD_RESET_FIX.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/alert-service-context.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/algo-engine-context.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/api-gateway-context.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/backend-context.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/billing-service-context-old.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/billing-service-context.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/config-service-context.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/data-relay-service-context.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/market-data-service-context.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/marketplace-context.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/message-service-context.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/news-service-context.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/order-service-context.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/payoff-service-context.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/screener-service-context.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/signal-service-context.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/system-overview.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/token-manager-context.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/user-service-context.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/ws-gateway-service-context.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/qa/prompts/aef_next_tracks/AEF_PARALLEL_ENTERPRISE_ARCHITECTURE_REVIEW_PROMPT.md` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/bootstrap-dev-owner-service-prereqs.py` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/bootstrap_broker_rate_limit_profiles.py` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/deploy-staging.sh` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/fix_timezone_data.py` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/lock-production.sh` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/production_checklist.py` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/run_phase2_tests.sh` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/setup-deployment-env.sh` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/test_acl_database.py` | critical | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `.github/workflows/load-tests.yml` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `.github/workflows/streaming-tracker-watch.yml` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `BACKEND_TEAM_PROMPT_LOGIN_AFTER_SIGNUP.md` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/API_GATEWAY_TESTING_CONTINUATION.md` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/prompts/FRONTEND_API_GATEWAY_MIGRATION.md` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/qa/prompts/aef_next_tracks/AEF_DEFERRED_RATE_POLICY_RUNTIME_ADMISSION_PROMPT.md` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `docs/qa/prompts/aef_next_tracks/AEF_PARALLEL_MANUAL_TRADING_SHARED_FOUNDATION_REVIEW_PROMPT.md` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `prompts_for_validation.md` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/acl_comprehensive_test.py` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/backup-database.sh` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/bootstrap-dev-entity-acl-prereqs.py` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/bootstrap_environment_databases.sh` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/deploy-dev.sh` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/encrypt_secrets.py` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/validate-environment-drift.sh` | medium | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/verify-doc-manifest.py` | low | convert embedded owner hint into owner-map rule |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `.claude/commands/assess-architecture.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `.claude/commands/assess-infrastructure.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-governance | GitHub workflow governance | `.github/workflows/backend-production-promotion-diagnose.yml` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-governance | GitHub workflow governance | `.github/workflows/ci.yml` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-governance | GitHub workflow governance | `.github/workflows/config-service-production-pipeline.yml` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-governance | GitHub workflow governance | `.github/workflows/deploy-backend-staging.yml` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-governance | GitHub workflow governance | `.github/workflows/deploy-frontend-production.yml` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-governance | GitHub workflow governance | `.github/workflows/deploy-staging.yml` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-governance | GitHub workflow governance | `.github/workflows/environment-baseline-sync.yml` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `BACKEND_FIX_PROMPTS.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `NEXT_SESSION_PROMPT.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `backend_prompt.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `dev-prompt.txt` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `docs/prompts/CLAUDE_CLI_PROMPT_GREEKS_CACHE_IMPLEMENTATION.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `docs/prompts/CONFIG_SERVICE_GUIDE.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `docs/prompts/CONFIG_SERVICE_IMPROVEMENTS.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `docs/prompts/EXTENDED_CONFIG_SERVICE.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `docs/prompts/MULTI_SERVICE_REFACTOR_BATCH_PROMPT.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `docs/prompts/MY_STRATEGIES_SPRINT_PLAN.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `docs/prompts/README.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `docs/prompts/calendar-service-context.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `docs/prompts/comms-service-context.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `docs/prompts/fix-verified-issues-prompt.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `docs/prompts/rating-service-context.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `docs/prompts/support-service-context.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `docs/prompts/ticker-service-context.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `docs/qa/prompts/aef_next_tracks/AEF_306_STRATEGY_SDK_CHANNEL_EXECUTION_HANDOFF_PROMPT.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `docs/qa/prompts/aef_next_tracks/AEF_DEFERRED_PRODUCTION_RESILIENCE_READINESS_PROMPT.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `docs/qa/prompts/aef_next_tracks/AEF_ORCHESTRATOR_PROMPT.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | trading-platform | broker and order safety | `docs/qa/prompts/aef_next_tracks/README.md` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `infra-prompt.txt` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/apply_algo_engine_sql_migrations.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/apply_instrument_registry_migrations.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/apply_payoff_live_mode_config.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/apply_service_sql_migrations.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/backfill_today_via_ticker_service.py` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/bootstrap-dev-api-gateway-prereqs.py` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/bootstrap_nonprod_config_from_prod.py` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/code-quality-scan.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/config.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/copy_market_data.py` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/copy_market_data.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/data-migration.py` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/deploy-phase1.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/deploy.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/deployment-gate.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/detect_migration_regressions.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/fetch_today_options_data.py` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/fix_config_service_encryption.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/fix_timezone_data_all_tables.py` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/migrate-to-stocksblitz-naming.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/migrate_secrets_to_config_service.py` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/migrate_service_configs.py` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/morning_refresh.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/phase2_data_coverage_validation.py` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/phase2_performance_baseline.py` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/phase2_verification_suite.py` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/post-deployment-health-check.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/production-health-check.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/real-time-data-sync.py` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/redeploy_changed_runtime_wave.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/restore-database.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/retired/rename-to-stocksblitz.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/rollback-phase1.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/rotate_encryption_key.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/run_load_tests.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/run_production_promotion.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/secure-deploy.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/seed-gateway-routes.py` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/seed-gateway-routes.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/seed-route-registry.py` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/setup-monitoring-service.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/setup-network-security.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/smoke/verify_gateway_critical_paths.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/standards_audit.py` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/sync-config-routes-from-ports.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/sync-ports-from-config.sh` | critical | owner review required before treating suggestion as approved |
