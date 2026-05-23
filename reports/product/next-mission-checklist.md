# Autopilot Mission Checklist

Generated: `2026-05-23T04:00:36+00:00`

Mission: `multi-repo-onboarding-v1`
Title: Multi-Repo Onboarding V1
Risk: `medium`
Safe mode: `plan_only`
Product completion delta if completed: `+5.0%`
Projected product completion: `78.0%`

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

- [ ] Onboarding metadata describes how a repository is scanned without custom code changes.
- [ ] Generated onboarding outputs include required policy, scan, validation, and report paths.
- [ ] Acceptance gates validate multi-repo onboarding export contracts.

## Validation Commands

- [ ] `python3 -m edi scan ml-pilot`
- [ ] `python3 -m edi validate`

## Completion Rule

- [ ] Implementation stayed within allowed paths.
- [ ] No blocked path was modified.
- [ ] All validation commands passed.
- [ ] Product progress was regenerated and checked.
- [ ] CI passed after push.
