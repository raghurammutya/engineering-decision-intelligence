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

After installation from this repository, the same CLI is exposed as:

```bash
edi scan ml-pilot
```

Use `python3 -m edi self-scan` to regenerate product self-governance reports.
Use `python3 -m edi check-drift` to verify committed reports still match
scanner and policy sources.
Use `python3 -m edi validate` to run the local safe validation chain.
Use `python3 -m edi api snapshot` to materialize `reports/product/api-snapshot.json`.
Use `python3 -m edi ui build` to materialize `reports/product/operator-view.html`.

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
| `reports/ml-pilot/owner-confidence-map.md` | Owner assignment confidence and review classes |
| `reports/ml-pilot/autonomy-mode-summary.md` | Autonomy mode counts and samples |
| `reports/ml-pilot/repository-state-summary.md` | Local/GitHub repository state summary |
| `reports/ml-pilot/github-protection-findings.md` | Branch/environment protection decisions |
| `reports/ml-pilot/cicd-event-summary.md` | CI/CD workflow event surfaces and deployment-capable workflow split |
| `reports/ml-pilot/runtime-signal-summary.md` | Inferred runtime-risk signals grouped by environment and mutation type |
| `reports/ml-pilot/telemetry-correlation-summary.md` | Runtime, CI/CD, owner, and evidence correlation gaps |
| `reports/ml-pilot/ai-agent-capability-summary.md` | AI-agent, prompt, command, and evaluation capability boundaries |
| `reports/ml-pilot/agent-drift-eval-summary.md` | AI-agent drift and evaluation coverage review queue |
| `reports/ml-pilot/agent-semantic-classifier-summary.md` | AI-agent semantic class and direct versus prompted capability claims |
| `reports/ml-pilot/review-state-summary.md` | Deterministic review states, expiry needs, and owner/evidence actions |
| `reports/ml-pilot/review-workflow-summary.md` | Queueable review workflow lanes and status transitions |
| `reports/ml-pilot/github-pr-event-summary.md` | GitHub PR event ingestion and changed-file risk priorities |
| `reports/ml-pilot/github-actions-run-summary.md` | GitHub Actions run ingestion and deployment-like run detection |
| `reports/ml-pilot/deployment-event-evidence-summary.md` | Deployment-event evidence correlation candidates |
| `reports/ml-pilot/baseline-trend-v2.md` | Baseline trend deltas and blocked-path movement |
| `reports/ml-pilot/v1.5-acceptance-pack.md` | v1.5 operationalization acceptance state |
| `reports/ml-pilot/policy-pack-summary.md` | Reusable scanner policy-pack metadata |
| `reports/ml-pilot/onboarding-summary.md` | Repository onboarding command, inputs, validations, and generated reports |
| `reports/ml-pilot/policy-coverage-report.md` | Policy coverage and gap report |
| `reports/ml-pilot/evidence-quality-map.md` | Evidence quality by artifact |
| `reports/ml-pilot/risk-explanation-map.md` | Rule-level reasons for risk and autonomy classification |
| `reports/ml-pilot/executive-decision-summary.md` | Calibrated priority summary |
| `reports/ml-pilot/finding-family-summary.md` | Family-grouped operational risk summary |
| `reports/ml-pilot/decision-insight-clusters.md` | Top decision clusters, scanner tuning candidates, and operational blockers |
| `reports/ml-pilot/scanner-tuning-pack.md` | False-positive review pack and suggested policy tuning actions |
| `reports/ml-pilot/remediation-playbook-map.md` | Mapping from findings to standard remediation playbooks |
| `reports/ml-pilot/pr-risk-summary.md` | Pull request risk summary |
| `reports/ml-pilot/graph/entities.json` | Knowledge graph entities |
| `reports/ml-pilot/graph/relationships.json` | Knowledge graph relationships |
| `reports/ml-pilot/graph/backend.json` | Graph backend metadata and JSON contract compatibility |
| `reports/ml-pilot/exports/owner-backlog.json` | Machine-readable owner backlog |
| `reports/ml-pilot/exports/owner-backlog.csv` | Spreadsheet-friendly owner backlog |
| `reports/ml-pilot/exports/owner-workflows.json` | Owner workflow records with assignment confidence |
| `reports/ml-pilot/exports/cicd-events.json` | Workflow event records for CI/CD decision ingestion |
| `reports/ml-pilot/exports/runtime-signals.json` | Inferred runtime signal records for later telemetry reconciliation |
| `reports/ml-pilot/exports/telemetry-correlations.json` | Runtime signal correlations with CI/CD, owner, and evidence dimensions |
| `reports/ml-pilot/exports/ai-agent-capabilities.json` | Machine-readable AI-agent capability and safety-status records |
| `reports/ml-pilot/exports/agent-drift-evals.json` | Machine-readable AI-agent drift and evaluation records |
| `reports/ml-pilot/exports/agent-semantic-classifier.json` | Machine-readable AI-agent semantic classifier records |
| `reports/ml-pilot/exports/review-state.json` | Machine-readable review-state records |
| `reports/ml-pilot/exports/review-workflows.json` | Machine-readable review workflow records |
| `reports/ml-pilot/exports/github-pr-events.json` | Machine-readable GitHub PR event records |
| `reports/ml-pilot/exports/github-actions-runs.json` | Machine-readable GitHub Actions run records |
| `reports/ml-pilot/exports/deployment-event-evidence.json` | Machine-readable deployment evidence correlation records |
| `reports/ml-pilot/exports/baseline-trend-v2.json` | Machine-readable baseline trend v2 payload |
| `reports/ml-pilot/exports/v1.5-acceptance-pack.json` | Machine-readable v1.5 acceptance pack |
| `reports/ml-pilot/exports/policy-pack.json` | Reusable scanner policy-pack metadata for productization |
| `reports/ml-pilot/exports/onboarding.json` | Machine-readable repository onboarding contract |
| `reports/ml-pilot/exports/executive-decisions.json` | Executive decision summary for dashboards/API |
| `reports/ml-pilot/exports/decision-clusters.json` | Machine-readable decision clusters and blocker/tuning split |
| `reports/ml-pilot/exports/scanner-tuning-pack.json` | Machine-readable false-positive review and scanner tuning pack |
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
