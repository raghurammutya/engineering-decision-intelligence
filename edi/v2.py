"""Materialize v2 operational intelligence reports."""

from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


V2_REPORT_FILES = [
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
]


def load_json(path: Path, default: Any | None = None) -> Any:
    if not path.exists():
        if default is not None:
            return default
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_lines(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def generated_timestamp(generated_at: str | None = None) -> str:
    return generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def count_values(records: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        value = str(record.get(field, "unknown"))
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def load_portfolio_config(root: Path) -> dict[str, Any]:
    return load_json(root / "policies" / "portfolio-repositories.json")


def repository_records(root: Path, generated_at: str) -> list[dict[str, Any]]:
    config = load_portfolio_config(root)
    records: list[dict[str, Any]] = []
    for item in config.get("repositories", []):
        report_dir = root / str(item["report_dir"])
        manifest = load_json(report_dir / "manifest.json", {})
        counts = manifest.get("counts") or {}
        local_git_state = manifest.get("local_git_state") or {}
        records.append(
            {
                "repo_id": item["repo_id"],
                "name": item["name"],
                "path": item["path"],
                "role": item.get("role", "unknown"),
                "owner": item.get("owner", "unknown"),
                "evidence_boundary": item.get("evidence_boundary", "unspecified"),
                "report_dir": item["report_dir"],
                "scan_observed": bool(manifest),
                "artifact_count": counts.get("artifacts", 0),
                "risk_counts": counts.get("risk", {}),
                "autonomy_counts": counts.get("autonomy_mode", {}),
                "branch": local_git_state.get("branch", "unknown"),
                "dirty_file_count": local_git_state.get("dirty_file_count", "unknown"),
                "generated_at": manifest.get("generated_at", generated_at),
            }
        )
    return records


def portfolio_payload(root: Path, generated_at: str) -> dict[str, Any]:
    records = repository_records(root, generated_at)
    total_artifacts = sum(int(record.get("artifact_count") or 0) for record in records)
    blocked_repos = [
        record["repo_id"]
        for record in records
        if int((record.get("autonomy_counts") or {}).get("blocked", 0)) > 0
    ]
    return {
        "generated_at": generated_at,
        "portfolio_id": load_portfolio_config(root).get("portfolio_id"),
        "repo_count": len(records),
        "total_artifacts": total_artifacts,
        "blocked_repo_ids": blocked_repos,
        "records": records,
    }


def runtime_connector_payload(root: Path, generated_at: str) -> dict[str, Any]:
    raw = load_json(root / "policies" / "runtime-connector-fixtures.json")
    required = {
        "event_id",
        "source",
        "source_type",
        "observed_at",
        "service",
        "signal_type",
        "environment",
        "confidence",
        "related_paths",
        "evidence_boundary",
    }
    records = raw.get("events", [])
    invalid = [
        {"event_id": record.get("event_id", "unknown"), "missing_fields": sorted(required - set(record))}
        for record in records
        if required - set(record)
    ]
    return {
        "generated_at": generated_at,
        "contract_id": raw.get("contract_id", "runtime-connector-contract-v1"),
        "source_boundary": "static_fixture_contract_not_live_runtime_truth",
        "record_count": len(records),
        "valid_record_count": len(records) - len(invalid),
        "invalid_records": invalid,
        "signal_type_counts": count_values(records, "signal_type"),
        "environment_counts": count_values(records, "environment"),
        "records": records,
        "contract_state": "pass" if not invalid and records else "incomplete",
    }


def load_decisions(root: Path) -> list[dict[str, Any]]:
    executive = load_json(root / "reports" / "ml-pilot" / "exports" / "executive-decisions.json", {})
    records = executive.get("top_decisions") or []
    return records


def incident_payload(root: Path, generated_at: str) -> dict[str, Any]:
    raw = load_json(root / "policies" / "incident-fixtures.json")
    decisions = load_decisions(root)
    decision_paths = {record.get("path") for record in decisions}
    correlations: list[dict[str, Any]] = []
    for incident in raw.get("incidents", []):
        related = [path for path in incident.get("related_paths", []) if path in decision_paths]
        correlations.append(
            {
                "incident_id": incident["incident_id"],
                "severity": incident["severity"],
                "service": incident["service"],
                "status": incident["status"],
                "related_decision_paths": related,
                "correlation_state": "matched_decision" if related else "no_matching_decision",
                "evidence_boundary": incident.get("evidence_boundary", "fixture"),
            }
        )
    return {
        "generated_at": generated_at,
        "source_boundary": "static_incident_fixture_not_live_incident_feed",
        "record_count": len(correlations),
        "matched_count": sum(1 for record in correlations if record["correlation_state"] == "matched_decision"),
        "severity_counts": count_values(correlations, "severity"),
        "records": correlations,
    }


def remediation_payload(root: Path, generated_at: str) -> dict[str, Any]:
    raw = load_json(root / "policies" / "v2-remediation-state.json")
    decisions = load_decisions(root)
    decision_by_path = {record.get("path"): record for record in decisions}
    records: list[dict[str, Any]] = []
    for item in raw.get("records", []):
        decision = decision_by_path.get(item["path"], {})
        records.append(
            {
                "path": item["path"],
                "state": item["state"],
                "owner": item["owner"],
                "expires_at": item["expires_at"],
                "evidence": item["evidence"],
                "next_action": item["next_action"],
                "risk_level": decision.get("risk_level", "unknown"),
                "priority": decision.get("priority", "unknown"),
                "decision_linked": bool(decision),
            }
        )
    high_risk_unlinked = [
        record
        for record in decisions
        if record.get("risk_level") in {"critical", "high"} and record.get("path") not in {item["path"] for item in records}
    ]
    return {
        "generated_at": generated_at,
        "record_count": len(records),
        "state_counts": count_values(records, "state"),
        "records": records,
        "high_risk_unlinked_count": len(high_risk_unlinked),
        "high_risk_unlinked_paths": [record.get("path") for record in high_risk_unlinked[:25]],
    }


def policy_preflight_payload(root: Path, generated_at: str) -> dict[str, Any]:
    decisions = load_decisions(root)
    records: list[dict[str, Any]] = []
    for decision in decisions[:100]:
        risk = decision.get("risk_level", "unknown")
        owner = decision.get("owner", "")
        evidence = decision.get("evidence_status", "")
        if risk == "critical":
            state = "blocked"
            reason = "critical risk requires controlled admission before execution"
        elif risk == "high" and (not owner or owner in {"missing_or_unknown", "unknown"}):
            state = "approval_required"
            reason = "high risk requires owner review"
        elif evidence == "missing" and risk in {"high", "medium"}:
            state = "approval_required"
            reason = "evidence is missing for elevated risk"
        else:
            state = "allowed"
            reason = "no blocking deterministic rule matched"
        records.append(
            {
                "path": decision.get("path"),
                "risk_level": risk,
                "owner": owner,
                "decision": state,
                "reason": reason,
                "deterministic": True,
            }
        )
    return {
        "generated_at": generated_at,
        "record_count": len(records),
        "decision_counts": count_values(records, "decision"),
        "records": records,
    }


def confidence_for_decision(decision: dict[str, Any]) -> tuple[float, list[str]]:
    score = 0.55
    reasons = ["base scanner inference"]
    if decision.get("owner") and decision.get("owner") not in {"missing_or_unknown", "unknown"}:
        score += 0.15
        reasons.append("owner available")
    if decision.get("evidence_status") == "present":
        score += 0.15
        reasons.append("evidence present")
    if decision.get("risk_level") in {"critical", "high"}:
        score += 0.05
        reasons.append("high-risk deterministic rules applied")
    if decision.get("canonical_status") in {"canonical", "uses_canonical_command"}:
        score += 0.1
        reasons.append("canonical path evidence")
    return round(min(score, 0.95), 2), reasons


def trust_confidence_payload(root: Path, generated_at: str) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for decision in load_decisions(root)[:100]:
        score, reasons = confidence_for_decision(decision)
        review_required = score < 0.75 and decision.get("risk_level") in {"critical", "high"}
        records.append(
            {
                "path": decision.get("path"),
                "risk_level": decision.get("risk_level"),
                "confidence": score,
                "confidence_reasons": reasons,
                "review_required": review_required,
                "enforcement_authority": "none_ai_cannot_raise_authority",
            }
        )
    return {
        "generated_at": generated_at,
        "record_count": len(records),
        "low_confidence_high_risk_count": sum(1 for record in records if record["review_required"]),
        "records": records,
    }


def evidence_lineage_payload(root: Path, generated_at: str) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for decision in load_decisions(root)[:50]:
        path = decision.get("path")
        evidence = [
            "reports/ml-pilot/findings.jsonl",
            "reports/ml-pilot/exports/executive-decisions.json",
            "policies/ml-pilot-policy.json",
        ]
        if decision.get("evidence_status") == "present":
            evidence.append("reports/ml-pilot/evidence-quality-map.md")
        gaps = []
        if decision.get("owner") in {"", "unknown", "missing_or_unknown", None}:
            gaps.append("owner evidence")
        if decision.get("evidence_status") == "missing":
            gaps.append("rollback or safety evidence")
        records.append(
            {
                "decision_id": f"decision:{path}",
                "path": path,
                "risk_level": decision.get("risk_level"),
                "source_evidence": evidence,
                "lineage": [
                    {"source": f"artifact:{path}", "relation": "has_decision", "target": f"decision:{path}"},
                    {"source": f"decision:{path}", "relation": "derived_from", "target": "reports/ml-pilot/findings.jsonl"},
                    {"source": f"decision:{path}", "relation": "evaluated_by", "target": "policies/ml-pilot-policy.json"},
                ],
                "lineage_gaps": gaps,
            }
        )
    return {
        "generated_at": generated_at,
        "record_count": len(records),
        "lineage_gap_count": sum(1 for record in records if record["lineage_gaps"]),
        "records": records,
    }


def connector_sdk_payload(root: Path, generated_at: str) -> dict[str, Any]:
    connectors = [
        {
            "connector_type": "repository",
            "input_contract": "policies/portfolio-repositories.json",
            "required_behavior": "declare path, report_dir, owner, role, and evidence boundary",
        },
        {
            "connector_type": "runtime",
            "input_contract": "policies/runtime-connector-fixtures.json",
            "required_behavior": "declare source, timestamp, confidence, signal type, and related paths",
        },
        {
            "connector_type": "incident",
            "input_contract": "policies/incident-fixtures.json",
            "required_behavior": "declare incident id, severity, service, related paths, and evidence boundary",
        },
        {
            "connector_type": "remediation",
            "input_contract": "policies/v2-remediation-state.json",
            "required_behavior": "declare state, owner, expiry, evidence, and next action",
        },
    ]
    return {
        "generated_at": generated_at,
        "sdk_version": "connector-sdk-v1",
        "dependency_free": True,
        "connector_count": len(connectors),
        "connectors": connectors,
        "validation_command": "python3 -m edi v2 build --check",
    }


def completed_v2_slices(root: Path) -> tuple[int, int]:
    backlog = load_json(root / "roadmap" / "v2-operational-intelligence-backlog.json")
    slices = backlog.get("slices", [])
    completed = [item for item in slices if item.get("status") == "completed"]
    return len(completed), len(slices)


def v2_acceptance_payload(root: Path, out: Path, generated_at: str) -> dict[str, Any]:
    required_exports = [
        "portfolio-summary.json",
        "runtime-connector-contract.json",
        "incident-correlations.json",
        "closed-loop-remediation.json",
        "policy-preflight.json",
        "trust-confidence.json",
        "evidence-lineage.json",
        "connector-sdk.json",
        "v2-acceptance-pack.json",
    ]
    export_dir = out / "exports"
    present = [name for name in required_exports if name == "v2-acceptance-pack.json" or (export_dir / name).exists()]
    completed, total = completed_v2_slices(root)
    portfolio = load_json(export_dir / "portfolio-summary.json", {})
    runtime = load_json(export_dir / "runtime-connector-contract.json", {})
    preflight = load_json(export_dir / "policy-preflight.json", {})
    pass_state = (
        len(present) == len(required_exports)
        and completed == total
        and int(portfolio.get("repo_count", 0)) >= 2
        and runtime.get("contract_state") == "pass"
        and int(preflight.get("record_count", 0)) > 0
    )
    return {
        "generated_at": generated_at,
        "acceptance_state": "pass" if pass_state else "incomplete",
        "completed_slices": completed,
        "total_slices": total,
        "required_exports": required_exports,
        "present_exports": present,
        "missing_exports": sorted(set(required_exports) - set(present)),
        "portfolio_repo_count": portfolio.get("repo_count", 0),
        "runtime_contract_state": runtime.get("contract_state", "unknown"),
        "preflight_record_count": preflight.get("record_count", 0),
        "readiness_claim": (
            "initial v2 operational intelligence pack ready"
            if pass_state
            else "initial v2 operational intelligence pack not ready"
        ),
    }


def build_payloads(root: Path, out: Path, generated_at: str) -> dict[str, Any]:
    payloads = {
        "portfolio-summary": portfolio_payload(root, generated_at),
        "runtime-connector-contract": runtime_connector_payload(root, generated_at),
        "incident-correlations": incident_payload(root, generated_at),
        "closed-loop-remediation": remediation_payload(root, generated_at),
        "policy-preflight": policy_preflight_payload(root, generated_at),
        "trust-confidence": trust_confidence_payload(root, generated_at),
        "evidence-lineage": evidence_lineage_payload(root, generated_at),
        "connector-sdk": connector_sdk_payload(root, generated_at),
    }
    return payloads


def render_table(records: list[dict[str, Any]], fields: list[str], empty: str = "No records available.") -> list[str]:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    if not records:
        lines.append(f"| {empty} " + " | " * (len(fields) - 1) + "|")
        return lines
    for record in records[:50]:
        lines.append("| " + " | ".join(str(record.get(field, "")) for field in fields) + " |")
    return lines


def write_v2_markdown(out: Path, payloads: dict[str, Any], acceptance: dict[str, Any], generated_at: str) -> None:
    portfolio = payloads["portfolio-summary"]
    write_lines(
        out / "portfolio-summary.md",
        [
            "# V2 Portfolio Summary",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Portfolio: `{portfolio.get('portfolio_id')}`",
            f"Repositories: `{portfolio.get('repo_count')}`",
            f"Total scanned artifacts: `{portfolio.get('total_artifacts')}`",
            f"Repositories with blocked autonomy: `{len(portfolio.get('blocked_repo_ids', []))}`",
            "",
            *render_table(
                portfolio.get("records", []),
                ["repo_id", "role", "owner", "scan_observed", "artifact_count", "dirty_file_count"],
            ),
        ],
    )

    runtime = payloads["runtime-connector-contract"]
    write_lines(
        out / "runtime-connector-contract.md",
        [
            "# Runtime Connector Contract",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Contract state: `{runtime['contract_state']}`",
            f"Source boundary: `{runtime['source_boundary']}`",
            f"Records: `{runtime['record_count']}`",
            "",
            *render_table(runtime.get("records", []), ["event_id", "source", "signal_type", "environment", "confidence"]),
        ],
    )

    incidents = payloads["incident-correlations"]
    write_lines(
        out / "incident-correlation-summary.md",
        [
            "# Incident Correlation Summary",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Source boundary: `{incidents['source_boundary']}`",
            f"Matched incidents: `{incidents['matched_count']} / {incidents['record_count']}`",
            "",
            *render_table(incidents.get("records", []), ["incident_id", "severity", "service", "correlation_state"]),
        ],
    )

    remediation = payloads["closed-loop-remediation"]
    write_lines(
        out / "closed-loop-remediation-summary.md",
        [
            "# Closed-Loop Remediation Summary",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Records: `{remediation['record_count']}`",
            f"High-risk decisions without state: `{remediation['high_risk_unlinked_count']}`",
            "",
            *render_table(remediation.get("records", []), ["path", "state", "owner", "expires_at", "risk_level"]),
        ],
    )

    preflight = payloads["policy-preflight"]
    write_lines(
        out / "policy-preflight-summary.md",
        [
            "# Policy Preflight Summary",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Records: `{preflight['record_count']}`",
            "",
            *render_table(preflight.get("records", []), ["path", "risk_level", "decision", "reason"]),
        ],
    )

    confidence = payloads["trust-confidence"]
    write_lines(
        out / "trust-confidence-summary.md",
        [
            "# Trust And Confidence Summary",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Records: `{confidence['record_count']}`",
            f"Low-confidence high-risk decisions: `{confidence['low_confidence_high_risk_count']}`",
            "",
            *render_table(confidence.get("records", []), ["path", "risk_level", "confidence", "review_required"]),
        ],
    )

    lineage = payloads["evidence-lineage"]
    write_lines(
        out / "evidence-lineage-summary.md",
        [
            "# Evidence Lineage Summary",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Records: `{lineage['record_count']}`",
            f"Lineage gaps: `{lineage['lineage_gap_count']}`",
            "",
            *render_table(lineage.get("records", []), ["decision_id", "path", "risk_level"]),
        ],
    )

    sdk = payloads["connector-sdk"]
    write_lines(
        out / "connector-sdk-summary.md",
        [
            "# Connector SDK Summary",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"SDK version: `{sdk['sdk_version']}`",
            f"Dependency free: `{sdk['dependency_free']}`",
            f"Validation command: `{sdk['validation_command']}`",
            "",
            *render_table(sdk.get("connectors", []), ["connector_type", "input_contract", "required_behavior"]),
        ],
    )

    write_lines(
        out / "v2-acceptance-pack.md",
        [
            "# V2 Acceptance Pack",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Acceptance state: `{acceptance['acceptance_state']}`",
            f"Completed slices: `{acceptance['completed_slices']} / {acceptance['total_slices']}`",
            f"Portfolio repositories: `{acceptance['portfolio_repo_count']}`",
            f"Runtime contract state: `{acceptance['runtime_contract_state']}`",
            f"Preflight records: `{acceptance['preflight_record_count']}`",
            f"Readiness claim: `{acceptance['readiness_claim']}`",
        ],
    )

    write_lines(
        out / "README.md",
        [
            "# V2 Operational Intelligence Reports",
            "",
            f"Generated: `{generated_at}`",
            "",
            "These reports are generated materialized views. They support decisions and reviews; they are not the source of truth.",
            "",
            "## Start Here",
            "",
            "- `portfolio-summary.md`",
            "- `policy-preflight-summary.md`",
            "- `v2-acceptance-pack.md`",
            "",
            "## Machine Outputs",
            "",
            "- `exports/portfolio-summary.json`",
            "- `exports/runtime-connector-contract.json`",
            "- `exports/incident-correlations.json`",
            "- `exports/closed-loop-remediation.json`",
            "- `exports/policy-preflight.json`",
            "- `exports/trust-confidence.json`",
            "- `exports/evidence-lineage.json`",
            "- `exports/connector-sdk.json`",
            "- `exports/v2-acceptance-pack.json`",
        ],
    )


def write_portfolio_operator_view(out: Path, payloads: dict[str, Any], acceptance: dict[str, Any], generated_at: str) -> None:
    portfolio = payloads["portfolio-summary"]
    preflight = payloads["policy-preflight"]
    confidence = payloads["trust-confidence"]
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>EDI V2 Portfolio Operator View</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; color: #172026; background: #f4f7f9; }}
    header {{ background: #17324d; color: white; padding: 22px 30px; }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 24px 30px 40px; }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 12px; }}
    .metric, section {{ background: white; border: 1px solid #d7e0e7; border-radius: 6px; padding: 16px; }}
    .metric strong {{ display: block; font-size: 26px; margin-top: 6px; }}
    section {{ margin-top: 16px; }}
  </style>
</head>
<body>
  <header>
    <h1>Engineering Decision Intelligence V2</h1>
    <p>Generated: {generated_at}</p>
  </header>
  <main>
    <div class="metrics">
      <div class="metric">V2 acceptance<strong>{acceptance['acceptance_state']}</strong></div>
      <div class="metric">Repositories<strong>{portfolio['repo_count']}</strong></div>
      <div class="metric">Scanned artifacts<strong>{portfolio['total_artifacts']}</strong></div>
      <div class="metric">Preflight decisions<strong>{preflight['record_count']}</strong></div>
      <div class="metric">Low-confidence high-risk<strong>{confidence['low_confidence_high_risk_count']}</strong></div>
    </div>
    <section>
      <h2>Operational Intelligence Boundary</h2>
      <p>Portfolio views, connector fixtures, incident correlations, policy preflight, confidence scores, and evidence lineage are generated from declared inputs and existing scanner reports.</p>
    </section>
  </main>
</body>
</html>
"""
    (out / "portfolio-operator-view.html").write_text(html, encoding="utf-8")


def build_v2_outputs(root: Path, out: Path | None = None, generated_at: str | None = None) -> dict[str, Any]:
    generated = generated_timestamp(generated_at)
    target = out or root / "reports" / "product" / "v2"
    payloads = build_payloads(root, target, generated)
    export_dir = target / "exports"
    for name, payload in payloads.items():
        write_json(export_dir / f"{name}.json", payload)
    acceptance = v2_acceptance_payload(root, target, generated)
    write_json(export_dir / "v2-acceptance-pack.json", acceptance)
    write_v2_markdown(target, payloads, acceptance, generated)
    write_portfolio_operator_view(target, payloads, acceptance, generated)
    return {"payloads": payloads, "acceptance": acceptance}


def check_v2_outputs(root: Path, out: Path | None = None) -> bool:
    target = out or root / "reports" / "product" / "v2"
    with tempfile.TemporaryDirectory() as tmp:
        temp_out = Path(tmp) / "v2"
        generated_at = load_json(target / "exports" / "v2-acceptance-pack.json").get("generated_at")
        build_v2_outputs(root, temp_out, generated_at)
        for filename in V2_REPORT_FILES:
            current = (target / filename).read_text(encoding="utf-8")
            expected = (temp_out / filename).read_text(encoding="utf-8")
            if current != expected:
                raise SystemExit(f"V2 report drift detected: {filename}")
    return True
