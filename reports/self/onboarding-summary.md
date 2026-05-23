# Repository Onboarding Summary

Generated: `2026-05-23T05:32:41+00:00`

Repository: `/home/stocksadmin/workspace/engineering-decision-intelligence`
Output directory: `reports/self`
Custom code required: `False`
Onboarding contract: `repo_path + policy files + output directory`

## Scan Command

```bash
python3 tools/operational_state_scan.py --repo /home/stocksadmin/workspace/engineering-decision-intelligence --out reports/self --policy policies/autonomy-policy.json --include-tools --github-baseline policies/github-control-baseline.json
```

## Required Inputs

| Input | Value |
| --- | --- |
| `repo_path` | `/home/stocksadmin/workspace/engineering-decision-intelligence` |
| `policy_path` | `policies/autonomy-policy.json` |
| `github_enabled` | `False` |
| `include_tools` | `True` |
| `github_baseline_path` | `policies/github-control-baseline.json` |
| `owner_suggestions_path` | `none` |
| `control_remediation_path` | `none` |
| `false_positive_review_path` | `none` |

## Validation Commands

- `python3 -m edi validate`
- `python3 -m edi progress --check`

## Generated Reports

- `reports/self/README.md`
- `reports/self/findings.jsonl`
- `reports/self/operational-state-mutation-registry.csv`
- `reports/self/operational-state-mutation-registry.md`
- `reports/self/decision-backlog.md`
- `reports/self/owner-review-queue.md`
- `reports/self/owner-confidence-map.md`
- `reports/self/autonomy-mode-summary.md`
- `reports/self/repository-state-summary.md`
- `reports/self/github-protection-findings.md`
- `reports/self/github-control-baseline-assessment.md`
- `reports/self/cicd-event-summary.md`
- `reports/self/runtime-signal-summary.md`
- `reports/self/telemetry-correlation-summary.md`
- `reports/self/ai-agent-capability-summary.md`
- `reports/self/agent-drift-eval-summary.md`
- `reports/self/agent-semantic-classifier-summary.md`
- `reports/self/review-state-summary.md`
- `reports/self/review-workflow-summary.md`
- `reports/self/github-pr-event-summary.md`
- `reports/self/github-actions-run-summary.md`
- `reports/self/deployment-event-evidence-summary.md`
- `reports/self/baseline-trend-v2.md`
- `reports/self/v1.5-acceptance-pack.md`
- `reports/self/policy-pack-summary.md`
- `reports/self/onboarding-summary.md`
- `reports/self/control-remediation-tracker.md`
- `reports/self/policy-coverage-report.md`
- `reports/self/evidence-quality-map.md`
- `reports/self/risk-explanation-map.md`
- `reports/self/executive-decision-summary.md`
- `reports/self/finding-family-summary.md`
- `reports/self/decision-insight-clusters.md`
- `reports/self/false-positive-candidates.md`
- `reports/self/scanner-tuning-pack.md`
- `reports/self/owner-assignment-plan.md`
- `reports/self/remediation-playbook-map.md`
- `reports/self/drift-from-baseline.md`
- `reports/self/pr-risk-summary.md`
- `reports/self/graph/entities.json`
- `reports/self/graph/relationships.json`
- `reports/self/graph/backend.json`
- `reports/self/exports/owner-backlog.json`
- `reports/self/exports/owner-backlog.csv`
- `reports/self/exports/owner-workflows.json`
- `reports/self/exports/cicd-events.json`
- `reports/self/exports/runtime-signals.json`
- `reports/self/exports/telemetry-correlations.json`
- `reports/self/exports/ai-agent-capabilities.json`
- `reports/self/exports/agent-drift-evals.json`
- `reports/self/exports/agent-semantic-classifier.json`
- `reports/self/exports/review-state.json`
- `reports/self/exports/review-workflows.json`
- `reports/self/exports/github-pr-events.json`
- `reports/self/exports/github-actions-runs.json`
- `reports/self/exports/deployment-event-evidence.json`
- `reports/self/exports/baseline-trend-v2.json`
- `reports/self/exports/v1.5-acceptance-pack.json`
- `reports/self/exports/policy-pack.json`
- `reports/self/exports/onboarding.json`
- `reports/self/exports/executive-decisions.json`
- `reports/self/exports/decision-clusters.json`
- `reports/self/exports/scanner-tuning-pack.json`
- `reports/self/exports/remediation-packs.json`
- `reports/self/baseline-history/latest.json`
- `reports/self/manifest.json`
