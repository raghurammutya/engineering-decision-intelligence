# Product Vision

## Name

Engineering Decision Intelligence

## Thesis

Continuously detect divergence between intended engineering policy and observed
operational reality, then turn that divergence into evidence-backed decisions.

## Problem

Engineering organizations accumulate workflows, scripts, services, deployment
paths, runtime dependencies, prompts, agents, evidence, and process documents
faster than humans can govern them manually.

Traditional approaches fail because metadata decays:

- CMDB records go stale.
- Architecture diagrams drift from runtime behavior.
- Registries become manually maintained inventory.
- Governance processes become broad, slow, and easy to bypass.
- Dashboards show data but do not identify decisions.

The failure mode is not lack of documentation. The failure mode is that observed
engineering reality no longer matches intended operating policy.

## Product

Engineering Decision Intelligence is a continuous reconciliation system for
engineering organizations.

It ingests engineering reality from source control, CI/CD, deployments,
telemetry, incidents, ownership signals, and AI-agent execution. It models that
reality in a knowledge graph, compares it with intended policy, detects drift,
infers risk, and produces prioritized decisions.

## Primary Question

Where does actual engineering behavior diverge from what we believe, allow,
certify, or intend?

## What The Product Is Not

- It is not a static artifact inventory.
- It is not a documentation repository.
- It is not a conventional CMDB.
- It is not dashboard-first governance.
- It is not an opaque AI scoring system.

## What The Product Produces

- drift findings,
- risk decisions,
- owner review queues,
- local and GitHub repository management intelligence,
- safe-autonomy controls for engineering agents and automation,
- evidence-backed remediation items,
- generated registries,
- generated audit packs,
- generated dashboards,
- architecture and operational intelligence views.

These outputs are materialized views over observed reality and policy. They are
not the authoritative source of truth.

## Initial Target User

- product owners who need risk and decision clarity,
- IT and platform specialists who need operational control,
- repository administrators who need local and GitHub governance visibility,
- engineering leaders who need delivery and governance visibility,
- architecture teams who need drift detection,
- agent and automation owners who need safe autonomy boundaries,
- audit and compliance teams who need evidence-backed traceability.

## First-Class Capabilities

### GitHub And Local Repository Management

The product must understand both local repository reality and GitHub-hosted
reality:

- local worktrees, branches, uncommitted changes, generated files, and scripts,
- GitHub repositories, branches, pull requests, issues, workflows, releases,
  environments, secrets references, branch protection, and code owners,
- divergence between local state and remote state,
- governance gaps such as unprotected deploy branches, risky workflows,
  orphaned repositories, and stale pull requests.

This capability should help users manage engineering systems where work happens:
locally during development and remotely in GitHub during collaboration,
review, automation, and release.

### Safe But Autonomous Engineering

The product should make engineering more autonomous without making it unsafe.

Autonomy should increase when evidence, policy, ownership, tests, rollback,
and operational boundaries are strong. Autonomy should narrow when risk,
ambiguity, missing evidence, or production mutation capability increases.

The intended model is not manual approval for everything. The intended model is
risk-based autonomy with clear controls, auditability, and fail-closed behavior
for high-risk actions.

## First Pilot

The first pilot is the ML system. The first product slice is Operational State
Mutation Reconciliation:

> Which workflows, scripts, agents, jobs, or automations can change operational
> state, and are they canonical, owner-approved, evidenced, and safe?
