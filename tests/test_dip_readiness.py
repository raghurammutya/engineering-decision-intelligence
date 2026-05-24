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
            self.assertIn(acceptance["pre_runtime_completion_scope_percent"], {0.0, 100.0})
            self.assertEqual(acceptance["approver_subject"], "Raghurammutya@gmail.com")
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
            if acceptance["target_repo_governance_clean_percent"] == 0.0:
                self.assertIn("DIP main updates are governed without admin bypass", acceptance["blocked_claims"])
            self.assertIn("DIP runtime integration is authorized", acceptance["blocked_claims"])

    def test_committed_dip_outputs_are_current(self) -> None:
        self.assertTrue(check_dip_outputs(Path(".")))


if __name__ == "__main__":
    unittest.main()
