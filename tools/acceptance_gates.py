#!/usr/bin/env python3
"""Run deterministic acceptance gates for generated product outputs."""

from __future__ import annotations

import json
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_REPORTS = {
    "reports/ml-pilot": [
        "manifest.json",
        "decision-backlog.md",
        "decision-insight-clusters.md",
        "scanner-tuning-pack.md",
        "owner-confidence-map.md",
        "cicd-event-summary.md",
        "runtime-signal-summary.md",
        "telemetry-correlation-summary.md",
        "ai-agent-capability-summary.md",
        "agent-drift-eval-summary.md",
        "agent-semantic-classifier-summary.md",
        "review-state-summary.md",
        "review-workflow-summary.md",
        "github-pr-event-summary.md",
        "github-actions-run-summary.md",
        "deployment-event-evidence-summary.md",
        "baseline-trend-v2.md",
        "v1.5-acceptance-pack.md",
        "policy-pack-summary.md",
        "onboarding-summary.md",
        "risk-explanation-map.md",
        "graph/entities.json",
        "graph/relationships.json",
        "graph/backend.json",
        "exports/owner-backlog.json",
        "exports/owner-backlog.csv",
        "exports/owner-workflows.json",
        "exports/cicd-events.json",
        "exports/runtime-signals.json",
        "exports/telemetry-correlations.json",
        "exports/ai-agent-capabilities.json",
        "exports/agent-drift-evals.json",
        "exports/agent-semantic-classifier.json",
        "exports/review-state.json",
        "exports/review-workflows.json",
        "exports/github-pr-events.json",
        "exports/github-actions-runs.json",
        "exports/deployment-event-evidence.json",
        "exports/baseline-trend-v2.json",
        "exports/v1.5-acceptance-pack.json",
        "exports/policy-pack.json",
        "exports/onboarding.json",
        "exports/executive-decisions.json",
        "exports/decision-clusters.json",
        "exports/scanner-tuning-pack.json",
        "exports/remediation-packs.json",
    ],
    "reports/self": [
        "manifest.json",
        "decision-backlog.md",
        "decision-insight-clusters.md",
        "scanner-tuning-pack.md",
        "owner-confidence-map.md",
        "cicd-event-summary.md",
        "runtime-signal-summary.md",
        "telemetry-correlation-summary.md",
        "ai-agent-capability-summary.md",
        "agent-drift-eval-summary.md",
        "agent-semantic-classifier-summary.md",
        "review-state-summary.md",
        "review-workflow-summary.md",
        "github-pr-event-summary.md",
        "github-actions-run-summary.md",
        "deployment-event-evidence-summary.md",
        "baseline-trend-v2.md",
        "v1.5-acceptance-pack.md",
        "policy-pack-summary.md",
        "onboarding-summary.md",
        "risk-explanation-map.md",
        "graph/entities.json",
        "graph/relationships.json",
        "graph/backend.json",
        "exports/owner-backlog.json",
        "exports/owner-backlog.csv",
        "exports/owner-workflows.json",
        "exports/cicd-events.json",
        "exports/runtime-signals.json",
        "exports/telemetry-correlations.json",
        "exports/ai-agent-capabilities.json",
        "exports/agent-drift-evals.json",
        "exports/agent-semantic-classifier.json",
        "exports/review-state.json",
        "exports/review-workflows.json",
        "exports/github-pr-events.json",
        "exports/github-actions-runs.json",
        "exports/deployment-event-evidence.json",
        "exports/baseline-trend-v2.json",
        "exports/v1.5-acceptance-pack.json",
        "exports/policy-pack.json",
        "exports/onboarding.json",
        "exports/executive-decisions.json",
        "exports/decision-clusters.json",
        "exports/scanner-tuning-pack.json",
        "exports/remediation-packs.json",
    ],
    "reports/product": [
        "progress.md",
        "progress.json",
        "next-mission-checklist.md",
        "next-mission.json",
        "api-snapshot.json",
        "operator-view.html",
    ],
    "reports/product/v2": [
        "README.md",
        "portfolio-summary.md",
        "runtime-connector-contract.md",
        "incident-correlation-summary.md",
        "closed-loop-remediation-summary.md",
        "policy-preflight-summary.md",
        "portfolio-operator-view.html",
        "trust-confidence-summary.md",
        "evidence-lineage-summary.md",
        "connector-sdk-summary.md",
        "v2-acceptance-pack.md",
        "exports/portfolio-summary.json",
        "exports/runtime-connector-contract.json",
        "exports/incident-correlations.json",
        "exports/closed-loop-remediation.json",
        "exports/policy-preflight.json",
        "exports/trust-confidence.json",
        "exports/evidence-lineage.json",
        "exports/connector-sdk.json",
        "exports/v2-acceptance-pack.json",
    ],
    "reports/product/v3": [
        "README.md",
        "connector-ingestion-summary.md",
        "reconciliation-loop-summary.md",
        "portfolio-onboarding-summary.md",
        "evidence-lineage-v3-summary.md",
        "remediation-workflow-summary.md",
        "policy-preflight-ci-summary.md",
        "product-ux-summary.md",
        "reusable-packaging-summary.md",
        "external-pilot-readiness.md",
        "v3-operator-view.html",
        "v3-acceptance-pack.md",
        "exports/connector-ingestion.json",
        "exports/reconciliation-loops.json",
        "exports/portfolio-onboarding.json",
        "exports/evidence-lineage-v3.json",
        "exports/remediation-workflow.json",
        "exports/policy-preflight-ci.json",
        "exports/product-ux.json",
        "exports/reusable-packaging.json",
        "exports/external-pilot-readiness.json",
        "exports/v3-acceptance-pack.json",
    ],
    "reports/product/v4": [
        "README.md",
        "live-connector-readiness.md",
        "continuous-reconciliation-summary.md",
        "ci-pr-enforcement-summary.md",
        "remediation-operations-summary.md",
        "security-access-summary.md",
        "persistence-history-summary.md",
        "deployment-packaging-summary.md",
        "operational-slo-summary.md",
        "external-pilot-operations.md",
        "v4-operator-view.html",
        "v4-acceptance-pack.md",
        "exports/live-connector-readiness.json",
        "exports/continuous-reconciliation.json",
        "exports/ci-pr-enforcement.json",
        "exports/remediation-operations.json",
        "exports/security-access.json",
        "exports/persistence-history.json",
        "exports/deployment-packaging.json",
        "exports/operational-slos.json",
        "exports/external-pilot-operations.json",
        "exports/v4-acceptance-pack.json",
    ],
    "reports/product/v5": [
        "README.md",
        "onepassword-installation.md",
        "onepassword-secret-flow.md",
        "live-evidence-intake.md",
        "runtime-truth-completeness.md",
        "autonomous-enforcement.md",
        "live-evidence-claims.md",
        "v5-acceptance-pack.md",
        "exports/onepassword-installation.json",
        "exports/onepassword-secret-flow.json",
        "exports/v5-live-evidence.json",
        "exports/runtime-truth-completeness.json",
        "exports/autonomous-enforcement.json",
        "exports/live-evidence-claims.json",
        "exports/v5-acceptance-pack.json",
    ],
}
REQUIRED_GRAPH_ENTITY_TYPES = {"artifact", "control", "decision", "evidence", "policy", "repo"}
REQUIRED_GRAPH_RELATIONSHIPS = {
    "blocked_by_control",
    "has_decision",
    "requires_evidence",
    "suggested_owner",
    "violates_policy",
}


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def check_cli_contracts() -> None:
    commands = [
        ([sys.executable, "-m", "edi", "progress", "--dry-run"], "tools/autopilot_progress.py"),
        ([sys.executable, "-m", "edi", "progress", "--check", "--dry-run"], "--check"),
        ([sys.executable, "-m", "edi", "scan", "--repo", "/tmp/example", "--out", "reports/example", "--dry-run"], "tools/operational_state_scan.py"),
        ([sys.executable, "-m", "edi", "autopilot", "checklist", "--dry-run"], "--checklist"),
        ([sys.executable, "-m", "edi", "api", "snapshot", "--dry-run"], "api-snapshot.json"),
        ([sys.executable, "-m", "edi", "ui", "build", "--dry-run"], "operator-view.html"),
        ([sys.executable, "-m", "edi", "v2", "build", "--dry-run"], "v2 operational intelligence"),
        ([sys.executable, "-m", "edi", "v3", "build", "--dry-run"], "v3 operationalization"),
        ([sys.executable, "-m", "edi", "v4", "build", "--dry-run"], "v4 live enforcement readiness"),
        ([sys.executable, "-m", "edi", "v5", "build", "--dry-run"], "v5 target installation"),
    ]
    for command, expected in commands:
        result = run_command(command)
        require(result.returncode == 0, f"CLI dry-run command failed: {' '.join(command)}\n{result.stderr}")
        require(expected in result.stdout, f"CLI dry-run output missing {expected!r}: {' '.join(command)}")

    result = run_command([sys.executable, "-m", "edi", "autopilot", "next", "--json"])
    require(result.returncode == 0, f"autopilot next --json failed: {result.stderr}")
    payload = json.loads(result.stdout)
    require(payload.get("safe_mode") == "plan_only", "autopilot next --json must remain plan_only")
    if payload.get("mission") is not None:
        require("/home/stocksadmin/workspace/ML/**" in payload.get("blocked_paths", []), "autopilot plan must block ML writes")


