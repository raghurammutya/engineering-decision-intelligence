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
python3 -m edi scan ml-pilot
```

Use `python3 -m edi self-scan` to regenerate product self-governance reports.
Use `python3 -m edi check-drift` to verify committed reports still match
scanner and policy sources.
Use `python3 -m edi validate` to run the local safe validation chain.

For non-preset repositories:

```bash
python3 -m edi scan --repo /path/to/repo --out reports/custom --policy policies/autonomy-policy.json
```

## Generated Files

| File | Purpose |
| --- | --- |
| `reports/ml-pilot/operational-state-mutation-registry.md` | Product-owner and engineering-readable registry |
| `reports/ml-pilot/operational-state-mutation-registry.csv` | Spreadsheet-friendly registry |
| `reports/ml-pilot/findings.jsonl` | Machine-readable finding records |
| `reports/ml-pilot/manifest.json` | Generation metadata, counts, local Git state, GitHub state |
| `reports/ml-pilot/decision-backlog.md` | Prioritized action backlog |
| `reports/ml-pilot/owner-review-queue.md` | Owner-focused review queue |
| `reports/ml-pilot/autonomy-mode-summary.md` | Autonomy mode counts and samples |
| `reports/ml-pilot/repository-state-summary.md` | Local/GitHub repository state summary |
| `reports/ml-pilot/github-protection-findings.md` | Branch/environment protection decisions |
| `reports/ml-pilot/policy-coverage-report.md` | Policy coverage and gap report |
| `reports/ml-pilot/evidence-quality-map.md` | Evidence quality by artifact |
| `reports/ml-pilot/risk-explanation-map.md` | Rule-level reasons for risk and autonomy classification |
| `reports/ml-pilot/executive-decision-summary.md` | Calibrated priority summary |
| `reports/ml-pilot/finding-family-summary.md` | Family-grouped operational risk summary |
| `reports/ml-pilot/remediation-playbook-map.md` | Mapping from findings to standard remediation playbooks |
| `reports/ml-pilot/pr-risk-summary.md` | Pull request risk summary |
| `reports/ml-pilot/graph/entities.json` | Knowledge graph entities |
| `reports/ml-pilot/graph/relationships.json` | Knowledge graph relationships |
| `reports/ml-pilot/exports/owner-backlog.json` | Machine-readable owner backlog |
| `reports/ml-pilot/exports/owner-backlog.csv` | Spreadsheet-friendly owner backlog |
| `reports/ml-pilot/exports/executive-decisions.json` | Executive decision summary for dashboards/API |
| `reports/ml-pilot/exports/remediation-packs.json` | Remediation packs grouped by action lane |

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
