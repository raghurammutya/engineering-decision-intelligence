# GitHub Protection Findings

Generated: `2026-05-23T02:03:32+00:00`

| Severity | Finding | Evidence | Decision |
| --- | --- | --- | --- |
| P1 | Default branch protection not visible | GitHub API returned no protection payload | Review branch protection for default branch |
| P0 | `prod` environment has no protection rules | `protection_rules` is empty | Add required reviewers or deployment protection |
| P1 | `prod` allows admin bypass | `can_admins_bypass=true` | Review bypass policy for production environments |
| P0 | `production` environment has no protection rules | `protection_rules` is empty | Add required reviewers or deployment protection |
| P1 | `production` allows admin bypass | `can_admins_bypass=true` | Review bypass policy for production environments |
| P0 | Mutation-capable workflow `.github/workflows/backend-production-promotion-diagnose.yml` needs protection review | critical/blocked | Confirm branch and environment protection before execution |
| P0 | Mutation-capable workflow `.github/workflows/ci.yml` needs protection review | critical/blocked | Confirm branch and environment protection before execution |
| P0 | Mutation-capable workflow `.github/workflows/config-service-production-pipeline.yml` needs protection review | critical/blocked | Confirm branch and environment protection before execution |
| P0 | Mutation-capable workflow `.github/workflows/deploy-backend-production.yml` needs protection review | critical/blocked | Confirm branch and environment protection before execution |
| P0 | Mutation-capable workflow `.github/workflows/deploy-backend-staging.yml` needs protection review | critical/blocked | Confirm branch and environment protection before execution |
| P2 | Mutation-capable workflow `.github/workflows/deploy-dev.yml` needs protection review | high/prepare | Confirm branch and environment protection before execution |
| P0 | Mutation-capable workflow `.github/workflows/deploy-frontend-production.yml` needs protection review | critical/blocked | Confirm branch and environment protection before execution |
| P2 | Mutation-capable workflow `.github/workflows/deploy-frontend-staging.yml` needs protection review | high/prepare | Confirm branch and environment protection before execution |
| P0 | Mutation-capable workflow `.github/workflows/deploy-production.yml` needs protection review | critical/blocked | Confirm branch and environment protection before execution |
| P0 | Mutation-capable workflow `.github/workflows/deploy-staging.yml` needs protection review | critical/blocked | Confirm branch and environment protection before execution |
| P0 | Mutation-capable workflow `.github/workflows/environment-baseline-sync.yml` needs protection review | critical/blocked | Confirm branch and environment protection before execution |
| P2 | Mutation-capable workflow `.github/workflows/environment-code-parity.yml` needs protection review | high/prepare | Confirm branch and environment protection before execution |
| P0 | Mutation-capable workflow `.github/workflows/integration-tests.yml` needs protection review | critical/blocked | Confirm branch and environment protection before execution |
| P3 | Mutation-capable workflow `.github/workflows/load-tests.yml` needs protection review | high/prepare | Confirm branch and environment protection before execution |
| P2 | Mutation-capable workflow `.github/workflows/phase1-tests.yml` needs protection review | high/prepare | Confirm branch and environment protection before execution |
| P0 | Mutation-capable workflow `.github/workflows/port-consistency-check.yml` needs protection review | critical/blocked | Confirm branch and environment protection before execution |
| P2 | Mutation-capable workflow `.github/workflows/streaming-tracker-watch.yml` needs protection review | high/prepare | Confirm branch and environment protection before execution |
| P2 | GitHub workflow `.github/workflows/deploy-to-development.yml` is visible remotely but absent locally | workflow list divergence | Reconcile local branch with GitHub default branch |
| P2 | GitHub workflow `.github/workflows/deploy-to-production.yml` is visible remotely but absent locally | workflow list divergence | Reconcile local branch with GitHub default branch |
| P2 | GitHub workflow `.github/workflows/manual-production-deploy.yml` is visible remotely but absent locally | workflow list divergence | Reconcile local branch with GitHub default branch |
