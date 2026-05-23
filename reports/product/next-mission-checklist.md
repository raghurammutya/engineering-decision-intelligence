# Autopilot Mission Checklist

Generated: `2026-05-23T04:06:36+00:00`

Mission: `product-api-v1`
Title: Product API V1
Risk: `medium`
Safe mode: `plan_only`
Product completion delta if completed: `+5.0%`
Projected product completion: `89.0%`

## Safety Boundary

This command selects and explains work. It does not edit files, mutate external systems, or touch blocked paths.

## Allowed Paths

- `tools/**`
- `tests/**`
- `reports/**`
- `docs/mvp/**`
- `roadmap/autopilot-backlog.json`
- `edi/**`

## Blocked Paths

- `/home/stocksadmin/workspace/ML/**`

## Acceptance Criteria

- [ ] Product API emits a stable machine-readable snapshot from generated reports.
- [ ] API output includes progress, next mission, executive decisions, and top operational risks.
- [ ] Acceptance gates validate product API contracts.

## Validation Commands

- [ ] `python3 -m edi validate`

## Completion Rule

- [ ] Implementation stayed within allowed paths.
- [ ] No blocked path was modified.
- [ ] All validation commands passed.
- [ ] Product progress was regenerated and checked.
- [ ] CI passed after push.
