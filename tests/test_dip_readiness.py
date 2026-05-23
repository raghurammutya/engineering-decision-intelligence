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
            self.assertTrue(record["main_update_bypass_observed"])
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
            self.assertEqual(acceptance["maturity_status_labels"]["policy_preflight"], "computed_for_first_fixture")
            self.assertIn(acceptance["deterministic_policy_engine_readiness_percent"], {45.0, 60.0})
            self.assertIn(acceptance["computed_simulation_diff_readiness_percent"], {10.0, 45.0, 70.0})
            self.assertIn(acceptance["durable_case_store_readiness_percent"], {30.0, 60.0})
            self.assertIn(acceptance["identity_backed_approval_readiness_percent"], {0.0, 25.0})
            self.assertIn(acceptance["release_management_readiness_percent"], {35.0, 40.0})
            self.assertIn(
                acceptance["maturity_status_labels"]["release_management"],
                {
                    "tag_and_local_acceptance_present_ci_artifact_missing_admin_bypass_observed",
                    "tag_and_artifact_backed_acceptance_present_admin_bypass_observed",
                },
            )
            self.assertEqual(acceptance["runtime_execution_readiness_percent"], 0.0)
            self.assertEqual(acceptance["production_decision_authority_percent"], 0.0)
            self.assertEqual(acceptance["implementation_backlog_defined_percent"], 100.0)
            self.assertEqual(acceptance["implementation_evidence_percent"], 100.0)
            self.assertIn(acceptance["target_repo_evidence_percent"], {0.0, 100.0})
            self.assertEqual(acceptance["target_repo_governance_clean_percent"], 0.0)
            self.assertIn("DIP deterministic policy engine is ready", acceptance["blocked_claims"])
            self.assertIn("DIP main updates are governed without admin bypass", acceptance["blocked_claims"])
            self.assertIn("DIP runtime integration is authorized", acceptance["blocked_claims"])

    def test_committed_dip_outputs_are_current(self) -> None:
        self.assertTrue(check_dip_outputs(Path(".")))


if __name__ == "__main__":
    unittest.main()
