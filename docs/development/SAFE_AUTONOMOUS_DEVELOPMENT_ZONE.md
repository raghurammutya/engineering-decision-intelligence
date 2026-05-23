# Safe Autonomous Development Zone

## Purpose

This repository should allow fast autonomous development while preventing silent
changes to safety, policy, and autonomy behavior.

The goal is not to remove human control. The goal is to make routine work more
autonomous while keeping high-risk changes visible, tested, and reviewable.

## Current Safety Rails

| Rail | Status |
| --- | --- |
| Policy-as-code | `policies/*.json` |
| Scanner regression tests | `tests/test_operational_state_scan.py` |
| CI workflow | `.github/workflows/ci.yml` |
| Product self-scan | CI smoke test with `--include-tools` |
| Generated report manifest | `reports/ml-pilot/manifest.json` |
| Deterministic autonomy modes | `observe`, `recommend`, `prepare`, `controlled_execute`, `blocked` |

## Development Autonomy Lanes

| Area | Default Autonomy |
| --- | --- |
| Product docs | `guarded_execute` |
| Generated reports | `guarded_execute` |
| Scanner code | `controlled_execute` |
| Policy files | `controlled_execute` |
| GitHub settings | `recommend` |
| Deletion/cleanup | `blocked` |
| Release publishing | `blocked` |

## Required Validation

Before scanner or policy changes are merged:

```bash
python3 -m py_compile tools/operational_state_scan.py
python3 -m unittest discover -s tests -p "test_*.py"
python3 -m json.tool policies/autonomy-policy.json >/dev/null
python3 -m json.tool policies/ml-pilot-policy.json >/dev/null
python3 tools/operational_state_scan.py \
  --repo "$PWD" \
  --out /tmp/edi-self-scan \
  --policy policies/autonomy-policy.json \
  --include-tools
```

## Safe Expansion Path

1. Add tests before changing risk or autonomy logic.
2. Keep policy changes separate from scanner implementation changes where
   practical.
3. Regenerate materialized views after policy changes.
4. Treat generated views as review artifacts, not source truth.
5. Require human review for anything that changes autonomy from `blocked` or
   `prepare` toward execution.

## Blocked Without Explicit Approval

- deleting repository files,
- changing GitHub branch protection,
- changing GitHub secrets or environments,
- mutating the ML pilot repository,
- triggering deployment workflows,
- publishing releases,
- adding autonomous execution against external systems.
