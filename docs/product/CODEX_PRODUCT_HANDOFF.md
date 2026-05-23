# Codex Product Handoff

## Product Positioning

Engineering Decision Intelligence helps teams make engineering systems safer and
more autonomous by continuously turning repository evidence, GitHub events,
scanner inference, policy rules, ownership hints, and generated review workflows
into governed decisions.

The product is a decision and reconciliation system. It is not just an artifact
registry, static documentation repository, dashboard, CMDB, or opaque AI scoring
layer.

The core question is:

```text
Where does actual engineering behavior diverge from what we believe, allow,
certify, or intend?
```

## Current Maturity

| Scope | Status |
| --- | --- |
| v1 MVP | complete |
| v1.5 operationalization | complete |
| v2 operational intelligence | complete |
| v3 operationalization | complete |
| v4 live enforcement readiness | complete |
| v5 secure 1Password tooling | complete |
| v5 live target evidence | blocked |

v1 proves the initial decision loop:

```text
observed repo and GitHub reality
  -> mutation capability candidates
  -> policy reconciliation
  -> risk and autonomy decision
  -> owner review
  -> improved policy/rules
```

v1.5 adds operationalization capabilities:

- agent semantic classifier v2,
- review-state model,
- review workflow exports,
- GitHub pull request event ingestion,
- GitHub Actions run ingestion,
- deployment/event evidence model,
- baseline trend v2,
- scanner tuning pack,
- v1.5 acceptance pack.

v2 moves the product from single-repository operationalization toward
multi-repository, connector-ready, closed-loop operational intelligence. Claims
must remain tied to `reports/product/v2/exports/v2-acceptance-pack.json`; v2
does not imply live runtime enforcement or complete production telemetry.

v3 adds dedicated connector input payloads, reconciliation loops, repeatable
portfolio onboarding, expanded evidence lineage, remediation workflow state,
CI-facing policy preflight, UX surfaces, reusable packaging, external pilot
readiness, and a v3 acceptance pack. Claims must remain tied to
`reports/product/v3/exports/v3-acceptance-pack.json`; v3 still does not imply
autonomous production enforcement.

v4 adds live connector configuration, continuous reconciliation schedules,
CI/PR enforcement policy, remediation operating states, security and access
controls, persistence and history requirements, deployment packaging, SLOs, and
external pilot operation criteria. Claims must remain tied to
`reports/product/v4/exports/v4-acceptance-pack.json`; v4 proves readiness, not
target-system installation.

v5 installs and uses 1Password CLI safely through secret references. It does
not list vaults, list items, or read existing secret values. Claims must remain
tied to `reports/product/v5/exports/v5-acceptance-pack.json`; v5 tooling is
complete, while live target evidence is intentionally incomplete until a user
signs in and runs against real target systems.

## What Another Codex Session Can Use It For

A Codex session can use Engineering Decision Intelligence in two modes.

### Mode 1: Use EDI Directly On A Repository

Use the product to:

- onboard a repository safely,
- scan workflows, scripts, prompts, and agent surfaces,
- generate risk, owner, and review queues,
- identify governance gaps,
- classify AI-agent autonomy risk,
- produce Product API and UI outputs,
- operate through safe autopilot missions.

### Mode 2: Reuse The Safe-Autonomy Pattern

Use the EDI pattern inside another product development process:

- classify actions by autonomy mode,
- require evidence before execution authority expands,
- keep generated outputs separate from source truth,
- fail closed on high-risk uncertainty,
- preserve review and validation evidence,
- expose owner-review and policy-gap queues.

## What Is Observed vs Inferred

EDI combines multiple evidence classes. Do not overstate them.

Observed or directly read:

- repository files,
- local Git state,
- configured policy files,
- generated report manifests,
- GitHub workflow definitions when available,
- GitHub pull request and workflow run data when ingestion is enabled.

Inferred:

- operational-state mutation capability,
- runtime-risk signals,
- owner confidence,
- autonomy mode recommendations,
- prompt or agent capability class,
- scanner-derived deployment or event evidence.

