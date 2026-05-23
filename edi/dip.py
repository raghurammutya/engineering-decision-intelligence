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
    runs_response = _gh_api(f"repos/{repo}/actions/runs?event=push&per_page=20")
    runs_body = runs_response["body"] if runs_response["available"] else {}
    workflow_runs = [run for run in runs_body.get("workflow_runs", []) if isinstance(run, dict)]
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
            and release_acceptance.get("durable_evidence_store_policy_observed") is True
            and release_acceptance.get("durable_store_contract_valid") is True
            and release_acceptance.get("production_storage_backend_observed") is False
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
                "external_identity_contract_observed": release_acceptance.get("external_identity_contract_observed")
                is True,
                "external_identity_contract_valid": release_acceptance.get("external_identity_contract_valid") is True,
                "live_external_identity_provider_authenticated": release_acceptance.get(
                    "live_external_identity_provider_authenticated"
                )
                is True,
                "durable_evidence_store_policy_observed": release_acceptance.get(
                    "durable_evidence_store_policy_observed"
                )
                is True,
                "durable_store_contract_valid": release_acceptance.get("durable_store_contract_valid") is True,
                "production_storage_backend_observed": release_acceptance.get("production_storage_backend_observed")
                is True,
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
    release_management_readiness_percent = 45.0
    if v0_8_complete and v0_7_complete:
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
            "simulation_and_diff": "computed_diff_fixture_simulation",
            "replay": "manifest_backed_replay_pre_runtime" if v0_5_complete else "evidence_shaped_not_reproducible",
            "case_store": "append_only_manifest_chain" if v0_5_complete else "file_backed_tamper_evident_not_durable",
            "durable_store": "durable_store_contract_content_addressed_no_production_backend"
            if v1_0_complete
            else "manifest_chain_without_store_contract",
            "approval": "local_identity_rbac_authority_evaluated_external_idp_missing"
            if v0_9_complete
            else "local_identity_rbac_authority_evaluated_external_idp_missing"
            if v0_6_complete
            else "manifest_bound_role_validated_fixture_identity"
            if v0_5_complete
            else "fixture_backed_not_identity_governed",
            "release_management": "tag_and_local_acceptance_present_ci_artifact_missing_admin_bypass_observed"
            if release_governance_gaps and release_artifact_gaps
            else "tag_and_artifact_backed_acceptance_present_admin_bypass_observed"
            if release_governance_gaps
            else "release_lifecycle_policy_artifact_backed_admin_enforced"
            if v0_8_complete and v0_7_complete
            else "admin_enforced_tag_and_artifact_backed_acceptance_present"
            if v0_7_complete
            else "release_tag_and_artifact_backed_acceptance_present",
            "runtime_execution": "blocked_pending_durable_evidence",
            "production_decision_authority": "blocked_pending_durable_evidence",
        },
        "deterministic_policy_engine_readiness_percent": 60.0 if v0_3_complete else 45.0,
        "computed_simulation_diff_readiness_percent": 70.0 if v0_4_complete else 45.0 if v0_3_complete else 10.0,
        "durable_case_store_readiness_percent": 80.0 if v1_0_complete else 60.0 if v0_5_complete else 30.0,
        "identity_backed_approval_readiness_percent": 65.0
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
        "implementation_evidence_percent": readiness["implementation_evidence_percent"],
        "target_repo_evidence_percent": target_evidence["target_repo_evidence_percent"],
        "readiness_claim": "DIP contract skeleton and first-wedge evidence loop ready" if policy_ready else "DIP governance skeleton incomplete",
        "blocked_claims": [
            "DIP deterministic policy engine is ready",
            "DIP computed simulation and diff are ready",
            "DIP durable immutable case store is ready",
            "DIP identity-backed approvals are ready",
            "DIP release management is ready",
            *(["DIP main updates are governed without admin bypass"] if not v0_7_complete else []),
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
            f"Implementation evidence: `{acceptance['implementation_evidence_percent']}%`",
            f"Target repo evidence: `{acceptance['target_repo_evidence_percent']}%`",
            f"Target repo governance clean: `{acceptance['target_repo_governance_clean_percent']}%`",
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
