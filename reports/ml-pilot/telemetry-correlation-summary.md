# Telemetry Correlation Summary

Generated: `2026-05-23T03:58:52+00:00`

These correlations currently join inferred runtime signals with CI/CD, owner, and evidence dimensions. Observed telemetry is not ingested yet.

Correlation records: `458`

## Telemetry State

- `inferred_only`: 458

## CI/CD Surface Class

- `deployment_capable`: 18
- `not_workflow`: 435
- `validation_only`: 5

## Owner Assignment Type

- `declared_owner_map`: 225
- `embedded_hint`: 23
- `inferred_suggestion`: 194
- `missing_owner`: 16

## Evidence Status

- `missing`: 156
- `present`: 302

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
| `scripts/governance/run_cross_service_contra_replay_e2e.py` | critical | not_workflow | declared_owner_map | present | prod | database, infrastructure, configuration, broker_order, queue_stream |
| `scripts/governance/run_cross_service_contra_replay_paper_e2e.py` | critical | not_workflow | declared_owner_map | present | prod | database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `scripts/governance/run_environment_baseline_sync.sh` | critical | not_workflow | declared_owner_map | present | prod, staging, test, dev | database, configuration |
| `scripts/governance/run_gateway_relay_guardrail_cycle.sh` | critical | not_workflow | declared_owner_map | present | prod, staging, dev | infrastructure, queue_stream |
| `scripts/governance/run_governance_bootstrap_checks.py` | critical | not_workflow | declared_owner_map | present | prod, staging, test, dev | deployment, infrastructure |
| `scripts/governance/run_grouped_metrics_live_pack.py` | critical | not_workflow | declared_owner_map | present | prod | database, infrastructure, configuration, broker_order |
| `scripts/governance/run_live_entry_exit_basket_probe.sh` | critical | not_workflow | declared_owner_map | present | prod, dev | configuration, broker_order, ai_agent |
| `scripts/governance/run_market_open_live_certification.py` | critical | not_workflow | declared_owner_map | present | prod, staging, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream |
| `scripts/governance/run_mf_portfolio_ingestion_batch.sh` | critical | not_workflow | declared_owner_map | missing | prod | database, infrastructure, configuration, runtime_shell |
| `scripts/governance/run_model_inference_fail_closed_cutover.sh` | critical | not_workflow | declared_owner_map | missing | prod, staging, dev | database, configuration |
| `scripts/governance/run_order_projection_resiliency_drill.py` | critical | not_workflow | declared_owner_map | present | prod, staging, test | database, broker_order, queue_stream |
| `scripts/governance/run_payoff_context_live_pack.py` | critical | not_workflow | declared_owner_map | present | prod | database, infrastructure, configuration |
| `scripts/governance/run_portfolio_context_live_pack.py` | critical | not_workflow | declared_owner_map | present | prod | database, infrastructure, configuration, broker_order |
| `scripts/governance/run_promotion_preflight.sh` | critical | not_workflow | declared_owner_map | present | prod, staging, test, dev | database, infrastructure, configuration, broker_order, queue_stream, runtime_shell, ai_agent |
| `scripts/governance/run_signal_indicator_matrix_live_pack.py` | critical | not_workflow | declared_owner_map | present | prod | database, infrastructure, configuration |
| `scripts/governance/run_strategy_context_live_pack.py` | critical | not_workflow | declared_owner_map | present | prod | database, infrastructure, configuration, broker_order |
| `scripts/governance/run_support_delegation_cutover.sh` | critical | not_workflow | declared_owner_map | present | prod, staging, dev | database, infrastructure, configuration |
| `scripts/governance/validate_config_service_control_plane_contract.py` | critical | not_workflow | declared_owner_map | present | prod, test | configuration |
| `scripts/governance/validate_kubernetes_service_classification.py` | critical | not_workflow | declared_owner_map | missing | prod | deployment |
| `scripts/governance/validate_no_redundant_code.py` | critical | not_workflow | declared_owner_map | missing | prod | database |
| `scripts/governance/validate_performance_regression.py` | critical | not_workflow | declared_owner_map | present | prod, staging, test | database, configuration |
| `scripts/governance/validate_strict_sdk_provider_contracts.py` | critical | not_workflow | declared_owner_map | present | prod, staging, test | database, configuration |
| `scripts/governance/validate_support_resistance_contract.py` | critical | not_workflow | declared_owner_map | present | prod, staging, test | database, infrastructure, runtime_shell |
| `scripts/governance/validate_trading_trust_release_gate.py` | critical | not_workflow | declared_owner_map | present | prod, staging | deployment, database, infrastructure, configuration, broker_order, runtime_shell |
| `scripts/lock-production.sh` | critical | not_workflow | embedded_hint | missing | prod, dev | deployment, database, infrastructure, configuration, queue_stream, runtime_shell |
| `scripts/migrate-to-stocksblitz-naming.sh` | critical | not_workflow | inferred_suggestion | present | prod, test, dev | database, infrastructure, configuration, runtime_shell |
| `scripts/migrate_secrets_to_config_service.py` | critical | not_workflow | inferred_suggestion | present | prod, staging, dev | database, configuration, queue_stream |
| `scripts/migrate_service_configs.py` | critical | not_workflow | inferred_suggestion | missing | prod, staging, dev | database, configuration, broker_order, queue_stream |
| `scripts/morning_refresh.sh` | critical | not_workflow | inferred_suggestion | missing | prod, dev | database, infrastructure, configuration, broker_order, runtime_shell |
| `scripts/phase2_data_coverage_validation.py` | critical | not_workflow | inferred_suggestion | present | prod, dev | deployment, database, configuration, broker_order |
| `scripts/phase2_performance_baseline.py` | critical | not_workflow | inferred_suggestion | present | prod, test, dev | database, configuration, broker_order, runtime_shell |
| `scripts/phase2_verification_suite.py` | critical | not_workflow | inferred_suggestion | present | prod, test, dev | deployment, database, configuration |
| `scripts/post-deployment-health-check.sh` | critical | not_workflow | inferred_suggestion | present | prod, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream |
| `scripts/production-health-check.sh` | critical | not_workflow | inferred_suggestion | present | prod, test, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream, runtime_shell |
| `scripts/production_checklist.py` | critical | not_workflow | embedded_hint | present | prod, test | database, infrastructure, configuration, ai_agent |
| `scripts/qa/reconcile_gateway_routes.py` | critical | not_workflow | declared_owner_map | present | prod | database, configuration |
| `scripts/qa/run_blocker_closure_cycle.py` | critical | not_workflow | declared_owner_map | present | prod | database, infrastructure, configuration, broker_order, runtime_shell |
| `scripts/qa/run_guardrail_suite.py` | critical | not_workflow | declared_owner_map | present | prod, test | database, infrastructure, configuration, queue_stream, runtime_shell |
| `scripts/qa/run_python_sdk_negative_path_certification.py` | critical | not_workflow | declared_owner_map | present | prod | database, configuration, broker_order |
| `scripts/qa/run_reference_strategy_sdk_suite.py` | critical | not_workflow | declared_owner_map | present | prod | configuration, broker_order, queue_stream |
| `scripts/real-time-data-sync.py` | critical | not_workflow | inferred_suggestion | missing | prod, dev | database, infrastructure, configuration, broker_order, queue_stream |
| `scripts/redeploy_changed_runtime_wave.sh` | critical | not_workflow | inferred_suggestion | present | prod, dev | deployment, infrastructure, configuration, broker_order |
| `scripts/restore-database.sh` | critical | not_workflow | inferred_suggestion | present | prod, test, dev | database, infrastructure, configuration |
| `scripts/retired/rename-to-stocksblitz.sh` | critical | not_workflow | inferred_suggestion | present | prod, dev | deployment, database, infrastructure, configuration, broker_order, queue_stream |
| `scripts/rollback-phase1.sh` | critical | not_workflow | inferred_suggestion | present | prod, test, dev | deployment, database, infrastructure, configuration, broker_order |
| `scripts/rotate_encryption_key.sh` | critical | not_workflow | inferred_suggestion | present | prod, dev | database, infrastructure, configuration, runtime_shell, ai_agent |
| `scripts/run_load_tests.sh` | critical | not_workflow | inferred_suggestion | present | prod, test, dev | database, configuration, broker_order |
| `scripts/run_phase2_tests.sh` | critical | not_workflow | embedded_hint | present | prod, test, dev | database, infrastructure, configuration, broker_order, runtime_shell |
