"""Materialize Decision Intelligence Platform governance readiness reports."""

from __future__ import annotations

import json
import subprocess
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
    "v0.2-backlog.md",
    "implementation-evidence.md",
    "autopilot-lanes.md",
    "target-evidence.md",
    "dip-acceptance-pack.md",
    "exports/governance-policy.json",
    "exports/wedge-readiness.json",
    "exports/implementation-backlog.json",
    "exports/v0.2-backlog.json",
    "exports/implementation-evidence.json",
    "exports/autopilot-lanes.json",
    "exports/target-evidence.json",
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


def _local_release_acceptance(repo_path: Path, version: str) -> dict[str, Any]:
    path = repo_path / "reports" / "release" / version / "release-acceptance.json"
    return load_json(path) if path.exists() else {}


def generated_timestamp(generated_at: str | None = None) -> str:
    return generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def dip_config(root: Path) -> dict[str, Any]:
    return load_json(root / "runtime-config" / "dip-readiness.json")


def dip_backlog(root: Path) -> dict[str, Any]:
    return load_json(root / "roadmap" / "dip-governed-decision-review-backlog.json")


def dip_v0_2_backlog(root: Path) -> dict[str, Any]:
    return load_json(root / "roadmap" / "dip-v0.2-backlog.json")


def dip_targets(root: Path) -> dict[str, Any]:
    return load_json(root / "runtime-config" / "dip-targets.json")


