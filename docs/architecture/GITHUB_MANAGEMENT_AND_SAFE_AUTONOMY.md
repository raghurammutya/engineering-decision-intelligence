# GitHub Management And Safe Autonomy

## Purpose

Two product capabilities must be first-class from the beginning:

1. GitHub and local repository management.
2. Safe but autonomous engineering.

They are connected. GitHub and local repository state show where engineering
work is actually happening. Safe autonomy defines what the system, automation,
or AI agents are allowed to do with that reality.

## Capability A: GitHub And Local Repository Management

The product should reconcile local development reality with GitHub-hosted
collaboration and automation reality.

### Local Reality

The system should understand:

- local repositories,
- side worktrees,
- uncommitted changes,
- branch divergence,
- generated files,
- local scripts,
- local evidence artifacts,
- ignored files that may still matter operationally.

### GitHub Reality

The system should understand:

- repositories,
- default branches,
- active branches,
- pull requests,
- issues,
- releases,
- workflow definitions,
- workflow runs,
- environments,
- branch protection,
- code owners,
- repository owners,
- secret references,
- deployment records where available.

### Management Decisions

The product should answer:

- Which repositories are active, stale, ownerless, or risky?
- Which branches diverge from intended release policy?
- Which pull requests touch high-risk automation or operational-state mutation?
- Which workflows can deploy, mutate infrastructure, or use secrets?
- Which local artifacts should remain non-canonical?
- Which generated evidence should be retained, archived, or regenerated?
- Which GitHub controls are missing for a high-risk repository?

## Capability B: Safe But Autonomous Engineering

The product should increase autonomy where the system has enough evidence and
reduce autonomy where risk or ambiguity rises.

The goal is not manual approval for every action. The goal is controlled,
evidence-backed autonomy.

## Autonomy Modes

| Mode | Allowed Behavior |
| --- | --- |
| observe | scan and report only |
| recommend | suggest actions without changing files or systems |
| prepare | generate proposed changes for human review |
| guarded_execute | execute low-risk approved actions with evidence |
| controlled_execute | execute high-risk actions only through gated policy |
| blocked | refuse execution because risk or ambiguity is too high |

## Autonomy Inputs

Autonomy decisions should consider:

- mutation capability,
- target environment,
- secret sensitivity,
- owner confidence,
- test evidence,
- rollback evidence,
- policy coverage,
- production impact,
- branch protection,
- pull request review state,
- incident correlation,
- AI-agent tool permissions.

## Safe Autonomy Principles

- More evidence should enable more autonomy.
- Missing evidence should reduce autonomy.
- High-risk mutation should require controlled admission.
- Uncertainty should fail closed for production-impacting actions.
- AI can recommend and explain before it executes.
- Autonomous actions must leave evidence.
- Generated outputs must declare their inputs.

## First MVP Application

For the ML pilot, the system should:

1. Scan local workflows and scripts.
2. Scan GitHub repository and pull request state.
3. Detect operational-state mutation capability.
4. Compare mutation paths with promotion policy.
5. Assign each path an autonomy mode.
6. Generate a materialized view showing allowed, guarded, owner-review, and
   blocked paths.

## Example Decision

```text
workflow: deploy-production.yml
observed: can mutate prod
intended_policy: production promotion must use promote_by_environment.sh
evidence: no rollback evidence found
owner: unknown
risk: critical
autonomy_mode: blocked
decision: owner review and canonical promotion migration required
```
