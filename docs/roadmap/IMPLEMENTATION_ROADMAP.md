# Implementation Roadmap

## Product Direction

Build a continuous engineering reality reconciliation system. The first
implementation should prove one decision loop end to end before expanding into
broader governance, dashboards, AI reasoning, or enterprise packaging.

## Phase 0: Product Foundation

Status: started.

Required:

- product vision,
- strategic principles,
- architecture decision records,
- initial graph model,
- first MVP charter,
- GitHub/local management capability definition,
- safe-autonomy capability definition,
- ML pilot boundary.

Completion signal:

- product repo exists,
- product direction is documented,
- ML remains a pilot/customer system rather than the product container.

## Phase 1: ML Pilot Discovery

Objective:

Discover workflows and scripts in the ML pilot that can change operational
state.

Build:

- repository scanner for workflows and scripts,
- local Git state scanner,
- GitHub repository and pull request scanner,
- mutation keyword and command detector,
- environment target detector,
- secret-sensitive action detector,
- evidence reference collector,
- owner hint collector.

Outputs:

- raw discovery event records,
- initial graph records,
- local-vs-remote repository state view,
- generated mutation-capability view for the ML pilot.

Do not build:

- polished dashboard,
- broad enterprise ontology,
- AI enforcement,
- deletion automation.

## Phase 2: Deterministic Policy Reconciliation

Objective:

Compare observed mutation paths with intended operating policy.

Build:

- policy rules for environment promotion order,
- canonical promotion-path detection,
- direct production mutation detection,
- branch and environment protection checks,
- pull-request risk annotation rules,
- rollback/evidence-required checks,
- owner-review-required checks,
- severity and confidence model.

Outputs:

- drift findings,
- risk decisions,
- owner review queue,
- safe-autonomy recommendation per mutation path,
- evidence gap report.

Completion signal:

- the system can answer which ML workflows/scripts can mutate operational state,
  whether each path is canonical, and what action is required.

## Phase 3: Materialized Views

Objective:

Generate human-usable outputs from graph and policy state.

Build:

- markdown registry generator,
- CSV export generator,
- audit pack generator,
- product-owner summary generator,
- engineering remediation queue.

Principle:

Generated views must declare inputs, generation timestamp, and whether they are
derived from observed evidence or human policy.

## Phase 4: Self-Governance

Objective:

Apply the platform's own rules to itself.

Build:

- scanner registry,
- policy registry,
- generated-view manifest,
- rule coverage report,
- automation mutation review for this repository.

Completion signal:

- the platform can explain its own scanners, rules, generated outputs, and
  evidence boundaries.

## Phase 5: Runtime And Delivery Correlation

Objective:

Move beyond static repo discovery into live operational truth.

Build:

- CI/CD event ingestion,
- deployment event ingestion,
- incident/alert ingestion,
- runtime topology hooks,
- expected-vs-observed deploy path reconciliation.

Outputs:

- deployment-risk findings,
- runtime drift findings,
- incident-correlation views.

## Phase 6: AI-Agent Intelligence

Objective:

Treat AI agents as runtime systems with capabilities, permissions, tools,
prompts, memory scopes, and evaluation evidence.

Build:

- agent capability model,
- tool permission scanner,
- prompt lineage scanner,
- evaluation coverage mapper,
- AI autonomy risk rules.

Constraint:

Govern runtime safety, permissions, and outcomes. Do not over-govern reasoning
style, experimentation, or early prompt exploration.

## Phase 6A: Safe Autonomy Controls

Objective:

Convert risk decisions into autonomy decisions for engineering automation and
AI agents.

Build:

- autonomy mode model,
- tool permission registry,
- guarded execution policy,
- approval and evidence requirements by risk tier,
- audit trail for autonomous actions,
- fail-closed behavior for high-risk uncertainty.

Outputs:

- autonomy recommendation per workflow, script, and agent,
- blocked-action reasons,
- owner-approval queue,
- execution evidence records.

## Phase 7: Productization

Objective:

Package the system for reuse beyond the ML pilot.

Build:

- installable CLI,
- configurable policy packs,
- connector interface,
- graph storage backend abstraction,
- documentation generator,
- enterprise deployment model.

Completion signal:

- a second repository or project can be onboarded without rewriting the core
  scanner, graph, rule, or reporting model.

## Immediate Next Actions

1. Define the initial event record format.
2. Define the initial graph storage format for the MVP.
3. Build a workflow scanner for GitHub Actions.
4. Build a script scanner for shell and Python automation.
5. Build a local Git state scanner.
6. Build a GitHub repository and pull request scanner.
7. Build deterministic mutation classification rules.
8. Encode the ML pilot promotion policy.
9. Generate the first ML operational-state mutation view.
10. Assign safe-autonomy modes to each mutation path.
11. Compare generated results with the existing ML workflow and script
    registries.
12. Add owner-review states.
13. Document false positives and missing signals.
