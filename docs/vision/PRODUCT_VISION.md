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
- engineering leaders who need delivery and governance visibility,
- architecture teams who need drift detection,
- audit and compliance teams who need evidence-backed traceability.

## First Pilot

The first pilot is the ML system. The first product slice is Operational State
Mutation Reconciliation:

> Which workflows, scripts, agents, jobs, or automations can change operational
> state, and are they canonical, owner-approved, evidenced, and safe?
