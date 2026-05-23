#!/usr/bin/env python3
"""Generate and validate product autopilot progress reports."""

from __future__ import annotations

import argparse
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BACKLOG = ROOT / "roadmap" / "autopilot-backlog.json"
DEFAULT_OUT = ROOT / "reports" / "product"
VALID_STATUSES = {"completed", "in_progress", "planned", "blocked", "retired"}


def load_backlog(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    validate_backlog(data)
    return data


def validate_backlog(data: dict[str, Any]) -> None:
    if int(data.get("schema_version", 0)) != 1:
        raise ValueError("autopilot backlog schema_version must be 1")
    capabilities = data.get("capabilities")
    missions = data.get("mission_packs")
    if not isinstance(capabilities, list) or not capabilities:
        raise ValueError("autopilot backlog requires non-empty capabilities")
    if not isinstance(missions, list) or not missions:
        raise ValueError("autopilot backlog requires non-empty mission_packs")

    capability_ids: set[str] = set()
    total_weight = 0.0
    for item in capabilities:
        capability_id = str(item.get("id", ""))
        status = str(item.get("status", ""))
        weight = float(item.get("weight", 0))
        if not capability_id:
            raise ValueError("capability is missing id")
        if capability_id in capability_ids:
            raise ValueError(f"duplicate capability id: {capability_id}")
        if status not in VALID_STATUSES:
            raise ValueError(f"invalid capability status for {capability_id}: {status}")
        if weight <= 0:
            raise ValueError(f"capability weight must be positive for {capability_id}")
        capability_ids.add(capability_id)
        total_weight += weight

    if round(total_weight, 2) != 100.0:
        raise ValueError(f"capability weights must sum to 100.0, got {total_weight:.2f}")

    mission_ids: set[str] = set()
    for mission in missions:
        mission_id = str(mission.get("id", ""))
        status = str(mission.get("status", ""))
        if not mission_id:
            raise ValueError("mission is missing id")
        if mission_id in mission_ids:
            raise ValueError(f"duplicate mission id: {mission_id}")
        if status not in VALID_STATUSES:
            raise ValueError(f"invalid mission status for {mission_id}: {status}")
        for capability_id in mission.get("capability_ids") or []:
            if capability_id not in capability_ids:
                raise ValueError(f"mission {mission_id} references unknown capability {capability_id}")
        mission_ids.add(mission_id)

    for mission in missions:
        for dependency in mission.get("depends_on") or []:
            if dependency not in mission_ids:
                raise ValueError(f"mission {mission.get('id')} depends on unknown mission {dependency}")


def completion_summary(data: dict[str, Any]) -> dict[str, Any]:
    capabilities = data["capabilities"]
    total_weight = sum(float(item["weight"]) for item in capabilities)
    completed_weight = sum(float(item["weight"]) for item in capabilities if item["status"] == "completed")
    in_progress_weight = sum(float(item["weight"]) for item in capabilities if item["status"] == "in_progress")
    return {
        "total_weight": round(total_weight, 2),
        "completed_weight": round(completed_weight, 2),
        "in_progress_weight": round(in_progress_weight, 2),
        "completion_percent": round((completed_weight / total_weight) * 100, 1),
        "with_in_progress_percent": round(((completed_weight + in_progress_weight) / total_weight) * 100, 1),
    }


def mission_ready(mission: dict[str, Any], mission_by_id: dict[str, dict[str, Any]]) -> bool:
    if mission.get("status") != "planned":
        return False
    for dependency in mission.get("depends_on") or []:
        if mission_by_id[dependency].get("status") != "completed":
            return False
    return True


def next_mission(data: dict[str, Any]) -> dict[str, Any] | None:
    mission_by_id = {mission["id"]: mission for mission in data["mission_packs"]}
    candidates = [mission for mission in data["mission_packs"] if mission_ready(mission, mission_by_id)]
    if not candidates:
        return None
    return sorted(candidates, key=lambda mission: (int(mission.get("priority", 999)), mission["id"]))[0]


def capability_by_id(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {capability["id"]: capability for capability in data["capabilities"]}


def mission_completion_delta(data: dict[str, Any], mission: dict[str, Any]) -> float:
    capabilities = capability_by_id(data)
    delta = 0.0
    for capability_id in mission.get("capability_ids") or []:
        capability = capabilities[capability_id]
        if capability.get("status") != "completed":
            delta += float(capability["weight"])
    return round(delta, 1)


def mission_after_completion_percent(data: dict[str, Any], mission: dict[str, Any]) -> float:
    summary = completion_summary(data)
    return round(summary["completion_percent"] + mission_completion_delta(data, mission), 1)


def mission_payload(data: dict[str, Any], mission: dict[str, Any] | None, generated_at: str) -> dict[str, Any]:
    if mission is None:
        return {
            "generated_at": generated_at,
            "mission": None,
            "safe_mode": "plan_only",
            "reason": "No dependency-ready planned mission is available.",
        }
    return {
        "generated_at": generated_at,
        "mission": mission,
        "safe_mode": "plan_only",
        "blocked_paths": mission.get("blocked_paths") or [],
        "allowed_paths": mission.get("allowed_paths") or [],
        "validation_commands": mission.get("validation_commands") or [],
        "completion_delta": mission_completion_delta(data, mission),
        "completion_after_mission": mission_after_completion_percent(data, mission),
        "execution_boundary": "This command selects and explains work. It does not edit files, mutate external systems, or touch blocked paths.",
    }


def render_mission_summary(data: dict[str, Any], generated_at: str) -> str:
    mission = next_mission(data)
    payload = mission_payload(data, mission, generated_at)
    if mission is None:
        return "No dependency-ready planned mission is available.\n"
    lines = [
        f"Mission: {mission['id']}",
        f"Title: {mission['title']}",
        f"Risk: {mission.get('risk', 'unknown')}",
        f"Safe mode: {payload['safe_mode']}",
        f"Product completion delta if completed: +{payload['completion_delta']}%",
        f"Projected product completion: {payload['completion_after_mission']}%",
        "Blocked paths:",
    ]
    for item in payload["blocked_paths"]:
        lines.append(f"- {item}")
    lines.append("Validation commands:")
    for item in payload["validation_commands"]:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def render_mission_checklist(data: dict[str, Any], generated_at: str) -> str:
    mission = next_mission(data)
    payload = mission_payload(data, mission, generated_at)
    if mission is None:
        return "# Autopilot Mission Checklist\n\nNo dependency-ready planned mission is available.\n"
    lines = [
        "# Autopilot Mission Checklist",
        "",
        f"Generated: `{generated_at}`",
        "",
        f"Mission: `{mission['id']}`",
        f"Title: {mission['title']}",
        f"Risk: `{mission.get('risk', 'unknown')}`",
        f"Safe mode: `{payload['safe_mode']}`",
        f"Product completion delta if completed: `+{payload['completion_delta']}%`",
        f"Projected product completion: `{payload['completion_after_mission']}%`",
        "",
        "## Safety Boundary",
        "",
        payload["execution_boundary"],
        "",
        "## Allowed Paths",
        "",
    ]
    for item in payload["allowed_paths"]:
        lines.append(f"- `{item}`")
    lines.extend(["", "## Blocked Paths", ""])
    for item in payload["blocked_paths"]:
        lines.append(f"- `{item}`")
    lines.extend(["", "## Acceptance Criteria", ""])
    for item in mission.get("acceptance_criteria") or []:
        lines.append(f"- [ ] {item}")
    lines.extend(["", "## Validation Commands", ""])
    for item in payload["validation_commands"]:
        lines.append(f"- [ ] `{item}`")
    lines.extend(
        [
            "",
            "## Completion Rule",
            "",
            "- [ ] Implementation stayed within allowed paths.",
            "- [ ] No blocked path was modified.",
            "- [ ] All validation commands passed.",
            "- [ ] Product progress was regenerated and checked.",
            "- [ ] CI passed after push.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_markdown(data: dict[str, Any], generated_at: str) -> str:
    summary = completion_summary(data)
    mission = next_mission(data)
    completed = [item for item in data["capabilities"] if item["status"] == "completed"]
    planned = [item for item in data["capabilities"] if item["status"] == "planned"]

    lines = [
        "# Product Autopilot Progress",
        "",
        f"Generated: `{generated_at}`",
        "",
        f"Product vision: `{data.get('product_vision', 'unknown')}`",
        "",
        "## Completion",
        "",
        f"- Completion against product vision: `{summary['completion_percent']}%`",
        f"- Completed weighted scope: `{summary['completed_weight']} / {summary['total_weight']}`",
        f"- Including in-progress scope: `{summary['with_in_progress_percent']}%`",
        "",
        "## Next Recommended Mission",
        "",
    ]
    if mission:
        lines.extend(
            [
                f"- Mission: `{mission['id']}`",
                f"- Title: {mission['title']}",
                f"- Priority: `{mission.get('priority', 'unknown')}`",
                f"- Risk: `{mission.get('risk', 'unknown')}`",
                f"- Acceptance criteria: `{len(mission.get('acceptance_criteria') or [])}`",
                "",
                "### Mission Acceptance Criteria",
                "",
            ]
        )
        for criterion in mission.get("acceptance_criteria") or []:
            lines.append(f"- {criterion}")
        lines.extend(["", "### Mission Validation Commands", ""])
        for command in mission.get("validation_commands") or []:
            lines.append(f"- `{command}`")
    else:
        lines.append("No dependency-ready planned mission is available.")

    lines.extend(
        [
            "",
            "## Completed Capabilities",
            "",
            "| Capability | Weight | Evidence Count |",
            "| --- | --- | --- |",
        ]
    )
    for item in completed:
        lines.append(f"| {item['title']} | {item['weight']} | {len(item.get('evidence') or [])} |")

    lines.extend(
        [
            "",
            "## Planned Capability Weight",
            "",
            "| Capability | Weight |",
            "| --- | --- |",
        ]
    )
    for item in planned:
        lines.append(f"| {item['title']} | {item['weight']} |")

    return "\n".join(lines) + "\n"


def render_json(data: dict[str, Any], generated_at: str) -> dict[str, Any]:
    mission = next_mission(data)
    summary = completion_summary(data)
    return {
        "generated_at": generated_at,
        "product_vision": data.get("product_vision", ""),
        "completion": summary,
        "completed_capabilities": [
            item["id"] for item in data["capabilities"] if item["status"] == "completed"
        ],
        "planned_capabilities": [
            item["id"] for item in data["capabilities"] if item["status"] == "planned"
        ],
        "next_recommended_mission": mission,
    }


def write_outputs(data: dict[str, Any], out: Path, generated_at: str) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / "progress.md").write_text(render_markdown(data, generated_at), encoding="utf-8")
    (out / "progress.json").write_text(
        json.dumps(render_json(data, generated_at), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    mission = next_mission(data)
    (out / "next-mission-checklist.md").write_text(
        render_mission_checklist(data, generated_at),
        encoding="utf-8",
    )
    (out / "next-mission.json").write_text(
        json.dumps(mission_payload(data, mission, generated_at), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def check_outputs(data: dict[str, Any], out: Path, generated_at: str) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_out = Path(tmp)
        write_outputs(data, tmp_out, generated_at)
        for filename in ("progress.md", "progress.json", "next-mission-checklist.md", "next-mission.json"):
            expected = (tmp_out / filename).read_text(encoding="utf-8")
            actual_path = out / filename
            if not actual_path.exists():
                raise SystemExit(f"missing generated product progress report: {actual_path}")
            actual = actual_path.read_text(encoding="utf-8")
            if actual != expected:
                raise SystemExit(f"product progress report is stale: {actual_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backlog", type=Path, default=DEFAULT_BACKLOG)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true", help="Fail if committed progress reports are stale.")
    parser.add_argument("--next", action="store_true", help="Print the next safe autopilot mission.")
    parser.add_argument("--next-json", action="store_true", help="Print the next safe autopilot mission as JSON.")
    parser.add_argument("--checklist", action="store_true", help="Print the next safe autopilot mission checklist.")
    parser.add_argument("--generated-at", default=None, help="Override generated timestamp for deterministic checks.")
    args = parser.parse_args()

    data = load_backlog(args.backlog)
    if args.next or args.next_json or args.checklist:
        generated_at = args.generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        mission = next_mission(data)
        if args.next_json:
            print(json.dumps(mission_payload(data, mission, generated_at), indent=2, sort_keys=True))
        elif args.checklist:
            print(render_mission_checklist(data, generated_at), end="")
        else:
            print(render_mission_summary(data, generated_at), end="")
    elif args.check:
        if args.generated_at:
            generated_at = args.generated_at
        else:
            progress_json = args.out / "progress.json"
            if not progress_json.exists():
                raise SystemExit(f"missing generated product progress report: {progress_json}")
            generated_at = str(json.loads(progress_json.read_text(encoding="utf-8")).get("generated_at", ""))
        check_outputs(data, args.out, generated_at)
    else:
        generated_at = args.generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        write_outputs(data, args.out, generated_at)
        summary = completion_summary(data)
        mission = next_mission(data)
        print(f"Product vision completion: {summary['completion_percent']}%")
        if mission:
            print(f"Next recommended mission: {mission['id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
