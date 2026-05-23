# ML Pilot Scanner Usage

## Purpose

The first prototype scanner generates an Operational State Mutation Registry for
the ML pilot repository.

It detects candidate workflows and scripts that may change operational state,
then assigns:

- mutation type,
- environment exposure,
- risk level,
- autonomy mode,
- canonical status,
- owner status,
- evidence status,
- blocked claims,
- next action.

## Run

```bash
python3 tools/operational_state_scan.py \
  --repo /home/stocksadmin/workspace/ML \
  --out reports/ml-pilot \
  --github
```

The `--github` flag enriches the report with GitHub repository, pull request,
and workflow state through the GitHub CLI when available.

## Generated Files

| File | Purpose |
| --- | --- |
| `reports/ml-pilot/operational-state-mutation-registry.md` | Product-owner and engineering-readable registry |
| `reports/ml-pilot/operational-state-mutation-registry.csv` | Spreadsheet-friendly registry |
| `reports/ml-pilot/findings.jsonl` | Machine-readable finding records |
| `reports/ml-pilot/manifest.json` | Generation metadata, counts, local Git state, GitHub state |

## Current Limitations

This is a heuristic scanner. It intentionally favors surfacing risk candidates
over suppressing possible operational mutation paths.

Known limitations:

- It does not fully parse GitHub Actions YAML semantics.
- It does not execute scripts or resolve dynamic shell branches.
- It can classify validation/reporting scripts as operationally relevant when
  they mention production, database, config, broker, or deployment terms.
- Owner detection is based on local textual hints, not CODEOWNERS enforcement.
- Evidence detection is based on references, not proof quality.
- GitHub branch/environment protection checks are not fully implemented yet.

## How To Use The First Report

Use the report as an owner-review queue:

1. Start with `blocked` autonomy paths.
2. Confirm whether each path can actually mutate operational state.
3. Mark canonical paths and accepted exceptions.
4. Attach owner and evidence references.
5. Convert false positives into rule improvements.
6. Re-run the scanner and compare the materialized view.

## Product Learning Goal

The first learning goal is not perfect classification. The first learning goal
is proving that the system can create a useful decision loop:

```text
observed repo and GitHub reality
  -> mutation capability candidates
  -> policy reconciliation
  -> risk and autonomy decision
  -> owner review
  -> improved policy/rules
```
