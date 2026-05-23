# ADR-0004: GitHub/Local Management And Safe Autonomy Are First-Class

## Status

Accepted

## Context

The product must manage engineering reality where it actually exists. That
means both local development state and GitHub-hosted collaboration, automation,
review, and release state.

The product must also make engineering more autonomous without making it unsafe.
Autonomy without controls creates operational risk. Governance without autonomy
creates drag and bypass behavior.

## Decision

GitHub/local repository management and safe autonomy will be first-class product
capabilities.

GitHub/local management will reconcile:

- local worktrees and branches,
- GitHub repositories,
- pull requests,
- workflows,
- environments,
- branch protection,
- ownership and review state.

Safe autonomy will assign an autonomy mode to workflows, scripts, agents, and
automation based on evidence, risk, policy, owner confidence, and operational
mutation capability.

## Consequences

- Repository management is decision-oriented, not inventory-oriented.
- Pull requests and workflows become part of the engineering knowledge graph.
- Automation and AI agents are governed by capability and risk.
- Low-risk actions can become more autonomous.
- High-risk or ambiguous actions fail closed or require controlled admission.
