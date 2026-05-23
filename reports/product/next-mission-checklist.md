# Autopilot Mission Checklist

Generated: `2026-05-23T04:03:50+00:00`

Mission: `installable-packaging-v1`
Title: Installable Packaging V1
Risk: `medium`
Safe mode: `plan_only`
Product completion delta if completed: `+6.0%`
Projected product completion: `84.0%`

## Safety Boundary

This command selects and explains work. It does not edit files, mutate external systems, or touch blocked paths.

## Allowed Paths

- `tools/**`
- `tests/**`
- `reports/**`
- `docs/mvp/**`
- `roadmap/autopilot-backlog.json`
- `edi/**`
- `pyproject.toml`

## Blocked Paths

- `/home/stocksadmin/workspace/ML/**`

## Acceptance Criteria

- [ ] A minimal Python packaging contract exposes the EDI CLI as an installable console script.
- [ ] Packaging metadata remains lightweight and aligned to the existing CLI.
- [ ] Acceptance gates validate installable packaging metadata.

## Validation Commands

- [ ] `python3 -m edi validate`

## Completion Rule

- [ ] Implementation stayed within allowed paths.
- [ ] No blocked path was modified.
- [ ] All validation commands passed.
- [ ] Product progress was regenerated and checked.
- [ ] CI passed after push.
