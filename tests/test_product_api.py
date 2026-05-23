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

    def test_write_snapshot_materializes_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "api.json"

            snapshot = write_snapshot(Path("."), out, "2026-05-23T00:00:00+00:00")

            written = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(written["api_version"], "v1")
            self.assertEqual(written["generated_at"], snapshot["generated_at"])


if __name__ == "__main__":
    unittest.main()
