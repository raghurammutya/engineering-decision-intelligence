# Engineering Decision Intelligence

Engineering Decision Intelligence is a product initiative for continuously
reconciling intended engineering policy with observed operational reality.

The core question is not "what artifacts exist?"

The core question is:

> Where does actual engineering behavior diverge from what we believe, allow,
> certify, or intend?

This repository holds the reusable product vision, architecture, schemas,
decision records, and implementation roadmap. The existing ML system is the
first pilot/customer system, not the product itself.

## Product Thesis

Continuously detect divergence between intended engineering policy and observed
operational reality, then turn that divergence into evidence-backed decisions.

## First MVP

Operational State Mutation Reconciliation:

> Which workflows, scripts, agents, jobs, or automations can change operational
> state, and are they canonical, owner-approved, evidenced, and safe?

Operational state includes deployments, database mutation, infrastructure
changes, broker/order writes, queue mutation, configuration mutation, secret
usage, runtime shell execution, and AI-agent tool execution.

## Current Prototype

The first prototype scanner is:

```bash
python3 -m edi scan ml-pilot
python3 -m edi scan --repo /path/to/repo --out reports/custom --policy policies/autonomy-policy.json
python3 -m edi self-scan
python3 -m edi check-drift
python3 -m edi progress
python3 -m edi validate
```

It generates:

- `reports/ml-pilot/operational-state-mutation-registry.md`
- `reports/ml-pilot/operational-state-mutation-registry.csv`
- `reports/ml-pilot/findings.jsonl`
- `reports/ml-pilot/manifest.json`
- `reports/ml-pilot/decision-backlog.md`
- `reports/ml-pilot/owner-review-queue.md`
- `reports/ml-pilot/autonomy-mode-summary.md`
- `reports/ml-pilot/repository-state-summary.md`
- `reports/ml-pilot/github-protection-findings.md`
- `reports/ml-pilot/policy-coverage-report.md`
- `reports/ml-pilot/evidence-quality-map.md`
- `reports/ml-pilot/risk-explanation-map.md`
- `reports/ml-pilot/executive-decision-summary.md`
- `reports/ml-pilot/finding-family-summary.md`
- `reports/ml-pilot/remediation-playbook-map.md`
- `reports/ml-pilot/pr-risk-summary.md`
- `reports/ml-pilot/graph/entities.json`
- `reports/ml-pilot/graph/relationships.json`
- `reports/product/progress.md`
- `reports/product/progress.json`

The generated registry is a materialized view. Treat it as decision support and
review input, not authoritative truth.

## Repository Structure

```text
docs/
  vision/          Product vision and strategic principles
  architecture/    System architecture and graph model
  mvp/             Initial operational slice and acceptance criteria
  decisions/       Architecture decision records
  schemas/         Entity, relationship, and risk model drafts
  examples/        Pilot and reference-system notes
  notes/           Dated strategy notes and discussion captures
```

## Current Product Boundary

- This repository is the reusable product/system.
- The ML repository is the first pilot/reference implementation.
- Registries and dashboards are generated materialized views, not primary
  sources of truth.
- Deterministic, explainable policy must precede AI-assisted scoring for safety
  and enforcement decisions.
