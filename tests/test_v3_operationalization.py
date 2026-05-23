import json
import tempfile
import unittest
from pathlib import Path

from edi.v3 import (
    build_v3_outputs,
    check_v3_outputs,
    completed_v3_slices,
    connector_ingestion_payload,
    reconciliation_payload,
)


class V3OperationalizationTests(unittest.TestCase):
    def test_connector_ingestion_reads_dedicated_inputs(self) -> None:
        payload = connector_ingestion_payload(Path("."), "2026-05-23T00:00:00+00:00")

        self.assertGreaterEqual(payload["connector_count"], 6)
        self.assertGreater(payload["total_records"], 0)
        self.assertEqual(payload["source_boundary"], "imported_connector_payloads_not_live_polling")

    def test_reconciliation_payload_has_decision_loops(self) -> None:
        payload = reconciliation_payload(Path("."), "2026-05-23T00:00:00+00:00")

        self.assertGreaterEqual(payload["loop_count"], 4)
        self.assertIn("divergence_count", payload)

    def test_build_v3_outputs_materializes_acceptance_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "v3"

            result = build_v3_outputs(Path("."), out, "2026-05-23T00:00:00+00:00")

            acceptance = json.loads((out / "exports" / "v3-acceptance-pack.json").read_text(encoding="utf-8"))
            self.assertEqual(result["acceptance"]["acceptance_state"], "pass")
            self.assertEqual(acceptance["completed_slices"], 10)
            self.assertTrue((out / "v3-operator-view.html").exists())

    def test_committed_v3_outputs_are_current(self) -> None:
        self.assertTrue(check_v3_outputs(Path(".")))

    def test_v3_backlog_is_complete(self) -> None:
        completed, total = completed_v3_slices(Path("."))

        self.assertEqual((completed, total), (10, 10))


if __name__ == "__main__":
    unittest.main()
