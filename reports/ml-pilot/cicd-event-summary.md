# CI/CD Event Summary

Generated: `2026-05-23T03:25:33+00:00`

Workflow findings: `23`
Remote workflows visible: `26`
Remote-only workflows: `3`
Local-only workflows: `0`

## Surface Classes

- `deployment_capable`: 18
- `validation_only`: 5

## Trigger Counts

- `workflow_dispatch`: 20
- `push`: 12
- `pull_request`: 8
- `schedule`: 1

## Deployment-Capable Workflows

| Path | Risk | Autonomy | Triggers | Environments | Called Scripts | Next Action |
| --- | --- | --- | --- | --- | --- | --- |
| `.github/workflows/backend-production-promotion-diagnose.yml` | critical | blocked | workflow_dispatch | prod, test, dev | none_detected | block or require controlled owner review before use |
| `.github/workflows/ci.yml` | critical | blocked | pull_request, push | prod, staging, test | none_detected | block or require controlled owner review before use |
| `.github/workflows/config-service-production-pipeline.yml` | critical | blocked | pull_request, push, workflow_dispatch | prod, staging, test, dev | scripts/detect_parameter_duplicates.sh, scripts/generate_service_parameters.sh, scripts/validate_parameters.sh, scripts/verify-production-readiness.sh | block or require controlled owner review before use |
| `.github/workflows/deploy-backend-production.yml` | critical | blocked | workflow_dispatch | prod, test, dev | scripts/apply_service_sql_migrations.sh, scripts/governance/check_migration_bootstrap_audit.py, scripts/governance/run_backend_promotion_contract_preflight.sh, scripts/governance/run_service_sql_migration_dry_run.sh, scripts/verify_service_sql_migration_checksums.sh | block or require controlled owner review before use |
| `.github/workflows/deploy-backend-staging.yml` | critical | blocked | workflow_dispatch | prod, staging, test, dev | scripts/apply_service_sql_migrations.sh, scripts/governance/check_migration_bootstrap_audit.py, scripts/governance/run_backend_promotion_contract_preflight.sh, scripts/governance/run_service_sql_migration_dry_run.sh, scripts/verify_service_sql_migration_checksums.sh | block or require controlled owner review before use |
| `.github/workflows/deploy-frontend-production.yml` | critical | blocked | workflow_dispatch | prod, staging, test, dev | none_detected | block or require controlled owner review before use |
| `.github/workflows/deploy-production.yml` | critical | blocked | workflow_dispatch | prod, test, dev | none_detected | block or require controlled owner review before use |
| `.github/workflows/deploy-staging.yml` | critical | blocked | push, workflow_dispatch | prod, staging, test, dev | none_detected | block or require controlled owner review before use |
| `.github/workflows/environment-baseline-sync.yml` | critical | blocked | workflow_dispatch | prod, staging, test, dev | scripts/governance/run_environment_baseline_sync.sh | block or require controlled owner review before use |
| `.github/workflows/integration-tests.yml` | critical | blocked | pull_request, push, workflow_dispatch | prod, staging, test, dev | scripts/deployment-gate.sh | block or require controlled owner review before use |
| `.github/workflows/port-consistency-check.yml` | critical | blocked | pull_request, push | prod | scripts/validate-port-consistency.py | block or require controlled owner review before use |
| `.github/workflows/deploy-dev.yml` | high | prepare | push, workflow_dispatch | test, dev | none_detected | map to canonical automation or document exception |
| `.github/workflows/deploy-frontend-staging.yml` | high | prepare | workflow_dispatch | staging, test, dev | none_detected | map to canonical automation or document exception |
| `.github/workflows/environment-code-parity.yml` | high | prepare | push, workflow_dispatch | prod, staging, dev | scripts/governance/report_env_code_parity.py | map to canonical automation or document exception |
| `.github/workflows/load-tests.yml` | high | prepare | pull_request, push, workflow_dispatch | test | none_detected | map to canonical automation or document exception |
| `.github/workflows/phase1-tests.yml` | high | prepare | pull_request, push, workflow_dispatch | test | none_detected | map to canonical automation or document exception |
| `.github/workflows/promote-environments.yml` | high | controlled_execute | workflow_dispatch | prod, staging, test, dev | scripts/governance/promote_by_environment.sh | retain controlled execution with evidence |
| `.github/workflows/streaming-tracker-watch.yml` | high | prepare | push, workflow_dispatch | unknown | none_detected | map to canonical automation or document exception |

## Validation-Only Workflows

| Path | Risk | Triggers | Evidence | Next Action |
| --- | --- | --- | --- | --- |
| `.github/workflows/api-routing-validation.yml` | medium | pull_request, push, workflow_dispatch | present | map to canonical automation or document exception |
| `.github/workflows/credential-readiness-gate.yml` | medium | workflow_dispatch | missing | review accepted exception and renewal evidence |
| `.github/workflows/governance-readiness-cadence.yml` | medium | schedule, workflow_dispatch | present | map to canonical automation or document exception |
| `.github/workflows/promotion-preflight.yml` | medium | workflow_dispatch | missing | review accepted exception and renewal evidence |
| `.github/workflows/standards-guard.yml` | medium | pull_request, push | present | review accepted exception and renewal evidence |

## Remote-Only Workflows

- `.github/workflows/deploy-to-development.yml`
- `.github/workflows/deploy-to-production.yml`
- `.github/workflows/manual-production-deploy.yml`
