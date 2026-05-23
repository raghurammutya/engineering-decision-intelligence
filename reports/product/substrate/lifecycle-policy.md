# Operational Substrate Lifecycle Policy

Generated: `2026-05-23T16:16:11+00:00`

Scope: `recommended_default_for_production_edi_targets`
Promotion order: `dev -> test -> staging -> prod`
Promotion contract: `build_once_validate_in_dev_promote_same_artifact`
Promotion path policy: `one_canonical_path_required`
GHCR policy: `allowed_only_as_wrapper_or_implementation_detail_behind_canonical_promotion_contract`

## Runtime Separation

| environment | purpose | builds_allowed | broad_tests_allowed | runtime_only |
| --- | --- | --- | --- | --- |
| dev | developer validation only | True | True | False |
| test | integration and regression validation | False | True | False |
| staging | production-like release candidate validation | False | False | False |
| prod | runtime, health checks, rollback verification | False | False | True |

## Admission Model

| operation | admission |
| --- | --- |
| read_only_checks | free |
| targeted_cleanup | explicit_scope_required |
| docker_volume_cleanup | sre_dba_approval_and_backup_proof_required |
| promotion_preflight | explicit_admission_required |
| promotion | separate_explicit_admission_required |
| order_service_changes | separate_owner_admission_required |
