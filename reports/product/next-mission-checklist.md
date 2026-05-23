# Autopilot Mission Checklist

Generated: `2026-05-23T04:11:18+00:00`

Mission: `product-ui-v1`
Title: Product UI V1
Risk: `medium`
Safe mode: `plan_only`
Product completion delta if completed: `+3.0%`
Projected product completion: `92.0%`

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

- [ ] Operator-facing product view is generated from the Product API snapshot.
- [ ] UI output summarizes progress, next mission, decision backlog, and risk signals without requiring source repository changes.
- [ ] Acceptance gates validate the product UI contract.

## Validation Commands

- [ ] `python3 -m edi validate`

## Completion Rule

- [ ] Implementation stayed within allowed paths.
- [ ] No blocked path was modified.
- [ ] All validation commands passed.
- [ ] Product progress was regenerated and checked.
- [ ] CI passed after push.