def check_report_contracts() -> None:
    for report_dir, filenames in REQUIRED_REPORTS.items():
        base = ROOT / report_dir
        for filename in filenames:
            path = base / filename
            require(path.exists(), f"missing required report: {path}")
            require(path.stat().st_size > 0, f"empty required report: {path}")

    progress = load_json(ROOT / "reports" / "product" / "progress.json")
    next_mission = load_json(ROOT / "reports" / "product" / "next-mission.json")
    require(progress["completion"]["completion_percent"] > 0, "product progress percent must be positive")
    require(next_mission["safe_mode"] == "plan_only", "next mission must remain plan-only")
    if next_mission.get("mission") is not None:
        require("/home/stocksadmin/workspace/ML/**" in next_mission["blocked_paths"], "next mission must block ML writes")


def check_graph_contract(report_dir: str, require_full_relationships: bool) -> None:
    base = ROOT / report_dir / "graph"
    entities = load_json(base / "entities.json")
    relationships = load_json(base / "relationships.json")
    backend = load_json(base / "backend.json")
    entity_types = {entity.get("type") for entity in entities}
    relationship_types = {relationship.get("relation") for relationship in relationships}
    missing_entity_types = REQUIRED_GRAPH_ENTITY_TYPES - entity_types
    require(not missing_entity_types, f"{report_dir} graph missing entity types: {sorted(missing_entity_types)}")
    require(backend.get("backend_id") == "json-files-v1", f"{report_dir} graph backend must be json-files-v1")
    require(backend.get("contract_compatibility") == "json_graph_v1", f"{report_dir} graph contract compatibility mismatch")
    require(backend.get("entity_count") == len(entities), f"{report_dir} graph backend entity count mismatch")
    require(backend.get("relationship_count") == len(relationships), f"{report_dir} graph backend relationship count mismatch")
    if require_full_relationships:
        missing_relationships = REQUIRED_GRAPH_RELATIONSHIPS - relationship_types
        require(not missing_relationships, f"{report_dir} graph missing relationships: {sorted(missing_relationships)}")


def check_graph_contracts() -> None:
    check_graph_contract("reports/ml-pilot", require_full_relationships=True)
    check_graph_contract("reports/self", require_full_relationships=False)


