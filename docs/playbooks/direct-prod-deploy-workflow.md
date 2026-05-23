# Direct Production Deploy Workflow

## Trigger

A workflow can mutate production outside the canonical promotion path.

## Standard Remediation

1. Block autonomous execution.
2. Map the workflow to `scripts/governance/promote_by_environment.sh`.
3. Require owner review.
4. Attach promotion and rollback evidence.
5. Retire or disable the direct deploy path after replacement.

## Completion Evidence

- canonical workflow path identified,
- owner boundary assigned,
- rollback evidence linked,
- production environment protection confirmed.
