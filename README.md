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

Start here when handing the product to another Codex session or product team:

- `docs/product/CODEX_PRODUCT_HANDOFF.md`
- `docs/roadmap/V2_OPERATIONAL_INTELLIGENCE_ROADMAP.md`
- `roadmap/v2-operational-intelligence-backlog.json`
- `docs/roadmap/V3_OPERATIONALIZATION_ROADMAP.md`
- `roadmap/v3-operationalization-backlog.json`
- `docs/roadmap/V4_LIVE_ENFORCEMENT_READINESS_ROADMAP.md`
- `roadmap/v4-live-enforcement-readiness-backlog.json`
- `docs/roadmap/V5_TARGET_INSTALLATION_LIVE_EVIDENCE_ROADMAP.md`
- `roadmap/v5-target-installation-live-evidence-backlog.json`

The first prototype scanner is:

```bash
python3 -m edi scan ml-pilot
python3 -m edi scan --repo /path/to/repo --out reports/custom --policy policies/autonomy-policy.json
python3 -m edi self-scan
python3 -m edi check-drift
python3 -m edi progress
python3 -m edi autopilot next
python3 -m edi autopilot next --json
python3 -m edi autopilot checklist
python3 -m edi v2 build
python3 -m edi v3 build
python3 -m edi v4 build
python3 -m edi v5 build
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
- `reports/product/next-mission-checklist.md`
- `reports/product/next-mission.json`

The generated registry is a materialized view. Treat it as decision support and
review input, not authoritative truth.

## Repository Structure

```text
docs/
  vision/          Product vision and strategic principles
  architecture/    System architecture and graph model
  mvp/             Initial operational slice and acceptance criteria
  product/         Product handoff and cross-team usage notes
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

## Current Roadmap State

- v1 MVP: complete.
- v1.5 operationalization: complete.
- v2 operational intelligence: complete.
- v3 operationalization: complete.
- v4 live enforcement readiness: complete.
- v5 secure 1Password tooling: complete.
- v5 live target evidence: blocked until target-system installation evidence
  exists.

v2 moves the product toward multi-repository portfolio intelligence,
connector-ready runtime and incident evidence contracts, closed-loop
remediation, policy preflight, confidence scoring, evidence lineage, and a v2
acceptance pack. The initial v2 operational intelligence pack is complete when
`reports/product/v2/exports/v2-acceptance-pack.json` reports `pass`.

v3 adds dedicated connector input payloads, reconciliation loop summaries,
repeatable portfolio onboarding, expanded evidence lineage, remediation
workflow state, CI-facing policy preflight, product UX surfaces, reusable
packaging evidence, external pilot readiness, and a v3 acceptance pack. The
initial v3 operationalization pack is complete when
`reports/product/v3/exports/v3-acceptance-pack.json` reports `pass`.

v4 adds live connector configuration, continuous reconciliation schedules,
CI/PR enforcement policy, remediation operating states, security and access
controls, persistence and history requirements, deployment packaging, SLOs,
external pilot operation criteria, and a v4 acceptance pack. It is a readiness
pack: target credentials, scheduled connector execution, target-repo PR checks,
and production enforcement still require installation evidence.

v5 adds 1Password-backed secret reference tooling. The CLI is installed and the
repo contains only `op://` references and templates, not resolved secret values.
Live claims remain blocked until you sign in, create a dedicated EDI vault or
Environment, run with `op run`, and provide target-system evidence.
