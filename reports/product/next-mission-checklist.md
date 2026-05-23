# Autopilot Mission Checklist

Generated: `2026-05-23T02:38:40+00:00`

Mission: `graph-v2-decision-relationships`
Title: Graph v2 + Decision Relationships
Risk: `medium`
Safe mode: `plan_only`
Product completion delta if completed: `+6.0%`
Projected product completion: `21.0%`

## Safety Boundary

This command selects and explains work. It does not edit files, mutate external systems, or touch blocked paths.

## Allowed Paths

- `tools/operational_state_scan.py`
- `tests/**`
- `reports/**`
- `docs/schemas/**`
- `roadmap/autopilot-backlog.json`

## Blocked Paths

- `/home/stocksadmin/workspace/ML/**`

## Acceptance Criteria

- [ ] Graph includes policy, control, evidence, and decision nodes.
- [ ] Relationships include violates_policy, requires_evidence, suggested_owner, and blocked_by_control.
- [ ] Graph schema expectations are covered by tests.

## Validation Commands

- [ ] `python3 -m edi scan ml-pilot`
- [ ] `python3 -m edi self-scan`
- [ ] `python3 -m edi validate`

## Completion Rule

- [ ] Implementation stayed within allowed paths.
- [ ] No blocked path was modified.
- [ ] All validation commands passed.
- [ ] Product progress was regenerated and checked.
- [ ] CI passed after push.
