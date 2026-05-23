"""Materialize a stable product API snapshot from generated reports."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_json_or_empty(path: Path) -> Any:
    if not path.exists():
        return {}
    return load_json(path)


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
    agent_capabilities = load_json(ml_exports / "ai-agent-capabilities.json")
    agent_drift = load_json(ml_exports / "agent-drift-evals.json")
    scanner_tuning = load_json(ml_exports / "scanner-tuning-pack.json")
    review_state = load_json(ml_exports / "review-state.json")
    review_workflows = load_json(ml_exports / "review-workflows.json")
    pr_events = load_json(ml_exports / "github-pr-events.json")
    action_runs = load_json(ml_exports / "github-actions-runs.json")
    deployment_evidence = load_json(ml_exports / "deployment-event-evidence.json")
    v1_5_acceptance = load_json(ml_exports / "v1.5-acceptance-pack.json")
    v2_exports = product_dir / "v2" / "exports"
    v2_portfolio = load_json_or_empty(v2_exports / "portfolio-summary.json")
    v2_preflight = load_json_or_empty(v2_exports / "policy-preflight.json")
    v2_confidence = load_json_or_empty(v2_exports / "trust-confidence.json")
    v2_lineage = load_json_or_empty(v2_exports / "evidence-lineage.json")
    v2_acceptance = load_json_or_empty(v2_exports / "v2-acceptance-pack.json")
    v3_exports = product_dir / "v3" / "exports"
    v3_connectors = load_json_or_empty(v3_exports / "connector-ingestion.json")
    v3_reconciliation = load_json_or_empty(v3_exports / "reconciliation-loops.json")
    v3_preflight = load_json_or_empty(v3_exports / "policy-preflight-ci.json")
    v3_pilot = load_json_or_empty(v3_exports / "external-pilot-readiness.json")
    v3_acceptance = load_json_or_empty(v3_exports / "v3-acceptance-pack.json")
    v4_exports = product_dir / "v4" / "exports"
    v4_connectors = load_json_or_empty(v4_exports / "live-connector-readiness.json")
    v4_reconciliation = load_json_or_empty(v4_exports / "continuous-reconciliation.json")
    v4_ci = load_json_or_empty(v4_exports / "ci-pr-enforcement.json")
    v4_slos = load_json_or_empty(v4_exports / "operational-slos.json")
    v4_acceptance = load_json_or_empty(v4_exports / "v4-acceptance-pack.json")
    v5_exports = product_dir / "v5" / "exports"
    v5_acceptance = load_json_or_empty(v5_exports / "v5-acceptance-pack.json")
    substrate_exports = product_dir / "substrate" / "exports"
    substrate_acceptance = load_json_or_empty(substrate_exports / "substrate-acceptance-pack.json")
    substrate_lifecycle = load_json_or_empty(substrate_exports / "lifecycle-policy.json")
    dip_exports = product_dir / "dip" / "exports"
    dip_acceptance = load_json_or_empty(dip_exports / "dip-acceptance-pack.json")
    dip_policy = load_json_or_empty(dip_exports / "governance-policy.json")
    dip_target_evidence = load_json_or_empty(dip_exports / "target-evidence.json")

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
        "ai_agents": {
            "capability_count": agent_capabilities.get("record_count", 0),
            "capability_level_counts": agent_capabilities.get("capability_level_counts", {}),
            "safety_status_counts": agent_capabilities.get("safety_status_counts", {}),
            "drift_record_count": agent_drift.get("record_count", 0),
            "drift_status_counts": agent_drift.get("drift_status_counts", {}),
        },
        "scanner_tuning": {
            "candidate_count": scanner_tuning.get("record_count", 0),
            "action_counts": scanner_tuning.get("action_counts", {}),
            "review_status_counts": scanner_tuning.get("review_status_counts", {}),
        },
        "operationalization": {
            "review_state_count": review_state.get("record_count", 0),
            "review_workflow_count": review_workflows.get("record_count", 0),
            "github_pr_event_count": pr_events.get("record_count", 0),
            "github_actions_run_count": action_runs.get("record_count", 0),
            "deployment_evidence_count": deployment_evidence.get("record_count", 0),
            "v1_5_acceptance_state": v1_5_acceptance.get("acceptance_state", "unknown"),
        },
        "v2": {
            "acceptance_state": v2_acceptance.get("acceptance_state", "not_generated"),
            "completed_slices": v2_acceptance.get("completed_slices", 0),
            "total_slices": v2_acceptance.get("total_slices", 10),
            "completion_percent": round(
                (float(v2_acceptance.get("completed_slices", 0)) / float(v2_acceptance.get("total_slices", 10))) * 100,
                1,
            ),
            "portfolio_repo_count": v2_portfolio.get("repo_count", 0),
            "portfolio_artifact_count": v2_portfolio.get("total_artifacts", 0),
            "preflight_decision_count": v2_preflight.get("record_count", 0),
            "preflight_decision_counts": v2_preflight.get("decision_counts", {}),
            "low_confidence_high_risk_count": v2_confidence.get("low_confidence_high_risk_count", 0),
            "lineage_gap_count": v2_lineage.get("lineage_gap_count", 0),
        },
        "v3": {
            "acceptance_state": v3_acceptance.get("acceptance_state", "not_generated"),
            "completed_slices": v3_acceptance.get("completed_slices", 0),
            "total_slices": v3_acceptance.get("total_slices", 10),
            "completion_percent": round(
                (float(v3_acceptance.get("completed_slices", 0)) / float(v3_acceptance.get("total_slices", 10))) * 100,
                1,
            ),
            "connector_count": v3_connectors.get("connector_count", 0),
            "connector_record_count": v3_connectors.get("total_records", 0),
            "reconciliation_loop_count": v3_reconciliation.get("loop_count", 0),
            "divergence_count": v3_reconciliation.get("divergence_count", 0),
            "preflight_ci_record_count": v3_preflight.get("record_count", 0),
            "pilot_state": v3_pilot.get("pilot_state", "not_generated"),
        },
        "v4": {
            "acceptance_state": v4_acceptance.get("acceptance_state", "not_generated"),
            "completed_slices": v4_acceptance.get("completed_slices", 0),
            "total_slices": v4_acceptance.get("total_slices", 10),
            "completion_percent": round(
                (float(v4_acceptance.get("completed_slices", 0)) / float(v4_acceptance.get("total_slices", 10))) * 100,
                1,
            ),
            "connector_count": v4_connectors.get("connector_count", 0),
            "ready_for_install_count": v4_connectors.get("ready_for_install_count", 0),
            "reconciliation_loop_count": v4_reconciliation.get("loop_count", 0),
            "ci_target_state": v4_ci.get("target_state", "not_generated"),
            "slo_count": v4_slos.get("slo_count", 0),
            "blocked_claims": v4_acceptance.get("blocked_claims", []),
        },
        "v5": {
            "acceptance_state": v5_acceptance.get("acceptance_state", "not_generated"),
            "tooling_completion_percent": v5_acceptance.get("tooling_completion_percent", 0.0),
            "live_claim_completion_percent": v5_acceptance.get("live_claim_completion_percent", 0.0),
            "completed_slices": v5_acceptance.get("completed_slices", 0),
            "blocked_slices": v5_acceptance.get("blocked_slices", 0),
            "total_slices": v5_acceptance.get("total_slices", 10),
            "op_installed": v5_acceptance.get("op_installed", False),
            "secret_reference_count": v5_acceptance.get("secret_reference_count", 0),
            "blocked_claims": v5_acceptance.get("blocked_claims", []),
        },
        "substrate": {
            "acceptance_state": substrate_acceptance.get("acceptance_state", "not_generated"),
            "policy_completion_percent": substrate_acceptance.get("policy_completion_percent", 0.0),
            "live_evidence_completion_percent": substrate_acceptance.get("live_evidence_completion_percent", 0.0),
            "required_live_evidence_count": substrate_acceptance.get("required_live_evidence_count", 0),
            "observed_live_evidence_count": substrate_acceptance.get("observed_live_evidence_count", 0),
            "promotion_order": substrate_lifecycle.get("promotion_order", []),
            "maturity_level_count": substrate_lifecycle.get("maturity_level_count", 0),
            "blocked_claims": substrate_acceptance.get("blocked_claims", []),
        },
        "dip": {
            "acceptance_state": dip_acceptance.get("acceptance_state", "not_generated"),
            "maturity_claim": dip_acceptance.get("maturity_claim", "not_generated"),
            "policy_readiness_percent": dip_acceptance.get("policy_readiness_percent", 0.0),
            "v0_1_pre_runtime_trust_loop_skeleton_percent": dip_acceptance.get(
                "v0_1_pre_runtime_trust_loop_skeleton_percent", 0.0
            ),
            "contract_shape_evidence_percent": dip_acceptance.get("contract_shape_evidence_percent", 0.0),
            "local_validation_and_ci_evidence_percent": dip_acceptance.get("local_validation_and_ci_evidence_percent", 0.0),
            "github_repository_governance_baseline": dip_acceptance.get("github_repository_governance_baseline", "unknown"),
            "maturity_status_labels": dip_acceptance.get("maturity_status_labels", {}),
            "deterministic_policy_engine_readiness_percent": dip_acceptance.get(
                "deterministic_policy_engine_readiness_percent", 0.0
            ),
            "computed_simulation_diff_readiness_percent": dip_acceptance.get(
                "computed_simulation_diff_readiness_percent", 0.0
            ),
            "durable_case_store_readiness_percent": dip_acceptance.get("durable_case_store_readiness_percent", 0.0),
            "identity_backed_approval_readiness_percent": dip_acceptance.get(
                "identity_backed_approval_readiness_percent", 0.0
            ),
            "release_management_readiness_percent": dip_acceptance.get("release_management_readiness_percent", 0.0),
            "runtime_execution_readiness_percent": dip_acceptance.get("runtime_execution_readiness_percent", 0.0),
            "production_decision_authority_percent": dip_acceptance.get("production_decision_authority_percent", 0.0),
            "implementation_backlog_defined_percent": dip_acceptance.get("implementation_backlog_defined_percent", 0.0),
            "v0_2_backlog_defined_percent": dip_acceptance.get("v0_2_backlog_defined_percent", 0.0),
            "v0_2_backlog_status_label": dip_acceptance.get("v0_2_backlog_status_label", "not_generated"),
            "v0_3_computed_policy_diff_evidence_percent": dip_acceptance.get(
                "v0_3_computed_policy_diff_evidence_percent", 0.0
            ),
            "v0_3_status_label": dip_acceptance.get("v0_3_status_label", "not_generated"),
            "implementation_evidence_percent": dip_acceptance.get("implementation_evidence_percent", 0.0),
            "target_repo_evidence_percent": dip_acceptance.get("target_repo_evidence_percent", 0.0),
            "target_repo_governance_clean_percent": dip_acceptance.get("target_repo_governance_clean_percent", 0.0),
            "target_repo_state": (
                dip_target_evidence.get("records", [{}])[0].get("state", "not_generated")
                if dip_target_evidence.get("records")
                else "not_generated"
            ),
            "first_wedge": dip_policy.get("first_wedge", "not_generated"),
            "source_label_count": dip_policy.get("source_label_count", 0),
            "wedge_step_count": dip_policy.get("wedge_step_count", 0),
            "blocked_claims": dip_acceptance.get("blocked_claims", []),
        },
    }


def write_snapshot(root: Path, out: Path, generated_at: str | None = None) -> dict[str, Any]:
    snapshot = build_snapshot(root, generated_at)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return snapshot
