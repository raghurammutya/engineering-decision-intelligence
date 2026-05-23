# V2 Operational Intelligence Roadmap

Status as of 2026-05-23: planned.

v1 proved the first operational-state mutation decision loop. v1.5 made that
loop usable through safer scanner tuning, review workflows, GitHub event
ingestion, deployment evidence, baseline trends, Product API output, and an
operator view.

v2 moves the product from single-repository operationalization toward
multi-repository, connector-ready, closed-loop operational intelligence.

## Product Objective

Answer this at portfolio level:

```text
Where does observed engineering reality diverge from intended operating policy,
and which decisions require action now?
```

The product should keep registries and dashboards as materialized outputs. The
truth model should come from scanned evidence, connector inputs, policy
contracts, review state, and explicit evidence lineage.

## Operating Principles

- Observed evidence is stronger than manual metadata.
- Scanner inference must stay labeled as inference.
- Deterministic policy decisions come before AI-assisted explanation.
- Generated views are outputs, not sources of truth.
- High-risk uncertainty fails closed into review.
- Governance should activate when risk increases, not for every artifact.
- Connectors must declare source, timestamp, confidence, and failure behavior.

## V2 Slices

| Order | Slice | Purpose | Readiness Signal |
| --- | --- | --- | --- |
| 1 | Multi-repo portfolio model | Make EDI reusable across more than the ML pilot. | A second repository can be represented without custom scanner code. |
| 2 | Observed runtime connector contract | Define runtime evidence boundaries before live telemetry is trusted. | Runtime inputs declare source, timestamp, confidence, and observed-vs-inferred status. |
| 3 | Incident correlation ingestion | Bring alert and incident evidence into decisions. | Incidents correlate to workflows, services, owners, and decisions from fixture inputs. |
| 4 | Closed-loop remediation state | Track findings through review, acceptance, remediation, expiry, and verification. | High-risk findings cannot silently disappear. |
| 5 | Policy-as-code preflight | Check risky changes before execution authority expands. | Blocked, approval-required, and allowed decisions are deterministic and explainable. |
| 6 | Portfolio operator UI | Show cross-repo risk and decision queues. | Operators can see portfolio totals while drilling back to repository evidence. |
| 7 | Trust and confidence scoring | Make uncertainty visible in every decision output. | Low-confidence high-risk decisions route to review. |
| 8 | Evidence lineage model | Explain why each decision exists. | High-risk decisions link to artifacts, policies, evidence, reviews, and gaps. |
| 9 | Connector SDK | Standardize connector contracts for future integrations. | New connectors can be validated without changing core decision logic. |
| 10 | v2 acceptance pack | Prevent readiness overclaiming. | v2 claims are backed by generated evidence and acceptance gates. |

The machine-readable backlog is:

```text
roadmap/v2-operational-intelligence-backlog.json
```

## First Recommended Slice

Start with `multi-repo-portfolio-model-v1`.

Reason:

- It directly tests whether EDI is a reusable product rather than an ML-only
  scanner.
- It can be implemented with static local inputs first.
- It creates the portfolio object needed by later UI, confidence, connector,
  and evidence-lineage work.
- It does not require live runtime or external GitHub writes.

Expected first implementation:

- portfolio manifest schema,
- portfolio loader,
- portfolio summary export,
- Product API section for portfolio counts,
- acceptance gate proving single-repo behavior still works.

## Deferred Until Later

Do not build these during early v2:

- live production enforcement,
- opaque AI risk scoring,
- large UI portal,
- broad connector marketplace,
- automatic remediation against external systems,
- runtime truth claims without observed connector evidence.

## Validation

Use the existing safety loop:

```bash
python3 -m edi validate
python3 -m edi progress --check
python3 -m edi autopilot next --json
```

For v2, the expected starting state is:

```text
v1 MVP: 100%
v1.5 operationalization: 100%
v2 operational intelligence: 0%
```
