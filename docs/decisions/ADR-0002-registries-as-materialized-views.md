# ADR-0002: Registries As Materialized Views

## Status

Accepted

## Context

Manual registries are useful during exploration but decay as systems change.
The product needs to avoid becoming another stale CMDB or documentation estate.

## Decision

Registries, dashboards, owner queues, and audit packs will be treated as
materialized views generated from event history, graph state, policy, and
evidence.

## Consequences

- The graph and event evidence are closer to truth than markdown tables.
- Generated reports must declare their inputs and generation timestamp.
- Human edits should feed policy, ownership, or exception records rather than
  directly editing generated truth.
- Staleness becomes detectable.
