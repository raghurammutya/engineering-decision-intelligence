# Autopilot Mission Checklist

Generated: `2026-05-23T04:29:19+00:00`

Mission: `agent-discovery-v1`
Title: AI Agent Discovery V1
Risk: `medium`
Safe mode: `plan_only`
Product completion delta if completed: `+2.0%`
Projected product completion: `94.0%`

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

- [ ] Scanner discovers agent, prompt, command, and evaluation artifacts without modifying source repositories.
- [ ] AI-agent artifact counts are materialized in reports and exports.
- [ ] Acceptance gates validate AI-agent discovery contracts.

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
