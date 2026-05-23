#!/usr/bin/env python3
"""Run deterministic acceptance gates for generated product outputs."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_REPORTS = {
    "reports/ml-pilot": [
        "manifest.json",
        "decision-backlog.md",
        "decision-insight-clusters.md",
        "risk-explanation-map.md",
        "graph/entities.json",
        "graph/relationships.json",
        "exports/owner-backlog.json",
        "exports/owner-backlog.csv",
        "exports/executive-decisions.json",
        "exports/decision-clusters.json",
        "exports/remediation-packs.json",
    ],
    "reports/self": [
        "manifest.json",
        "decision-backlog.md",
        "decision-insight-clusters.md",
        "risk-explanation-map.md",
        "graph/entities.json",
        "graph/relationships.json",
        "exports/owner-backlog.json",
        "exports/owner-backlog.csv",
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
    entity_types = {entity.get("type") for entity in entities}
    relationship_types = {relationship.get("relation") for relationship in relationships}
    missing_entity_types = REQUIRED_GRAPH_ENTITY_TYPES - entity_types
    require(not missing_entity_types, f"{report_dir} graph missing entity types: {sorted(missing_entity_types)}")
    if require_full_relationships:
        missing_relationships = REQUIRED_GRAPH_RELATIONSHIPS - relationship_types
        require(not missing_relationships, f"{report_dir} graph missing relationships: {sorted(missing_relationships)}")


def check_graph_contracts() -> None:
    check_graph_contract("reports/ml-pilot", require_full_relationships=True)
    check_graph_contract("reports/self", require_full_relationships=False)


def check_export_contract(report_dir: str) -> None:
    base = ROOT / report_dir / "exports"
    owner_backlog = load_json(base / "owner-backlog.json")
    executive = load_json(base / "executive-decisions.json")
    clusters = load_json(base / "decision-clusters.json")
    remediation = load_json(base / "remediation-packs.json")

    require(isinstance(owner_backlog.get("records"), list), f"{report_dir} owner backlog records must be a list")
    require(owner_backlog.get("record_count") == len(owner_backlog["records"]), f"{report_dir} owner backlog count mismatch")
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


def main() -> int:
    check_cli_contracts()
    check_report_contracts()
    check_graph_contracts()
    check_export_contracts()
    check_progress_freshness()
    print("Acceptance gates passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
