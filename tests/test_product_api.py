import json
import tempfile
import unittest
from pathlib import Path

from edi.product_api import build_snapshot, write_snapshot


class ProductApiTests(unittest.TestCase):
    def test_build_snapshot_contains_stable_sections(self) -> None:
        snapshot = build_snapshot(Path("."), "2026-05-23T00:00:00+00:00")

        self.assertEqual(snapshot["api_version"], "v1")
        self.assertIn("product", snapshot)
        self.assertIn("executive", snapshot)
        self.assertIn("risk", snapshot)
        self.assertIn("ai_agents", snapshot)
        self.assertIn("scanner_tuning", snapshot)
        self.assertIn("operationalization", snapshot)
        self.assertIn("v2", snapshot)
        self.assertIn("v3", snapshot)
        self.assertIn("v4", snapshot)
        self.assertIn("v5", snapshot)
        self.assertIn("substrate", snapshot)
        self.assertIn("dip", snapshot)
        self.assertGreater(snapshot["product"]["completion_percent"], 0)
        self.assertIsInstance(snapshot["executive"]["top_decisions"], list)
        self.assertGreater(snapshot["risk"]["runtime_signal_count"], 0)
        self.assertGreaterEqual(snapshot["ai_agents"]["capability_count"], 0)
        self.assertGreaterEqual(snapshot["scanner_tuning"]["candidate_count"], 0)
        self.assertGreaterEqual(snapshot["operationalization"]["review_workflow_count"], 0)
        self.assertEqual(snapshot["v2"]["acceptance_state"], "pass")
        self.assertEqual(snapshot["v3"]["acceptance_state"], "pass")
        self.assertGreaterEqual(snapshot["v3"]["connector_count"], 6)
        self.assertEqual(snapshot["v4"]["acceptance_state"], "pass")
        self.assertGreaterEqual(snapshot["v4"]["connector_count"], 6)
        self.assertEqual(snapshot["v5"]["tooling_completion_percent"], 100.0)
        self.assertGreaterEqual(snapshot["v5"]["live_claim_completion_percent"], 0.0)
        self.assertLess(snapshot["v5"]["live_claim_completion_percent"], 100.0)
        self.assertIn("autonomous production enforcement is active", snapshot["v5"]["blocked_claims"])
        self.assertIn("complete live runtime truth exists", snapshot["v5"]["blocked_claims"])
        self.assertEqual(snapshot["substrate"]["policy_completion_percent"], 100.0)
        self.assertEqual(snapshot["substrate"]["live_evidence_completion_percent"], 0.0)
        self.assertEqual(snapshot["substrate"]["promotion_order"], ["dev", "test", "staging", "prod"])
        self.assertEqual(snapshot["dip"]["policy_readiness_percent"], 100.0)
        self.assertEqual(snapshot["dip"]["v0_1_pre_runtime_trust_loop_skeleton_percent"], 100.0)
        self.assertEqual(snapshot["dip"]["v0_2_backlog_defined_percent"], 100.0)
        self.assertEqual(snapshot["dip"]["v0_2_backlog_status_label"], "completed_pre_runtime")
        self.assertEqual(snapshot["dip"]["v0_3_computed_policy_diff_evidence_percent"], 100.0)
        self.assertEqual(snapshot["dip"]["v0_3_status_label"], "completed_pre_runtime")
        self.assertEqual(snapshot["dip"]["v0_4_computed_simulation_evidence_percent"], 100.0)
        self.assertEqual(snapshot["dip"]["v0_4_status_label"], "completed_pre_runtime")
        self.assertEqual(snapshot["dip"]["maturity_status_labels"]["policy_preflight"], "computed_for_first_fixture")
        self.assertEqual(snapshot["dip"]["deterministic_policy_engine_readiness_percent"], 60.0)
        self.assertEqual(snapshot["dip"]["computed_simulation_diff_readiness_percent"], 70.0)
        self.assertEqual(snapshot["dip"]["durable_case_store_readiness_percent"], 30.0)
        self.assertEqual(snapshot["dip"]["identity_backed_approval_readiness_percent"], 0.0)
        self.assertEqual(snapshot["dip"]["release_management_readiness_percent"], 40.0)
        self.assertEqual(snapshot["dip"]["runtime_execution_readiness_percent"], 0.0)
        self.assertEqual(snapshot["dip"]["production_decision_authority_percent"], 0.0)
        self.assertEqual(snapshot["dip"]["implementation_backlog_defined_percent"], 100.0)
        self.assertEqual(snapshot["dip"]["implementation_evidence_percent"], 100.0)
        self.assertEqual(snapshot["dip"]["target_repo_evidence_percent"], 100.0)
        self.assertEqual(snapshot["dip"]["target_repo_governance_clean_percent"], 0.0)
        self.assertEqual(snapshot["dip"]["target_repo_state"], "pre_runtime_evidence_observed_release_governance_gaps")
        self.assertEqual(snapshot["dip"]["first_wedge"], "Governed Decision Review and Simulation")

    def test_write_snapshot_materializes_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "api.json"

            snapshot = write_snapshot(Path("."), out, "2026-05-23T00:00:00+00:00")

            written = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(written["api_version"], "v1")
            self.assertEqual(written["generated_at"], snapshot["generated_at"])


if __name__ == "__main__":
    unittest.main()