def check_export_contract(report_dir: str) -> None:
    base = ROOT / report_dir / "exports"
    owner_backlog = load_json(base / "owner-backlog.json")
    owner_workflows = load_json(base / "owner-workflows.json")
    cicd_events = load_json(base / "cicd-events.json")
    runtime_signals = load_json(base / "runtime-signals.json")
    telemetry = load_json(base / "telemetry-correlations.json")
    agent_capabilities = load_json(base / "ai-agent-capabilities.json")
    agent_drift = load_json(base / "agent-drift-evals.json")
    agent_semantic = load_json(base / "agent-semantic-classifier.json")
    review_state = load_json(base / "review-state.json")
    review_workflows = load_json(base / "review-workflows.json")
    pr_events = load_json(base / "github-pr-events.json")
    action_runs = load_json(base / "github-actions-runs.json")
    deployment_evidence = load_json(base / "deployment-event-evidence.json")
    baseline_trend = load_json(base / "baseline-trend-v2.json")
    v1_5_acceptance = load_json(base / "v1.5-acceptance-pack.json")
    policy_pack = load_json(base / "policy-pack.json")
    onboarding = load_json(base / "onboarding.json")
    executive = load_json(base / "executive-decisions.json")
    clusters = load_json(base / "decision-clusters.json")
    scanner_tuning = load_json(base / "scanner-tuning-pack.json")
    remediation = load_json(base / "remediation-packs.json")

    require(isinstance(owner_backlog.get("records"), list), f"{report_dir} owner backlog records must be a list")
    require(owner_backlog.get("record_count") == len(owner_backlog["records"]), f"{report_dir} owner backlog count mismatch")
    require(isinstance(owner_workflows.get("records"), list), f"{report_dir} owner workflow records must be a list")
    require(
        owner_workflows.get("record_count") == len(owner_workflows["records"]),
        f"{report_dir} owner workflow count mismatch",
    )
    require(
        isinstance(owner_workflows.get("assignment_type_counts"), dict),
        f"{report_dir} owner workflow assignment counts must be present",
    )
    require(
        isinstance(owner_workflows.get("review_class_counts"), dict),
        f"{report_dir} owner workflow review class counts must be present",
    )
    require(isinstance(cicd_events.get("records"), list), f"{report_dir} CI/CD event records must be a list")
    require(cicd_events.get("record_count") == len(cicd_events["records"]), f"{report_dir} CI/CD event count mismatch")
    require(
        isinstance(cicd_events.get("surface_class_counts"), dict),
        f"{report_dir} CI/CD surface class counts must be present",
    )
    require(
        isinstance(cicd_events.get("deployment_capable"), list),
        f"{report_dir} deployment-capable workflow records must be a list",
    )
    require(
        isinstance(cicd_events.get("validation_only"), list),
        f"{report_dir} validation-only workflow records must be a list",
    )
    require(isinstance(runtime_signals.get("records"), list), f"{report_dir} runtime signal records must be a list")
    require(
        runtime_signals.get("record_count") == len(runtime_signals["records"]),
        f"{report_dir} runtime signal count mismatch",
    )
    require(runtime_signals.get("runtime_observed") is False, f"{report_dir} runtime signals must be inference-only")
    require(
        runtime_signals.get("signal_source") == "scanner_inference",
        f"{report_dir} runtime signal source must be scanner_inference",
    )
    require(
        isinstance(runtime_signals.get("surface_groups"), list),
        f"{report_dir} runtime surface groups must be a list",
    )
    require(
        runtime_signals.get("surface_group_count") == len(runtime_signals["surface_groups"]),
        f"{report_dir} runtime surface group count mismatch",
    )
    require(isinstance(telemetry.get("records"), list), f"{report_dir} telemetry correlation records must be a list")
    require(telemetry.get("record_count") == len(telemetry["records"]), f"{report_dir} telemetry correlation count mismatch")
    require(
        telemetry.get("observed_telemetry_ingested") is False,
        f"{report_dir} telemetry correlations must declare observed telemetry is not ingested",
    )
    require(isinstance(telemetry.get("summary"), dict), f"{report_dir} telemetry correlation summary must be present")
    require(isinstance(agent_capabilities.get("records"), list), f"{report_dir} AI-agent capability records must be a list")
    require(
        agent_capabilities.get("record_count") == len(agent_capabilities["records"]),
        f"{report_dir} AI-agent capability count mismatch",
    )
    require(
        isinstance(agent_capabilities.get("capability_level_counts"), dict),
        f"{report_dir} AI-agent capability counts must be present",
    )
    require(
        isinstance(agent_capabilities.get("safety_status_counts"), dict),
        f"{report_dir} AI-agent safety counts must be present",
    )
    require(isinstance(agent_drift.get("records"), list), f"{report_dir} agent drift records must be a list")
    require(agent_drift.get("record_count") == len(agent_drift["records"]), f"{report_dir} agent drift count mismatch")
    require(
        isinstance(agent_drift.get("drift_status_counts"), dict),
        f"{report_dir} agent drift status counts must be present",
    )
    for name, payload in {
        "agent semantic": agent_semantic,
        "review state": review_state,
        "review workflows": review_workflows,
        "PR events": pr_events,
        "Actions runs": action_runs,
        "deployment evidence": deployment_evidence,
    }.items():
        require(isinstance(payload.get("records"), list), f"{report_dir} {name} records must be a list")
        require(payload.get("record_count") == len(payload["records"]), f"{report_dir} {name} count mismatch")
    require(isinstance(baseline_trend.get("new_blocked_paths"), list), f"{report_dir} baseline trend new blocked paths must be a list")
    require(isinstance(baseline_trend.get("resolved_blocked_paths"), list), f"{report_dir} baseline trend resolved blocked paths must be a list")
    require(v1_5_acceptance.get("acceptance_state") == "pass", f"{report_dir} v1.5 acceptance pack must pass")
    require(policy_pack.get("pack_id"), f"{report_dir} policy pack must have pack_id")
    require(isinstance(policy_pack.get("sections"), dict), f"{report_dir} policy pack sections must be present")
    require(isinstance(policy_pack.get("counts"), dict), f"{report_dir} policy pack counts must be present")
    for section in (
        "canonical_commands",
        "canonical_artifacts",
        "owner_rules",
        "owner_suggestion_rules",
        "accepted_exceptions",
        "readonly_patterns",
    ):
        require(section in policy_pack["sections"], f"{report_dir} policy pack missing section {section}")
        require(
            policy_pack["counts"].get(section) == len(policy_pack["sections"][section]),
            f"{report_dir} policy pack count mismatch for {section}",
        )
    require(onboarding.get("custom_code_required") is False, f"{report_dir} onboarding must not require custom code")
    require(isinstance(onboarding.get("scan_command"), list), f"{report_dir} onboarding scan command must be a list")
    require("--repo" in onboarding["scan_command"], f"{report_dir} onboarding scan command must include --repo")
    require("--out" in onboarding["scan_command"], f"{report_dir} onboarding scan command must include --out")
    require(
        isinstance(onboarding.get("generated_report_paths"), list) and onboarding["generated_report_paths"],
        f"{report_dir} onboarding generated report paths must be present",
    )
    require(
        isinstance(onboarding.get("validation_commands"), list) and "python3 -m edi validate" in onboarding["validation_commands"],
        f"{report_dir} onboarding validation commands must include edi validate",
    )
    require("counts" in executive and "top_decisions" in executive, f"{report_dir} executive export missing required keys")
    require(isinstance(executive["top_decisions"], list), f"{report_dir} top decisions must be a list")
    require(isinstance(clusters.get("clusters"), list), f"{report_dir} decision clusters must be a list")
    require(clusters.get("counts", {}).get("cluster_count") == len(clusters["clusters"]), f"{report_dir} cluster count mismatch")
    require(
        isinstance(clusters.get("scanner_tuning_candidates"), list),
        f"{report_dir} scanner tuning candidates must be a list",
    )
    require(
        isinstance(clusters.get("operational_blockers"), list),
        f"{report_dir} operational blockers must be a list",
    )
    require(isinstance(scanner_tuning.get("records"), list), f"{report_dir} scanner tuning records must be a list")
    require(
        scanner_tuning.get("record_count") == len(scanner_tuning["records"]),
        f"{report_dir} scanner tuning count mismatch",
    )
    require(
        isinstance(scanner_tuning.get("action_counts"), dict),
        f"{report_dir} scanner tuning action counts must be present",
    )
    require(
        isinstance(scanner_tuning.get("review_status_counts"), dict),
        f"{report_dir} scanner tuning review status counts must be present",
    )
    require(isinstance(remediation.get("packs"), list), f"{report_dir} remediation packs must be a list")
    require(remediation.get("pack_count") == len(remediation["packs"]), f"{report_dir} remediation pack count mismatch")
    scores = [pack.get("risk_reduction_score", 0) for pack in remediation["packs"]]
    require(scores == sorted(scores, reverse=True), f"{report_dir} remediation packs must be risk-reduction ranked")
    if owner_backlog["records"]:
        required_fields = {"priority", "action_lane", "owner", "risk_level", "path", "next_action"}
        missing = required_fields - set(owner_backlog["records"][0])
        require(not missing, f"{report_dir} owner backlog record missing fields: {sorted(missing)}")
    if owner_workflows["records"]:
        required_owner_fields = {
            "path",
            "owner",
            "owner_boundary",
            "assignment_type",
            "assignment_confidence",
            "review_class",
            "review_action",
        }
        missing = required_owner_fields - set(owner_workflows["records"][0])
        require(not missing, f"{report_dir} owner workflow record missing fields: {sorted(missing)}")
        confidence_values = [float(record["assignment_confidence"]) for record in owner_workflows["records"]]
        require(
            confidence_values == sorted(confidence_values),
            f"{report_dir} owner workflow records must be sorted by assignment confidence",
        )
    if cicd_events["records"]:
        required_cicd_fields = {
            "path",
            "surface_class",
            "risk_level",
            "autonomy_mode",
            "triggers",
            "detected_environments",
            "mutation_types",
        }
        missing = required_cicd_fields - set(cicd_events["records"][0])
        require(not missing, f"{report_dir} CI/CD event record missing fields: {sorted(missing)}")
    if runtime_signals["records"]:
        required_runtime_fields = {
            "path",
            "signal_source",
            "runtime_observed",
            "environments",
            "mutation_types",
            "evidence_status",
            "risk_level",
        }
        missing = required_runtime_fields - set(runtime_signals["records"][0])
        require(not missing, f"{report_dir} runtime signal record missing fields: {sorted(missing)}")
    if telemetry["records"]:
        required_telemetry_fields = {
            "path",
            "telemetry_state",
            "observed_telemetry_present",
            "telemetry_gap",
            "cicd_surface_class",
            "owner_assignment_type",
            "evidence_status",
        }
        missing = required_telemetry_fields - set(telemetry["records"][0])
        require(not missing, f"{report_dir} telemetry correlation record missing fields: {sorted(missing)}")
    if agent_capabilities["records"]:
        required_agent_fields = {
            "path",
            "artifact_type",
            "capability_level",
            "safety_status",
            "risk_level",
            "autonomy_mode",
            "eval_coverage",
            "drift_status",
        }
        missing = required_agent_fields - set(agent_capabilities["records"][0])
        require(not missing, f"{report_dir} AI-agent capability record missing fields: {sorted(missing)}")
    if agent_drift["records"]:
        required_drift_fields = {
            "path",
            "capability_level",
            "drift_status",
            "eval_coverage",
            "risk_level",
            "safety_status",
        }
        missing = required_drift_fields - set(agent_drift["records"][0])
        require(not missing, f"{report_dir} agent drift record missing fields: {sorted(missing)}")
    if agent_semantic["records"]:
        required_semantic_fields = {"path", "semantic_class", "capability_assertion", "capability_level", "risk_level"}
        missing = required_semantic_fields - set(agent_semantic["records"][0])
        require(not missing, f"{report_dir} agent semantic record missing fields: {sorted(missing)}")
    if review_state["records"]:
        required_review_fields = {"path", "review_state", "review_action", "priority", "risk_level", "owner"}
        missing = required_review_fields - set(review_state["records"][0])
        require(not missing, f"{report_dir} review state record missing fields: {sorted(missing)}")
    if review_workflows["records"]:
        required_workflow_fields = {"path", "review_state", "workflow_lane", "status_transition", "review_action"}
        missing = required_workflow_fields - set(review_workflows["records"][0])
        require(not missing, f"{report_dir} review workflow record missing fields: {sorted(missing)}")
    if scanner_tuning["records"]:
        required_tuning_fields = {
            "path",
            "artifact_type",
            "risk_level",
            "autonomy_mode",
            "reason",
            "review_status",
            "suggested_policy_action",
        }
        missing = required_tuning_fields - set(scanner_tuning["records"][0])
        require(not missing, f"{report_dir} scanner tuning record missing fields: {sorted(missing)}")
    if report_dir == "reports/ml-pilot":
        review_counts = owner_workflows.get("review_class_counts", {})
        require("inferred-owner-review" in review_counts, "ML pilot owner workflows must include inferred owner review")
        require("missing-owner-assignment" in review_counts, "ML pilot owner workflows must include missing owner assignment")
        surface_counts = cicd_events.get("surface_class_counts", {})
        require("deployment_capable" in surface_counts, "ML pilot CI/CD events must include deployment-capable workflows")
        require("validation_only" in surface_counts, "ML pilot CI/CD events must include validation-only workflows")
        require(
            "prod" in runtime_signals.get("environment_counts", {}),
            "ML pilot runtime signals must include production environment inference",
        )
        require(
            "database" in runtime_signals.get("mutation_counts", {}),
            "ML pilot runtime signals must include database mutation inference",
        )
        require(
            telemetry.get("summary", {}).get("telemetry_state", {}).get("inferred_only", 0) > 0,
            "ML pilot telemetry correlations must include inferred-only telemetry state",
        )
        require(
            telemetry.get("summary", {}).get("cicd_surface_class", {}).get("deployment_capable", 0) > 0,
            "ML pilot telemetry correlations must include deployment-capable CI/CD correlation",
        )
        require(agent_capabilities.get("record_count", 0) > 0, "ML pilot must include AI-agent capability records")
        require(
            "financial_or_order_capable" in agent_capabilities.get("capability_level_counts", {}),
            "ML pilot AI-agent capabilities must include financial/order-capable surfaces",
        )
        require(
            agent_drift.get("record_count", 0) > 0,
            "ML pilot agent drift/eval export must include review records",
        )
        require(agent_semantic.get("record_count", 0) > 0, "ML pilot agent semantic export must include records")
        require(review_state.get("record_count", 0) > 0, "ML pilot review-state export must include records")
        require(review_workflows.get("record_count", 0) > 0, "ML pilot review workflow export must include records")
        require(deployment_evidence.get("record_count", 0) > 0, "ML pilot deployment evidence export must include records")
        require(
            policy_pack["counts"].get("canonical_commands", 0) >= 2,
            "ML pilot policy pack must include canonical commands",
        )
        require(policy_pack["counts"].get("owner_rules", 0) > 0, "ML pilot policy pack must include owner rules")
        require(
            policy_pack["counts"].get("accepted_exceptions", 0) > 0,
            "ML pilot policy pack must include accepted exceptions",
        )
        require(
            policy_pack["counts"].get("readonly_patterns", 0) > 0,
            "ML pilot policy pack must include read-only patterns",
        )
        require(scanner_tuning.get("record_count", 0) > 0, "ML pilot scanner tuning pack must include records")
        require(
            scanner_tuning.get("action_counts", {}).get("add or confirm readonly pattern", 0) > 0,
            "ML pilot scanner tuning pack must include read-only policy actions",
        )
    if clusters["clusters"]:
        required_cluster_fields = {
            "cluster_id",
            "finding_count",
            "risk_reduction_score",
            "scanner_tuning_candidates",
            "operational_blockers",
        }
        missing = required_cluster_fields - set(clusters["clusters"][0])
        require(not missing, f"{report_dir} decision cluster missing fields: {sorted(missing)}")
    if report_dir == "reports/ml-pilot":
        manifest = load_json(ROOT / report_dir / "manifest.json")
        require(
            clusters.get("counts", {}).get("artifacts") == manifest.get("counts", {}).get("artifacts"),
            "ML pilot clusters must cover all manifest findings",
        )


