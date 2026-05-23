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
    target_github_repo,
    v5_live_target_config,
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

    def test_default_live_target_is_edi_product_not_ml_pilot(self) -> None:
        target = v5_live_target_config(Path("."))
        repo = target_github_repo(Path("."))

        self.assertEqual(target["id"], "edi-product")
        self.assertEqual(repo["target_id"], "edi-product")
        self.assertEqual(repo["name_with_owner"], "raghurammutya/engineering-decision-intelligence")

    def test_build_v5_outputs_keeps_live_claims_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "v5"

            result = build_v5_outputs(Path("."), out, "2026-05-23T00:00:00+00:00")

            acceptance = json.loads((out / "exports" / "v5-acceptance-pack.json").read_text(encoding="utf-8"))
            self.assertEqual(result["acceptance"]["acceptance_state"], "tooling_pass_live_evidence_incomplete")
            self.assertEqual(acceptance["tooling_completion_percent"], 100.0)
            self.assertEqual(acceptance["live_claim_completion_percent"], 0.0)
            self.assertEqual(len(acceptance["blocked_claims"]), 5)

    def test_existing_live_evidence_advances_backed_claims(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "v5"
            evidence = {
                "schema_version": 1,
                "generated_at": "2026-05-23T00:00:00+00:00",
                "live_check_requested": True,
                "target": {
                    "target_id": "edi-product",
                    "repo_id": "edi-product",
                    "path": "/home/stocksadmin/workspace/engineering-decision-intelligence",
                    "name_with_owner": "raghurammutya/engineering-decision-intelligence",
                    "remote_detected": True,
                    "role": "product_self_governance",
                },
                "credential_resolution": {
                    "required_count": 5,
                    "resolved_count": 5,
                    "all_required_resolved": True,
                    "secrets_logged": False,
                    "records": [],
                },
                "github_api": {
                    "attempted": True,
                    "rate_limit_http_status": 200,
                    "authenticated": True,
                    "repo_http_status": 200,
                    "default_branch": "main",
                    "branch_protection_http_status": 200,
                    "branch_protection_observed": True,
                    "required_status_checks_observed": True,
                    "pull_request_reviews_observed": False,
                    "actions_runs_http_status": 200,
                    "recent_actions_run_observed": True,
                    "scheduled_connector_workflow_file": ".github/workflows/edi-v5-scheduled-connectors.yml",
                    "scheduled_connector_runs_http_status": 200,
                    "scheduled_connector_observed": True,
                    "scheduled_connector_run": {
                        "workflow_name": "EDI V5 Scheduled Connectors",
                        "workflow_file": ".github/workflows/edi-v5-scheduled-connectors.yml",
                        "target_id": "edi-product",
                        "event": "workflow_dispatch",
                        "status": "completed",
                        "conclusion": "success",
                        "observed_at": "2026-05-23T00:00:00Z",
                        "run_id": "123",
                    },
                },
            }

            result = build_v5_outputs(
                Path("."),
                out,
                "2026-05-23T00:00:00+00:00",
                live_check=True,
                existing_live_evidence=evidence,
            )

            self.assertEqual(result["acceptance"]["live_claim_completion_percent"], 60.0)
            self.assertEqual(result["acceptance"]["blocked_slices"], 6)
            self.assertNotIn("scheduled connectors have run", result["acceptance"]["blocked_claims"])
            self.assertIn("autonomous production enforcement is active", result["acceptance"]["blocked_claims"])

    def test_committed_v5_outputs_are_current(self) -> None:
        self.assertTrue(check_v5_outputs(Path(".")))

    def test_live_check_outputs_are_current(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "v5"

            build_v5_outputs(Path("."), out, "2026-05-23T00:00:00+00:00", live_check=True)

            self.assertTrue(check_v5_outputs(Path("."), out))

    def test_v5_backlog_separates_completed_tooling_from_blocked_live_evidence(self) -> None:
        completed, blocked, total = completed_v5_slices(Path("."))

        self.assertEqual((completed, blocked, total), (4, 6, 10))


if __name__ == "__main__":
    unittest.main()
