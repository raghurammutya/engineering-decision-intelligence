"""Materialize v4 live enforcement readiness reports."""

from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


V4_REPORT_FILES = [
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
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_lines(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def generated_timestamp(generated_at: str | None = None) -> str:
    return generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def runtime_config(root: Path, filename: str) -> dict[str, Any]:
    return load_json(root / "runtime-config" / filename)


def completed_v4_slices(root: Path) -> tuple[int, int]:
    backlog = load_json(root / "roadmap" / "v4-live-enforcement-readiness-backlog.json")
    slices = backlog.get("slices", [])
    completed = [item for item in slices if item.get("status") == "completed"]
    return len(completed), len(slices)


def live_connector_payload(root: Path, generated_at: str) -> dict[str, Any]:
    config = runtime_config(root, "live-connectors.json")
    records = config.get("connectors", [])
    return {
        "generated_at": generated_at,
        "connector_count": len(records),
        "ready_for_install_count": sum(1 for item in records if item.get("status") == "ready_for_install"),
        "credential_refs": sorted({item.get("credential_ref") for item in records}),
        "records": records,
        "claim_boundary": "configured_for_install_not_authenticated_live_polling",
    }


def reconciliation_payload(root: Path, generated_at: str) -> dict[str, Any]:
    config = runtime_config(root, "reconciliation-schedule.json")
    records = config.get("loops", [])
    return {
        "generated_at": generated_at,
        "loop_count": len(records),
        "fail_closed_count": sum(1 for item in records if item.get("fail_closed")),
        "records": records,
    }


def ci_enforcement_payload(root: Path, generated_at: str) -> dict[str, Any]:
    config = runtime_config(root, "ci-enforcement-policy.json")
    records = config.get("enforcement_modes", [])
    return {
        "generated_at": generated_at,
        "mode_count": len(records),
        "blocking_modes": [item for item in records if item.get("ci_status") == "fail"],
        "manual_review_modes": [item for item in records if item.get("ci_status") == "manual_review"],
        "commands": config.get("commands", []),
        "target_state": config.get("target_state"),
        "records": records,
    }


def remediation_payload(root: Path, generated_at: str) -> dict[str, Any]:
    config = runtime_config(root, "remediation-operating-model.json")
    return {
        "generated_at": generated_at,
        "state_count": len(config.get("states", [])),
        "transition_count": len(config.get("transitions", [])),
        "fail_closed_states": config.get("fail_closed_states", []),
        "records": config.get("transitions", []),
    }


def security_payload(root: Path, generated_at: str) -> dict[str, Any]:
    config = runtime_config(root, "security-access-model.json")
    return {
        "generated_at": generated_at,
        "role_count": len(config.get("principals", [])),
        "plaintext_secrets_allowed": bool(config.get("secret_policy", {}).get("plaintext_in_repo")),
        "audit_policy": config.get("audit_policy", {}),
        "records": config.get("principals", []),
    }


def persistence_payload(root: Path, generated_at: str) -> dict[str, Any]:
    config = runtime_config(root, "persistence-model.json")
    return {
        "generated_at": generated_at,
        "store_count": len(config.get("stores", [])),
        "current_backend": config.get("current_backend"),
        "backend_observation": config.get("backend_observation", {}),
        "production_backend_required": config.get("production_backend_required"),
        "records": config.get("stores", []),
    }


def packaging_payload(root: Path, generated_at: str) -> dict[str, Any]:
    config = runtime_config(root, "deployment-packaging.json")
    return {
        "generated_at": generated_at,
        "artifact_count": len(config.get("artifacts", [])),
        "install_modes": config.get("install_modes", []),
        "production_installation_status": config.get("production_installation_status"),
        "records": config.get("artifacts", []),
    }


def slo_payload(root: Path, generated_at: str) -> dict[str, Any]:
    config = runtime_config(root, "operational-slos.json")
    return {
        "generated_at": generated_at,
        "slo_count": len(config.get("slos", [])),
        "records": config.get("slos", []),
    }


def pilot_payload(root: Path, generated_at: str) -> dict[str, Any]:
    config = runtime_config(root, "external-pilot-operation.json")
    return {
        "generated_at": generated_at,
        "pilot_name": config.get("pilot_name"),
        "entry_criteria_count": len(config.get("entry_criteria", [])),
        "exit_criteria_count": len(config.get("exit_criteria", [])),
        "status": config.get("status"),
        "entry_criteria": config.get("entry_criteria", []),
        "exit_criteria": config.get("exit_criteria", []),
    }


def build_payloads(root: Path, generated_at: str) -> dict[str, Any]:
    return {
        "live-connector-readiness": live_connector_payload(root, generated_at),
        "continuous-reconciliation": reconciliation_payload(root, generated_at),
        "ci-pr-enforcement": ci_enforcement_payload(root, generated_at),
        "remediation-operations": remediation_payload(root, generated_at),
        "security-access": security_payload(root, generated_at),
        "persistence-history": persistence_payload(root, generated_at),
        "deployment-packaging": packaging_payload(root, generated_at),
        "operational-slos": slo_payload(root, generated_at),
        "external-pilot-operations": pilot_payload(root, generated_at),
    }


def acceptance_payload(root: Path, out: Path, payloads: dict[str, Any], generated_at: str) -> dict[str, Any]:
    completed, total = completed_v4_slices(root)
    required_exports = [
        "live-connector-readiness.json",
        "continuous-reconciliation.json",
        "ci-pr-enforcement.json",
        "remediation-operations.json",
        "security-access.json",
        "persistence-history.json",
        "deployment-packaging.json",
        "operational-slos.json",
        "external-pilot-operations.json",
        "v4-acceptance-pack.json",
    ]
    export_dir = out / "exports"
    present = [name for name in required_exports if name == "v4-acceptance-pack.json" or (export_dir / name).exists()]
    pass_state = (
        completed == total
        and len(present) == len(required_exports)
        and payloads["live-connector-readiness"]["connector_count"] >= 6
        and payloads["continuous-reconciliation"]["loop_count"] >= 5
        and payloads["ci-pr-enforcement"]["target_state"] == "ready_for_pr_check_install"
        and payloads["security-access"]["plaintext_secrets_allowed"] is False
        and payloads["persistence-history"]["production_backend_required"] is True
        and payloads["operational-slos"]["slo_count"] >= 5
        and payloads["external-pilot-operations"]["status"] == "ready_to_schedule"
    )
    return {
        "generated_at": generated_at,
        "acceptance_state": "pass" if pass_state else "incomplete",
        "completed_slices": completed,
        "total_slices": total,
        "required_exports": required_exports,
        "present_exports": present,
        "missing_exports": sorted(set(required_exports) - set(present)),
        "connector_count": payloads["live-connector-readiness"]["connector_count"],
        "reconciliation_loop_count": payloads["continuous-reconciliation"]["loop_count"],
        "ci_target_state": payloads["ci-pr-enforcement"]["target_state"],
        "security_roles": payloads["security-access"]["role_count"],
        "slo_count": payloads["operational-slos"]["slo_count"],
        "pilot_status": payloads["external-pilot-operations"]["status"],
        "readiness_claim": "initial v4 live enforcement readiness pack ready" if pass_state else "initial v4 readiness pack not ready",
        "blocked_claims": [
            "credentials installed in target systems",
            "scheduled connectors observed running",
            "target repositories enforcing PR checks",
            "autonomous production enforcement active",
            "complete live runtime truth",
        ],
    }


def render_table(records: list[dict[str, Any]], fields: list[str]) -> list[str]:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    if not records:
        lines.append("| No records available " + " | " * (len(fields) - 1) + "|")
        return lines
    for record in records[:80]:
        lines.append("| " + " | ".join(str(record.get(field, "")) for field in fields) + " |")
    return lines


def write_markdown(out: Path, payloads: dict[str, Any], acceptance: dict[str, Any], generated_at: str) -> None:
    specs = [
        ("live-connector-readiness.md", "# Live Connector Readiness", "live-connector-readiness", ["id", "type", "mode", "status"]),
        ("continuous-reconciliation-summary.md", "# Continuous Reconciliation Summary", "continuous-reconciliation", ["id", "cadence", "source", "fail_closed"]),
        ("ci-pr-enforcement-summary.md", "# CI PR Enforcement Summary", "ci-pr-enforcement", ["risk", "ci_status", "requires"]),
        ("remediation-operations-summary.md", "# Remediation Operations Summary", "remediation-operations", ["from", "to", "requires"]),
        ("security-access-summary.md", "# Security Access Summary", "security-access", ["role", "permissions"]),
        ("persistence-history-summary.md", "# Persistence History Summary", "persistence-history", ["id", "type", "retention_days"]),
        ("deployment-packaging-summary.md", "# Deployment Packaging Summary", "deployment-packaging", ["id", "path", "status"]),
        ("operational-slo-summary.md", "# Operational SLO Summary", "operational-slos", ["id", "target", "measurement"]),
    ]
    for filename, title, key, fields in specs:
        payload = payloads[key]
        lines = [title, "", f"Generated: `{generated_at}`", ""]
        if key == "persistence-history":
            lines.extend(
                [
                    f"Current backend: `{payload.get('current_backend', 'unknown')}`",
                    f"Backend observed: `{payload.get('backend_observation', {}).get('backend_type', 'unknown')}`",
                    f"Backend observed at: `{payload.get('backend_observation', {}).get('observed_at', 'unknown')}`",
                    "",
                ]
            )
        lines.extend(render_table(payload.get("records", []), fields))
        write_lines(out / filename, lines)

    pilot = payloads["external-pilot-operations"]
    write_lines(
        out / "external-pilot-operations.md",
        [
            "# External Pilot Operations",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Pilot: `{pilot['pilot_name']}`",
            f"Status: `{pilot['status']}`",
            "",
            "## Entry Criteria",
            "",
            *[f"- {item}" for item in pilot["entry_criteria"]],
            "",
            "## Exit Criteria",
            "",
            *[f"- {item}" for item in pilot["exit_criteria"]],
        ],
    )
    write_lines(
        out / "v4-acceptance-pack.md",
        [
            "# V4 Acceptance Pack",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Acceptance state: `{acceptance['acceptance_state']}`",
            f"Completed slices: `{acceptance['completed_slices']} / {acceptance['total_slices']}`",
            f"Connectors: `{acceptance['connector_count']}`",
            f"Reconciliation loops: `{acceptance['reconciliation_loop_count']}`",
            f"CI target state: `{acceptance['ci_target_state']}`",
            f"Security roles: `{acceptance['security_roles']}`",
            f"SLOs: `{acceptance['slo_count']}`",
            f"Pilot status: `{acceptance['pilot_status']}`",
            f"Readiness claim: `{acceptance['readiness_claim']}`",
            "",
            "## Blocked Claims",
            "",
            *[f"- `{claim}`" for claim in acceptance["blocked_claims"]],
        ],
    )
    write_lines(
        out / "README.md",
        [
            "# V4 Live Enforcement Readiness Reports",
            "",
            f"Generated: `{generated_at}`",
            "",
            "These reports prove readiness contracts for live connectors and CI enforcement.",
            "They do not prove target-system installation or active production enforcement.",
        ],
    )


def write_operator_view(out: Path, acceptance: dict[str, Any], generated_at: str) -> None:
    html = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>EDI V4 Readiness</title>
<style>body{{margin:0;font-family:Arial,sans-serif;color:#172026;background:#f4f7f9}}header{{background:#17324d;color:white;padding:22px 30px}}main{{max-width:1120px;margin:0 auto;padding:24px 30px 40px}}.metrics{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}}.metric,section{{background:white;border:1px solid #d7e0e7;border-radius:6px;padding:16px}}.metric strong{{display:block;font-size:26px;margin-top:6px}}section{{margin-top:16px}}</style></head>
<body><header><h1>Engineering Decision Intelligence V4</h1><p>Generated: {generated_at}</p></header>
<main><div class="metrics">
<div class="metric">V4 acceptance<strong>{acceptance['acceptance_state']}</strong></div>
<div class="metric">Connectors<strong>{acceptance['connector_count']}</strong></div>
<div class="metric">Reconciliation loops<strong>{acceptance['reconciliation_loop_count']}</strong></div>
<div class="metric">SLOs<strong>{acceptance['slo_count']}</strong></div>
<div class="metric">Pilot status<strong>{acceptance['pilot_status']}</strong></div>
</div><section><h2>Boundary</h2><p>V4 proves readiness contracts. It does not prove target credentials, scheduled connector execution, or active production enforcement.</p></section></main></body></html>
"""
    (out / "v4-operator-view.html").write_text(html, encoding="utf-8")


def build_v4_outputs(root: Path, out: Path | None = None, generated_at: str | None = None) -> dict[str, Any]:
    generated = generated_timestamp(generated_at)
    target = out or root / "reports" / "product" / "v4"
    payloads = build_payloads(root, generated)
    export_dir = target / "exports"
    for name, payload in payloads.items():
        write_json(export_dir / f"{name}.json", payload)
    acceptance = acceptance_payload(root, target, payloads, generated)
    write_json(export_dir / "v4-acceptance-pack.json", acceptance)
    write_markdown(target, payloads, acceptance, generated)
    write_operator_view(target, acceptance, generated)
    return {"payloads": payloads, "acceptance": acceptance}


def check_v4_outputs(root: Path, out: Path | None = None) -> bool:
    target = out or root / "reports" / "product" / "v4"
    with tempfile.TemporaryDirectory() as tmp:
        temp_out = Path(tmp) / "v4"
        generated_at = load_json(target / "exports" / "v4-acceptance-pack.json").get("generated_at")
        build_v4_outputs(root, temp_out, generated_at)
        for filename in V4_REPORT_FILES:
            current = (target / filename).read_text(encoding="utf-8")
            expected = (temp_out / filename).read_text(encoding="utf-8")
            if current != expected:
                raise SystemExit(f"V4 report drift detected: {filename}")
    return True
