# V4 Live Enforcement Readiness Roadmap

Status as of 2026-05-23: implemented as the initial v4 readiness pack.

v4 defines the controls required before Engineering Decision Intelligence can
operate with scheduled connectors and CI/PR enforcement in a real target
environment.

## Boundary

v4 is a readiness and operating-control pack. It does not claim that credentials
are installed, target repositories have adopted the CI gate, or production
enforcement is active. Those claims require target-system installation evidence.

## Completion Model

```text
v1 MVP: 100%
v1.5 operationalization: 100%
v2 operational intelligence: 100%
v3 operationalization: 100%
v4 live enforcement readiness: 100%
```

## Required Before Real Production Enforcement

- target organization credentials installed through approved secret storage,
- connector jobs scheduled and observed,
- PR checks enabled in target repositories,
- owner approval workflow exercised by real owners,
- persistence backend deployed with retention policy,
- SLOs measured from live connector runs,
- security review and audit logging accepted.
