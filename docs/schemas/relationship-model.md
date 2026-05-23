# Relationship Model Draft

## Required Fields

| Field | Meaning |
| --- | --- |
| id | stable relationship id |
| source_entity_id | relationship source |
| relationship_type | normalized relationship label |
| target_entity_id | relationship target |
| source_system | origin of relationship observation |
| source_ref | path, URL, event id, or external reference |
| first_observed_at | first observation timestamp |
| last_observed_at | most recent observation timestamp |
| confidence | high, medium, low |
| evidence_refs | supporting evidence ids |

## First MVP Relationships

| Relationship | Meaning |
| --- | --- |
| workflow_invokes_script | workflow calls a script |
| workflow_mutates_environment | workflow can change an environment |
| script_mutates_environment | script can change an environment |
| policy_governs_workflow | policy applies to workflow |
| policy_governs_script | policy applies to script |
| evidence_supports_decision | evidence supports a finding or decision |
| owner_maintains_entity | owner is accountable for entity |

## Later Relationships

- service_depends_on_service,
- workflow_deploys_service,
- deployment_correlates_with_incident,
- agent_invokes_tool,
- prompt_used_by_agent.