def check_export_contracts() -> None:
    check_export_contract("reports/ml-pilot")
    check_export_contract("reports/self")


def check_progress_freshness() -> None:
    result = run_command([sys.executable, "tools/autopilot_progress.py", "--check"])
    require(result.returncode == 0, f"product progress check failed: {result.stderr or result.stdout}")


def check_packaging_contract() -> None:
    path = ROOT / "pyproject.toml"
    require(path.exists(), "missing pyproject.toml")
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    project = data.get("project") or {}
    scripts = project.get("scripts") or {}
    require(project.get("name") == "engineering-decision-intelligence", "project name mismatch")
    require(scripts.get("edi") == "edi.__main__:main", "edi console script must point to edi.__main__:main")
    require(project.get("requires-python", "").startswith(">="), "requires-python must be declared")
    require(project.get("dependencies") == [], "packaging must remain dependency-free for v1")


def check_product_api_contract() -> None:
    snapshot = load_json(ROOT / "reports" / "product" / "api-snapshot.json")
    v5_acceptance = load_json(ROOT / "reports" / "product" / "v5" / "exports" / "v5-acceptance-pack.json")
    require(snapshot.get("api_version") == "v1", "product API snapshot must declare api_version v1")
    require(
        "product" in snapshot
        and "executive" in snapshot
        and "risk" in snapshot
        and "ai_agents" in snapshot
        and "scanner_tuning" in snapshot,
        "product API snapshot missing sections",
    )
    require("v2" in snapshot, "product API snapshot missing v2 section")
    require("v3" in snapshot, "product API snapshot missing v3 section")
    require("v4" in snapshot, "product API snapshot missing v4 section")
    require("v5" in snapshot, "product API snapshot missing v5 section")
    require(snapshot["product"].get("completion_percent") > 0, "product API completion percent must be positive")
    require(isinstance(snapshot["executive"].get("top_decisions"), list), "product API top decisions must be a list")
    require(snapshot["risk"].get("runtime_signal_count", 0) > 0, "product API runtime signal count must be positive")
    require(
        snapshot["risk"].get("telemetry_correlation_count", 0) > 0,
        "product API telemetry correlation count must be positive",
    )
    require(snapshot["ai_agents"].get("capability_count", 0) > 0, "product API AI-agent capability count must be positive")
    require(
        snapshot["scanner_tuning"].get("candidate_count", 0) > 0,
        "product API scanner tuning candidate count must be positive",
    )
    require(snapshot["v2"].get("completion_percent") == 100.0, "product API v2 completion percent must be 100")
    require(snapshot["v2"].get("acceptance_state") == "pass", "product API v2 acceptance must pass")
    require(snapshot["v2"].get("portfolio_repo_count", 0) >= 2, "product API v2 portfolio must include at least two repos")
    require(snapshot["v3"].get("completion_percent") == 100.0, "product API v3 completion percent must be 100")
    require(snapshot["v3"].get("acceptance_state") == "pass", "product API v3 acceptance must pass")
    require(snapshot["v3"].get("connector_count", 0) >= 6, "product API v3 must include connector inputs")
    require(snapshot["v4"].get("completion_percent") == 100.0, "product API v4 completion percent must be 100")
    require(snapshot["v4"].get("acceptance_state") == "pass", "product API v4 acceptance must pass")
    require(snapshot["v4"].get("connector_count", 0) >= 6, "product API v4 must include live connector configs")
    require(snapshot["v5"].get("tooling_completion_percent") == 100.0, "product API v5 tooling must be complete")
    v5_live_percent = snapshot["v5"].get("live_claim_completion_percent", 0.0)
    require(0.0 <= v5_live_percent < 100.0, "product API v5 live claims must remain incomplete until all live evidence passes")
    require(
        v5_live_percent == v5_acceptance.get("live_claim_completion_percent"),
        "product API v5 live percent must match v5 acceptance pack",
    )
    require(
        "autonomous production enforcement is active" in snapshot["v5"].get("blocked_claims", []),
        "product API v5 must keep autonomous production enforcement blocked",
    )
    require(
        "complete live runtime truth exists" in snapshot["v5"].get("blocked_claims", []),
        "product API v5 must keep complete runtime truth blocked",
    )


