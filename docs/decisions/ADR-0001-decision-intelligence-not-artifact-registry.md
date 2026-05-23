# ADR-0001: Decision Intelligence, Not Artifact Registry

## Status

Accepted

## Context

The initiative began from artifact indexing and classification. That is useful
for a pilot, but insufficient as a product foundation. Static registries tend to
become stale because engineering reality changes faster than manually maintained
metadata.

## Decision

The product will be framed as Engineering Decision Intelligence.

Its primary purpose is to detect divergence between intended engineering policy
and observed operational reality, then convert that divergence into
evidence-backed decisions.

## Consequences

- Inventory is supporting infrastructure, not the product.
- Registries and dashboards are generated outputs.
- The knowledge graph and reconciliation engines are core capabilities.
- Product value is measured by decision quality and operational usefulness.
