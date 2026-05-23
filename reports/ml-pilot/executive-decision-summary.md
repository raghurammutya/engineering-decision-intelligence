# Executive Decision Summary

Generated: `2026-05-23T03:25:33+00:00`

## Priority Counts

- `P0`: 120
- `P2`: 119
- `P3`: 62
- `P4`: 186

## Top Decisions

| Priority | Path | Reason | Owner | Decision |
| --- | --- | --- | --- | --- |
| P0 | `.github/workflows/backend-production-promotion-diagnose.yml` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `.github/workflows/ci.yml` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `.github/workflows/config-service-production-pipeline.yml` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `.github/workflows/deploy-backend-production.yml` | blocked production mutation | present | block or require controlled owner review before use |
| P0 | `.github/workflows/deploy-backend-staging.yml` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `.github/workflows/deploy-frontend-production.yml` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `.github/workflows/deploy-production.yml` | blocked production mutation | present | block or require controlled owner review before use |
| P0 | `.github/workflows/deploy-staging.yml` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `.github/workflows/environment-baseline-sync.yml` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `.github/workflows/integration-tests.yml` | blocked production mutation | present | block or require controlled owner review before use |
| P0 | `.github/workflows/port-consistency-check.yml` | blocked production mutation | present | block or require controlled owner review before use |
| P0 | `scripts/apply_algo_engine_sql_migrations.sh` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/apply_instrument_registry_migrations.sh` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/apply_payoff_live_mode_config.sh` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/apply_service_sql_migrations.sh` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/backfill_today_via_ticker_service.py` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/backup/backup-service.py` | blocked production mutation | platform-operations (backup and recovery) | block or require controlled owner review before use |
| P0 | `scripts/bootstrap-dev-api-gateway-prereqs.py` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/bootstrap-dev-owner-service-prereqs.py` | blocked production mutation | present | block or require controlled owner review before use |
| P0 | `scripts/bootstrap_broker_rate_limit_profiles.py` | blocked production mutation | present | block or require controlled owner review before use |
| P0 | `scripts/bootstrap_nonprod_config_from_prod.py` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/code-quality-scan.sh` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/config.sh` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/copy_market_data.py` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/copy_market_data.sh` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/data-migration.py` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/deploy-phase1.sh` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/deploy-staging.sh` | blocked production mutation | present | block or require controlled owner review before use |
| P0 | `scripts/deploy.sh` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/deployment-gate.sh` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/detect_migration_regressions.sh` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/fetch_today_options_data.py` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/fix_config_service_encryption.sh` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/fix_timezone_data.py` | blocked production mutation | present | block or require controlled owner review before use |
| P0 | `scripts/fix_timezone_data_all_tables.py` | blocked production mutation | missing_or_unknown | block or require controlled owner review before use |
| P0 | `scripts/governance/apply_prod_schema_to_envs.sh` | blocked production mutation | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/backfill_news_impacts_recent.sh` | blocked production mutation | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/bootstrap_algo_engine_sdk_contracts_config.py` | blocked production mutation | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/bootstrap_env_roles_and_grants.sh` | blocked production mutation | platform-governance (governance automation) | block or require controlled owner review before use |
| P0 | `scripts/governance/bootstrap_instrument_universe_config.py` | blocked production mutation | platform-governance (governance automation) | block or require controlled owner review before use |