def check_product_ui_contract() -> None:
    html = (ROOT / "reports" / "product" / "operator-view.html").read_text(encoding="utf-8")
    require("<!doctype html>" in html.lower(), "operator view must be HTML")
    require("Engineering Decision Intelligence" in html, "operator view must identify the product")
    require("Product completion" in html, "operator view must show product completion")
    require("Next mission" in html, "operator view must show next mission")
    require("Top Decisions" in html, "operator view must show top decisions")
    require("Telemetry correlations" in html, "operator view must show telemetry correlations")
    require("Scanner tuning candidates" in html, "operator view must show scanner tuning candidates")
    require("V2 Operational Intelligence" in html, "operator view must show v2 operational intelligence")
    require("V3 Operationalization" in html, "operator view must show v3 operationalization")
    require("V4 Live Enforcement Readiness" in html, "operator view must show v4 readiness")
    require("V5 Target Installation" in html, "operator view must show v5 target installation")


def check_v2_report_contract() -> None:
    base = ROOT / "reports" / "product" / "v2" / "exports"
    portfolio = load_json(base / "portfolio-summary.json")
    runtime = load_json(base / "runtime-connector-contract.json")
    incidents = load_json(base / "incident-correlations.json")
    remediation = load_json(base / "closed-loop-remediation.json")
    preflight = load_json(base / "policy-preflight.json")
    confidence = load_json(base / "trust-confidence.json")
    lineage = load_json(base / "evidence-lineage.json")
    sdk = load_json(base / "connector-sdk.json")
    acceptance = load_json(base / "v2-acceptance-pack.json")

    require(portfolio.get("repo_count", 0) >= 2, "v2 portfolio must include at least two repositories")
    require(runtime.get("contract_state") == "pass", "v2 runtime connector contract must pass")
    require(runtime.get("source_boundary") == "static_fixture_contract_not_live_runtime_truth", "v2 runtime boundary mismatch")
    require(incidents.get("record_count", 0) > 0, "v2 incident correlations must include records")
    require(remediation.get("record_count", 0) > 0, "v2 remediation state must include records")
    require(preflight.get("record_count", 0) > 0, "v2 policy preflight must include records")
    require(isinstance(preflight.get("decision_counts"), dict), "v2 preflight must include decision counts")
    require(confidence.get("record_count", 0) > 0, "v2 confidence scoring must include records")
    require(lineage.get("record_count", 0) > 0, "v2 evidence lineage must include records")
    require(sdk.get("sdk_version") == "connector-sdk-v1", "v2 connector SDK version mismatch")
    require(acceptance.get("acceptance_state") == "pass", "v2 acceptance pack must pass")
    require(acceptance.get("completed_slices") == acceptance.get("total_slices") == 10, "v2 acceptance slice count mismatch")


