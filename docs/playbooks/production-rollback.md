# Production Rollback

## Trigger

A production release or enforcement action causes a regression, failed control,
or unacceptable runtime risk.

## Standard Remediation

1. Stop additional autonomous production actions for the affected target.
2. Identify the last known good release, workflow run, or promotion record.
3. Revert through the approved repository promotion or deployment path.
4. Re-run required validation and target health checks.
5. Attach rollback evidence to the incident, deployment, or enforcement record.

## Completion Evidence

- affected target identified,
- rollback path used,
- validation and health checks passed,
- owner review recorded,
- follow-up reconciliation item opened if runtime truth changed.
