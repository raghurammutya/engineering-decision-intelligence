# Finding Family Summary

Generated: `2026-05-23T03:54:54+00:00`

| Family | Count | Critical | High | Blocked | Representative Next Action |
| --- | --- | --- | --- | --- | --- |
| `broker_order_scripts` | 19 | 0 | 12 | 0 | assign owner boundary |
| `config_secret_scripts` | 275 | 94 | 93 | 94 | block or require controlled owner review before use |
| `db_migration_scripts` | 76 | 17 | 38 | 17 | block or require controlled owner review before use |
| `deploy_workflows` | 7 | 5 | 2 | 5 | block or require controlled owner review before use |
| `governance_probes` | 73 | 3 | 6 | 3 | block or require controlled owner review before use |
| `other_scripts` | 20 | 1 | 5 | 1 | block or require controlled owner review before use |
| `other_workflows` | 1 | 0 | 1 | 0 | map to canonical automation or document exception |
| `qa_readiness_checks` | 16 | 0 | 2 | 0 | map to canonical automation or document exception |

## Highest-Risk Examples By Family

### `broker_order_scripts`

- `scripts/bootstrap_env_files.sh`: high, controlled_execute
- `scripts/governance/check_capability_drift.py`: high, prepare
- `scripts/governance/collect_runtime_probe_actual_vs_expected.py`: high, prepare
- `scripts/governance/install_market_open_live_certification_cron.sh`: high, prepare
- `scripts/governance/promote_images_by_tag.sh`: high, controlled_execute
- `scripts/governance/run_daily_broker_smoke.sh`: high, controlled_execute
- `scripts/governance/run_release_readiness_gate.sh`: high, prepare
- `scripts/phase3_contract_checks.sh`: high, prepare
- `scripts/qa/eth_sma200_paper_strategy.py`: high, prepare
- `scripts/qa/run_week1_golden_chain.py`: high, prepare

### `config_secret_scripts`

- `.github/workflows/backend-production-promotion-diagnose.yml`: critical, blocked
- `.github/workflows/ci.yml`: critical, blocked
- `.github/workflows/config-service-production-pipeline.yml`: critical, blocked
- `.github/workflows/environment-baseline-sync.yml`: critical, blocked
- `.github/workflows/integration-tests.yml`: critical, blocked
- `.github/workflows/port-consistency-check.yml`: critical, blocked
- `scripts/apply_payoff_live_mode_config.sh`: critical, blocked
- `scripts/backup/backup-service.py`: critical, blocked
- `scripts/bootstrap-dev-api-gateway-prereqs.py`: critical, blocked
- `scripts/bootstrap-dev-owner-service-prereqs.py`: critical, blocked

### `db_migration_scripts`

- `scripts/apply_algo_engine_sql_migrations.sh`: critical, blocked
- `scripts/apply_instrument_registry_migrations.sh`: critical, blocked
- `scripts/apply_service_sql_migrations.sh`: critical, blocked
- `scripts/backfill_today_via_ticker_service.py`: critical, blocked
- `scripts/copy_market_data.py`: critical, blocked
- `scripts/governance/apply_prod_schema_to_envs.sh`: critical, blocked
- `scripts/governance/bootstrap_env_roles_and_grants.sh`: critical, blocked
- `scripts/governance/check_runtime_public_schema_usage.py`: critical, blocked
- `scripts/governance/run_order_projection_resiliency_drill.py`: critical, blocked
- `scripts/governance/validate_no_redundant_code.py`: critical, blocked

### `deploy_workflows`

- `.github/workflows/deploy-backend-production.yml`: critical, blocked
- `.github/workflows/deploy-backend-staging.yml`: critical, blocked
- `.github/workflows/deploy-frontend-production.yml`: critical, blocked
- `.github/workflows/deploy-production.yml`: critical, blocked
- `.github/workflows/deploy-staging.yml`: critical, blocked
- `.github/workflows/deploy-dev.yml`: high, prepare
- `.github/workflows/deploy-frontend-staging.yml`: high, prepare

### `governance_probes`

- `scripts/governance/run_gateway_relay_guardrail_cycle.sh`: critical, blocked
- `scripts/governance/run_governance_bootstrap_checks.py`: critical, blocked
- `scripts/governance/validate_kubernetes_service_classification.py`: critical, blocked
- `scripts/governance/run_fo_snapshot_hydrator_health_report.py`: high, prepare
- `scripts/governance/run_option_query_live_session.py`: high, prepare
- `scripts/governance/run_signal_active_candle_audit.py`: high, prepare
- `scripts/governance/run_signal_service_indicator_viability_slice.py`: high, prepare
- `scripts/governance/run_signal_service_universal_viability_slice.py`: high, prepare
- `scripts/governance/run_support_delegation_smoke.sh`: high, prepare
- `scripts/governance/check_runtime_hardcoding_hygiene.py`: medium, recommend

### `other_scripts`

- `scripts/switch-env.sh`: critical, blocked
- `scripts/ingest_mf_disclosure_file.sh`: high, prepare
- `scripts/retired/compare_v1_v2.sh`: high, prepare
- `scripts/retired/deploy_v2.sh`: high, prepare
- `scripts/retired/rollback_to_v1.sh`: high, prepare
- `scripts/service_health_summary.sh`: high, prepare
- `scripts/gh_repo.sh`: medium, recommend
- `scripts/setup_acl_test_env.sh`: medium, recommend
- `scripts/__init__.py`: low, observe
- `scripts/apply_sim_fixes.py`: low, observe

### `other_workflows`

- `.github/workflows/environment-code-parity.yml`: high, prepare

### `qa_readiness_checks`

- `scripts/qa/service_taxonomy_parity/adapters/signal_service.py`: high, prepare
- `scripts/qa/service_taxonomy_parity/adapters/ticker_service.py`: high, prepare
- `scripts/check-data-relay-slo.sh`: medium, recommend
- `scripts/check-relay-backpressure.sh`: medium, recommend
- `scripts/qa/run_regression_gate.sh`: medium, recommend
- `scripts/validate-deployment.sh`: medium, recommend
- `scripts/qa/binance_screener_payoff_e2e.py`: low, observe
- `scripts/qa/check_signal_personal_ownership_acl.py`: low, observe
- `scripts/qa/market_surface_observer_strategy.py`: low, observe
- `scripts/qa/run_python_sdk_construct_certification.py`: low, observe
