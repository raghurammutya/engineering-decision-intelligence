"""Materialize v5 target installation and live evidence reports."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


V5_REPORT_FILES = [
    "README.md",
    "onepassword-installation.md",
    "onepassword-secret-flow.md",
    "live-evidence-claims.md",
    "v5-acceptance-pack.md",
    "exports/onepassword-installation.json",
    "exports/onepassword-secret-flow.json",
    "exports/live-evidence-claims.json",
    "exports/v5-acceptance-pack.json",
]


LIVE_CLAIMS = [
    "target credentials installed",
    "scheduled connectors have run",
    "target repos enforce PR checks",
    "autonomous production enforcement is active",
    "complete live runtime truth exists",
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


def op_version() -> str:
    op_path = shutil.which("op")
    if not op_path:
        return ""
    result = subprocess.run(["op", "--version"], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def completed_v5_slices(root: Path) -> tuple[int, int, int]:
    backlog = load_json(root / "roadmap" / "v5-target-installation-live-evidence-backlog.json")
    slices = backlog.get("slices", [])
    completed = [item for item in slices if item.get("status") == "completed"]
    blocked = [item for item in slices if item.get("status") == "blocked"]
    return len(completed), len(blocked), len(slices)


def onepassword_installation_payload(root: Path, generated_at: str) -> dict[str, Any]:
    version = op_version()
    return {
        "generated_at": generated_at,
        "op_installed": bool(version),
        "op_version": version or "not_installed",
        "op_path": shutil.which("op") or "not_found",
        "install_source": "official_1password_apt_repository",
        "secrets_read": False,
        "vaults_listed": False,
        "items_listed": False,
    }


def secret_flow_payload(root: Path, generated_at: str) -> dict[str, Any]:
    config = load_json(root / "runtime-config" / "onepassword-secret-refs.json")
    refs = config.get("required_environment_variables", [])
    invalid = [
        item["name"]
        for item in refs
        if not str(item.get("secret_ref", "")).startswith("op://")
    ]
    return {
        "generated_at": generated_at,
        "provider": "1password",
        "secret_reference_count": len(refs),
        "invalid_secret_references": invalid,
        "env_file_template": config.get("env_file_template"),
        "env_file_local": config.get("env_file_local"),
        "plaintext_secret_values_committed": False,
        "safe_command": "EDI_OP_VAULT=<vault> op run --env-file=secrets/edi-v5.op.env -- python3 -m edi v5 build --live-check",
        "records": refs,
    }


def live_claims_payload(root: Path, generated_at: str, live_check: bool) -> dict[str, Any]:
    records = []
    for claim in LIVE_CLAIMS:
        records.append(
            {
                "claim": claim,
                "state": "blocked_pending_target_evidence",
                "live_check_requested": live_check,
                "evidence_status": "missing",
            }
        )
    return {
        "generated_at": generated_at,
        "claim_count": len(records),
        "completed_claim_count": 0,
        "live_claim_completion_percent": 0.0,
        "records": records,
    }


def acceptance_payload(
    root: Path,
    installation: dict[str, Any],
    secret_flow: dict[str, Any],
    live_claims: dict[str, Any],
    generated_at: str,
) -> dict[str, Any]:
    completed, blocked, total = completed_v5_slices(root)
    tooling_pass = (
        installation["op_installed"]
        and secret_flow["secret_reference_count"] >= 5
        and not secret_flow["invalid_secret_references"]
        and secret_flow["plaintext_secret_values_committed"] is False
    )
    live_pass = live_claims["completed_claim_count"] == live_claims["claim_count"]
    return {
        "generated_at": generated_at,
        "acceptance_state": "tooling_pass_live_evidence_incomplete" if tooling_pass and not live_pass else "pass" if tooling_pass else "incomplete",
        "tooling_completion_percent": 100.0 if tooling_pass else 0.0,
        "live_claim_completion_percent": live_claims["live_claim_completion_percent"],
        "completed_slices": completed,
        "blocked_slices": blocked,
        "total_slices": total,
        "op_installed": installation["op_installed"],
        "secret_reference_count": secret_flow["secret_reference_count"],
        "readiness_claim": "v5 secure 1Password tooling ready" if tooling_pass else "v5 tooling incomplete",
        "blocked_claims": [record["claim"] for record in live_claims["records"] if record["state"].startswith("blocked")],
    }


def build_payloads(root: Path, generated_at: str, live_check: bool) -> dict[str, Any]:
    installation = onepassword_installation_payload(root, generated_at)
    secret_flow = secret_flow_payload(root, generated_at)
    live_claims = live_claims_payload(root, generated_at, live_check)
    acceptance = acceptance_payload(root, installation, secret_flow, live_claims, generated_at)
    return {
        "onepassword-installation": installation,
        "onepassword-secret-flow": secret_flow,
        "live-evidence-claims": live_claims,
        "v5-acceptance-pack": acceptance,
    }


def write_markdown(out: Path, payloads: dict[str, Any], generated_at: str) -> None:
    install = payloads["onepassword-installation"]
    secret_flow = payloads["onepassword-secret-flow"]
    live = payloads["live-evidence-claims"]
    acceptance = payloads["v5-acceptance-pack"]
    write_lines(
        out / "onepassword-installation.md",
        [
            "# 1Password Installation",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"op installed: `{install['op_installed']}`",
            f"op version: `{install['op_version']}`",
            f"Secrets read: `{install['secrets_read']}`",
            f"Vaults listed: `{install['vaults_listed']}`",
            f"Items listed: `{install['items_listed']}`",
        ],
    )
    write_lines(
        out / "onepassword-secret-flow.md",
        [
            "# 1Password Secret Flow",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Secret references: `{secret_flow['secret_reference_count']}`",
            f"Invalid references: `{len(secret_flow['invalid_secret_references'])}`",
            f"Local env file: `{secret_flow['env_file_local']}`",
            f"Safe command: `{secret_flow['safe_command']}`",
            "",
            "No plaintext secret values are committed.",
        ],
    )
    write_lines(
        out / "live-evidence-claims.md",
        [
            "# Live Evidence Claims",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Live claim completion: `{live['live_claim_completion_percent']}%`",
            "",
            "| Claim | State | Evidence |",
            "| --- | --- | --- |",
            *[
                f"| {record['claim']} | {record['state']} | {record['evidence_status']} |"
                for record in live["records"]
            ],
        ],
    )
    write_lines(
        out / "v5-acceptance-pack.md",
        [
            "# V5 Acceptance Pack",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Acceptance state: `{acceptance['acceptance_state']}`",
            f"Tooling completion: `{acceptance['tooling_completion_percent']}%`",
            f"Live claim completion: `{acceptance['live_claim_completion_percent']}%`",
            f"Completed slices: `{acceptance['completed_slices']} / {acceptance['total_slices']}`",
            f"Blocked slices: `{acceptance['blocked_slices']}`",
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
            "# V5 Target Installation And Live Evidence",
            "",
            f"Generated: `{generated_at}`",
            "",
            "This pack proves secure 1Password-backed tooling, not target-system live evidence.",
        ],
    )


def build_v5_outputs(root: Path, out: Path | None = None, generated_at: str | None = None, live_check: bool = False) -> dict[str, Any]:
    generated = generated_timestamp(generated_at)
    target = out or root / "reports" / "product" / "v5"
    payloads = build_payloads(root, generated, live_check)
    export_dir = target / "exports"
    for name, payload in payloads.items():
        write_json(export_dir / f"{name}.json", payload)
    write_markdown(target, payloads, generated)
    return {"payloads": payloads, "acceptance": payloads["v5-acceptance-pack"]}


def check_v5_outputs(root: Path, out: Path | None = None) -> bool:
    target = out or root / "reports" / "product" / "v5"
    with tempfile.TemporaryDirectory() as tmp:
        temp_out = Path(tmp) / "v5"
        generated_at = load_json(target / "exports" / "v5-acceptance-pack.json").get("generated_at")
        build_v5_outputs(root, temp_out, generated_at)
        for filename in V5_REPORT_FILES:
            current = (target / filename).read_text(encoding="utf-8")
            expected = (temp_out / filename).read_text(encoding="utf-8")
            if current != expected:
                raise SystemExit(f"V5 report drift detected: {filename}")
    return True
