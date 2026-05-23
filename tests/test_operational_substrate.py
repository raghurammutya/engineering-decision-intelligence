import json
import tempfile
import unittest
from pathlib import Path

from edi.substrate import (
    build_substrate_outputs,
    check_substrate_outputs,
    lifecycle_payload,
    substrate_config,
)


class OperationalSubstrateTests(unittest.TestCase):
    def test_lifecycle_declares_dev_first_canonical_promotion(self) -> None:
        config = substrate_config(Path("."))
        payload = lifecycle_payload(config, "2026-05-23T00:00:00+00:00")

        self.assertEqual(payload["promotion_order"], ["dev", "test", "staging", "prod"])
        self.assertEqual(payload["promotion_contract"], "build_once_validate_in_dev_promote_same_artifact")
        self.assertGreaterEqual(payload["canonical_operation_count"], 3)
        self.assertTrue(payload["fail_closed"])

    def test_build_substrate_outputs_blocks_live_claims(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "substrate"

            result = build_substrate_outputs(Path("."), out, "2026-05-23T00:00:00+00:00")

            acceptance = json.loads((out / "exports" / "substrate-acceptance-pack.json").read_text(encoding="utf-8"))
            self.assertEqual(result["acceptance"]["acceptance_state"], "policy_pack_ready_live_evidence_incomplete")
            self.assertEqual(acceptance["policy_completion_percent"], 100.0)
            self.assertGreater(acceptance["live_evidence_completion_percent"], 0.0)
            self.assertLess(acceptance["live_evidence_completion_percent"], 100.0)
            self.assertEqual(len(acceptance["blocked_claims"]), 3)

    def test_committed_substrate_outputs_are_current(self) -> None:
        self.assertTrue(check_substrate_outputs(Path(".")))


if __name__ == "__main__":
    unittest.main()