Not fully claimed yet:

- complete live runtime observability,
- complete production topology truth,
- complete secret or environment protection truth,
- complete semantic understanding of all workflow and shell branches,
- autonomous enforcement against external systems.

Preferred wording:

```text
It combines repository evidence, GitHub events, scanner inference, policy rules,
ownership hints, and generated review workflows into decision-ready outputs.
```

Avoid wording that implies full live runtime truth unless a specific connector
or runtime evidence source proves it.

## Read First

Core product documents:

1. `/home/stocksadmin/workspace/engineering-decision-intelligence/docs/vision/PRODUCT_VISION.md`
2. `/home/stocksadmin/workspace/engineering-decision-intelligence/docs/architecture/SYSTEM_ARCHITECTURE.md`
3. `/home/stocksadmin/workspace/engineering-decision-intelligence/docs/development/SAFE_AUTONOMOUS_DEVELOPMENT_ZONE.md`
4. `/home/stocksadmin/workspace/engineering-decision-intelligence/docs/architecture/GITHUB_MANAGEMENT_AND_SAFE_AUTONOMY.md`
5. `/home/stocksadmin/workspace/engineering-decision-intelligence/docs/mvp/ML_PILOT_SCANNER_USAGE.md`
6. `/home/stocksadmin/workspace/engineering-decision-intelligence/docs/roadmap/IMPLEMENTATION_ROADMAP.md`
7. `/home/stocksadmin/workspace/engineering-decision-intelligence/docs/roadmap/V2_OPERATIONAL_INTELLIGENCE_ROADMAP.md`
8. `/home/stocksadmin/workspace/engineering-decision-intelligence/roadmap/v2-operational-intelligence-backlog.json`
9. `/home/stocksadmin/workspace/engineering-decision-intelligence/docs/roadmap/V3_OPERATIONALIZATION_ROADMAP.md`
10. `/home/stocksadmin/workspace/engineering-decision-intelligence/roadmap/v3-operationalization-backlog.json`
11. `/home/stocksadmin/workspace/engineering-decision-intelligence/docs/roadmap/V4_LIVE_ENFORCEMENT_READINESS_ROADMAP.md`
12. `/home/stocksadmin/workspace/engineering-decision-intelligence/roadmap/v4-live-enforcement-readiness-backlog.json`
13. `/home/stocksadmin/workspace/engineering-decision-intelligence/docs/roadmap/V5_TARGET_INSTALLATION_LIVE_EVIDENCE_ROADMAP.md`
14. `/home/stocksadmin/workspace/engineering-decision-intelligence/roadmap/v5-target-installation-live-evidence-backlog.json`

Current product and operator outputs:

15. `/home/stocksadmin/workspace/engineering-decision-intelligence/reports/product/progress.md`
16. `/home/stocksadmin/workspace/engineering-decision-intelligence/reports/product/operator-view.html`
17. `/home/stocksadmin/workspace/engineering-decision-intelligence/reports/product/api-snapshot.json`
18. `/home/stocksadmin/workspace/engineering-decision-intelligence/reports/product/v3/v3-acceptance-pack.md`
19. `/home/stocksadmin/workspace/engineering-decision-intelligence/reports/product/v4/v4-acceptance-pack.md`
20. `/home/stocksadmin/workspace/engineering-decision-intelligence/reports/product/v5/v5-acceptance-pack.md`

ML pilot intelligence reports:

