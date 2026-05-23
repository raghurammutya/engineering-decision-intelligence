# Strategic Principles

## 1. Reconciliation Is The Product Spine

Every major capability should help reconcile intended engineering policy with
observed operational reality.

If a feature does not improve reconciliation, decision quality, evidence
quality, or operational actionability, defer it.

## 2. Reality First

The system should learn primarily from machine-observed truth:

- Git,
- CI/CD,
- deployment events,
- runtime telemetry,
- logs and traces,
- incidents,
- ownership signals,
- AI-agent execution records.

Humans approve, explain, override, and govern. Humans should not be the primary
maintenance mechanism for inventory.

## 3. Registries Are Materialized Views

Registries, dashboards, reports, and audit packs are outputs generated from the
graph and event history. They are not the canonical source of truth.

## 4. Detect Divergence Before Judging It

Divergence is not automatically failure. Some teams intentionally deviate for
valid reasons. The system should first detect and explain divergence, then route
it through risk-appropriate review.

## 5. Deterministic Enforcement First

Policy enforcement, safety gates, production mutation controls, and deletion
recommendations should be deterministic and evidence-backed before any AI
assistance is introduced.

AI can help with summarization, clustering, semantic grouping, duplicate
suggestions, and human-readable explanations.

## 6. Adaptive Governance

Governance should activate according to risk:

| Risk Level | Governance |
| --- | --- |
| Low | lightweight metadata |
| Medium | owner review |
| High | evidence required |
| Critical | controlled admission |

## 7. Small Ontology First

Start with the smallest useful graph:

- repo,
- service,
- workflow,
- script,
- environment,
- owner,
- evidence,
- deployment,
- incident,
- agent.

Expand only when a new entity or relationship improves decisions.

## 8. Self-Governance

The platform must apply its own principles to itself. Its scanners, policies,
rules, generated views, AI assistance, and automation must be discoverable,
versioned, evidenced, and owner-reviewable.
