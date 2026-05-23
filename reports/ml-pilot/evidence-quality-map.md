# Evidence Quality Map

Generated: `2026-05-23T02:17:10+00:00`

## Quality Counts

- `missing`: 175
- `test_evidence`: 174
- `generated_report`: 72
- `referenced_only`: 43
- `rollback_evidence`: 21
- `promotion_evidence`: 2

## High-Risk Missing Or Weak Evidence

| Path | Risk | Evidence Quality | Next Action |
| --- | --- | --- | --- |
| `scripts/governance/generate_trading_safety_dashboard_snapshot.py` | critical | generated_report | block or require controlled owner review before use |
| `scripts/governance/run_backend_promotion_contract_preflight.sh` | critical | generated_report | block or require controlled owner review before use |
| `scripts/governance/run_cross_service_contra_replay_e2e.py` | critical | generated_report | block or require controlled owner review before use |
| `scripts/governance/run_cross_service_contra_replay_paper_e2e.py` | critical | generated_report | block or require controlled owner review before use |
| `scripts/governance/run_gateway_relay_guardrail_cycle.sh` | critical | generated_report | block or require controlled owner review before use |
| `scripts/governance/run_grouped_metrics_live_pack.py` | critical | generated_report | block or require controlled owner review before use |
| `scripts/governance/run_payoff_context_live_pack.py` | critical | generated_report | block or require controlled owner review before use |
| `scripts/governance/run_portfolio_context_live_pack.py` | critical | generated_report | block or require controlled owner review before use |
| `scripts/governance/run_signal_indicator_matrix_live_pack.py` | critical | generated_report | block or require controlled owner review before use |
| `scripts/governance/run_strategy_context_live_pack.py` | critical | generated_report | block or require controlled owner review before use |
| `scripts/governance/validate_trading_trust_release_gate.py` | critical | generated_report | block or require controlled owner review before use |
| `scripts/qa/reconcile_gateway_routes.py` | critical | generated_report | block or require controlled owner review before use |
| `scripts/qa/run_reference_strategy_sdk_suite.py` | critical | generated_report | block or require controlled owner review before use |
| `scripts/security/rotate_token_manager_encryption.py` | critical | generated_report | block or require controlled owner review before use |
| `.github/workflows/port-consistency-check.yml` | critical | missing | block or require controlled owner review before use |
| `scripts/apply_algo_engine_sql_migrations.sh` | critical | missing | block or require controlled owner review before use |
| `scripts/apply_instrument_registry_migrations.sh` | critical | missing | block or require controlled owner review before use |
| `scripts/backfill_today_via_ticker_service.py` | critical | missing | block or require controlled owner review before use |
| `scripts/backup/backup-service.py` | critical | missing | block or require controlled owner review before use |
| `scripts/config.sh` | critical | missing | block or require controlled owner review before use |
| `scripts/copy_market_data.py` | critical | missing | block or require controlled owner review before use |
| `scripts/copy_market_data.sh` | critical | missing | block or require controlled owner review before use |
| `scripts/data-migration.py` | critical | missing | block or require controlled owner review before use |
| `scripts/fetch_today_options_data.py` | critical | missing | block or require controlled owner review before use |
| `scripts/fix_config_service_encryption.sh` | critical | missing | block or require controlled owner review before use |
| `scripts/fix_timezone_data.py` | critical | missing | block or require controlled owner review before use |
| `scripts/fix_timezone_data_all_tables.py` | critical | missing | block or require controlled owner review before use |
| `scripts/governance/apply_prod_schema_to_envs.sh` | critical | missing | block or require controlled owner review before use |
| `scripts/governance/backfill_news_impacts_recent.sh` | critical | missing | block or require controlled owner review before use |
| `scripts/governance/bootstrap_env_roles_and_grants.sh` | critical | missing | block or require controlled owner review before use |
| `scripts/governance/bootstrap_internal_order_route_signing.py` | critical | missing | block or require controlled owner review before use |
| `scripts/governance/bootstrap_internal_service_identity_config.py` | critical | missing | block or require controlled owner review before use |
| `scripts/governance/bootstrap_order_service_trading_safety_config.py` | critical | missing | block or require controlled owner review before use |
| `scripts/governance/check_config_parameter_seeds.py` | critical | missing | block or require controlled owner review before use |
| `scripts/governance/run_mf_portfolio_ingestion_batch.sh` | critical | missing | block or require controlled owner review before use |
| `scripts/governance/run_model_inference_fail_closed_cutover.sh` | critical | missing | block or require controlled owner review before use |
| `scripts/governance/validate_kubernetes_service_classification.py` | critical | missing | block or require controlled owner review before use |
| `scripts/governance/validate_no_redundant_code.py` | critical | missing | block or require controlled owner review before use |
| `scripts/lock-production.sh` | critical | missing | block or require controlled owner review before use |
| `scripts/migrate_service_configs.py` | critical | missing | block or require controlled owner review before use |
| `scripts/morning_refresh.sh` | critical | missing | block or require controlled owner review before use |
| `scripts/real-time-data-sync.py` | critical | missing | block or require controlled owner review before use |
| `scripts/setup-monitoring-service.sh` | critical | missing | block or require controlled owner review before use |
| `scripts/switch-env.sh` | critical | missing | block or require controlled owner review before use |
| `scripts/sync-registry-from-ports.sh` | critical | missing | block or require controlled owner review before use |
| `scripts/sync_instrument_registry_broker_tokens.sh` | critical | missing | block or require controlled owner review before use |
| `scripts/migrate_secrets_to_config_service.py` | critical | referenced_only | block or require controlled owner review before use |
| `scripts/redeploy_changed_runtime_wave.sh` | critical | referenced_only | block or require controlled owner review before use |
| `scripts/rotate_encryption_key.sh` | critical | referenced_only | block or require controlled owner review before use |
| `scripts/run_production_promotion.sh` | critical | referenced_only | block or require controlled owner review before use |
| `scripts/seed-gateway-routes.py` | critical | referenced_only | block or require controlled owner review before use |
| `scripts/seed-gateway-routes.sh` | critical | referenced_only | block or require controlled owner review before use |
| `scripts/governance/check_capability_drift.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/collect_runtime_probe_actual_vs_expected.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/export_signal_service_matrix_baseline.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/install_market_open_live_certification_cron.sh` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_anchored_vwap_runtime_probe.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_beta_readiness_gate.sh` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_context_runtime_e2e_suite.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_cross_service_algo_order_refactor_e2e.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_daily_broker_smoke.sh` | high | generated_report | retain controlled execution with evidence |
| `scripts/governance/run_fo_snapshot_hydrator_health_report.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_mcx_live_entry_exit_probe.sh` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_option_query_live_session.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_order_service_live_policy_matrix.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_order_service_refactor_extended_live_suite.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_order_service_refactor_live_runtime_suite.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_paper_execution_runtime_suite.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_pivot_points_runtime_probe.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_release_readiness_gate.sh` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_signal_service_indicator_viability_slice.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_signal_service_remaining_indicator_viability_slice.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_signal_service_universal_viability_slice.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_signal_service_viability_matrix.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_standard_indicator_strategy_probe.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_support_delegation_smoke.sh` | high | generated_report | map to canonical automation or document exception |
| `scripts/governance/run_volatility_runtime_probe.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/qa/run_acl_account_matrix.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/qa/run_acl_share_gateway_regression.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/qa/run_eth_sma200_paper_pipeline_check.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/qa/run_week1_golden_chain.py` | high | generated_report | map to canonical automation or document exception |
| `scripts/run_maturation_guardrail_cycle.sh` | high | generated_report | map to canonical automation or document exception |
| `scripts/stocksblitz_docker_conformance.sh` | high | generated_report | map to canonical automation or document exception |
| `scripts/stocksblitz_memory_report.sh` | high | generated_report | map to canonical automation or document exception |
| `scripts/stocksblitz_report_retention.sh` | high | generated_report | map to canonical automation or document exception |
| `.github/workflows/environment-code-parity.yml` | high | missing | map to canonical automation or document exception |
| `.github/workflows/streaming-tracker-watch.yml` | high | missing | map to canonical automation or document exception |
| `scripts/apply_marketplace_migrations.sh` | high | missing | map to canonical automation or document exception |
| `scripts/backfill_7days_complete.py` | high | missing | map to canonical automation or document exception |
| `scripts/backfill_7days_optimized.py` | high | missing | map to canonical automation or document exception |
| `scripts/backfill_enhanced_greeks.py` | high | missing | map to canonical automation or document exception |
| `scripts/backfill_from_last_till_now.py` | high | missing | map to canonical automation or document exception |
| `scripts/backfill_today.py` | high | missing | map to canonical automation or document exception |
| `scripts/backfill_today_kite.py` | high | missing | map to canonical automation or document exception |
| `scripts/backup-database.sh` | high | missing | map to canonical automation or document exception |
| `scripts/bootstrap-dev-auth-prereqs.py` | high | missing | map to canonical automation or document exception |
| `scripts/bootstrap-dev-entity-acl-prereqs.py` | high | missing | map to canonical automation or document exception |
| `scripts/bootstrap_environment_databases.sh` | high | missing | map to canonical automation or document exception |
| `scripts/broker_account_sync.py` | high | missing | map to canonical automation or document exception |
| `scripts/broker_account_sync_v2.py` | high | missing | map to canonical automation or document exception |
| `scripts/broker_account_sync_v3.py` | high | missing | map to canonical automation or document exception |
| `scripts/classify_market_cap.py` | high | missing | map to canonical automation or document exception |
| `scripts/daily_aggregation.sh` | high | missing | map to canonical automation or document exception |
| `scripts/decrypt_mf_xls.sh` | high | missing | map to canonical automation or document exception |
| `scripts/decrypt_secrets.py` | high | missing | map to canonical automation or document exception |
| `scripts/deep_code_analyzer.py` | high | missing | map to canonical automation or document exception |
| `scripts/dev_validation/seed_positions_sidecar_positive_fixture.py` | high | missing | map to canonical automation or document exception |
| `scripts/encrypt_secrets.py` | high | missing | map to canonical automation or document exception |
| `scripts/fetch_index_data.py` | high | missing | map to canonical automation or document exception |
| `scripts/governance/build_guardrail_dashboard.py` | high | missing | map to canonical automation or document exception |
| `scripts/governance/evaluate_kpi_targets.py` | high | missing | map to canonical automation or document exception |
| `scripts/governance/import_broker_statement.py` | high | missing | map to canonical automation or document exception |
| `scripts/governance/mf_constituent_coverage_diagnostics.py` | high | missing | map to canonical automation or document exception |
| `scripts/governance/probe_live_optionability.py` | high | missing | map to canonical automation or document exception |
| `scripts/governance/report_config_seed_key_families.py` | high | missing | map to canonical automation or document exception |
| `scripts/governance/run_backend_migrations.sh` | high | missing | map to canonical automation or document exception |
| `scripts/governance/run_cross_asset_derivatives_smoke.py` | high | missing | map to canonical automation or document exception |
| `scripts/governance/run_market_open_assurance.sh` | high | missing | map to canonical automation or document exception |
| `scripts/governance/run_service_sql_migration_dry_run.sh` | high | missing | map to canonical automation or document exception |
| `scripts/governance/run_signal_active_candle_audit.py` | high | missing | map to canonical automation or document exception |
| `scripts/governance/run_statement_reconciliation.py` | high | missing | map to canonical automation or document exception |
| `scripts/governance_checks.py` | high | missing | map to canonical automation or document exception |
| `scripts/infra_replay_preflight.py` | high | missing | map to canonical automation or document exception |
| `scripts/ingest_mf_disclosure_file.sh` | high | missing | map to canonical automation or document exception |
| `scripts/ingest_mf_portfolio_statement_encrypted.sh` | high | missing | map to canonical automation or document exception |
| `scripts/ingest_mf_portfolio_statement_file.sh` | high | missing | map to canonical automation or document exception |
| `scripts/map_service_dependencies.sh` | high | missing | map to canonical automation or document exception |
| `scripts/marketplace_latency_probe.py` | high | missing | map to canonical automation or document exception |
| `scripts/midnight_refresh.sh` | high | missing | map to canonical automation or document exception |
| `scripts/orchestrate_codex_claude.sh` | high | missing | map to canonical automation or document exception |
| `scripts/phase3_contract_checks.sh` | high | missing | map to canonical automation or document exception |
| `scripts/postgres-replica-init.sh` | high | missing | map to canonical automation or document exception |
| `scripts/pre-commit-check.sh` | high | missing | map to canonical automation or document exception |
| `scripts/qa/eth_sma200_paper_strategy.py` | high | missing | map to canonical automation or document exception |
| `scripts/qa/run_service_taxonomy_parity.py` | high | missing | map to canonical automation or document exception |
| `scripts/qa/service_taxonomy_parity/core.py` | high | missing | map to canonical automation or document exception |
| `scripts/reconcile_mf_soa_vs_broker_holdings.sh` | high | missing | map to canonical automation or document exception |
| `scripts/register_user_service_mfa_key.py` | high | missing | map to canonical automation or document exception |
| `scripts/run_auth_orchestration.sh` | high | missing | map to canonical automation or document exception |
| `scripts/run_live_probe.py` | high | missing | map to canonical automation or document exception |
| `scripts/secrets_restore.sh` | high | missing | map to canonical automation or document exception |
| `scripts/setup_daily_aggregation.sh` | high | missing | map to canonical automation or document exception |
| `scripts/staging/bootstrap_user_service_identity.sh` | high | missing | map to canonical automation or document exception |
| `scripts/stocksblitz_memory_guard.sh` | high | missing | map to canonical automation or document exception |
| `scripts/store_manual_token.sh` | high | missing | map to canonical automation or document exception |
| `scripts/sync-config-parameters.sh` | high | missing | map to canonical automation or document exception |
| `scripts/system-cleanup.sh` | high | missing | map to canonical automation or document exception |
| `scripts/update_binance_credentials_prod.sh` | high | missing | map to canonical automation or document exception |
| `scripts/cache_warmup.py` | high | referenced_only | map to canonical automation or document exception |
| `scripts/final_health_check.sh` | high | referenced_only | map to canonical automation or document exception |
