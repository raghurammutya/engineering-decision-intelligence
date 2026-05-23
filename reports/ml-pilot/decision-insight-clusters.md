# Decision Insight Clusters

Generated: `2026-05-23T04:03:11+00:00`

Findings grouped: `487`
Decision clusters: `30`
Likely scanner tuning candidates: `135`
Likely operational blockers: `261`

## Top Decision Clusters

| Rank | Cluster | Findings | Risk Reduction Score | Scanner Tuning | Operational Blockers | Top Action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `config_secret_scripts::block-or-certify-critical-operational-mutation` | 94 | 18375 | 5 | 89 | block or require controlled owner review before use |
| 2 | `db_migration_scripts::block-or-certify-critical-operational-mutation` | 17 | 3550 | 0 | 17 | block or require controlled owner review before use |
| 3 | `config_secret_scripts::assign-accountable-owner-boundary` | 49 | 3357 | 17 | 32 | map to canonical automation or document exception |
| 4 | `config_secret_scripts::canonicalize-or-document-exception` | 85 | 1899 | 71 | 14 | map to canonical automation or document exception |
| 5 | `governance_probes::review-before-autonomy-expansion` | 62 | 1684 | 0 | 0 | map to canonical automation or document exception |
| 6 | `db_migration_scripts::assign-accountable-owner-boundary` | 17 | 1347 | 1 | 16 | map to canonical automation or document exception |
| 7 | `config_secret_scripts::attach-safety-and-rollback-evidence` | 26 | 1022 | 16 | 10 | map to canonical automation or document exception |
| 8 | `deploy_workflows::block-or-certify-critical-operational-mutation` | 5 | 1010 | 0 | 5 | block or require controlled owner review before use |
| 9 | `config_secret_scripts::review-before-autonomy-expansion` | 20 | 782 | 1 | 15 | retain controlled execution with evidence |
| 10 | `db_migration_scripts::review-before-autonomy-expansion` | 18 | 636 | 0 | 9 | map to canonical automation or document exception |
| 11 | `governance_probes::block-or-certify-critical-operational-mutation` | 3 | 585 | 0 | 3 | block or require controlled owner review before use |
| 12 | `other_scripts::review-before-autonomy-expansion` | 12 | 489 | 0 | 12 | assign owner boundary |
| 13 | `db_migration_scripts::attach-safety-and-rollback-evidence` | 8 | 482 | 2 | 6 | map to canonical automation or document exception |
| 14 | `other_scripts::assign-accountable-owner-boundary` | 5 | 425 | 0 | 5 | map to canonical automation or document exception |
| 15 | `db_migration_scripts::canonicalize-or-document-exception` | 16 | 383 | 11 | 5 | map to canonical automation or document exception |
| 16 | `broker_order_scripts::assign-accountable-owner-boundary` | 4 | 375 | 0 | 4 | map to canonical automation or document exception |
| 17 | `governance_probes::canonicalize-or-document-exception` | 7 | 354 | 0 | 5 | map to canonical automation or document exception |
| 18 | `broker_order_scripts::review-before-autonomy-expansion` | 8 | 292 | 0 | 4 | retain controlled execution with evidence |
| 19 | `broker_order_scripts::canonicalize-or-document-exception` | 6 | 285 | 2 | 4 | map to canonical automation or document exception |
| 20 | `other_scripts::block-or-certify-critical-operational-mutation` | 1 | 225 | 0 | 1 | block or require controlled owner review before use |

## Scanner Tuning Candidates

