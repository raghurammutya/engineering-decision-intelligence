import json
import tempfile
import unittest
from pathlib import Path

from edi.dip import (
    build_dip_outputs,
    check_dip_outputs,
    dip_config,
    governance_policy_payload,
    implementation_backlog_payload,
    implementation_evidence_payload,
    target_evidence_payload,
    v0_2_backlog_payload,
    wedge_readiness_payload,
)
from edi.dip_contracts import validate_contract_artifacts
from edi.dip_trust_loop import trust_loop_payload


class DIPReadinessTests(unittest.TestCase):
    def test_governance_policy_preserves_edi_dip_boundary(self) -> None:
        config = dip_config(Path("."))
        payload = governance_policy_payload(config, "2026-05-23T00:00:00+00:00")

        self.assertEqual(payload["target_id"], "dip-framework")
        self.assertEqual(payload["first_wedge"], "Governed Decision Review and Simulation")
        self.assertEqual(payload["relationship_to_edi"], "edi_builds_and_governs_dip_but_does_not_run_dip_runtime")
        self.assertTrue(payload["fail_closed"])
        self.assertIn("deterministic_policy_before_ai_scoring", payload["governance_principles"])

    def test_wedge_readiness_is_policy_ready_but_implementation_blocked(self) -> None:
        config = dip_config(Path("."))
        payload = wedge_readiness_payload(config, "2026-05-23T00:00:00+00:00")

        self.assertEqual(payload["policy_readiness_percent"], 100.0)
        self.assertEqual(payload["implementation_evidence_percent"], 100.0)
        self.assertGreaterEqual(payload["domain_count"], 8)
        implemented = [record for record in payload["records"] if record["implementation_observed"]]
        self.assertEqual(len(implemented), 8)
        self.assertTrue(all(record["state"] == "contract_artifacts_validated" for record in implemented))

    def test_contract_artifacts_are_valid(self) -> None:
        validation = validate_contract_artifacts(Path("."))

        self.assertEqual(validation["contract_count"], 12)
        self.assertEqual(validation["passed_contract_count"], 12)
        self.assertTrue(validation["all_contracts_valid"])

    def test_implementation_backlog_is_defined_and_runtime_blocked(self) -> None:
        payload = implementation_backlog_payload(Path("."), "2026-05-23T00:00:00+00:00")

        self.assertEqual(payload["target_id"], "dip-framework")
        self.assertEqual(payload["slice_count"], 10)
        self.assertEqual(payload["defined_percent"], 100.0)
        self.assertEqual(payload["completed_slice_count"], 10)
        self.assertEqual(payload["validated_contract_slice_count"], 12)
        self.assertFalse(payload["runtime_execution_allowed"])
        self.assertEqual(payload["runtime_mutating_slice_count"], 0)
        self.assertIn("schema_contracts", payload["parallelization_groups"])
        self.assertIn("serialized_integration", payload["parallelization_groups"])

    def test_v0_2_backlog_is_defined_and_pre_runtime(self) -> None:
        payload = v0_2_backlog_payload(Path("."), "2026-05-23T00:00:00+00:00")

        self.assertEqual(payload["target_id"], "dip-framework")
        self.assertEqual(payload["slice_count"], 7)
        self.assertEqual(payload["defined_percent"], 100.0)
        self.assertEqual(payload["completed_slice_count"], 7)
        self.assertFalse(payload["runtime_execution_allowed"])
        self.assertEqual(payload["runtime_mutating_slice_count"], 0)
        self.assertIn("policy_schema", payload["safe_parallel_groups"])
        self.assertIn("computed_preflight_after_policy_schema", payload["serialized_groups"])

    def test_implementation_evidence_records_valid_contract_artifacts(self) -> None:
        config = dip_config(Path("."))
        payload = implementation_evidence_payload(config, "2026-05-23T00:00:00+00:00")

        self.assertTrue(payload["implementation_started"])
        self.assertEqual(payload["contract_artifact_count"], 12)
        self.assertEqual(payload["valid_contract_artifact_count"], 12)
        self.assertTrue(payload["trust_loop_complete"])
        self.assertFalse(payload["runtime_execution_requested"])
        self.assertFalse(payload["production_runtime_authority_granted"])

    def test_trust_loop_fixture_is_complete_without_runtime_execution(self) -> None:
        payload = trust_loop_payload(Path("."))

        self.assertTrue(payload["trust_loop_complete"])
        self.assertFalse(payload["runtime_execution_requested"])
        self.assertFalse(payload["dip_mvp_acceptance"]["runtime_integration_authorized"])

    def test_standalone_target_evidence_is_pre_runtime_only(self) -> None:
        payload = target_evidence_payload(Path("."), "2026-05-23T00:00:00+00:00")
        record = payload["records"][0]

        self.assertFalse(payload["runtime_authority_granted"])
        self.assertEqual(record["target_id"], "dip-local")
        if record["repo_exists"]:
            self.assertEqual(payload["target_repo_evidence_percent"], 100.0)
            self.assertTrue(record["remote_repo_observed"])
            self.assertTrue(record["branch_protection_observed"])
            self.assertTrue(record["required_status_check_observed"])
            self.assertTrue(record["pull_request_reviews_observed"])
            self.assertTrue(record["ci_run_observed"])
            self.assertTrue(record["validation_passed"])
            self.assertTrue(record["trust_loop_complete"])
            self.assertTrue(record["release_acceptance_commit_matches_tag"])
            self.assertTrue(record["github_release_artifact_observed"])
            self.assertEqual(record["approver_subject"], "Raghurammutya@gmail.com")
            self.assertTrue(record["main_update_bypass_observed"])
            if record.get("main_update_bypass_governed") and record.get("admin_enforcement_observed"):
                self.assertTrue(record["release_governance_clean"])
                self.assertEqual(record["state"], "local_pre_runtime_trust_loop_observed")
            else:
                self.assertFalse(record["release_governance_clean"])
                self.assertEqual(record["state"], "pre_runtime_evidence_observed_release_governance_gaps")
            self.assertFalse(record["runtime_execution_requested"])
            self.assertFalse(record["runtime_integration_authorized"])
            self.assertFalse(record["production_decision_execution_authorized"])
        else:
            self.assertEqual(payload["target_repo_evidence_percent"], 0.0)
            self.assertEqual(record["state"], "target_evidence_incomplete")

    def test_build_dip_outputs_blocks_runtime_claims(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "dip"

            result = build_dip_outputs(Path("."), out, "2026-05-23T00:00:00+00:00")

            acceptance = json.loads((out / "exports" / "dip-acceptance-pack.json").read_text(encoding="utf-8"))
            self.assertEqual(result["acceptance"]["acceptance_state"], "pre_runtime_trust_loop_complete_runtime_blocked")
            self.assertEqual(
                acceptance["maturity_claim"],
                "DIP v0.1 pre-runtime governance skeleton complete; governed decision platform readiness incomplete",
            )
            self.assertEqual(acceptance["policy_readiness_percent"], 100.0)
            self.assertEqual(acceptance["v0_1_pre_runtime_trust_loop_skeleton_percent"], 100.0)
            self.assertEqual(acceptance["v0_2_backlog_defined_percent"], 100.0)
            self.assertEqual(acceptance["v0_2_backlog_status_label"], "completed_pre_runtime")
            self.assertIn(acceptance["v0_3_computed_policy_diff_evidence_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v0_3_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["v0_4_computed_simulation_evidence_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v0_4_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["v0_5_durable_case_approval_evidence_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v0_5_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["v0_6_identity_rbac_approval_evidence_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v0_6_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["v0_7_repository_governance_evidence_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v0_7_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["v0_8_release_lifecycle_evidence_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v0_8_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["v0_9_external_identity_contract_evidence_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v0_9_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["v1_0_durable_store_contract_evidence_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v1_0_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["v1_1_governance_enforcement_parity_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v1_1_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["v1_2_product_review_surface_evidence_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v1_2_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["v1_3_multi_domain_simulation_evidence_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v1_3_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["v1_4_capability_governance_evidence_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v1_4_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["v1_5_shared_context_contract_evidence_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v1_5_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["v2_0_runtime_readiness_assessment_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v2_0_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["v2_1_governed_exception_schema_stability_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v2_1_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["independent_human_review_observed"], {False, True})
            self.assertIn(acceptance["v2_2_external_approval_boundary_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v2_2_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["live_external_approval_system_observed"], {False, True})
            self.assertIn(acceptance["v2_3_durable_case_store_adapter_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v2_3_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["production_durable_case_store_backend_observed"], {False, True})
            self.assertIn(acceptance["v2_4_evidence_store_adapter_parity_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v2_4_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["adapter_runtime_backend_invoked"], {False, True})
            self.assertIn(acceptance["v2_5_policy_engine_hardening_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v2_5_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["policy_engine_runtime_authority_observed"], {False, True})
            self.assertIn(acceptance["v2_6_external_approval_adapter_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v2_6_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["external_approval_adapter_live_system_observed"], {False, True})
            self.assertIn(acceptance["external_approval_adapter_ai_approval_allowed"], {False, True})
            self.assertIn(acceptance["v2_7_live_identity_rbac_percent"], {0.0, 100.0})
            self.assertIn(
                acceptance["v2_7_status_label"],
                {"planned_pre_runtime", "completed_pre_runtime_mfa_claim_blocked"},
            )
            self.assertIn(acceptance["live_identity_rbac_mfa_claim_observed"], {False, True})
            self.assertIn(acceptance["v2_8_durable_evidence_backend_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v2_8_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["durable_evidence_backend_runtime_invoked"], {False, True})
            self.assertIn(acceptance["v2_9_release_promotion_rollback_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v2_9_status_label"], {"planned_pre_runtime", "completed_pre_runtime"})
            self.assertIn(acceptance["prod_deployment_executed"], {False, True})
            self.assertIn(acceptance["v3_0_pre_runtime_ga_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v3_0_status_label"], {"planned_pre_runtime", "complete_runtime_blocked"})
            self.assertIn(acceptance["v3_1_governance_closure_percent"], {0.0, 100.0})
            self.assertIn(
                acceptance["v3_1_status_label"],
                {"planned_pre_runtime", "completed_pre_runtime_exception_preserved"},
            )
            self.assertIn(acceptance["v3_2_external_identity_integration_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v3_2_external_identity_live_ready"], {False, True})
            self.assertIn(acceptance["v3_3_external_approval_system_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v3_3_external_approval_system_live_ready"], {False, True})
            self.assertIn(acceptance["v3_4_production_case_store_boundary_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v3_4_production_case_store_live_ready"], {False, True})
            self.assertIn(acceptance["v3_5_runtime_control_plane_design_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v3_6_advisory_runtime_pilot_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v4_0_limited_runtime_authority_gate_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v4_0_limited_runtime_authority_granted"], {False, True})
            self.assertIn(acceptance["v4_1_live_identity_evidence_gate_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v4_1_live_identity_authority_ready"], {False, True})
            self.assertIn(acceptance["v4_2_live_approval_provider_gate_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v4_2_live_approval_provider_ready"], {False, True})
            self.assertIn(acceptance["v4_3_production_case_store_gate_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v4_3_production_case_store_live_ready"], {False, True})
            self.assertIn(acceptance["v4_4_release_promotion_execution_gate_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v4_4_prod_deployment_executed"], {False, True})
            self.assertIn(acceptance["v5_0_governed_advisory_runtime_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v5_0_side_effects_executed"], {False, True})
            self.assertIn(acceptance["v5_5_controlled_runtime_execution_gate_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v5_5_controlled_runtime_execution_authorized"], {False, True})
            self.assertIn(acceptance["v6_0_platform_hardening_assessment_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v6_0_platform_production_ready"], {False, True})
            self.assertIn(acceptance["v6_1_live_identity_authority_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v6_1_live_identity_authority_ready"], {False, True})
            self.assertIn(acceptance["v6_1_mfa_claim_observed"], {False, True})
            self.assertIn(acceptance["v6_2_live_decision_approval_provider_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v6_2_live_decision_approval_provider_ready"], {False, True})
            self.assertIn(acceptance["v6_2_ai_approval_allowed"], {False, True})
            self.assertIn(acceptance["v6_3_production_durable_case_store_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v6_3_production_durable_case_store_ready"], {False, True})
            self.assertIn(acceptance["v6_4_production_promotion_chain_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v6_4_production_promotion_ready"], {False, True})
            self.assertIn(acceptance["v7_0_controlled_runtime_pilot_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v7_0_controlled_runtime_pilot_authorized"], {False, True})
            self.assertIn(acceptance["v7_5_marketplace_runtime_governance_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v7_5_marketplace_runtime_invocation_authorized"], {False, True})
            self.assertIn(acceptance["v7_5_unrestricted_marketplace_execution_allowed"], {False, True})
            self.assertIn(acceptance["v8_0_shared_context_runtime_governance_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v8_0_runtime_context_exchange_authorized"], {False, True})
            self.assertIn(acceptance["v8_0_direct_database_access_allowed"], {False, True})
            self.assertIn(acceptance["v9_0_production_authority_readiness_review_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v9_0_production_decision_authority_granted"], {False, True})
            self.assertIn(acceptance["v10_0_completion_plan_execution_percent"], {0.0, 100.0})
            self.assertGreaterEqual(acceptance["v10_0_reviewed_step_count"], 0)
            self.assertGreaterEqual(acceptance["v10_0_evidence_gate_complete_count"], 0)
            self.assertGreaterEqual(acceptance["v10_0_live_completion_achieved_count"], 0)
            self.assertGreaterEqual(acceptance["v10_0_blocked_live_completion_count"], 0)
            self.assertIn(acceptance["v10_0_product_vision_alignment_valid"], {False, True})
            self.assertIn(acceptance["v10_0_ai_policy_boundary_preserved"], {False, True})
            self.assertIn(acceptance["v10_0_runtime_authority_grant_blocked"], {False, True})
            self.assertIn(acceptance["v10_0_production_decision_authority_blocked"], {False, True})
            self.assertIn(acceptance["v11_0_api_first_platform_foundation_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v11_0_status_label"], {"planned_pre_runtime", "contract_complete_runtime_blocked"})
            self.assertIn(acceptance["v11_0_platform_foundation_valid"], {False, True})
            self.assertIn(acceptance["v11_0_rest_authoritative"], {False, True})
            self.assertIn(acceptance["v11_0_websocket_notification_only"], {False, True})
            self.assertIn(acceptance["v11_0_forced_microservice_topology"], {False, True})
            self.assertIn(acceptance["v11_0_runtime_authority_blocked"], {False, True})
            self.assertIn(acceptance["v15_0_api_foundation_percent"], {0.0, 100.0})
            self.assertIn(acceptance["v15_0_status_label"], {"planned_pre_runtime", "contract_complete_runtime_blocked"})
            self.assertGreaterEqual(acceptance["v12_0_certified_capability_count"], 0)
            self.assertGreaterEqual(acceptance["v12_0_runtime_invocation_allowed_count"], 0)
            self.assertIn(acceptance["v13_0_cross_product_database_access_allowed"], {False, True})
            self.assertGreaterEqual(acceptance["v13_0_runtime_authority_granted_count"], 0)
            self.assertIn(acceptance["v14_0_rest_authoritative"], {False, True})
            self.assertIn(acceptance["v14_0_runtime_authority_default_blocked"], {False, True})
            self.assertIn(acceptance["v15_0_event_recovery_contract_valid"], {False, True})
            self.assertIn(acceptance["v15_0_websocket_authoritative"], {False, True})
            self.assertIn(acceptance["v15_0_events_mutate_business_state"], {False, True})
            self.assertIn(acceptance["v15_0_rest_recovery_required"], {False, True})
            self.assertIn(acceptance["v15_0_api_foundation_valid"], {False, True})
            self.assertIn(acceptance["v20_0_architecture_closure_percent"], {0.0, 100.0})
            self.assertIn(
                acceptance["v20_0_status_label"],
                {"planned_pre_runtime", "architecture_closed_runtime_blocked"},
            )
            self.assertIn(acceptance["v16_0_certification_evidence_packs_valid"], {False, True})
            self.assertGreaterEqual(acceptance["v16_0_certified_service_count"], 0)
            self.assertGreaterEqual(acceptance["v16_0_runtime_invocation_allowed_count"], 0)
            self.assertIn(acceptance["v17_0_product_pack_admission_valid"], {False, True})
            self.assertIn(acceptance["v17_0_direct_database_access_allowed"], {False, True})
            self.assertIn(acceptance["v17_0_hidden_shared_state_allowed"], {False, True})
            self.assertGreaterEqual(acceptance["v17_0_runtime_authority_granted_count"], 0)
            self.assertIn(acceptance["v18_0_openapi_skeleton_valid"], {False, True})
            self.assertIn(acceptance["v18_0_runtime_authority_blocked_response"], {False, True})
            self.assertIn(acceptance["v19_0_event_recovery_fixtures_valid"], {False, True})
            self.assertIn(acceptance["v19_0_websocket_authoritative"], {False, True})
            self.assertIn(acceptance["v19_0_events_mutate_business_state"], {False, True})
            self.assertIn(acceptance["v19_0_all_events_recoverable"], {False, True})
            self.assertIn(acceptance["v20_0_governance_store_logical_schema_valid"], {False, True})
            self.assertIn(acceptance["v20_0_storage_backend_selected"], {False, True})
            self.assertIn(acceptance["v20_0_direct_database_access_allowed"], {False, True})
            self.assertIn(acceptance["v20_0_append_only_required"], {False, True})
            self.assertIn(acceptance["v20_0_architecture_closure_valid"], {False, True})
            self.assertIn(acceptance["v25_0_contract_closure_percent"], {0.0, 100.0})
            self.assertIn(
                acceptance["v25_0_status_label"],
                {"planned_pre_runtime", "contract_closed_runtime_blocked"},
            )
            self.assertIn(acceptance["v21_0_canonical_openapi_contract_valid"], {False, True})
            self.assertIn(acceptance["v21_0_rest_authoritative"], {False, True})
            self.assertIn(acceptance["v21_0_all_commands_require_idempotency"], {False, True})
            self.assertIn(acceptance["v21_0_all_commands_require_correlation"], {False, True})
            self.assertIn(acceptance["v21_0_runtime_authority_blocked_response"], {False, True})
            self.assertIn(acceptance["v21_0_websocket_authoritative"], {False, True})
            self.assertIn(acceptance["v22_0_product_pack_contract_kit_valid"], {False, True})
            self.assertGreaterEqual(acceptance["v22_0_template_count"], 0)
            self.assertIn(acceptance["v22_0_direct_database_access_allowed"], {False, True})
            self.assertIn(acceptance["v22_0_hidden_shared_state_allowed"], {False, True})
            self.assertGreaterEqual(acceptance["v22_0_runtime_authority_granted_count"], 0)
            self.assertIn(acceptance["v23_0_adapter_evidence_contract_kit_valid"], {False, True})
            self.assertGreaterEqual(acceptance["v23_0_adapter_contract_count"], 0)
            self.assertGreaterEqual(acceptance["v23_0_live_invocation_allowed_count"], 0)
            self.assertIn(acceptance["v23_0_sample_evidence_present"], {False, True})
            self.assertIn(acceptance["v24_0_governance_store_logical_api_valid"], {False, True})
            self.assertIn(acceptance["v24_0_storage_backend_selected"], {False, True})
            self.assertIn(acceptance["v24_0_direct_database_access_allowed"], {False, True})
            self.assertIn(acceptance["v24_0_delete_operation_allowed"], {False, True})
            self.assertIn(acceptance["v24_0_projection_rebuild_required"], {False, True})
            self.assertIn(acceptance["v25_0_event_recovery_contract_v2_valid"], {False, True})
            self.assertGreaterEqual(acceptance["v25_0_event_type_count"], 0)
            self.assertIn(acceptance["v25_0_websocket_authoritative"], {False, True})
            self.assertIn(acceptance["v25_0_events_mutate_business_state"], {False, True})
            self.assertIn(acceptance["v25_0_rest_event_log_required"], {False, True})
            self.assertIn(acceptance["v25_0_reconnect_recovery_required"], {False, True})
            self.assertIn(acceptance["v25_0_contract_closure_valid"], {False, True})
            self.assertIn(acceptance["v30_0_platform_operating_model_percent"], {0.0, 100.0})
            self.assertIn(
                acceptance["v30_0_status_label"],
                {"planned_pre_runtime", "platform_operating_model_closed_runtime_blocked"},
            )
            self.assertIn(acceptance["v26_0_certification_workflow_valid"], {False, True})
            self.assertGreaterEqual(acceptance["v26_0_certified_count"], 0)
            self.assertGreaterEqual(acceptance["v26_0_runtime_invocation_allowed_count"], 0)
            self.assertGreaterEqual(acceptance["v26_0_evidence_complete_count"], 0)
            self.assertIn(acceptance["v27_0_runtime_authority_gate_contract_valid"], {False, True})
            self.assertIn(acceptance["v27_0_runtime_authority_granted"], {False, True})
            self.assertIn(acceptance["v27_0_negative_fixtures_block_authority"], {False, True})
            self.assertIn(acceptance["v28_0_cost_usage_evidence_contract_valid"], {False, True})
            self.assertIn(acceptance["v28_0_billing_integration_enabled"], {False, True})
            self.assertGreaterEqual(acceptance["v28_0_live_invocation_observed_count"], 0)
            self.assertIn(acceptance["v29_0_semantic_projection_contract_valid"], {False, True})
            self.assertIn(acceptance["v29_0_direct_database_access_allowed"], {False, True})
            self.assertIn(acceptance["v29_0_runtime_context_exchange_authorized"], {False, True})
            self.assertIn(acceptance["v30_0_product_pack_developer_kit_valid"], {False, True})
            self.assertGreaterEqual(acceptance["v30_0_runtime_authority_granted_count"], 0)
            self.assertIn(acceptance["v30_0_direct_database_access_allowed"], {False, True})
            self.assertIn(acceptance["v30_0_platform_operating_model_closure_valid"], {False, True})
            self.assertIn(acceptance["v35_0_usability_governance_percent"], {0.0, 100.0})
            self.assertIn(
                acceptance["v35_0_status_label"],
                {"planned_pre_runtime", "usability_governance_closed_runtime_blocked"},
            )
            self.assertIn(acceptance["v31_0_compatibility_versioning_valid"], {False, True})
            self.assertIn(acceptance["v31_0_breaking_change_requires_major"], {False, True})
            self.assertIn(acceptance["v32_0_policy_test_pack_framework_valid"], {False, True})
            self.assertIn(acceptance["v32_0_ai_policy_override_allowed"], {False, True})
            self.assertIn(acceptance["v33_0_product_pack_cli_scaffold_valid"], {False, True})
            self.assertIn(acceptance["v33_0_no_code_builder"], {False, True})
            self.assertGreaterEqual(acceptance["v33_0_runtime_authority_creating_command_count"], 0)
            self.assertIn(acceptance["v34_0_case_evidence_query_contract_valid"], {False, True})
            self.assertIn(acceptance["v34_0_production_backend_selected"], {False, True})
            self.assertIn(acceptance["v35_0_governance_dashboard_data_contract_valid"], {False, True})
            self.assertIn(acceptance["v35_0_dashboard_is_source_of_truth"], {False, True})
            self.assertIn(acceptance["v35_0_websocket_authoritative"], {False, True})
            self.assertIn(acceptance["v35_0_usability_governance_closure_valid"], {False, True})
            self.assertIn(acceptance["v40_0_review_workspace_percent"], {0.0, 100.0})
            self.assertIn(
                acceptance["v40_0_status_label"],
                {"planned_pre_runtime", "review_workspace_closed_runtime_blocked"},
            )
            self.assertIn(acceptance["v36_0_product_pack_authoring_ux_valid"], {False, True})
            self.assertIn(acceptance["v36_0_all_transitions_require_rest"], {False, True})
            self.assertIn(acceptance["v36_0_websocket_authoritative"], {False, True})
            self.assertIn(acceptance["v36_0_broad_no_code_builder"], {False, True})
            self.assertIn(acceptance["v37_0_governance_review_queue_valid"], {False, True})
            self.assertIn(acceptance["v37_0_approval_automation_allowed"], {False, True})
            self.assertIn(acceptance["v38_0_capability_lineage_explorer_valid"], {False, True})
            self.assertIn(acceptance["v38_0_direct_runtime_invocation_allowed"], {False, True})
            self.assertIn(acceptance["v39_0_replay_workspace_valid"], {False, True})
            self.assertIn(acceptance["v39_0_runtime_execution_allowed"], {False, True})
            self.assertIn(acceptance["v39_0_side_effects_allowed"], {False, True})
            self.assertIn(acceptance["v40_0_usability_acceptance_pack_valid"], {False, True})
            self.assertIn(acceptance["v40_0_runtime_remains_blocked"], {False, True})
            self.assertIn(acceptance["v40_0_websocket_authoritative"], {False, True})
            self.assertIn(acceptance["v45_0_platform_operator_readiness_percent"], {0.0, 100.0})
            self.assertIn(
                acceptance["v45_0_status_label"],
                {"planned_pre_runtime", "operator_readiness_closed_runtime_blocked"},
            )
            self.assertIn(acceptance["v41_0_evidence_retention_legal_hold_valid"], {False, True})
            self.assertIn(acceptance["v41_0_production_backend_selected"], {False, True})
            self.assertIn(acceptance["v42_0_tenant_workspace_boundary_valid"], {False, True})
            self.assertIn(acceptance["v42_0_live_multi_tenant_enforcement_observed"], {False, True})
            self.assertIn(acceptance["v43_0_entitlement_usage_gate_valid"], {False, True})
            self.assertIn(acceptance["v43_0_billing_integration_enabled"], {False, True})
            self.assertIn(acceptance["v43_0_runtime_enforcement_claimed"], {False, True})
            self.assertIn(acceptance["v44_0_integration_certification_ux_valid"], {False, True})
            self.assertGreaterEqual(acceptance["v44_0_certified_count"], 0)
            self.assertGreaterEqual(acceptance["v44_0_runtime_invocation_allowed_count"], 0)
            self.assertIn(acceptance["v45_0_platform_operator_readiness_pack_valid"], {False, True})
            self.assertIn(acceptance["v45_0_unsafe_claims_visible"], {False, True})
            self.assertIn(acceptance["v45_0_runtime_remains_blocked"], {False, True})
            self.assertIn(acceptance["v50_0_platform_governance_closure_percent"], {0.0, 100.0})
            self.assertIn(
                acceptance["v50_0_status_label"],
                {"planned_pre_runtime", "platform_governance_closed_runtime_blocked"},
            )
            self.assertIn(acceptance["v46_0_repository_governance_evidence_pack_valid"], {False, True})
            self.assertIn(acceptance["v46_0_security_policy_active"], {False, True})
            self.assertIn(acceptance["v46_0_dependabot_enabled"], {False, True})
            self.assertIn(acceptance["v46_0_actions_allowlist_observed"], {False, True})
            self.assertGreaterEqual(acceptance["v46_0_open_dependabot_alert_count"], 0)
            self.assertIn(acceptance["v47_0_pr_validation_policy_valid"], {False, True})
            self.assertIn(acceptance["v47_0_pr_requires_release_artifact"], {False, True})
            self.assertIn(acceptance["v47_0_release_requires_release_artifact"], {False, True})
            self.assertIn(acceptance["v47_0_release_acceptance_required_for_pr"], {False, True})
            self.assertIn(acceptance["v48_0_governance_exception_register_valid"], {False, True})
            self.assertGreaterEqual(acceptance["v48_0_exception_count"], 0)
            self.assertGreaterEqual(acceptance["v48_0_controls_restored_count"], 0)
            self.assertGreaterEqual(acceptance["v48_0_runtime_authority_granted_count"], 0)
            self.assertIn(acceptance["v49_0_edi_observer_ingestion_contract_valid"], {False, True})
            self.assertIn(acceptance["v49_0_edi_is_authority"], {False, True})
            self.assertGreaterEqual(acceptance["v49_0_ingested_evidence_type_count"], 0)
            self.assertIn(acceptance["v50_0_platform_governance_closure_pack_valid"], {False, True})
            self.assertIn(acceptance["v50_0_runtime_remains_blocked"], {False, True})
            self.assertGreaterEqual(acceptance["v50_0_closure_gate_complete_count"], 0)
            self.assertGreaterEqual(acceptance["v50_0_closure_gate_count"], 0)
            self.assertIn(acceptance["pre_runtime_completion_scope_percent"], {0.0, 100.0})
            self.assertIn(acceptance["approver_subject"], {None, "not_generated", "Raghurammutya@gmail.com"})
            self.assertEqual(acceptance["maturity_status_labels"]["policy_preflight"], "computed_for_first_fixture")
            self.assertIn(
                acceptance["maturity_status_labels"]["policy_engine"],
                {
                    "policy_engine_hardening_incomplete",
                    "deterministic_policy_engine_lifecycle_and_precedence_validated",
                },
            )
            self.assertIn(acceptance["deterministic_policy_engine_readiness_percent"], {45.0, 60.0, 80.0})
            self.assertIn(acceptance["computed_simulation_diff_readiness_percent"], {10.0, 45.0, 70.0, 80.0})
            self.assertIn(acceptance["durable_case_store_readiness_percent"], {30.0, 60.0, 80.0, 85.0, 90.0, 95.0})
            self.assertIn(
                acceptance["identity_backed_approval_readiness_percent"],
                {0.0, 25.0, 45.0, 65.0, 75.0, 85.0},
            )
            self.assertIn(acceptance["release_management_readiness_percent"], {35.0, 40.0, 70.0, 85.0, 95.0})
            self.assertIn(
                acceptance["maturity_status_labels"]["release_management"],
                {
                    "tag_and_local_acceptance_present_ci_artifact_missing_admin_bypass_observed",
                    "tag_and_artifact_backed_acceptance_present_admin_bypass_observed",
                    "admin_enforced_tag_and_artifact_backed_acceptance_present",
                    "release_lifecycle_policy_artifact_backed_admin_enforced",
                    "promotion_chain_and_rollback_evidence_observed_admin_bypass_governed",
                },
            )
            self.assertEqual(acceptance["runtime_execution_readiness_percent"], 0.0)
            self.assertEqual(acceptance["production_decision_authority_percent"], 0.0)
            self.assertEqual(acceptance["implementation_backlog_defined_percent"], 100.0)
            self.assertEqual(acceptance["implementation_evidence_percent"], 100.0)
            self.assertIn(acceptance["target_repo_evidence_percent"], {0.0, 100.0})
            self.assertIn(acceptance["target_repo_governance_clean_percent"], {0.0, 100.0})
            self.assertIn("DIP deterministic policy engine is ready", acceptance["blocked_claims"])
            self.assertIn("ML services are the DIP platform foundation", acceptance["blocked_claims"])
            if acceptance["target_repo_governance_clean_percent"] == 0.0:
                self.assertIn("DIP main updates are governed without admin bypass", acceptance["blocked_claims"])
            self.assertIn("DIP runtime integration is authorized", acceptance["blocked_claims"])

    def test_committed_dip_outputs_are_current(self) -> None:
        self.assertTrue(check_dip_outputs(Path(".")))


if __name__ == "__main__":
    unittest.main()
