# Policies

Policy files make scanner behavior auditable and safer to change.

The prototype uses JSON rather than YAML so CI can run with Python standard
library only.

## Files

| File | Purpose |
| --- | --- |
| `autonomy-policy.json` | Default autonomy-mode mapping by risk |
| `ml-pilot-policy.json` | ML pilot canonical commands and intended promotion policy |
| `ml-owner-map.json` | Owner and service-boundary hints for ML artifacts |
| `ml-accepted-exceptions.json` | Known exception paths that remain visible for review |
| `ml-readonly-patterns.json` | Patterns that usually represent validation/reporting rather than mutation |
| `ml-canonical-artifacts.json` | Canonical or accepted artifact-path classifications |
| `github-control-baseline.json` | Expected GitHub branch and environment controls |

## Current Policy Scope

The scanner currently consumes:

- `canonical_commands`
- `canonical_artifacts`
- `accepted_exceptions`
- `owner_map`
- `readonly_patterns`
- `autonomy.default_by_risk`
- `autonomy.controlled_execute_when`

Other fields document intended policy and will be wired into later
reconciliation rules. `ml-pilot-policy.json` includes the other ML policy maps
so callers can use one policy entrypoint.

## Safety Principle

Policy changes should be tested because they can change autonomy decisions.
For example, adding a canonical command can move an artifact from `blocked` or
`prepare` toward `controlled_execute`.
