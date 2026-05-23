# Decision Insight Clusters

Generated: `2026-05-23T04:52:01+00:00`

Findings grouped: `567`
Decision clusters: `33`
Likely scanner tuning candidates: `149`
Likely operational blockers: `327`

## Top Decision Clusters

| Rank | Cluster | Findings | Risk Reduction Score | Scanner Tuning | Operational Blockers | Top Action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `config_secret_scripts::block-or-certify-critical-operational-mutation` | 137 | 26980 | 5 | 132 | block or require controlled owner review before use |
| 2 | `db_migration_scripts::block-or-certify-critical-operational-mutation` | 22 | 4560 | 0 | 22 | block or require controlled owner review before use |
| 3 | `config_secret_scripts::assign-accountable-owner-boundary` | 61 | 3924 | 23 | 38 | map to canonical automation or document exception |
| 4 | `config_secret_scripts::canonicalize-or-document-exception` | 87 | 1961 | 72 | 15 | map to canonical automation or document exception |
| 5 | `db_migration_scripts::assign-accountable-owner-boundary` | 26 | 1780 | 5 | 21 | map to canonical automation or document exception |
| 6 | `governance_probes::review-before-autonomy-expansion` | 62 | 1684 | 0 | 0 | map to canonical automation or document exception |
| 7 | `config_secret_scripts::attach-safety-and-rollback-evidence` | 26 | 1022 | 16 | 10 | map to canonical automation or document exception |
| 8 | `deploy_workflows::block-or-certify-critical-operational-mutation` | 5 | 1010 | 0 | 5 | block or require controlled owner review before use |
| 9 | `config_secret_scripts::review-before-autonomy-expansion` | 20 | 782 | 1 | 15 | retain controlled execution with evidence |
| 10 | `db_migration_scripts::review-before-autonomy-expansion` | 18 | 636 | 0 | 9 | map to canonical automation or document exception |
| 11 | `governance_probes::block-or-certify-critical-operational-mutation` | 3 | 585 | 0 | 3 | block or require controlled owner review before use |
| 12 | `db_migration_scripts::canonicalize-or-document-exception` | 20 | 507 | 13 | 7 | map to canonical automation or document exception |
| 13 | `other_scripts::review-before-autonomy-expansion` | 12 | 489 | 0 | 12 | assign owner boundary |
| 14 | `db_migration_scripts::attach-safety-and-rollback-evidence` | 8 | 482 | 2 | 6 | map to canonical automation or document exception |
| 15 | `broker_order_scripts::assign-accountable-owner-boundary` | 5 | 465 | 0 | 5 | map to canonical automation or document exception |
| 16 | `other_scripts::assign-accountable-owner-boundary` | 5 | 425 | 0 | 5 | map to canonical automation or document exception |
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
| `.claude/commands/browser-test.md` | high | db_migration_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `.github/workflows/deploy-dev.yml` | high | deploy_workflows | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `.github/workflows/deploy-frontend-staging.yml` | high | deploy_workflows | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `.github/workflows/load-tests.yml` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `.github/workflows/phase1-tests.yml` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `BACKEND_TEAM_PROMPT_LOGIN_AFTER_SIGNUP.md` | high | db_migration_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `BROWSER_DEBUGGING_PROMPT.md` | high | ai_agent_tooling | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `PHASE_2.5_DAY3_IMPLEMENTATION_PROMPT.md` | high | db_migration_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `SPRINT_1.5_MARKETPLACE_INFRASTRUCTURE_PROMPT.md` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `alert_service/app/background/evaluation_worker.py` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `alert_service/test_evaluation.py` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `docs/prompts/ADV_ADVISORY_LAYER_IMPLEMENTATION.md` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `docs/prompts/API_GATEWAY_TESTING_CONTINUATION.md` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `docs/prompts/MESSAGING_SERVICE_SPRINT_PLAN.md` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `docs/prompts/algo-engine-advanced-intent-wiring-prompt.md` | high | db_migration_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `docs/prompts/new-broker-integration-master-prompt.md` | high | config_secret_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `docs/qa/prompts/aef_next_tracks/AEF_PARALLEL_SCRIPT_STRATEGY_EXECUTION_REVIEW_PROMPT.md` | high | db_migration_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
| `prompts_for_validation.md` | high | db_migration_scripts | test evidence present but mutation words triggered high risk | review rule, read-only pattern, or accepted exception |
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

## Operational Blockers

| Path | Risk | Autonomy | Family | Next Action |
| --- | --- | --- | --- | --- |
| `docs/prompts/CONFIG_SERVICE_IMPROVEMENTS.md` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
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
| `.claude/commands/assess-architecture.md` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `.claude/commands/assess-infrastructure.md` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `.github/workflows/backend-production-promotion-diagnose.yml` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `.github/workflows/ci.yml` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `.github/workflows/config-service-production-pipeline.yml` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `.github/workflows/deploy-backend-staging.yml` | critical | blocked | deploy_workflows | block or require controlled owner review before use |
| `.github/workflows/deploy-frontend-production.yml` | critical | blocked | deploy_workflows | block or require controlled owner review before use |
| `.github/workflows/deploy-staging.yml` | critical | blocked | deploy_workflows | block or require controlled owner review before use |
| `.github/workflows/environment-baseline-sync.yml` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `BACKEND_FIX_PROMPTS.md` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `NEXT_SESSION_PROMPT.md` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `backend_prompt.md` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `dev-prompt.txt` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `docs/prompts/CLAUDE_CLI_PROMPT_GREEKS_CACHE_IMPLEMENTATION.md` | critical | blocked | db_migration_scripts | block or require controlled owner review before use |
| `docs/prompts/CONFIG_SERVICE_GUIDE.md` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `docs/prompts/EXTENDED_CONFIG_SERVICE.md` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `docs/prompts/MULTI_SERVICE_REFACTOR_BATCH_PROMPT.md` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `docs/prompts/MY_STRATEGIES_SPRINT_PLAN.md` | critical | blocked | db_migration_scripts | block or require controlled owner review before use |
| `docs/prompts/README.md` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `docs/prompts/calendar-service-context.md` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `docs/prompts/comms-service-context.md` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `docs/prompts/fix-verified-issues-prompt.md` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `docs/prompts/rating-service-context.md` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `docs/prompts/support-service-context.md` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `docs/prompts/ticker-service-context.md` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `docs/qa/prompts/aef_next_tracks/AEF_306_STRATEGY_SDK_CHANNEL_EXECUTION_HANDOFF_PROMPT.md` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `docs/qa/prompts/aef_next_tracks/AEF_DEFERRED_PRODUCTION_RESILIENCE_READINESS_PROMPT.md` | critical | blocked | db_migration_scripts | block or require controlled owner review before use |
| `docs/qa/prompts/aef_next_tracks/AEF_ORCHESTRATOR_PROMPT.md` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
| `docs/qa/prompts/aef_next_tracks/README.md` | critical | blocked | broker_order_scripts | block or require controlled owner review before use |
| `infra-prompt.txt` | critical | blocked | config_secret_scripts | block or require controlled owner review before use |
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
