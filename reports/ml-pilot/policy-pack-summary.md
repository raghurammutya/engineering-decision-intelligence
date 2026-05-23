# Policy Pack Summary

Generated: `2026-05-23T03:29:22+00:00`

Policy pack: `scanner-operational-safety-v1`
Source policy: `/home/stocksadmin/workspace/engineering-decision-intelligence/policies/ml-pilot-policy.json`

## Section Counts

- `accepted_exceptions`: 3
- `canonical_artifacts`: 6
- `canonical_commands`: 2
- `owner_rules`: 10
- `owner_suggestion_rules`: 10
- `readonly_patterns`: 23

## Canonical Commands

| Command | Type |
| --- | --- |
| `scripts/envctl.sh` | canonical_command |
| `scripts/governance/promote_by_environment.sh` | canonical_command |

## Owner Rules

| Pattern | Owner | Boundary |
| --- | --- | --- |
| `.github/workflows/promote-environments.yml` | platform-governance | environment promotion |
| `.github/workflows/promotion-preflight.yml` | platform-governance | promotion readiness |
| `.github/workflows/standards-guard.yml` | architecture-governance | standards enforcement |
| `scripts/envctl.sh` | platform-governance | environment lifecycle |
| `scripts/governance/promote_by_environment.sh` | platform-governance | environment promotion |
| `scripts/governance/*.sh` | platform-governance | governance automation |
| `scripts/governance/*.py` | platform-governance | governance automation |
| `scripts/qa/**` | qa-governance | quality evidence |
| `scripts/security/**` | security-governance | security operations |
| `scripts/backup/**` | platform-operations | backup and recovery |

## Owner Suggestion Rules

| Type | Key | Owner | Boundary |
| --- | --- | --- | --- |
| path_rule | `.github/workflows/*.yml` | platform-governance | GitHub workflow governance |
| path_rule | `scripts/security/**` | security-governance | security operations |
| family_rule | `deploy_workflows` | platform-governance | deployment and promotion |
| family_rule | `db_migration_scripts` | data-platform | database migration and data mutation |
| family_rule | `config_secret_scripts` | platform-security | configuration and secret handling |
| family_rule | `broker_order_scripts` | trading-platform | broker and order safety |
| family_rule | `governance_probes` | platform-governance | runtime governance probes |
| family_rule | `qa_readiness_checks` | qa-governance | quality and readiness evidence |
| family_rule | `backup_restore` | platform-operations | backup and restore |
| family_rule | `ai_agent_tooling` | agent-platform | AI-agent tooling |

## Accepted Exceptions

| Pattern | Reason |
| --- | --- |
| `.github/workflows/promotion-preflight.yml` | Readiness gate may reference production and staging policy without performing promotion. |
| `.github/workflows/credential-readiness-gate.yml` | Credential gate may inspect secret readiness but should remain non-mutating. |
| `.github/workflows/standards-guard.yml` | Standards guard may reference production policy while enforcing read-only checks. |

## Read-Only Patterns

- `.github/workflows/*validation*.yml`
- `.github/workflows/*readiness*.yml`
- `.github/workflows/*guard*.yml`
- `.github/workflows/*preflight*.yml`
- `scripts/check_*`
- `scripts/check-*`
- `scripts/audit_*`
- `scripts/audit-*`
- `scripts/validate_*`
- `scripts/validate-*`
- `scripts/verify_*`
- `scripts/verify-*`
- `scripts/generate_*`
- `scripts/generate-*`
- `scripts/find_*`
- `scripts/find-*`
- `scripts/compare_*`
- `scripts/compare-*`
- `scripts/extract_*`
- `scripts/extract-*`
- `scripts/qa/check_*`
- `scripts/qa/verify_*`
- `scripts/qa/*probe*`