12. `/home/stocksadmin/workspace/engineering-decision-intelligence/reports/ml-pilot/ai-agent-capability-summary.md`
13. `/home/stocksadmin/workspace/engineering-decision-intelligence/reports/ml-pilot/agent-drift-eval-summary.md`
14. `/home/stocksadmin/workspace/engineering-decision-intelligence/reports/ml-pilot/scanner-tuning-pack.md`
15. `/home/stocksadmin/workspace/engineering-decision-intelligence/reports/ml-pilot/agent-semantic-classifier-summary.md`
16. `/home/stocksadmin/workspace/engineering-decision-intelligence/reports/ml-pilot/review-state-summary.md`
17. `/home/stocksadmin/workspace/engineering-decision-intelligence/reports/ml-pilot/review-workflow-summary.md`
18. `/home/stocksadmin/workspace/engineering-decision-intelligence/reports/ml-pilot/github-actions-run-summary.md`
19. `/home/stocksadmin/workspace/engineering-decision-intelligence/reports/ml-pilot/deployment-event-evidence-summary.md`
20. `/home/stocksadmin/workspace/engineering-decision-intelligence/reports/ml-pilot/baseline-trend-v2.md`
21. `/home/stocksadmin/workspace/engineering-decision-intelligence/reports/ml-pilot/v1.5-acceptance-pack.md`

## Useful Commands

Validate the product:

```bash
python3 -m edi validate
```

Scan a repository:

```bash
python3 -m edi scan --repo /path/to/repo --out reports/custom --policy policies/autonomy-policy.json
```

Regenerate the ML pilot:

```bash
python3 -m edi scan ml-pilot
```

Run product self-governance:

```bash
python3 -m edi self-scan
```

Check generated report drift:

```bash
python3 -m edi check-drift
```

Build Product API and UI outputs:

```bash
python3 -m edi api snapshot
python3 -m edi ui build
python3 -m edi v2 build
python3 -m edi v3 build
python3 -m edi v4 build
python3 -m edi v5 build
```

Check product progress and safe autopilot planning:

```bash
python3 -m edi progress --check
python3 -m edi autopilot next --json
python3 -m edi autopilot checklist
```

## Onboarding A New Repository

1. Start in observe/recommend mode.
2. Use a policy file appropriate to the repository.
3. Generate reports into a dedicated output directory.
4. Review blocked and approval-required findings first.
5. Confirm false positives before changing policy.
6. Add owner hints, canonical artifact rules, accepted exceptions, and review
   state only when there is evidence.
7. Re-run validation and drift checks after policy or scanner changes.

Example:

```bash
python3 -m edi scan --repo /path/to/repo --out reports/custom --policy policies/autonomy-policy.json
python3 -m edi validate
```

## Validation Expectations For Codex

Before claiming product changes are safe:

- run `python3 -m edi validate`,
- update generated reports when scanner or policy behavior changes,
- run `python3 -m edi check-drift`,
- keep policy changes separate from scanner implementation changes where
  practical,
- do not treat generated reports as source truth,
- do not expand autonomy without evidence and review.

## What Not To Claim Yet

Do not claim:

- complete live runtime observability,
- production enforcement,
- full workflow semantic parsing,
- complete GitHub/environment protection coverage,
- unbounded safe autonomous execution,
- opaque AI authority over engineering decisions.
- v2 live runtime enforcement or complete production telemetry without observed
  connector evidence.
- v3 autonomous production enforcement or complete live runtime truth from
  imported connector payloads alone.
- v4 target-system credential installation, scheduled connector execution, or
  target-repository PR enforcement without installation evidence.
- v5 live target evidence before `op run` has been executed against dedicated
  target secret references and real target systems.

The current product is strongest when described as:

```text
evidence-backed engineering reality reconciliation with safe-autonomy review
outputs
```

not as a complete runtime control plane.

## Relationship To The Broader Decision Platform

EDI can serve as the first domain application for a broader governed decision
platform. In that model:

- EDI is the engineering-governance domain pack,
- repository and GitHub signals are domain-specific evidence sources,
- safe-autonomy modes are reusable platform primitives,
- generated reports are materialized decision views,
- Product API/UI outputs are early trust surfaces,
- policy reconciliation and review queues become reusable platform patterns.

The neutral platform should still extract broader primitives separately:

- decision spec,
- capability registry,
- capability graph,
- case store,
- policy preflight,
- approval record,
- shared context,
- simulation evidence,
- execution lineage.

EDI should accelerate that platform, not replace the need for neutral product
contracts.
