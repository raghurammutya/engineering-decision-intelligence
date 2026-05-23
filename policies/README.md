# Policies

Policy files make scanner behavior auditable and safer to change.

The prototype uses JSON rather than YAML so CI can run with Python standard
library only.

## Files

| File | Purpose |
| --- | --- |
| `autonomy-policy.json` | Default autonomy-mode mapping by risk |
| `ml-pilot-policy.json` | ML pilot canonical commands and intended promotion policy |

## Current Policy Scope

The scanner currently consumes:

- `canonical_commands`
- `autonomy.default_by_risk`
- `autonomy.controlled_execute_when`

Other fields document intended policy and will be wired into later
reconciliation rules.

## Safety Principle

Policy changes should be tested because they can change autonomy decisions.
For example, adding a canonical command can move an artifact from `blocked` or
`prepare` toward `controlled_execute`.