def _git_head(repo_path: Path) -> str | None:
    if not (repo_path / ".git").exists():
        return None
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_path,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def _gh_api(path: str) -> dict[str, Any]:
    result = subprocess.run(
        ["gh", "api", "--method", "GET", path],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        return {"available": False, "body": {}, "error": result.stderr.strip()}
    try:
        body = json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        body = {}
    return {"available": True, "body": body, "error": ""}


def _remote_target_evidence(target: dict[str, Any]) -> dict[str, Any]:
    repo = str(target.get("github_repo", ""))
    branch = str(target.get("default_branch", "main"))
    required_check = str(target.get("required_status_check", ""))
    workflow_name = str(target.get("ci_workflow_name", ""))
    empty = {
        "remote_repo": repo,
        "remote_url": target.get("github_url", ""),
        "remote_repo_observed": False,
        "remote_visibility": "",
        "remote_default_branch": "",
        "branch_protection_observed": False,
        "required_status_check_observed": False,
        "pull_request_reviews_observed": False,
        "admin_enforcement_observed": False,
        "force_pushes_blocked": False,
        "deletions_blocked": False,
        "ci_run_observed": False,
        "ci_workflow_name": workflow_name,
        "ci_run_status": "",
        "ci_run_conclusion": "",
        "ci_run_id": None,
        "ci_run_url": "",
        "ci_run_head_sha": "",
    }
    if not repo:
        return empty

    repo_response = _gh_api(f"repos/{repo}")
    repo_body = repo_response["body"] if repo_response["available"] else {}
    protection_response = _gh_api(f"repos/{repo}/branches/{branch}/protection")
    protection_body = protection_response["body"] if protection_response["available"] else {}
    runs_response = _gh_api(f"repos/{repo}/actions/runs?branch={branch}&per_page=10")
    runs_body = runs_response["body"] if runs_response["available"] else {}
    contexts = protection_body.get("required_status_checks", {}).get("contexts", [])
    checks = protection_body.get("required_status_checks", {}).get("checks", [])
    check_contexts = {str(item.get("context", "")) for item in checks if isinstance(item, dict)}
    review_rules = protection_body.get("required_pull_request_reviews", {})
    enforce_admins = protection_body.get("enforce_admins", {})
    allow_force_pushes = protection_body.get("allow_force_pushes", {})
    allow_deletions = protection_body.get("allow_deletions", {})
    workflow_runs = [run for run in runs_body.get("workflow_runs", []) if isinstance(run, dict)]
    matching_runs = [run for run in workflow_runs if not workflow_name or run.get("name") == workflow_name]
    latest_run = matching_runs[0] if matching_runs else {}
    return {
        "remote_repo": repo,
        "remote_url": repo_body.get("html_url", target.get("github_url", "")),
        "remote_repo_observed": repo_response["available"] and repo_body.get("full_name") == repo,
        "remote_visibility": repo_body.get("visibility", ""),
        "remote_default_branch": repo_body.get("default_branch", ""),
        "branch_protection_observed": protection_response["available"],
        "required_status_check_observed": required_check in contexts or required_check in check_contexts,
        "pull_request_reviews_observed": int(review_rules.get("required_approving_review_count", 0) or 0) >= 1,
        "admin_enforcement_observed": enforce_admins.get("enabled") is True,
        "force_pushes_blocked": allow_force_pushes.get("enabled") is False,
        "deletions_blocked": allow_deletions.get("enabled") is False,
        "ci_run_observed": latest_run.get("status") == "completed" and latest_run.get("conclusion") == "success",
        "ci_workflow_name": workflow_name,
        "ci_run_status": latest_run.get("status", ""),
        "ci_run_conclusion": latest_run.get("conclusion", ""),
        "ci_run_id": latest_run.get("id"),
        "ci_run_url": latest_run.get("html_url", ""),
        "ci_run_head_sha": latest_run.get("head_sha", ""),
    }


def _remote_release_evidence(target: dict[str, Any]) -> dict[str, Any]:
    repo = str(target.get("github_repo", ""))
    version = str(target.get("release_version", ""))
    workflow_name = str(target.get("release_workflow_name", ""))
    artifact_name = str(target.get("github_release_artifact_name", f"dip-release-evidence-{version}"))
    empty = {
        "release_version": version,
        "release_tag_observed": False,
        "release_tag_sha": "",
        "release_workflow_observed": False,
        "release_workflow_name": workflow_name,
        "release_workflow_run_id": None,
        "release_workflow_run_url": "",
        "release_workflow_conclusion": "",
        "github_release_artifact_name": artifact_name,
        "github_release_artifact_observed": False,
        "github_release_artifact_id": None,
        "github_release_artifact_expired": None,
        "artifact_release_acceptance": {},
    }
    if not repo or not version:
        return empty

    tag_response = _gh_api(f"repos/{repo}/git/ref/tags/{version}")
    tag_body = tag_response["body"] if tag_response["available"] else {}
    tag_object_sha = tag_body.get("object", {}).get("sha", "")
    tag_object_type = tag_body.get("object", {}).get("type", "")
    release_commit_sha = tag_object_sha
    if tag_response["available"] and tag_object_sha and tag_object_type == "tag":
        tag_object_response = _gh_api(f"repos/{repo}/git/tags/{tag_object_sha}")
        tag_object_body = tag_object_response["body"] if tag_object_response["available"] else {}
        release_commit_sha = tag_object_body.get("object", {}).get("sha", tag_object_sha)
    workflow_runs = []
    for event in ("push", "workflow_dispatch"):
        runs_response = _gh_api(f"repos/{repo}/actions/runs?event={event}&per_page=20")
        runs_body = runs_response["body"] if runs_response["available"] else {}
        workflow_runs.extend(
            run for run in runs_body.get("workflow_runs", []) if isinstance(run, dict)
        )
    matching_runs = [
        run
        for run in workflow_runs
        if run.get("name") == workflow_name
        and run.get("head_branch") == version
        and run.get("status") == "completed"
        and run.get("conclusion") == "success"
    ]
    latest_run = matching_runs[0] if matching_runs else {}
    artifact = {}
    artifact_acceptance = {}
    if latest_run.get("id"):
        artifact_response = _gh_api(f"repos/{repo}/actions/runs/{latest_run['id']}/artifacts")
        artifact_body = artifact_response["body"] if artifact_response["available"] else {}
        artifacts = [item for item in artifact_body.get("artifacts", []) if isinstance(item, dict)]
        artifact = next((item for item in artifacts if item.get("name") == artifact_name), {})
        if artifact:
            with tempfile.TemporaryDirectory() as tmp:
                download = subprocess.run(
                    [
                        "gh",
                        "run",
                        "download",
                        str(latest_run["id"]),
                        "--repo",
                        repo,
                        "--name",
                        artifact_name,
                        "--dir",
                        tmp,
                    ],
                    check=False,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                acceptance_path = Path(tmp) / "release-acceptance.json"
                if download.returncode == 0 and acceptance_path.exists():
                    artifact_acceptance = load_json(acceptance_path)
    return {
        "release_version": version,
        "release_tag_observed": tag_response["available"],
        "release_tag_sha": release_commit_sha,
        "release_workflow_observed": bool(latest_run),
        "release_workflow_name": workflow_name,
        "release_workflow_run_id": latest_run.get("id"),
        "release_workflow_run_url": latest_run.get("html_url", ""),
        "release_workflow_conclusion": latest_run.get("conclusion", ""),
        "github_release_artifact_name": artifact_name,
        "github_release_artifact_observed": bool(artifact) and artifact.get("expired") is False and bool(artifact_acceptance),
        "github_release_artifact_id": artifact.get("id"),
        "github_release_artifact_expired": artifact.get("expired"),
        "artifact_release_acceptance": artifact_acceptance,
    }


def target_evidence_payload(
    root: Path,
    generated_at: str,
    existing_target_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if existing_target_evidence is not None:
        preserved = dict(existing_target_evidence)
        preserved["generated_at"] = generated_at
        return preserved

    config = dip_targets(root)
    targets = config.get("targets", [])
    records = []
    for target in targets:
        repo_path = Path(str(target.get("repo_path", "")))
        evidence_root = repo_path / str(target.get("evidence_root", "reports/trust-loop"))
        validation_path = evidence_root / "validation.json"
        trust_loop_path = evidence_root / "trust-loop-run.json"
        acceptance_path = evidence_root / "dip-mvp-acceptance.json"
        approval_authority_path = evidence_root / "approval-authority.json"
        release_acceptance_path = repo_path / str(target.get("release_acceptance_path", ""))
        repo_exists = repo_path.exists()
        validation = load_json(validation_path) if validation_path.exists() else {}
        trust_loop = load_json(trust_loop_path) if trust_loop_path.exists() else {}
        acceptance = load_json(acceptance_path) if acceptance_path.exists() else {}
        approval_authority = load_json(approval_authority_path) if approval_authority_path.exists() else {}
        local_release_acceptance = load_json(release_acceptance_path) if release_acceptance_path.exists() else {}
        v11_release_acceptance = _local_release_acceptance(repo_path, "v11.0.0-pre")
        validation_passed = validation.get("passed") is True
        trust_loop_complete = bool(
            trust_loop.get("run_id")
            and trust_loop.get("runtime_execution_requested") is False
            and acceptance.get("trust_loop_complete") is True
            and acceptance.get("runtime_integration_authorized") is False
            and acceptance.get("production_decision_execution_authorized") is False
        )
        remote_evidence = _remote_target_evidence(target)
        release_evidence = _remote_release_evidence(target)
        artifact_release_acceptance = release_evidence.pop("artifact_release_acceptance", {})
        release_acceptance = artifact_release_acceptance or local_release_acceptance
        remote_complete = (
            remote_evidence["remote_repo_observed"]
            and remote_evidence["remote_visibility"] == "public"
            and remote_evidence["remote_default_branch"] == target.get("default_branch")
            and remote_evidence["branch_protection_observed"]
            and remote_evidence["required_status_check_observed"]
            and remote_evidence["pull_request_reviews_observed"]
            and remote_evidence["admin_enforcement_observed"]
            and remote_evidence["force_pushes_blocked"]
            and remote_evidence["deletions_blocked"]
            and remote_evidence["ci_run_observed"]
        )
        release_complete = (
            release_evidence["release_tag_observed"]
            and release_evidence["release_workflow_observed"]
            and release_acceptance.get("release_acceptance_passed") is True
            and release_acceptance.get("computed_policy_preflight_observed") is True
            and release_acceptance.get("computed_simulation_observed") is True
            and release_acceptance.get("computed_decision_diff_observed") is True
            and int(release_acceptance.get("computed_simulation_domain_count", 0) or 0) >= 2
            and int(release_acceptance.get("computed_simulation_decision_shape_count", 0) or 0) >= 2
            and release_acceptance.get("case_manifest_valid") is True
            and release_acceptance.get("durable_case_manifest_valid") is True
            and release_acceptance.get("append_only_chain_valid") is True
            and release_acceptance.get("case_mutation_detected") is False
            and release_acceptance.get("replay_from_manifest_observed") is True
            and release_acceptance.get("replay_manifest_valid") is True
            and release_acceptance.get("approval_bound_to_manifest") is True
            and release_acceptance.get("approval_role_binding_valid") is True
            and release_acceptance.get("approval_authority_evaluated") is True
            and release_acceptance.get("approval_authority_valid") is True
            and release_acceptance.get("approval_identity_active") is True
            and release_acceptance.get("approval_identity_not_expired") is True
            and release_acceptance.get("approval_mfa_satisfied") is True
            and release_acceptance.get("approval_decision_scope_authorized") is True
            and release_acceptance.get("ai_self_approval_blocked") is True
            and release_acceptance.get("external_identity_provider_observed") is False
            and release_acceptance.get("repository_governance_policy_observed") is True
            and release_acceptance.get("admin_enforcement_required") is True
            and int(release_acceptance.get("required_status_check_count", 0) or 0) >= 1
            and release_acceptance.get("break_glass_policy_defined") is True
            and release_acceptance.get("release_lifecycle_policy_observed") is True
            and release_acceptance.get("release_lifecycle_valid") is True
            and release_acceptance.get("independent_release_approval_required") is True
            and release_acceptance.get("codeowner_review_required") is True
            and release_acceptance.get("conversation_resolution_required") is True
            and release_acceptance.get("rollback_criteria_defined") is True
            and release_acceptance.get("external_identity_contract_observed") is True
            and release_acceptance.get("external_identity_contract_valid") is True
            and release_acceptance.get("live_external_identity_provider_authenticated") is False
            and release_acceptance.get("live_identity_rbac_observed") is True
            and release_acceptance.get("live_identity_rbac_valid") is True
            and release_acceptance.get("live_identity_rbac_provider") == "github"
            and release_acceptance.get("live_identity_rbac_permission_sufficient") is True
            and release_acceptance.get("live_identity_rbac_decision_scope_authorized") is True
            and release_acceptance.get("live_identity_rbac_mfa_claim_observed") is False
            and release_acceptance.get("durable_evidence_store_policy_observed") is True
            and release_acceptance.get("durable_store_contract_valid") is True
            and release_acceptance.get("production_storage_backend_observed") is False
            and release_acceptance.get("capability_governance_observed") is True
            and release_acceptance.get("capability_governance_valid") is True
            and int(release_acceptance.get("resolved_capability_count", 0) or 0) >= 3
            and release_acceptance.get("shared_context_contract_observed") is True
            and release_acceptance.get("shared_context_contract_valid") is True
            and release_acceptance.get("solo_maintainer_exception_observed") is True
            and release_acceptance.get("solo_maintainer_exception_valid") is True
            and release_acceptance.get("solo_maintainer_constraint") is True
            and release_acceptance.get("independent_human_review_available") is False
            and release_acceptance.get("independent_human_review_observed") is False
            and release_acceptance.get("review_relaxation_allowed") is True
            and release_acceptance.get("review_gate_restoration_required") is True
            and release_acceptance.get("schema_stability_observed") is True
            and release_acceptance.get("schema_stability_valid") is True
            and int(release_acceptance.get("frozen_contract_count", 0) or 0) >= 16
            and int(release_acceptance.get("negative_fixture_count", 0) or 0) >= 2
            and release_acceptance.get("negative_fixtures_valid") is True
            and release_acceptance.get("external_approval_boundary_observed") is True
            and release_acceptance.get("external_approval_boundary_valid") is True
            and release_acceptance.get("live_external_approval_system_observed") is False
            and release_acceptance.get("decision_approval_required") is True
            and release_acceptance.get("decision_approval_separate_from_code_merge") is True
            and release_acceptance.get("github_code_review_is_decision_approval") is False
            and release_acceptance.get("solo_maintainer_exception_is_decision_approval") is False
            and release_acceptance.get("external_approval_required_evidence_complete") is True
            and release_acceptance.get("external_approval_admission_controls_complete") is True
            and release_acceptance.get("external_approval_adapter_observed") is True
            and release_acceptance.get("external_approval_adapter_valid") is True
            and release_acceptance.get("external_approval_adapter_required_operations_complete") is True
            and release_acceptance.get("external_approval_adapter_denied_operations_complete") is True
            and release_acceptance.get("external_approval_adapter_request_evidence_complete") is True
            and release_acceptance.get("external_approval_adapter_decision_evidence_complete") is True
            and release_acceptance.get("external_approval_adapter_decision_lifecycle_complete") is True
            and release_acceptance.get("external_approval_adapter_admission_controls_complete") is True
            and release_acceptance.get("external_approval_adapter_audit_requirements_complete") is True
            and release_acceptance.get("external_approval_adapter_boundary_compatible") is True
            and release_acceptance.get("external_approval_adapter_live_system_observed") is False
            and release_acceptance.get("external_approval_adapter_ai_approval_allowed") is False
            and release_acceptance.get("durable_case_store_adapter_observed") is True
            and release_acceptance.get("durable_case_store_adapter_valid") is True
            and release_acceptance.get("adapter_production_storage_backend_observed") is False
            and release_acceptance.get("adapter_append_only_writes_required") is True
            and release_acceptance.get("adapter_content_addressed_records_required") is True
            and release_acceptance.get("adapter_delete_denied_required") is True
            and release_acceptance.get("adapter_mutation_detection_required") is True
            and release_acceptance.get("adapter_replay_export_required") is True
            and release_acceptance.get("adapter_audit_export_required") is True
            and release_acceptance.get("adapter_retention_policy_valid") is True
            and release_acceptance.get("adapter_required_operations_complete") is True
            and release_acceptance.get("adapter_denied_operations_complete") is True
            and release_acceptance.get("evidence_store_adapter_parity_observed") is True
            and release_acceptance.get("evidence_store_adapter_parity_valid") is True
            and release_acceptance.get("adapter_required_operations_valid") is True
            and release_acceptance.get("adapter_denied_operations_enforced") is True
            and release_acceptance.get("adapter_append_case_record_valid") is True
            and release_acceptance.get("adapter_read_case_record_valid") is True
            and release_acceptance.get("adapter_verify_manifest_chain_valid") is True
            and release_acceptance.get("adapter_export_replay_pack_valid") is True
            and release_acceptance.get("adapter_export_audit_pack_valid") is True
            and release_acceptance.get("adapter_runtime_backend_invoked") is False
            and release_acceptance.get("durable_evidence_backend_observed") is True
            and release_acceptance.get("durable_evidence_backend_valid") is True
            and release_acceptance.get("durable_backend_runtime_backend_invoked") is False
            and release_acceptance.get("durable_backend_production_storage_backend_observed") is False
            and release_acceptance.get("release_promotion_chain_observed") is True
            and release_acceptance.get("release_promotion_chain_valid") is True
            and release_acceptance.get("immutable_artifact_digest_observed") is True
            and release_acceptance.get("source_commit_bound") is True
            and release_acceptance.get("build_run_id_observed") is True
            and release_acceptance.get("rollback_evidence_valid") is True
            and release_acceptance.get("prod_deployment_executed") is False
            and release_acceptance.get("pre_runtime_ga_observed") is True
            and release_acceptance.get("pre_runtime_ga_valid") is True
            and release_acceptance.get("pre_runtime_runtime_blocked") is True
            and release_acceptance.get("v3_1_governance_closure_valid") is True
            and release_acceptance.get("v3_1_independent_human_review_observed") is False
            and release_acceptance.get("v3_2_external_identity_boundary_valid") is True
            and release_acceptance.get("v3_2_external_identity_live_ready") is False
            and release_acceptance.get("v3_2_mfa_claim_observed") is False
            and release_acceptance.get("v3_3_external_approval_system_boundary_valid") is True
            and release_acceptance.get("v3_3_external_approval_system_live_ready") is False
            and release_acceptance.get("v3_3_ai_approval_allowed") is False
            and release_acceptance.get("v3_4_production_case_store_contract_ready") is True
            and release_acceptance.get("v3_4_production_case_store_live_ready") is False
            and release_acceptance.get("v3_4_production_storage_backend_observed") is False
            and release_acceptance.get("v3_5_runtime_control_plane_design_valid") is True
            and release_acceptance.get("v3_5_runtime_authority_grant_allowed") is False
            and release_acceptance.get("v3_6_advisory_runtime_pilot_valid") is True
            and release_acceptance.get("v3_6_advisory_side_effects_executed") is False
            and release_acceptance.get("v3_6_production_mutation_executed") is False
            and release_acceptance.get("v4_0_limited_runtime_authority_gate_complete") is True
            and release_acceptance.get("v4_0_limited_runtime_authority_granted") is False
            and release_acceptance.get("v4_1_live_identity_evidence_gate_complete") is True
            and release_acceptance.get("v4_1_live_identity_authority_ready") is False
            and release_acceptance.get("v4_1_mfa_claim_observed") is False
            and release_acceptance.get("v4_2_live_approval_provider_gate_complete") is True
            and release_acceptance.get("v4_2_live_approval_provider_ready") is False
            and release_acceptance.get("v4_2_ai_approval_allowed") is False
            and release_acceptance.get("v4_3_production_case_store_gate_complete") is True
            and release_acceptance.get("v4_3_production_case_store_live_ready") is False
            and release_acceptance.get("v4_4_release_promotion_execution_gate_complete") is True
            and release_acceptance.get("v4_4_prod_deployment_executed") is False
            and release_acceptance.get("v5_0_governed_advisory_runtime_complete") is True
            and release_acceptance.get("v5_0_runtime_recommendation_only") is True
            and release_acceptance.get("v5_0_side_effects_executed") is False
            and release_acceptance.get("v5_5_controlled_runtime_execution_gate_complete") is True
            and release_acceptance.get("v5_5_controlled_runtime_execution_authorized") is False
            and release_acceptance.get("v6_0_platform_hardening_assessment_complete") is True
            and release_acceptance.get("v6_0_platform_production_ready") is False
            and release_acceptance.get("v6_1_live_identity_authority_contract_complete") is True
            and release_acceptance.get("v6_1_live_identity_authority_ready") is False
            and release_acceptance.get("v6_1_mfa_claim_observed") is False
            and release_acceptance.get("v6_2_live_decision_approval_provider_contract_complete") is True
            and release_acceptance.get("v6_2_live_decision_approval_provider_ready") is False
            and release_acceptance.get("v6_2_ai_approval_allowed") is False
            and release_acceptance.get("v6_3_production_durable_case_store_contract_complete") is True
            and release_acceptance.get("v6_3_production_durable_case_store_ready") is False
            and release_acceptance.get("v6_4_production_promotion_chain_contract_complete") is True
            and release_acceptance.get("v6_4_production_promotion_ready") is False
            and release_acceptance.get("v7_0_controlled_runtime_pilot_admission_complete") is True
            and release_acceptance.get("v7_0_controlled_runtime_pilot_authorized") is False
            and release_acceptance.get("v7_5_marketplace_runtime_governance_complete") is True
            and release_acceptance.get("v7_5_marketplace_runtime_invocation_authorized") is False
            and release_acceptance.get("v7_5_unrestricted_marketplace_execution_allowed") is False
            and release_acceptance.get("v8_0_shared_context_runtime_governance_complete") is True
            and release_acceptance.get("v8_0_runtime_context_exchange_authorized") is False
            and release_acceptance.get("v8_0_direct_database_access_allowed") is False
            and release_acceptance.get("v9_0_production_authority_readiness_review_complete") is True
            and release_acceptance.get("v9_0_production_decision_authority_granted") is False
            and release_acceptance.get("v10_0_completion_plan_execution_observed") is True
            and release_acceptance.get("v10_0_autopilot_execution_review_complete") is True
            and int(release_acceptance.get("v10_0_reviewed_step_count", 0) or 0) == 9
            and int(release_acceptance.get("v10_0_evidence_gate_complete_count", 0) or 0) == 9
            and int(release_acceptance.get("v10_0_blocked_live_completion_count", 0) or 0) >= 9
            and release_acceptance.get("v10_0_product_vision_alignment_valid") is True
            and release_acceptance.get("v10_0_ai_policy_boundary_preserved") is True
            and release_acceptance.get("v10_0_runtime_authority_grant_blocked") is True
            and release_acceptance.get("v10_0_production_decision_authority_blocked") is True
            and release_acceptance.get("computed_policy_engine_observed") is True
            and release_acceptance.get("computed_policy_engine_result") == "approval_required"
            and release_acceptance.get("policy_engine_valid") is True
            and int(release_acceptance.get("policy_engine_supported_rule_type_count", 0) or 0) >= 5
            and int(release_acceptance.get("policy_engine_active_policy_count", 0) or 0) >= 5
            and int(release_acceptance.get("policy_engine_revoked_policy_count", 0) or 0) == 0
            and release_acceptance.get("policy_engine_deny_precedence_enforced") is True
            and release_acceptance.get("policy_engine_escalate_outcome_supported") is True
            and release_acceptance.get("policy_engine_compatibility_valid") is True
            and release_acceptance.get("product_review_surface_observed") is True
            and int(release_acceptance.get("product_review_surface_count", 0) or 0) >= 43
            and release_acceptance.get("runtime_readiness_assessment_observed") is True
            and float(release_acceptance.get("runtime_readiness_percent", 100.0) or 0.0) == 0.0
            and float(release_acceptance.get("production_decision_authority_percent", 100.0) or 0.0) == 0.0
            and release_acceptance.get("runtime_integration_authorized") is False
            and release_acceptance.get("production_decision_execution_authorized") is False
        )
        release_acceptance_source_commit = str(release_acceptance.get("source_commit", ""))
        release_acceptance_commit_matches_tag = bool(
            release_acceptance_source_commit
            and release_acceptance_source_commit == release_evidence.get("release_tag_sha")
        )
        github_release_artifact_observed = bool(release_evidence.get("github_release_artifact_observed", False))
        main_update_bypass_observed = bool(target.get("main_update_bypass_observed", False))
        main_update_bypass_governed = bool(target.get("main_update_bypass_governed", False))
        evidence_files_present = validation_path.exists() and trust_loop_path.exists() and acceptance_path.exists()
        record_complete = (
            repo_exists
            and evidence_files_present
            and validation_passed
            and trust_loop_complete
            and remote_complete
            and release_complete
            and target.get("runtime_integration_authorized") is False
            and target.get("production_decision_execution_authorized") is False
        )
        release_governance_clean = (
            record_complete
            and (not main_update_bypass_observed or main_update_bypass_governed)
            and remote_evidence["admin_enforcement_observed"]
            and release_acceptance.get("break_glass_policy_defined") is True
            and release_acceptance_commit_matches_tag
            and github_release_artifact_observed
        )
        records.append(
            {
                "target_id": target.get("target_id"),
                "target_name": target.get("target_name"),
                "repo_role": target.get("repo_role"),
                "repo_path": str(repo_path),
                **remote_evidence,
                **release_evidence,
                "git_commit": _git_head(repo_path) if repo_exists else None,
                "validation_command": target.get("validation_command"),
                "evidence_root": str(evidence_root),
                "evidence_source_boundary": target.get("evidence_source_boundary"),
                "repo_exists": repo_exists,
                "evidence_files_present": evidence_files_present,
                "release_acceptance_path": str(release_acceptance_path),
                "release_acceptance_observed": bool(release_acceptance),
                "release_acceptance_source": "github_actions_artifact"
                if artifact_release_acceptance
                else "local_committed_file"
                if local_release_acceptance
                else "missing",
                "release_acceptance_passed": release_acceptance.get("release_acceptance_passed") is True,
                "release_acceptance_source_commit": release_acceptance_source_commit,
                "release_acceptance_commit_matches_tag": release_acceptance_commit_matches_tag,
                "github_release_artifact_observed": github_release_artifact_observed,
                "release_governance_clean": release_governance_clean,
                "computed_policy_preflight_observed": release_acceptance.get("computed_policy_preflight_observed") is True,
                "computed_policy_preflight_result": release_acceptance.get("computed_policy_preflight_result"),
                "computed_simulation_observed": release_acceptance.get("computed_simulation_observed") is True,
                "computed_simulation_case_count": release_acceptance.get("computed_simulation_case_count", 0),
                "computed_simulation_domain_count": release_acceptance.get("computed_simulation_domain_count", 0),
                "computed_simulation_decision_shape_count": release_acceptance.get(
                    "computed_simulation_decision_shape_count", 0
                ),
                "computed_decision_diff_observed": release_acceptance.get("computed_decision_diff_observed") is True,
                "computed_decision_diff_changed_outcomes": release_acceptance.get(
                    "computed_decision_diff_changed_outcomes", 0
                ),
                "case_manifest_valid": release_acceptance.get("case_manifest_valid") is True,
                "case_manifest_artifact_count": release_acceptance.get("case_manifest_artifact_count", 0),
                "durable_case_manifest_observed": release_acceptance.get("durable_case_manifest_observed") is True,
                "durable_case_manifest_hash": release_acceptance.get("durable_case_manifest_hash", ""),
                "durable_case_manifest_valid": release_acceptance.get("durable_case_manifest_valid") is True,
                "append_only_chain_valid": release_acceptance.get("append_only_chain_valid") is True,
                "case_mutation_detected": release_acceptance.get("case_mutation_detected") is True,
                "replay_from_manifest_observed": release_acceptance.get("replay_from_manifest_observed") is True,
                "replay_manifest_valid": release_acceptance.get("replay_manifest_valid") is True,
                "approval_bound_to_manifest": release_acceptance.get("approval_bound_to_manifest") is True,
                "approval_role_binding_valid": release_acceptance.get("approval_role_binding_valid") is True,
                "approval_authority_evaluated": release_acceptance.get("approval_authority_evaluated") is True,
                "approval_authority_valid": release_acceptance.get("approval_authority_valid") is True,
                "approver_subject": approval_authority.get("approver_subject"),
                "approval_identity_active": release_acceptance.get("approval_identity_active") is True,
                "approval_identity_not_expired": release_acceptance.get("approval_identity_not_expired") is True,
                "approval_mfa_satisfied": release_acceptance.get("approval_mfa_satisfied") is True,
                "approval_decision_scope_authorized": release_acceptance.get("approval_decision_scope_authorized") is True,
                "ai_self_approval_blocked": release_acceptance.get("ai_self_approval_blocked") is True,
                "external_identity_provider_observed": release_acceptance.get("external_identity_provider_observed") is True,
                "repository_governance_policy_observed": release_acceptance.get(
                    "repository_governance_policy_observed"
                )
                is True,
                "admin_enforcement_required": release_acceptance.get("admin_enforcement_required") is True,
                "required_status_check_count": release_acceptance.get("required_status_check_count", 0),
                "break_glass_policy_defined": release_acceptance.get("break_glass_policy_defined") is True,
                "release_lifecycle_policy_observed": release_acceptance.get("release_lifecycle_policy_observed") is True,
                "release_lifecycle_valid": release_acceptance.get("release_lifecycle_valid") is True,
                "independent_release_approval_required": release_acceptance.get(
                    "independent_release_approval_required"
                )
                is True,
                "codeowner_review_required": release_acceptance.get("codeowner_review_required") is True,
                "conversation_resolution_required": release_acceptance.get("conversation_resolution_required") is True,
                "rollback_criteria_defined": release_acceptance.get("rollback_criteria_defined") is True,
                "required_status_checks_observed": release_acceptance.get("required_status_checks_observed") is True,
                "required_approving_review_count_observed": release_acceptance.get(
                    "required_approving_review_count_observed", 0
                ),
                "codeowner_review_required_observed": release_acceptance.get("codeowner_review_required_observed")
                is True,
                "conversation_resolution_required_observed": release_acceptance.get(
                    "conversation_resolution_required_observed"
                )
                is True,
                "external_identity_contract_observed": release_acceptance.get("external_identity_contract_observed")
                is True,
                "external_identity_contract_valid": release_acceptance.get("external_identity_contract_valid") is True,
                "live_external_identity_provider_authenticated": release_acceptance.get(
                    "live_external_identity_provider_authenticated"
                )
                is True,
                "live_identity_rbac_observed": release_acceptance.get("live_identity_rbac_observed") is True,
                "live_identity_rbac_valid": release_acceptance.get("live_identity_rbac_valid") is True,
                "live_identity_rbac_provider": release_acceptance.get("live_identity_rbac_provider"),
                "live_identity_rbac_subject": release_acceptance.get("live_identity_rbac_subject"),
                "live_identity_rbac_repository_permission": release_acceptance.get(
                    "live_identity_rbac_repository_permission"
                ),
                "live_identity_rbac_permission_sufficient": release_acceptance.get(
                    "live_identity_rbac_permission_sufficient"
                )
                is True,
                "live_identity_rbac_decision_scope_authorized": release_acceptance.get(
                    "live_identity_rbac_decision_scope_authorized"
                )
                is True,
                "live_identity_rbac_mfa_claim_observed": release_acceptance.get(
                    "live_identity_rbac_mfa_claim_observed"
                )
                is True,
                "durable_evidence_store_policy_observed": release_acceptance.get(
                    "durable_evidence_store_policy_observed"
                )
                is True,
                "durable_store_contract_valid": release_acceptance.get("durable_store_contract_valid") is True,
                "production_storage_backend_observed": release_acceptance.get("production_storage_backend_observed")
                is True,
                "capability_governance_observed": release_acceptance.get("capability_governance_observed") is True,
                "capability_governance_valid": release_acceptance.get("capability_governance_valid") is True,
                "resolved_capability_count": release_acceptance.get("resolved_capability_count", 0),
                "shared_context_contract_observed": release_acceptance.get("shared_context_contract_observed") is True,
                "shared_context_contract_valid": release_acceptance.get("shared_context_contract_valid") is True,
                "solo_maintainer_exception_observed": release_acceptance.get("solo_maintainer_exception_observed")
                is True,
                "solo_maintainer_exception_valid": release_acceptance.get("solo_maintainer_exception_valid") is True,
                "solo_maintainer_constraint": release_acceptance.get("solo_maintainer_constraint") is True,
                "independent_human_review_available": release_acceptance.get("independent_human_review_available")
                is True,
                "independent_human_review_observed": release_acceptance.get("independent_human_review_observed")
                is True,
                "review_relaxation_allowed": release_acceptance.get("review_relaxation_allowed") is True,
                "review_relaxation_max_minutes": release_acceptance.get("review_relaxation_max_minutes", 0),
                "review_gate_restoration_required": release_acceptance.get("review_gate_restoration_required") is True,
                "schema_stability_observed": release_acceptance.get("schema_stability_observed") is True,
                "schema_stability_valid": release_acceptance.get("schema_stability_valid") is True,
                "frozen_contract_count": release_acceptance.get("frozen_contract_count", 0),
                "compatibility_rule_count": release_acceptance.get("compatibility_rule_count", 0),
                "negative_fixture_count": release_acceptance.get("negative_fixture_count", 0),
                "negative_fixtures_valid": release_acceptance.get("negative_fixtures_valid") is True,
                "external_approval_boundary_observed": release_acceptance.get("external_approval_boundary_observed")
                is True,
                "external_approval_boundary_valid": release_acceptance.get("external_approval_boundary_valid") is True,
                "live_external_approval_system_observed": release_acceptance.get(
                    "live_external_approval_system_observed"
                )
                is True,
                "decision_approval_required": release_acceptance.get("decision_approval_required") is True,
                "decision_approval_separate_from_code_merge": release_acceptance.get(
                    "decision_approval_separate_from_code_merge"
                )
                is True,
                "github_code_review_is_decision_approval": release_acceptance.get(
                    "github_code_review_is_decision_approval"
                )
                is True,
                "solo_maintainer_exception_is_decision_approval": release_acceptance.get(
                    "solo_maintainer_exception_is_decision_approval"
                )
                is True,
                "external_approval_required_evidence_count": release_acceptance.get(
                    "external_approval_required_evidence_count", 0
                ),
                "external_approval_required_evidence_complete": release_acceptance.get(
                    "external_approval_required_evidence_complete"
                )
                is True,
                "external_approval_admission_controls_complete": release_acceptance.get(
                    "external_approval_admission_controls_complete"
                )
                is True,
                "external_approval_adapter_observed": release_acceptance.get(
                    "external_approval_adapter_observed"
                )
                is True,
                "external_approval_adapter_valid": release_acceptance.get("external_approval_adapter_valid")
                is True,
                "external_approval_adapter_required_operations_complete": release_acceptance.get(
                    "external_approval_adapter_required_operations_complete"
                )
                is True,
                "external_approval_adapter_denied_operations_complete": release_acceptance.get(
                    "external_approval_adapter_denied_operations_complete"
                )
                is True,
                "external_approval_adapter_request_evidence_complete": release_acceptance.get(
                    "external_approval_adapter_request_evidence_complete"
                )
                is True,
                "external_approval_adapter_decision_evidence_complete": release_acceptance.get(
                    "external_approval_adapter_decision_evidence_complete"
                )
                is True,
                "external_approval_adapter_decision_lifecycle_complete": release_acceptance.get(
                    "external_approval_adapter_decision_lifecycle_complete"
                )
                is True,
                "external_approval_adapter_admission_controls_complete": release_acceptance.get(
                    "external_approval_adapter_admission_controls_complete"
                )
                is True,
                "external_approval_adapter_audit_requirements_complete": release_acceptance.get(
                    "external_approval_adapter_audit_requirements_complete"
                )
                is True,
                "external_approval_adapter_boundary_compatible": release_acceptance.get(
                    "external_approval_adapter_boundary_compatible"
                )
                is True,
                "external_approval_adapter_live_system_observed": release_acceptance.get(
                    "external_approval_adapter_live_system_observed"
                )
                is True,
                "external_approval_adapter_ai_approval_allowed": release_acceptance.get(
                    "external_approval_adapter_ai_approval_allowed"
                )
                is True,
                "durable_case_store_adapter_observed": release_acceptance.get(
                    "durable_case_store_adapter_observed"
                )
                is True,
                "durable_case_store_adapter_valid": release_acceptance.get("durable_case_store_adapter_valid")
                is True,
                "adapter_production_storage_backend_observed": release_acceptance.get(
                    "adapter_production_storage_backend_observed"
                )
                is True,
                "adapter_append_only_writes_required": release_acceptance.get("adapter_append_only_writes_required")
                is True,
                "adapter_content_addressed_records_required": release_acceptance.get(
                    "adapter_content_addressed_records_required"
                )
                is True,
                "adapter_delete_denied_required": release_acceptance.get("adapter_delete_denied_required") is True,
                "adapter_mutation_detection_required": release_acceptance.get("adapter_mutation_detection_required")
                is True,
                "adapter_replay_export_required": release_acceptance.get("adapter_replay_export_required") is True,
                "adapter_audit_export_required": release_acceptance.get("adapter_audit_export_required") is True,
                "adapter_retention_policy_valid": release_acceptance.get("adapter_retention_policy_valid") is True,
                "adapter_required_operations_complete": release_acceptance.get("adapter_required_operations_complete")
                is True,
                "adapter_denied_operations_complete": release_acceptance.get("adapter_denied_operations_complete")
                is True,
                "evidence_store_adapter_parity_observed": release_acceptance.get(
                    "evidence_store_adapter_parity_observed"
                )
                is True,
                "evidence_store_adapter_parity_valid": release_acceptance.get(
                    "evidence_store_adapter_parity_valid"
                )
                is True,
                "adapter_required_operations_valid": release_acceptance.get("adapter_required_operations_valid")
                is True,
                "adapter_denied_operations_enforced": release_acceptance.get("adapter_denied_operations_enforced")
                is True,
                "adapter_append_case_record_valid": release_acceptance.get("adapter_append_case_record_valid")
                is True,
                "adapter_read_case_record_valid": release_acceptance.get("adapter_read_case_record_valid") is True,
                "adapter_verify_manifest_chain_valid": release_acceptance.get(
                    "adapter_verify_manifest_chain_valid"
                )
                is True,
                "adapter_export_replay_pack_valid": release_acceptance.get("adapter_export_replay_pack_valid")
                is True,
                "adapter_export_audit_pack_valid": release_acceptance.get("adapter_export_audit_pack_valid")
                is True,
                "adapter_runtime_backend_invoked": release_acceptance.get("adapter_runtime_backend_invoked") is True,
                "durable_evidence_backend_observed": release_acceptance.get("durable_evidence_backend_observed")
                is True,
                "durable_evidence_backend_valid": release_acceptance.get("durable_evidence_backend_valid") is True,
                "durable_backend_runtime_backend_invoked": release_acceptance.get(
                    "durable_backend_runtime_backend_invoked"
                )
                is True,
                "durable_backend_production_storage_backend_observed": release_acceptance.get(
                    "durable_backend_production_storage_backend_observed"
                )
                is True,
                "release_promotion_chain_observed": release_acceptance.get("release_promotion_chain_observed")
                is True,
                "release_promotion_chain_valid": release_acceptance.get("release_promotion_chain_valid") is True,
                "immutable_artifact_digest_observed": release_acceptance.get("immutable_artifact_digest_observed")
                is True,
                "source_commit_bound": release_acceptance.get("source_commit_bound") is True,
                "build_run_id_observed": release_acceptance.get("build_run_id_observed") is True,
                "rollback_evidence_valid": release_acceptance.get("rollback_evidence_valid") is True,
                "prod_deployment_executed": release_acceptance.get("prod_deployment_executed") is True,
                "pre_runtime_ga_observed": release_acceptance.get("pre_runtime_ga_observed") is True,
                "pre_runtime_ga_valid": release_acceptance.get("pre_runtime_ga_valid") is True,
                "pre_runtime_ga_status_label": release_acceptance.get("pre_runtime_ga_status_label", "not_generated"),
                "pre_runtime_runtime_blocked": release_acceptance.get("pre_runtime_runtime_blocked") is True,
                "v3_1_governance_closure_observed": release_acceptance.get("v3_1_governance_closure_observed")
                is True,
                "v3_1_governance_closure_valid": release_acceptance.get("v3_1_governance_closure_valid") is True,
                "v3_1_independent_human_review_observed": release_acceptance.get(
                    "v3_1_independent_human_review_observed"
                )
                is True,
                "v3_2_external_identity_integration_observed": release_acceptance.get(
                    "v3_2_external_identity_integration_observed"
                )
                is True,
                "v3_2_external_identity_boundary_valid": release_acceptance.get(
                    "v3_2_external_identity_boundary_valid"
                )
                is True,
                "v3_2_external_identity_live_ready": release_acceptance.get(
                    "v3_2_external_identity_live_ready"
                )
                is True,
                "v3_2_mfa_claim_observed": release_acceptance.get("v3_2_mfa_claim_observed") is True,
                "v3_3_external_approval_system_observed": release_acceptance.get(
                    "v3_3_external_approval_system_observed"
                )
                is True,
                "v3_3_external_approval_system_boundary_valid": release_acceptance.get(
                    "v3_3_external_approval_system_boundary_valid"
                )
                is True,
                "v3_3_external_approval_system_live_ready": release_acceptance.get(
                    "v3_3_external_approval_system_live_ready"
                )
                is True,
                "v3_3_ai_approval_allowed": release_acceptance.get("v3_3_ai_approval_allowed") is True,
                "v3_4_production_case_store_backend_observed": release_acceptance.get(
                    "v3_4_production_case_store_backend_observed"
                )
                is True,
                "v3_4_production_case_store_contract_ready": release_acceptance.get(
                    "v3_4_production_case_store_contract_ready"
                )
                is True,
                "v3_4_production_case_store_live_ready": release_acceptance.get(
                    "v3_4_production_case_store_live_ready"
                )
                is True,
                "v3_4_production_storage_backend_observed": release_acceptance.get(
                    "v3_4_production_storage_backend_observed"
                )
                is True,
                "v3_5_runtime_control_plane_observed": release_acceptance.get(
                    "v3_5_runtime_control_plane_observed"
                )
                is True,
                "v3_5_runtime_control_plane_design_valid": release_acceptance.get(
                    "v3_5_runtime_control_plane_design_valid"
                )
                is True,
                "v3_5_runtime_authority_grant_allowed": release_acceptance.get(
                    "v3_5_runtime_authority_grant_allowed"
                )
                is True,
                "v3_6_advisory_runtime_pilot_observed": release_acceptance.get(
                    "v3_6_advisory_runtime_pilot_observed"
                )
                is True,
                "v3_6_advisory_runtime_pilot_valid": release_acceptance.get(
                    "v3_6_advisory_runtime_pilot_valid"
                )
                is True,
                "v3_6_advisory_side_effects_executed": release_acceptance.get(
                    "v3_6_advisory_side_effects_executed"
                )
                is True,
                "v3_6_production_mutation_executed": release_acceptance.get(
                    "v3_6_production_mutation_executed"
                )
                is True,
                "v4_0_limited_runtime_authority_gate_observed": release_acceptance.get(
                    "v4_0_limited_runtime_authority_gate_observed"
                )
                is True,
                "v4_0_limited_runtime_authority_gate_complete": release_acceptance.get(
                    "v4_0_limited_runtime_authority_gate_complete"
                )
                is True,
                "v4_0_limited_runtime_authority_granted": release_acceptance.get(
                    "v4_0_limited_runtime_authority_granted"
                )
                is True,
                "v4_0_status_label": release_acceptance.get("v4_0_status_label", "not_generated"),
                "v4_1_live_identity_evidence_gate_observed": release_acceptance.get(
                    "v4_1_live_identity_evidence_gate_observed"
                )
                is True,
                "v4_1_live_identity_evidence_gate_complete": release_acceptance.get(
                    "v4_1_live_identity_evidence_gate_complete"
                )
                is True,
                "v4_1_live_identity_authority_ready": release_acceptance.get(
                    "v4_1_live_identity_authority_ready"
                )
                is True,
                "v4_1_mfa_claim_observed": release_acceptance.get("v4_1_mfa_claim_observed") is True,
                "v4_2_live_approval_provider_gate_observed": release_acceptance.get(
                    "v4_2_live_approval_provider_gate_observed"
                )
                is True,
                "v4_2_live_approval_provider_gate_complete": release_acceptance.get(
                    "v4_2_live_approval_provider_gate_complete"
                )
                is True,
                "v4_2_live_approval_provider_ready": release_acceptance.get(
                    "v4_2_live_approval_provider_ready"
                )
                is True,
                "v4_2_ai_approval_allowed": release_acceptance.get("v4_2_ai_approval_allowed") is True,
                "v4_3_production_case_store_gate_observed": release_acceptance.get(
                    "v4_3_production_case_store_gate_observed"
                )
                is True,
                "v4_3_production_case_store_gate_complete": release_acceptance.get(
                    "v4_3_production_case_store_gate_complete"
                )
                is True,
                "v4_3_production_case_store_live_ready": release_acceptance.get(
                    "v4_3_production_case_store_live_ready"
                )
                is True,
                "v4_4_release_promotion_execution_gate_observed": release_acceptance.get(
                    "v4_4_release_promotion_execution_gate_observed"
                )
                is True,
                "v4_4_release_promotion_execution_gate_complete": release_acceptance.get(
                    "v4_4_release_promotion_execution_gate_complete"
                )
                is True,
                "v4_4_prod_deployment_executed": release_acceptance.get("v4_4_prod_deployment_executed") is True,
                "v5_0_governed_advisory_runtime_observed": release_acceptance.get(
                    "v5_0_governed_advisory_runtime_observed"
                )
                is True,
                "v5_0_governed_advisory_runtime_complete": release_acceptance.get(
                    "v5_0_governed_advisory_runtime_complete"
                )
                is True,
                "v5_0_runtime_recommendation_only": release_acceptance.get(
                    "v5_0_runtime_recommendation_only"
                )
                is True,
                "v5_0_side_effects_executed": release_acceptance.get("v5_0_side_effects_executed") is True,
                "v5_5_controlled_runtime_execution_gate_observed": release_acceptance.get(
                    "v5_5_controlled_runtime_execution_gate_observed"
                )
                is True,
                "v5_5_controlled_runtime_execution_gate_complete": release_acceptance.get(
                    "v5_5_controlled_runtime_execution_gate_complete"
                )
                is True,
                "v5_5_controlled_runtime_execution_authorized": release_acceptance.get(
                    "v5_5_controlled_runtime_execution_authorized"
                )
                is True,
                "v6_0_platform_hardening_assessment_observed": release_acceptance.get(
                    "v6_0_platform_hardening_assessment_observed"
                )
                is True,
                "v6_0_platform_hardening_assessment_complete": release_acceptance.get(
                    "v6_0_platform_hardening_assessment_complete"
                )
                is True,
                "v6_0_platform_production_ready": release_acceptance.get("v6_0_platform_production_ready")
                is True,
                "v6_0_hardening_control_count": release_acceptance.get("v6_0_hardening_control_count", 0),
                "v6_1_live_identity_authority_observed": release_acceptance.get(
                    "v6_1_live_identity_authority_observed"
                )
                is True,
                "v6_1_live_identity_authority_contract_complete": release_acceptance.get(
                    "v6_1_live_identity_authority_contract_complete"
                )
                is True,
                "v6_1_live_identity_authority_ready": release_acceptance.get(
                    "v6_1_live_identity_authority_ready"
                )
                is True,
                "v6_1_mfa_claim_observed": release_acceptance.get("v6_1_mfa_claim_observed") is True,
                "v6_2_live_decision_approval_provider_observed": release_acceptance.get(
                    "v6_2_live_decision_approval_provider_observed"
                )
                is True,
                "v6_2_live_decision_approval_provider_contract_complete": release_acceptance.get(
                    "v6_2_live_decision_approval_provider_contract_complete"
                )
                is True,
                "v6_2_live_decision_approval_provider_ready": release_acceptance.get(
                    "v6_2_live_decision_approval_provider_ready"
                )
                is True,
                "v6_2_ai_approval_allowed": release_acceptance.get("v6_2_ai_approval_allowed") is True,
                "v6_3_production_durable_case_store_observed": release_acceptance.get(
                    "v6_3_production_durable_case_store_observed"
                )
                is True,
                "v6_3_production_durable_case_store_contract_complete": release_acceptance.get(
                    "v6_3_production_durable_case_store_contract_complete"
                )
                is True,
                "v6_3_production_durable_case_store_ready": release_acceptance.get(
                    "v6_3_production_durable_case_store_ready"
                )
                is True,
                "v6_4_production_promotion_chain_observed": release_acceptance.get(
                    "v6_4_production_promotion_chain_observed"
                )
                is True,
                "v6_4_production_promotion_chain_contract_complete": release_acceptance.get(
                    "v6_4_production_promotion_chain_contract_complete"
                )
                is True,
                "v6_4_production_promotion_ready": release_acceptance.get("v6_4_production_promotion_ready")
                is True,
                "v7_0_controlled_runtime_pilot_observed": release_acceptance.get(
                    "v7_0_controlled_runtime_pilot_observed"
                )
                is True,
                "v7_0_controlled_runtime_pilot_admission_complete": release_acceptance.get(
                    "v7_0_controlled_runtime_pilot_admission_complete"
                )
                is True,
                "v7_0_controlled_runtime_pilot_authorized": release_acceptance.get(
                    "v7_0_controlled_runtime_pilot_authorized"
                )
                is True,
                "v7_5_marketplace_runtime_governance_observed": release_acceptance.get(
                    "v7_5_marketplace_runtime_governance_observed"
                )
                is True,
                "v7_5_marketplace_runtime_governance_complete": release_acceptance.get(
                    "v7_5_marketplace_runtime_governance_complete"
                )
                is True,
                "v7_5_marketplace_runtime_invocation_authorized": release_acceptance.get(
                    "v7_5_marketplace_runtime_invocation_authorized"
                )
                is True,
                "v7_5_unrestricted_marketplace_execution_allowed": release_acceptance.get(
                    "v7_5_unrestricted_marketplace_execution_allowed"
                )
                is True,
                "v8_0_shared_context_runtime_governance_observed": release_acceptance.get(
                    "v8_0_shared_context_runtime_governance_observed"
                )
                is True,
                "v8_0_shared_context_runtime_governance_complete": release_acceptance.get(
                    "v8_0_shared_context_runtime_governance_complete"
                )
                is True,
                "v8_0_runtime_context_exchange_authorized": release_acceptance.get(
                    "v8_0_runtime_context_exchange_authorized"
                )
                is True,
                "v8_0_direct_database_access_allowed": release_acceptance.get(
                    "v8_0_direct_database_access_allowed"
                )
                is True,
                "v9_0_production_authority_readiness_review_observed": release_acceptance.get(
                    "v9_0_production_authority_readiness_review_observed"
                )
                is True,
                "v9_0_production_authority_readiness_review_complete": release_acceptance.get(
                    "v9_0_production_authority_readiness_review_complete"
                )
                is True,
                "v9_0_production_decision_authority_granted": release_acceptance.get(
                    "v9_0_production_decision_authority_granted"
                )
                is True,
                "v10_0_completion_plan_execution_observed": release_acceptance.get(
                    "v10_0_completion_plan_execution_observed"
                )
                is True,
                "v10_0_autopilot_execution_review_complete": release_acceptance.get(
                    "v10_0_autopilot_execution_review_complete"
                )
                is True,
                "v10_0_reviewed_step_count": release_acceptance.get("v10_0_reviewed_step_count", 0),
                "v10_0_evidence_gate_complete_count": release_acceptance.get(
                    "v10_0_evidence_gate_complete_count", 0
                ),
                "v10_0_live_completion_achieved_count": release_acceptance.get(
                    "v10_0_live_completion_achieved_count", 0
                ),
                "v10_0_blocked_live_completion_count": release_acceptance.get(
                    "v10_0_blocked_live_completion_count", 0
                ),
                "v10_0_product_vision_alignment_valid": release_acceptance.get(
                    "v10_0_product_vision_alignment_valid"
                )
                is True,
                "v10_0_ai_policy_boundary_preserved": release_acceptance.get(
                    "v10_0_ai_policy_boundary_preserved"
                )
                is True,
                "v10_0_runtime_authority_grant_blocked": release_acceptance.get(
                    "v10_0_runtime_authority_grant_blocked"
                )
                is True,
                "v10_0_production_decision_authority_blocked": release_acceptance.get(
                    "v10_0_production_decision_authority_blocked"
                )
                is True,
                "v11_0_api_first_platform_foundation_observed": bool(v11_release_acceptance),
                "v11_0_platform_foundation_valid": v11_release_acceptance.get("v11_0_platform_foundation_valid")
                is True,
                "v11_0_api_architecture_contract_valid": v11_release_acceptance.get(
                    "v11_0_api_architecture_contract_valid"
                )
                is True,
                "v11_0_rest_authoritative": v11_release_acceptance.get("v11_0_rest_authoritative") is True,
                "v11_0_websocket_notification_only": v11_release_acceptance.get(
                    "v11_0_websocket_notification_only"
                )
                is True,
                "v11_0_event_recovery_rest_twin_declared": v11_release_acceptance.get(
                    "v11_0_event_recovery_rest_twin_declared"
                )
                is True,
                "v11_0_topology_flexible": v11_release_acceptance.get("v11_0_topology_flexible") is True,
                "v11_0_forced_microservice_topology": v11_release_acceptance.get(
                    "v11_0_forced_microservice_topology"
                )
                is True,
                "v11_0_product_pack_foundation_valid": v11_release_acceptance.get(
                    "v11_0_product_pack_foundation_valid"
                )
                is True,
                "v11_0_product_pack_count": v11_release_acceptance.get("v11_0_product_pack_count", 0),
                "v11_0_ml_product_pack_observed": v11_release_acceptance.get("v11_0_ml_product_pack_observed")
                is True,
                "v11_0_edi_product_pack_observed": v11_release_acceptance.get("v11_0_edi_product_pack_observed")
                is True,
                "v11_0_shared_service_certification_valid": v11_release_acceptance.get(
                    "v11_0_shared_service_certification_valid"
                )
                is True,
                "v11_0_service_certification_evidence_complete_count": v11_release_acceptance.get(
                    "v11_0_service_certification_evidence_complete_count", 0
                ),
                "v11_0_ml_shared_capability_inventory_valid": v11_release_acceptance.get(
                    "v11_0_ml_shared_capability_inventory_valid"
                )
                is True,
                "v11_0_ml_capability_count": v11_release_acceptance.get("v11_0_ml_capability_count", 0),
                "v11_0_algo_engine_observe_first": v11_release_acceptance.get("v11_0_algo_engine_observe_first")
                is True,
                "v11_0_adapter_evidence_contract_valid": v11_release_acceptance.get(
                    "v11_0_adapter_evidence_contract_valid"
                )
                is True,
                "v11_0_governance_store_contract_valid": v11_release_acceptance.get(
                    "v11_0_governance_store_contract_valid"
                )
                is True,
                "v11_0_edi_universal_governance_store": v11_release_acceptance.get(
                    "v11_0_edi_universal_governance_store"
                )
                is True,
                "v11_0_direct_database_access_allowed": v11_release_acceptance.get(
                    "v11_0_direct_database_access_allowed"
                )
                is True,
                "v11_0_runtime_authority_blocked_model_valid": v11_release_acceptance.get(
                    "v11_0_runtime_authority_blocked_model_valid"
                )
                is True,
                "v11_0_runtime_authority_blocked": v11_release_acceptance.get("v11_0_runtime_authority_blocked")
                is True,
                "v11_0_foundation_gate_complete_count": v11_release_acceptance.get(
                    "v11_0_foundation_gate_complete_count", 0
                ),
                "v11_0_foundation_gate_count": v11_release_acceptance.get("v11_0_foundation_gate_count", 0),
                "v12_0_shared_capability_certification_states_valid": release_acceptance.get(
                    "v12_0_shared_capability_certification_states_valid"
                )
                is True,
                "v12_0_certified_capability_count": release_acceptance.get("v12_0_certified_capability_count", 0),
                "v12_0_runtime_invocation_allowed_count": release_acceptance.get(
                    "v12_0_runtime_invocation_allowed_count", 0
                ),
                "v13_0_product_pack_contracts_valid": release_acceptance.get(
                    "v13_0_product_pack_contracts_valid"
                )
                is True,
                "v13_0_cross_product_database_access_allowed": release_acceptance.get(
                    "v13_0_cross_product_database_access_allowed"
                )
                is True,
                "v13_0_runtime_authority_granted_count": release_acceptance.get(
                    "v13_0_runtime_authority_granted_count", 0
                ),
                "v14_0_rest_api_contracts_valid": release_acceptance.get("v14_0_rest_api_contracts_valid")
                is True,
                "v14_0_rest_authoritative": release_acceptance.get("v14_0_rest_authoritative") is True,
                "v14_0_runtime_authority_default_blocked": release_acceptance.get(
                    "v14_0_runtime_authority_default_blocked"
                )
                is True,
                "v15_0_event_recovery_contract_valid": release_acceptance.get(
                    "v15_0_event_recovery_contract_valid"
                )
                is True,
                "v15_0_websocket_authoritative": release_acceptance.get("v15_0_websocket_authoritative") is True,
                "v15_0_events_mutate_business_state": release_acceptance.get(
                    "v15_0_events_mutate_business_state"
                )
                is True,
                "v15_0_rest_recovery_required": release_acceptance.get("v15_0_rest_recovery_required") is True,
                "v15_0_api_foundation_valid": release_acceptance.get("v15_0_api_foundation_valid") is True,
                "v15_0_foundation_gate_complete_count": release_acceptance.get(
                    "v15_0_foundation_gate_complete_count", 0
                ),
                "v15_0_foundation_gate_count": release_acceptance.get("v15_0_foundation_gate_count", 0),
                "v16_0_certification_evidence_packs_valid": release_acceptance.get(
                    "v16_0_certification_evidence_packs_valid"
                )
                is True,
                "v16_0_certified_service_count": release_acceptance.get("v16_0_certified_service_count", 0),
                "v16_0_runtime_invocation_allowed_count": release_acceptance.get(
                    "v16_0_runtime_invocation_allowed_count", 0
                ),
                "v17_0_product_pack_admission_valid": release_acceptance.get(
                    "v17_0_product_pack_admission_valid"
                )
                is True,
                "v17_0_direct_database_access_allowed": release_acceptance.get(
                    "v17_0_direct_database_access_allowed"
                )
                is True,
                "v17_0_hidden_shared_state_allowed": release_acceptance.get(
                    "v17_0_hidden_shared_state_allowed"
                )
                is True,
                "v17_0_runtime_authority_granted_count": release_acceptance.get(
                    "v17_0_runtime_authority_granted_count", 0
                ),
                "v18_0_openapi_skeleton_valid": release_acceptance.get("v18_0_openapi_skeleton_valid") is True,
                "v18_0_rest_authoritative": release_acceptance.get("v18_0_rest_authoritative") is True,
                "v18_0_runtime_authority_blocked_response": release_acceptance.get(
                    "v18_0_runtime_authority_blocked_response"
                )
                is True,
                "v19_0_event_recovery_fixtures_valid": release_acceptance.get(
                    "v19_0_event_recovery_fixtures_valid"
                )
                is True,
                "v19_0_websocket_authoritative": release_acceptance.get("v19_0_websocket_authoritative")
                is True,
                "v19_0_events_mutate_business_state": release_acceptance.get(
                    "v19_0_events_mutate_business_state"
                )
                is True,
                "v19_0_all_events_recoverable": release_acceptance.get("v19_0_all_events_recoverable") is True,
                "v20_0_governance_store_logical_schema_valid": release_acceptance.get(
                    "v20_0_governance_store_logical_schema_valid"
                )
                is True,
                "v20_0_storage_backend_selected": release_acceptance.get("v20_0_storage_backend_selected")
                is True,
                "v20_0_direct_database_access_allowed": release_acceptance.get(
                    "v20_0_direct_database_access_allowed"
                )
                is True,
                "v20_0_append_only_required": release_acceptance.get("v20_0_append_only_required") is True,
                "v20_0_architecture_closure_valid": release_acceptance.get("v20_0_architecture_closure_valid")
                is True,
                "v20_0_closure_gate_complete_count": release_acceptance.get(
                    "v20_0_closure_gate_complete_count", 0
                ),
                "v20_0_closure_gate_count": release_acceptance.get("v20_0_closure_gate_count", 0),
                "v21_0_canonical_openapi_contract_valid": release_acceptance.get(
                    "v21_0_canonical_openapi_contract_valid"
                )
                is True,
                "v21_0_rest_authoritative": release_acceptance.get("v21_0_rest_authoritative") is True,
                "v21_0_all_commands_require_idempotency": release_acceptance.get(
                    "v21_0_all_commands_require_idempotency"
                )
                is True,
                "v21_0_all_commands_require_correlation": release_acceptance.get(
                    "v21_0_all_commands_require_correlation"
                )
                is True,
                "v21_0_runtime_authority_blocked_response": release_acceptance.get(
                    "v21_0_runtime_authority_blocked_response"
                )
                is True,
                "v21_0_websocket_authoritative": release_acceptance.get("v21_0_websocket_authoritative") is True,
                "v22_0_product_pack_contract_kit_valid": release_acceptance.get(
                    "v22_0_product_pack_contract_kit_valid"
                )
                is True,
                "v22_0_template_count": release_acceptance.get("v22_0_template_count", 0),
                "v22_0_direct_database_access_allowed": release_acceptance.get(
                    "v22_0_direct_database_access_allowed"
                )
                is True,
                "v22_0_hidden_shared_state_allowed": release_acceptance.get(
                    "v22_0_hidden_shared_state_allowed"
                )
                is True,
                "v22_0_runtime_authority_granted_count": release_acceptance.get(
                    "v22_0_runtime_authority_granted_count", 0
                ),
                "v23_0_adapter_evidence_contract_kit_valid": release_acceptance.get(
                    "v23_0_adapter_evidence_contract_kit_valid"
                )
                is True,
                "v23_0_adapter_contract_count": release_acceptance.get("v23_0_adapter_contract_count", 0),
                "v23_0_live_invocation_allowed_count": release_acceptance.get(
                    "v23_0_live_invocation_allowed_count", 0
                ),
                "v23_0_sample_evidence_present": release_acceptance.get("v23_0_sample_evidence_present")
                is True,
                "v24_0_governance_store_logical_api_valid": release_acceptance.get(
                    "v24_0_governance_store_logical_api_valid"
                )
                is True,
                "v24_0_storage_backend_selected": release_acceptance.get("v24_0_storage_backend_selected")
                is True,
                "v24_0_direct_database_access_allowed": release_acceptance.get(
                    "v24_0_direct_database_access_allowed"
                )
                is True,
                "v24_0_delete_operation_allowed": release_acceptance.get("v24_0_delete_operation_allowed")
                is True,
                "v24_0_projection_rebuild_required": release_acceptance.get("v24_0_projection_rebuild_required")
                is True,
                "v25_0_event_recovery_contract_v2_valid": release_acceptance.get(
                    "v25_0_event_recovery_contract_v2_valid"
                )
                is True,
                "v25_0_event_type_count": release_acceptance.get("v25_0_event_type_count", 0),
                "v25_0_websocket_authoritative": release_acceptance.get("v25_0_websocket_authoritative")
                is True,
                "v25_0_events_mutate_business_state": release_acceptance.get(
                    "v25_0_events_mutate_business_state"
                )
                is True,
                "v25_0_rest_event_log_required": release_acceptance.get("v25_0_rest_event_log_required")
                is True,
                "v25_0_reconnect_recovery_required": release_acceptance.get(
                    "v25_0_reconnect_recovery_required"
                )
                is True,
                "v25_0_contract_closure_valid": release_acceptance.get("v25_0_contract_closure_valid") is True,
                "v25_0_closure_gate_complete_count": release_acceptance.get(
                    "v25_0_closure_gate_complete_count", 0
                ),
                "v25_0_closure_gate_count": release_acceptance.get("v25_0_closure_gate_count", 0),
                "v26_0_certification_workflow_valid": release_acceptance.get(
                    "v26_0_certification_workflow_valid"
                )
                is True,
                "v26_0_certified_count": release_acceptance.get("v26_0_certified_count", 0),
                "v26_0_runtime_invocation_allowed_count": release_acceptance.get(
                    "v26_0_runtime_invocation_allowed_count", 0
                ),
                "v26_0_evidence_complete_count": release_acceptance.get("v26_0_evidence_complete_count", 0),
                "v27_0_runtime_authority_gate_contract_valid": release_acceptance.get(
                    "v27_0_runtime_authority_gate_contract_valid"
                )
                is True,
                "v27_0_runtime_authority_granted": release_acceptance.get("v27_0_runtime_authority_granted")
                is True,
                "v27_0_negative_fixtures_block_authority": release_acceptance.get(
                    "v27_0_negative_fixtures_block_authority"
                )
                is True,
                "v27_0_required_live_evidence_count": release_acceptance.get(
                    "v27_0_required_live_evidence_count", 0
                ),
                "v28_0_cost_usage_evidence_contract_valid": release_acceptance.get(
                    "v28_0_cost_usage_evidence_contract_valid"
                )
                is True,
                "v28_0_billing_integration_enabled": release_acceptance.get("v28_0_billing_integration_enabled")
                is True,
                "v28_0_usage_record_type_count": release_acceptance.get("v28_0_usage_record_type_count", 0),
                "v28_0_live_invocation_observed_count": release_acceptance.get(
                    "v28_0_live_invocation_observed_count", 0
                ),
                "v29_0_semantic_projection_contract_valid": release_acceptance.get(
                    "v29_0_semantic_projection_contract_valid"
                )
                is True,
                "v29_0_direct_database_access_allowed": release_acceptance.get(
                    "v29_0_direct_database_access_allowed"
                )
                is True,
                "v29_0_hidden_shared_state_allowed": release_acceptance.get(
                    "v29_0_hidden_shared_state_allowed"
                )
                is True,
                "v29_0_runtime_context_exchange_authorized": release_acceptance.get(
                    "v29_0_runtime_context_exchange_authorized"
                )
                is True,
                "v29_0_all_projections_require_approval": release_acceptance.get(
                    "v29_0_all_projections_require_approval"
                )
                is True,
                "v29_0_all_projections_have_policy_evidence": release_acceptance.get(
                    "v29_0_all_projections_have_policy_evidence"
                )
                is True,
                "v30_0_product_pack_developer_kit_valid": release_acceptance.get(
                    "v30_0_product_pack_developer_kit_valid"
                )
                is True,
                "v30_0_example_product_count": release_acceptance.get("v30_0_example_product_count", 0),
                "v30_0_runtime_authority_granted_count": release_acceptance.get(
                    "v30_0_runtime_authority_granted_count", 0
                ),
                "v30_0_direct_database_access_allowed": release_acceptance.get(
                    "v30_0_direct_database_access_allowed"
                )
                is True,
                "v30_0_platform_operating_model_closure_valid": release_acceptance.get(
                    "v30_0_platform_operating_model_closure_valid"
                )
                is True,
                "v30_0_closure_gate_complete_count": release_acceptance.get(
                    "v30_0_closure_gate_complete_count", 0
                ),
                "v30_0_closure_gate_count": release_acceptance.get("v30_0_closure_gate_count", 0),
                "v31_0_compatibility_versioning_valid": release_acceptance.get(
                    "v31_0_compatibility_versioning_valid"
                )
                is True,
                "v31_0_versioned_contract_type_count": release_acceptance.get(
                    "v31_0_versioned_contract_type_count", 0
                ),
                "v31_0_breaking_change_requires_major": release_acceptance.get(
                    "v31_0_breaking_change_requires_major"
                )
                is True,
                "v31_0_deprecated_requires_replacement": release_acceptance.get(
                    "v31_0_deprecated_requires_replacement"
                )
                is True,
                "v32_0_policy_test_pack_framework_valid": release_acceptance.get(
                    "v32_0_policy_test_pack_framework_valid"
                )
                is True,
                "v32_0_fixture_count": release_acceptance.get("v32_0_fixture_count", 0),
                "v32_0_deterministic_policy_first": release_acceptance.get(
                    "v32_0_deterministic_policy_first"
                )
                is True,
                "v32_0_ai_policy_override_allowed": release_acceptance.get(
                    "v32_0_ai_policy_override_allowed"
                )
                is True,
                "v32_0_required_outcomes_covered": release_acceptance.get(
                    "v32_0_required_outcomes_covered"
                )
                is True,
                "v33_0_product_pack_cli_scaffold_valid": release_acceptance.get(
                    "v33_0_product_pack_cli_scaffold_valid"
                )
                is True,
                "v33_0_command_count": release_acceptance.get("v33_0_command_count", 0),
                "v33_0_no_code_builder": release_acceptance.get("v33_0_no_code_builder") is True,
                "v33_0_runtime_authority_default": release_acceptance.get("v33_0_runtime_authority_default"),
                "v33_0_direct_database_access_allowed": release_acceptance.get(
                    "v33_0_direct_database_access_allowed"
                )
                is True,
                "v33_0_runtime_authority_creating_command_count": release_acceptance.get(
                    "v33_0_runtime_authority_creating_command_count", 0
                ),
                "v34_0_case_evidence_query_contract_valid": release_acceptance.get(
                    "v34_0_case_evidence_query_contract_valid"
                )
                is True,
                "v34_0_query_resource_count": release_acceptance.get("v34_0_query_resource_count", 0),
                "v34_0_rest_authoritative": release_acceptance.get("v34_0_rest_authoritative") is True,
                "v34_0_production_backend_selected": release_acceptance.get(
                    "v34_0_production_backend_selected"
                )
                is True,
                "v34_0_direct_database_access_allowed": release_acceptance.get(
                    "v34_0_direct_database_access_allowed"
                )
                is True,
                "v35_0_governance_dashboard_data_contract_valid": release_acceptance.get(
                    "v35_0_governance_dashboard_data_contract_valid"
                )
                is True,
                "v35_0_dashboard_section_count": release_acceptance.get("v35_0_dashboard_section_count", 0),
                "v35_0_derived_from_rest_evidence": release_acceptance.get(
                    "v35_0_derived_from_rest_evidence"
                )
                is True,
                "v35_0_dashboard_is_source_of_truth": release_acceptance.get(
                    "v35_0_dashboard_is_source_of_truth"
                )
                is True,
                "v35_0_websocket_authoritative": release_acceptance.get("v35_0_websocket_authoritative")
                is True,
                "v35_0_blocked_claims_visible": release_acceptance.get("v35_0_blocked_claims_visible")
                is True,
                "v35_0_usability_governance_closure_valid": release_acceptance.get(
                    "v35_0_usability_governance_closure_valid"
                )
                is True,
                "v35_0_closure_gate_complete_count": release_acceptance.get(
                    "v35_0_closure_gate_complete_count", 0
                ),
                "v35_0_closure_gate_count": release_acceptance.get("v35_0_closure_gate_count", 0),
                "v36_0_product_pack_authoring_ux_valid": release_acceptance.get(
                    "v36_0_product_pack_authoring_ux_valid"
                )
                is True,
                "v36_0_authoring_state_count": release_acceptance.get("v36_0_authoring_state_count", 0),
                "v36_0_required_panel_count": release_acceptance.get("v36_0_required_panel_count", 0),
                "v36_0_all_transitions_require_rest": release_acceptance.get(
                    "v36_0_all_transitions_require_rest"
                )
                is True,
                "v36_0_rest_authoritative": release_acceptance.get("v36_0_rest_authoritative") is True,
                "v36_0_websocket_authoritative": release_acceptance.get("v36_0_websocket_authoritative")
                is True,
                "v36_0_broad_no_code_builder": release_acceptance.get("v36_0_broad_no_code_builder")
                is True,
                "v36_0_direct_database_access_allowed": release_acceptance.get(
                    "v36_0_direct_database_access_allowed"
                )
                is True,
                "v37_0_governance_review_queue_valid": release_acceptance.get(
                    "v37_0_governance_review_queue_valid"
                )
                is True,
                "v37_0_filter_count": release_acceptance.get("v37_0_filter_count", 0),
                "v37_0_required_evidence_count": release_acceptance.get("v37_0_required_evidence_count", 0),
                "v37_0_reviewer_action_count": release_acceptance.get("v37_0_reviewer_action_count", 0),
                "v37_0_solo_maintainer_exception_visible": release_acceptance.get(
                    "v37_0_solo_maintainer_exception_visible"
                )
                is True,
                "v37_0_approval_automation_allowed": release_acceptance.get(
                    "v37_0_approval_automation_allowed"
                )
                is True,
                "v38_0_capability_lineage_explorer_valid": release_acceptance.get(
                    "v38_0_capability_lineage_explorer_valid"
                )
                is True,
                "v38_0_lineage_resource_count": release_acceptance.get("v38_0_lineage_resource_count", 0),
                "v38_0_version_trace_example_count": release_acceptance.get(
                    "v38_0_version_trace_example_count", 0
                ),
                "v38_0_capability_version_lineage_required": release_acceptance.get(
                    "v38_0_capability_version_lineage_required"
                )
                is True,
                "v38_0_direct_runtime_invocation_allowed": release_acceptance.get(
                    "v38_0_direct_runtime_invocation_allowed"
                )
                is True,
                "v38_0_all_traces_have_evidence": release_acceptance.get("v38_0_all_traces_have_evidence")
                is True,
                "v39_0_replay_workspace_valid": release_acceptance.get("v39_0_replay_workspace_valid")
                is True,
                "v39_0_replay_input_count": release_acceptance.get("v39_0_replay_input_count", 0),
                "v39_0_replay_output_count": release_acceptance.get("v39_0_replay_output_count", 0),
                "v39_0_rest_recovery_endpoint_count": release_acceptance.get(
                    "v39_0_rest_recovery_endpoint_count", 0
                ),
                "v39_0_drift_comparison_required": release_acceptance.get("v39_0_drift_comparison_required")
                is True,
                "v39_0_evidence_references_required": release_acceptance.get(
                    "v39_0_evidence_references_required"
                )
                is True,
                "v39_0_websocket_authoritative": release_acceptance.get("v39_0_websocket_authoritative")
                is True,
                "v39_0_runtime_execution_allowed": release_acceptance.get("v39_0_runtime_execution_allowed")
                is True,
                "v39_0_side_effects_allowed": release_acceptance.get("v39_0_side_effects_allowed") is True,
                "v40_0_usability_acceptance_pack_valid": release_acceptance.get(
                    "v40_0_usability_acceptance_pack_valid"
                )
                is True,
                "v40_0_usability_surface_count": release_acceptance.get("v40_0_usability_surface_count", 0),
                "v40_0_rest_authoritative": release_acceptance.get("v40_0_rest_authoritative") is True,
                "v40_0_websocket_authoritative": release_acceptance.get("v40_0_websocket_authoritative")
                is True,
                "v40_0_evidence_backed": release_acceptance.get("v40_0_evidence_backed") is True,
                "v40_0_runtime_remains_blocked": release_acceptance.get("v40_0_runtime_remains_blocked")
                is True,
                "v40_0_closure_gate_complete_count": release_acceptance.get(
                    "v40_0_closure_gate_complete_count", 0
                ),
                "v40_0_closure_gate_count": release_acceptance.get("v40_0_closure_gate_count", 0),
                "computed_policy_engine_observed": release_acceptance.get("computed_policy_engine_observed") is True,
                "computed_policy_engine_result": release_acceptance.get("computed_policy_engine_result"),
                "policy_engine_valid": release_acceptance.get("policy_engine_valid") is True,
                "policy_engine_supported_rule_type_count": release_acceptance.get(
                    "policy_engine_supported_rule_type_count", 0
                ),
                "policy_engine_active_policy_count": release_acceptance.get("policy_engine_active_policy_count", 0),
                "policy_engine_revoked_policy_count": release_acceptance.get("policy_engine_revoked_policy_count", 0),
                "policy_engine_deny_precedence_enforced": release_acceptance.get(
                    "policy_engine_deny_precedence_enforced"
                )
                is True,
                "policy_engine_escalate_outcome_supported": release_acceptance.get(
                    "policy_engine_escalate_outcome_supported"
                )
                is True,
                "policy_engine_compatibility_valid": release_acceptance.get(
                    "policy_engine_compatibility_valid"
                )
                is True,
                "product_review_surface_observed": release_acceptance.get("product_review_surface_observed") is True,
                "product_review_surface_count": release_acceptance.get("product_review_surface_count", 0),
                "runtime_readiness_assessment_observed": release_acceptance.get(
                    "runtime_readiness_assessment_observed"
                )
                is True,
                "runtime_readiness_percent": release_acceptance.get("runtime_readiness_percent", 0.0),
                "production_decision_authority_percent": release_acceptance.get(
                    "production_decision_authority_percent", 0.0
                ),
                "main_update_bypass_observed": main_update_bypass_observed,
                "main_update_bypass_reason": target.get("main_update_bypass_reason", ""),
                "main_update_bypass_governed": main_update_bypass_governed,
                "main_update_bypass_governance_evidence": target.get("main_update_bypass_governance_evidence", ""),
                "validation_passed": validation_passed,
                "validation_passed_count": validation.get("passed_count", 0),
                "validation_record_count": validation.get("record_count", 0),
                "trust_loop_run_id": trust_loop.get("run_id"),
                "trust_loop_complete": trust_loop_complete,
                "runtime_execution_requested": trust_loop.get("runtime_execution_requested"),
                "runtime_integration_authorized": acceptance.get("runtime_integration_authorized"),
                "production_decision_execution_authorized": acceptance.get("production_decision_execution_authorized"),
                "state": "local_pre_runtime_trust_loop_observed"
                if release_governance_clean
                else "pre_runtime_evidence_observed_release_governance_gaps"
                if record_complete
                else "target_evidence_incomplete",
            }
        )
    complete_count = len(
        [
            record
            for record in records
            if record["state"]
            in {
                "local_pre_runtime_trust_loop_observed",
                "pre_runtime_evidence_observed_release_governance_gaps",
            }
        ]
    )
    clean_governance_count = len([record for record in records if record.get("release_governance_clean") is True])
    return {
        "generated_at": generated_at,
        "schema_version": config.get("schema_version"),
        "target_count": len(records),
        "complete_target_count": complete_count,
        "target_repo_evidence_percent": round(complete_count / len(records) * 100, 1) if records else 0.0,
        "target_repo_governance_clean_percent": round(clean_governance_count / len(records) * 100, 1)
        if records
        else 0.0,
        "runtime_authority_granted": False,
        "evidence_preserved_for_drift_check": False,
        "records": records,
    }


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


def v0_2_backlog_payload(root: Path, generated_at: str) -> dict[str, Any]:
    backlog = dip_v0_2_backlog(root)
    slices = backlog.get("slices", [])
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
    planned_count = len([item for item in slices if item.get("status") == "planned"])
    strategy = backlog.get("parallelization_strategy", {})
    return {
        "generated_at": generated_at,
        "target_id": backlog.get("target_id"),
        "milestone": backlog.get("milestone"),
        "source_boundary": backlog.get("source_boundary"),
        "runtime_execution_allowed": bool(backlog.get("runtime_execution_allowed", False)),
        "release_authority_allowed": bool(backlog.get("release_authority_allowed", False)),
        "slice_count": len(slices),
        "defined_slice_count": len(defined_records),
        "planned_slice_count": planned_count,
        "completed_slice_count": len([item for item in slices if item.get("status") == "completed"]),
        "defined_percent": round(len(defined_records) / len(slices) * 100, 1) if slices else 0.0,
        "runtime_mutating_slice_count": len(runtime_mutating),
        "parallelization_groups": groups,
        "safe_parallel_groups": strategy.get("safe_parallel_groups", []),
        "serialized_groups": strategy.get("serialized_groups", []),
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
    v0_2_backlog = payloads["v0.2-backlog"]
    evidence = payloads["implementation-evidence"]
    autopilot = payloads["autopilot-lanes"]
    target_evidence = payloads["target-evidence"]
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
    v0_1_complete = policy_ready and readiness["implementation_evidence_percent"] == 100.0
    target_records = target_evidence.get("records", [])
    release_artifact_gaps = any(record.get("github_release_artifact_observed") is not True for record in target_records)
    release_governance_gaps = any(record.get("release_governance_clean") is not True for record in target_records)
    v0_3_complete = any(
        record.get("computed_policy_preflight_observed") is True
        and record.get("computed_decision_diff_observed") is True
        and int(record.get("computed_decision_diff_changed_outcomes", 0) or 0) > 0
        and record.get("runtime_execution_requested") is False
        for record in target_records
    )
    v0_4_complete = any(
        record.get("computed_simulation_observed") is True
        and int(record.get("computed_simulation_case_count", 0) or 0) >= 9
        and int(record.get("computed_simulation_domain_count", 0) or 0) >= 2
        and int(record.get("computed_simulation_decision_shape_count", 0) or 0) >= 2
        and record.get("computed_decision_diff_observed") is True
        and record.get("runtime_execution_requested") is False
        for record in target_records
    )
    v0_5_complete = any(
        record.get("durable_case_manifest_observed") is True
        and record.get("durable_case_manifest_valid") is True
        and record.get("append_only_chain_valid") is True
        and record.get("case_mutation_detected") is False
        and record.get("replay_from_manifest_observed") is True
        and record.get("replay_manifest_valid") is True
        and record.get("approval_bound_to_manifest") is True
        and record.get("approval_role_binding_valid") is True
        and record.get("runtime_execution_requested") is False
        for record in target_records
    )
    v0_6_complete = any(
        record.get("approval_authority_evaluated") is True
        and record.get("approval_authority_valid") is True
        and record.get("approval_identity_active") is True
        and record.get("approval_identity_not_expired") is True
        and record.get("approval_mfa_satisfied") is True
        and record.get("approval_decision_scope_authorized") is True
        and record.get("ai_self_approval_blocked") is True
        and record.get("external_identity_provider_observed") is False
        and record.get("runtime_execution_requested") is False
        for record in target_records
    )
    v0_7_complete = any(
        record.get("repository_governance_policy_observed") is True
        and record.get("admin_enforcement_required") is True
        and int(record.get("required_status_check_count", 0) or 0) >= 1
        and record.get("break_glass_policy_defined") is True
        and record.get("admin_enforcement_observed") is True
        and record.get("release_governance_clean") is True
        and record.get("runtime_execution_requested") is False
        for record in target_records
    )
    v0_8_complete = any(
        record.get("release_lifecycle_policy_observed") is True
        and record.get("release_lifecycle_valid") is True
        and record.get("independent_release_approval_required") is True
        and record.get("codeowner_review_required") is True
        and record.get("conversation_resolution_required") is True
        and record.get("rollback_criteria_defined") is True
        and record.get("runtime_execution_requested") is False
        for record in target_records
    )
    v0_9_complete = any(
        record.get("external_identity_contract_observed") is True
        and record.get("external_identity_contract_valid") is True
        and record.get("live_external_identity_provider_authenticated") is False
        and record.get("runtime_execution_requested") is False
        for record in target_records
    )
    v1_0_complete = any(
        record.get("durable_evidence_store_policy_observed") is True
        and record.get("durable_store_contract_valid") is True
        and record.get("production_storage_backend_observed") is False
        and record.get("runtime_execution_requested") is False
        for record in target_records
    )
    v1_1_complete = any(
        record.get("required_status_checks_observed") is True
        and int(record.get("required_approving_review_count_observed", 0) or 0) >= 1
        and record.get("codeowner_review_required_observed") is True
        and record.get("conversation_resolution_required_observed") is True
        and record.get("release_governance_clean") is True
        and record.get("runtime_execution_requested") is False
        for record in target_records
    )
    v1_2_complete = any(
        record.get("product_review_surface_observed") is True
        and int(record.get("product_review_surface_count", 0) or 0) >= 8
        and record.get("runtime_execution_requested") is False
        for record in target_records
    )
    v1_3_complete = any(
        record.get("computed_simulation_observed") is True
        and int(record.get("computed_simulation_case_count", 0) or 0) >= 13
        and int(record.get("computed_simulation_domain_count", 0) or 0) >= 3
        and int(record.get("computed_simulation_decision_shape_count", 0) or 0) >= 3
        and record.get("runtime_execution_requested") is False
        for record in target_records
    )
    v1_4_complete = any(
        record.get("capability_governance_observed") is True
        and record.get("capability_governance_valid") is True
        and int(record.get("resolved_capability_count", 0) or 0) >= 3
        and record.get("runtime_execution_requested") is False
        for record in target_records
    )
    v1_5_complete = any(
        record.get("shared_context_contract_observed") is True
        and record.get("shared_context_contract_valid") is True
        and record.get("runtime_execution_requested") is False
        and record.get("runtime_integration_authorized") is False
        for record in target_records
    )
    v2_0_complete = any(
        record.get("runtime_readiness_assessment_observed") is True
        and float(record.get("runtime_readiness_percent", 100.0) or 0.0) == 0.0
        and float(record.get("production_decision_authority_percent", 100.0) or 0.0) == 0.0
        and record.get("runtime_execution_requested") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v2_1_complete = any(
        record.get("solo_maintainer_exception_observed") is True
        and record.get("solo_maintainer_exception_valid") is True
        and record.get("solo_maintainer_constraint") is True
        and record.get("independent_human_review_available") is False
        and record.get("independent_human_review_observed") is False
        and record.get("review_relaxation_allowed") is True
        and record.get("review_gate_restoration_required") is True
        and record.get("schema_stability_observed") is True
        and record.get("schema_stability_valid") is True
        and int(record.get("frozen_contract_count", 0) or 0) >= 16
        and int(record.get("negative_fixture_count", 0) or 0) >= 2
        and record.get("negative_fixtures_valid") is True
        and record.get("runtime_execution_requested") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v2_2_complete = any(
        record.get("external_approval_boundary_observed") is True
        and record.get("external_approval_boundary_valid") is True
        and record.get("live_external_approval_system_observed") is False
        and record.get("decision_approval_required") is True
        and record.get("decision_approval_separate_from_code_merge") is True
        and record.get("github_code_review_is_decision_approval") is False
        and record.get("solo_maintainer_exception_is_decision_approval") is False
        and record.get("external_approval_required_evidence_complete") is True
        and record.get("external_approval_admission_controls_complete") is True
        and record.get("runtime_execution_requested") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v2_3_complete = any(
        record.get("durable_case_store_adapter_observed") is True
        and record.get("durable_case_store_adapter_valid") is True
        and record.get("adapter_production_storage_backend_observed") is False
        and record.get("adapter_append_only_writes_required") is True
        and record.get("adapter_content_addressed_records_required") is True
        and record.get("adapter_delete_denied_required") is True
        and record.get("adapter_mutation_detection_required") is True
        and record.get("adapter_replay_export_required") is True
        and record.get("adapter_audit_export_required") is True
        and record.get("adapter_retention_policy_valid") is True
        and record.get("adapter_required_operations_complete") is True
        and record.get("adapter_denied_operations_complete") is True
        and record.get("runtime_execution_requested") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v2_4_complete = any(
        record.get("evidence_store_adapter_parity_observed") is True
        and record.get("evidence_store_adapter_parity_valid") is True
        and record.get("adapter_required_operations_valid") is True
        and record.get("adapter_denied_operations_enforced") is True
        and record.get("adapter_append_case_record_valid") is True
        and record.get("adapter_read_case_record_valid") is True
        and record.get("adapter_verify_manifest_chain_valid") is True
        and record.get("adapter_export_replay_pack_valid") is True
        and record.get("adapter_export_audit_pack_valid") is True
        and record.get("adapter_runtime_backend_invoked") is False
        and record.get("adapter_production_storage_backend_observed") is False
        and record.get("runtime_execution_requested") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v2_5_complete = any(
        record.get("computed_policy_engine_observed") is True
        and record.get("computed_policy_engine_result") == "approval_required"
        and record.get("policy_engine_valid") is True
        and int(record.get("policy_engine_supported_rule_type_count", 0) or 0) >= 5
        and int(record.get("policy_engine_active_policy_count", 0) or 0) >= 5
        and int(record.get("policy_engine_revoked_policy_count", 0) or 0) == 0
        and record.get("policy_engine_deny_precedence_enforced") is True
        and record.get("policy_engine_escalate_outcome_supported") is True
        and record.get("policy_engine_compatibility_valid") is True
        and record.get("runtime_execution_requested") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v2_6_complete = any(
        record.get("external_approval_adapter_observed") is True
        and record.get("external_approval_adapter_valid") is True
        and record.get("external_approval_adapter_required_operations_complete") is True
        and record.get("external_approval_adapter_denied_operations_complete") is True
        and record.get("external_approval_adapter_request_evidence_complete") is True
        and record.get("external_approval_adapter_decision_evidence_complete") is True
        and record.get("external_approval_adapter_decision_lifecycle_complete") is True
        and record.get("external_approval_adapter_admission_controls_complete") is True
        and record.get("external_approval_adapter_audit_requirements_complete") is True
        and record.get("external_approval_adapter_boundary_compatible") is True
        and record.get("external_approval_adapter_live_system_observed") is False
        and record.get("external_approval_adapter_ai_approval_allowed") is False
        and record.get("runtime_execution_requested") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v2_7_complete = any(
        record.get("live_identity_rbac_observed") is True
        and record.get("live_identity_rbac_valid") is True
        and record.get("live_identity_rbac_provider") == "github"
        and record.get("live_identity_rbac_permission_sufficient") is True
        and record.get("live_identity_rbac_decision_scope_authorized") is True
        and record.get("live_identity_rbac_mfa_claim_observed") is False
        and record.get("live_external_identity_provider_authenticated") is False
        and record.get("runtime_execution_requested") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v2_8_complete = any(
        record.get("durable_evidence_backend_observed") is True
        and record.get("durable_evidence_backend_valid") is True
        and record.get("durable_backend_runtime_backend_invoked") is False
        and record.get("durable_backend_production_storage_backend_observed") is False
        and record.get("runtime_execution_requested") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v2_9_complete = any(
        record.get("release_promotion_chain_observed") is True
        and record.get("release_promotion_chain_valid") is True
        and record.get("immutable_artifact_digest_observed") is True
        and record.get("source_commit_bound") is True
        and record.get("build_run_id_observed") is True
        and record.get("rollback_evidence_valid") is True
        and record.get("prod_deployment_executed") is False
        and record.get("runtime_execution_requested") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v3_0_complete = any(
        record.get("pre_runtime_ga_observed") is True
        and record.get("pre_runtime_ga_valid") is True
        and record.get("pre_runtime_runtime_blocked") is True
        and record.get("runtime_execution_requested") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v3_1_complete = any(
        record.get("v3_1_governance_closure_valid") is True
        and record.get("v3_1_independent_human_review_observed") is False
        and record.get("runtime_execution_requested") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v3_2_complete = any(
        record.get("v3_2_external_identity_boundary_valid") is True
        and record.get("v3_2_external_identity_live_ready") is False
        and record.get("v3_2_mfa_claim_observed") is False
        and record.get("runtime_execution_requested") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v3_3_complete = any(
        record.get("v3_3_external_approval_system_boundary_valid") is True
        and record.get("v3_3_external_approval_system_live_ready") is False
        and record.get("v3_3_ai_approval_allowed") is False
        and record.get("runtime_execution_requested") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v3_4_complete = any(
        record.get("v3_4_production_case_store_contract_ready") is True
        and record.get("v3_4_production_case_store_live_ready") is False
        and record.get("v3_4_production_storage_backend_observed") is False
        and record.get("runtime_execution_requested") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v3_5_complete = any(
        record.get("v3_5_runtime_control_plane_design_valid") is True
        and record.get("v3_5_runtime_authority_grant_allowed") is False
        and record.get("runtime_execution_requested") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v3_6_complete = any(
        record.get("v3_6_advisory_runtime_pilot_valid") is True
        and record.get("v3_6_advisory_side_effects_executed") is False
        and record.get("v3_6_production_mutation_executed") is False
        and record.get("runtime_execution_requested") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v4_0_complete = any(
        record.get("v4_0_limited_runtime_authority_gate_complete") is True
        and record.get("v4_0_limited_runtime_authority_granted") is False
        and record.get("runtime_execution_requested") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v4_1_complete = any(
        record.get("v4_1_live_identity_evidence_gate_complete") is True
        and record.get("v4_1_live_identity_authority_ready") is False
        and record.get("v4_1_mfa_claim_observed") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v4_2_complete = any(
        record.get("v4_2_live_approval_provider_gate_complete") is True
        and record.get("v4_2_live_approval_provider_ready") is False
        and record.get("v4_2_ai_approval_allowed") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v4_3_complete = any(
        record.get("v4_3_production_case_store_gate_complete") is True
        and record.get("v4_3_production_case_store_live_ready") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v4_4_complete = any(
        record.get("v4_4_release_promotion_execution_gate_complete") is True
        and record.get("v4_4_prod_deployment_executed") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v5_0_complete = any(
        record.get("v5_0_governed_advisory_runtime_complete") is True
        and record.get("v5_0_runtime_recommendation_only") is True
        and record.get("v5_0_side_effects_executed") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v5_5_complete = any(
        record.get("v5_5_controlled_runtime_execution_gate_complete") is True
        and record.get("v5_5_controlled_runtime_execution_authorized") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v6_0_complete = any(
        record.get("v6_0_platform_hardening_assessment_complete") is True
        and record.get("v6_0_platform_production_ready") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v6_1_complete = any(
        record.get("v6_1_live_identity_authority_contract_complete") is True
        and record.get("v6_1_live_identity_authority_ready") is False
        and record.get("v6_1_mfa_claim_observed") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v6_2_complete = any(
        record.get("v6_2_live_decision_approval_provider_contract_complete") is True
        and record.get("v6_2_live_decision_approval_provider_ready") is False
        and record.get("v6_2_ai_approval_allowed") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v6_3_complete = any(
        record.get("v6_3_production_durable_case_store_contract_complete") is True
        and record.get("v6_3_production_durable_case_store_ready") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v6_4_complete = any(
        record.get("v6_4_production_promotion_chain_contract_complete") is True
        and record.get("v6_4_production_promotion_ready") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v7_0_complete = any(
        record.get("v7_0_controlled_runtime_pilot_admission_complete") is True
        and record.get("v7_0_controlled_runtime_pilot_authorized") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v7_5_complete = any(
        record.get("v7_5_marketplace_runtime_governance_complete") is True
        and record.get("v7_5_marketplace_runtime_invocation_authorized") is False
        and record.get("v7_5_unrestricted_marketplace_execution_allowed") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v8_0_complete = any(
        record.get("v8_0_shared_context_runtime_governance_complete") is True
        and record.get("v8_0_runtime_context_exchange_authorized") is False
        and record.get("v8_0_direct_database_access_allowed") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v9_0_complete = any(
        record.get("v9_0_production_authority_readiness_review_complete") is True
        and record.get("v9_0_production_decision_authority_granted") is False
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v10_0_complete = any(
        record.get("v10_0_completion_plan_execution_observed") is True
        and record.get("v10_0_autopilot_execution_review_complete") is True
        and int(record.get("v10_0_reviewed_step_count", 0) or 0) == 9
        and int(record.get("v10_0_evidence_gate_complete_count", 0) or 0) == 9
        and int(record.get("v10_0_blocked_live_completion_count", 0) or 0) >= 9
        and record.get("v10_0_product_vision_alignment_valid") is True
        and record.get("v10_0_ai_policy_boundary_preserved") is True
        and record.get("v10_0_runtime_authority_grant_blocked") is True
        and record.get("v10_0_production_decision_authority_blocked") is True
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v11_0_complete = any(
        record.get("v11_0_api_first_platform_foundation_observed") is True
        and record.get("v11_0_platform_foundation_valid") is True
        and record.get("v11_0_api_architecture_contract_valid") is True
        and record.get("v11_0_rest_authoritative") is True
        and record.get("v11_0_websocket_notification_only") is True
        and record.get("v11_0_event_recovery_rest_twin_declared") is True
        and record.get("v11_0_topology_flexible") is True
        and record.get("v11_0_forced_microservice_topology") is False
        and record.get("v11_0_product_pack_foundation_valid") is True
        and int(record.get("v11_0_product_pack_count", 0) or 0) >= 3
        and record.get("v11_0_ml_product_pack_observed") is True
        and record.get("v11_0_edi_product_pack_observed") is True
        and record.get("v11_0_shared_service_certification_valid") is True
        and int(record.get("v11_0_service_certification_evidence_complete_count", 0) or 0) == 0
        and record.get("v11_0_ml_shared_capability_inventory_valid") is True
        and int(record.get("v11_0_ml_capability_count", 0) or 0) >= 10
        and record.get("v11_0_algo_engine_observe_first") is True
        and record.get("v11_0_adapter_evidence_contract_valid") is True
        and record.get("v11_0_governance_store_contract_valid") is True
        and record.get("v11_0_edi_universal_governance_store") is False
        and record.get("v11_0_direct_database_access_allowed") is False
        and record.get("v11_0_runtime_authority_blocked_model_valid") is True
        and record.get("v11_0_runtime_authority_blocked") is True
        and int(record.get("v11_0_foundation_gate_complete_count", 0) or 0)
        == int(record.get("v11_0_foundation_gate_count", -1) or -1)
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v15_0_complete = any(
        record.get("v12_0_shared_capability_certification_states_valid") is True
        and int(record.get("v12_0_certified_capability_count", -1)) == 0
        and int(record.get("v12_0_runtime_invocation_allowed_count", -1)) == 0
        and record.get("v13_0_product_pack_contracts_valid") is True
        and record.get("v13_0_cross_product_database_access_allowed") is False
        and int(record.get("v13_0_runtime_authority_granted_count", -1)) == 0
        and record.get("v14_0_rest_api_contracts_valid") is True
        and record.get("v14_0_rest_authoritative") is True
        and record.get("v14_0_runtime_authority_default_blocked") is True
        and record.get("v15_0_event_recovery_contract_valid") is True
        and record.get("v15_0_websocket_authoritative") is False
        and record.get("v15_0_events_mutate_business_state") is False
        and record.get("v15_0_rest_recovery_required") is True
        and record.get("v15_0_api_foundation_valid") is True
        and int(record.get("v15_0_foundation_gate_complete_count", 0) or 0)
        == int(record.get("v15_0_foundation_gate_count", -1) or -1)
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v20_0_complete = any(
        record.get("v16_0_certification_evidence_packs_valid") is True
        and int(record.get("v16_0_certified_service_count", -1)) == 0
        and int(record.get("v16_0_runtime_invocation_allowed_count", -1)) == 0
        and record.get("v17_0_product_pack_admission_valid") is True
        and record.get("v17_0_direct_database_access_allowed") is False
        and record.get("v17_0_hidden_shared_state_allowed") is False
        and int(record.get("v17_0_runtime_authority_granted_count", -1)) == 0
        and record.get("v18_0_openapi_skeleton_valid") is True
        and record.get("v18_0_rest_authoritative") is True
        and record.get("v18_0_runtime_authority_blocked_response") is True
        and record.get("v19_0_event_recovery_fixtures_valid") is True
        and record.get("v19_0_websocket_authoritative") is False
        and record.get("v19_0_events_mutate_business_state") is False
        and record.get("v19_0_all_events_recoverable") is True
        and record.get("v20_0_governance_store_logical_schema_valid") is True
        and record.get("v20_0_storage_backend_selected") is False
        and record.get("v20_0_direct_database_access_allowed") is False
        and record.get("v20_0_append_only_required") is True
        and record.get("v20_0_architecture_closure_valid") is True
        and int(record.get("v20_0_closure_gate_complete_count", 0) or 0)
        == int(record.get("v20_0_closure_gate_count", -1) or -1)
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v25_0_complete = any(
        record.get("v21_0_canonical_openapi_contract_valid") is True
        and record.get("v21_0_rest_authoritative") is True
        and record.get("v21_0_all_commands_require_idempotency") is True
        and record.get("v21_0_all_commands_require_correlation") is True
        and record.get("v21_0_runtime_authority_blocked_response") is True
        and record.get("v21_0_websocket_authoritative") is False
        and record.get("v22_0_product_pack_contract_kit_valid") is True
        and record.get("v22_0_direct_database_access_allowed") is False
        and record.get("v22_0_hidden_shared_state_allowed") is False
        and int(record.get("v22_0_runtime_authority_granted_count", -1)) == 0
        and record.get("v23_0_adapter_evidence_contract_kit_valid") is True
        and int(record.get("v23_0_live_invocation_allowed_count", -1)) == 0
        and record.get("v23_0_sample_evidence_present") is True
        and record.get("v24_0_governance_store_logical_api_valid") is True
        and record.get("v24_0_storage_backend_selected") is False
        and record.get("v24_0_direct_database_access_allowed") is False
        and record.get("v24_0_delete_operation_allowed") is False
        and record.get("v24_0_projection_rebuild_required") is True
        and record.get("v25_0_event_recovery_contract_v2_valid") is True
        and record.get("v25_0_websocket_authoritative") is False
        and record.get("v25_0_events_mutate_business_state") is False
        and record.get("v25_0_rest_event_log_required") is True
        and record.get("v25_0_reconnect_recovery_required") is True
        and record.get("v25_0_contract_closure_valid") is True
        and int(record.get("v25_0_closure_gate_complete_count", 0) or 0)
        == int(record.get("v25_0_closure_gate_count", -1) or -1)
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v30_0_complete = any(
        record.get("v26_0_certification_workflow_valid") is True
        and int(record.get("v26_0_certified_count", -1)) == 0
        and int(record.get("v26_0_runtime_invocation_allowed_count", -1)) == 0
        and record.get("v27_0_runtime_authority_gate_contract_valid") is True
        and record.get("v27_0_runtime_authority_granted") is False
        and record.get("v27_0_negative_fixtures_block_authority") is True
        and record.get("v28_0_cost_usage_evidence_contract_valid") is True
        and record.get("v28_0_billing_integration_enabled") is False
        and int(record.get("v28_0_live_invocation_observed_count", -1)) == 0
        and record.get("v29_0_semantic_projection_contract_valid") is True
        and record.get("v29_0_direct_database_access_allowed") is False
        and record.get("v29_0_hidden_shared_state_allowed") is False
        and record.get("v29_0_runtime_context_exchange_authorized") is False
        and record.get("v29_0_all_projections_require_approval") is True
        and record.get("v29_0_all_projections_have_policy_evidence") is True
        and record.get("v30_0_product_pack_developer_kit_valid") is True
        and int(record.get("v30_0_runtime_authority_granted_count", -1)) == 0
        and record.get("v30_0_direct_database_access_allowed") is False
        and record.get("v30_0_platform_operating_model_closure_valid") is True
        and int(record.get("v30_0_closure_gate_complete_count", 0) or 0)
        == int(record.get("v30_0_closure_gate_count", -1) or -1)
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v35_0_complete = any(
        record.get("v31_0_compatibility_versioning_valid") is True
        and record.get("v31_0_breaking_change_requires_major") is True
        and record.get("v31_0_deprecated_requires_replacement") is True
        and record.get("v32_0_policy_test_pack_framework_valid") is True
        and record.get("v32_0_deterministic_policy_first") is True
        and record.get("v32_0_ai_policy_override_allowed") is False
        and record.get("v32_0_required_outcomes_covered") is True
        and record.get("v33_0_product_pack_cli_scaffold_valid") is True
        and record.get("v33_0_no_code_builder") is False
        and record.get("v33_0_runtime_authority_default") == "none"
        and record.get("v33_0_direct_database_access_allowed") is False
        and int(record.get("v33_0_runtime_authority_creating_command_count", -1)) == 0
        and record.get("v34_0_case_evidence_query_contract_valid") is True
        and record.get("v34_0_rest_authoritative") is True
        and record.get("v34_0_production_backend_selected") is False
        and record.get("v34_0_direct_database_access_allowed") is False
        and record.get("v35_0_governance_dashboard_data_contract_valid") is True
        and record.get("v35_0_derived_from_rest_evidence") is True
        and record.get("v35_0_dashboard_is_source_of_truth") is False
        and record.get("v35_0_websocket_authoritative") is False
        and record.get("v35_0_blocked_claims_visible") is True
        and record.get("v35_0_usability_governance_closure_valid") is True
        and int(record.get("v35_0_closure_gate_complete_count", 0) or 0)
        == int(record.get("v35_0_closure_gate_count", -1) or -1)
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    v40_0_complete = any(
        record.get("v36_0_product_pack_authoring_ux_valid") is True
        and record.get("v36_0_all_transitions_require_rest") is True
        and record.get("v36_0_rest_authoritative") is True
        and record.get("v36_0_websocket_authoritative") is False
        and record.get("v36_0_broad_no_code_builder") is False
        and record.get("v36_0_direct_database_access_allowed") is False
        and record.get("v37_0_governance_review_queue_valid") is True
        and record.get("v37_0_solo_maintainer_exception_visible") is True
        and record.get("v37_0_approval_automation_allowed") is False
        and record.get("v38_0_capability_lineage_explorer_valid") is True
        and record.get("v38_0_capability_version_lineage_required") is True
        and record.get("v38_0_direct_runtime_invocation_allowed") is False
        and record.get("v38_0_all_traces_have_evidence") is True
        and record.get("v39_0_replay_workspace_valid") is True
        and record.get("v39_0_drift_comparison_required") is True
        and record.get("v39_0_evidence_references_required") is True
        and record.get("v39_0_websocket_authoritative") is False
        and record.get("v39_0_runtime_execution_allowed") is False
        and record.get("v39_0_side_effects_allowed") is False
        and record.get("v40_0_usability_acceptance_pack_valid") is True
        and record.get("v40_0_rest_authoritative") is True
        and record.get("v40_0_websocket_authoritative") is False
        and record.get("v40_0_evidence_backed") is True
        and record.get("v40_0_runtime_remains_blocked") is True
        and int(record.get("v40_0_closure_gate_complete_count", 0) or 0)
        == int(record.get("v40_0_closure_gate_count", -1) or -1)
        and record.get("runtime_integration_authorized") is False
        and record.get("production_decision_execution_authorized") is False
        for record in target_records
    )
    pre_runtime_completion_scope_complete = all(
        [
            v0_1_complete,
            v0_3_complete,
            v0_4_complete,
            v0_5_complete,
            v0_6_complete,
            v0_7_complete,
            v0_8_complete,
            v0_9_complete,
            v1_0_complete,
            v1_1_complete,
            v1_2_complete,
            v1_3_complete,
            v1_4_complete,
            v1_5_complete,
            v2_0_complete,
            v2_1_complete,
            v2_2_complete,
            v2_3_complete,
            v2_4_complete,
            v2_5_complete,
            v2_6_complete,
            v2_7_complete,
            v2_8_complete,
            v2_9_complete,
            v3_0_complete,
            v3_1_complete,
            v3_2_complete,
            v3_3_complete,
            v3_4_complete,
            v3_5_complete,
            v3_6_complete,
            v4_0_complete,
            v4_1_complete,
            v4_2_complete,
            v4_3_complete,
            v4_4_complete,
            v5_0_complete,
            v5_5_complete,
            v6_0_complete,
            v6_1_complete,
            v6_2_complete,
            v6_3_complete,
            v6_4_complete,
            v7_0_complete,
            v7_5_complete,
            v8_0_complete,
            v9_0_complete,
            v10_0_complete,
            v11_0_complete,
            v15_0_complete,
            v20_0_complete,
            v25_0_complete,
            v30_0_complete,
            v35_0_complete,
            v40_0_complete,
        ]
    )
    release_management_readiness_percent = 45.0
    if v2_9_complete:
        release_management_readiness_percent = 95.0
    elif v0_8_complete and v0_7_complete:
        release_management_readiness_percent = 85.0
    elif v0_7_complete:
        release_management_readiness_percent = 70.0
    elif release_governance_gaps and release_artifact_gaps:
        release_management_readiness_percent = 35.0
    elif release_governance_gaps:
        release_management_readiness_percent = 40.0
    return {
        "generated_at": generated_at,
        "acceptance_state": (
            "pre_runtime_trust_loop_complete_runtime_blocked"
            if v0_1_complete
            else "governance_pack_ready_implementation_evidence_incomplete"
            if policy_ready
            else "incomplete"
        ),
        "maturity_claim": (
            "DIP v0.1 pre-runtime governance skeleton complete; governed decision platform readiness incomplete"
            if v0_1_complete
            else "DIP v0.1 pre-runtime governance skeleton incomplete"
        ),
        "policy_readiness_percent": 100.0 if policy_ready else 0.0,
        "v0_1_pre_runtime_trust_loop_skeleton_percent": 100.0 if v0_1_complete else 0.0,
        "contract_shape_evidence_percent": 100.0 if evidence["all_contract_artifacts_valid"] else 0.0,
        "local_validation_and_ci_evidence_percent": target_evidence["target_repo_evidence_percent"],
        "target_repo_governance_clean_percent": target_evidence.get("target_repo_governance_clean_percent", 0.0),
        "github_repository_governance_baseline": "strong_incomplete"
        if target_evidence["target_repo_evidence_percent"] == 100.0
        else "incomplete",
        "maturity_status_labels": {
            "policy_preflight": "computed_for_first_fixture",
            "policy_engine": "deterministic_policy_engine_lifecycle_and_precedence_validated"
            if v2_5_complete
            else "policy_engine_hardening_incomplete",
            "simulation_and_diff": "computed_diff_fixture_simulation",
            "replay": "manifest_backed_replay_pre_runtime" if v0_5_complete else "evidence_shaped_not_reproducible",
            "case_store": "append_only_manifest_chain" if v0_5_complete else "file_backed_tamper_evident_not_durable",
            "durable_store": "durable_store_contract_content_addressed_no_production_backend"
            if v1_0_complete
            else "manifest_chain_without_store_contract",
            "approval": "local_identity_rbac_authority_evaluated_external_idp_missing"
            if v0_9_complete and not v2_7_complete
            else "live_github_rbac_observed_mfa_claim_missing"
            if v2_7_complete
            else "local_identity_rbac_authority_evaluated_external_idp_missing"
            if v0_6_complete
            else "manifest_bound_role_validated_fixture_identity"
            if v0_5_complete
            else "fixture_backed_not_identity_governed",
            "release_management": "promotion_chain_and_rollback_evidence_observed_admin_bypass_governed"
            if v2_9_complete
            else "tag_and_local_acceptance_present_ci_artifact_missing_admin_bypass_observed"
            if release_governance_gaps and release_artifact_gaps
            else "tag_and_artifact_backed_acceptance_present_admin_bypass_observed"
            if release_governance_gaps
            else "release_lifecycle_policy_artifact_backed_admin_enforced"
            if v0_8_complete and v0_7_complete
            else "admin_enforced_tag_and_artifact_backed_acceptance_present"
            if v0_7_complete
            else "release_tag_and_artifact_backed_acceptance_present",
            "product_review_surface": "review_workspace_generated" if v1_2_complete else "review_workspace_missing",
            "multi_domain": "three_decision_shapes_simulated" if v1_3_complete else "domain_generalization_incomplete",
            "capability_governance": "capability_graph_and_policy_validated"
            if v1_4_complete
            else "capability_governance_incomplete",
            "shared_context": "semantic_contract_validated_no_runtime_exchange"
            if v1_5_complete
            else "shared_context_contract_incomplete",
            "runtime_execution": "blocked_by_runtime_readiness_assessment"
            if v2_0_complete
            else "blocked_pending_durable_evidence",
            "production_decision_authority": "blocked_by_runtime_readiness_assessment"
            if v2_0_complete
            else "blocked_pending_durable_evidence",
            "solo_maintainer_exception": "governed_exception_no_independent_review_claim"
            if v2_1_complete
            else "solo_maintainer_exception_missing",
            "schema_stability": "frozen_contracts_and_negative_fixtures_validated"
            if v2_1_complete
            else "schema_stability_incomplete",
            "external_approval": "decision_approval_boundary_separate_from_code_merge"
            if v2_2_complete
            else "external_approval_boundary_incomplete",
            "external_approval_adapter": "adapter_contract_valid_no_live_approval_system"
            if v2_6_complete
            else "external_approval_adapter_incomplete",
            "live_identity_rbac": "live_github_rbac_observed_mfa_claim_missing"
            if v2_7_complete
            else "live_identity_rbac_incomplete",
            "durable_adapter": "adapter_boundary_valid_no_production_backend"
            if v2_3_complete
            else "durable_adapter_boundary_incomplete",
            "evidence_store_adapter_parity": "required_and_denied_operations_valid_no_runtime_backend"
            if v2_4_complete
            else "evidence_store_adapter_parity_incomplete",
            "durable_evidence_backend": "observed_pre_runtime_backend_no_runtime_invocation"
            if v2_8_complete
            else "durable_evidence_backend_incomplete",
            "release_promotion": "promotion_chain_and_rollback_evidence_observed"
            if v2_9_complete
            else "release_promotion_incomplete",
            "pre_runtime_ga": "complete_runtime_blocked" if v3_0_complete else "pre_runtime_ga_incomplete",
            "governance_closure": "review_gates_restored_exception_preserved"
            if v3_1_complete
            else "governance_closure_incomplete",
            "external_identity_integration": "boundary_valid_live_idp_mfa_blocked"
            if v3_2_complete
            else "external_identity_integration_incomplete",
            "external_approval_system": "boundary_valid_live_provider_blocked"
            if v3_3_complete
            else "external_approval_system_incomplete",
            "production_case_store": "contract_ready_live_backend_blocked"
            if v3_4_complete
            else "production_case_store_incomplete",
            "runtime_control_plane": "design_valid_authority_grant_blocked"
            if v3_5_complete
            else "runtime_control_plane_incomplete",
            "advisory_runtime": "advisory_only_no_side_effects"
            if v3_6_complete
            else "advisory_runtime_incomplete",
            "limited_runtime_authority": "gate_complete_authority_blocked"
            if v4_0_complete
            else "limited_runtime_authority_incomplete",
            "live_identity_evidence": "gate_complete_live_idp_mfa_blocked"
            if v4_1_complete
            else "live_identity_evidence_incomplete",
            "live_approval_provider": "gate_complete_live_provider_blocked"
            if v4_2_complete
            else "live_approval_provider_incomplete",
            "production_case_store_gate": "gate_complete_live_backend_blocked"
            if v4_3_complete
            else "production_case_store_gate_incomplete",
            "release_promotion_execution": "gate_complete_prod_deployment_blocked"
            if v4_4_complete
            else "release_promotion_execution_incomplete",
            "governed_advisory_runtime": "advisory_only_recommendation_no_side_effects"
            if v5_0_complete
            else "governed_advisory_runtime_incomplete",
            "controlled_runtime_execution": "gate_complete_execution_blocked"
            if v5_5_complete
            else "controlled_runtime_execution_incomplete",
            "platform_hardening": "assessment_complete_production_readiness_blocked"
            if v6_0_complete
            else "platform_hardening_incomplete",
            "live_identity_authority": "contract_complete_live_idp_mfa_blocked"
            if v6_1_complete
            else "live_identity_authority_incomplete",
            "live_decision_approval_provider": "contract_complete_live_provider_blocked"
            if v6_2_complete
            else "live_decision_approval_provider_incomplete",
            "production_durable_case_store": "contract_complete_live_backend_blocked"
            if v6_3_complete
            else "production_durable_case_store_incomplete",
            "production_promotion_chain": "contract_complete_prod_deployment_blocked"
            if v6_4_complete
            else "production_promotion_chain_incomplete",
            "controlled_runtime_pilot": "admission_complete_authority_blocked"
            if v7_0_complete
            else "controlled_runtime_pilot_incomplete",
            "marketplace_runtime_governance": "governance_complete_invocation_blocked"
            if v7_5_complete
            else "marketplace_runtime_governance_incomplete",
            "shared_context_runtime_governance": "governance_complete_exchange_blocked"
            if v8_0_complete
            else "shared_context_runtime_governance_incomplete",
            "production_authority_readiness": "review_complete_authority_blocked"
            if v9_0_complete
            else "production_authority_readiness_incomplete",
            "completion_plan_execution": "review_complete_live_completion_blocked"
            if v10_0_complete
            else "completion_plan_execution_incomplete",
            "api_first_platform_foundation": "contract_complete_runtime_blocked"
            if v11_0_complete
            else "api_first_platform_foundation_incomplete",
        },
        "deterministic_policy_engine_readiness_percent": 80.0
        if v2_5_complete
        else 60.0
        if v0_3_complete
        else 45.0,
        "computed_simulation_diff_readiness_percent": 80.0
        if v1_3_complete
        else 70.0
        if v0_4_complete
        else 45.0
        if v0_3_complete
        else 10.0,
        "durable_case_store_readiness_percent": 95.0
        if v2_8_complete
        else 90.0
        if v2_4_complete
        else 85.0
        if v2_3_complete
        else 80.0
        if v1_0_complete
        else 60.0
        if v0_5_complete
        else 30.0,
        "identity_backed_approval_readiness_percent": 85.0
        if v2_7_complete
        else 75.0
        if v2_6_complete
        else 65.0
        if v0_9_complete
        else 45.0
        if v0_6_complete
        else 25.0
        if v0_5_complete
        else 0.0,
        "release_management_readiness_percent": release_management_readiness_percent,
        "runtime_execution_readiness_percent": 0.0,
        "production_decision_authority_percent": 0.0,
        "implementation_backlog_defined_percent": backlog["defined_percent"],
        "v0_2_backlog_defined_percent": v0_2_backlog["defined_percent"],
        "v0_2_backlog_status_label": "completed_pre_runtime"
        if v0_2_backlog["completed_slice_count"] == v0_2_backlog["slice_count"]
        else "planned_pre_runtime",
        "v0_3_computed_policy_diff_evidence_percent": 100.0 if v0_3_complete else 0.0,
        "v0_3_status_label": "completed_pre_runtime" if v0_3_complete else "planned_pre_runtime",
        "v0_4_computed_simulation_evidence_percent": 100.0 if v0_4_complete else 0.0,
        "v0_4_status_label": "completed_pre_runtime" if v0_4_complete else "planned_pre_runtime",
        "v0_5_durable_case_approval_evidence_percent": 100.0 if v0_5_complete else 0.0,
        "v0_5_status_label": "completed_pre_runtime" if v0_5_complete else "planned_pre_runtime",
        "v0_6_identity_rbac_approval_evidence_percent": 100.0 if v0_6_complete else 0.0,
        "v0_6_status_label": "completed_pre_runtime" if v0_6_complete else "planned_pre_runtime",
        "v0_7_repository_governance_evidence_percent": 100.0 if v0_7_complete else 0.0,
        "v0_7_status_label": "completed_pre_runtime" if v0_7_complete else "planned_pre_runtime",
        "v0_8_release_lifecycle_evidence_percent": 100.0 if v0_8_complete else 0.0,
        "v0_8_status_label": "completed_pre_runtime" if v0_8_complete else "planned_pre_runtime",
        "v0_9_external_identity_contract_evidence_percent": 100.0 if v0_9_complete else 0.0,
        "v0_9_status_label": "completed_pre_runtime" if v0_9_complete else "planned_pre_runtime",
        "v1_0_durable_store_contract_evidence_percent": 100.0 if v1_0_complete else 0.0,
        "v1_0_status_label": "completed_pre_runtime" if v1_0_complete else "planned_pre_runtime",
        "v1_1_governance_enforcement_parity_percent": 100.0 if v1_1_complete else 0.0,
        "v1_1_status_label": "completed_pre_runtime" if v1_1_complete else "planned_pre_runtime",
        "v1_2_product_review_surface_evidence_percent": 100.0 if v1_2_complete else 0.0,
        "v1_2_status_label": "completed_pre_runtime" if v1_2_complete else "planned_pre_runtime",
        "v1_3_multi_domain_simulation_evidence_percent": 100.0 if v1_3_complete else 0.0,
        "v1_3_status_label": "completed_pre_runtime" if v1_3_complete else "planned_pre_runtime",
        "v1_4_capability_governance_evidence_percent": 100.0 if v1_4_complete else 0.0,
        "v1_4_status_label": "completed_pre_runtime" if v1_4_complete else "planned_pre_runtime",
        "v1_5_shared_context_contract_evidence_percent": 100.0 if v1_5_complete else 0.0,
        "v1_5_status_label": "completed_pre_runtime" if v1_5_complete else "planned_pre_runtime",
        "v2_0_runtime_readiness_assessment_percent": 100.0 if v2_0_complete else 0.0,
        "v2_0_status_label": "completed_pre_runtime" if v2_0_complete else "planned_pre_runtime",
        "v2_1_governed_exception_schema_stability_percent": 100.0 if v2_1_complete else 0.0,
        "v2_1_status_label": "completed_pre_runtime" if v2_1_complete else "planned_pre_runtime",
        "independent_human_review_observed": any(
            record.get("independent_human_review_observed") is True for record in target_records
        ),
        "v2_2_external_approval_boundary_percent": 100.0 if v2_2_complete else 0.0,
        "v2_2_status_label": "completed_pre_runtime" if v2_2_complete else "planned_pre_runtime",
        "live_external_approval_system_observed": any(
            record.get("live_external_approval_system_observed") is True for record in target_records
        ),
        "v2_3_durable_case_store_adapter_percent": 100.0 if v2_3_complete else 0.0,
        "v2_3_status_label": "completed_pre_runtime" if v2_3_complete else "planned_pre_runtime",
        "production_durable_case_store_backend_observed": any(
            record.get("adapter_production_storage_backend_observed") is True for record in target_records
        ),
        "v2_4_evidence_store_adapter_parity_percent": 100.0 if v2_4_complete else 0.0,
        "v2_4_status_label": "completed_pre_runtime" if v2_4_complete else "planned_pre_runtime",
        "adapter_runtime_backend_invoked": any(
            record.get("adapter_runtime_backend_invoked") is True for record in target_records
        ),
        "v2_5_policy_engine_hardening_percent": 100.0 if v2_5_complete else 0.0,
        "v2_5_status_label": "completed_pre_runtime" if v2_5_complete else "planned_pre_runtime",
        "policy_engine_runtime_authority_observed": any(
            record.get("runtime_integration_authorized") is True
            or record.get("production_decision_execution_authorized") is True
            for record in target_records
        ),
        "v2_6_external_approval_adapter_percent": 100.0 if v2_6_complete else 0.0,
        "v2_6_status_label": "completed_pre_runtime" if v2_6_complete else "planned_pre_runtime",
        "external_approval_adapter_live_system_observed": any(
            record.get("external_approval_adapter_live_system_observed") is True for record in target_records
        ),
        "external_approval_adapter_ai_approval_allowed": any(
            record.get("external_approval_adapter_ai_approval_allowed") is True for record in target_records
        ),
        "v2_7_live_identity_rbac_percent": 100.0 if v2_7_complete else 0.0,
        "v2_7_status_label": "completed_pre_runtime_mfa_claim_blocked"
        if v2_7_complete
        else "planned_pre_runtime",
        "live_identity_rbac_provider": next(
            (record.get("live_identity_rbac_provider") for record in target_records if record.get("live_identity_rbac_provider")),
            "not_observed",
        ),
        "live_identity_rbac_subject": next(
            (record.get("live_identity_rbac_subject") for record in target_records if record.get("live_identity_rbac_subject")),
            "not_observed",
        ),
        "live_identity_rbac_repository_permission": next(
            (
                record.get("live_identity_rbac_repository_permission")
                for record in target_records
                if record.get("live_identity_rbac_repository_permission")
            ),
            "not_observed",
        ),
        "live_identity_rbac_mfa_claim_observed": any(
            record.get("live_identity_rbac_mfa_claim_observed") is True for record in target_records
        ),
        "v2_8_durable_evidence_backend_percent": 100.0 if v2_8_complete else 0.0,
        "v2_8_status_label": "completed_pre_runtime" if v2_8_complete else "planned_pre_runtime",
        "durable_evidence_backend_runtime_invoked": any(
            record.get("durable_backend_runtime_backend_invoked") is True for record in target_records
        ),
        "v2_9_release_promotion_rollback_percent": 100.0 if v2_9_complete else 0.0,
        "v2_9_status_label": "completed_pre_runtime" if v2_9_complete else "planned_pre_runtime",
        "prod_deployment_executed": any(record.get("prod_deployment_executed") is True for record in target_records),
        "v3_0_pre_runtime_ga_percent": 100.0 if v3_0_complete else 0.0,
        "v3_0_status_label": "complete_runtime_blocked" if v3_0_complete else "planned_pre_runtime",
        "v3_1_governance_closure_percent": 100.0 if v3_1_complete else 0.0,
        "v3_1_status_label": "completed_pre_runtime_exception_preserved"
        if v3_1_complete
        else "planned_pre_runtime",
        "v3_2_external_identity_integration_percent": 100.0 if v3_2_complete else 0.0,
        "v3_2_status_label": "boundary_complete_live_idp_mfa_blocked"
        if v3_2_complete
        else "planned_pre_runtime",
        "v3_2_external_identity_live_ready": any(
            record.get("v3_2_external_identity_live_ready") is True for record in target_records
        ),
        "v3_3_external_approval_system_percent": 100.0 if v3_3_complete else 0.0,
        "v3_3_status_label": "boundary_complete_live_provider_blocked"
        if v3_3_complete
        else "planned_pre_runtime",
        "v3_3_external_approval_system_live_ready": any(
            record.get("v3_3_external_approval_system_live_ready") is True for record in target_records
        ),
        "v3_4_production_case_store_boundary_percent": 100.0 if v3_4_complete else 0.0,
        "v3_4_status_label": "contract_complete_live_backend_blocked"
        if v3_4_complete
        else "planned_pre_runtime",
        "v3_4_production_case_store_live_ready": any(
            record.get("v3_4_production_case_store_live_ready") is True for record in target_records
        ),
        "v3_5_runtime_control_plane_design_percent": 100.0 if v3_5_complete else 0.0,
        "v3_5_status_label": "design_complete_authority_grant_blocked"
        if v3_5_complete
        else "planned_pre_runtime",
        "v3_6_advisory_runtime_pilot_percent": 100.0 if v3_6_complete else 0.0,
        "v3_6_status_label": "advisory_only_no_side_effects" if v3_6_complete else "planned_pre_runtime",
        "v4_0_limited_runtime_authority_gate_percent": 100.0 if v4_0_complete else 0.0,
        "v4_0_status_label": "gate_complete_authority_blocked" if v4_0_complete else "planned_pre_runtime",
        "v4_0_limited_runtime_authority_granted": any(
            record.get("v4_0_limited_runtime_authority_granted") is True for record in target_records
        ),
        "v4_1_live_identity_evidence_gate_percent": 100.0 if v4_1_complete else 0.0,
        "v4_1_status_label": "gate_complete_live_idp_mfa_blocked" if v4_1_complete else "planned_pre_runtime",
        "v4_1_live_identity_authority_ready": any(
            record.get("v4_1_live_identity_authority_ready") is True for record in target_records
        ),
        "v4_1_mfa_claim_observed": any(record.get("v4_1_mfa_claim_observed") is True for record in target_records),
        "v4_2_live_approval_provider_gate_percent": 100.0 if v4_2_complete else 0.0,
        "v4_2_status_label": "gate_complete_live_provider_blocked" if v4_2_complete else "planned_pre_runtime",
        "v4_2_live_approval_provider_ready": any(
            record.get("v4_2_live_approval_provider_ready") is True for record in target_records
        ),
        "v4_2_ai_approval_allowed": any(record.get("v4_2_ai_approval_allowed") is True for record in target_records),
        "v4_3_production_case_store_gate_percent": 100.0 if v4_3_complete else 0.0,
        "v4_3_status_label": "gate_complete_live_backend_blocked" if v4_3_complete else "planned_pre_runtime",
        "v4_3_production_case_store_live_ready": any(
            record.get("v4_3_production_case_store_live_ready") is True for record in target_records
        ),
        "v4_4_release_promotion_execution_gate_percent": 100.0 if v4_4_complete else 0.0,
        "v4_4_status_label": "gate_complete_prod_deployment_blocked" if v4_4_complete else "planned_pre_runtime",
        "v4_4_prod_deployment_executed": any(
            record.get("v4_4_prod_deployment_executed") is True for record in target_records
        ),
        "v5_0_governed_advisory_runtime_percent": 100.0 if v5_0_complete else 0.0,
        "v5_0_status_label": "advisory_only_recommendation_no_side_effects"
        if v5_0_complete
        else "planned_pre_runtime",
        "v5_0_runtime_recommendation_only": any(
            record.get("v5_0_runtime_recommendation_only") is True for record in target_records
        ),
        "v5_0_side_effects_executed": any(
            record.get("v5_0_side_effects_executed") is True for record in target_records
        ),
        "v5_5_controlled_runtime_execution_gate_percent": 100.0 if v5_5_complete else 0.0,
        "v5_5_status_label": "gate_complete_execution_blocked" if v5_5_complete else "planned_pre_runtime",
        "v5_5_controlled_runtime_execution_authorized": any(
            record.get("v5_5_controlled_runtime_execution_authorized") is True for record in target_records
        ),
        "v6_0_platform_hardening_assessment_percent": 100.0 if v6_0_complete else 0.0,
        "v6_0_status_label": "assessment_complete_production_readiness_blocked"
        if v6_0_complete
        else "planned_pre_runtime",
        "v6_0_platform_production_ready": any(
            record.get("v6_0_platform_production_ready") is True for record in target_records
        ),
        "v6_0_hardening_control_count": max(
            [int(record.get("v6_0_hardening_control_count", 0) or 0) for record in target_records] or [0]
        ),
        "v6_1_live_identity_authority_percent": 100.0 if v6_1_complete else 0.0,
        "v6_1_status_label": "contract_complete_live_idp_mfa_blocked"
        if v6_1_complete
        else "planned_pre_runtime",
        "v6_1_live_identity_authority_ready": any(
            record.get("v6_1_live_identity_authority_ready") is True for record in target_records
        ),
        "v6_1_mfa_claim_observed": any(
            record.get("v6_1_mfa_claim_observed") is True for record in target_records
        ),
        "v6_2_live_decision_approval_provider_percent": 100.0 if v6_2_complete else 0.0,
        "v6_2_status_label": "contract_complete_live_provider_blocked"
        if v6_2_complete
        else "planned_pre_runtime",
        "v6_2_live_decision_approval_provider_ready": any(
            record.get("v6_2_live_decision_approval_provider_ready") is True for record in target_records
        ),
        "v6_2_ai_approval_allowed": any(record.get("v6_2_ai_approval_allowed") is True for record in target_records),
        "v6_3_production_durable_case_store_percent": 100.0 if v6_3_complete else 0.0,
        "v6_3_status_label": "contract_complete_live_backend_blocked"
        if v6_3_complete
        else "planned_pre_runtime",
        "v6_3_production_durable_case_store_ready": any(
            record.get("v6_3_production_durable_case_store_ready") is True for record in target_records
        ),
        "v6_4_production_promotion_chain_percent": 100.0 if v6_4_complete else 0.0,
        "v6_4_status_label": "contract_complete_prod_deployment_blocked"
        if v6_4_complete
        else "planned_pre_runtime",
        "v6_4_production_promotion_ready": any(
            record.get("v6_4_production_promotion_ready") is True for record in target_records
        ),
        "v7_0_controlled_runtime_pilot_percent": 100.0 if v7_0_complete else 0.0,
        "v7_0_status_label": "admission_complete_authority_blocked" if v7_0_complete else "planned_pre_runtime",
        "v7_0_controlled_runtime_pilot_authorized": any(
            record.get("v7_0_controlled_runtime_pilot_authorized") is True for record in target_records
        ),
        "v7_5_marketplace_runtime_governance_percent": 100.0 if v7_5_complete else 0.0,
        "v7_5_status_label": "governance_complete_invocation_blocked"
        if v7_5_complete
        else "planned_pre_runtime",
        "v7_5_marketplace_runtime_invocation_authorized": any(
            record.get("v7_5_marketplace_runtime_invocation_authorized") is True for record in target_records
        ),
        "v7_5_unrestricted_marketplace_execution_allowed": any(
            record.get("v7_5_unrestricted_marketplace_execution_allowed") is True for record in target_records
        ),
        "v8_0_shared_context_runtime_governance_percent": 100.0 if v8_0_complete else 0.0,
        "v8_0_status_label": "governance_complete_exchange_blocked"
        if v8_0_complete
        else "planned_pre_runtime",
        "v8_0_runtime_context_exchange_authorized": any(
            record.get("v8_0_runtime_context_exchange_authorized") is True for record in target_records
        ),
        "v8_0_direct_database_access_allowed": any(
            record.get("v8_0_direct_database_access_allowed") is True for record in target_records
        ),
        "v9_0_production_authority_readiness_review_percent": 100.0 if v9_0_complete else 0.0,
        "v9_0_status_label": "review_complete_authority_blocked" if v9_0_complete else "planned_pre_runtime",
        "v9_0_production_decision_authority_granted": any(
            record.get("v9_0_production_decision_authority_granted") is True for record in target_records
        ),
        "v10_0_completion_plan_execution_percent": 100.0 if v10_0_complete else 0.0,
        "v10_0_status_label": "review_complete_live_completion_blocked"
        if v10_0_complete
        else "planned_pre_runtime",
        "v10_0_reviewed_step_count": max(
            [int(record.get("v10_0_reviewed_step_count", 0) or 0) for record in target_records] or [0]
        ),
        "v10_0_evidence_gate_complete_count": max(
            [int(record.get("v10_0_evidence_gate_complete_count", 0) or 0) for record in target_records] or [0]
        ),
        "v10_0_live_completion_achieved_count": max(
            [int(record.get("v10_0_live_completion_achieved_count", 0) or 0) for record in target_records] or [0]
        ),
        "v10_0_blocked_live_completion_count": max(
            [int(record.get("v10_0_blocked_live_completion_count", 0) or 0) for record in target_records] or [0]
        ),
        "v10_0_product_vision_alignment_valid": any(
            record.get("v10_0_product_vision_alignment_valid") is True for record in target_records
        ),
        "v10_0_ai_policy_boundary_preserved": any(
            record.get("v10_0_ai_policy_boundary_preserved") is True for record in target_records
        ),
        "v10_0_runtime_authority_grant_blocked": any(
            record.get("v10_0_runtime_authority_grant_blocked") is True for record in target_records
        ),
        "v10_0_production_decision_authority_blocked": any(
            record.get("v10_0_production_decision_authority_blocked") is True for record in target_records
        ),
        "v11_0_api_first_platform_foundation_percent": 100.0 if v11_0_complete else 0.0,
        "v11_0_status_label": "contract_complete_runtime_blocked" if v11_0_complete else "planned_pre_runtime",
        "v11_0_platform_foundation_valid": any(
            record.get("v11_0_platform_foundation_valid") is True for record in target_records
        ),
        "v11_0_rest_authoritative": any(record.get("v11_0_rest_authoritative") is True for record in target_records),
        "v11_0_websocket_notification_only": any(
            record.get("v11_0_websocket_notification_only") is True for record in target_records
        ),
        "v11_0_topology_flexible": any(record.get("v11_0_topology_flexible") is True for record in target_records),
        "v11_0_forced_microservice_topology": any(
            record.get("v11_0_forced_microservice_topology") is True for record in target_records
        ),
        "v11_0_product_pack_count": max(
            [int(record.get("v11_0_product_pack_count", 0) or 0) for record in target_records] or [0]
        ),
        "v11_0_ml_capability_count": max(
            [int(record.get("v11_0_ml_capability_count", 0) or 0) for record in target_records] or [0]
        ),
        "v11_0_service_certification_evidence_complete_count": max(
            [
                int(record.get("v11_0_service_certification_evidence_complete_count", 0) or 0)
                for record in target_records
            ]
            or [0]
        ),
        "v11_0_edi_universal_governance_store": any(
            record.get("v11_0_edi_universal_governance_store") is True for record in target_records
        ),
        "v11_0_direct_database_access_allowed": any(
            record.get("v11_0_direct_database_access_allowed") is True for record in target_records
        ),
        "v11_0_runtime_authority_blocked": any(
            record.get("v11_0_runtime_authority_blocked") is True for record in target_records
        ),
        "v15_0_api_foundation_percent": 100.0 if v15_0_complete else 0.0,
        "v15_0_status_label": "contract_complete_runtime_blocked" if v15_0_complete else "planned_pre_runtime",
        "v20_0_architecture_closure_percent": 100.0 if v20_0_complete else 0.0,
        "v20_0_status_label": "architecture_closed_runtime_blocked" if v20_0_complete else "planned_pre_runtime",
        "v25_0_contract_closure_percent": 100.0 if v25_0_complete else 0.0,
        "v25_0_status_label": "contract_closed_runtime_blocked" if v25_0_complete else "planned_pre_runtime",
        "v30_0_platform_operating_model_percent": 100.0 if v30_0_complete else 0.0,
        "v30_0_status_label": "platform_operating_model_closed_runtime_blocked"
        if v30_0_complete
        else "planned_pre_runtime",
        "v35_0_usability_governance_percent": 100.0 if v35_0_complete else 0.0,
        "v35_0_status_label": "usability_governance_closed_runtime_blocked"
        if v35_0_complete
        else "planned_pre_runtime",
        "v40_0_review_workspace_percent": 100.0 if v40_0_complete else 0.0,
        "v40_0_status_label": "review_workspace_closed_runtime_blocked"
        if v40_0_complete
        else "planned_pre_runtime",
        "v12_0_shared_capability_certification_states_valid": any(
            record.get("v12_0_shared_capability_certification_states_valid") is True for record in target_records
        ),
        "v12_0_certified_capability_count": max(
            [int(record.get("v12_0_certified_capability_count", 0) or 0) for record in target_records] or [0]
        ),
        "v12_0_runtime_invocation_allowed_count": max(
            [int(record.get("v12_0_runtime_invocation_allowed_count", 0) or 0) for record in target_records] or [0]
        ),
        "v13_0_product_pack_contracts_valid": any(
            record.get("v13_0_product_pack_contracts_valid") is True for record in target_records
        ),
        "v13_0_cross_product_database_access_allowed": any(
            record.get("v13_0_cross_product_database_access_allowed") is True for record in target_records
        ),
        "v13_0_runtime_authority_granted_count": max(
            [int(record.get("v13_0_runtime_authority_granted_count", 0) or 0) for record in target_records] or [0]
        ),
        "v14_0_rest_api_contracts_valid": any(
            record.get("v14_0_rest_api_contracts_valid") is True for record in target_records
        ),
        "v14_0_rest_authoritative": any(record.get("v14_0_rest_authoritative") is True for record in target_records),
        "v14_0_runtime_authority_default_blocked": any(
            record.get("v14_0_runtime_authority_default_blocked") is True for record in target_records
        ),
        "v15_0_event_recovery_contract_valid": any(
            record.get("v15_0_event_recovery_contract_valid") is True for record in target_records
        ),
        "v15_0_websocket_authoritative": any(
            record.get("v15_0_websocket_authoritative") is True for record in target_records
        ),
        "v15_0_events_mutate_business_state": any(
            record.get("v15_0_events_mutate_business_state") is True for record in target_records
        ),
        "v15_0_rest_recovery_required": any(
            record.get("v15_0_rest_recovery_required") is True for record in target_records
        ),
        "v15_0_api_foundation_valid": any(
            record.get("v15_0_api_foundation_valid") is True for record in target_records
        ),
        "v16_0_certification_evidence_packs_valid": any(
            record.get("v16_0_certification_evidence_packs_valid") is True for record in target_records
        ),
        "v16_0_certified_service_count": max(
            [int(record.get("v16_0_certified_service_count", 0) or 0) for record in target_records] or [0]
        ),
        "v16_0_runtime_invocation_allowed_count": max(
            [int(record.get("v16_0_runtime_invocation_allowed_count", 0) or 0) for record in target_records]
            or [0]
        ),
        "v17_0_product_pack_admission_valid": any(
            record.get("v17_0_product_pack_admission_valid") is True for record in target_records
        ),
        "v17_0_direct_database_access_allowed": any(
            record.get("v17_0_direct_database_access_allowed") is True for record in target_records
        ),
        "v17_0_hidden_shared_state_allowed": any(
            record.get("v17_0_hidden_shared_state_allowed") is True for record in target_records
        ),
        "v17_0_runtime_authority_granted_count": max(
            [int(record.get("v17_0_runtime_authority_granted_count", 0) or 0) for record in target_records]
            or [0]
        ),
        "v18_0_openapi_skeleton_valid": any(
            record.get("v18_0_openapi_skeleton_valid") is True for record in target_records
        ),
        "v18_0_rest_authoritative": any(
            record.get("v18_0_rest_authoritative") is True for record in target_records
        ),
        "v18_0_runtime_authority_blocked_response": any(
            record.get("v18_0_runtime_authority_blocked_response") is True for record in target_records
        ),
        "v19_0_event_recovery_fixtures_valid": any(
            record.get("v19_0_event_recovery_fixtures_valid") is True for record in target_records
        ),
        "v19_0_websocket_authoritative": any(
            record.get("v19_0_websocket_authoritative") is True for record in target_records
        ),
        "v19_0_events_mutate_business_state": any(
            record.get("v19_0_events_mutate_business_state") is True for record in target_records
        ),
        "v19_0_all_events_recoverable": any(
            record.get("v19_0_all_events_recoverable") is True for record in target_records
        ),
        "v20_0_governance_store_logical_schema_valid": any(
            record.get("v20_0_governance_store_logical_schema_valid") is True for record in target_records
        ),
        "v20_0_storage_backend_selected": any(
            record.get("v20_0_storage_backend_selected") is True for record in target_records
        ),
        "v20_0_direct_database_access_allowed": any(
            record.get("v20_0_direct_database_access_allowed") is True for record in target_records
        ),
        "v20_0_append_only_required": any(
            record.get("v20_0_append_only_required") is True for record in target_records
        ),
        "v20_0_architecture_closure_valid": any(
            record.get("v20_0_architecture_closure_valid") is True for record in target_records
        ),
        "v20_0_closure_gate_complete_count": max(
            [int(record.get("v20_0_closure_gate_complete_count", 0) or 0) for record in target_records] or [0]
        ),
        "v20_0_closure_gate_count": max(
            [int(record.get("v20_0_closure_gate_count", 0) or 0) for record in target_records] or [0]
        ),
        "v21_0_canonical_openapi_contract_valid": any(
            record.get("v21_0_canonical_openapi_contract_valid") is True for record in target_records
        ),
        "v21_0_rest_authoritative": any(
            record.get("v21_0_rest_authoritative") is True for record in target_records
        ),
        "v21_0_all_commands_require_idempotency": any(
            record.get("v21_0_all_commands_require_idempotency") is True for record in target_records
        ),
        "v21_0_all_commands_require_correlation": any(
            record.get("v21_0_all_commands_require_correlation") is True for record in target_records
        ),
        "v21_0_runtime_authority_blocked_response": any(
            record.get("v21_0_runtime_authority_blocked_response") is True for record in target_records
        ),
        "v21_0_websocket_authoritative": any(
            record.get("v21_0_websocket_authoritative") is True for record in target_records
        ),
        "v22_0_product_pack_contract_kit_valid": any(
            record.get("v22_0_product_pack_contract_kit_valid") is True for record in target_records
        ),
        "v22_0_template_count": max(
            [int(record.get("v22_0_template_count", 0) or 0) for record in target_records] or [0]
        ),
        "v22_0_direct_database_access_allowed": any(
            record.get("v22_0_direct_database_access_allowed") is True for record in target_records
        ),
        "v22_0_hidden_shared_state_allowed": any(
            record.get("v22_0_hidden_shared_state_allowed") is True for record in target_records
        ),
        "v22_0_runtime_authority_granted_count": max(
            [int(record.get("v22_0_runtime_authority_granted_count", 0) or 0) for record in target_records]
            or [0]
        ),
        "v23_0_adapter_evidence_contract_kit_valid": any(
            record.get("v23_0_adapter_evidence_contract_kit_valid") is True for record in target_records
        ),
        "v23_0_adapter_contract_count": max(
            [int(record.get("v23_0_adapter_contract_count", 0) or 0) for record in target_records] or [0]
        ),
        "v23_0_live_invocation_allowed_count": max(
            [int(record.get("v23_0_live_invocation_allowed_count", 0) or 0) for record in target_records] or [0]
        ),
        "v23_0_sample_evidence_present": any(
            record.get("v23_0_sample_evidence_present") is True for record in target_records
        ),
        "v24_0_governance_store_logical_api_valid": any(
            record.get("v24_0_governance_store_logical_api_valid") is True for record in target_records
        ),
        "v24_0_storage_backend_selected": any(
            record.get("v24_0_storage_backend_selected") is True for record in target_records
        ),
        "v24_0_direct_database_access_allowed": any(
            record.get("v24_0_direct_database_access_allowed") is True for record in target_records
        ),
        "v24_0_delete_operation_allowed": any(
            record.get("v24_0_delete_operation_allowed") is True for record in target_records
        ),
        "v24_0_projection_rebuild_required": any(
            record.get("v24_0_projection_rebuild_required") is True for record in target_records
        ),
        "v25_0_event_recovery_contract_v2_valid": any(
            record.get("v25_0_event_recovery_contract_v2_valid") is True for record in target_records
        ),
        "v25_0_event_type_count": max(
            [int(record.get("v25_0_event_type_count", 0) or 0) for record in target_records] or [0]
        ),
        "v25_0_websocket_authoritative": any(
            record.get("v25_0_websocket_authoritative") is True for record in target_records
        ),
        "v25_0_events_mutate_business_state": any(
            record.get("v25_0_events_mutate_business_state") is True for record in target_records
        ),
        "v25_0_rest_event_log_required": any(
            record.get("v25_0_rest_event_log_required") is True for record in target_records
        ),
        "v25_0_reconnect_recovery_required": any(
            record.get("v25_0_reconnect_recovery_required") is True for record in target_records
        ),
        "v25_0_contract_closure_valid": any(
            record.get("v25_0_contract_closure_valid") is True for record in target_records
        ),
        "v25_0_closure_gate_complete_count": max(
            [int(record.get("v25_0_closure_gate_complete_count", 0) or 0) for record in target_records] or [0]
        ),
        "v25_0_closure_gate_count": max(
            [int(record.get("v25_0_closure_gate_count", 0) or 0) for record in target_records] or [0]
        ),
        "v26_0_certification_workflow_valid": any(
            record.get("v26_0_certification_workflow_valid") is True for record in target_records
        ),
        "v26_0_certified_count": max(
            [int(record.get("v26_0_certified_count", 0) or 0) for record in target_records] or [0]
        ),
        "v26_0_runtime_invocation_allowed_count": max(
            [int(record.get("v26_0_runtime_invocation_allowed_count", 0) or 0) for record in target_records]
            or [0]
        ),
        "v26_0_evidence_complete_count": max(
            [int(record.get("v26_0_evidence_complete_count", 0) or 0) for record in target_records] or [0]
        ),
        "v27_0_runtime_authority_gate_contract_valid": any(
            record.get("v27_0_runtime_authority_gate_contract_valid") is True for record in target_records
        ),
        "v27_0_runtime_authority_granted": any(
            record.get("v27_0_runtime_authority_granted") is True for record in target_records
        ),
        "v27_0_negative_fixtures_block_authority": any(
            record.get("v27_0_negative_fixtures_block_authority") is True for record in target_records
        ),
        "v27_0_required_live_evidence_count": max(
            [int(record.get("v27_0_required_live_evidence_count", 0) or 0) for record in target_records] or [0]
        ),
        "v28_0_cost_usage_evidence_contract_valid": any(
            record.get("v28_0_cost_usage_evidence_contract_valid") is True for record in target_records
        ),
        "v28_0_billing_integration_enabled": any(
            record.get("v28_0_billing_integration_enabled") is True for record in target_records
        ),
        "v28_0_usage_record_type_count": max(
            [int(record.get("v28_0_usage_record_type_count", 0) or 0) for record in target_records] or [0]
        ),
        "v28_0_live_invocation_observed_count": max(
            [int(record.get("v28_0_live_invocation_observed_count", 0) or 0) for record in target_records]
            or [0]
        ),
        "v29_0_semantic_projection_contract_valid": any(
            record.get("v29_0_semantic_projection_contract_valid") is True for record in target_records
        ),
        "v29_0_direct_database_access_allowed": any(
            record.get("v29_0_direct_database_access_allowed") is True for record in target_records
        ),
        "v29_0_hidden_shared_state_allowed": any(
            record.get("v29_0_hidden_shared_state_allowed") is True for record in target_records
        ),
        "v29_0_runtime_context_exchange_authorized": any(
            record.get("v29_0_runtime_context_exchange_authorized") is True for record in target_records
        ),
        "v29_0_all_projections_require_approval": any(
            record.get("v29_0_all_projections_require_approval") is True for record in target_records
        ),
        "v29_0_all_projections_have_policy_evidence": any(
            record.get("v29_0_all_projections_have_policy_evidence") is True for record in target_records
        ),
        "v30_0_product_pack_developer_kit_valid": any(
            record.get("v30_0_product_pack_developer_kit_valid") is True for record in target_records
        ),
        "v30_0_example_product_count": max(
            [int(record.get("v30_0_example_product_count", 0) or 0) for record in target_records] or [0]
        ),
        "v30_0_runtime_authority_granted_count": max(
            [int(record.get("v30_0_runtime_authority_granted_count", 0) or 0) for record in target_records]
            or [0]
        ),
        "v30_0_direct_database_access_allowed": any(
            record.get("v30_0_direct_database_access_allowed") is True for record in target_records
        ),
        "v30_0_platform_operating_model_closure_valid": any(
            record.get("v30_0_platform_operating_model_closure_valid") is True for record in target_records
        ),
        "v30_0_closure_gate_complete_count": max(
            [int(record.get("v30_0_closure_gate_complete_count", 0) or 0) for record in target_records] or [0]
        ),
        "v30_0_closure_gate_count": max(
            [int(record.get("v30_0_closure_gate_count", 0) or 0) for record in target_records] or [0]
        ),
        "v31_0_compatibility_versioning_valid": any(
            record.get("v31_0_compatibility_versioning_valid") is True for record in target_records
        ),
        "v31_0_versioned_contract_type_count": max(
            [int(record.get("v31_0_versioned_contract_type_count", 0) or 0) for record in target_records] or [0]
        ),
        "v31_0_breaking_change_requires_major": any(
            record.get("v31_0_breaking_change_requires_major") is True for record in target_records
        ),
        "v31_0_deprecated_requires_replacement": any(
            record.get("v31_0_deprecated_requires_replacement") is True for record in target_records
        ),
        "v32_0_policy_test_pack_framework_valid": any(
            record.get("v32_0_policy_test_pack_framework_valid") is True for record in target_records
        ),
        "v32_0_fixture_count": max(
            [int(record.get("v32_0_fixture_count", 0) or 0) for record in target_records] or [0]
        ),
        "v32_0_deterministic_policy_first": any(
            record.get("v32_0_deterministic_policy_first") is True for record in target_records
        ),
        "v32_0_ai_policy_override_allowed": any(
            record.get("v32_0_ai_policy_override_allowed") is True for record in target_records
        ),
        "v32_0_required_outcomes_covered": any(
            record.get("v32_0_required_outcomes_covered") is True for record in target_records
        ),
        "v33_0_product_pack_cli_scaffold_valid": any(
            record.get("v33_0_product_pack_cli_scaffold_valid") is True for record in target_records
        ),
        "v33_0_command_count": max(
            [int(record.get("v33_0_command_count", 0) or 0) for record in target_records] or [0]
        ),
        "v33_0_no_code_builder": any(record.get("v33_0_no_code_builder") is True for record in target_records),
        "v33_0_runtime_authority_default": next(
            (
                record.get("v33_0_runtime_authority_default")
                for record in target_records
                if record.get("v33_0_runtime_authority_default")
            ),
            "not_generated",
        ),
        "v33_0_direct_database_access_allowed": any(
            record.get("v33_0_direct_database_access_allowed") is True for record in target_records
        ),
        "v33_0_runtime_authority_creating_command_count": max(
            [
                int(record.get("v33_0_runtime_authority_creating_command_count", 0) or 0)
                for record in target_records
            ]
            or [0]
        ),
        "v34_0_case_evidence_query_contract_valid": any(
            record.get("v34_0_case_evidence_query_contract_valid") is True for record in target_records
        ),
        "v34_0_query_resource_count": max(
            [int(record.get("v34_0_query_resource_count", 0) or 0) for record in target_records] or [0]
        ),
        "v34_0_rest_authoritative": any(
            record.get("v34_0_rest_authoritative") is True for record in target_records
        ),
        "v34_0_production_backend_selected": any(
            record.get("v34_0_production_backend_selected") is True for record in target_records
        ),
        "v34_0_direct_database_access_allowed": any(
            record.get("v34_0_direct_database_access_allowed") is True for record in target_records
        ),
        "v35_0_governance_dashboard_data_contract_valid": any(
            record.get("v35_0_governance_dashboard_data_contract_valid") is True for record in target_records
        ),
        "v35_0_dashboard_section_count": max(
            [int(record.get("v35_0_dashboard_section_count", 0) or 0) for record in target_records] or [0]
        ),
        "v35_0_derived_from_rest_evidence": any(
            record.get("v35_0_derived_from_rest_evidence") is True for record in target_records
        ),
        "v35_0_dashboard_is_source_of_truth": any(
            record.get("v35_0_dashboard_is_source_of_truth") is True for record in target_records
        ),
        "v35_0_websocket_authoritative": any(
            record.get("v35_0_websocket_authoritative") is True for record in target_records
        ),
        "v35_0_blocked_claims_visible": any(
            record.get("v35_0_blocked_claims_visible") is True for record in target_records
        ),
        "v35_0_usability_governance_closure_valid": any(
            record.get("v35_0_usability_governance_closure_valid") is True for record in target_records
        ),
        "v35_0_closure_gate_complete_count": max(
            [int(record.get("v35_0_closure_gate_complete_count", 0) or 0) for record in target_records] or [0]
        ),
        "v35_0_closure_gate_count": max(
            [int(record.get("v35_0_closure_gate_count", 0) or 0) for record in target_records] or [0]
        ),
        "v36_0_product_pack_authoring_ux_valid": any(
            record.get("v36_0_product_pack_authoring_ux_valid") is True for record in target_records
        ),
        "v36_0_authoring_state_count": max(
            [int(record.get("v36_0_authoring_state_count", 0) or 0) for record in target_records] or [0]
        ),
        "v36_0_required_panel_count": max(
            [int(record.get("v36_0_required_panel_count", 0) or 0) for record in target_records] or [0]
        ),
        "v36_0_all_transitions_require_rest": any(
            record.get("v36_0_all_transitions_require_rest") is True for record in target_records
        ),
        "v36_0_rest_authoritative": any(
            record.get("v36_0_rest_authoritative") is True for record in target_records
        ),
        "v36_0_websocket_authoritative": any(
            record.get("v36_0_websocket_authoritative") is True for record in target_records
        ),
        "v36_0_broad_no_code_builder": any(
            record.get("v36_0_broad_no_code_builder") is True for record in target_records
        ),
        "v36_0_direct_database_access_allowed": any(
            record.get("v36_0_direct_database_access_allowed") is True for record in target_records
        ),
        "v37_0_governance_review_queue_valid": any(
            record.get("v37_0_governance_review_queue_valid") is True for record in target_records
        ),
        "v37_0_filter_count": max(
            [int(record.get("v37_0_filter_count", 0) or 0) for record in target_records] or [0]
        ),
        "v37_0_required_evidence_count": max(
            [int(record.get("v37_0_required_evidence_count", 0) or 0) for record in target_records] or [0]
        ),
        "v37_0_reviewer_action_count": max(
            [int(record.get("v37_0_reviewer_action_count", 0) or 0) for record in target_records] or [0]
        ),
        "v37_0_solo_maintainer_exception_visible": any(
            record.get("v37_0_solo_maintainer_exception_visible") is True for record in target_records
        ),
        "v37_0_approval_automation_allowed": any(
            record.get("v37_0_approval_automation_allowed") is True for record in target_records
        ),
        "v38_0_capability_lineage_explorer_valid": any(
            record.get("v38_0_capability_lineage_explorer_valid") is True for record in target_records
        ),
        "v38_0_lineage_resource_count": max(
            [int(record.get("v38_0_lineage_resource_count", 0) or 0) for record in target_records] or [0]
        ),
        "v38_0_version_trace_example_count": max(
            [int(record.get("v38_0_version_trace_example_count", 0) or 0) for record in target_records] or [0]
        ),
        "v38_0_capability_version_lineage_required": any(
            record.get("v38_0_capability_version_lineage_required") is True for record in target_records
        ),
        "v38_0_direct_runtime_invocation_allowed": any(
            record.get("v38_0_direct_runtime_invocation_allowed") is True for record in target_records
        ),
        "v38_0_all_traces_have_evidence": any(
            record.get("v38_0_all_traces_have_evidence") is True for record in target_records
        ),
        "v39_0_replay_workspace_valid": any(
            record.get("v39_0_replay_workspace_valid") is True for record in target_records
        ),
        "v39_0_replay_input_count": max(
            [int(record.get("v39_0_replay_input_count", 0) or 0) for record in target_records] or [0]
        ),
        "v39_0_replay_output_count": max(
            [int(record.get("v39_0_replay_output_count", 0) or 0) for record in target_records] or [0]
        ),
        "v39_0_rest_recovery_endpoint_count": max(
            [int(record.get("v39_0_rest_recovery_endpoint_count", 0) or 0) for record in target_records] or [0]
        ),
        "v39_0_drift_comparison_required": any(
            record.get("v39_0_drift_comparison_required") is True for record in target_records
        ),
        "v39_0_evidence_references_required": any(
            record.get("v39_0_evidence_references_required") is True for record in target_records
        ),
        "v39_0_websocket_authoritative": any(
            record.get("v39_0_websocket_authoritative") is True for record in target_records
        ),
        "v39_0_runtime_execution_allowed": any(
            record.get("v39_0_runtime_execution_allowed") is True for record in target_records
        ),
        "v39_0_side_effects_allowed": any(
            record.get("v39_0_side_effects_allowed") is True for record in target_records
        ),
        "v40_0_usability_acceptance_pack_valid": any(
            record.get("v40_0_usability_acceptance_pack_valid") is True for record in target_records
        ),
        "v40_0_usability_surface_count": max(
            [int(record.get("v40_0_usability_surface_count", 0) or 0) for record in target_records] or [0]
        ),
        "v40_0_rest_authoritative": any(
            record.get("v40_0_rest_authoritative") is True for record in target_records
        ),
        "v40_0_websocket_authoritative": any(
            record.get("v40_0_websocket_authoritative") is True for record in target_records
        ),
        "v40_0_evidence_backed": any(record.get("v40_0_evidence_backed") is True for record in target_records),
        "v40_0_runtime_remains_blocked": any(
            record.get("v40_0_runtime_remains_blocked") is True for record in target_records
        ),
        "v40_0_closure_gate_complete_count": max(
            [int(record.get("v40_0_closure_gate_complete_count", 0) or 0) for record in target_records] or [0]
        ),
        "v40_0_closure_gate_count": max(
            [int(record.get("v40_0_closure_gate_count", 0) or 0) for record in target_records] or [0]
        ),
        "pre_runtime_completion_scope_percent": 100.0 if pre_runtime_completion_scope_complete else 0.0,
        "pre_runtime_completion_scope_label": "complete_runtime_blocked"
        if pre_runtime_completion_scope_complete
        else "incomplete_runtime_blocked",
        "implementation_evidence_percent": readiness["implementation_evidence_percent"],
        "target_repo_evidence_percent": target_evidence["target_repo_evidence_percent"],
        "readiness_claim": "DIP contract skeleton and first-wedge evidence loop ready" if policy_ready else "DIP governance skeleton incomplete",
        "approver_subject": target_evidence.get("records", [{}])[0].get("approver_subject", "not_generated")
        if target_evidence.get("records")
        else "not_generated",
        "blocked_claims": [
            "DIP deterministic policy engine is ready",
            "DIP computed simulation and diff are ready",
            "DIP durable immutable case store is ready",
            "DIP identity-backed approvals are ready",
            "DIP release management is ready",
            "DIP independent human review was observed",
            "DIP live external decision approval system is observed",
            "DIP production durable case store backend is observed",
            "DIP live identity authority is ready",
            "DIP live approval provider is ready",
            "DIP production case store live backend is ready",
            "DIP controlled runtime execution is authorized",
            "DIP platform production readiness is complete",
            "DIP live decision approval provider is ready",
            "DIP production durable case store is ready",
            "DIP production promotion chain is ready",
            "DIP controlled runtime pilot is authorized",
            "DIP marketplace runtime invocation is authorized",
            "DIP shared context runtime exchange is authorized",
            "DIP production decision authority is granted",
            "DIP completion plan live prerequisites are all satisfied",
            *(["DIP main updates are governed without admin bypass"] if not v0_7_complete else []),
            "DIP requires microservice deployment topology on day one",
            "DIP WebSocket events are authoritative",
            "ML services are the DIP platform foundation",
            "EDI is the universal governance store for every DIP product",
            "DIP shared service certification evidence is complete",
            "DIP marketplace capability runtime execution is authorized",
            "DIP runtime integration is authorized",
            "DIP production decision execution is authorized",
        ],
    }


def build_payloads(
    root: Path,
    generated_at: str,
    existing_target_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    config = dip_config(root)
    payloads = {
        "governance-policy": governance_policy_payload(config, generated_at),
        "wedge-readiness": wedge_readiness_payload(config, generated_at),
        "implementation-backlog": implementation_backlog_payload(root, generated_at),
        "implementation-evidence": implementation_evidence_payload(config, generated_at),
        "autopilot-lanes": autopilot_lanes_payload(config, generated_at),
        "target-evidence": target_evidence_payload(root, generated_at, existing_target_evidence),
    }
    payloads["v0.2-backlog"] = v0_2_backlog_payload(root, generated_at)
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
    v0_2_backlog = payloads["v0.2-backlog"]
    evidence = payloads["implementation-evidence"]
    autopilot = payloads["autopilot-lanes"]
    target_evidence = payloads["target-evidence"]
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
        out / "v0.2-backlog.md",
        [
            "# DIP v0.2 Backlog",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Milestone: `{v0_2_backlog['milestone']}`",
            f"Source boundary: `{v0_2_backlog['source_boundary']}`",
            f"Runtime execution allowed: `{v0_2_backlog['runtime_execution_allowed']}`",
            f"Release authority allowed: `{v0_2_backlog['release_authority_allowed']}`",
            f"Backlog defined: `{v0_2_backlog['defined_percent']}%`",
            f"Slices: `{v0_2_backlog['defined_slice_count']} / {v0_2_backlog['slice_count']}`",
            f"Safe parallel groups: `{', '.join(v0_2_backlog['safe_parallel_groups'])}`",
            f"Serialized groups: `{', '.join(v0_2_backlog['serialized_groups'])}`",
            "",
            *render_table(v0_2_backlog["records"], ["id", "status", "allowed_autonomy", "parallelization_group", "depends_on"]),
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
        out / "target-evidence.md",
        [
            "# DIP Target Evidence",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Target repo evidence: `{target_evidence['target_repo_evidence_percent']}%`",
            f"Target repo governance clean: `{target_evidence['target_repo_governance_clean_percent']}%`",
            f"Runtime authority granted: `{target_evidence['runtime_authority_granted']}`",
            f"Evidence preserved for drift check: `{target_evidence['evidence_preserved_for_drift_check']}`",
            "",
            *render_table(
                target_evidence["records"],
                [
                    "target_id",
                    "repo_role",
                    "repo_exists",
                    "remote_repo_observed",
                    "branch_protection_observed",
                    "required_status_check_observed",
                    "ci_run_observed",
                    "release_tag_observed",
                    "release_workflow_observed",
                    "release_acceptance_passed",
                    "release_acceptance_commit_matches_tag",
                    "github_release_artifact_observed",
                    "approver_subject",
                    "main_update_bypass_observed",
                    "validation_passed",
                    "trust_loop_complete",
                    "runtime_execution_requested",
                    "state",
                ],
            ),
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
            f"Maturity claim: `{acceptance['maturity_claim']}`",
            f"Policy readiness: `{acceptance['policy_readiness_percent']}%`",
            f"v0.1 pre-runtime trust-loop skeleton: `{acceptance['v0_1_pre_runtime_trust_loop_skeleton_percent']}%`",
            f"Contract shape evidence: `{acceptance['contract_shape_evidence_percent']}%`",
            f"Implementation backlog defined: `{acceptance['implementation_backlog_defined_percent']}%`",
            f"v0.2 backlog defined: `{acceptance['v0_2_backlog_defined_percent']}%`",
            f"v0.2 backlog status: `{acceptance['v0_2_backlog_status_label']}`",
            f"v0.3 computed policy/diff evidence: `{acceptance['v0_3_computed_policy_diff_evidence_percent']}%`",
            f"v0.3 status: `{acceptance['v0_3_status_label']}`",
            f"v0.4 computed simulation evidence: `{acceptance['v0_4_computed_simulation_evidence_percent']}%`",
            f"v0.4 status: `{acceptance['v0_4_status_label']}`",
            f"v0.5 durable case/approval evidence: `{acceptance['v0_5_durable_case_approval_evidence_percent']}%`",
            f"v0.5 status: `{acceptance['v0_5_status_label']}`",
            f"v0.6 identity/RBAC approval evidence: `{acceptance['v0_6_identity_rbac_approval_evidence_percent']}%`",
            f"v0.6 status: `{acceptance['v0_6_status_label']}`",
            f"v0.7 repository governance evidence: `{acceptance['v0_7_repository_governance_evidence_percent']}%`",
            f"v0.7 status: `{acceptance['v0_7_status_label']}`",
            f"v0.8 release lifecycle evidence: `{acceptance['v0_8_release_lifecycle_evidence_percent']}%`",
            f"v0.8 status: `{acceptance['v0_8_status_label']}`",
            f"v0.9 external identity contract evidence: `{acceptance['v0_9_external_identity_contract_evidence_percent']}%`",
            f"v0.9 status: `{acceptance['v0_9_status_label']}`",
            f"v1.0 durable store contract evidence: `{acceptance['v1_0_durable_store_contract_evidence_percent']}%`",
            f"v1.0 status: `{acceptance['v1_0_status_label']}`",
            f"v1.1 governance enforcement parity: `{acceptance['v1_1_governance_enforcement_parity_percent']}%`",
            f"v1.1 status: `{acceptance['v1_1_status_label']}`",
            f"v1.2 product review surface evidence: `{acceptance['v1_2_product_review_surface_evidence_percent']}%`",
            f"v1.2 status: `{acceptance['v1_2_status_label']}`",
            f"v1.3 multi-domain simulation evidence: `{acceptance['v1_3_multi_domain_simulation_evidence_percent']}%`",
            f"v1.3 status: `{acceptance['v1_3_status_label']}`",
            f"v1.4 capability governance evidence: `{acceptance['v1_4_capability_governance_evidence_percent']}%`",
            f"v1.4 status: `{acceptance['v1_4_status_label']}`",
            f"v1.5 shared context contract evidence: `{acceptance['v1_5_shared_context_contract_evidence_percent']}%`",
            f"v1.5 status: `{acceptance['v1_5_status_label']}`",
            f"v2.0 runtime readiness assessment: `{acceptance['v2_0_runtime_readiness_assessment_percent']}%`",
            f"v2.0 status: `{acceptance['v2_0_status_label']}`",
            f"v2.1 governed exception/schema stability: `{acceptance['v2_1_governed_exception_schema_stability_percent']}%`",
            f"v2.1 status: `{acceptance['v2_1_status_label']}`",
            f"Independent human review observed: `{acceptance['independent_human_review_observed']}`",
            f"v2.2 external approval boundary: `{acceptance['v2_2_external_approval_boundary_percent']}%`",
            f"v2.2 status: `{acceptance['v2_2_status_label']}`",
            f"Live external approval system observed: `{acceptance['live_external_approval_system_observed']}`",
            f"v2.3 durable case store adapter: `{acceptance['v2_3_durable_case_store_adapter_percent']}%`",
            f"v2.3 status: `{acceptance['v2_3_status_label']}`",
            f"Production durable case store backend observed: `{acceptance['production_durable_case_store_backend_observed']}`",
            f"v2.4 evidence store adapter parity: `{acceptance['v2_4_evidence_store_adapter_parity_percent']}%`",
            f"v2.4 status: `{acceptance['v2_4_status_label']}`",
            f"Adapter runtime backend invoked: `{acceptance['adapter_runtime_backend_invoked']}`",
            f"v2.5 policy engine hardening: `{acceptance['v2_5_policy_engine_hardening_percent']}%`",
            f"v2.5 status: `{acceptance['v2_5_status_label']}`",
            f"Policy engine runtime authority observed: `{acceptance['policy_engine_runtime_authority_observed']}`",
            f"v2.6 external approval adapter: `{acceptance['v2_6_external_approval_adapter_percent']}%`",
            f"v2.6 status: `{acceptance['v2_6_status_label']}`",
            f"External approval adapter live system observed: `{acceptance['external_approval_adapter_live_system_observed']}`",
            f"External approval adapter AI approval allowed: `{acceptance['external_approval_adapter_ai_approval_allowed']}`",
            f"v2.7 live identity/RBAC: `{acceptance['v2_7_live_identity_rbac_percent']}%`",
            f"v2.7 status: `{acceptance['v2_7_status_label']}`",
            f"Live identity RBAC provider: `{acceptance['live_identity_rbac_provider']}`",
            f"Live identity RBAC subject: `{acceptance['live_identity_rbac_subject']}`",
            f"Live identity RBAC repository permission: `{acceptance['live_identity_rbac_repository_permission']}`",
            f"Live identity RBAC MFA claim observed: `{acceptance['live_identity_rbac_mfa_claim_observed']}`",
            f"v2.8 durable evidence backend: `{acceptance['v2_8_durable_evidence_backend_percent']}%`",
            f"v2.8 status: `{acceptance['v2_8_status_label']}`",
            f"Durable evidence backend runtime invoked: `{acceptance['durable_evidence_backend_runtime_invoked']}`",
            f"v2.9 release promotion/rollback: `{acceptance['v2_9_release_promotion_rollback_percent']}%`",
            f"v2.9 status: `{acceptance['v2_9_status_label']}`",
            f"Production deployment executed: `{acceptance['prod_deployment_executed']}`",
            f"v3.0 pre-runtime GA: `{acceptance['v3_0_pre_runtime_ga_percent']}%`",
            f"v3.0 status: `{acceptance['v3_0_status_label']}`",
            f"v3.1 governance closure: `{acceptance['v3_1_governance_closure_percent']}%`",
            f"v3.1 status: `{acceptance['v3_1_status_label']}`",
            f"v3.2 external identity integration: `{acceptance['v3_2_external_identity_integration_percent']}%`",
            f"v3.2 status: `{acceptance['v3_2_status_label']}`",
            f"v3.2 external identity live ready: `{acceptance['v3_2_external_identity_live_ready']}`",
            f"v3.3 external approval system: `{acceptance['v3_3_external_approval_system_percent']}%`",
            f"v3.3 status: `{acceptance['v3_3_status_label']}`",
            f"v3.3 external approval live ready: `{acceptance['v3_3_external_approval_system_live_ready']}`",
            f"v3.4 production case-store boundary: `{acceptance['v3_4_production_case_store_boundary_percent']}%`",
            f"v3.4 status: `{acceptance['v3_4_status_label']}`",
            f"v3.4 production case store live ready: `{acceptance['v3_4_production_case_store_live_ready']}`",
            f"v3.5 runtime control-plane design: `{acceptance['v3_5_runtime_control_plane_design_percent']}%`",
            f"v3.5 status: `{acceptance['v3_5_status_label']}`",
            f"v3.6 advisory runtime pilot: `{acceptance['v3_6_advisory_runtime_pilot_percent']}%`",
            f"v3.6 status: `{acceptance['v3_6_status_label']}`",
            f"v4.0 limited runtime authority gate: `{acceptance['v4_0_limited_runtime_authority_gate_percent']}%`",
            f"v4.0 status: `{acceptance['v4_0_status_label']}`",
            f"v4.0 limited runtime authority granted: `{acceptance['v4_0_limited_runtime_authority_granted']}`",
            f"v4.1 live identity evidence gate: `{acceptance['v4_1_live_identity_evidence_gate_percent']}%`",
            f"v4.1 status: `{acceptance['v4_1_status_label']}`",
            f"v4.1 live identity authority ready: `{acceptance['v4_1_live_identity_authority_ready']}`",
            f"v4.2 live approval provider gate: `{acceptance['v4_2_live_approval_provider_gate_percent']}%`",
            f"v4.2 status: `{acceptance['v4_2_status_label']}`",
            f"v4.2 live approval provider ready: `{acceptance['v4_2_live_approval_provider_ready']}`",
            f"v4.3 production case-store gate: `{acceptance['v4_3_production_case_store_gate_percent']}%`",
            f"v4.3 status: `{acceptance['v4_3_status_label']}`",
            f"v4.3 production case store live ready: `{acceptance['v4_3_production_case_store_live_ready']}`",
            f"v4.4 release promotion execution gate: `{acceptance['v4_4_release_promotion_execution_gate_percent']}%`",
            f"v4.4 status: `{acceptance['v4_4_status_label']}`",
            f"v4.4 production deployment executed: `{acceptance['v4_4_prod_deployment_executed']}`",
            f"v5.0 governed advisory runtime: `{acceptance['v5_0_governed_advisory_runtime_percent']}%`",
            f"v5.0 status: `{acceptance['v5_0_status_label']}`",
            f"v5.0 side effects executed: `{acceptance['v5_0_side_effects_executed']}`",
            f"v5.5 controlled runtime execution gate: `{acceptance['v5_5_controlled_runtime_execution_gate_percent']}%`",
            f"v5.5 status: `{acceptance['v5_5_status_label']}`",
            f"v5.5 controlled runtime execution authorized: `{acceptance['v5_5_controlled_runtime_execution_authorized']}`",
            f"v6.0 platform hardening assessment: `{acceptance['v6_0_platform_hardening_assessment_percent']}%`",
            f"v6.0 status: `{acceptance['v6_0_status_label']}`",
            f"v6.0 platform production ready: `{acceptance['v6_0_platform_production_ready']}`",
            f"v6.1 live identity authority: `{acceptance['v6_1_live_identity_authority_percent']}%`",
            f"v6.1 status: `{acceptance['v6_1_status_label']}`",
            f"v6.1 live identity authority ready: `{acceptance['v6_1_live_identity_authority_ready']}`",
            f"v6.1 MFA claim observed: `{acceptance['v6_1_mfa_claim_observed']}`",
            f"v6.2 live decision approval provider: `{acceptance['v6_2_live_decision_approval_provider_percent']}%`",
            f"v6.2 status: `{acceptance['v6_2_status_label']}`",
            f"v6.2 live decision approval provider ready: `{acceptance['v6_2_live_decision_approval_provider_ready']}`",
            f"v6.2 AI approval allowed: `{acceptance['v6_2_ai_approval_allowed']}`",
            f"v6.3 production durable case store: `{acceptance['v6_3_production_durable_case_store_percent']}%`",
            f"v6.3 status: `{acceptance['v6_3_status_label']}`",
            f"v6.3 production durable case store ready: `{acceptance['v6_3_production_durable_case_store_ready']}`",
            f"v6.4 production promotion chain: `{acceptance['v6_4_production_promotion_chain_percent']}%`",
            f"v6.4 status: `{acceptance['v6_4_status_label']}`",
            f"v6.4 production promotion ready: `{acceptance['v6_4_production_promotion_ready']}`",
            f"v7.0 controlled runtime pilot: `{acceptance['v7_0_controlled_runtime_pilot_percent']}%`",
            f"v7.0 status: `{acceptance['v7_0_status_label']}`",
            f"v7.0 controlled runtime pilot authorized: `{acceptance['v7_0_controlled_runtime_pilot_authorized']}`",
            f"v7.5 marketplace runtime governance: `{acceptance['v7_5_marketplace_runtime_governance_percent']}%`",
            f"v7.5 status: `{acceptance['v7_5_status_label']}`",
            f"v7.5 marketplace runtime invocation authorized: `{acceptance['v7_5_marketplace_runtime_invocation_authorized']}`",
            f"v7.5 unrestricted marketplace execution allowed: `{acceptance['v7_5_unrestricted_marketplace_execution_allowed']}`",
            f"v8.0 shared context runtime governance: `{acceptance['v8_0_shared_context_runtime_governance_percent']}%`",
            f"v8.0 status: `{acceptance['v8_0_status_label']}`",
            f"v8.0 runtime context exchange authorized: `{acceptance['v8_0_runtime_context_exchange_authorized']}`",
            f"v8.0 direct database access allowed: `{acceptance['v8_0_direct_database_access_allowed']}`",
            f"v9.0 production authority readiness review: `{acceptance['v9_0_production_authority_readiness_review_percent']}%`",
            f"v9.0 status: `{acceptance['v9_0_status_label']}`",
            f"v9.0 production decision authority granted: `{acceptance['v9_0_production_decision_authority_granted']}`",
            f"v10.0 completion plan execution: `{acceptance['v10_0_completion_plan_execution_percent']}%`",
            f"v10.0 status: `{acceptance['v10_0_status_label']}`",
            f"v10.0 reviewed steps: `{acceptance['v10_0_reviewed_step_count']}`",
            f"v10.0 evidence gates complete: `{acceptance['v10_0_evidence_gate_complete_count']}`",
            f"v10.0 live completions achieved: `{acceptance['v10_0_live_completion_achieved_count']}`",
            f"v10.0 blocked live completions: `{acceptance['v10_0_blocked_live_completion_count']}`",
            f"v10.0 product vision alignment valid: `{acceptance['v10_0_product_vision_alignment_valid']}`",
            f"v10.0 AI policy boundary preserved: `{acceptance['v10_0_ai_policy_boundary_preserved']}`",
            f"v10.0 runtime authority blocked: `{acceptance['v10_0_runtime_authority_grant_blocked']}`",
            f"v10.0 production decision authority blocked: `{acceptance['v10_0_production_decision_authority_blocked']}`",
            f"v11.0 API-first platform foundation: `{acceptance['v11_0_api_first_platform_foundation_percent']}%`",
            f"v11.0 status: `{acceptance['v11_0_status_label']}`",
            f"v11.0 platform foundation valid: `{acceptance['v11_0_platform_foundation_valid']}`",
            f"v11.0 REST authoritative: `{acceptance['v11_0_rest_authoritative']}`",
            f"v11.0 WebSocket notification only: `{acceptance['v11_0_websocket_notification_only']}`",
            f"v11.0 topology flexible: `{acceptance['v11_0_topology_flexible']}`",
            f"v11.0 forced microservice topology: `{acceptance['v11_0_forced_microservice_topology']}`",
            f"v11.0 product pack count: `{acceptance['v11_0_product_pack_count']}`",
            f"v11.0 ML capability count: `{acceptance['v11_0_ml_capability_count']}`",
            f"v11.0 complete shared-service certification count: `{acceptance['v11_0_service_certification_evidence_complete_count']}`",
            f"v11.0 EDI universal governance store: `{acceptance['v11_0_edi_universal_governance_store']}`",
            f"v11.0 direct database access allowed: `{acceptance['v11_0_direct_database_access_allowed']}`",
            f"v11.0 runtime authority blocked: `{acceptance['v11_0_runtime_authority_blocked']}`",
            f"v15.0 API foundation: `{acceptance['v15_0_api_foundation_percent']}%`",
            f"v15.0 status: `{acceptance['v15_0_status_label']}`",
            f"v12.0 certified capability count: `{acceptance['v12_0_certified_capability_count']}`",
            f"v12.0 runtime invocation allowed count: `{acceptance['v12_0_runtime_invocation_allowed_count']}`",
            f"v13.0 cross-product database access allowed: `{acceptance['v13_0_cross_product_database_access_allowed']}`",
            f"v13.0 runtime authority granted count: `{acceptance['v13_0_runtime_authority_granted_count']}`",
            f"v14.0 REST authoritative: `{acceptance['v14_0_rest_authoritative']}`",
            f"v14.0 runtime authority default blocked: `{acceptance['v14_0_runtime_authority_default_blocked']}`",
            f"v15.0 event recovery valid: `{acceptance['v15_0_event_recovery_contract_valid']}`",
            f"v15.0 WebSocket authoritative: `{acceptance['v15_0_websocket_authoritative']}`",
            f"v15.0 events mutate business state: `{acceptance['v15_0_events_mutate_business_state']}`",
            f"v15.0 REST recovery required: `{acceptance['v15_0_rest_recovery_required']}`",
            f"v15.0 API foundation valid: `{acceptance['v15_0_api_foundation_valid']}`",
            f"v20.0 architecture closure: `{acceptance['v20_0_architecture_closure_percent']}%`",
            f"v20.0 status: `{acceptance['v20_0_status_label']}`",
            f"v16.0 certification evidence packs valid: `{acceptance['v16_0_certification_evidence_packs_valid']}`",
            f"v16.0 certified service count: `{acceptance['v16_0_certified_service_count']}`",
            f"v16.0 runtime invocation allowed count: `{acceptance['v16_0_runtime_invocation_allowed_count']}`",
            f"v17.0 product pack admission valid: `{acceptance['v17_0_product_pack_admission_valid']}`",
            f"v17.0 direct database access allowed: `{acceptance['v17_0_direct_database_access_allowed']}`",
            f"v17.0 hidden shared state allowed: `{acceptance['v17_0_hidden_shared_state_allowed']}`",
            f"v17.0 runtime authority granted count: `{acceptance['v17_0_runtime_authority_granted_count']}`",
            f"v18.0 OpenAPI skeleton valid: `{acceptance['v18_0_openapi_skeleton_valid']}`",
            f"v18.0 REST authoritative: `{acceptance['v18_0_rest_authoritative']}`",
            f"v18.0 runtime authority blocked response: `{acceptance['v18_0_runtime_authority_blocked_response']}`",
            f"v19.0 event recovery fixtures valid: `{acceptance['v19_0_event_recovery_fixtures_valid']}`",
            f"v19.0 WebSocket authoritative: `{acceptance['v19_0_websocket_authoritative']}`",
            f"v19.0 events mutate business state: `{acceptance['v19_0_events_mutate_business_state']}`",
            f"v19.0 all events recoverable: `{acceptance['v19_0_all_events_recoverable']}`",
            f"v20.0 governance store logical schema valid: `{acceptance['v20_0_governance_store_logical_schema_valid']}`",
            f"v20.0 storage backend selected: `{acceptance['v20_0_storage_backend_selected']}`",
            f"v20.0 direct database access allowed: `{acceptance['v20_0_direct_database_access_allowed']}`",
            f"v20.0 append-only required: `{acceptance['v20_0_append_only_required']}`",
            f"v20.0 closure gates complete: `{acceptance['v20_0_closure_gate_complete_count']}/{acceptance['v20_0_closure_gate_count']}`",
            f"v25.0 contract closure: `{acceptance['v25_0_contract_closure_percent']}%`",
            f"v25.0 status: `{acceptance['v25_0_status_label']}`",
            f"v21.0 canonical OpenAPI valid: `{acceptance['v21_0_canonical_openapi_contract_valid']}`",
            f"v21.0 REST authoritative: `{acceptance['v21_0_rest_authoritative']}`",
            f"v21.0 idempotency required: `{acceptance['v21_0_all_commands_require_idempotency']}`",
            f"v21.0 correlation required: `{acceptance['v21_0_all_commands_require_correlation']}`",
            f"v21.0 runtime authority blocked response: `{acceptance['v21_0_runtime_authority_blocked_response']}`",
            f"v21.0 WebSocket authoritative: `{acceptance['v21_0_websocket_authoritative']}`",
            f"v22.0 product-pack kit valid: `{acceptance['v22_0_product_pack_contract_kit_valid']}`",
            f"v22.0 template count: `{acceptance['v22_0_template_count']}`",
            f"v22.0 direct database access allowed: `{acceptance['v22_0_direct_database_access_allowed']}`",
            f"v22.0 hidden shared state allowed: `{acceptance['v22_0_hidden_shared_state_allowed']}`",
            f"v22.0 runtime authority granted count: `{acceptance['v22_0_runtime_authority_granted_count']}`",
            f"v23.0 adapter evidence kit valid: `{acceptance['v23_0_adapter_evidence_contract_kit_valid']}`",
            f"v23.0 adapter contract count: `{acceptance['v23_0_adapter_contract_count']}`",
            f"v23.0 live invocation allowed count: `{acceptance['v23_0_live_invocation_allowed_count']}`",
            f"v24.0 governance-store logical API valid: `{acceptance['v24_0_governance_store_logical_api_valid']}`",
            f"v24.0 storage backend selected: `{acceptance['v24_0_storage_backend_selected']}`",
            f"v24.0 direct database access allowed: `{acceptance['v24_0_direct_database_access_allowed']}`",
            f"v24.0 delete operation allowed: `{acceptance['v24_0_delete_operation_allowed']}`",
            f"v24.0 projection rebuild required: `{acceptance['v24_0_projection_rebuild_required']}`",
            f"v25.0 event recovery v2 valid: `{acceptance['v25_0_event_recovery_contract_v2_valid']}`",
            f"v25.0 event type count: `{acceptance['v25_0_event_type_count']}`",
            f"v25.0 WebSocket authoritative: `{acceptance['v25_0_websocket_authoritative']}`",
            f"v25.0 events mutate business state: `{acceptance['v25_0_events_mutate_business_state']}`",
            f"v25.0 REST event log required: `{acceptance['v25_0_rest_event_log_required']}`",
            f"v25.0 reconnect recovery required: `{acceptance['v25_0_reconnect_recovery_required']}`",
            f"v25.0 closure gates complete: `{acceptance['v25_0_closure_gate_complete_count']}/{acceptance['v25_0_closure_gate_count']}`",
            f"v30.0 platform operating model: `{acceptance['v30_0_platform_operating_model_percent']}%`",
            f"v30.0 status: `{acceptance['v30_0_status_label']}`",
            f"v26.0 certification workflow valid: `{acceptance['v26_0_certification_workflow_valid']}`",
            f"v26.0 certified count: `{acceptance['v26_0_certified_count']}`",
            f"v26.0 runtime invocation allowed count: `{acceptance['v26_0_runtime_invocation_allowed_count']}`",
            f"v27.0 runtime authority gate valid: `{acceptance['v27_0_runtime_authority_gate_contract_valid']}`",
            f"v27.0 runtime authority granted: `{acceptance['v27_0_runtime_authority_granted']}`",
            f"v27.0 negative fixtures block authority: `{acceptance['v27_0_negative_fixtures_block_authority']}`",
            f"v28.0 cost usage evidence valid: `{acceptance['v28_0_cost_usage_evidence_contract_valid']}`",
            f"v28.0 billing integration enabled: `{acceptance['v28_0_billing_integration_enabled']}`",
            f"v28.0 live invocation observed count: `{acceptance['v28_0_live_invocation_observed_count']}`",
            f"v29.0 semantic projection valid: `{acceptance['v29_0_semantic_projection_contract_valid']}`",
            f"v29.0 direct database access allowed: `{acceptance['v29_0_direct_database_access_allowed']}`",
            f"v29.0 runtime context exchange authorized: `{acceptance['v29_0_runtime_context_exchange_authorized']}`",
            f"v30.0 product-pack developer kit valid: `{acceptance['v30_0_product_pack_developer_kit_valid']}`",
            f"v30.0 runtime authority granted count: `{acceptance['v30_0_runtime_authority_granted_count']}`",
            f"v30.0 direct database access allowed: `{acceptance['v30_0_direct_database_access_allowed']}`",
            f"v30.0 closure gates complete: `{acceptance['v30_0_closure_gate_complete_count']}/{acceptance['v30_0_closure_gate_count']}`",
            f"v35.0 usability governance: `{acceptance['v35_0_usability_governance_percent']}%`",
            f"v35.0 status: `{acceptance['v35_0_status_label']}`",
            f"v31.0 compatibility versioning valid: `{acceptance['v31_0_compatibility_versioning_valid']}`",
            f"v31.0 breaking changes require major: `{acceptance['v31_0_breaking_change_requires_major']}`",
            f"v32.0 policy test pack valid: `{acceptance['v32_0_policy_test_pack_framework_valid']}`",
            f"v32.0 AI policy override allowed: `{acceptance['v32_0_ai_policy_override_allowed']}`",
            f"v33.0 product-pack CLI scaffold valid: `{acceptance['v33_0_product_pack_cli_scaffold_valid']}`",
            f"v33.0 no-code builder: `{acceptance['v33_0_no_code_builder']}`",
            f"v33.0 runtime-authority creating commands: `{acceptance['v33_0_runtime_authority_creating_command_count']}`",
            f"v34.0 case evidence query valid: `{acceptance['v34_0_case_evidence_query_contract_valid']}`",
            f"v34.0 production backend selected: `{acceptance['v34_0_production_backend_selected']}`",
            f"v35.0 governance dashboard data valid: `{acceptance['v35_0_governance_dashboard_data_contract_valid']}`",
            f"v35.0 dashboard source of truth: `{acceptance['v35_0_dashboard_is_source_of_truth']}`",
            f"v35.0 WebSocket authoritative: `{acceptance['v35_0_websocket_authoritative']}`",
            f"v35.0 closure gates complete: `{acceptance['v35_0_closure_gate_complete_count']}/{acceptance['v35_0_closure_gate_count']}`",
            f"v40.0 review workspace: `{acceptance['v40_0_review_workspace_percent']}%`",
            f"v40.0 status: `{acceptance['v40_0_status_label']}`",
            f"v36.0 product-pack authoring UX valid: `{acceptance['v36_0_product_pack_authoring_ux_valid']}`",
            f"v36.0 transitions require REST: `{acceptance['v36_0_all_transitions_require_rest']}`",
            f"v36.0 broad no-code builder: `{acceptance['v36_0_broad_no_code_builder']}`",
            f"v37.0 governance review queue valid: `{acceptance['v37_0_governance_review_queue_valid']}`",
            f"v37.0 approval automation allowed: `{acceptance['v37_0_approval_automation_allowed']}`",
            f"v38.0 capability lineage explorer valid: `{acceptance['v38_0_capability_lineage_explorer_valid']}`",
            f"v38.0 direct runtime invocation allowed: `{acceptance['v38_0_direct_runtime_invocation_allowed']}`",
            f"v39.0 replay workspace valid: `{acceptance['v39_0_replay_workspace_valid']}`",
            f"v39.0 runtime execution allowed: `{acceptance['v39_0_runtime_execution_allowed']}`",
            f"v39.0 side effects allowed: `{acceptance['v39_0_side_effects_allowed']}`",
            f"v40.0 usability acceptance pack valid: `{acceptance['v40_0_usability_acceptance_pack_valid']}`",
            f"v40.0 runtime remains blocked: `{acceptance['v40_0_runtime_remains_blocked']}`",
            f"v40.0 WebSocket authoritative: `{acceptance['v40_0_websocket_authoritative']}`",
            f"v40.0 closure gates complete: `{acceptance['v40_0_closure_gate_complete_count']}/{acceptance['v40_0_closure_gate_count']}`",
            f"Pre-runtime completion scope: `{acceptance['pre_runtime_completion_scope_percent']}%`",
            f"Pre-runtime completion label: `{acceptance['pre_runtime_completion_scope_label']}`",
            f"Implementation evidence: `{acceptance['implementation_evidence_percent']}%`",
            f"Target repo evidence: `{acceptance['target_repo_evidence_percent']}%`",
            f"Target repo governance clean: `{acceptance['target_repo_governance_clean_percent']}%`",
            f"Approver subject: `{acceptance.get('approver_subject', 'not_generated')}`",
            f"GitHub repository governance baseline: `{acceptance['github_repository_governance_baseline']}`",
            f"Readiness claim: `{acceptance['readiness_claim']}`",
            "",
            "## Maturity Labels",
            "",
            *[
                f"- {key}: `{value}`"
                for key, value in sorted(acceptance["maturity_status_labels"].items())
            ],
            "",
            "## Platform Readiness Gaps",
            "",
            f"- Deterministic policy engine readiness: `{acceptance['deterministic_policy_engine_readiness_percent']}%`",
            f"- Computed simulation/diff readiness: `{acceptance['computed_simulation_diff_readiness_percent']}%`",
            f"- Durable case store readiness: `{acceptance['durable_case_store_readiness_percent']}%`",
            f"- Identity-backed approval readiness: `{acceptance['identity_backed_approval_readiness_percent']}%`",
            f"- Release management readiness: `{acceptance['release_management_readiness_percent']}%`",
            f"- Runtime execution readiness: `{acceptance['runtime_execution_readiness_percent']}%`",
            f"- Production decision authority: `{acceptance['production_decision_authority_percent']}%`",
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


def build_dip_outputs(
    root: Path,
    out: Path | None = None,
    generated_at: str | None = None,
    existing_target_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    generated = generated_timestamp(generated_at)
    target = out or root / "reports" / "product" / "dip"
    payloads = build_payloads(root, generated, existing_target_evidence)
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
        existing_target_evidence = load_json(target / "exports" / "target-evidence.json")
        build_dip_outputs(root, temp_out, generated_at, existing_target_evidence)
        for filename in DIP_REPORT_FILES:
            current = (target / filename).read_text(encoding="utf-8")
            expected = (temp_out / filename).read_text(encoding="utf-8")
            if current != expected:
                raise SystemExit(f"DIP report drift detected: {filename}")
    return True
