# Entity Model Draft

## Required Fields

| Field | Meaning |
| --- | --- |
| id | stable entity id |
| type | repo, service, workflow, script, environment, owner, evidence, deployment, incident, agent, prompt, policy |
| name | human-readable name |
| source_system | Git, CI/CD, telemetry, observability, manual policy, AI-agent log |
| source_ref | path, URL, event id, or external reference |
| first_observed_at | first observation timestamp |
| last_observed_at | most recent observation timestamp |
| confidence | high, medium, low |
| lifecycle_state | active, shadow, retired, unknown, experimental |
| owner_ref | owner id if known |
| evidence_refs | supporting evidence ids |

## First MVP Entity Types

- workflow,
- script,
- environment,
- owner,
- evidence,
- policy.

Service, deployment, incident, and agent become stronger in later phases.
