import json
import tempfile
import unittest
from pathlib import Path

from edi.v2 import (
    build_v2_outputs,
    check_v2_outputs,
    completed_v2_slices,
    portfolio_payload,
    runtime_connector_payload,
)


class V2OperationalIntelligenceTests(unittest.TestCase):
    def test_portfolio_payload_reads_multiple_repositories(self) -> None:
        payload = portfolio_payload(Path("."), "2026-05-23T00:00:00+00:00")

        self.assertGreaterEqual(payload["repo_count"], 2)
        self.assertGreater(payload["total_artifacts"], 0)
        self.assertTrue(any(record["repo_id"] == "ml-pilot" for record in payload["records"]))

    def test_runtime_connector_contract_stays_fixture_bounded(self) -> None:
        payload = runtime_connector_payload(Path("."), "2026-05-23T00:00:00+00:00")

        self.assertEqual(payload["contract_state"], "pass")
        self.assertEqual(payload["source_boundary"], "static_fixture_contract_not_live_runtime_truth")
        self.assertGreater(payload["record_count"], 0)

    def test_build_v2_outputs_materializes_acceptance_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "v2"

            result = build_v2_outputs(Path("."), out, "2026-05-23T00:00:00+00:00")

            acceptance = json.loads((out / "exports" / "v2-acceptance-pack.json").read_text(encoding="utf-8"))
            self.assertEqual(result["acceptance"]["acceptance_state"], "pass")
            self.assertEqual(acceptance["completed_slices"], 10)
            self.assertTrue((out / "portfolio-operator-view.html").exists())

    def test_committed_v2_outputs_are_current(self) -> None:
        self.assertTrue(check_v2_outputs(Path(".")))

    def test_v2_backlog_is_complete(self) -> None:
        completed, total = completed_v2_slices(Path("."))

        self.assertEqual((completed, total), (10, 10))


if __name__ == "__main__":
    unittest.main()
