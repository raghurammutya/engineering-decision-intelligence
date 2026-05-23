# Autopilot Mission Checklist

Generated: `2026-05-23T03:08:00+00:00`

Mission: `owner-workflows-v2`
Title: Owner Workflows V2
Risk: `medium`
Safe mode: `plan_only`
Product completion delta if completed: `+4.0%`
Projected product completion: `40.0%`

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

- [ ] Owner assignment confidence is materialized for ML pilot findings.
- [ ] Owner review queues distinguish inferred owners from missing owners.
- [ ] Acceptance gates validate owner workflow export contracts.

## Validation Commands

- [ ] `python3 -m edi scan ml-pilot`
- [ ] `python3 -m edi validate`

## Completion Rule

- [ ] Implementation stayed within allowed paths.
- [ ] No blocked path was modified.
- [ ] All validation commands passed.
- [ ] Product progress was regenerated and checked.
- [ ] CI passed after push.
