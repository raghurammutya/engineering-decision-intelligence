# Owner Confidence Map

Generated: `2026-05-23T04:03:11+00:00`

Owner workflow records: `487`

## Assignment Types

- `declared_owner_map`: 250
- `inferred_suggestion`: 194
- `embedded_hint`: 23
- `missing_owner`: 20

## Review Classes

- `inferred-owner-review`: 194
- `owner-confirmation`: 134
- `owner-approved-risk-review`: 116
- `owner-map-normalization`: 23
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
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/acl_comprehensive_test.py` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/backup-database.sh` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/bootstrap-dev-entity-acl-prereqs.py` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/bootstrap_environment_databases.sh` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/deploy-dev.sh` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/encrypt_secrets.py` | high | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/validate-environment-drift.sh` | medium | convert embedded owner hint into owner-map rule |
| 0.45 | owner-map-normalization | embedded_owner_hint | owner text present without policy owner-map entry | `scripts/verify-doc-manifest.py` | low | convert embedded owner hint into owner-map rule |
| 0.65 | inferred-owner-review | platform-governance | GitHub workflow governance | `.github/workflows/backend-production-promotion-diagnose.yml` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-governance | GitHub workflow governance | `.github/workflows/ci.yml` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-governance | GitHub workflow governance | `.github/workflows/config-service-production-pipeline.yml` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-governance | GitHub workflow governance | `.github/workflows/deploy-backend-staging.yml` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-governance | GitHub workflow governance | `.github/workflows/deploy-frontend-production.yml` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-governance | GitHub workflow governance | `.github/workflows/deploy-staging.yml` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-governance | GitHub workflow governance | `.github/workflows/environment-baseline-sync.yml` | critical | owner review required before treating suggestion as approved |
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
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/sync-registry-from-ports.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/sync_instrument_registry_broker_tokens.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/sync_instrument_registry_instruments.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/test_mf_pan_consent_flow.sh` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/test_real_weights.py` | critical | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-governance | GitHub workflow governance | `.github/workflows/deploy-dev.yml` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-governance | GitHub workflow governance | `.github/workflows/deploy-frontend-staging.yml` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-governance | GitHub workflow governance | `.github/workflows/environment-code-parity.yml` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-governance | GitHub workflow governance | `.github/workflows/phase1-tests.yml` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/apply_config_service_alias_policy.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/apply_marketplace_migrations.sh` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/autonomous-debug.sh` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/backfill_7days_complete.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/backfill_7days_optimized.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/backfill_enhanced_greeks.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/backfill_from_last_till_now.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/backfill_today.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/backfill_today_kite.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/bootstrap-dev-auth-prereqs.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | trading-platform | broker and order safety | `scripts/bootstrap_env_files.sh` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/broker_account_sync.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/broker_account_sync_v2.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/broker_account_sync_v3.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/cache_warmup.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/classify_market_cap.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/daily_aggregation.sh` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/database_fixes/find_and_update_code.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/decrypt_mf_xls.sh` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/decrypt_secrets.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/deep_code_analyzer.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/deploy-frontend.sh` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/dev_validation/seed_positions_sidecar_positive_fixture.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/enforce_config_hot_reload_guardrail.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/enforce_no_env_no_hardcoded_ports.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/fetch_index_data.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/final_health_check.sh` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/go_live_verify.sh` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/governance_checks.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/grant-claude-permissions.sh` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/infra_replay_preflight.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/ingest_mf_portfolio_statement_encrypted.sh` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/ingest_mf_portfolio_statement_file.sh` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/install_hooks.sh` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/load_test.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/map_service_dependencies.sh` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/marketplace_latency_probe.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/midnight_refresh.sh` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/monitor_database_health.sh` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/monitoring/ha-smoke-tests.py` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/nonprod_reference_sync.sh` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/orchestrate_codex_claude.sh` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | trading-platform | broker and order safety | `scripts/phase3_contract_checks.sh` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | data-platform | database migration and data mutation | `scripts/postgres-replica-init.sh` | high | owner review required before treating suggestion as approved |
| 0.65 | inferred-owner-review | platform-security | configuration and secret handling | `scripts/pre-commit-check.sh` | high | owner review required before treating suggestion as approved |
