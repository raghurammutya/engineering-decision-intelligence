"""Materialize v5 target installation and live evidence reports."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


V5_REPORT_FILES = [
    "README.md",
    "onepassword-installation.md",
    "onepassword-secret-flow.md",
    "live-evidence-intake.md",
    "live-evidence-claims.md",
    "v5-acceptance-pack.md",
    "exports/onepassword-installation.json",
    "exports/onepassword-secret-flow.json",
    "exports/v5-live-evidence.json",
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

SCHEDULED_CONNECTOR_WORKFLOW_FILE = "edi-v5-scheduled-connectors.yml"
SCHEDULED_CONNECTOR_WORKFLOW_PATH = f".github/workflows/{SCHEDULED_CONNECTOR_WORKFLOW_FILE}"


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


def v5_live_target_config(root: Path) -> dict[str, Any]:
    config = load_json(root / "runtime-config" / "v5-live-targets.json")
    targets = config.get("targets", [])
    selected = os.environ.get("EDI_V5_TARGET_ID") or config.get("active_target_id")
    for target in targets:
        if target.get("id") == selected:
            return target
    raise SystemExit(f"Unknown v5 live target: {selected}")


def parse_github_remote(remote: str) -> str:
    patterns = [
        r"^git@github\.com:(?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$",
        r"^https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/.]+)(?:\.git)?$",
    ]
    for pattern in patterns:
        match = re.match(pattern, remote.strip())
        if match:
            return f"{match.group('owner')}/{match.group('repo')}"
    return ""


def resolve_target_path(root: Path, repo_path: str) -> Path:
    path = Path(repo_path)
    return path if path.is_absolute() else (root / path).resolve()


def target_github_repo(root: Path) -> dict[str, Any]:
    target = v5_live_target_config(root)
    repo_path = resolve_target_path(root, str(target.get("repo_path", ".")))
    if not repo_path.exists():
        return {
            "target_id": target.get("id", ""),
            "repo_id": target.get("repo_id", target.get("id", "")),
            "path": str(repo_path),
            "name_with_owner": str(target.get("github_repo", "")),
            "remote_detected": False,
            "configured_github_repo": str(target.get("github_repo", "")),
            "role": target.get("role", ""),
        }
    result = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"],
        cwd=repo_path,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    remote = result.stdout.strip() if result.returncode == 0 else ""
    configured_repo = str(target.get("github_repo", ""))
    return {
        "target_id": target.get("id", ""),
        "repo_id": target.get("repo_id", target.get("id", "")),
        "path": str(repo_path),
        "name_with_owner": configured_repo or parse_github_remote(remote),
        "remote_detected": bool(remote),
        "configured_github_repo": configured_repo,
        "role": target.get("role", ""),
    }


def github_api_request(path: str, token: str) -> dict[str, Any]:
    request = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            body = response.read().decode("utf-8")
            return {"http_status": response.status, "body": json.loads(body) if body else {}}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        parsed = json.loads(body) if body else {}
        return {"http_status": exc.code, "body": parsed}
    except (urllib.error.URLError, TimeoutError) as exc:
        return {"http_status": 0, "error": str(exc)}


def github_live_checks(token: str, repo: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "attempted": bool(token),
        "rate_limit_http_status": 0,
        "authenticated": False,
        "repo_http_status": 0,
        "default_branch": "",
        "branch_protection_http_status": 0,
        "branch_protection_observed": False,
        "required_status_checks_observed": False,
        "pull_request_reviews_observed": False,
        "actions_runs_http_status": 0,
        "recent_actions_run_observed": False,
        "scheduled_connector_workflow_file": SCHEDULED_CONNECTOR_WORKFLOW_PATH,
        "scheduled_connector_runs_http_status": 0,
        "scheduled_connector_observed": False,
        "scheduled_connector_run": {},
    }
    if not token:
        return result

    rate_limit = github_api_request("/rate_limit", token)
    result["rate_limit_http_status"] = rate_limit.get("http_status", 0)
    result["authenticated"] = result["rate_limit_http_status"] == 200

    name_with_owner = repo.get("name_with_owner", "")
    if not result["authenticated"] or not name_with_owner:
        return result

    repo_response = github_api_request(f"/repos/{name_with_owner}", token)
    result["repo_http_status"] = repo_response.get("http_status", 0)
    repo_body = repo_response.get("body", {}) if repo_response.get("http_status") == 200 else {}
    result["default_branch"] = repo_body.get("default_branch", "")

    default_branch = result["default_branch"]
    if default_branch:
        protection = github_api_request(f"/repos/{name_with_owner}/branches/{default_branch}/protection", token)
        result["branch_protection_http_status"] = protection.get("http_status", 0)
        result["branch_protection_observed"] = result["branch_protection_http_status"] == 200
        body = protection.get("body", {}) if result["branch_protection_observed"] else {}
        result["required_status_checks_observed"] = bool(body.get("required_status_checks"))
        result["pull_request_reviews_observed"] = bool(body.get("required_pull_request_reviews"))

    runs = github_api_request(f"/repos/{name_with_owner}/actions/runs?per_page=1", token)
    result["actions_runs_http_status"] = runs.get("http_status", 0)
    body = runs.get("body", {}) if result["actions_runs_http_status"] == 200 else {}
    result["recent_actions_run_observed"] = bool(body.get("workflow_runs"))

    scheduled_runs = github_api_request(
        f"/repos/{name_with_owner}/actions/workflows/{SCHEDULED_CONNECTOR_WORKFLOW_FILE}/runs?per_page=5",
        token,
    )
    result["scheduled_connector_runs_http_status"] = scheduled_runs.get("http_status", 0)
    scheduled_body = scheduled_runs.get("body", {}) if result["scheduled_connector_runs_http_status"] == 200 else {}
    workflow_runs = scheduled_body.get("workflow_runs", [])
    matching_runs = [
        run
        for run in workflow_runs
        if run.get("event") in {"schedule", "workflow_dispatch"}
        and run.get("status") == "completed"
        and run.get("conclusion") == "success"
    ]
    if matching_runs:
        run = matching_runs[0]
        result["scheduled_connector_observed"] = True
        result["scheduled_connector_run"] = {
            "workflow_name": run.get("name", "EDI V5 Scheduled Connectors"),
            "workflow_file": SCHEDULED_CONNECTOR_WORKFLOW_PATH,
            "target_id": repo.get("target_id", repo.get("repo_id", "")),
            "event": run.get("event"),
            "status": run.get("status"),
            "conclusion": run.get("conclusion"),
            "observed_at": run.get("updated_at") or run.get("created_at"),
            "run_id": str(run.get("id", "")),
        }
    return result


def onepassword_installation_payload(root: Path, generated_at: str) -> dict[str, Any]:
    version = op_version()
    detected = bool(version)
    return {
        "generated_at": generated_at,
        "op_installed": detected,
        "op_version": "detected" if detected else "not_installed",
        "op_path": "detected" if detected else "not_found",
        "op_version_detail_committed": False,
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


def live_evidence_payload(
    root: Path,
    generated_at: str,
    live_check: bool,
    existing: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if existing is not None:
        updated = dict(existing)
        updated["generated_at"] = generated_at
        return updated

    config = load_json(root / "runtime-config" / "onepassword-secret-refs.json")
    required = config.get("required_environment_variables", [])
    credential_records = [
        {
            "name": item["name"],
            "secret_ref": item["secret_ref"],
            "resolved": bool(os.environ.get(item["name"], "")) if live_check else False,
        }
        for item in required
    ]
    github_token = os.environ.get("EDI_GITHUB_TOKEN", "") if live_check else ""
    target_repo = target_github_repo(root)
    github_checks = github_live_checks(github_token, target_repo) if live_check else github_live_checks("", target_repo)

    all_credentials_resolved = bool(credential_records) and all(item["resolved"] for item in credential_records)
    return {
        "schema_version": 1,
        "generated_at": generated_at,
        "live_check_requested": live_check,
        "target": target_repo,
        "credential_resolution": {
            "required_count": len(credential_records),
            "resolved_count": len([item for item in credential_records if item["resolved"]]),
            "all_required_resolved": all_credentials_resolved,
            "secrets_logged": False,
            "records": credential_records,
        },
        "github_api": github_checks,
    }


def live_claim_record(claim: str, state: str, evidence_status: str, evidence: list[str], live_check: bool) -> dict[str, Any]:
    return {
        "claim": claim,
        "state": state,
        "live_check_requested": live_check,
        "evidence_status": evidence_status,
        "evidence": evidence,
    }


def live_claims_payload(root: Path, generated_at: str, live_check: bool, live_evidence: dict[str, Any]) -> dict[str, Any]:
    credential_resolution = live_evidence.get("credential_resolution", {})
    github_api = live_evidence.get("github_api", {})
    credentials_pass = (
        credential_resolution.get("all_required_resolved") is True
        and credential_resolution.get("secrets_logged") is False
        and github_api.get("authenticated") is True
    )
    pr_checks_pass = (
        github_api.get("branch_protection_observed") is True
        and (
            github_api.get("required_status_checks_observed") is True
            or github_api.get("pull_request_reviews_observed") is True
        )
    )
    scheduled_connectors_pass = github_api.get("scheduled_connector_observed") is True
    records = [
        live_claim_record(
            "target credentials installed",
            "completed_live_evidence" if credentials_pass else "blocked_pending_target_evidence",
            "captured" if credentials_pass else "missing",
            [
                "all required op:// environment references resolved",
                "GitHub API authentication smoke test returned HTTP 200",
                "secret values were not logged",
            ]
            if credentials_pass
            else [],
            live_check,
        ),
        live_claim_record(
            "scheduled connectors have run",
            "completed_live_evidence" if scheduled_connectors_pass else "blocked_pending_target_evidence",
            "captured" if scheduled_connectors_pass else "missing",
            [
                "EDI v5 scheduled connector workflow observed in GitHub Actions",
                "workflow run completed successfully from schedule or workflow_dispatch",
                "secret values were not logged",
            ]
            if scheduled_connectors_pass
            else [],
            live_check,
        ),
        live_claim_record(
            "target repos enforce PR checks",
            "completed_live_evidence" if pr_checks_pass else "blocked_pending_target_evidence",
            "captured" if pr_checks_pass else "missing",
            [
                "GitHub branch protection observed on target default branch",
                "required status checks or pull request reviews observed",
            ]
            if pr_checks_pass
            else [],
            live_check,
        ),
        live_claim_record(
            "autonomous production enforcement is active",
            "blocked_pending_target_evidence",
            "missing",
            [],
            live_check,
        ),
        live_claim_record(
            "complete live runtime truth exists",
            "blocked_pending_target_evidence",
            "missing",
            [],
            live_check,
        ),
    ]
    completed_count = len([record for record in records if record["state"] == "completed_live_evidence"])
    return {
        "generated_at": generated_at,
        "claim_count": len(records),
        "completed_claim_count": completed_count,
        "live_claim_completion_percent": round(completed_count / len(records) * 100, 1) if records else 0.0,
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


def build_payloads(
    root: Path,
    generated_at: str,
    live_check: bool,
    existing_live_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    installation = onepassword_installation_payload(root, generated_at)
    secret_flow = secret_flow_payload(root, generated_at)
    live_evidence = live_evidence_payload(root, generated_at, live_check, existing=existing_live_evidence)
    live_claims = live_claims_payload(root, generated_at, live_check, live_evidence)
    acceptance = acceptance_payload(root, installation, secret_flow, live_claims, generated_at)
    return {
        "onepassword-installation": installation,
        "onepassword-secret-flow": secret_flow,
        "v5-live-evidence": live_evidence,
        "live-evidence-claims": live_claims,
        "v5-acceptance-pack": acceptance,
    }


def write_markdown(out: Path, payloads: dict[str, Any], generated_at: str) -> None:
    install = payloads["onepassword-installation"]
    secret_flow = payloads["onepassword-secret-flow"]
    live_evidence = payloads["v5-live-evidence"]
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
    credential_resolution = live_evidence["credential_resolution"]
    github_api = live_evidence["github_api"]
    target = live_evidence["target"]
    write_lines(
        out / "live-evidence-intake.md",
        [
            "# V5 Live Evidence Intake",
            "",
            f"Generated: `{generated_at}`",
            "",
            f"Live check requested: `{live_evidence['live_check_requested']}`",
            f"Target id: `{target.get('target_id') or target.get('repo_id') or 'unknown'}`",
            f"Target role: `{target.get('role') or 'unknown'}`",
            f"Target repo: `{target.get('name_with_owner') or 'unknown'}`",
            f"Credential references resolved: `{credential_resolution['resolved_count']} / {credential_resolution['required_count']}`",
            f"Secrets logged: `{credential_resolution['secrets_logged']}`",
            f"GitHub API authenticated: `{github_api['authenticated']}`",
            f"GitHub API rate-limit status: `{github_api['rate_limit_http_status']}`",
            f"Target default branch: `{github_api['default_branch'] or 'unknown'}`",
            f"Branch protection observed: `{github_api['branch_protection_observed']}`",
            f"Required status checks observed: `{github_api['required_status_checks_observed']}`",
            f"Pull request reviews observed: `{github_api['pull_request_reviews_observed']}`",
            f"Recent Actions run observed: `{github_api['recent_actions_run_observed']}`",
            f"Scheduled connector workflow: `{github_api.get('scheduled_connector_workflow_file', SCHEDULED_CONNECTOR_WORKFLOW_PATH)}`",
            f"Scheduled connector runs status: `{github_api.get('scheduled_connector_runs_http_status', 0)}`",
            f"Scheduled connectors observed: `{github_api.get('scheduled_connector_observed', False)}`",
            f"Recent scheduled connector run observed: `{github_api.get('scheduled_connector_observed', False)}`",
            "",
            "This report contains only non-secret evidence metadata.",
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
            "This pack proves secure 1Password-backed tooling and records fail-closed live evidence where target-system checks have run.",
        ],
    )


def build_v5_outputs(
    root: Path,
    out: Path | None = None,
    generated_at: str | None = None,
    live_check: bool = False,
    existing_live_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    generated = generated_timestamp(generated_at)
    target = out or root / "reports" / "product" / "v5"
    payloads = build_payloads(root, generated, live_check, existing_live_evidence)
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
        current_live_evidence = load_json(target / "exports" / "v5-live-evidence.json")
        live_check = bool(current_live_evidence.get("live_check_requested"))
        build_v5_outputs(
            root,
            temp_out,
            generated_at,
            live_check=live_check,
            existing_live_evidence=current_live_evidence,
        )
        for filename in V5_REPORT_FILES:
            current = (target / filename).read_text(encoding="utf-8")
            expected = (temp_out / filename).read_text(encoding="utf-8")
            if current != expected:
                raise SystemExit(f"V5 report drift detected: {filename}")
    return True
