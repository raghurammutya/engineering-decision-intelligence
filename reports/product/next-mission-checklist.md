# Autopilot Mission Checklist

Generated: `2026-05-23T03:30:05+00:00`

Mission: `graph-backend-abstraction-v1`
Title: Graph Backend Abstraction V1
Risk: `medium`
Safe mode: `plan_only`
Product completion delta if completed: `+7.0%`
Projected product completion: `68.0%`

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

- [ ] Graph output writer is abstracted behind a backend-neutral interface.
- [ ] Current JSON graph output remains byte-for-byte contract compatible after regeneration.
- [ ] Acceptance gates validate graph backend abstraction contracts.

## Validation Commands

- [ ] `python3 -m edi scan ml-pilot`
- [ ] `python3 -m edi validate`

## Completion Rule

- [ ] Implementation stayed within allowed paths.
- [ ] No blocked path was modified.
- [ ] All validation commands passed.
- [ ] Product progress was regenerated and checked.
- [ ] CI passed after push.
