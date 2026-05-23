# Remediation Playbook Map

Generated: `2026-05-23T03:54:54+00:00`

| Path | Risk | Family | Playbook | Next Action |
| --- | --- | --- | --- | --- |
| `.github/workflows/backend-production-promotion-diagnose.yml` | critical | config_secret_scripts | `docs/playbooks/direct-prod-deploy-workflow.md` | block or require controlled owner review before use |
| `.github/workflows/ci.yml` | critical | config_secret_scripts | `docs/playbooks/direct-prod-deploy-workflow.md` | block or require controlled owner review before use |
| `.github/workflows/config-service-production-pipeline.yml` | critical | config_secret_scripts | `docs/playbooks/direct-prod-deploy-workflow.md` | block or require controlled owner review before use |
| `.github/workflows/deploy-backend-production.yml` | critical | deploy_workflows | `docs/playbooks/direct-prod-deploy-workflow.md` | block or require controlled owner review before use |
| `.github/workflows/deploy-backend-staging.yml` | critical | deploy_workflows | `docs/playbooks/direct-prod-deploy-workflow.md` | block or require controlled owner review before use |
| `.github/workflows/deploy-frontend-production.yml` | critical | deploy_workflows | `docs/playbooks/direct-prod-deploy-workflow.md` | block or require controlled owner review before use |
| `.github/workflows/deploy-production.yml` | critical | deploy_workflows | `docs/playbooks/direct-prod-deploy-workflow.md` | block or require controlled owner review before use |
| `.github/workflows/deploy-staging.yml` | critical | deploy_workflows | `docs/playbooks/direct-prod-deploy-workflow.md` | block or require controlled owner review before use |
| `.github/workflows/environment-baseline-sync.yml` | critical | config_secret_scripts | `docs/playbooks/direct-prod-deploy-workflow.md` | block or require controlled owner review before use |
| `.github/workflows/integration-tests.yml` | critical | config_secret_scripts | `docs/playbooks/direct-prod-deploy-workflow.md` | block or require controlled owner review before use |
| `.github/workflows/port-consistency-check.yml` | critical | config_secret_scripts | `docs/playbooks/direct-prod-deploy-workflow.md` | block or require controlled owner review before use |
| `scripts/apply_algo_engine_sql_migrations.sh` | critical | db_migration_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/apply_instrument_registry_migrations.sh` | critical | db_migration_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/apply_payoff_live_mode_config.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/apply_service_sql_migrations.sh` | critical | db_migration_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/backfill_today_via_ticker_service.py` | critical | db_migration_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/backup/backup-service.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/bootstrap-dev-api-gateway-prereqs.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/bootstrap-dev-owner-service-prereqs.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/bootstrap_broker_rate_limit_profiles.py` | critical | config_secret_scripts | owner review | block or require controlled owner review before use |
| `scripts/bootstrap_nonprod_config_from_prod.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/code-quality-scan.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/config.sh` | critical | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | block or require controlled owner review before use |
| `scripts/copy_market_data.py` | critical | db_migration_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/copy_market_data.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/data-migration.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/deploy-phase1.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/deploy-staging.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/deploy.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/deployment-gate.sh` | critical | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | block or require controlled owner review before use |
| `scripts/detect_migration_regressions.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/fetch_today_options_data.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/fix_config_service_encryption.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/fix_timezone_data.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/fix_timezone_data_all_tables.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/apply_prod_schema_to_envs.sh` | critical | db_migration_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/backfill_news_impacts_recent.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/bootstrap_algo_engine_sdk_contracts_config.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/bootstrap_env_roles_and_grants.sh` | critical | db_migration_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/bootstrap_instrument_universe_config.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/bootstrap_internal_order_route_signing.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/bootstrap_internal_service_identity_config.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/bootstrap_model_inference_config.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/bootstrap_model_inference_config.sh` | critical | config_secret_scripts | owner review | block or require controlled owner review before use |
| `scripts/governance/bootstrap_order_service_trading_safety_config.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/bootstrap_support_service_config.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/check_config_parameter_seeds.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/check_runtime_public_schema_usage.py` | critical | db_migration_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/generate_trading_safety_dashboard_snapshot.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/mirror_prod_images_to_lower_envs.sh` | critical | config_secret_scripts | owner review | block or require controlled owner review before use |
| `scripts/governance/run_backend_promotion_contract_preflight.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/run_channel_services_pilot_beta.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/run_cross_service_contra_replay_e2e.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/run_cross_service_contra_replay_paper_e2e.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/run_environment_baseline_sync.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/run_gateway_relay_guardrail_cycle.sh` | critical | governance_probes | owner review | block or require controlled owner review before use |
| `scripts/governance/run_governance_bootstrap_checks.py` | critical | governance_probes | owner review | block or require controlled owner review before use |
| `scripts/governance/run_grouped_metrics_live_pack.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/run_live_entry_exit_basket_probe.sh` | critical | config_secret_scripts | owner review | block or require controlled owner review before use |
| `scripts/governance/run_market_open_live_certification.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/run_mf_portfolio_ingestion_batch.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/run_model_inference_fail_closed_cutover.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/run_order_projection_resiliency_drill.py` | critical | db_migration_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/run_payoff_context_live_pack.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/run_portfolio_context_live_pack.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/run_promotion_preflight.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/run_signal_indicator_matrix_live_pack.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/run_strategy_context_live_pack.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/run_support_delegation_cutover.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/validate_config_service_control_plane_contract.py` | critical | config_secret_scripts | owner review | block or require controlled owner review before use |
| `scripts/governance/validate_kubernetes_service_classification.py` | critical | governance_probes | owner review | block or require controlled owner review before use |
| `scripts/governance/validate_no_redundant_code.py` | critical | db_migration_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/validate_performance_regression.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/validate_strict_sdk_provider_contracts.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/validate_support_resistance_contract.py` | critical | db_migration_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/governance/validate_trading_trust_release_gate.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/lock-production.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/migrate-to-stocksblitz-naming.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/migrate_secrets_to_config_service.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/migrate_service_configs.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/morning_refresh.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/phase2_data_coverage_validation.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/phase2_performance_baseline.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/phase2_verification_suite.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/post-deployment-health-check.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/production-health-check.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/production_checklist.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/qa/reconcile_gateway_routes.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/qa/run_blocker_closure_cycle.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/qa/run_guardrail_suite.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/qa/run_python_sdk_negative_path_certification.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/qa/run_reference_strategy_sdk_suite.py` | critical | config_secret_scripts | owner review | block or require controlled owner review before use |
| `scripts/real-time-data-sync.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/redeploy_changed_runtime_wave.sh` | critical | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | block or require controlled owner review before use |
| `scripts/restore-database.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/retired/rename-to-stocksblitz.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/rollback-phase1.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/rotate_encryption_key.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/run_load_tests.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/run_phase2_tests.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/run_production_promotion.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/secure-deploy.sh` | critical | db_migration_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/security/rotate_token_manager_encryption.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/seed-gateway-routes.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/seed-gateway-routes.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/seed-route-registry.py` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/setup-deployment-env.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/setup-monitoring-service.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/setup-network-security.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/smoke/verify_gateway_critical_paths.sh` | critical | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | block or require controlled owner review before use |
| `scripts/standards_audit.py` | critical | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | block or require controlled owner review before use |
| `scripts/switch-env.sh` | critical | other_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | block or require controlled owner review before use |
| `scripts/sync-config-routes-from-ports.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/sync-ports-from-config.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/sync-registry-from-ports.sh` | critical | config_secret_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/sync_instrument_registry_broker_tokens.sh` | critical | db_migration_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/sync_instrument_registry_instruments.sh` | critical | db_migration_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/test_acl_database.py` | critical | db_migration_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/test_mf_pan_consent_flow.sh` | critical | db_migration_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `scripts/test_real_weights.py` | critical | db_migration_scripts | `docs/playbooks/db-migration-script.md` | block or require controlled owner review before use |
| `.github/workflows/deploy-dev.yml` | high | deploy_workflows | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `.github/workflows/deploy-frontend-staging.yml` | high | deploy_workflows | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `.github/workflows/environment-code-parity.yml` | high | other_workflows | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `.github/workflows/phase1-tests.yml` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `.github/workflows/streaming-tracker-watch.yml` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/apply_config_service_alias_policy.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/apply_marketplace_migrations.sh` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/autonomous-debug.sh` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/backfill_7days_complete.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/backfill_7days_optimized.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/backfill_enhanced_greeks.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/backfill_from_last_till_now.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/backfill_today.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/backfill_today_kite.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/backup-database.sh` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/bootstrap-dev-auth-prereqs.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/bootstrap-dev-entity-acl-prereqs.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/bootstrap_env_files.sh` | high | broker_order_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | assign owner boundary |
| `scripts/bootstrap_environment_databases.sh` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/broker_account_sync.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/broker_account_sync_v2.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/broker_account_sync_v3.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/cache_warmup.py` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/classify_market_cap.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/daily_aggregation.sh` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/database_fixes/find_and_update_code.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/decrypt_mf_xls.sh` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/decrypt_secrets.py` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/deep_code_analyzer.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/deploy-frontend.sh` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/dev_validation/seed_positions_sidecar_positive_fixture.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/encrypt_secrets.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/enforce_config_hot_reload_guardrail.py` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/enforce_no_env_no_hardcoded_ports.py` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/fetch_index_data.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/final_health_check.sh` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/go_live_verify.sh` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/build_guardrail_dashboard.py` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/evaluate_kpi_targets.py` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/import_broker_statement.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/mf_constituent_coverage_diagnostics.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/probe_live_optionability.py` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/report_config_seed_key_families.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/run_backend_migrations.sh` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/run_cross_asset_derivatives_smoke.py` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/run_market_open_assurance.sh` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/run_service_sql_migration_dry_run.sh` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/run_signal_active_candle_audit.py` | high | governance_probes | owner review | map to canonical automation or document exception |
| `scripts/governance/run_statement_reconciliation.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance_checks.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/grant-claude-permissions.sh` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/infra_replay_preflight.py` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/ingest_mf_disclosure_file.sh` | high | other_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/ingest_mf_portfolio_statement_encrypted.sh` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/ingest_mf_portfolio_statement_file.sh` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/install_hooks.sh` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/load_test.py` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/map_service_dependencies.sh` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/marketplace_latency_probe.py` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/midnight_refresh.sh` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/monitor_database_health.sh` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/monitoring/ha-smoke-tests.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/nonprod_reference_sync.sh` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/orchestrate_codex_claude.sh` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/phase3_contract_checks.sh` | high | broker_order_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/postgres-replica-init.sh` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/pre-commit-check.sh` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/qa/eth_sma200_paper_strategy.py` | high | broker_order_scripts | owner review | map to canonical automation or document exception |
| `scripts/qa/run_service_taxonomy_parity.py` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/qa/service_taxonomy_parity/core.py` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/reconcile_mf_soa_vs_broker_holdings.sh` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/register_user_service_mfa_key.py` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/retired/compare_v1_v2.sh` | high | other_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/retired/deploy_v2.sh` | high | other_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/retired/rollback_to_v1.sh` | high | other_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/run-phase1-tests.sh` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/run_auth_orchestration.sh` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/run_credential_readiness_gate.sh` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/run_live_probe.py` | high | broker_order_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/run_maturation_guardrail_cycle.sh` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/secrets_backup.sh` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/secrets_restore.sh` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/seed_environment_baseline.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/service_health_summary.sh` | high | other_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/setup_daily_aggregation.sh` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/staging/bootstrap_user_service_identity.sh` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/start-config-service-for-testing.sh` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/start-trading-services.sh` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/stocksblitz_docker_conformance.sh` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/stocksblitz_memory_guard.sh` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/stocksblitz_memory_report.sh` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/stocksblitz_report_retention.sh` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/stop-config-service-testing.sh` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/store_manual_token.sh` | high | broker_order_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/sync-config-parameters.sh` | high | config_secret_scripts | `docs/playbooks/ownerless-high-risk-automation.md` | map to canonical automation or document exception |
| `scripts/sync_instrument_registry_from_prod_to_all_nonprod.sh` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/system-cleanup.sh` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/update_binance_credentials_prod.sh` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `.github/workflows/credential-readiness-gate.yml` | medium | config_secret_scripts | `docs/playbooks/accepted-exception-renewal.md` | review accepted exception and renewal evidence |
| `.github/workflows/promotion-preflight.yml` | medium | config_secret_scripts | `docs/playbooks/accepted-exception-renewal.md` | review accepted exception and renewal evidence |
| `scripts/generate-nginx-config.py` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/generate_capital_attribution_observability_snapshot.py` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/validate_mutual_fund_enrichment_quality.py` | medium | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/verify_env_schema_parity.sh` | medium | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/qa/run_live_two_execution_non_contra_probe.py` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/validate-environment-drift.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/validate-port-consistency.py` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/validate-service-urls.py` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `.github/workflows/load-tests.yml` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `.github/workflows/promote-environments.yml` | high | config_secret_scripts | owner review | retain controlled execution with evidence |
| `scripts/acl_comprehensive_test.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/deploy-dev.sh` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/envctl.sh` | high | config_secret_scripts | owner review | retain controlled execution with evidence |
| `scripts/governance/backfill_marketplace_support_to_support_service.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/bootstrap_algo_engine_sdk_contracts_config.sh` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/bootstrap_instrument_universe_config.sh` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/bootstrap_support_service_config.sh` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/check_capability_drift.py` | high | broker_order_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/check_ci_no_silent_failures.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/check_communication_runtime_usage.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/check_config_key_reuse.py` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/check_config_service_runtime_policy.py` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/check_cross_service_boundary_integrity.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/check_migration_bootstrap_audit.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/check_service_url_resolution_policy.py` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/collect_runtime_probe_actual_vs_expected.py` | high | broker_order_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/export_signal_service_matrix_baseline.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/install_market_open_live_certification_cron.sh` | high | broker_order_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/promote_by_environment.sh` | high | config_secret_scripts | owner review | retain controlled execution with evidence |
| `scripts/governance/promote_images_by_tag.sh` | high | broker_order_scripts | owner review | retain controlled execution with evidence |
| `scripts/governance/run_acl_guardrail_cycle.sh` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/run_anchored_vwap_runtime_probe.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/run_beta_readiness_gate.sh` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/run_context_runtime_e2e_suite.py` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/run_cross_service_algo_order_refactor_e2e.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/run_daily_broker_smoke.sh` | high | broker_order_scripts | owner review | retain controlled execution with evidence |
| `scripts/governance/run_execution_manual_order_probe.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/run_fo_snapshot_hydrator_health_report.py` | high | governance_probes | owner review | map to canonical automation or document exception |
| `scripts/governance/run_mcx_live_entry_exit_probe.sh` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/run_option_query_live_session.py` | high | governance_probes | owner review | map to canonical automation or document exception |
| `scripts/governance/run_order_service_live_policy_matrix.py` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/run_order_service_refactor_extended_live_suite.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/run_order_service_refactor_live_runtime_suite.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/run_paper_execution_runtime_suite.py` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/run_pivot_points_runtime_probe.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/run_release_readiness_gate.sh` | high | broker_order_scripts | owner review | map to canonical automation or document exception |
| `scripts/governance/run_signal_service_indicator_viability_slice.py` | high | governance_probes | owner review | map to canonical automation or document exception |
| `scripts/governance/run_signal_service_remaining_indicator_viability_slice.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/run_signal_service_universal_viability_slice.py` | high | governance_probes | owner review | map to canonical automation or document exception |
| `scripts/governance/run_signal_service_viability_matrix.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/run_standard_indicator_strategy_probe.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/run_support_delegation_smoke.sh` | high | governance_probes | owner review | map to canonical automation or document exception |
| `scripts/governance/run_volatility_runtime_probe.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/validate_kubernetes_core_service_manifests.py` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/qa/run_acl_account_matrix.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/qa/run_acl_share_gateway_regression.py` | high | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/qa/run_eth_sma200_paper_pipeline_check.py` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/qa/run_regression_gate.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/qa/run_week1_golden_chain.py` | high | broker_order_scripts | owner review | map to canonical automation or document exception |
| `scripts/qa/service_taxonomy_parity/adapters/algo_engine.py` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/qa/service_taxonomy_parity/adapters/order_service.py` | high | config_secret_scripts | owner review | map to canonical automation or document exception |
| `scripts/qa/service_taxonomy_parity/adapters/signal_service.py` | high | qa_readiness_checks | owner review | map to canonical automation or document exception |
| `scripts/qa/service_taxonomy_parity/adapters/ticker_service.py` | high | qa_readiness_checks | owner review | map to canonical automation or document exception |
| `scripts/qa/tests/test_service_taxonomy_parity_algo_engine.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/qa/tests/test_service_taxonomy_parity_core.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/qa/tests/test_service_taxonomy_parity_instrument_registry.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/qa/tests/test_service_taxonomy_parity_order_service.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/qa/tests/test_service_taxonomy_parity_signal_service.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/qa/tests/test_service_taxonomy_parity_ticker_service.py` | high | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `.github/workflows/standards-guard.yml` | medium | config_secret_scripts | `docs/playbooks/accepted-exception-renewal.md` | review accepted exception and renewal evidence |
| `.github/workflows/api-routing-validation.yml` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/capture_api_baseline.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/generate-fix-priority.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/generate_docker_compose.py` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/capture_news_ws_trace.py` | medium | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/qa/run_communication_surface_probe.py` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/qa/run_l5_l8_l9_api_probe.py` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/qa/run_live_portfolio_control_probe.py` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/qa/run_markdown_strategy_probe.py` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/retired/verify-ticker-service-v2-migration.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/validate-api-contracts.py` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/validate-config-standardization.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/validate_binance_env.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | assign owner boundary |
| `scripts/verify-alert-service-migration.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify-api-gateway-migration.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify-backtest-migration.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify-calendar-service-migration.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify-data-relay-service-migration.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify-market-data-service-migration.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify-message-service-migration.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify-migration-complete.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify-news-service-migration.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify-order-service-migration.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify-payoff-service-migration.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify-production-readiness.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify-screener-service-migration.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify-token-manager-migration.sh` | medium | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/audit_database_access.sh` | low | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/check-port-drift.sh` | low | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/check_public_schema_empty.sh` | low | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/compare_schema.py` | low | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/extract_model_schema.py` | low | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/find_cross_service_access.py` | low | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/find_missing_migrations.py` | low | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/generate_signal_service_compute_inventory.py` | low | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/audit_instrument_registry_migration.py` | low | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/check_deprecated_config_keys_usage.py` | low | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/check_public_schema_ddl.py` | low | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/governance/verify_env_db_isolation.sh` | low | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/qa/live_execution_hold_probe_strategy.py` | low | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/qa/live_mcx_futures_control_probe_strategy.py` | low | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/qa/live_non_contra_probe_strategy.py` | low | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/qa/live_portfolio_control_probe_script.py` | low | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/qa/live_short_strangle_control_probe_strategy.py` | low | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/retired/verify-line-count-reduction.sh` | low | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/test_system.py` | low | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/validate_config_service_uniqueness.py` | low | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/validate_redis_publisher_guardrails.py` | low | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify-all-services.sh` | low | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify-comms-service-migration.sh` | low | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify-doc-manifest.py` | low | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify-no-dead-patterns.sh` | low | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify-no-orphaned-files.sh` | low | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify_acl_system.py` | low | config_secret_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
| `scripts/verify_service_sql_migration_checksums.sh` | low | db_migration_scripts | `docs/playbooks/db-migration-script.md` | map to canonical automation or document exception |