def check_v3_report_contract() -> None:
    base = ROOT / "reports" / "product" / "v3" / "exports"
    connectors = load_json(base / "connector-ingestion.json")
    reconciliation = load_json(base / "reconciliation-loops.json")
    onboarding = load_json(base / "portfolio-onboarding.json")
    lineage = load_json(base / "evidence-lineage-v3.json")
    remediation = load_json(base / "remediation-workflow.json")
    preflight = load_json(base / "policy-preflight-ci.json")
    ux = load_json(base / "product-ux.json")
    packaging = load_json(base / "reusable-packaging.json")
    pilot = load_json(base / "external-pilot-readiness.json")
    acceptance = load_json(base / "v3-acceptance-pack.json")

    require(connectors.get("connector_count", 0) >= 6, "v3 connector ingestion must include six connector inputs")
    require(connectors.get("source_boundary") == "imported_connector_payloads_not_live_polling", "v3 connector boundary mismatch")
    require(reconciliation.get("loop_count", 0) >= 4, "v3 reconciliation loops must include at least four loops")
    require(onboarding.get("ready_count", 0) >= 2, "v3 onboarding must mark at least two repos ready")
    require(lineage.get("record_count", 0) > 0, "v3 lineage must include records")
    require(remediation.get("record_count", 0) > 0, "v3 remediation workflow must include records")
    require(preflight.get("record_count", 0) > 0, "v3 policy preflight CI must include records")
    require(ux.get("surface_count", 0) >= 5, "v3 product UX must include role-based surfaces")
    require(packaging.get("dependency_free") is True, "v3 packaging must remain dependency-free")
    require(pilot.get("pilot_state") == "ready_for_controlled_external_pilot", "v3 pilot readiness mismatch")
    require(acceptance.get("acceptance_state") == "pass", "v3 acceptance pack must pass")
    require(acceptance.get("completed_slices") == acceptance.get("total_slices") == 10, "v3 acceptance slice count mismatch")
    require("complete live runtime truth" in acceptance.get("blocked_claims", []), "v3 acceptance must block live truth overclaim")


