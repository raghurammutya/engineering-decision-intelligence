# Autopilot Mission Checklist

Generated: `2026-05-23T03:19:35+00:00`

Mission: `cicd-event-ingestion-v1`
Title: CI/CD Event Ingestion V1
Risk: `medium`
Safe mode: `plan_only`
Product completion delta if completed: `+6.0%`
Projected product completion: `46.0%`

## Safety Boundary

This command selects and explains work. It does not edit files, mutate external systems, or touch blocked paths.

## Allowed Paths

- `tools/**`
- `tests/**`
- `reports/**`
- `docs/mvp/**`
- `roadmap/autopilot-backlog.json`

## Blocked Paths

- `/home/stocksadmin/workspace/ML/**`

## Acceptance Criteria

- [ ] Workflow event summaries are materialized from discovered workflow findings and GitHub enrichment.
- [ ] Deployment-capable CI/CD surfaces are separated from validation-only workflows.
- [ ] Acceptance gates validate CI/CD ingestion export contracts.

## Validation Commands

- [ ] `python3 -m edi scan ml-pilot`
- [ ] `python3 -m edi validate`

## Completion Rule

- [ ] Implementation stayed within allowed paths.
- [ ] No blocked path was modified.
- [ ] All validation commands passed.
- [ ] Product progress was regenerated and checked.
- [ ] CI passed after push.
