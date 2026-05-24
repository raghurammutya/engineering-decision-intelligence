"""Materialize operational substrate reconciliation reports."""

from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SUBSTRATE_REPORT_FILES = [
    "README.md",
    "lifecycle-policy.md",
    "release-management.md",
    "storage-management.md",
    "infrastructure-management.md",
    "substrate-acceptance-pack.md",
    "exports/lifecycle-policy.json",
    "exports/release-management.json",
    "exports/storage-management.json",
    "exports/infrastructure-management.json",
    "exports/substrate-acceptance-pack.json",
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


def substrate_config(root: Path) -> dict[str, Any]:
    return load_json(root / "runtime-config" / "operational-substrate.json")


def live_evidence_config(root: Path) -> dict[str, Any]:
    path = root / "runtime-config" / "operational-substrate-live-evidence.json"
    return load_json(path) if path.exists() else {}


def evidence_records(config: dict[str, Any], live_evidence: dict[str, Any], domain: str) -> list[dict[str, Any]]:
    records = []
    live_domain = live_evidence.get(domain, {})
    observed_at = live_evidence.get("generated_at", "")
    for item in config.get(domain, {}).get("required_evidence", []):
        override = live_domain.get(item.get("id", ""), {})
        observed = bool(override.get("observed", False))
        records.append(
            {
                "id": item.get("id", ""),
                "label": item.get("label", item.get("id", "")),
                "live_required": bool(item.get("live_required", True)),
                "observed": observed,
                "state": override.get(
                    "state",
                    "observed_live_target_evidence" if observed else "missing_live_target_evidence",
                ),
                "evidence": override.get("evidence", ""),
                "observed_at": override.get("observed_at", observed_at),
            }
        )
    return records


def domain_payload(config: dict[str, Any], live_evidence: dict[str, Any], generated_at: str, domain: str) -> dict[str, Any]:
    records = evidence_records(config, live_evidence, domain)
    observed_count = len([record for record in records if record["observed"]])
    evidence_count = len(records)
    return {
        "generated_at": generated_at,
        "domain": domain,
        "source_boundary": config.get("source_boundary"),
        "fail_closed": bool(config.get("fail_closed", True)),
        "required_evidence_count": evidence_count,
        "observed_evidence_count": observed_count,
        "live_evidence_completion_percent": round(observed_count / evidence_count * 100, 1) if evidence_count else 0.0,
        "records": records,
        "policy": {key: value for key, value in config.get(domain, {}).items() if key != "required_evidence"},
    }


def lifecycle_payload(config: dict[str, Any], generated_at: str) -> dict[str, Any]:
    lifecycle = config.get("canonical_lifecycle", {})
    admission = config.get("admission_model", [])
    maturity = config.get("maturity_levels", [])
    return {
        "generated_at": generated_at,
        "domain": config.get("domain"),
        "scope": config.get("scope"),
        "source_boundary": config.get("source_boundary"),
        "fail_closed": bool(config.get("fail_closed", True)),
        "environment_count": len(lifecycle.get("runtime_separation", [])),
        "canonical_operation_count": len(lifecycle.get("canonical_operations", [])),
        "promotion_order": lifecycle.get("promotion_order", []),
        "promotion_contract": lifecycle.get("promotion_contract"),
        "promotion_path_policy": lifecycle.get("promotion_path_policy"),
        "ghcr_policy": lifecycle.get("ghcr_policy"),
        "maturity_level_count": len(maturity),
        "admission_rule_count": len(admission),
        "runtime_separation": lifecycle.get("runtime_separation", []),
        "canonical_operations": lifecycle.get("canonical_operations", []),
        "maturity_levels": maturity,
        "admission_model": admission,
    }


def acceptance_payload(payloads: dict[str, Any], generated_at: str) -> dict[str, Any]:
    lifecycle = payloads["lifecycle-policy"]
    release = payloads["release-management"]
    storage = payloads["storage-management"]
    infrastructure = payloads["infrastructure-management"]
    policy_ready = (
        lifecycle["environment_count"] == 4
        and lifecycle["promotion_order"] == ["dev", "test", "staging", "prod"]
        and lifecycle["canonical_operation_count"] >= 3
        and release["required_evidence_count"] >= 6
        and storage["required_evidence_count"] >= 6
        and infrastructure["required_evidence_count"] >= 6
        and release["fail_closed"]
        and storage["fail_closed"]
        and infrastructure["fail_closed"]
    )
    domains = [release, storage, infrastructure]
    required_count = sum(domain["required_evidence_count"] for domain in domains)
    observed_count = sum(domain["observed_evidence_count"] for domain in domains)
    live_percent = round(observed_count / required_count * 100, 1) if required_count else 0.0
    if policy_ready and live_percent == 100.0:
        acceptance_state = "policy_pack_ready_live_evidence_complete"
    elif policy_ready:
        acceptance_state = "policy_pack_ready_live_evidence_incomplete"
    else:
        acceptance_state = "incomplete"
    blocked_claims = []
    for domain, claim in (
        (release, "release management live evidence is complete"),
        (storage, "storage management live evidence is complete"),
        (infrastructure, "infrastructure management live evidence is complete"),
    ):
        if domain["live_evidence_completion_percent"] < 100.0:
            blocked_claims.append(claim)
    return {
        "generated_at": generated_at,
        "acceptance_state": acceptance_state,
        "policy_completion_percent": 100.0 if policy_ready else 0.0,
        "live_evidence_completion_percent": live_percent,
        "required_live_evidence_count": required_count,
        "observed_live_evidence_count": observed_count,
        "readiness_claim": "operational substrate lifecycle policy pack ready" if policy_ready else "operational substrate lifecycle policy pack incomplete",
        "blocked_claims": blocked_claims,
    }


def build_payloads(root: Path, generated_at: str) -> dict[str, Any]:
    config = substrate_config(root)
    live_evidence = live_evidence_config(root)
    payloads = {
        "lifecycle-policy": lifecycle_payload(config, generated_at),
        "release-management": domain_payload(config, live_evidence, generated_at, "release_management"),
        "storage-management": domain_payload(config, live_evidence, generated_at, "storage_management"),
        "infrastructure-management": domain_payload(config, live_evidence, generated_at, "infrastructure_management"),
    }
    payloads["substrate-acceptance-pack"] = acceptance_payload(payloads, generated_at)
    return payloads


def render_table(records: list[dict[str, Any]], fields: list[str]) -> list[str]:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for record in records:
        lines.append("| " + " | ".join(str(record.get(field, "")) for field in fields) + " |")
    return lines


def write_markdown(out: Path, payloads: dict[str, Any], generated_at: str) -> None:
    lifecycle = payloads["lifecycle-policy"]
    acceptance = payloads["substrate-acceptance-pack"]
    write_lines(
        out / "lifecycle-policy.md",
        [
            "# Operational Substrate Lifecycle Policy",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Scope: `{lifecycle['scope']}`",
            f"Promotion order: `{' -> '.join(lifecycle['promotion_order'])}`",
            f"Promotion contract: `{lifecycle['promotion_contract']}`",
            f"Promotion path policy: `{lifecycle['promotion_path_policy']}`",
            f"GHCR policy: `{lifecycle['ghcr_policy']}`",
            "",
            "## Runtime Separation",
            "",
            *render_table(lifecycle["runtime_separation"], ["environment", "purpose", "builds_allowed", "broad_tests_allowed", "runtime_only"]),
            "",
            "## Admission Model",
            "",
            *render_table(lifecycle["admission_model"], ["operation", "admission"]),
        ],
    )
    for name, title in [
        ("release-management", "# Release Management Evidence"),
        ("storage-management", "# Storage Management Evidence"),
        ("infrastructure-management", "# Infrastructure Management Evidence"),
    ]:
        payload = payloads[name]
        write_lines(
            out / f"{name}.md",
            [
                title,
                "",
                f"Generated: `{generated_at}`",
                "",
                f"Source boundary: `{payload['source_boundary']}`",
                f"Fail closed: `{payload['fail_closed']}`",
                f"Live evidence completion: `{payload['live_evidence_completion_percent']}%`",
                "",
                *render_table(payload["records"], ["id", "label", "live_required", "state", "evidence"]),
            ],
        )
    write_lines(
        out / "substrate-acceptance-pack.md",
        [
            "# Operational Substrate Acceptance Pack",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Acceptance state: `{acceptance['acceptance_state']}`",
            f"Policy completion: `{acceptance['policy_completion_percent']}%`",
            f"Live evidence completion: `{acceptance['live_evidence_completion_percent']}%`",
            f"Live evidence observed: `{acceptance['observed_live_evidence_count']} / {acceptance['required_live_evidence_count']}`",
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
            "# Operational Substrate Reconciliation",
            "",
            f"Generated: `{generated_at}`",
            "",
            "This pack makes release management, storage management, and infrastructure management first-class EDI lifecycle domains.",
            "It defines the recommended dev-first artifact-promoted lifecycle, and live substrate claims remain blocked until the required target evidence is fully observed.",
        ],
    )


def build_substrate_outputs(root: Path, out: Path | None = None, generated_at: str | None = None) -> dict[str, Any]:
    generated = generated_timestamp(generated_at)
    target = out or root / "reports" / "product" / "substrate"
    payloads = build_payloads(root, generated)
    export_dir = target / "exports"
    for name, payload in payloads.items():
        write_json(export_dir / f"{name}.json", payload)
    write_markdown(target, payloads, generated)
    return {"payloads": payloads, "acceptance": payloads["substrate-acceptance-pack"]}


def check_substrate_outputs(root: Path, out: Path | None = None) -> bool:
    target = out or root / "reports" / "product" / "substrate"
    with tempfile.TemporaryDirectory() as tmp:
        temp_out = Path(tmp) / "substrate"
        generated_at = load_json(target / "exports" / "substrate-acceptance-pack.json").get("generated_at")
        build_substrate_outputs(root, temp_out, generated_at)
        for filename in SUBSTRATE_REPORT_FILES:
            current = (target / filename).read_text(encoding="utf-8")
            expected = (temp_out / filename).read_text(encoding="utf-8")
            if current != expected:
                raise SystemExit(f"Operational substrate report drift detected: {filename}")
    return True
