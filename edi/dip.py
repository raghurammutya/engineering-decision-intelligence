"""Materialize Decision Intelligence Platform governance readiness reports."""

from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from edi.dip_contracts import validate_contract_artifacts
from edi.dip_trust_loop import trust_loop_payload


DIP_REPORT_FILES = [
    "README.md",
    "governance-policy.md",
    "wedge-readiness.md",
    "implementation-backlog.md",
    "implementation-evidence.md",
    "autopilot-lanes.md",
    "dip-acceptance-pack.md",
    "exports/governance-policy.json",
    "exports/wedge-readiness.json",
    "exports/implementation-backlog.json",
    "exports/implementation-evidence.json",
    "exports/autopilot-lanes.json",
    "exports/dip-acceptance-pack.json",
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


def dip_config(root: Path) -> dict[str, Any]:
    return load_json(root / "runtime-config" / "dip-readiness.json")


def dip_backlog(root: Path) -> dict[str, Any]:
    return load_json(root / "roadmap" / "dip-governed-decision-review-backlog.json")


def governance_policy_payload(config: dict[str, Any], generated_at: str) -> dict[str, Any]:
    return {
        "generated_at": generated_at,
        "target_id": config.get("target_id"),
        "target_name": config.get("target_name"),
        "first_wedge": config.get("first_wedge"),
        "relationship_to_edi": config.get("relationship_to_edi"),
        "source_boundary": config.get("source_boundary"),
        "fail_closed": bool(config.get("fail_closed", True)),
        "principle_count": len(config.get("governance_principles", [])),
        "source_label_count": len(config.get("source_labels", [])),
        "wedge_step_count": len(config.get("wedge_loop", [])),
        "governance_principles": config.get("governance_principles", []),
        "source_labels": config.get("source_labels", []),
        "wedge_loop": config.get("wedge_loop", []),
        "runtime_authority": config.get("runtime_authority", {}),
    }


def wedge_readiness_payload(config: dict[str, Any], generated_at: str) -> dict[str, Any]:
    validation = validate_contract_artifacts(Path("."))
    valid_contracts = {record["slice_id"] for record in validation["records"] if record["passed"]}
    implemented_domain_to_slice = {
        "decision_spec": "decision-spec-contract-v1",
        "capability_registry": "capability-registry-contract-v1",
        "policy_preflight": "policy-preflight-contract-v1",
        "simulation": "simulation-evidence-contract-v1",
        "approval_case_store": "case-evidence-pack-v1",
        "replay": "replay-reader-v1",
        "marketplace_governance": "marketplace-governance-contract-v1",
        "shared_context_governance": "shared-context-governance-contract-v1",
    }
    records = []
    for domain in config.get("readiness_domains", []):
        required = domain.get("required_evidence", [])
        slice_id = implemented_domain_to_slice.get(str(domain.get("id", "")), "")
        implemented = bool(slice_id and slice_id in valid_contracts)
        records.append(
            {
                "id": domain.get("id", ""),
                "label": domain.get("label", domain.get("id", "")),
                "required_evidence_count": len(required),
                "required_evidence": required,
                "policy_declared": bool(required),
                "implementation_observed": implemented,
                "state": "contract_artifacts_validated" if implemented else "policy_declared_runtime_evidence_missing",
            }
        )
    domain_count = len(records)
    policy_declared_count = len([record for record in records if record["policy_declared"]])
    implementation_count = len([record for record in records if record["implementation_observed"]])
    return {
        "generated_at": generated_at,
        "target_id": config.get("target_id"),
        "first_wedge": config.get("first_wedge"),
        "source_boundary": config.get("source_boundary"),
        "fail_closed": bool(config.get("fail_closed", True)),
        "domain_count": domain_count,
        "policy_declared_count": policy_declared_count,
        "implementation_observed_count": implementation_count,
        "policy_readiness_percent": round(policy_declared_count / domain_count * 100, 1) if domain_count else 0.0,
        "implementation_evidence_percent": round(implementation_count / domain_count * 100, 1) if domain_count else 0.0,
        "records": records,
    }


def implementation_backlog_payload(root: Path, generated_at: str) -> dict[str, Any]:
    backlog = dip_backlog(root)
    slices = backlog.get("slices", [])
    validation = validate_contract_artifacts(root)
    valid_contracts = {record["slice_id"] for record in validation["records"] if record["passed"]}
    defined_records = [
        item
        for item in slices
        if item.get("id")
        and item.get("purpose")
        and isinstance(item.get("expected_outputs"), list)
        and item.get("expected_outputs")
        and isinstance(item.get("acceptance"), list)
        and item.get("acceptance")
        and item.get("allowed_autonomy")
        and item.get("parallelization_group")
    ]
    runtime_mutating = [
        item
        for item in slices
        if item.get("allowed_autonomy") in {"runtime_execute", "production_execute", "autonomous_execute"}
    ]
    groups = sorted({str(item.get("parallelization_group")) for item in slices if item.get("parallelization_group")})
    dependency_edges = sum(len(item.get("depends_on", [])) for item in slices)
    return {
        "generated_at": generated_at,
        "target_id": backlog.get("target_id"),
        "milestone": backlog.get("milestone"),
        "first_wedge": backlog.get("first_wedge"),
        "source_boundary": backlog.get("source_boundary"),
        "runtime_execution_allowed": bool(backlog.get("runtime_execution_allowed", False)),
        "slice_count": len(slices),
        "defined_slice_count": len(defined_records),
        "defined_percent": round(len(defined_records) / len(slices) * 100, 1) if slices else 0.0,
        "completed_slice_count": len([item for item in slices if item.get("status") == "completed"]),
        "planned_slice_count": len([item for item in slices if item.get("status") == "planned"]),
        "validated_contract_slice_count": len(valid_contracts),
        "runtime_mutating_slice_count": len(runtime_mutating),
        "parallelization_groups": groups,
        "dependency_edge_count": dependency_edges,
        "records": slices,
    }


def implementation_evidence_payload(config: dict[str, Any], generated_at: str) -> dict[str, Any]:
    blocked = config.get("runtime_authority", {}).get("blocked_until_evidenced", [])
    validation = validate_contract_artifacts(Path("."))
    trust_loop = trust_loop_payload(Path("."))
    implementation_records = [
        {
            "slice_id": record["slice_id"],
            "state": "completed" if record["passed"] else "missing_or_invalid",
            "contract_path": record["contract_path"],
            "example_path": record["example_path"],
            "errors": record["errors"],
        }
        for record in validation["records"]
    ]
    return {
        "generated_at": generated_at,
        "target_id": config.get("target_id"),
        "source_boundary": config.get("source_boundary"),
        "dip_runtime_managed_by_edi": False,
        "implementation_started": bool(implementation_records),
        "runtime_integration_deferred": True,
        "production_runtime_authority_granted": False,
        "contract_artifact_count": validation["contract_count"],
        "valid_contract_artifact_count": validation["passed_contract_count"],
        "all_contract_artifacts_valid": validation["all_contracts_valid"],
        "trust_loop_complete": trust_loop["trust_loop_complete"],
        "runtime_execution_requested": trust_loop["runtime_execution_requested"],
        "blocked_runtime_claim_count": len(blocked),
        "blocked_runtime_claims": blocked,
        "implementation_records": implementation_records,
    }


def autopilot_lanes_payload(config: dict[str, Any], generated_at: str) -> dict[str, Any]:
    lanes = config.get("autopilot_lanes", [])
    return {
        "generated_at": generated_at,
        "target_id": config.get("target_id"),
        "lane_count": len(lanes),
        "controlled_execute_allowed": any(lane.get("mode") == "controlled_execute" and lane.get("allowed") for lane in lanes),
        "runtime_mutation_blocked": any(lane.get("mode") == "blocked" and lane.get("blocked") for lane in lanes),
        "records": lanes,
    }


def acceptance_payload(payloads: dict[str, Any], generated_at: str) -> dict[str, Any]:
    policy = payloads["governance-policy"]
    readiness = payloads["wedge-readiness"]
    backlog = payloads["implementation-backlog"]
    evidence = payloads["implementation-evidence"]
    autopilot = payloads["autopilot-lanes"]
    policy_ready = (
        policy["principle_count"] >= 7
        and policy["source_label_count"] >= 8
        and policy["wedge_step_count"] >= 10
        and readiness["domain_count"] >= 8
        and readiness["policy_readiness_percent"] == 100.0
        and backlog["slice_count"] >= 10
        and backlog["defined_percent"] == 100.0
        and backlog["runtime_execution_allowed"] is False
        and backlog["runtime_mutating_slice_count"] == 0
        and evidence["dip_runtime_managed_by_edi"] is False
        and evidence["runtime_integration_deferred"] is True
        and evidence["production_runtime_authority_granted"] is False
        and autopilot["runtime_mutation_blocked"] is True
    )
    return {
        "generated_at": generated_at,
        "acceptance_state": (
            "pre_runtime_trust_loop_complete_runtime_blocked"
            if policy_ready and readiness["implementation_evidence_percent"] == 100.0
            else "governance_pack_ready_implementation_evidence_incomplete"
            if policy_ready
            else "incomplete"
        ),
        "policy_readiness_percent": 100.0 if policy_ready else 0.0,
        "implementation_backlog_defined_percent": backlog["defined_percent"],
        "implementation_evidence_percent": readiness["implementation_evidence_percent"],
        "readiness_claim": "DIP governance and first-wedge readiness pack ready" if policy_ready else "DIP governance readiness pack incomplete",
        "blocked_claims": [
            "DIP runtime integration is authorized",
            "DIP production decision execution is authorized",
        ],
    }


def build_payloads(root: Path, generated_at: str) -> dict[str, Any]:
    config = dip_config(root)
    payloads = {
        "governance-policy": governance_policy_payload(config, generated_at),
        "wedge-readiness": wedge_readiness_payload(config, generated_at),
        "implementation-backlog": implementation_backlog_payload(root, generated_at),
        "implementation-evidence": implementation_evidence_payload(config, generated_at),
        "autopilot-lanes": autopilot_lanes_payload(config, generated_at),
    }
    payloads["dip-acceptance-pack"] = acceptance_payload(payloads, generated_at)
    return payloads


def render_table(records: list[dict[str, Any]], fields: list[str]) -> list[str]:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for record in records:
        lines.append("| " + " | ".join(str(record.get(field, "")) for field in fields) + " |")
    return lines


def write_markdown(out: Path, payloads: dict[str, Any], generated_at: str) -> None:
    policy = payloads["governance-policy"]
    readiness = payloads["wedge-readiness"]
    backlog = payloads["implementation-backlog"]
    evidence = payloads["implementation-evidence"]
    autopilot = payloads["autopilot-lanes"]
    acceptance = payloads["dip-acceptance-pack"]
    write_lines(
        out / "governance-policy.md",
        [
            "# DIP Governance Policy",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Target: `{policy['target_name']}`",
            f"First wedge: `{policy['first_wedge']}`",
            f"EDI relationship: `{policy['relationship_to_edi']}`",
            f"Source boundary: `{policy['source_boundary']}`",
            f"Fail closed: `{policy['fail_closed']}`",
            "",
            "## Governance Principles",
            "",
            *[f"- `{item}`" for item in policy["governance_principles"]],
            "",
            "## Source Labels",
            "",
            *[f"- `{item}`" for item in policy["source_labels"]],
        ],
    )
    write_lines(
        out / "wedge-readiness.md",
        [
            "# DIP First-Wedge Readiness",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Policy readiness: `{readiness['policy_readiness_percent']}%`",
            f"Implementation evidence: `{readiness['implementation_evidence_percent']}%`",
            "",
            *render_table(readiness["records"], ["id", "label", "required_evidence_count", "state"]),
        ],
    )
    write_lines(
        out / "implementation-backlog.md",
        [
            "# DIP Implementation Backlog",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Milestone: `{backlog['milestone']}`",
            f"Source boundary: `{backlog['source_boundary']}`",
            f"Runtime execution allowed: `{backlog['runtime_execution_allowed']}`",
            f"Backlog defined: `{backlog['defined_percent']}%`",
            f"Slices: `{backlog['defined_slice_count']} / {backlog['slice_count']}`",
            f"Parallelization groups: `{', '.join(backlog['parallelization_groups'])}`",
            "",
            *render_table(backlog["records"], ["id", "status", "allowed_autonomy", "parallelization_group", "depends_on"]),
        ],
    )
    write_lines(
        out / "implementation-evidence.md",
        [
            "# DIP Implementation Evidence",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"DIP runtime managed by EDI: `{evidence['dip_runtime_managed_by_edi']}`",
            f"Implementation started: `{evidence['implementation_started']}`",
            f"Runtime integration deferred: `{evidence['runtime_integration_deferred']}`",
            f"Production runtime authority granted: `{evidence['production_runtime_authority_granted']}`",
            f"Valid contract artifacts: `{evidence['valid_contract_artifact_count']} / {evidence['contract_artifact_count']}`",
            f"Trust loop complete: `{evidence['trust_loop_complete']}`",
            f"Runtime execution requested: `{evidence['runtime_execution_requested']}`",
            "",
            *render_table(evidence["implementation_records"], ["slice_id", "state", "contract_path", "example_path"]),
            "",
            "## Blocked Runtime Claims",
            "",
            *[f"- `{claim}`" for claim in evidence["blocked_runtime_claims"]],
        ],
    )
    write_lines(
        out / "autopilot-lanes.md",
        [
            "# DIP Autopilot Lanes",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Controlled execute allowed: `{autopilot['controlled_execute_allowed']}`",
            f"Runtime mutation blocked: `{autopilot['runtime_mutation_blocked']}`",
            "",
            *render_table(autopilot["records"], ["mode", "allowed", "blocked"]),
        ],
    )
    write_lines(
        out / "dip-acceptance-pack.md",
        [
            "# DIP Acceptance Pack",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Acceptance state: `{acceptance['acceptance_state']}`",
            f"Policy readiness: `{acceptance['policy_readiness_percent']}%`",
            f"Implementation backlog defined: `{acceptance['implementation_backlog_defined_percent']}%`",
            f"Implementation evidence: `{acceptance['implementation_evidence_percent']}%`",
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
            "# Decision Intelligence Platform Readiness",
            "",
            f"Generated: `{generated_at}`",
            "",
            "This pack uses EDI to govern DIP construction without making EDI the DIP runtime.",
            "The first wedge is governed decision review and simulation, and runtime execution claims remain blocked until evidenced.",
        ],
    )


def build_dip_outputs(root: Path, out: Path | None = None, generated_at: str | None = None) -> dict[str, Any]:
    generated = generated_timestamp(generated_at)
    target = out or root / "reports" / "product" / "dip"
    payloads = build_payloads(root, generated)
    export_dir = target / "exports"
    for name, payload in payloads.items():
        write_json(export_dir / f"{name}.json", payload)
    write_markdown(target, payloads, generated)
    return {"payloads": payloads, "acceptance": payloads["dip-acceptance-pack"]}


def check_dip_outputs(root: Path, out: Path | None = None) -> bool:
    target = out or root / "reports" / "product" / "dip"
    with tempfile.TemporaryDirectory() as tmp:
        temp_out = Path(tmp) / "dip"
        generated_at = load_json(target / "exports" / "dip-acceptance-pack.json").get("generated_at")
        build_dip_outputs(root, temp_out, generated_at)
        for filename in DIP_REPORT_FILES:
            current = (target / filename).read_text(encoding="utf-8")
            expected = (temp_out / filename).read_text(encoding="utf-8")
            if current != expected:
                raise SystemExit(f"DIP report drift detected: {filename}")
    return True
