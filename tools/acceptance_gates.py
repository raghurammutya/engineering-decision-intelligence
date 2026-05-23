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
        "owner-confidence-map.md",
        "cicd-event-summary.md",
        "runtime-signal-summary.md",
        "telemetry-correlation-summary.md",
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
        "exports/policy-pack.json",
        "exports/onboarding.json",
        "exports/executive-decisions.json",
        "exports/decision-clusters.json",
        "exports/remediation-packs.json",
    ],
    "reports/self": [
        "manifest.json",
        "decision-backlog.md",
        "decision-insight-clusters.md",
        "owner-confidence-map.md",
        "cicd-event-summary.md",
        "runtime-signal-summary.md",
        "telemetry-correlation-summary.md",
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
        "exports/policy-pack.json",
        "exports/onboarding.json",
        "exports/executive-decisions.json",
        "exports/decision-clusters.json",
        "exports/remediation-packs.json",
    ],
    "reports/product": [
        "progress.md",
        "progress.json",
        "next-mission-checklist.md",
        "next-mission.json",
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
    ]
    for command, expected in commands:
        result = run_command(command)
        require(result.returncode == 0, f"CLI dry-run command failed: {' '.join(command)}\n{result.stderr}")
        require(expected in result.stdout, f"CLI dry-run output missing {expected!r}: {' '.join(command)}")

    result = run_command([sys.executable, "-m", "edi", "autopilot", "next", "--json"])
    require(result.returncode == 0, f"autopilot next --json failed: {result.stderr}")
    payload = json.loads(result.stdout)
    require(payload.get("safe_mode") == "plan_only", "autopilot next --json must remain plan_only")
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
    policy_pack = load_json(base / "policy-pack.json")
    onboarding = load_json(base / "onboarding.json")
    executive = load_json(base / "executive-decisions.json")
    clusters = load_json(base / "decision-clusters.json")
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
        require(clusters.get("counts", {}).get("artifacts") == 487, "ML pilot clusters must cover 487 findings")


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


def main() -> int:
    check_cli_contracts()
    check_report_contracts()
    check_graph_contracts()
    check_export_contracts()
    check_progress_freshness()
    check_packaging_contract()
    print("Acceptance gates passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
