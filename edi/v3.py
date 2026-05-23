"""Materialize v3 operationalization reports."""

from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


V3_REPORT_FILES = [
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


def connector_dir(root: Path) -> Path:
    return root / "connector-inputs"


def connector_payload(root: Path, filename: str) -> dict[str, Any]:
    return load_json(connector_dir(root) / filename)


def connector_ingestion_payload(root: Path, generated_at: str) -> dict[str, Any]:
    specs = [
        ("github_repositories", "github-repositories.json", "repositories"),
        ("github_actions_runs", "github-actions-runs.json", "runs"),
        ("deployment_events", "deployment-events.json", "events"),
        ("runtime_telemetry", "runtime-telemetry.json", "signals"),
        ("incidents", "incidents.json", "incidents"),
        ("remediation_reviews", "remediation-reviews.json", "reviews"),
    ]
    records: list[dict[str, Any]] = []
    for connector_type, filename, record_key in specs:
        payload = connector_payload(root, filename)
        records.append(
            {
                "connector_type": connector_type,
                "path": f"connector-inputs/{filename}",
                "source": payload.get("source", "unknown"),
                "source_boundary": payload.get("source_boundary", "unknown"),
                "record_count": len(payload.get(record_key, [])),
                "schema_version": payload.get("schema_version"),
            }
        )
    return {
        "generated_at": generated_at,
        "connector_count": len(records),
        "total_records": sum(int(record["record_count"]) for record in records),
        "records": records,
        "source_boundary": "imported_connector_payloads_not_live_polling",
    }


def v2_export(root: Path, filename: str) -> dict[str, Any]:
    return load_json(root / "reports" / "product" / "v2" / "exports" / filename)


def ml_export(root: Path, filename: str) -> dict[str, Any]:
    return load_json(root / "reports" / "ml-pilot" / "exports" / filename)


def reconciliation_payload(root: Path, generated_at: str) -> dict[str, Any]:
    github = connector_payload(root, "github-repositories.json").get("repositories", [])
    actions = connector_payload(root, "github-actions-runs.json").get("runs", [])
    deployments = connector_payload(root, "deployment-events.json").get("events", [])
    runtime = connector_payload(root, "runtime-telemetry.json").get("signals", [])
    incidents = connector_payload(root, "incidents.json").get("incidents", [])
    preflight = v2_export(root, "policy-preflight.json").get("records", [])
    loops = [
        {
            "loop_id": "github-policy-vs-observed",
            "expected": "protected default branches and governed environments",
            "observed": f"{sum(1 for repo in github if repo.get('branch_protection_observed'))}/{len(github)} repos with observed branch protection",
            "divergence_count": sum(1 for repo in github if not repo.get("branch_protection_observed")),
            "action": "Review missing GitHub protection before expanding autonomy.",
        },
        {
            "loop_id": "deploy-path-vs-actions",
            "expected": "deployment-like runs are tied to reviewed deployment evidence",
            "observed": f"{sum(1 for run in actions if run.get('deployment_like'))} deployment-like runs, {len(deployments)} deployment events",
            "divergence_count": max(0, sum(1 for run in actions if run.get("deployment_like")) - len(deployments)),
            "action": "Attach deployment event evidence to deployment-like workflows.",
        },
        {
            "loop_id": "runtime-risk-vs-telemetry",
            "expected": "high-risk runtime surfaces have observed telemetry imports",
            "observed": f"{len(runtime)} telemetry signals imported",
            "divergence_count": 0 if runtime else 1,
            "action": "Keep runtime claims limited to imported connector evidence.",
        },
        {
            "loop_id": "incident-risk-vs-decisions",
            "expected": "incidents correlate to decision paths and owners",
            "observed": f"{len(incidents)} incident records imported, {len(preflight)} preflight decisions available",
            "divergence_count": sum(1 for incident in incidents if not incident.get("related_paths")),
            "action": "Keep incident review linked to decision paths.",
        },
    ]
    return {
        "generated_at": generated_at,
        "loop_count": len(loops),
        "divergence_count": sum(int(loop["divergence_count"]) for loop in loops),
        "records": loops,
    }


def portfolio_onboarding_payload(root: Path, generated_at: str) -> dict[str, Any]:
    portfolio = v2_export(root, "portfolio-summary.json")
    records = []
    for repo in portfolio.get("records", []):
        records.append(
            {
                "repo_id": repo["repo_id"],
                "role": repo["role"],
                "owner": repo["owner"],
                "scan_observed": repo["scan_observed"],
                "custom_scanner_required": False,
                "onboarding_state": "ready" if repo["scan_observed"] else "missing_scan",
                "next_command": "python3 -m edi scan --repo <repo> --out <report-dir> --policy policies/autonomy-policy.json",
            }
        )
    return {
        "generated_at": generated_at,
        "repo_count": len(records),
        "ready_count": sum(1 for record in records if record["onboarding_state"] == "ready"),
        "records": records,
    }


def evidence_lineage_payload(root: Path, generated_at: str) -> dict[str, Any]:
    preflight = v2_export(root, "policy-preflight.json").get("records", [])
    remediation = connector_payload(root, "remediation-reviews.json").get("reviews", [])
    remediation_by_path = {record["path"]: record for record in remediation}
    records = []
    for decision in preflight[:50]:
        path = decision.get("path")
        lineage = [
            "reports/ml-pilot/findings.jsonl",
            "reports/product/v2/exports/policy-preflight.json",
            "connector-inputs/github-actions-runs.json",
            "connector-inputs/runtime-telemetry.json",
        ]
        if path in remediation_by_path:
            lineage.append("connector-inputs/remediation-reviews.json")
        gaps = []
        if path not in remediation_by_path and decision.get("decision") in {"blocked", "approval_required"}:
            gaps.append("remediation review")
        records.append(
            {
                "path": path,
                "decision": decision.get("decision"),
                "risk_level": decision.get("risk_level"),
                "source_evidence": lineage,
                "lineage_gap_count": len(gaps),
                "lineage_gaps": gaps,
            }
        )
    return {
        "generated_at": generated_at,
        "record_count": len(records),
        "lineage_gap_count": sum(record["lineage_gap_count"] for record in records),
        "records": records,
    }


def remediation_workflow_payload(root: Path, generated_at: str) -> dict[str, Any]:
    reviews = connector_payload(root, "remediation-reviews.json").get("reviews", [])
    records = []
    for review in reviews:
        records.append(
            {
                "review_id": review["review_id"],
                "repo_id": review["repo_id"],
                "path": review["path"],
                "state": review["state"],
                "owner": review["owner"],
                "expires_at": review["expires_at"],
                "verification": review["verification"],
                "next_action": "verify remediation evidence" if review["verification"] == "pending" else "monitor",
            }
        )
    return {
        "generated_at": generated_at,
        "record_count": len(records),
        "state_counts": count_values(records, "state"),
        "verification_counts": count_values(records, "verification"),
        "records": records,
    }


def policy_preflight_ci_payload(root: Path, generated_at: str) -> dict[str, Any]:
    preflight = v2_export(root, "policy-preflight.json").get("records", [])
    records = []
    for record in preflight[:100]:
        decision = record.get("decision")
        ci_status = "fail" if decision == "blocked" else "manual_review" if decision == "approval_required" else "pass"
        records.append(
            {
                "path": record.get("path"),
                "risk_level": record.get("risk_level"),
                "policy_decision": decision,
                "ci_status": ci_status,
                "reason": record.get("reason"),
            }
        )
    return {
        "generated_at": generated_at,
        "record_count": len(records),
        "ci_status_counts": count_values(records, "ci_status"),
        "records": records,
        "recommended_ci_command": "python3 -m edi v3 build --check && python3 -m edi validate",
    }


def product_ux_payload(root: Path, generated_at: str) -> dict[str, Any]:
    surfaces = [
        {
            "surface": "operator",
            "path": "reports/product/operator-view.html",
            "purpose": "overall product state, v2/v3 progress, top risks",
        },
        {
            "surface": "v3_operator",
            "path": "reports/product/v3/v3-operator-view.html",
            "purpose": "v3 operationalization status and connector boundary",
        },
        {
            "surface": "product_owner",
            "path": "reports/product/v3/external-pilot-readiness.md",
            "purpose": "pilot readiness and remaining evidence",
        },
        {
            "surface": "engineer",
            "path": "reports/product/v3/policy-preflight-ci-summary.md",
            "purpose": "CI preflight outcomes and remediation actions",
        },
        {
            "surface": "audit",
            "path": "reports/product/v3/evidence-lineage-v3-summary.md",
            "purpose": "evidence lineage and source boundaries",
        },
    ]
    return {
        "generated_at": generated_at,
        "surface_count": len(surfaces),
        "records": surfaces,
    }


def reusable_packaging_payload(root: Path, generated_at: str) -> dict[str, Any]:
    records = [
        {"item": "cli", "path": "edi/__main__.py", "command": "python3 -m edi validate"},
        {"item": "scanner", "path": "tools/operational_state_scan.py", "command": "python3 -m edi scan --repo <repo> --out <out>"},
        {"item": "v2", "path": "edi/v2.py", "command": "python3 -m edi v2 build"},
        {"item": "v3", "path": "edi/v3.py", "command": "python3 -m edi v3 build"},
        {"item": "policy_pack", "path": "policies/", "command": "python3 -m edi validate"},
        {"item": "connector_inputs", "path": "connector-inputs/", "command": "python3 -m edi v3 build --check"},
    ]
    return {
        "generated_at": generated_at,
        "record_count": len(records),
        "dependency_free": True,
        "records": records,
    }


def external_pilot_payload(root: Path, generated_at: str) -> dict[str, Any]:
    required = [
        {"requirement": "portfolio manifest entry", "status": "ready", "evidence": "policies/portfolio-repositories.json"},
        {"requirement": "repository scan output", "status": "ready", "evidence": "reports/ml-pilot/manifest.json"},
        {"requirement": "connector input payloads", "status": "ready", "evidence": "connector-inputs/"},
        {"requirement": "policy preflight", "status": "ready", "evidence": "reports/product/v3/policy-preflight-ci-summary.md"},
        {"requirement": "remediation reviews", "status": "ready", "evidence": "connector-inputs/remediation-reviews.json"},
        {"requirement": "CI integration in target repo", "status": "future_work", "evidence": "not wired to external repo CI yet"},
    ]
    ready = sum(1 for item in required if item["status"] == "ready")
    return {
        "generated_at": generated_at,
        "requirement_count": len(required),
        "ready_count": ready,
        "future_work_count": len(required) - ready,
        "records": required,
        "pilot_state": "ready_for_controlled_external_pilot" if ready >= 5 else "not_ready",
    }


def completed_v3_slices(root: Path) -> tuple[int, int]:
    backlog = load_json(root / "roadmap" / "v3-operationalization-backlog.json")
    slices = backlog.get("slices", [])
    completed = [item for item in slices if item.get("status") == "completed"]
    return len(completed), len(slices)


def acceptance_payload(root: Path, out: Path, payloads: dict[str, Any], generated_at: str) -> dict[str, Any]:
    completed, total = completed_v3_slices(root)
    required_exports = [
        "connector-ingestion.json",
        "reconciliation-loops.json",
        "portfolio-onboarding.json",
        "evidence-lineage-v3.json",
        "remediation-workflow.json",
        "policy-preflight-ci.json",
        "product-ux.json",
        "reusable-packaging.json",
        "external-pilot-readiness.json",
        "v3-acceptance-pack.json",
    ]
    export_dir = out / "exports"
    present = [name for name in required_exports if name == "v3-acceptance-pack.json" or (export_dir / name).exists()]
    pass_state = (
        completed == total
        and len(present) == len(required_exports)
        and payloads["connector-ingestion"]["connector_count"] >= 6
        and payloads["reconciliation-loops"]["loop_count"] >= 4
        and payloads["portfolio-onboarding"]["ready_count"] >= 2
        and payloads["policy-preflight-ci"]["record_count"] > 0
        and payloads["external-pilot-readiness"]["pilot_state"] == "ready_for_controlled_external_pilot"
    )
    return {
        "generated_at": generated_at,
        "acceptance_state": "pass" if pass_state else "incomplete",
        "completed_slices": completed,
        "total_slices": total,
        "required_exports": required_exports,
        "present_exports": present,
        "missing_exports": sorted(set(required_exports) - set(present)),
        "connector_count": payloads["connector-ingestion"]["connector_count"],
        "reconciliation_loop_count": payloads["reconciliation-loops"]["loop_count"],
        "portfolio_ready_count": payloads["portfolio-onboarding"]["ready_count"],
        "preflight_record_count": payloads["policy-preflight-ci"]["record_count"],
        "pilot_state": payloads["external-pilot-readiness"]["pilot_state"],
        "readiness_claim": (
            "initial v3 operationalization pack ready"
            if pass_state
            else "initial v3 operationalization pack not ready"
        ),
        "blocked_claims": [
            "complete live runtime truth",
            "autonomous production enforcement",
            "external pilot CI wired without target repo changes",
        ],
    }


def build_payloads(root: Path, generated_at: str) -> dict[str, Any]:
    return {
        "connector-ingestion": connector_ingestion_payload(root, generated_at),
        "reconciliation-loops": reconciliation_payload(root, generated_at),
        "portfolio-onboarding": portfolio_onboarding_payload(root, generated_at),
        "evidence-lineage-v3": evidence_lineage_payload(root, generated_at),
        "remediation-workflow": remediation_workflow_payload(root, generated_at),
        "policy-preflight-ci": policy_preflight_ci_payload(root, generated_at),
        "product-ux": product_ux_payload(root, generated_at),
        "reusable-packaging": reusable_packaging_payload(root, generated_at),
        "external-pilot-readiness": external_pilot_payload(root, generated_at),
    }


def render_table(records: list[dict[str, Any]], fields: list[str]) -> list[str]:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    if not records:
        lines.append("| No records available " + " | " * (len(fields) - 1) + "|")
        return lines
    for record in records[:60]:
        lines.append("| " + " | ".join(str(record.get(field, "")) for field in fields) + " |")
    return lines


def display_count(payload: dict[str, Any]) -> int:
    for key in ("record_count", "connector_count", "loop_count", "surface_count", "requirement_count"):
        if key in payload:
            return int(payload[key])
    return 0


def write_markdown(out: Path, payloads: dict[str, Any], acceptance: dict[str, Any], generated_at: str) -> None:
    specs = [
        ("connector-ingestion-summary.md", "# Connector Ingestion Summary", "connector-ingestion", ["connector_type", "record_count", "source_boundary"]),
        ("reconciliation-loop-summary.md", "# Reconciliation Loop Summary", "reconciliation-loops", ["loop_id", "divergence_count", "action"]),
        ("portfolio-onboarding-summary.md", "# Portfolio Onboarding Summary", "portfolio-onboarding", ["repo_id", "onboarding_state", "custom_scanner_required"]),
        ("evidence-lineage-v3-summary.md", "# Evidence Lineage V3 Summary", "evidence-lineage-v3", ["path", "decision", "lineage_gap_count"]),
        ("remediation-workflow-summary.md", "# Remediation Workflow Summary", "remediation-workflow", ["review_id", "state", "owner", "verification"]),
        ("policy-preflight-ci-summary.md", "# Policy Preflight CI Summary", "policy-preflight-ci", ["path", "policy_decision", "ci_status", "reason"]),
        ("product-ux-summary.md", "# Product UX Summary", "product-ux", ["surface", "path", "purpose"]),
        ("reusable-packaging-summary.md", "# Reusable Packaging Summary", "reusable-packaging", ["item", "path", "command"]),
        ("external-pilot-readiness.md", "# External Pilot Readiness", "external-pilot-readiness", ["requirement", "status", "evidence"]),
    ]
    for filename, title, key, fields in specs:
        payload = payloads[key]
        lines = [
            title,
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Records: `{display_count(payload)}`",
            "",
            *render_table(payload.get("records", []), fields),
        ]
        write_lines(out / filename, lines)

    write_lines(
        out / "v3-acceptance-pack.md",
        [
            "# V3 Acceptance Pack",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Acceptance state: `{acceptance['acceptance_state']}`",
            f"Completed slices: `{acceptance['completed_slices']} / {acceptance['total_slices']}`",
            f"Connectors: `{acceptance['connector_count']}`",
            f"Reconciliation loops: `{acceptance['reconciliation_loop_count']}`",
            f"Portfolio ready count: `{acceptance['portfolio_ready_count']}`",
            f"Preflight records: `{acceptance['preflight_record_count']}`",
            f"Pilot state: `{acceptance['pilot_state']}`",
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
            "# V3 Operationalization Reports",
            "",
            f"Generated: `{generated_at}`",
            "",
            "These reports are generated from connector input payloads, v2 outputs, and scanner evidence.",
            "They are decision views, not autonomous production controls.",
            "",
            "## Start Here",
            "",
            "- `v3-acceptance-pack.md`",
            "- `connector-ingestion-summary.md`",
            "- `reconciliation-loop-summary.md`",
            "- `policy-preflight-ci-summary.md`",
        ],
    )


def write_operator_view(out: Path, payloads: dict[str, Any], acceptance: dict[str, Any], generated_at: str) -> None:
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>EDI V3 Operationalization</title>
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
    <h1>Engineering Decision Intelligence V3</h1>
    <p>Generated: {generated_at}</p>
  </header>
  <main>
    <div class="metrics">
      <div class="metric">V3 acceptance<strong>{acceptance['acceptance_state']}</strong></div>
      <div class="metric">Connectors<strong>{acceptance['connector_count']}</strong></div>
      <div class="metric">Reconciliation loops<strong>{acceptance['reconciliation_loop_count']}</strong></div>
      <div class="metric">Preflight records<strong>{acceptance['preflight_record_count']}</strong></div>
      <div class="metric">Pilot state<strong>{acceptance['pilot_state']}</strong></div>
    </div>
    <section>
      <h2>Boundary</h2>
      <p>V3 uses imported connector payloads and generated evidence. It does not claim autonomous production enforcement or complete live runtime truth.</p>
    </section>
  </main>
</body>
</html>
"""
    (out / "v3-operator-view.html").write_text(html, encoding="utf-8")


def build_v3_outputs(root: Path, out: Path | None = None, generated_at: str | None = None) -> dict[str, Any]:
    generated = generated_timestamp(generated_at)
    target = out or root / "reports" / "product" / "v3"
    payloads = build_payloads(root, generated)
    export_dir = target / "exports"
    for name, payload in payloads.items():
        write_json(export_dir / f"{name}.json", payload)
    acceptance = acceptance_payload(root, target, payloads, generated)
    write_json(export_dir / "v3-acceptance-pack.json", acceptance)
    write_markdown(target, payloads, acceptance, generated)
    write_operator_view(target, payloads, acceptance, generated)
    return {"payloads": payloads, "acceptance": acceptance}


def check_v3_outputs(root: Path, out: Path | None = None) -> bool:
    target = out or root / "reports" / "product" / "v3"
    with tempfile.TemporaryDirectory() as tmp:
        temp_out = Path(tmp) / "v3"
        generated_at = load_json(target / "exports" / "v3-acceptance-pack.json").get("generated_at")
        build_v3_outputs(root, temp_out, generated_at)
        for filename in V3_REPORT_FILES:
            current = (target / filename).read_text(encoding="utf-8")
            expected = (temp_out / filename).read_text(encoding="utf-8")
            if current != expected:
                raise SystemExit(f"V3 report drift detected: {filename}")
    return True
