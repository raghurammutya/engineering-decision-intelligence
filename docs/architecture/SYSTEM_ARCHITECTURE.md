# System Architecture

## Architecture Summary

Engineering Decision Intelligence is organized around six layers:

1. Event ingestion layer
2. Engineering knowledge graph
3. Drift engine
4. Risk engine
5. Decision engine
6. Materialized views

## 1. Event Ingestion Layer

The ingestion layer discovers observed engineering reality from:

- Git repositories,
- CI/CD workflows,
- deployment systems,
- runtime telemetry,
- observability platforms,
- incident records,
- ownership signals,
- AI-agent execution logs.

Each ingested record should preserve source, timestamp, confidence, and evidence
references.

## 2. Engineering Knowledge Graph

The graph models engineering entities and relationships. It is the central
working model for reality reconciliation.

Initial entities:

- repo,
- service,
- workflow,
- script,
- environment,
- owner,
- evidence,
- deployment,
- incident,
- agent,
- prompt,
- policy.

Initial relationships:

- workflow deploys service,
- script mutates environment,
- service depends on service,
- deployment changes environment,
- deployment correlates with incident,
- owner maintains artifact,
- evidence supports decision,
- agent invokes tool,
- prompt used by agent,
- policy governs capability.

## 3. Drift Engine

The drift engine compares intended policy with observed reality.

Examples:

| Intended | Observed |
| --- | --- |
| approved deploy path | actual deploy path |
| declared owner | active owner |
| retired script | executed script |
| architecture policy | runtime topology |
| safe workflow | unsafe runtime behavior |

The drift engine should classify findings as divergence, not automatically as
violations.

## 4. Risk Engine

The risk engine infers operational, governance, deployment, ownership,
architecture, and AI-autonomy risk.

Initial risk scoring should be deterministic, explainable, and evidence-backed.
Opaque AI scoring is explicitly deferred.

## 5. Decision Engine

The decision engine turns drift and risk into prioritized actions:

- owner review required,
- evidence missing,
- canonical path missing,
- unsafe mutation path,
- stale or orphaned automation,
- duplicate capability,
- blocked production promotion,
- retirement candidate.

## 6. Materialized Views

Generated outputs include:

- registries,
- dashboards,
- audit packs,
- owner queues,
- architecture summaries,
- compliance reports,
- product-owner decision views.

These are generated views over observed reality and policy, not manually
maintained truth.

## First Product Slice

The first slice is Operational State Mutation Reconciliation. It focuses on
workflows, scripts, jobs, and agents that can change operational state.
