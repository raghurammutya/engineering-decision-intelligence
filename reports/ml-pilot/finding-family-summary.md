# Finding Family Summary

Generated: `2026-05-23T02:07:35+00:00`

| Family | Count | Critical | High | Blocked | Representative Next Action |
| --- | --- | --- | --- | --- | --- |
| `broker_order_scripts` | 46 | 6 | 25 | 6 | block or require controlled owner review before use |
| `config_secret_scripts` | 80 | 7 | 36 | 7 | block or require controlled owner review before use |
| `db_migration_scripts` | 244 | 98 | 82 | 98 | block or require controlled owner review before use |
| `deploy_workflows` | 7 | 5 | 2 | 5 | block or require controlled owner review before use |
| `governance_probes` | 73 | 3 | 6 | 3 | block or require controlled owner review before use |
| `other_scripts` | 20 | 1 | 5 | 1 | block or require controlled owner review before use |
| `other_workflows` | 1 | 0 | 1 | 0 | map to canonical automation or document exception |
| `qa_readiness_checks` | 16 | 0 | 2 | 0 | map to canonical automation or document exception |

## Highest-Risk Examples By Family

### `broker_order_scripts`

- `scripts/bootstrap_broker_rate_limit_profiles.py`: critical, blocked
- `scripts/deployment-gate.sh`: critical, blocked
- `scripts/governance/mirror_prod_images_to_lower_envs.sh`: critical, blocked
- `scripts/governance/run_live_entry_exit_basket_probe.sh`: critical, blocked
- `scripts/qa/run_reference_strategy_sdk_suite.py`: critical, blocked
- `scripts/redeploy_changed_runtime_wave.sh`: critical, blocked
- `scripts/bootstrap_env_files.sh`: high, controlled_execute
- `scripts/final_health_check.sh`: high, prepare
- `scripts/governance/check_capability_drift.py`: high, prepare
- `scripts/governance/collect_runtime_probe_actual_vs_expected.py`: high, prepare

### `config_secret_scripts`

- `.github/workflows/ci.yml`: critical, blocked
- `.github/workflows/environment-baseline-sync.yml`: critical, blocked
- `scripts/config.sh`: critical, blocked
- `scripts/governance/bootstrap_model_inference_config.sh`: critical, blocked
- `scripts/governance/validate_config_service_control_plane_contract.py`: critical, blocked
- `scripts/smoke/verify_gateway_critical_paths.sh`: critical, blocked
- `scripts/standards_audit.py`: critical, blocked
- `.github/workflows/promote-environments.yml`: high, controlled_execute
- `scripts/autonomous-debug.sh`: high, prepare
- `scripts/cache_warmup.py`: high, prepare

### `db_migration_scripts`

- `.github/workflows/backend-production-promotion-diagnose.yml`: critical, blocked
- `.github/workflows/config-service-production-pipeline.yml`: critical, blocked
- `.github/workflows/integration-tests.yml`: critical, blocked
- `.github/workflows/port-consistency-check.yml`: critical, blocked
- `scripts/apply_algo_engine_sql_migrations.sh`: critical, blocked
- `scripts/apply_instrument_registry_migrations.sh`: critical, blocked
- `scripts/apply_payoff_live_mode_config.sh`: critical, blocked
- `scripts/apply_service_sql_migrations.sh`: critical, blocked
- `scripts/backfill_today_via_ticker_service.py`: critical, blocked
- `scripts/backup/backup-service.py`: critical, blocked

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
