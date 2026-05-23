import json
import tempfile
import unittest
from pathlib import Path

from tools.operational_state_scan import (
    decision_clusters,
    decision_priority,
    evidence_quality,
    finding_family,
    GraphJsonBackend,
    load_policy,
    operational_blocker,
    owner_assignment,
    owner_review_class,
    policy_pack_payload,
    pr_file_risk,
    remediation_playbook,
    risk_reduction_score,
    runtime_signal_records,
    runtime_surface_groups,
    scan_file,
    scanner_tuning_candidate,
    write_cicd_event_exports,
    write_cicd_event_summary,
    write_decision_exports,
    write_decision_insight_clusters,
    write_owner_confidence_map,
    write_owner_workflow_exports,
    write_policy_pack_exports,
    write_policy_pack_summary,
    write_graph_outputs,
    write_runtime_signal_exports,
    write_runtime_signal_summary,
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
            echo production
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

    def test_owner_workflow_confidence_separates_declared_inferred_and_missing(self) -> None:
        declared_path = self.write_file(
            "scripts/governance/run_environment_baseline_sync.sh",
            """
            #!/usr/bin/env bash
            ./scripts/governance/promote_by_environment.sh --source dev --target test
            """,
        )
        inferred_path = self.write_file(
            "scripts/apply_service_sql_migrations.sh",
            """
            #!/usr/bin/env bash
            psql "$PROD_DATABASE_URL" -f migrations/latest.sql
            """,
        )
        missing_path = self.write_file(
            "scripts/custom_prod_restart.sh",
            """
            #!/usr/bin/env bash
            docker compose -f docker-compose.prod.yml restart api
            """,
        )
        suggestions = {
            "family_rules": {
                "db_migration_scripts": {
                    "owner": "data-platform",
                    "boundary": "database migration and data mutation",
                }
            }
        }

        declared = scan_file(self.repo, "script", declared_path, self.mapped_policy)
        inferred = scan_file(self.repo, "script", inferred_path, self.policy)
        missing = scan_file(self.repo, "script", missing_path, self.policy)
        out = self.repo / "reports"
        out.mkdir(parents=True, exist_ok=True)

        write_owner_confidence_map(out / "owner-confidence-map.md", [declared, inferred, missing], suggestions, "2026-05-23T00:00:00+00:00")
        write_owner_workflow_exports(out, [declared, inferred, missing], suggestions, "2026-05-23T00:00:00+00:00")

        owner_export = json.loads((out / "exports" / "owner-workflows.json").read_text(encoding="utf-8"))
        report = (out / "owner-confidence-map.md").read_text(encoding="utf-8")

        self.assertEqual(owner_assignment(declared, suggestions)["assignment_type"], "declared_owner_map")
        self.assertEqual(owner_assignment(inferred, suggestions)["assignment_type"], "inferred_suggestion")
        self.assertEqual(owner_assignment(missing, suggestions)["assignment_type"], "missing_owner")
        self.assertEqual(owner_review_class(inferred, suggestions), "inferred-owner-review")
        self.assertEqual(owner_review_class(missing, suggestions), "missing-owner-assignment")
        self.assertEqual(owner_export["record_count"], 3)
        self.assertIn("declared_owner_map", owner_export["assignment_type_counts"])
        self.assertIn("inferred-owner-review", owner_export["review_class_counts"])
        self.assertIn("missing-owner-assignment", owner_export["review_class_counts"])
        self.assertIn("## Lowest-Confidence Owner Decisions", report)

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

    def test_major_family_classifications_are_stable(self) -> None:
        cases = [
            ("scripts/apply_service_sql_migrations.sh", "psql \"$PROD_DATABASE_URL\" -f migration.sql", "db_migration_scripts"),
            ("scripts/sync_broker_orders.py", "print('broker order trading sync')", "broker_order_scripts"),
            ("scripts/update_config_secret.py", "print('secret config update')", "config_secret_scripts"),
            ("scripts/governance/run_runtime_probe.py", "print('runtime probe evidence')", "governance_probes"),
            ("scripts/qa/verify_gateway_route_sync.py", "print('verify route only')", "qa_readiness_checks"),
        ]
        for relative_path, content, expected_family in cases:
            with self.subTest(relative_path=relative_path):
                path = self.write_file(relative_path, content)
                finding = scan_file(self.repo, "script", path, self.mapped_policy)
                self.assertEqual(finding_family(finding), expected_family)

    def test_risk_reasons_explain_classification(self) -> None:
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

        self.assertTrue(any("mutation capability" in reason for reason in finding.risk_reasons))
        self.assertTrue(any("canonical operating path is unknown" in reason for reason in finding.risk_reasons))

    def test_graph_outputs_include_artifact_relationships(self) -> None:
        path = self.write_file("scripts/list_services.py", "print('service inventory')")
        finding = scan_file(self.repo, "script", path, self.policy)
        out = self.repo / "reports"

        write_graph_outputs(out, self.repo, [finding], "2026-05-23T00:00:00+00:00")

        entities = (out / "graph" / "entities.json").read_text(encoding="utf-8")
        relationships = (out / "graph" / "relationships.json").read_text(encoding="utf-8")
        backend = json.loads((out / "graph" / "backend.json").read_text(encoding="utf-8"))
        self.assertIn("scripts/list_services.py", entities)
        self.assertIn("\"relation\": \"contains\"", relationships)
        self.assertEqual(backend["backend_id"], "json-files-v1")
        self.assertEqual(backend["contract_compatibility"], "json_graph_v1")

    def test_graph_backend_preserves_json_contract(self) -> None:
        backend = GraphJsonBackend()
        out = self.repo / "reports"
        entities = {
            "artifact:1": {"id": "artifact:1", "type": "artifact", "path": "scripts/a.sh"},
            "repo:1": {"id": "repo:1", "type": "repo", "name": "repo"},
        }
        relationships = [{"source": "repo:1", "relation": "contains", "target": "artifact:1"}]

        backend.write(out, entities, relationships, "2026-05-23T00:00:00+00:00")

        entity_rows = json.loads((out / "graph" / "entities.json").read_text(encoding="utf-8"))
        relationship_rows = json.loads((out / "graph" / "relationships.json").read_text(encoding="utf-8"))
        metadata = json.loads((out / "graph" / "backend.json").read_text(encoding="utf-8"))
        self.assertEqual([row["type"] for row in entity_rows], ["artifact", "repo"])
        self.assertEqual(relationship_rows, relationships)
        self.assertEqual(metadata["entity_count"], 2)
        self.assertEqual(metadata["relationship_count"], 1)

    def test_graph_v2_outputs_policy_control_decision_relationships(self) -> None:
        path = self.write_file(
            "scripts/apply_service_sql_migrations.sh",
            """
            #!/usr/bin/env bash
            psql "$PROD_DATABASE_URL" -f migrations/latest.sql
            """,
        )
        finding = scan_file(self.repo, "script", path, self.policy)
        out = self.repo / "reports"

        write_graph_outputs(
            out,
            self.repo,
            [finding],
            "2026-05-23T00:00:00+00:00",
            {
                "family_rules": {
                    "db_migration_scripts": {
                        "owner": "data-platform",
                        "boundary": "database migration and data mutation",
                    }
                }
            },
        )

        entities = json.loads((out / "graph" / "entities.json").read_text(encoding="utf-8"))
        relationships = json.loads((out / "graph" / "relationships.json").read_text(encoding="utf-8"))
        entity_types = {entity["type"] for entity in entities}
        relationship_types = {relationship["relation"] for relationship in relationships}

        self.assertIn("policy", entity_types)
        self.assertIn("control", entity_types)
        self.assertIn("decision", entity_types)
        self.assertIn("evidence", entity_types)
        self.assertIn("violates_policy", relationship_types)
        self.assertIn("requires_evidence", relationship_types)
        self.assertIn("suggested_owner", relationship_types)
        self.assertIn("blocked_by_control", relationship_types)

    def test_decision_exports_include_owner_executive_and_remediation_packs(self) -> None:
        path = self.write_file(
            "scripts/apply_service_sql_migrations.sh",
            """
            #!/usr/bin/env bash
            psql "$PROD_DATABASE_URL" -f migrations/latest.sql
            """,
        )
        finding = scan_file(self.repo, "script", path, self.policy)
        out = self.repo / "reports"

        write_decision_exports(out, [finding], "2026-05-23T00:00:00+00:00")

        owner_backlog = json.loads((out / "exports" / "owner-backlog.json").read_text(encoding="utf-8"))
        executive = json.loads((out / "exports" / "executive-decisions.json").read_text(encoding="utf-8"))
        remediation = json.loads((out / "exports" / "remediation-packs.json").read_text(encoding="utf-8"))
        clusters = json.loads((out / "exports" / "decision-clusters.json").read_text(encoding="utf-8"))
        csv_text = (out / "exports" / "owner-backlog.csv").read_text(encoding="utf-8")

        self.assertEqual(owner_backlog["record_count"], 1)
        self.assertEqual(owner_backlog["records"][0]["path"], "scripts/apply_service_sql_migrations.sh")
        self.assertEqual(executive["counts"]["actionable"], 1)
        self.assertEqual(clusters["counts"]["artifacts"], 1)
        self.assertEqual(clusters["counts"]["cluster_count"], 1)
        self.assertEqual(remediation["pack_count"], 1)
        self.assertGreater(remediation["packs"][0]["risk_reduction_score"], 0)
        self.assertIn("priority,action_lane,owner", csv_text)

    def test_decision_clusters_separate_tuning_candidates_from_blockers(self) -> None:
        deploy_path = self.write_file(
            ".github/workflows/deploy-production.yml",
            """
            name: Deploy Production
            jobs:
              deploy:
                steps:
                  - run: docker compose -f docker-compose.prod.yml up -d
            """,
        )
        qa_path = self.write_file(
            "scripts/qa/check_prod_deploy_report.sh",
            """
            #!/usr/bin/env bash
            kubectl get deployments
            echo "validate production deploy report"
            """,
        )

        deploy = scan_file(self.repo, "workflow", deploy_path, self.policy)
        qa = scan_file(self.repo, "script", qa_path, self.policy)
        clusters = decision_clusters([deploy, qa])
        out = self.repo / "reports"
        out.mkdir(parents=True, exist_ok=True)

        write_decision_insight_clusters(out / "decision-insight-clusters.md", [deploy, qa], "2026-05-23T00:00:00+00:00")
        write_decision_exports(out, [deploy, qa], "2026-05-23T00:00:00+00:00")

        cluster_export = json.loads((out / "exports" / "decision-clusters.json").read_text(encoding="utf-8"))
        remediation = json.loads((out / "exports" / "remediation-packs.json").read_text(encoding="utf-8"))
        report = (out / "decision-insight-clusters.md").read_text(encoding="utf-8")

        self.assertTrue(operational_blocker(deploy))
        self.assertFalse(scanner_tuning_candidate(deploy))
        self.assertTrue(scanner_tuning_candidate(qa))
        self.assertFalse(operational_blocker(qa))
        self.assertGreater(risk_reduction_score(deploy), risk_reduction_score(qa))
        self.assertEqual(cluster_export["counts"]["artifacts"], 2)
        self.assertEqual(cluster_export["counts"]["cluster_count"], len(clusters))
        self.assertEqual(cluster_export["counts"]["scanner_tuning_candidates"], 1)
        self.assertEqual(cluster_export["counts"]["operational_blockers"], 1)
        self.assertGreaterEqual(remediation["packs"][0]["risk_reduction_score"], remediation["packs"][-1]["risk_reduction_score"])
        self.assertIn("## Scanner Tuning Candidates", report)
        self.assertIn("## Operational Blockers", report)

    def test_cicd_event_exports_separate_deploy_and_validation_workflows(self) -> None:
        deploy_path = self.write_file(
            ".github/workflows/deploy-production.yml",
            """
            name: Deploy Production
            on:
              workflow_dispatch:
            jobs:
              deploy:
                environment: production
                steps:
                  - run: ./scripts/governance/promote_by_environment.sh --source staging --target prod
            """,
        )
        validation_path = self.write_file(
            ".github/workflows/promotion-preflight.yml",
            """
            name: Promotion Preflight
            on:
              pull_request:
            jobs:
              check:
                steps:
                  - run: echo production deployment readiness only
            """,
        )
        deploy = scan_file(self.repo, "workflow", deploy_path, self.policy)
        validation = scan_file(self.repo, "workflow", validation_path, self.mapped_policy)
        gh_state = {
            "workflows": [
                {"path": ".github/workflows/deploy-production.yml", "state": "active"},
                {"path": ".github/workflows/remote-only.yml", "state": "active"},
            ]
        }
        out = self.repo / "reports"
        out.mkdir(parents=True, exist_ok=True)

        write_cicd_event_summary(out / "cicd-event-summary.md", [deploy, validation], gh_state, "2026-05-23T00:00:00+00:00")
        write_cicd_event_exports(out, [deploy, validation], gh_state, "2026-05-23T00:00:00+00:00")

        payload = json.loads((out / "exports" / "cicd-events.json").read_text(encoding="utf-8"))
        report = (out / "cicd-event-summary.md").read_text(encoding="utf-8")

        self.assertEqual(payload["record_count"], 2)
        self.assertEqual(payload["surface_class_counts"]["deployment_capable"], 1)
        self.assertEqual(payload["surface_class_counts"]["validation_only"], 1)
        self.assertEqual(payload["deployment_capable"][0]["path"], ".github/workflows/deploy-production.yml")
        self.assertIn(".github/workflows/remote-only.yml", payload["remote_only_workflows"])
        self.assertIn("## Deployment-Capable Workflows", report)
        self.assertIn("## Validation-Only Workflows", report)

    def test_runtime_signal_exports_group_inferred_surfaces(self) -> None:
        db_path = self.write_file(
            "scripts/apply_service_sql_migrations.sh",
            """
            #!/usr/bin/env bash
            echo production
            psql "$PROD_DATABASE_URL" -f migrations/latest.sql
            """,
        )
        config_path = self.write_file(
            "scripts/apply_staging_config.sh",
            """
            #!/usr/bin/env bash
            echo "apply staging config"
            """,
        )
        db = scan_file(self.repo, "script", db_path, self.policy)
        config = scan_file(self.repo, "script", config_path, self.policy)
        out = self.repo / "reports"
        out.mkdir(parents=True, exist_ok=True)

        write_runtime_signal_summary(out / "runtime-signal-summary.md", [db, config], "2026-05-23T00:00:00+00:00")
        write_runtime_signal_exports(out, [db, config], "2026-05-23T00:00:00+00:00")

        payload = json.loads((out / "exports" / "runtime-signals.json").read_text(encoding="utf-8"))
        report = (out / "runtime-signal-summary.md").read_text(encoding="utf-8")
        records = runtime_signal_records([db, config])
        groups = runtime_surface_groups(records)

        self.assertFalse(payload["runtime_observed"])
        self.assertEqual(payload["signal_source"], "scanner_inference")
        self.assertEqual(payload["record_count"], len(records))
        self.assertEqual(payload["surface_group_count"], len(groups))
        self.assertIn("prod", payload["environment_counts"])
        self.assertIn("database", payload["mutation_counts"])
        self.assertIn("inferred from repository artifacts", report.lower())
        self.assertIn("## Runtime Surface Groups", report)

    def test_policy_pack_exports_separate_reusable_policy_sections(self) -> None:
        policy = {
            "canonical_commands": ["scripts/envctl.sh"],
            "canonical_artifacts": [{"pattern": "scripts/envctl.sh", "status": "canonical"}],
            "owner_map": [{"pattern": "scripts/envctl.sh", "owner": "platform", "boundary": "environment lifecycle"}],
            "accepted_exceptions": [{"pattern": ".github/workflows/preflight.yml", "reason": "readiness only"}],
            "readonly_patterns": ["scripts/check_*"],
            "autonomy": {"default_by_risk": {"critical": "blocked"}},
        }
        suggestions = {
            "family_rules": {
                "deploy_workflows": {"owner": "platform", "boundary": "deployment"}
            },
            "path_rules": [
                {"pattern": ".github/workflows/*.yml", "owner": "platform", "boundary": "workflow governance"}
            ],
        }
        out = self.repo / "reports"
        out.mkdir(parents=True, exist_ok=True)

        write_policy_pack_summary(out / "policy-pack-summary.md", policy, None, suggestions, "2026-05-23T00:00:00+00:00")
        write_policy_pack_exports(out, policy, None, suggestions, "2026-05-23T00:00:00+00:00")

        payload = json.loads((out / "exports" / "policy-pack.json").read_text(encoding="utf-8"))
        report = (out / "policy-pack-summary.md").read_text(encoding="utf-8")
        raw_payload = policy_pack_payload(policy, None, suggestions, "2026-05-23T00:00:00+00:00")

        self.assertEqual(payload["pack_id"], "scanner-operational-safety-v1")
        self.assertEqual(payload["counts"]["canonical_commands"], 1)
        self.assertEqual(payload["counts"]["owner_rules"], 1)
        self.assertEqual(payload["counts"]["owner_suggestion_rules"], 2)
        self.assertEqual(payload["counts"]["accepted_exceptions"], 1)
        self.assertEqual(payload["counts"]["readonly_patterns"], 1)
        self.assertEqual(payload["counts"], raw_payload["counts"])
        self.assertIn("## Canonical Commands", report)
        self.assertIn("## Owner Rules", report)
        self.assertIn("## Accepted Exceptions", report)


if __name__ == "__main__":
    unittest.main()
