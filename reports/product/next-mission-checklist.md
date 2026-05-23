# Autopilot Mission Checklist

Generated: `2026-05-23T03:26:00+00:00`

Mission: `policy-pack-productization-v1`
Title: Policy Pack Productization V1
Risk: `medium`
Safe mode: `plan_only`
Product completion delta if completed: `+5.0%`
Projected product completion: `61.0%`

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

- [ ] Reusable policy-pack metadata is generated from active scanner policy inputs.
- [ ] Policy-pack outputs separate canonical commands, owner rules, exceptions, and read-only rules.
- [ ] Acceptance gates validate policy-pack export contracts.

## Validation Commands

- [ ] `python3 -m edi scan ml-pilot`
- [ ] `python3 -m edi validate`

## Completion Rule

- [ ] Implementation stayed within allowed paths.
- [ ] No blocked path was modified.
- [ ] All validation commands passed.
- [ ] Product progress was regenerated and checked.
- [ ] CI passed after push.
