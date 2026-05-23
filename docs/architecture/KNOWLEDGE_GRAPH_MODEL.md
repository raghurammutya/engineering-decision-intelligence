# Knowledge Graph Model

## Purpose

The Engineering Knowledge Graph is the product's working model of observed
engineering reality and intended policy.

The graph exists to support decision-making, not to become a large abstract
ontology.

## Initial Entities

| Entity | Meaning |
| --- | --- |
| Repo | Source repository or codebase |
| Service | Runtime or deployable service |
| Workflow | CI/CD workflow or automation pipeline |
| Script | Executable utility or automation script |
| Environment | dev, test, staging, prod, or equivalent runtime |
| Owner | Team, person, or service boundary accountable for an entity |
| Evidence | Report, log, test result, approval, or audit artifact |
| Deployment | Deployment event or promotion action |
| Incident | Operational incident, alert, or failure event |
| Agent | AI or automation agent with tool capability |
| Prompt | AI instruction, policy prompt, or orchestration prompt |
| Policy | Intended rule, control, or operating policy |

## Initial Relationships

| Relationship | Example |
| --- | --- |
| repo contains service | ML contains order service |
| workflow deploys service | promote workflow deploys backend |
| script mutates environment | promotion script mutates staging |
| service depends on service | frontend depends on API gateway |
| deployment changes environment | release changes prod |
| deployment correlated with incident | release correlated with websocket lag |
| owner maintains entity | platform team owns deployment workflow |
| evidence supports decision | regression report supports limited live |
| agent invokes tool | deployment agent invokes shell |
| prompt used by agent | deploy policy prompt used by deployment agent |
| policy governs capability | prod promotion policy governs deploy workflow |

## Entity Record Requirements

Every graph record should preserve:

- stable id,
- entity type,
- source system,
- source path or external id,
- observed timestamp,
- confidence,
- owner if known,
- lifecycle state if known,
- evidence references.

## Relationship Record Requirements

Every relationship should preserve:

- source entity,
- relationship type,
- target entity,
- observed or declared source,
- confidence,
- evidence references,
- first observed timestamp,
- last observed timestamp.

## Design Constraint

Do not add entities just because they are conceptually interesting. Add an
entity only when it improves drift detection, risk inference, or decision
quality.
