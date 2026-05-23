import json
import tempfile
import unittest
from pathlib import Path

from edi.v5 import (
    build_v5_outputs,
    check_v5_outputs,
    completed_v5_slices,
    onepassword_installation_payload,
    secret_flow_payload,
)


class V5TargetInstallationTests(unittest.TestCase):
    def test_onepassword_install_check_does_not_read_secrets(self) -> None:
        payload = onepassword_installation_payload(Path("."), "2026-05-23T00:00:00+00:00")

        self.assertTrue(payload["op_installed"])
        self.assertFalse(payload["secrets_read"])
        self.assertFalse(payload["vaults_listed"])
        self.assertFalse(payload["items_listed"])

    def test_secret_flow_uses_op_references_only(self) -> None:
        payload = secret_flow_payload(Path("."), "2026-05-23T00:00:00+00:00")

        self.assertGreaterEqual(payload["secret_reference_count"], 5)
        self.assertEqual(payload["invalid_secret_references"], [])
        self.assertFalse(payload["plaintext_secret_values_committed"])

    def test_build_v5_outputs_keeps_live_claims_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "v5"

            result = build_v5_outputs(Path("."), out, "2026-05-23T00:00:00+00:00")

            acceptance = json.loads((out / "exports" / "v5-acceptance-pack.json").read_text(encoding="utf-8"))
            self.assertEqual(result["acceptance"]["acceptance_state"], "tooling_pass_live_evidence_incomplete")
            self.assertEqual(acceptance["tooling_completion_percent"], 100.0)
            self.assertEqual(acceptance["live_claim_completion_percent"], 0.0)
            self.assertEqual(len(acceptance["blocked_claims"]), 5)

    def test_committed_v5_outputs_are_current(self) -> None:
        self.assertTrue(check_v5_outputs(Path(".")))

    def test_v5_backlog_separates_completed_tooling_from_blocked_live_evidence(self) -> None:
        completed, blocked, total = completed_v5_slices(Path("."))

        self.assertEqual((completed, blocked, total), (4, 6, 10))


if __name__ == "__main__":
    unittest.main()
