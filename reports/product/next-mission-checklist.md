# Autopilot Mission Checklist

Generated: `2026-05-23T02:47:03+00:00`

Mission: `acceptance-gates-v2`
Title: Acceptance Gates v2
Risk: `medium`
Safe mode: `plan_only`
Product completion delta if completed: `+5.0%`
Projected product completion: `26.0%`

## Safety Boundary

This command selects and explains work. It does not edit files, mutate external systems, or touch blocked paths.

## Allowed Paths

- `.github/workflows/**`
- `edi/**`
- `tests/**`
- `tools/**`
- `reports/**`
- `roadmap/autopilot-backlog.json`

## Blocked Paths

- `/home/stocksadmin/workspace/ML/**`

## Acceptance Criteria

- [ ] CLI command contracts are tested.
- [ ] Generated graph and report output contracts are tested.
- [ ] CI blocks stale product progress reports.

## Validation Commands

- [ ] `python3 -m edi validate`
- [ ] `python3 -m edi progress --check`

## Completion Rule

- [ ] Implementation stayed within allowed paths.
- [ ] No blocked path was modified.
- [ ] All validation commands passed.
- [ ] Product progress was regenerated and checked.
- [ ] CI passed after push.
