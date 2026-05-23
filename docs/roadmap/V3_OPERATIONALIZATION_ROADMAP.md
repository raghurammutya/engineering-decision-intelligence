# V3 Operationalization Roadmap

Status as of 2026-05-23: implemented as the initial v3 operationalization
pack.

v3 turns the v2 operational intelligence pack into a more repeatable operating
layer. It introduces dedicated connector input payloads, reconciliation loop
summaries, portfolio onboarding evidence, remediation workflow state, CI-facing
policy preflight output, product UX surfaces, reusable packaging notes, external
pilot readiness, and an acceptance pack.

## Boundary

v3 does not claim autonomous production enforcement or complete live runtime
truth. Connector inputs are imported evidence payloads. They may come from real
systems, fixtures, or exported snapshots, but every output must declare its
source boundary.

## Completion Model

```text
v1 MVP: 100%
v1.5 operationalization: 100%
v2 operational intelligence: 100%
v3 operationalization: 100%
```

The v3 acceptance pack is:

```text
reports/product/v3/exports/v3-acceptance-pack.json
```

## Next Evolution After V3

- Replace imported connector payloads with scheduled connector collectors.
- Add authenticated GitHub and observability connectors behind explicit config.
- Wire policy preflight into pull request and promotion workflows.
- Exercise closed-loop remediation with real owner review records.
- Run a second external pilot and measure false positives, decision latency, and
  remediation closure.
