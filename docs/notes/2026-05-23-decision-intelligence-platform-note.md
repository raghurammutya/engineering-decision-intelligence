# Decision Intelligence Platform Note For EDI Team: 2026-05-23

## Summary

The ML repository now has a Decision Intelligence Platform direction that is closely aligned with EDI, but broader than engineering governance.

The platform framing is:

> Make automated decisions reviewable, replayable, and governable before they become production runtime behavior.

The first wedge is:

```text
Governed Decision Review and Simulation
```

This is a trust surface first, not a generic runtime rewrite, marketplace expansion, no-code builder, or autonomous AI execution layer.

## Why This Matters To EDI

EDI has already proven several patterns that the broader platform should reuse:

- observed-versus-inferred labeling,
- deterministic policy before AI scoring,
- evidence-backed review queues,
- owner review for ambiguous or high-risk cases,
- generated product API/UI views from declared inputs,
- autonomy modes that expand only when evidence improves,
- acceptance packs that prevent readiness overclaiming.

Those patterns are directly useful to the platform, but EDI should remain an engineering-governance domain pack and reference implementation. It should not become the full neutral Decision Intelligence Platform by itself.

## Platform Product Spine

The Decision Intelligence Platform starts with a pre-runtime governance loop:

```text
draft decision spec
  -> attach capability versions
  -> generate capability graph
  -> run policy preflight
  -> run simulation
  -> generate decision diff
  -> request approval
  -> record approval decision
  -> store immutable case evidence
  -> replay or compare later
```

The initial trust surface includes:

- decision spec,
- capability registry,
- capability graph,
- policy preflight,
- simulation evidence,
- decision diff,
- approval record,
- immutable case store,
- lineage and replay evidence.

Runtime integration should follow after these trust surfaces are credible.

## Relationship Between DIP And EDI

| EDI Pattern | DIP Translation |
| --- | --- |
| Operational-state mutation review | Side-effect and production-impact decision review |
| Scanner output | Capability and policy evidence ingestion |
| Owner review queue | Approval queue |
| Observed vs inferred | Declared, observed, inferred, and AI-proposed evidence labels |
| Safe autonomy mode | Decision execution authority level |
| Acceptance pack | Promotion and maturity evidence pack |

EDI asks:

> Where does actual engineering behavior diverge from what we believe, allow, certify, or intend?

DIP generalizes that into:

> What changed in an automated decision, what evidence proves its behavior, who approved it, and can it be replayed later?

## Agentic AI Boundary

The platform carries forward EDI's safety stance:

```text
AI proposes. Policy, approval, and runtime controls decide.
```

AI may help:

- convert intent into decision specs,
- explain diffs and simulations,
- summarize cases,
- suggest capability compositions,
- propose shared context contracts,
- answer governance questions over permissioned evidence.

AI must not:

- bypass policy,
- approve its own generated logic,
- mutate production directly,
- become hidden orchestration glue,
- read shared data without permissioned context contracts,
- execute without lineage, approval, and evidence.

## Marketplace And Shared Context Direction

The marketplace should be a governed capability distribution layer, not just a script or model store.

Capabilities may include:

- models,
- scripts,
- policies,
- transforms,
- connectors,
- workflow templates,
- evaluation packs,
- scoring logic.

Every composed decision must know exactly which capability versions contributed to the result.

Products should collaborate through governed semantic projections, not direct database access or hidden shared state. Shared context must declare purpose, TTL, masking rules, consent or approval requirements, source lineage, freshness, validity, and policy decision evidence.

## What EDI Should Do Next

EDI should stay focused on engineering governance while making its reusable patterns easier for DIP to adopt.

Useful next moves:

1. Keep EDI's evidence labels explicit: observed, inferred, policy-derived, AI-assisted, and user-reviewed.
2. Keep generated views clearly separate from source truth.
3. Treat EDI scanners and policies as candidate DIP capabilities with versions and evidence.
4. Map EDI review queues to the neutral approval queue pattern.
5. Map EDI acceptance packs to service maturity and promotion evidence packs.
6. Preserve deterministic policy as the enforcement authority before AI scoring.
7. Avoid turning EDI into a generic platform shell; let it remain the engineering-governance domain pack.

## Current DIP Artifacts In ML

The current Decision Intelligence Platform docs live in:

```text
/home/stocksadmin/workspace/ML/docs/product/decision-intelligence-platform/
```

Primary reads:

1. `PRODUCT_VISION_AND_FIRST_WEDGE.md`
2. `PRODUCT_SURFACES_AND_UX_WORKFLOWS.md`
3. `GOVERNED_DECISION_REVIEW_AND_SIMULATION_MVP_BLUEPRINT.md`
4. `DECISION_SPEC_SCHEMA_AND_EXAMPLES.md`
5. `marketplace-capability-layer.md`
6. `governed-shared-context-layer.md`

Architecture companion:

```text
/home/stocksadmin/workspace/ML/docs/architecture/DECISION_APPLICATION_FRAMEWORK_NOTE_2026-05-23.md
```

## Main Caution

The architecture is strong, but the product risk is wedge discipline.

Do not turn the first phase into:

- a universal automation platform,
- a broad no-code builder,
- a generic runtime rewrite,
- an unrestricted marketplace,
- direct production AI authority,
- hidden cross-product shared state.

The first win is making automated decision changes understandable, reviewable, simulatable, approvable, and replayable.
