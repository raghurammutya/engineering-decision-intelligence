# DIP Implementation Backlog

Generated: `2026-05-23T15:27:52+00:00`

Milestone: `DIP governed decision review and simulation MVP`
Source boundary: `edi_governed_backlog_not_dip_runtime_implementation`
Runtime execution allowed: `False`
Backlog defined: `100.0%`
Slices: `10 / 10`
Parallelization groups: `pre_runtime_engines, schema_contracts, serialized_integration`

| id | status | allowed_autonomy | parallelization_group | depends_on |
| --- | --- | --- | --- | --- |
| decision-spec-contract-v1 | completed | controlled_execute | schema_contracts | [] |
| capability-registry-contract-v1 | completed | controlled_execute | schema_contracts | [] |
| policy-preflight-contract-v1 | completed | controlled_execute | schema_contracts | [] |
| simulation-evidence-contract-v1 | completed | controlled_execute | schema_contracts | ['decision-spec-contract-v1', 'capability-registry-contract-v1'] |
| decision-diff-v1 | completed | controlled_execute | pre_runtime_engines | ['decision-spec-contract-v1', 'capability-registry-contract-v1', 'simulation-evidence-contract-v1'] |
| approval-record-contract-v1 | completed | controlled_execute | pre_runtime_engines | ['policy-preflight-contract-v1', 'simulation-evidence-contract-v1'] |
| case-evidence-pack-v1 | completed | controlled_execute | pre_runtime_engines | ['decision-diff-v1', 'approval-record-contract-v1'] |
| replay-reader-v1 | completed | controlled_execute | pre_runtime_engines | ['case-evidence-pack-v1'] |
| mvp-trust-loop-cli-v1 | completed | controlled_execute | serialized_integration | ['replay-reader-v1'] |
| dip-mvp-acceptance-pack-v1 | completed | controlled_execute | serialized_integration | ['mvp-trust-loop-cli-v1'] |
