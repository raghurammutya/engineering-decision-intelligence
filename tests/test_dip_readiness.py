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
    wedge_readiness_payload,
)
from edi.dip_contracts import validate_contract_artifacts


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
        self.assertEqual(payload["implementation_evidence_percent"], 50.0)
        self.assertGreaterEqual(payload["domain_count"], 8)
        implemented = [record for record in payload["records"] if record["implementation_observed"]]
        self.assertEqual(len(implemented), 4)
        self.assertTrue(all(record["state"] == "contract_artifacts_validated" for record in implemented))

    def test_contract_artifacts_are_valid(self) -> None:
        validation = validate_contract_artifacts(Path("."))

        self.assertEqual(validation["contract_count"], 4)
        self.assertEqual(validation["passed_contract_count"], 4)
        self.assertTrue(validation["all_contracts_valid"])

    def test_implementation_backlog_is_defined_and_runtime_blocked(self) -> None:
        payload = implementation_backlog_payload(Path("."), "2026-05-23T00:00:00+00:00")

        self.assertEqual(payload["target_id"], "dip-framework")
        self.assertEqual(payload["slice_count"], 10)
        self.assertEqual(payload["defined_percent"], 100.0)
        self.assertEqual(payload["completed_slice_count"], 4)
        self.assertFalse(payload["runtime_execution_allowed"])
        self.assertEqual(payload["runtime_mutating_slice_count"], 0)
        self.assertIn("schema_contracts", payload["parallelization_groups"])
        self.assertIn("serialized_integration", payload["parallelization_groups"])

    def test_implementation_evidence_records_valid_contract_artifacts(self) -> None:
        config = dip_config(Path("."))
        payload = implementation_evidence_payload(config, "2026-05-23T00:00:00+00:00")

        self.assertTrue(payload["implementation_started"])
        self.assertEqual(payload["contract_artifact_count"], 4)
        self.assertEqual(payload["valid_contract_artifact_count"], 4)
        self.assertFalse(payload["production_runtime_authority_granted"])

    def test_build_dip_outputs_blocks_runtime_claims(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "dip"

            result = build_dip_outputs(Path("."), out, "2026-05-23T00:00:00+00:00")

            acceptance = json.loads((out / "exports" / "dip-acceptance-pack.json").read_text(encoding="utf-8"))
            self.assertEqual(result["acceptance"]["acceptance_state"], "governance_pack_ready_implementation_evidence_incomplete")
            self.assertEqual(acceptance["policy_readiness_percent"], 100.0)
            self.assertEqual(acceptance["implementation_backlog_defined_percent"], 100.0)
            self.assertEqual(acceptance["implementation_evidence_percent"], 50.0)
            self.assertIn("DIP runtime integration is authorized", acceptance["blocked_claims"])

    def test_committed_dip_outputs_are_current(self) -> None:
        self.assertTrue(check_dip_outputs(Path(".")))


if __name__ == "__main__":
    unittest.main()
