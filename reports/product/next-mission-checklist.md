# Autopilot Mission Checklist

Generated: `2026-05-23T03:22:48+00:00`

Mission: `runtime-ingestion-v1`
Title: Runtime Ingestion V1
Risk: `medium`
Safe mode: `plan_only`
Product completion delta if completed: `+10.0%`
Projected product completion: `56.0%`

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

- [ ] Runtime signal records are inferred from scanner findings without touching runtime systems.
- [ ] Runtime mutation surfaces are grouped by environment, mutation type, and evidence state.
- [ ] Acceptance gates validate runtime ingestion export contracts.

## Validation Commands

- [ ] `python3 -m edi scan ml-pilot`
- [ ] `python3 -m edi validate`

## Completion Rule

- [ ] Implementation stayed within allowed paths.
- [ ] No blocked path was modified.
- [ ] All validation commands passed.
- [ ] Product progress was regenerated and checked.
- [ ] CI passed after push.