| Path | Risk | Family | Reason | Suggested Action |
| --- | --- | --- | --- | --- |
| `scripts/qa/reconcile_gateway_routes.py` | critical | config_secret_scripts | QA path with high-risk terms may need review before blocking | review rule, read-only pattern, or accepted exception |
| `scripts/qa/run_blocker_closure_cycle.py` | critical | config_secret_scripts | QA path with high-risk terms may need review before blocking | review rule, read-only pattern, or accepted exception |
| `scripts/qa/run_guardrail_suite.py` | critical | config_secret_scripts | QA path with high-risk terms may need review before blocking | review rule, read-only pattern, or accepted exception |
| `scripts/qa/run_python_sdk_negative_path_certification.py` | critical | config_secret_scripts | QA path with high-risk terms may need review before blocking | review rule, read-only pattern, or accepted exception |
| `scripts/qa/run_reference_strategy_sdk_suite.py` | critical | config_secret_scripts | QA path with high-risk terms may need review before blocking | review rule, read-only pattern, or accepted exception |
| `.github/workflows/deploy-dev.yml` | high | deploy_workflows | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `.github/workflows/deploy-frontend-staging.yml` | high | deploy_workflows | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `.github/workflows/load-tests.yml` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `.github/workflows/phase1-tests.yml` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/acl_comprehensive_test.py` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/apply_config_service_alias_policy.py` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/autonomous-debug.sh` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/database_fixes/find_and_update_code.py` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/deploy-dev.sh` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/deploy-frontend.sh` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/enforce_config_hot_reload_guardrail.py` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/enforce_no_env_no_hardcoded_ports.py` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/governance/bootstrap_algo_engine_sdk_contracts_config.sh` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/governance/bootstrap_instrument_universe_config.sh` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/governance/bootstrap_support_service_config.sh` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/governance/check_ci_no_silent_failures.py` | high | db_migration_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/governance/check_communication_runtime_usage.py` | high | db_migration_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/governance/check_config_key_reuse.py` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/governance/check_config_service_runtime_policy.py` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/governance/check_cross_service_boundary_integrity.py` | high | db_migration_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/governance/check_service_url_resolution_policy.py` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/governance/run_acl_guardrail_cycle.sh` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/grant-claude-permissions.sh` | high | db_migration_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/load_test.py` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/monitoring/ha-smoke-tests.py` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/nonprod_reference_sync.sh` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/qa/eth_sma200_paper_strategy.py` | high | broker_order_scripts | QA path with high-risk terms may need review before blocking | review rule, read-only pattern, or accepted exception |
| `scripts/qa/run_acl_account_matrix.py` | high | config_secret_scripts | QA path with high-risk terms may need review before blocking | review rule, read-only pattern, or accepted exception |
| `scripts/qa/run_acl_share_gateway_regression.py` | high | config_secret_scripts | QA path with high-risk terms may need review before blocking | review rule, read-only pattern, or accepted exception |
| `scripts/qa/run_eth_sma200_paper_pipeline_check.py` | high | config_secret_scripts | QA path with high-risk terms may need review before blocking | review rule, read-only pattern, or accepted exception |
| `scripts/qa/run_regression_gate.py` | high | db_migration_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/qa/run_service_taxonomy_parity.py` | high | config_secret_scripts | QA path with high-risk terms may need review before blocking | review rule, read-only pattern, or accepted exception |
| `scripts/qa/run_week1_golden_chain.py` | high | broker_order_scripts | QA path with high-risk terms may need review before blocking | review rule, read-only pattern, or accepted exception |
| `scripts/qa/service_taxonomy_parity/adapters/algo_engine.py` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/qa/service_taxonomy_parity/adapters/order_service.py` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/qa/service_taxonomy_parity/adapters/signal_service.py` | high | qa_readiness_checks | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/qa/service_taxonomy_parity/adapters/ticker_service.py` | high | qa_readiness_checks | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/qa/service_taxonomy_parity/core.py` | high | config_secret_scripts | QA path with high-risk terms may need review before blocking | review rule, read-only pattern, or accepted exception |
| `scripts/qa/tests/test_service_taxonomy_parity_algo_engine.py` | high | db_migration_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/qa/tests/test_service_taxonomy_parity_core.py` | high | db_migration_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/qa/tests/test_service_taxonomy_parity_instrument_registry.py` | high | db_migration_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/qa/tests/test_service_taxonomy_parity_order_service.py` | high | db_migration_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/qa/tests/test_service_taxonomy_parity_signal_service.py` | high | db_migration_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/qa/tests/test_service_taxonomy_parity_ticker_service.py` | high | db_migration_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/run-phase1-tests.sh` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/run_credential_readiness_gate.sh` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/secrets_backup.sh` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/seed_environment_baseline.py` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/start-config-service-for-testing.sh` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/stop-config-service-testing.sh` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `scripts/sync_instrument_registry_from_prod_to_all_nonprod.sh` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `.github/workflows/api-routing-validation.yml` | medium | config_secret_scripts | read-only naming or policy indicates validation/reporting | review rule, read-only pattern, or accepted exception |
| `.github/workflows/credential-readiness-gate.yml` | medium | config_secret_scripts | read-only naming or policy indicates validation/reporting | review rule, read-only pattern, or accepted exception |
| `.github/workflows/governance-readiness-cadence.yml` | medium | config_secret_scripts | read-only naming or policy indicates validation/reporting | review rule, read-only pattern, or accepted exception |
| `.github/workflows/promotion-preflight.yml` | medium | config_secret_scripts | read-only naming or policy indicates validation/reporting | review rule, read-only pattern, or accepted exception |
| `.github/workflows/standards-guard.yml` | medium | config_secret_scripts | read-only naming or policy indicates validation/reporting | review rule, read-only pattern, or accepted exception |
| `scripts/audit-all-services.sh` | medium | config_secret_scripts | read-only naming or policy indicates validation/reporting | review rule, read-only pattern, or accepted exception |
| `scripts/capture_api_baseline.sh` | medium | config_secret_scripts | read-only naming or policy indicates validation/reporting | review rule, read-only pattern, or accepted exception |
| `scripts/check-data-relay-slo.sh` | medium | qa_readiness_checks | read-only naming or policy indicates validation/reporting | review rule, read-only pattern, or accepted exception |
| `scripts/check-hardcoded-secrets.sh` | medium | config_secret_scripts | read-only naming or policy indicates validation/reporting | review rule, read-only pattern, or accepted exception |
| `scripts/check-relay-backpressure.sh` | medium | qa_readiness_checks | read-only naming or policy indicates validation/reporting | review rule, read-only pattern, or accepted exception |
| `scripts/check_all_services.sh` | medium | config_secret_scripts | read-only naming or policy indicates validation/reporting | review rule, read-only pattern, or accepted exception |
| `scripts/check_config_service_duplicates.py` | medium | config_secret_scripts | read-only naming or policy indicates validation/reporting | review rule, read-only pattern, or accepted exception |
| `scripts/generate-fix-priority.sh` | medium | config_secret_scripts | read-only naming or policy indicates validation/reporting | review rule, read-only pattern, or accepted exception |
| `scripts/generate-nginx-config.py` | medium | config_secret_scripts | read-only naming or policy indicates validation/reporting | review rule, read-only pattern, or accepted exception |
| `scripts/generate_docker_compose.py` | medium | config_secret_scripts | read-only naming or policy indicates validation/reporting | review rule, read-only pattern, or accepted exception |
| `scripts/governance/capture_news_ws_trace.py` | medium | db_migration_scripts | read-only naming or policy indicates validation/reporting | review rule, read-only pattern, or accepted exception |
| `scripts/governance/check_env_config_completeness.py` | medium | config_secret_scripts | read-only naming or policy indicates validation/reporting | review rule, read-only pattern, or accepted exception |
| `scripts/governance/check_ticker_runtime_naming.py` | medium | config_secret_scripts | read-only naming or policy indicates validation/reporting | review rule, read-only pattern, or accepted exception |
| `scripts/governance/generate_capital_attribution_observability_snapshot.py` | medium | config_secret_scripts | read-only naming or policy indicates validation/reporting | review rule, read-only pattern, or accepted exception |

## Operational Blockers

| Path | Risk | Autonomy | Family | Next Action |
| --- | --- | --- | --- | --- |
| `scripts/apply_algo_engine_sql_migrations.sh` | critical | blocked | db_migration_scripts | block or require controlled owner review before use |
| `scripts/apply_instrument_registry_migrations.sh` | critical | blocked | db_migration_scripts | block or require controlled owner review before use |
| `scripts/backfill_today_via_ticker_service.py` | critical | blocked | db_migration_scripts | block or require controlled owner review before use |
| `scripts/config.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/copy_market_data.py` | critical | blocked | db_migration_scripts | block or require controlled owner review before use |
| `scripts/copy_market_data.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/data-migration.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/fetch_today_options_data.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/fix_config_service_encryption.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/fix_timezone_data_all_tables.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/migrate_service_configs.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/morning_refresh.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/real-time-data-sync.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/setup-monitoring-service.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/switch-env.sh` | critical | blocked | other_scripts | block or require controlled owner review before use |
| `scripts/sync-registry-from-ports.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/sync_instrument_registry_broker_tokens.sh` | critical | blocked | db_migration_scripts | block or require controlled owner review before use |
| `.github/workflows/backend-production-promotion-diagnose.yml` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `.github/workflows/ci.yml` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `.github/workflows/config-service-production-pipeline.yml` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `.github/workflows/deploy-backend-staging.yml` | critical | blocked | deploy_workflows | block or require controlled owner review before use |
| `.github/workflows/deploy-frontend-production.yml` | critical | blocked | deploy_workflows | block or require controlled owner review before use |
| `.github/workflows/deploy-staging.yml` | critical | blocked | deploy_workflows | block or require controlled owner review before use |
| `.github/workflows/environment-baseline-sync.yml` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/apply_payoff_live_mode_config.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/apply_service_sql_migrations.sh` | critical | blocked | db_migration_scripts | block or require controlled owner review before use |
| `scripts/bootstrap-dev-api-gateway-prereqs.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/bootstrap_nonprod_config_from_prod.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/code-quality-scan.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/deploy-phase1.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/deploy.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/deployment-gate.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/detect_migration_regressions.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/migrate-to-stocksblitz-naming.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/migrate_secrets_to_config_service.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/phase2_data_coverage_validation.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/phase2_performance_baseline.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/phase2_verification_suite.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/post-deployment-health-check.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/production-health-check.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/redeploy_changed_runtime_wave.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/restore-database.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/retired/rename-to-stocksblitz.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/rollback-phase1.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/rotate_encryption_key.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/run_load_tests.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/run_production_promotion.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/secure-deploy.sh` | critical | blocked | db_migration_scripts | block or require controlled owner review before use |
| `scripts/seed-gateway-routes.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/seed-gateway-routes.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/seed-route-registry.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/setup-network-security.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/smoke/verify_gateway_critical_paths.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/standards_audit.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/sync-config-routes-from-ports.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/sync-ports-from-config.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/sync_instrument_registry_instruments.sh` | critical | blocked | db_migration_scripts | block or require controlled owner review before use |
| `scripts/test_mf_pan_consent_flow.sh` | critical | blocked | db_migration_scripts | block or require controlled owner review before use |
| `scripts/test_real_weights.py` | critical | blocked | db_migration_scripts | block or require controlled owner review before use |
| `.github/workflows/port-consistency-check.yml` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/backup/backup-service.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/fix_timezone_data.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/governance/apply_prod_schema_to_envs.sh` | critical | blocked | db_migration_scripts | block or require controlled owner review before use |
| `scripts/governance/backfill_news_impacts_recent.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/governance/bootstrap_env_roles_and_grants.sh` | critical | blocked | db_migration_scripts | block or require controlled owner review before use |
| `scripts/governance/bootstrap_internal_order_route_signing.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/governance/bootstrap_internal_service_identity_config.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/governance/bootstrap_order_service_trading_safety_config.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/governance/check_config_parameter_seeds.py` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/governance/run_mf_portfolio_ingestion_batch.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/governance/run_model_inference_fail_closed_cutover.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `scripts/governance/validate_kubernetes_service_classification.py` | critical | blocked | governance_probes | block or require controlled owner review before use |
| `scripts/governance/validate_no_redundant_code.py` | critical | blocked | db_migration_scripts | block or require controlled owner review before use |
| `scripts/lock-production.sh` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `.github/workflows/deploy-backend-production.yml` | critical | blocked | deploy_workflows | block or require controlled owner review before use |
