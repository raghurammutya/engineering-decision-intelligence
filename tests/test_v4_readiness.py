import json
import tempfile
import unittest
from pathlib import Path

from edi.v4 import (
    build_v4_outputs,
    check_v4_outputs,
    completed_v4_slices,
    live_connector_payload,
    ci_enforcement_payload,
)


class V4ReadinessTests(unittest.TestCase):
    def test_live_connector_payload_declares_boundary(self) -> None:
        payload = live_connector_payload(Path("."), "2026-05-23T00:00:00+00:00")

        self.assertGreaterEqual(payload["connector_count"], 6)
        self.assertEqual(payload["claim_boundary"], "configured_for_install_not_authenticated_live_polling")

    def test_ci_enforcement_payload_is_ready_for_pr_check_install(self) -> None:
        payload = ci_enforcement_payload(Path("."), "2026-05-23T00:00:00+00:00")

        self.assertEqual(payload["target_state"], "ready_for_pr_check_install")
        self.assertTrue(payload["blocking_modes"])

    def test_build_v4_outputs_materializes_acceptance_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "v4"

            result = build_v4_outputs(Path("."), out, "2026-05-23T00:00:00+00:00")

            acceptance = json.loads((out / "exports" / "v4-acceptance-pack.json").read_text(encoding="utf-8"))
            self.assertEqual(result["acceptance"]["acceptance_state"], "pass")
            self.assertEqual(acceptance["completed_slices"], 10)
            self.assertIn("target repositories enforcing PR checks", acceptance["blocked_claims"])

    def test_committed_v4_outputs_are_current(self) -> None:
        self.assertTrue(check_v4_outputs(Path(".")))

    def test_v4_backlog_is_complete(self) -> None:
        completed, total = completed_v4_slices(Path("."))

        self.assertEqual((completed, total), (10, 10))


if __name__ == "__main__":
    unittest.main()