def check_v4_report_contract() -> None:
    base = ROOT / "reports" / "product" / "v4" / "exports"
    connectors = load_json(base / "live-connector-readiness.json")
    reconciliation = load_json(base / "continuous-reconciliation.json")
    ci = load_json(base / "ci-pr-enforcement.json")
    remediation = load_json(base / "remediation-operations.json")
    security = load_json(base / "security-access.json")
    persistence = load_json(base / "persistence-history.json")
    packaging = load_json(base / "deployment-packaging.json")
    slos = load_json(base / "operational-slos.json")
    pilot = load_json(base / "external-pilot-operations.json")
    acceptance = load_json(base / "v4-acceptance-pack.json")

    require(connectors.get("connector_count", 0) >= 6, "v4 connector readiness must include six connectors")
    require(connectors.get("claim_boundary") == "configured_for_install_not_authenticated_live_polling", "v4 connector boundary mismatch")
    require(reconciliation.get("loop_count", 0) >= 5, "v4 reconciliation must include five loops")
    require(ci.get("target_state") == "ready_for_pr_check_install", "v4 CI target state mismatch")
    require(remediation.get("transition_count", 0) >= 5, "v4 remediation model must include transitions")
    require(security.get("plaintext_secrets_allowed") is False, "v4 security must block plaintext secrets")
    require(persistence.get("production_backend_required") is True, "v4 persistence must require production backend")
    require(packaging.get("production_installation_status") == "not_installed_in_target_environment", "v4 packaging boundary mismatch")
    require(slos.get("slo_count", 0) >= 5, "v4 SLOs must include at least five SLOs")
    require(pilot.get("status") == "ready_to_schedule", "v4 pilot operation status mismatch")
    require(acceptance.get("acceptance_state") == "pass", "v4 acceptance pack must pass")
    require(acceptance.get("completed_slices") == acceptance.get("total_slices") == 10, "v4 acceptance slice count mismatch")
    require(
        "target repositories enforcing PR checks" in acceptance.get("blocked_claims", []),
        "v4 acceptance must block target PR enforcement overclaim",
    )


def check_v5_report_contract() -> None:
    base = ROOT / "reports" / "product" / "v5" / "exports"
    install = load_json(base / "onepassword-installation.json")
    secret_flow = load_json(base / "onepassword-secret-flow.json")
    live_evidence = load_json(base / "v5-live-evidence.json")
    runtime_truth = load_json(base / "runtime-truth-completeness.json")
    autonomous = load_json(base / "autonomous-enforcement.json")
    live = load_json(base / "live-evidence-claims.json")
    acceptance = load_json(base / "v5-acceptance-pack.json")

    require(install.get("op_installed") is True, "v5 requires 1Password CLI installed")
    require(install.get("op_version_detail_committed") is False, "v5 must not commit runner-specific op version details")
    require(install.get("secrets_read") is False, "v5 install check must not read secrets")
    require(install.get("vaults_listed") is False, "v5 install check must not list vaults")
    require(install.get("items_listed") is False, "v5 install check must not list items")
    require(secret_flow.get("secret_reference_count", 0) >= 5, "v5 must include secret references")
    require(not secret_flow.get("invalid_secret_references"), "v5 secret references must be valid op:// refs")
    require(secret_flow.get("plaintext_secret_values_committed") is False, "v5 must not commit plaintext secrets")
    records = live.get("records", [])
    completed = [record for record in records if record.get("state") == "completed_live_evidence"]
    blocked = [record for record in records if record.get("state") == "blocked_pending_target_evidence"]
    expected_percent = round(len(completed) / len(records) * 100, 1) if records else 0.0
    require(live.get("completed_claim_count") == len(completed), "v5 completed live claim count mismatch")
    require(live.get("live_claim_completion_percent") == expected_percent, "v5 live claim percent must match backed records")
    require(len(blocked) > 0, "v5 must keep unsupported live claims blocked")
    for record in completed:
        require(record.get("evidence_status") == "captured", "v5 completed live claims must have captured evidence")
        require(record.get("evidence"), "v5 completed live claims must cite evidence")
    require(
        acceptance.get("acceptance_state") == "tooling_pass_live_evidence_incomplete",
        "v5 acceptance must show tooling pass and live evidence incomplete",
    )
    require(acceptance.get("tooling_completion_percent") == 100.0, "v5 tooling must be complete")
    require(acceptance.get("live_claim_completion_percent") == live.get("live_claim_completion_percent"), "v5 acceptance live percent mismatch")
    require(
        autonomous.get("required_evidence_count", 0) >= 7,
        "v5 autonomous enforcement must track required evidence",
    )
    require(
        autonomous.get("enforcement_percent", 0.0) <= autonomous.get("minimum_enforcement_percent", 100.0),
        "v5 autonomous enforcement score must not exceed its threshold",
    )
    autonomous_claim = next((record for record in records if record.get("claim") == "autonomous production enforcement is active"), {})
    if autonomous_claim.get("state") == "completed_live_evidence":
        require(
            autonomous.get("autonomous_production_enforcement_active") is True,
            "v5 autonomous claim requires complete enforcement evidence",
        )
    else:
        require(
            "autonomous production enforcement is active" in acceptance.get("blocked_claims", []),
            "v5 must keep autonomous production enforcement blocked until evidence passes",
        )
        require(
            autonomous.get("autonomous_production_enforcement_active") is False,
            "v5 autonomous enforcement must fail closed while claim is blocked",
        )
    require(
        "complete live runtime truth exists" in acceptance.get("blocked_claims", []),
        "v5 must keep complete runtime truth blocked",
    )
    require(
        runtime_truth.get("complete_live_runtime_truth") is False,
        "v5 runtime truth must fail closed until all required evidence classes pass",
    )
    require(
        runtime_truth.get("completeness_percent", 0.0) < runtime_truth.get("minimum_completeness_percent", 100.0),
        "v5 runtime truth score must remain below threshold while claim is blocked",
    )
    require(
        runtime_truth.get("required_evidence_class_count", 0) >= 6,
        "v5 runtime truth must track required evidence classes",
    )
    credential_claim = next((record for record in records if record.get("claim") == "target credentials installed"), {})
    if credential_claim.get("state") == "completed_live_evidence":
        credential_resolution = live_evidence.get("credential_resolution", {})
        github_api = live_evidence.get("github_api", {})
        require(credential_resolution.get("all_required_resolved") is True, "v5 credential claim requires all references resolved")
        require(credential_resolution.get("secrets_logged") is False, "v5 credential claim must not log secrets")
        require(github_api.get("authenticated") is True, "v5 credential claim requires GitHub auth smoke test")
    scheduled_claim = next((record for record in records if record.get("claim") == "scheduled connectors have run"), {})
    if scheduled_claim.get("state") == "completed_live_evidence":
        github_api = live_evidence.get("github_api", {})
        scheduled_run = github_api.get("scheduled_connector_run", {})
        require(github_api.get("scheduled_connector_observed") is True, "v5 scheduled connector claim requires observed workflow run")
        require(scheduled_run.get("workflow_file") == ".github/workflows/edi-v5-scheduled-connectors.yml", "v5 scheduled connector workflow path mismatch")
        require(scheduled_run.get("event") in {"schedule", "workflow_dispatch"}, "v5 scheduled connector event mismatch")
        require(scheduled_run.get("status") == "completed", "v5 scheduled connector status mismatch")
        require(scheduled_run.get("conclusion") == "success", "v5 scheduled connector conclusion mismatch")
        require(bool(scheduled_run.get("observed_at")), "v5 scheduled connector observed_at missing")
        require(bool(scheduled_run.get("run_id")), "v5 scheduled connector run_id missing")


