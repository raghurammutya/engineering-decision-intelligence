# Policy Coverage Report

Generated: `2026-05-23T04:52:01+00:00`

## Coverage Counts

- `evidence_reference`: 385
- `owner_map`: 250
- `readonly_pattern`: 124
- `uncovered`: 81
- `canonical_artifact`: 12
- `accepted_exception`: 3

## Gaps

- Ownerless artifacts: `264`
- High/critical artifacts without policy coverage: `74`

## High/Critical Without Policy Coverage

| Path | Risk | Autonomy | Next Action |
| --- | --- | --- | --- |
| `.github/workflows/port-consistency-check.yml` | critical | blocked | block or require controlled owner review before use |
| `docs/prompts/CONFIG_SERVICE_IMPROVEMENTS.md` | critical | blocked | block or require controlled owner review before use |
| `scripts/apply_algo_engine_sql_migrations.sh` | critical | blocked | block or require controlled owner review before use |
| `scripts/apply_instrument_registry_migrations.sh` | critical | blocked | block or require controlled owner review before use |
| `scripts/backfill_today_via_ticker_service.py` | critical | blocked | block or require controlled owner review before use |
| `scripts/config.sh` | critical | blocked | block or require controlled owner review before use |
| `scripts/copy_market_data.py` | critical | blocked | block or require controlled owner review before use |
| `scripts/copy_market_data.sh` | critical | blocked | block or require controlled owner review before use |
| `scripts/data-migration.py` | critical | blocked | block or require controlled owner review before use |
| `scripts/fetch_today_options_data.py` | critical | blocked | block or require controlled owner review before use |
| `scripts/fix_config_service_encryption.sh` | critical | blocked | block or require controlled owner review before use |
| `scripts/fix_timezone_data.py` | critical | blocked | block or require controlled owner review before use |
| `scripts/fix_timezone_data_all_tables.py` | critical | blocked | block or require controlled owner review before use |
| `scripts/lock-production.sh` | critical | blocked | block or require controlled owner review before use |
| `scripts/migrate_service_configs.py` | critical | blocked | block or require controlled owner review before use |
| `scripts/morning_refresh.sh` | critical | blocked | block or require controlled owner review before use |
| `scripts/real-time-data-sync.py` | critical | blocked | block or require controlled owner review before use |
| `scripts/setup-monitoring-service.sh` | critical | blocked | block or require controlled owner review before use |
| `scripts/switch-env.sh` | critical | blocked | block or require controlled owner review before use |
| `scripts/sync-registry-from-ports.sh` | critical | blocked | block or require controlled owner review before use |
| `scripts/sync_instrument_registry_broker_tokens.sh` | critical | blocked | block or require controlled owner review before use |
| `.claude/commands/debug-browser.md` | high | prepare | map to canonical automation or document exception |
| `.github/workflows/environment-code-parity.yml` | high | prepare | map to canonical automation or document exception |
| `.github/workflows/streaming-tracker-watch.yml` | high | prepare | map to canonical automation or document exception |
| `docs/prompts/API_GATEWAY_ARCHITECTURE.md` | high | prepare | map to canonical automation or document exception |
| `docs/prompts/MY_STRATEGIES_PAGE_REDESIGN.md` | high | prepare | map to canonical automation or document exception |
| `docs/prompts/dataflows.md` | high | prepare | map to canonical automation or document exception |
| `docs/prompts/domain-glossary.md` | high | prepare | map to canonical automation or document exception |
| `scripts/apply_marketplace_migrations.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/backfill_7days_complete.py` | high | prepare | map to canonical automation or document exception |
| `scripts/backfill_7days_optimized.py` | high | prepare | map to canonical automation or document exception |
| `scripts/backfill_enhanced_greeks.py` | high | prepare | map to canonical automation or document exception |
| `scripts/backfill_from_last_till_now.py` | high | prepare | map to canonical automation or document exception |
| `scripts/backfill_today.py` | high | prepare | map to canonical automation or document exception |
| `scripts/backfill_today_kite.py` | high | prepare | map to canonical automation or document exception |
| `scripts/backup-database.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/bootstrap-dev-auth-prereqs.py` | high | prepare | map to canonical automation or document exception |
| `scripts/bootstrap-dev-entity-acl-prereqs.py` | high | prepare | map to canonical automation or document exception |
| `scripts/bootstrap_environment_databases.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/broker_account_sync.py` | high | prepare | map to canonical automation or document exception |
| `scripts/broker_account_sync_v2.py` | high | prepare | map to canonical automation or document exception |
| `scripts/broker_account_sync_v3.py` | high | prepare | map to canonical automation or document exception |
| `scripts/classify_market_cap.py` | high | prepare | map to canonical automation or document exception |
| `scripts/daily_aggregation.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/decrypt_mf_xls.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/decrypt_secrets.py` | high | prepare | map to canonical automation or document exception |
| `scripts/deep_code_analyzer.py` | high | prepare | map to canonical automation or document exception |
| `scripts/dev_validation/seed_positions_sidecar_positive_fixture.py` | high | prepare | map to canonical automation or document exception |
| `scripts/encrypt_secrets.py` | high | prepare | map to canonical automation or document exception |
| `scripts/fetch_index_data.py` | high | prepare | map to canonical automation or document exception |
| `scripts/governance_checks.py` | high | prepare | map to canonical automation or document exception |
| `scripts/infra_replay_preflight.py` | high | prepare | map to canonical automation or document exception |
| `scripts/ingest_mf_disclosure_file.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/ingest_mf_portfolio_statement_encrypted.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/ingest_mf_portfolio_statement_file.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/map_service_dependencies.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/marketplace_latency_probe.py` | high | prepare | map to canonical automation or document exception |
| `scripts/midnight_refresh.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/orchestrate_codex_claude.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/phase3_contract_checks.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/postgres-replica-init.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/pre-commit-check.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/reconcile_mf_soa_vs_broker_holdings.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/register_user_service_mfa_key.py` | high | prepare | map to canonical automation or document exception |
| `scripts/run_auth_orchestration.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/run_live_probe.py` | high | prepare | map to canonical automation or document exception |
| `scripts/secrets_restore.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/setup_daily_aggregation.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/staging/bootstrap_user_service_identity.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/stocksblitz_memory_guard.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/store_manual_token.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/sync-config-parameters.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/system-cleanup.sh` | high | prepare | map to canonical automation or document exception |
| `scripts/update_binance_credentials_prod.sh` | high | prepare | map to canonical automation or document exception |
