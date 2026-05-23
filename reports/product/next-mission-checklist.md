# Autopilot Mission Checklist

Generated: `2026-05-23T03:01:08+00:00`

Mission: `ml-pilot-insight-clustering`
Title: ML Pilot Insight Clustering
Risk: `medium`
Safe mode: `plan_only`
Product completion delta if completed: `+5.0%`
Projected product completion: `36.0%`

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

- [ ] The 487 ML pilot findings are grouped into top decision clusters.
- [ ] Likely scanner tuning candidates are separated from likely operational blockers.
- [ ] Top remediation packs are ranked by risk reduction.

## Validation Commands

- [ ] `python3 -m edi scan ml-pilot`
- [ ] `python3 -m edi validate`

## Completion Rule

- [ ] Implementation stayed within allowed paths.
- [ ] No blocked path was modified.
- [ ] All validation commands passed.
- [ ] Product progress was regenerated and checked.
- [ ] CI passed after push.