def check_v1_5_backlog_contract() -> None:
    backlog = load_json(ROOT / "roadmap" / "v1.5-operationalization-backlog.json")
    slices = backlog.get("slices", [])
    require(backlog.get("milestone") == "v1.5 operationalization", "v1.5 backlog milestone mismatch")
    require(len(slices) == 10, "v1.5 backlog must track ten operationalization slices")
    completed = [item for item in slices if item.get("status") == "completed"]
    require(len(completed) == 10, "v1.5 backlog must have all operationalization slices completed")
    require(completed[0].get("id") == "scanner-tuning-pack-v1", "first v1.5 completed slice must be scanner tuning")


def check_v2_backlog_contract() -> None:
    backlog = load_json(ROOT / "roadmap" / "v2-operational-intelligence-backlog.json")
    slices = backlog.get("slices", [])
    require(backlog.get("milestone") == "v2 operational intelligence", "v2 backlog milestone mismatch")
    require(len(slices) == 10, "v2 backlog must track ten operational intelligence slices")
    require(slices[0].get("id") == "multi-repo-portfolio-model-v1", "first v2 slice must be multi-repo portfolio model")
    require(slices[-1].get("id") == "v2-acceptance-pack", "last v2 slice must be v2 acceptance pack")
    require(all(item.get("status") == "completed" for item in slices), "v2 backlog must have all slices completed")
    for item in slices:
        require(item.get("purpose"), f"v2 slice {item.get('id')} must declare purpose")
        require(isinstance(item.get("expected_outputs"), list), f"v2 slice {item.get('id')} must declare expected outputs")
        require(isinstance(item.get("acceptance"), list), f"v2 slice {item.get('id')} must declare acceptance checks")


def check_v3_backlog_contract() -> None:
    backlog = load_json(ROOT / "roadmap" / "v3-operationalization-backlog.json")
    slices = backlog.get("slices", [])
    require(backlog.get("milestone") == "v3 operationalization", "v3 backlog milestone mismatch")
    require(len(slices) == 10, "v3 backlog must track ten operationalization slices")
    require(slices[0].get("id") == "connector-inputs-v1", "first v3 slice must be connector inputs")
    require(slices[-1].get("id") == "v3-acceptance-pack", "last v3 slice must be v3 acceptance pack")
    require(all(item.get("status") == "completed" for item in slices), "v3 backlog must have all slices completed")
    for item in slices:
        require(item.get("purpose"), f"v3 slice {item.get('id')} must declare purpose")
        require(isinstance(item.get("evidence"), list) and item["evidence"], f"v3 slice {item.get('id')} must declare evidence")


def check_v4_backlog_contract() -> None:
    backlog = load_json(ROOT / "roadmap" / "v4-live-enforcement-readiness-backlog.json")
    slices = backlog.get("slices", [])
    require(backlog.get("milestone") == "v4 live enforcement readiness", "v4 backlog milestone mismatch")
    require(len(slices) == 10, "v4 backlog must track ten readiness slices")
    require(slices[0].get("id") == "live-connector-config-v1", "first v4 slice must be live connector config")
    require(slices[-1].get("id") == "v4-acceptance-pack", "last v4 slice must be v4 acceptance pack")
    require(all(item.get("status") == "completed" for item in slices), "v4 backlog must have all slices completed")
    for item in slices:
        require(isinstance(item.get("evidence"), list) and item["evidence"], f"v4 slice {item.get('id')} must declare evidence")


def check_v5_backlog_contract() -> None:
    backlog = load_json(ROOT / "roadmap" / "v5-target-installation-live-evidence-backlog.json")
    slices = backlog.get("slices", [])
    require(backlog.get("milestone") == "v5 target installation and live evidence", "v5 backlog milestone mismatch")
    require(len(slices) == 10, "v5 backlog must track ten slices")
    completed = [item for item in slices if item.get("status") == "completed"]
    blocked = [item for item in slices if item.get("status") == "blocked"]
    require(len(completed) == 4, "v5 must have four safe tooling slices completed")
    require(len(blocked) == 6, "v5 must keep six live-evidence slices blocked")


def main() -> int:
    check_cli_contracts()
    check_report_contracts()
    check_graph_contracts()
    check_export_contracts()
    check_progress_freshness()
    check_packaging_contract()
    check_product_api_contract()
    check_product_ui_contract()
    check_v1_5_backlog_contract()
    check_v2_backlog_contract()
    check_v2_report_contract()
    check_v3_backlog_contract()
    check_v3_report_contract()
    check_v4_backlog_contract()
    check_v4_report_contract()
    check_v5_backlog_contract()
    check_v5_report_contract()
    print("Acceptance gates passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
