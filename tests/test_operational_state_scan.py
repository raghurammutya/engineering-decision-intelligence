import tempfile
import unittest
from pathlib import Path

from tools.operational_state_scan import (
    decision_priority,
    evidence_quality,
    finding_family,
    load_policy,
    pr_file_risk,
    remediation_playbook,
    scan_file,
)


class OperationalStateScanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        (self.repo / "scripts" / "governance").mkdir(parents=True)
        (self.repo / ".github" / "workflows").mkdir(parents=True)
        self.policy = load_policy(None)
        self.mapped_policy = load_policy(None)
        self.mapped_policy.update(
            {
                "owner_map": [
                    {
                        "pattern": "scripts/governance/*.sh",
                        "owner": "platform-governance",
                        "boundary": "governance automation",
                    }
                ],
                "accepted_exceptions": [
                    {
                        "pattern": ".github/workflows/promotion-preflight.yml",
                        "reason": "readiness gate only",
                    }
                ],
                "readonly_patterns": [
                    ".github/workflows/*preflight*.yml",
                    "scripts/validate_*",
                ],
                "canonical_artifacts": [
                    {
                        "pattern": ".github/workflows/promotion-preflight.yml",
                        "status": "accepted_exception",
                    }
                ],
            }
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write_file(self, relative_path: str, content: str) -> Path:
        path = self.repo / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_direct_prod_deploy_is_blocked(self) -> None:
        path = self.write_file(
            ".github/workflows/deploy-production.yml",
            """
            name: Deploy Production
            jobs:
              deploy:
                steps:
                  - run: docker compose -f docker-compose.prod.yml up -d
            """,
        )

        finding = scan_file(self.repo, "workflow", path, self.policy)

        self.assertEqual(finding.risk_level, "critical")
        self.assertEqual(finding.autonomy_mode, "blocked")
        self.assertEqual(finding.canonical_status, "non_canonical_or_unknown")

    def test_canonical_promotion_with_evidence_is_controlled_execute(self) -> None:
        path = self.write_file(
            ".github/workflows/promote-environments.yml",
            """
            name: Promote Environments
            jobs:
              promote:
                steps:
                  - run: ./scripts/governance/promote_by_environment.sh --source staging --target prod --build
                  - run: echo deployment-reports/promotion-evidence.md
            """,
        )

        finding = scan_file(self.repo, "workflow", path, self.policy)

        self.assertEqual(finding.risk_level, "high")
        self.assertEqual(finding.autonomy_mode, "controlled_execute")
        self.assertEqual(finding.canonical_status, "uses_canonical_command")

    def test_read_only_validation_is_not_critical(self) -> None:
        path = self.write_file(
            "scripts/validate_config_service_uniqueness.py",
            """
            # validates production config references without writing
            print("checking database schema and config only")
            """,
        )

        finding = scan_file(self.repo, "script", path, self.policy)

        self.assertEqual(finding.intent, "validation_or_reporting")
        self.assertIn(finding.risk_level, {"low", "medium"})
        self.assertNotEqual(finding.autonomy_mode, "blocked")

    def test_db_migration_script_requires_review_or_block(self) -> None:
        path = self.write_file(
            "scripts/apply_service_sql_migrations.sh",
            """
            #!/usr/bin/env bash
            psql "$PROD_DATABASE_URL" -f migrations/latest.sql
            """,
        )

        finding = scan_file(self.repo, "script", path, self.policy)

        self.assertIn(finding.risk_level, {"critical", "high"})
        self.assertIn(finding.autonomy_mode, {"blocked", "prepare"})
        self.assertIn("database", finding.mutation_types)

    def test_non_mutation_script_observes_only(self) -> None:
        path = self.write_file(
            "scripts/list_services.py",
            """
            print("service inventory")
            """,
        )

        finding = scan_file(self.repo, "script", path, self.policy)

        self.assertEqual(finding.risk_level, "low")
        self.assertEqual(finding.autonomy_mode, "observe")
        self.assertEqual(finding.canonical_status, "not_mutation_capable")

    def test_owner_map_assigns_owner_boundary(self) -> None:
        path = self.write_file(
            "scripts/governance/run_environment_baseline_sync.sh",
            """
            #!/usr/bin/env bash
            echo deployment-reports/baseline.md
            ./scripts/governance/promote_by_environment.sh --source dev --target test
            """,
        )

        finding = scan_file(self.repo, "script", path, self.mapped_policy)

        self.assertEqual(finding.owner_status, "present")
        self.assertEqual(finding.owner, "platform-governance")
        self.assertEqual(finding.owner_boundary, "governance automation")

    def test_accepted_exception_remains_visible_but_not_blocked_when_readonly(self) -> None:
        path = self.write_file(
            ".github/workflows/promotion-preflight.yml",
            """
            name: Promotion Preflight
            jobs:
              check:
                steps:
                  - run: echo production deployment readiness only
            """,
        )

        finding = scan_file(self.repo, "workflow", path, self.mapped_policy)

        self.assertEqual(finding.exception_status, "accepted_exception")
        self.assertEqual(finding.canonical_status, "accepted_exception")
        self.assertEqual(finding.intent, "validation_or_reporting")
        self.assertNotEqual(finding.autonomy_mode, "blocked")

    def test_evidence_quality_classifies_promotion_and_rollback(self) -> None:
        self.assertEqual(
            evidence_quality("echo deployment-reports/prod.md", "scripts/deploy.sh", "present"),
            "promotion_evidence",
        )
        self.assertEqual(
            evidence_quality("echo rollback evidence", "scripts/deploy.sh", "present"),
            "rollback_evidence",
        )
        self.assertEqual(evidence_quality("", "scripts/deploy.sh", "missing"), "missing")

    def test_decision_priority_calibrates_prod_block_as_p0(self) -> None:
        path = self.write_file(
            ".github/workflows/deploy-production.yml",
            """
            name: Deploy Production
            jobs:
              deploy:
                steps:
                  - run: docker compose -f docker-compose.prod.yml up -d
            """,
        )

        finding = scan_file(self.repo, "workflow", path, self.policy)

        self.assertEqual(decision_priority(finding), "P0")

    def test_pr_file_risk_flags_policy_and_workflow_changes(self) -> None:
        self.assertEqual(pr_file_risk("policies/ml-pilot-policy.json", {})[0], "P1")
        self.assertEqual(pr_file_risk(".github/workflows/deploy-production.yml", {})[0], "P1")
        self.assertEqual(pr_file_risk("tools/operational_state_scan.py", {})[0], "P2")

    def test_family_and_playbook_for_prod_deploy(self) -> None:
        path = self.write_file(
            ".github/workflows/deploy-production.yml",
            """
            name: Deploy Production
            jobs:
              deploy:
                steps:
                  - run: docker compose -f docker-compose.prod.yml up -d
            """,
        )

        finding = scan_file(self.repo, "workflow", path, self.policy)

        self.assertEqual(finding_family(finding), "deploy_workflows")
        self.assertIn("direct-prod-deploy-workflow.md", remediation_playbook(finding))


if __name__ == "__main__":
    unittest.main()
