# DIP Governance Policy

Generated: `2026-05-24T00:28:47+00:00`

Target: `Decision Intelligence Platform`
First wedge: `Governed Decision Review and Simulation`
EDI relationship: `edi_builds_and_governs_dip_but_does_not_run_dip_runtime`
Source boundary: `declared_policy_not_dip_runtime_evidence`
Fail closed: `True`

## Governance Principles

- `decision_spec_is_source_of_intent`
- `generated_artifacts_are_derived_outputs`
- `deterministic_policy_before_ai_scoring`
- `ai_may_propose_but_not_approve_or_bypass_policy`
- `source_labels_are_visible_and_reviewable`
- `approval_and_case_evidence_precede_runtime_authority`
- `readiness_claims_fail_closed_without_target_evidence`

## Source Labels

- `user_declared`
- `imported`
- `observed`
- `inferred`
- `ai_proposed`
- `user_reviewed`
- `policy_derived`
- `system_generated`
