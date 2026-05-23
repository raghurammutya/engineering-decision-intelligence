# Decision Backlog

Generated: `2026-05-23T02:03:32+00:00`

This backlog is generated from scanner findings. It is decision support, not source truth.

| Priority | Path | Risk | Autonomy | Owner | Decision Needed |
| --- | --- | --- | --- | --- | --- |
| P0 | `.github/workflows/backend-production-promotion-diagnose.yml` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `.github/workflows/ci.yml` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `.github/workflows/config-service-production-pipeline.yml` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `.github/workflows/deploy-backend-production.yml` | critical | blocked | present | block or require controlled owner review before use |
| P0 | `.github/workflows/deploy-backend-staging.yml` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `.github/workflows/deploy-frontend-production.yml` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `.github/workflows/deploy-production.yml` | critical | blocked | present | block or require controlled owner review before use |
| P0 | `.github/workflows/deploy-staging.yml` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `.github/workflows/environment-baseline-sync.yml` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `.github/workflows/integration-tests.yml` | critical | blocked | present | block or require controlled owner review before use |
| P0 | `.github/workflows/port-consistency-check.yml` | critical | blocked | present | block or require controlled owner review before use |
| P0 | `scripts/apply_algo_engine_sql_migrations.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/apply_instrument_registry_migrations.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/apply_payoff_live_mode_config.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/apply_service_sql_migrations.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/backfill_today_via_ticker_service.py` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/backup/backup-service.py` | critical | blocked | platform-operations (backup and recovery) | block or require controlled owner review before use |
| P0 | `scripts/bootstrap-dev-api-gateway-prereqs.py` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/bootstrap-dev-owner-service-prereqs.py` | critical | blocked | present | block or require controlled owner review before use |
| P0 | `scripts/bootstrap_broker_rate_limit_profiles.py` | critical | blocked | present | block or require controlled owner review before use |
| P0 | `scripts/bootstrap_nonprod_config_from_prod.py` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/code-quality-scan.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/config.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/copy_market_data.py` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/copy_market_data.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/data-migration.py` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/deploy-phase1.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/deploy-staging.sh` | critical | blocked | present | block or require controlled owner review before use |
| P0 | `scripts/deploy.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/deployment-gate.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/detect_migration_regressions.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/fetch_today_options_data.py` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/fix_config_service_encryption.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/fix_timezone_data.py` | critical | blocked | present | block or require controlled owner review before use |
| P0 | `scripts/fix_timezone_data_all_tables.py` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/governance/apply_prod_schema_to_envs.sh` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/backfill_news_impacts_recent.sh` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/bootstrap_algo_engine_sdk_contracts_config.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/bootstrap_env_roles_and_grants.sh` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/bootstrap_instrument_universe_config.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/bootstrap_internal_order_route_signing.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/bootstrap_internal_service_identity_config.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/bootstrap_model_inference_config.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/bootstrap_model_inference_config.sh` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/bootstrap_order_service_trading_safety_config.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/bootstrap_support_service_config.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/check_config_parameter_seeds.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/check_runtime_public_schema_usage.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/generate_trading_safety_dashboard_snapshot.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/mirror_prod_images_to_lower_envs.sh` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/run_backend_promotion_contract_preflight.sh` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/run_channel_services_pilot_beta.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/run_cross_service_contra_replay_e2e.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/run_cross_service_contra_replay_paper_e2e.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/run_environment_baseline_sync.sh` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/run_gateway_relay_guardrail_cycle.sh` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/run_governance_bootstrap_checks.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/run_grouped_metrics_live_pack.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/run_live_entry_exit_basket_probe.sh` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/run_market_open_live_certification.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/run_mf_portfolio_ingestion_batch.sh` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/run_model_inference_fail_closed_cutover.sh` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/run_order_projection_resiliency_drill.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/run_payoff_context_live_pack.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/run_portfolio_context_live_pack.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/run_promotion_preflight.sh` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/run_signal_indicator_matrix_live_pack.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/run_strategy_context_live_pack.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/run_support_delegation_cutover.sh` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/validate_config_service_control_plane_contract.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/validate_kubernetes_service_classification.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/validate_no_redundant_code.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/validate_performance_regression.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/validate_strict_sdk_provider_contracts.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/validate_support_resistance_contract.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/validate_trading_trust_release_gate.py` | critical | blocked | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/lock-production.sh` | critical | blocked | present | block or require controlled owner review before use |
| P0 | `scripts/migrate-to-stocksblitz-naming.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/migrate_secrets_to_config_service.py` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/migrate_service_configs.py` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/morning_refresh.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/phase2_data_coverage_validation.py` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/phase2_performance_baseline.py` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/phase2_verification_suite.py` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/post-deployment-health-check.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/production-health-check.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/production_checklist.py` | critical | blocked | present | block or require controlled owner review before use |
| P0 | `scripts/qa/reconcile_gateway_routes.py` | critical | blocked | qa-governance (quality evidence) | block or require controlled owner review before use |
| P0 | `scripts/qa/run_blocker_closure_cycle.py` | critical | blocked | qa-governance (quality evidence) | block or require controlled owner review before use |
| P0 | `scripts/qa/run_guardrail_suite.py` | critical | blocked | qa-governance (quality evidence) | block or require controlled owner review before use |
| P0 | `scripts/qa/run_python_sdk_negative_path_certification.py` | critical | blocked | qa-governance (quality evidence) | block or require controlled owner review before use |
| P0 | `scripts/qa/run_reference_strategy_sdk_suite.py` | critical | blocked | qa-governance (quality evidence) | block or require controlled owner review before use |
| P0 | `scripts/real-time-data-sync.py` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/redeploy_changed_runtime_wave.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/restore-database.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/retired/rename-to-stocksblitz.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/rollback-phase1.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/rotate_encryption_key.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/run_load_tests.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/run_phase2_tests.sh` | critical | blocked | present | block or require controlled owner review before use |
| P0 | `scripts/run_production_promotion.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/secure-deploy.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/security/rotate_token_manager_encryption.py` | critical | blocked | security-governance (security operations) | block or require controlled owner review before use |
| P0 | `scripts/seed-gateway-routes.py` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/seed-gateway-routes.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/seed-route-registry.py` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/setup-deployment-env.sh` | critical | blocked | present | block or require controlled owner review before use |
| P0 | `scripts/setup-monitoring-service.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/setup-network-security.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/smoke/verify_gateway_critical_paths.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/standards_audit.py` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/switch-env.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/sync-config-routes-from-ports.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/sync-ports-from-config.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/sync-registry-from-ports.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/sync_instrument_registry_broker_tokens.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/sync_instrument_registry_instruments.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/test_acl_database.py` | critical | blocked | present | block or require controlled owner review before use |
| P0 | `scripts/test_mf_pan_consent_flow.sh` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/test_real_weights.py` | critical | blocked | missing_or_unknown | block or require controlled owner review before use |
| P2 | `.github/workflows/deploy-dev.yml` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `.github/workflows/deploy-frontend-staging.yml` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `.github/workflows/environment-code-parity.yml` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `.github/workflows/phase1-tests.yml` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `.github/workflows/streaming-tracker-watch.yml` | high | prepare | present | map to canonical automation or document exception |
| P2 | `scripts/apply_config_service_alias_policy.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/apply_marketplace_migrations.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/autonomous-debug.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/backfill_7days_complete.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/backfill_7days_optimized.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/backfill_enhanced_greeks.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/backfill_from_last_till_now.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/backfill_today.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/backfill_today_kite.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/backup-database.sh` | high | prepare | present | map to canonical automation or document exception |
| P2 | `scripts/bootstrap-dev-auth-prereqs.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/bootstrap-dev-entity-acl-prereqs.py` | high | prepare | present | map to canonical automation or document exception |
| P2 | `scripts/bootstrap_env_files.sh` | high | controlled_execute | missing_or_unknown | assign owner boundary |
| P2 | `scripts/bootstrap_environment_databases.sh` | high | prepare | present | map to canonical automation or document exception |
| P2 | `scripts/broker_account_sync.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/broker_account_sync_v2.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/broker_account_sync_v3.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/cache_warmup.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/classify_market_cap.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/daily_aggregation.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/database_fixes/find_and_update_code.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/decrypt_mf_xls.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/decrypt_secrets.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/deep_code_analyzer.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/deploy-frontend.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/dev_validation/seed_positions_sidecar_positive_fixture.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/encrypt_secrets.py` | high | prepare | present | map to canonical automation or document exception |
| P2 | `scripts/enforce_config_hot_reload_guardrail.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/enforce_no_env_no_hardcoded_ports.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/fetch_index_data.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/final_health_check.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/go_live_verify.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/governance/build_guardrail_dashboard.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P2 | `scripts/governance/evaluate_kpi_targets.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P2 | `scripts/governance/import_broker_statement.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P2 | `scripts/governance/mf_constituent_coverage_diagnostics.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P2 | `scripts/governance/probe_live_optionability.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P2 | `scripts/governance/report_config_seed_key_families.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P2 | `scripts/governance/run_backend_migrations.sh` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P2 | `scripts/governance/run_cross_asset_derivatives_smoke.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P2 | `scripts/governance/run_market_open_assurance.sh` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P2 | `scripts/governance/run_service_sql_migration_dry_run.sh` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P2 | `scripts/governance/run_signal_active_candle_audit.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P2 | `scripts/governance/run_statement_reconciliation.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P2 | `scripts/governance_checks.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/grant-claude-permissions.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/infra_replay_preflight.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/ingest_mf_disclosure_file.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/ingest_mf_portfolio_statement_encrypted.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/ingest_mf_portfolio_statement_file.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/install_hooks.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/load_test.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/map_service_dependencies.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/marketplace_latency_probe.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/midnight_refresh.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/monitor_database_health.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/monitoring/ha-smoke-tests.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/nonprod_reference_sync.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/orchestrate_codex_claude.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/phase3_contract_checks.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/postgres-replica-init.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/pre-commit-check.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/qa/eth_sma200_paper_strategy.py` | high | prepare | qa-governance (quality evidence) | map to canonical automation or document exception |
| P2 | `scripts/qa/run_service_taxonomy_parity.py` | high | prepare | qa-governance (quality evidence) | map to canonical automation or document exception |
| P2 | `scripts/qa/service_taxonomy_parity/core.py` | high | prepare | qa-governance (quality evidence) | map to canonical automation or document exception |
| P2 | `scripts/reconcile_mf_soa_vs_broker_holdings.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/register_user_service_mfa_key.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/retired/compare_v1_v2.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/retired/deploy_v2.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/retired/rollback_to_v1.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/run-phase1-tests.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/run_auth_orchestration.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/run_credential_readiness_gate.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/run_live_probe.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/run_maturation_guardrail_cycle.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/secrets_backup.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/secrets_restore.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/seed_environment_baseline.py` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/service_health_summary.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/setup_daily_aggregation.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/staging/bootstrap_user_service_identity.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/start-config-service-for-testing.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/start-trading-services.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/stocksblitz_docker_conformance.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/stocksblitz_memory_guard.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/stocksblitz_memory_report.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/stocksblitz_report_retention.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/stop-config-service-testing.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/store_manual_token.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/sync-config-parameters.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/sync_instrument_registry_from_prod_to_all_nonprod.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/system-cleanup.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/update_binance_credentials_prod.sh` | high | prepare | missing_or_unknown | map to canonical automation or document exception |
| P2 | `.github/workflows/credential-readiness-gate.yml` | medium | recommend | missing_or_unknown | review accepted exception and renewal evidence |
| P2 | `.github/workflows/promotion-preflight.yml` | medium | recommend | platform-governance (promotion readiness) | review accepted exception and renewal evidence |
| P2 | `scripts/check-data-relay-slo.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/check-relay-backpressure.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/check_config_service_duplicates.py` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/generate-nginx-config.py` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/gh_repo.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/governance/generate_capital_attribution_observability_snapshot.py` | medium | recommend | platform-governance (governance automation) | map to canonical automation or document exception |
| P2 | `scripts/governance/report_env_code_parity.py` | medium | recommend | platform-governance (governance automation) | map to canonical automation or document exception |
| P2 | `scripts/governance/validate_config_service_cache_failmode_matrix.py` | medium | recommend | platform-governance (governance automation) | map to canonical automation or document exception |
| P2 | `scripts/governance/validate_config_service_snapshot_version_contract.py` | medium | recommend | platform-governance (governance automation) | map to canonical automation or document exception |
| P2 | `scripts/governance/validate_mutual_fund_enrichment_quality.py` | medium | recommend | platform-governance (governance automation) | map to canonical automation or document exception |
| P2 | `scripts/governance/verify_env_schema_parity.sh` | medium | recommend | platform-governance (governance automation) | map to canonical automation or document exception |
| P2 | `scripts/qa/run_live_non_contra_probe.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P2 | `scripts/qa/run_live_two_execution_non_contra_probe.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P2 | `scripts/qa/run_regression_gate.sh` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P2 | `scripts/validate-deployment.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/validate-environment-drift.sh` | medium | recommend | present | map to canonical automation or document exception |
| P2 | `scripts/validate-port-consistency.py` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/validate-service-urls.py` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P2 | `scripts/verify-monitoring-setup.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P3 | `.github/workflows/load-tests.yml` | high | prepare | present | map to canonical automation or document exception |
| P3 | `.github/workflows/promote-environments.yml` | high | controlled_execute | platform-governance (environment promotion) | retain controlled execution with evidence |
| P3 | `scripts/acl_comprehensive_test.py` | high | prepare | present | map to canonical automation or document exception |
| P3 | `scripts/deploy-dev.sh` | high | prepare | present | map to canonical automation or document exception |
| P3 | `scripts/envctl.sh` | high | controlled_execute | platform-governance (environment lifecycle) | retain controlled execution with evidence |
| P3 | `scripts/governance/backfill_marketplace_support_to_support_service.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/bootstrap_algo_engine_sdk_contracts_config.sh` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/bootstrap_instrument_universe_config.sh` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/bootstrap_support_service_config.sh` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/check_capability_drift.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/check_ci_no_silent_failures.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/check_communication_runtime_usage.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/check_config_key_reuse.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/check_config_service_runtime_policy.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/check_cross_service_boundary_integrity.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/check_migration_bootstrap_audit.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/check_service_url_resolution_policy.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/collect_runtime_probe_actual_vs_expected.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/export_signal_service_matrix_baseline.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/install_market_open_live_certification_cron.sh` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/promote_by_environment.sh` | high | controlled_execute | platform-governance (environment promotion) | retain controlled execution with evidence |
| P3 | `scripts/governance/promote_images_by_tag.sh` | high | controlled_execute | platform-governance (governance automation) | retain controlled execution with evidence |
| P3 | `scripts/governance/run_acl_guardrail_cycle.sh` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_anchored_vwap_runtime_probe.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_beta_readiness_gate.sh` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_context_runtime_e2e_suite.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_cross_service_algo_order_refactor_e2e.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_daily_broker_smoke.sh` | high | controlled_execute | platform-governance (governance automation) | retain controlled execution with evidence |
| P3 | `scripts/governance/run_execution_manual_order_probe.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_fo_snapshot_hydrator_health_report.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_mcx_live_entry_exit_probe.sh` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_option_query_live_session.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_order_service_live_policy_matrix.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_order_service_refactor_extended_live_suite.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_order_service_refactor_live_runtime_suite.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_paper_execution_runtime_suite.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_pivot_points_runtime_probe.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_release_readiness_gate.sh` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_signal_service_indicator_viability_slice.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_signal_service_remaining_indicator_viability_slice.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_signal_service_universal_viability_slice.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_signal_service_viability_matrix.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_standard_indicator_strategy_probe.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_support_delegation_smoke.sh` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/run_volatility_runtime_probe.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/governance/validate_kubernetes_core_service_manifests.py` | high | prepare | platform-governance (governance automation) | map to canonical automation or document exception |
| P3 | `scripts/qa/run_acl_account_matrix.py` | high | prepare | qa-governance (quality evidence) | map to canonical automation or document exception |
| P3 | `scripts/qa/run_acl_share_gateway_regression.py` | high | prepare | qa-governance (quality evidence) | map to canonical automation or document exception |
| P3 | `scripts/qa/run_eth_sma200_paper_pipeline_check.py` | high | prepare | qa-governance (quality evidence) | map to canonical automation or document exception |
| P3 | `scripts/qa/run_regression_gate.py` | high | prepare | qa-governance (quality evidence) | map to canonical automation or document exception |
| P3 | `scripts/qa/run_week1_golden_chain.py` | high | prepare | qa-governance (quality evidence) | map to canonical automation or document exception |
| P3 | `scripts/qa/service_taxonomy_parity/adapters/algo_engine.py` | high | prepare | qa-governance (quality evidence) | map to canonical automation or document exception |
| P3 | `scripts/qa/service_taxonomy_parity/adapters/order_service.py` | high | prepare | qa-governance (quality evidence) | map to canonical automation or document exception |
| P3 | `scripts/qa/service_taxonomy_parity/adapters/signal_service.py` | high | prepare | qa-governance (quality evidence) | map to canonical automation or document exception |
| P3 | `scripts/qa/service_taxonomy_parity/adapters/ticker_service.py` | high | prepare | qa-governance (quality evidence) | map to canonical automation or document exception |
| P3 | `scripts/qa/tests/test_service_taxonomy_parity_algo_engine.py` | high | prepare | qa-governance (quality evidence) | map to canonical automation or document exception |
| P3 | `scripts/qa/tests/test_service_taxonomy_parity_core.py` | high | prepare | qa-governance (quality evidence) | map to canonical automation or document exception |
| P3 | `scripts/qa/tests/test_service_taxonomy_parity_instrument_registry.py` | high | prepare | qa-governance (quality evidence) | map to canonical automation or document exception |
| P3 | `scripts/qa/tests/test_service_taxonomy_parity_order_service.py` | high | prepare | qa-governance (quality evidence) | map to canonical automation or document exception |
| P3 | `scripts/qa/tests/test_service_taxonomy_parity_signal_service.py` | high | prepare | qa-governance (quality evidence) | map to canonical automation or document exception |
| P3 | `scripts/qa/tests/test_service_taxonomy_parity_ticker_service.py` | high | prepare | qa-governance (quality evidence) | map to canonical automation or document exception |
| P3 | `.github/workflows/standards-guard.yml` | medium | recommend | architecture-governance (standards enforcement) | review accepted exception and renewal evidence |
| P4 | `.github/workflows/api-routing-validation.yml` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `.github/workflows/governance-readiness-cadence.yml` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/audit-all-services.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/capture_api_baseline.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/check-hardcoded-secrets.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/check_all_services.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/generate-fix-priority.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/generate_docker_compose.py` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/governance/capture_news_ws_trace.py` | medium | recommend | platform-governance (governance automation) | map to canonical automation or document exception |
| P4 | `scripts/governance/check_env_config_completeness.py` | medium | recommend | platform-governance (governance automation) | map to canonical automation or document exception |
| P4 | `scripts/governance/check_runtime_hardcoding_hygiene.py` | medium | recommend | platform-governance (governance automation) | map to canonical automation or document exception |
| P4 | `scripts/governance/check_ticker_runtime_naming.py` | medium | recommend | platform-governance (governance automation) | map to canonical automation or document exception |
| P4 | `scripts/governance/generate_env_ports_files.py` | medium | recommend | platform-governance (governance automation) | map to canonical automation or document exception |
| P4 | `scripts/governance/install_weekly_hardening_reminder_cron.sh` | medium | recommend | platform-governance (governance automation) | map to canonical automation or document exception |
| P4 | `scripts/governance/validate_live_broker_certification.py` | medium | recommend | platform-governance (governance automation) | map to canonical automation or document exception |
| P4 | `scripts/governance/validate_marketplace_artifact_storage.py` | medium | recommend | platform-governance (governance automation) | map to canonical automation or document exception |
| P4 | `scripts/governance/validate_model_inference_contract.py` | medium | recommend | platform-governance (governance automation) | map to canonical automation or document exception |
| P4 | `scripts/governance/validate_model_inference_persistence.py` | medium | recommend | platform-governance (governance automation) | map to canonical automation or document exception |
| P4 | `scripts/governance/validate_mutual_fund_nav_slo.py` | medium | recommend | platform-governance (governance automation) | map to canonical automation or document exception |
| P4 | `scripts/governance/validate_news_path_slo.py` | medium | recommend | platform-governance (governance automation) | map to canonical automation or document exception |
| P4 | `scripts/governance/validate_support_service_contract.py` | medium | recommend | platform-governance (governance automation) | map to canonical automation or document exception |
| P4 | `scripts/qa/run_candle_close_event_probe.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P4 | `scripts/qa/run_communication_surface_probe.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P4 | `scripts/qa/run_dataset_surface_probe.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P4 | `scripts/qa/run_event_window_probe.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P4 | `scripts/qa/run_l5_l8_l9_api_probe.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P4 | `scripts/qa/run_lightweight_runtime_concurrency_probe.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P4 | `scripts/qa/run_live_portfolio_control_probe.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P4 | `scripts/qa/run_live_short_strangle_control_probe.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P4 | `scripts/qa/run_markdown_strategy_probe.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P4 | `scripts/qa/run_market_surface_observer_probe.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P4 | `scripts/qa/run_options_greeks_moneyness_probe.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P4 | `scripts/qa/run_payoff_surface_probe.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P4 | `scripts/qa/run_reference_strategy_sdk_concurrency_probe.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P4 | `scripts/qa/run_sdk_negative_path_probe.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P4 | `scripts/qa/run_signal_service_asset_coverage_probe.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P4 | `scripts/qa/run_trade_data_populated_probe.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P4 | `scripts/qa/run_trade_data_surface_probe.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P4 | `scripts/qa/verify_gateway_route_sync.py` | medium | recommend | qa-governance (quality evidence) | map to canonical automation or document exception |
| P4 | `scripts/retired/verify-ticker-service-v2-migration.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/setup_acl_test_env.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/validate-api-contracts.py` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/validate-api-routing.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/validate-config-standardization.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/validate_binance_env.sh` | medium | recommend | missing_or_unknown | assign owner boundary |
| P4 | `scripts/validate_binance_nonprod_gates.py` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/validate_binance_repo.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/validate_payoff_live_mode_config.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify-alert-service-migration.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify-api-gateway-migration.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify-backtest-migration.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify-calendar-service-migration.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify-data-relay-service-migration.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify-market-data-service-migration.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify-message-service-migration.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify-migration-complete.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify-news-service-migration.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify-order-service-migration.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify-payoff-service-migration.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify-production-readiness.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify-screener-service-migration.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify-token-manager-migration.sh` | medium | recommend | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/__init__.py` | low | observe | missing_or_unknown | assign owner boundary |
| P4 | `scripts/apply_sim_fixes.py` | low | observe | missing_or_unknown | assign owner boundary |
| P4 | `scripts/audit_database_access.sh` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/audit_scan_synthetic_mock_fallback.py` | low | observe | missing_or_unknown | assign owner boundary |
| P4 | `scripts/check-directory-health.sh` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/check-port-drift.sh` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/check_public_schema_empty.sh` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/compare_schema.py` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/continuous_demo_traffic.sh` | low | observe | missing_or_unknown | assign owner boundary |
| P4 | `scripts/enforce_instrument_key_contract.py` | low | observe | missing_or_unknown | assign owner boundary |
| P4 | `scripts/extract_model_schema.py` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/find_cross_service_access.py` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/find_missing_migrations.py` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/generate_signal_service_compute_inventory.py` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/generate_test_traffic.sh` | low | observe | missing_or_unknown | assign owner boundary |
| P4 | `scripts/health_check_v2.sh` | low | observe | missing_or_unknown | assign owner boundary |
| P4 | `scripts/internal_api_key_audit.py` | low | observe | missing_or_unknown | assign owner boundary |
| P4 | `scripts/monitor-production.sh` | low | observe | missing_or_unknown | assign owner boundary |
| P4 | `scripts/perf/run_baseline_profiles.sh` | low | observe | missing_or_unknown | assign owner boundary |
| P4 | `scripts/prove_health_compliance.sh` | low | observe | missing_or_unknown | assign owner boundary |
| P4 | `scripts/retired/verify-line-count-reduction.sh` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/test_endpoints.sh` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/test_envctl_option_contract.sh` | low | observe | missing_or_unknown | assign owner boundary |
| P4 | `scripts/test_system.py` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/validate_breeze_api_surface.py` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/validate_broker_uniformity_contract.sh` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/validate_config_service_uniqueness.py` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/validate_redis_publisher_guardrails.py` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify-all-services.sh` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify-comms-service-migration.sh` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify-no-dead-patterns.sh` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify-no-orphaned-files.sh` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify-service-cleanup.sh` | low | observe | missing_or_unknown | assign owner boundary |
| P4 | `scripts/verify_acl_system.py` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify_architecture_compliance.sh` | low | observe | missing_or_unknown | map to canonical automation or document exception |
| P4 | `scripts/verify_service_sql_migration_checksums.sh` | low | observe | missing_or_unknown | map to canonical automation or document exception |
