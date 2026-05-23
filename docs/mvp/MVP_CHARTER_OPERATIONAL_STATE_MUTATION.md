# MVP Charter: Operational State Mutation Reconciliation

## MVP Question

Which workflows, scripts, agents, jobs, or automations can change operational
state, and are they canonical, owner-approved, evidenced, and safe?

## Why This MVP

This slice is valuable because it is:

- high risk,
- visible to leadership,
- useful to engineering teams,
- available from existing repository and workflow data,
- connected to runtime and deployment safety,
- measurable through reduced ambiguity and unsafe paths.

## Operational State

Operational state includes:

- deployments,
- database mutation,
- infrastructure changes,
- queue mutation,
- broker/order writes,
- configuration mutation,
- secret usage,
- runtime shell execution,
- AI-agent tool execution.

## Initial Inputs

- repository file tree,
- workflow definitions,
- executable scripts,
- deployment scripts,
- environment lifecycle scripts,
- evidence reports,
- ownership hints,
- policy documents.

## Initial Decisions

The MVP should generate decisions such as:

- canonical automation exists,
- owner review required,
- direct production mutation path detected,
- evidence missing,
- rollback evidence missing,
- secret-sensitive automation detected,
- non-canonical duplicate automation detected,
- retired automation still appears active,
- AI/tool execution needs capability review.

## Acceptance Criteria

The MVP is useful when it can answer, for one pilot repository:

1. Which workflows and scripts can mutate operational state?
2. Which environments can each mutation path affect?
3. Which mutation paths are canonical?
4. Which mutation paths require owner review?
5. Which mutation paths lack evidence?
6. Which mutation paths conflict with intended policy?
7. Which findings are high enough risk to block or escalate?

## ML Pilot Policy Example

For the ML pilot, intended operating policy includes:

- development starts in dev,
- promotion order is dev to test to staging to prod,
- direct production deploys are prohibited except break-glass,
- promotion should use repository automation,
- promotion evidence should be recorded.

The MVP should detect divergence from this policy.

## Non-Goals

- full enterprise graph,
- polished dashboard,
- AI enforcement,
- broad artifact inventory,
- universal architecture truth,
- deletion automation.
