"""Materialize a stable product API snapshot from generated reports."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build_snapshot(root: Path, generated_at: str | None = None) -> dict[str, Any]:
    generated = generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    product_dir = root / "reports" / "product"
    ml_exports = root / "reports" / "ml-pilot" / "exports"
    progress = load_json(product_dir / "progress.json")
    next_mission = load_json(product_dir / "next-mission.json")
    executive = load_json(ml_exports / "executive-decisions.json")
    telemetry = load_json(ml_exports / "telemetry-correlations.json")
    runtime = load_json(ml_exports / "runtime-signals.json")
    owner = load_json(ml_exports / "owner-workflows.json")

    return {
        "generated_at": generated,
        "api_version": "v1",
        "product": {
            "completion_percent": progress["completion"]["completion_percent"],
            "completed_weight": progress["completion"]["completed_weight"],
            "total_weight": progress["completion"]["total_weight"],
            "next_recommended_mission": progress.get("next_recommended_mission"),
        },
        "next_mission": next_mission,
        "executive": {
            "counts": executive.get("counts", {}),
            "top_decisions": executive.get("top_decisions", [])[:25],
            "action_lanes": executive.get("action_lanes", []),
        },
        "risk": {
            "runtime_signal_count": runtime.get("record_count", 0),
            "runtime_surface_group_count": runtime.get("surface_group_count", 0),
            "telemetry_correlation_count": telemetry.get("record_count", 0),
            "telemetry_summary": telemetry.get("summary", {}),
            "owner_review_counts": owner.get("review_class_counts", {}),
        },
    }


def write_snapshot(root: Path, out: Path, generated_at: str | None = None) -> dict[str, Any]:
    snapshot = build_snapshot(root, generated_at)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return snapshot
