#!/usr/bin/env python3
"""Scan a pilot repository for operational-state mutation capability."""

from __future__ import annotations

import argparse
import csv
import fnmatch
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


CANONICAL_COMMANDS = (
    "scripts/envctl.sh",
    "scripts/governance/promote_by_environment.sh",
)

DEFAULT_POLICY: dict[str, Any] = {
    "canonical_commands": list(CANONICAL_COMMANDS),
    "canonical_artifacts": [],
    "accepted_exceptions": [],
    "owner_map": [],
    "readonly_patterns": [],
    "autonomy": {
        "default_by_risk": {
            "critical": "blocked",
            "high": "prepare",
            "medium": "recommend",
            "low": "observe",
        },
        "controlled_execute_when": {
            "risk": "high",
            "canonical_status": ["canonical", "uses_canonical_command"],
            "evidence_status": "present",
        },
    },
}

REPORT_FILES = [
    "README.md",
    "findings.jsonl",
    "operational-state-mutation-registry.csv",
    "operational-state-mutation-registry.md",
    "decision-backlog.md",
    "owner-review-queue.md",
    "owner-confidence-map.md",
    "autonomy-mode-summary.md",
    "repository-state-summary.md",
    "github-protection-findings.md",
    "github-control-baseline-assessment.md",
    "control-remediation-tracker.md",
    "policy-coverage-report.md",
    "evidence-quality-map.md",
    "risk-explanation-map.md",
    "executive-decision-summary.md",
    "finding-family-summary.md",
    "decision-insight-clusters.md",
    "false-positive-candidates.md",
    "owner-assignment-plan.md",
    "remediation-playbook-map.md",
    "drift-from-baseline.md",
    "pr-risk-summary.md",
    "graph/entities.json",
    "graph/relationships.json",
    "exports/owner-backlog.json",
    "exports/owner-backlog.csv",
    "exports/owner-workflows.json",
    "exports/executive-decisions.json",
    "exports/decision-clusters.json",
    "exports/remediation-packs.json",
    "baseline-history/latest.json",
    "manifest.json",
]

PLAYBOOKS = {
    "direct_prod_deploy": "docs/playbooks/direct-prod-deploy-workflow.md",
    "db_migration": "docs/playbooks/db-migration-script.md",
    "github_environment_protection": "docs/playbooks/github-production-environment-protection.md",
    "ownerless_high_risk": "docs/playbooks/ownerless-high-risk-automation.md",
    "accepted_exception": "docs/playbooks/accepted-exception-renewal.md",
}

ENV_PATTERNS = {
    "prod": re.compile(r"\b(prod|production)\b", re.IGNORECASE),
    "staging": re.compile(r"\bstaging\b", re.IGNORECASE),
    "test": re.compile(r"\btest\b", re.IGNORECASE),
    "dev": re.compile(r"\bdev(elopment)?\b", re.IGNORECASE),
}

MUTATION_PATTERNS = {
    "deployment": (
        r"\bdeploy(ment|ed|ing)?\b",
        r"\bpromote(_by_environment)?\b",
        r"\bdocker\s+compose\s+(up|down|restart|pull|build)",
        r"\bkubectl\b",
        r"\bhelm\b",
        r"\brelease\b",
    ),
    "database": (
        r"\bpsql\b",
        r"\balembic\b",
        r"\bmigrat(e|ion|ions)\b",
        r"\b(schema|database|db)\b",
        r"\b(TRUNCATE|DROP|DELETE|INSERT|UPDATE|ALTER|CREATE)\b",
    ),
    "infrastructure": (
        r"\bterraform\b",
        r"\bansible\b",
        r"\bsystemctl\b",
        r"\bservice\s+(restart|start|stop)",
        r"\bnginx\b",
        r"\bdocker\b",
    ),
    "configuration": (
        r"\bconfig(uration)?\b",
        r"\bsecret(s)?\b",
        r"\bcredential(s)?\b",
        r"\b\.env\b",
        r"\bencrypt(ed|ion)?\b",
        r"\bdecrypt(ed|ion)?\b",
    ),
    "broker_order": (
        r"\bbroker\b",
        r"\border(s)?\b",
        r"\bkite\b",
        r"\btrading\b",
        r"\bALLOW_NON_PROD_BROKER_WRITES\b",
        r"\bNON_PROD_BROKER_WRITE_DISABLED\b",
    ),
    "queue_stream": (
        r"\bqueue\b",
        r"\bredis\b",
        r"\bstream(s|ing)?\b",
        r"\bkafka\b",
        r"\bpubsub\b",
        r"\bcelery\b",
    ),
    "runtime_shell": (
        r"\bssh\b",
        r"\bscp\b",
        r"\brsync\b",
        r"\bsudo\b",
        r"\bshell\b",
        r"\bexec\b",
    ),
    "ai_agent": (
        r"\bagent\b",
        r"\bautonomous\b",
        r"\bcodex\b",
        r"\bclaude\b",
        r"\bprompt\b",
    ),
}

EVIDENCE_PATTERNS = (
    r"\bdeployment-reports/",
    r"\bdocs/qa/",
    r"\breports/",
    r"\bevidence\b",
    r"\bpytest\b",
    r"\btest(s|ing)?\b",
    r"\bhealth\b",
    r"\brollback\b",
)

OWNER_PATTERNS = (
    r"\bCODEOWNERS\b",
    r"\bowner\b",
    r"\bteam\b",
    r"\bservice boundary\b",
    r"\bmaintainer\b",
)

READ_ONLY_NAME_RE = re.compile(
    r"(^|/)(check|audit|validate|verify|generate|capture|find|compare|extract|test|detect|scan|report)[_-]",
    re.IGNORECASE,
)

STRONG_MUTATION_PATTERNS = (
    r"\bdeploy(ment|ed|ing)?\b",
    r"\bpromote_by_environment\b",
    r"\bdocker\s+compose\s+(up|down|restart|pull|build)",
    r"\bkubectl\s+(apply|delete|rollout|scale|patch|set)\b",
    r"\bhelm\s+(upgrade|install|rollback|uninstall)\b",
    r"\bterraform\s+(apply|destroy|import)\b",
    r"\balembic\s+(upgrade|downgrade)\b",
    r"\bpsql\b.*\s(-f|--file)\s",
    r"\b(TRUNCATE|DROP|DELETE|INSERT|UPDATE|ALTER|CREATE)\b",
    r"\bwrite(s|_to)?\b",
    r"\bbackfill\b",
    r"\bbootstrap\b",
    r"\bapply\b",
    r"\bfix\b",
    r"\bcopy\b",
)


@dataclass
class Finding:
    artifact_id: str
    artifact_type: str
    path: str
    mutation_types: list[str]
    environments: list[str]
    risk_level: str
    autonomy_mode: str
    intent: str
    confidence: str
    canonical_status: str
    owner_status: str
    owner: str
    owner_boundary: str
    evidence_status: str
    evidence_quality: str
    exception_status: str
    exception_reason: str
    workflow_triggers: list[str]
    declared_environments: list[str]
    secrets_referenced: list[str]
    called_scripts: list[str]
    blocked_claims: list[str]
    next_action: str
    risk_reasons: list[str] = field(default_factory=list)
    matched_terms: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, str]:
        return {
            "artifact_id": self.artifact_id,
            "artifact_type": self.artifact_type,
            "path": self.path,
            "mutation_types": ",".join(self.mutation_types),
            "environments": ",".join(self.environments),
            "risk_level": self.risk_level,
            "autonomy_mode": self.autonomy_mode,
            "intent": self.intent,
            "confidence": self.confidence,
            "canonical_status": self.canonical_status,
            "owner_status": self.owner_status,
            "owner": self.owner,
            "owner_boundary": self.owner_boundary,
            "evidence_status": self.evidence_status,
            "evidence_quality": self.evidence_quality,
            "exception_status": self.exception_status,
            "exception_reason": self.exception_reason,
            "workflow_triggers": ",".join(self.workflow_triggers),
            "declared_environments": ",".join(self.declared_environments),
            "secrets_referenced": ",".join(self.secrets_referenced),
            "called_scripts": ",".join(self.called_scripts),
            "blocked_claims": " | ".join(self.blocked_claims),
            "next_action": self.next_action,
            "risk_reasons": " | ".join(self.risk_reasons),
            "matched_terms": " | ".join(self.matched_terms[:20]),
        }


def run_git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return result.stdout.strip()


def run_gh(args: list[str], cwd: Path) -> dict | list | None:
    result = subprocess.run(
        ["gh", *args],
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"raw": result.stdout.strip()}


def discover_files(repo: Path, include_tools: bool = False) -> list[tuple[str, Path]]:
    files: list[tuple[str, Path]] = []
    workflow_root = repo / ".github" / "workflows"
    if workflow_root.exists():
        for path in sorted(workflow_root.glob("*.y*ml")):
            files.append(("workflow", path))

    script_root = repo / "scripts"
    if script_root.exists():
        for suffix in ("*.sh", "*.py"):
            for path in sorted(script_root.rglob(suffix)):
                files.append(("script", path))

    tools_root = repo / "tools"
    if include_tools and tools_root.exists():
        for path in sorted(tools_root.rglob("*.py")):
            files.append(("tool", path))

    return files


def read_text(path: Path, max_bytes: int = 400_000) -> str:
    data = path.read_bytes()[:max_bytes]
    return data.decode("utf-8", errors="replace")


def find_environments(text: str, relative_path: str) -> list[str]:
    source = f"{relative_path}\n{text}"
    found = [env for env, pattern in ENV_PATTERNS.items() if pattern.search(source)]
    return found or ["unknown"]


def find_workflow_triggers(text: str) -> list[str]:
    triggers: set[str] = set()
    for trigger in ("workflow_dispatch", "push", "pull_request", "schedule", "workflow_call"):
        if re.search(rf"\b{trigger}\b", text):
            triggers.add(trigger)
    return sorted(triggers)


def find_declared_environments(text: str) -> list[str]:
    declared: set[str] = set()
    for match in re.finditer(r"environment\s*:\s*['\"]?([A-Za-z0-9_-]+)", text):
        declared.add(match.group(1))
    return sorted(declared)


def find_secret_references(text: str) -> list[str]:
    secrets: set[str] = set()
    for match in re.finditer(r"secrets\.([A-Za-z_][A-Za-z0-9_]*)", text):
        secrets.add(match.group(1))
    return sorted(secrets)


def find_called_scripts(text: str) -> list[str]:
    scripts: set[str] = set()
    for match in re.finditer(r"(?:\.\/)?(scripts\/[A-Za-z0-9_./-]+\.(?:sh|py))", text):
        scripts.add(match.group(1))
    return sorted(scripts)


def workflow_permissions(text: str) -> list[str]:
    permissions: set[str] = set()
    for match in re.finditer(r"^\s+([a-z-]+):\s+(read|write|none)\s*$", text, re.MULTILINE):
        permissions.add(f"{match.group(1)}:{match.group(2)}")
    return sorted(permissions)


def find_mutations(text: str, relative_path: str) -> tuple[list[str], list[str]]:
    source = f"{relative_path}\n{text}"
    mutation_types: list[str] = []
    matched_terms: list[str] = []
    for mutation_type, patterns in MUTATION_PATTERNS.items():
        type_matches: list[str] = []
        for pattern in patterns:
            match = re.search(pattern, source, re.IGNORECASE | re.MULTILINE)
            if match:
                type_matches.append(match.group(0))
        if type_matches:
            mutation_types.append(mutation_type)
            matched_terms.extend(f"{mutation_type}:{term}" for term in type_matches[:5])
    return mutation_types, matched_terms


def has_any(patterns: Iterable[str], text: str, relative_path: str) -> bool:
    source = f"{relative_path}\n{text}"
    return any(re.search(pattern, source, re.IGNORECASE | re.MULTILINE) for pattern in patterns)


def evidence_quality(text: str, relative_path: str, evidence_status: str) -> str:
    if evidence_status == "missing":
        return "missing"
    source = f"{relative_path}\n{text}"
    if re.search(r"\brollback\b", source, re.IGNORECASE):
        return "rollback_evidence"
    if re.search(r"\bdeployment-reports/", source, re.IGNORECASE):
        return "promotion_evidence"
    if re.search(r"\bpytest\b|\btest(s|ing)?\b", source, re.IGNORECASE):
        return "test_evidence"
    if re.search(r"\breports/|\bdocs/qa/", source, re.IGNORECASE):
        return "generated_report"
    return "referenced_only"


def strong_mutation_present(text: str, relative_path: str) -> bool:
    return has_any(STRONG_MUTATION_PATTERNS, text, relative_path)


def policy_entries(policy: dict[str, Any], key: str) -> list[dict[str, Any]]:
    entries = policy.get(key) or []
    return [entry for entry in entries if isinstance(entry, dict)]


def policy_patterns(policy: dict[str, Any], key: str) -> list[str]:
    return [str(pattern) for pattern in policy.get(key) or []]


def path_matches(pattern: str, relative_path: str) -> bool:
    if pattern.startswith("re:"):
        return re.search(pattern[3:], relative_path) is not None
    return fnmatch.fnmatch(relative_path, pattern)


def first_matching_entry(policy: dict[str, Any], key: str, relative_path: str) -> dict[str, Any] | None:
    for entry in policy_entries(policy, key):
        pattern = str(entry.get("pattern", ""))
        if pattern and path_matches(pattern, relative_path):
            return entry
    return None


def infer_intent(
    text: str,
    relative_path: str,
    mutation_types: list[str],
    policy: dict[str, Any],
) -> str:
    if relative_path in CANONICAL_COMMANDS:
        return "canonical_control"
    if not mutation_types:
        return "no_mutation_detected"
    if any(path_matches(pattern, relative_path) for pattern in policy_patterns(policy, "readonly_patterns")):
        return "validation_or_reporting"
    if strong_mutation_present(text, relative_path):
        if "deployment" in mutation_types:
            return "operational_mutation"
        return "state_mutation_candidate"
    if READ_ONLY_NAME_RE.search(relative_path):
        return "validation_or_reporting"
    return "ambiguous_operational_access"


def confidence(intent: str, mutation_types: list[str]) -> str:
    if intent in {"canonical_control", "operational_mutation", "state_mutation_candidate"}:
        return "high"
    if intent == "ambiguous_operational_access" and mutation_types:
        return "medium"
    if intent == "validation_or_reporting":
        return "medium"
    return "low"


def merge_policy(base: dict[str, Any], extra: dict[str, Any]) -> dict[str, Any]:
    merged = json.loads(json.dumps(base))
    for key, value in extra.items():
        if key == "include_policy_files":
            continue
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_policy(merged[key], value)
        elif isinstance(value, list) and isinstance(merged.get(key), list):
            merged[key].extend(value)
        else:
            merged[key] = value
    return merged


def load_policy(path: Path | None) -> dict[str, Any]:
    if path is None:
        return DEFAULT_POLICY
    loaded = json.loads(path.read_text(encoding="utf-8"))
    policy = json.loads(json.dumps(DEFAULT_POLICY))
    for include in loaded.get("include_policy_files", []):
        include_path = (path.parent / include).resolve()
        policy = merge_policy(policy, json.loads(include_path.read_text(encoding="utf-8")))
    return merge_policy(policy, loaded)


def included_policy_paths(path: Path | None) -> list[Path]:
    if path is None:
        return []
    loaded = json.loads(path.read_text(encoding="utf-8"))
    paths = [(path.parent / include).resolve() for include in loaded.get("include_policy_files", [])]
    paths.append(path.resolve())
    return paths


def relative_or_absolute(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def canonical_commands(policy: dict[str, Any]) -> list[str]:
    return list(policy.get("canonical_commands") or CANONICAL_COMMANDS)


def canonical_status(
    text: str,
    relative_path: str,
    mutation_types: list[str],
    policy: dict[str, Any],
) -> str:
    normalized = text.replace("./", "")
    commands = canonical_commands(policy)
    canonical_entry = first_matching_entry(policy, "canonical_artifacts", relative_path)
    if canonical_entry:
        return str(canonical_entry.get("status", "canonical"))
    if relative_path in commands:
        return "canonical"
    if any(command in normalized for command in commands):
        return "uses_canonical_command"
    if not mutation_types:
        return "not_mutation_capable"
    return "non_canonical_or_unknown"


def risk_level(
    mutation_types: list[str],
    environments: list[str],
    canonical: str,
    evidence: str,
    owner: str,
    intent: str,
    exception_status: str,
) -> str:
    if not mutation_types:
        return "low"

    envs = set(environments)
    high_impact = {"database", "infrastructure", "configuration", "broker_order"}
    strong_intent = intent in {"canonical_control", "operational_mutation", "state_mutation_candidate"}

    if intent == "validation_or_reporting":
        if "prod" in envs and high_impact.intersection(mutation_types):
            return "medium"
        return "low"

    non_canonical = canonical == "non_canonical_or_unknown"
    if exception_status == "accepted_exception" and "prod" not in envs:
        return "medium"
    if "prod" in envs and strong_intent and non_canonical:
        return "critical"
    if "prod" in envs and strong_intent and evidence == "missing" and non_canonical:
        return "critical"
    if high_impact.intersection(mutation_types):
        return "high"
    if "deployment" in mutation_types and envs.intersection({"staging", "prod"}):
        return "high"
    return "medium"


def risk_reasons(
    mutation_types: list[str],
    environments: list[str],
    canonical: str,
    evidence: str,
    owner: str,
    intent: str,
    exception_status: str,
    matched_terms: list[str],
) -> list[str]:
    reasons: list[str] = []
    normalized_mutations = [item for item in mutation_types if item != "none_detected"]
    if normalized_mutations:
        reasons.append("mutation capability detected: " + ", ".join(normalized_mutations))
    else:
        reasons.append("no operational-state mutation capability detected")
    if environments and environments != ["unknown"]:
        reasons.append("environment evidence: " + ", ".join(environments))
    if canonical == "non_canonical_or_unknown":
        reasons.append("canonical operating path is unknown")
    elif canonical in {"canonical", "uses_canonical_command", "accepted_exception"}:
        reasons.append(f"canonical evidence: {canonical}")
    if owner == "missing_or_unknown":
        reasons.append("owner boundary is missing or unknown")
    if evidence == "missing":
        reasons.append("safety or rollback evidence is missing")
    else:
        reasons.append("evidence reference is present")
    if exception_status == "accepted_exception":
        reasons.append("accepted exception is in policy and needs renewal review")
    if intent != "no_mutation_detected":
        reasons.append(f"intent inference: {intent}")
    if matched_terms:
        reasons.append("matched scanner terms: " + ", ".join(matched_terms[:5]))
    return reasons


def autonomy_mode(
    level: str,
    canonical: str,
    evidence: str,
    policy: dict[str, Any],
    exception_status: str,
) -> str:
    autonomy_policy = policy.get("autonomy") or {}
    controlled = autonomy_policy.get("controlled_execute_when") or {}
    default_by_risk = autonomy_policy.get("default_by_risk") or {}

    if exception_status == "accepted_exception" and level != "critical":
        return "recommend"
    if (
        level == controlled.get("risk")
        and canonical in set(controlled.get("canonical_status") or [])
        and evidence == controlled.get("evidence_status")
    ):
        return "controlled_execute"
    return default_by_risk.get(level, "observe")


def blocked_claims(
    level: str,
    canonical: str,
    owner: str,
    evidence: str,
    exception_status: str,
) -> list[str]:
    claims: list[str] = []
    if canonical == "non_canonical_or_unknown" and exception_status != "accepted_exception":
        claims.append("cannot claim canonical operating path")
    if owner == "missing_or_unknown":
        claims.append("cannot claim owner-approved")
    if evidence == "missing":
        claims.append("cannot claim evidence-backed safety")
    if level in {"high", "critical"}:
        claims.append("cannot claim autonomous execution readiness")
    return claims


def next_action(
    level: str,
    canonical: str,
    owner: str,
    evidence: str,
    exception_status: str,
) -> str:
    if exception_status == "accepted_exception":
        return "review accepted exception and renewal evidence"
    if level == "critical":
        return "block or require controlled owner review before use"
    if canonical == "non_canonical_or_unknown":
        return "map to canonical automation or document exception"
    if owner == "missing_or_unknown":
        return "assign owner boundary"
    if evidence == "missing":
        return "attach or generate validation and rollback evidence"
    if level == "high":
        return "retain controlled execution with evidence"
    if level == "medium":
        return "review before expanding autonomy"
    return "observe"


def scan_file(
    repo: Path,
    artifact_type: str,
    path: Path,
    policy: dict[str, Any] | None = None,
) -> Finding:
    active_policy = policy or DEFAULT_POLICY
    relative_path = path.relative_to(repo).as_posix()
    text = read_text(path)
    mutation_types, matched_terms = find_mutations(text, relative_path)
    environments = find_environments(text, relative_path)
    evidence = "present" if has_any(EVIDENCE_PATTERNS, text, relative_path) else "missing"
    quality = evidence_quality(text, relative_path, evidence)
    owner_entry = first_matching_entry(active_policy, "owner_map", relative_path)
    owner = "present" if owner_entry or has_any(OWNER_PATTERNS, text, relative_path) else "missing_or_unknown"
    owner_name = str(owner_entry.get("owner", "")) if owner_entry else ""
    owner_boundary = str(owner_entry.get("boundary", "")) if owner_entry else ""
    exception_entry = first_matching_entry(active_policy, "accepted_exceptions", relative_path)
    exception_status = "accepted_exception" if exception_entry else "none"
    exception_reason = str(exception_entry.get("reason", "")) if exception_entry else ""
    canonical = canonical_status(text, relative_path, mutation_types, active_policy)
    intent = infer_intent(text, relative_path, mutation_types, active_policy)
    level = risk_level(
        mutation_types,
        environments,
        canonical,
        evidence,
        owner,
        intent,
        exception_status,
    )
    reasons = risk_reasons(
        mutation_types,
        environments,
        canonical,
        evidence,
        owner,
        intent,
        exception_status,
        matched_terms,
    )
    mode = autonomy_mode(level, canonical, evidence, active_policy, exception_status)
    finding_confidence = confidence(intent, mutation_types)
    artifact_id = hashlib.sha1(f"{artifact_type}:{relative_path}".encode()).hexdigest()[:12]
    return Finding(
        artifact_id=artifact_id,
        artifact_type=artifact_type,
        path=relative_path,
        mutation_types=mutation_types or ["none_detected"],
        environments=environments,
        risk_level=level,
        autonomy_mode=mode,
        intent=intent,
        confidence=finding_confidence,
        canonical_status=canonical,
        owner_status=owner,
        owner=owner_name,
        owner_boundary=owner_boundary,
        evidence_status=evidence,
        evidence_quality=quality,
        exception_status=exception_status,
        exception_reason=exception_reason,
        workflow_triggers=find_workflow_triggers(text) if artifact_type == "workflow" else [],
        declared_environments=find_declared_environments(text) if artifact_type == "workflow" else [],
        secrets_referenced=find_secret_references(text),
        called_scripts=find_called_scripts(text) if artifact_type == "workflow" else [],
        blocked_claims=blocked_claims(level, canonical, owner, evidence, exception_status),
        next_action=next_action(level, canonical, owner, evidence, exception_status),
        risk_reasons=reasons,
        matched_terms=matched_terms,
    )


def local_git_state(repo: Path) -> dict[str, object]:
    status_lines = run_git(["status", "--short"], repo).splitlines()
    branch = run_git(["branch", "--show-current"], repo)
    remote = run_git(["remote", "get-url", "origin"], repo)
    ahead_behind = run_git(["rev-list", "--left-right", "--count", "@{u}...HEAD"], repo)
    return {
        "branch": branch,
        "remote": remote,
        "dirty_file_count": len(status_lines),
        "dirty_sample": status_lines[:25],
        "ahead_behind": ahead_behind,
    }


def github_state(repo: Path) -> dict[str, object]:
    repo_info = run_gh(
        [
            "repo",
            "view",
            "--json",
            "nameWithOwner,visibility,defaultBranchRef,url,pushedAt",
        ],
        repo,
    )
    default_branch = None
    name_with_owner = None
    if isinstance(repo_info, dict):
        name_with_owner = repo_info.get("nameWithOwner")
        default_branch_ref = repo_info.get("defaultBranchRef") or {}
        if isinstance(default_branch_ref, dict):
            default_branch = default_branch_ref.get("name")
    branch_protection = None
    environments = None
    if name_with_owner and default_branch:
        branch_protection = run_gh(
            ["api", f"repos/{name_with_owner}/branches/{default_branch}/protection"],
            repo,
        )
    if name_with_owner:
        environments = run_gh(["api", f"repos/{name_with_owner}/environments"], repo)
    return {
        "repo": repo_info,
        "pull_requests": run_gh(
            [
                "pr",
                "list",
                "--state",
                "open",
                "--limit",
                "50",
                "--json",
                "number,title,author,updatedAt,baseRefName,headRefName,isDraft",
            ],
            repo,
        ),
        "workflows": run_gh(["workflow", "list", "--json", "name,path,state"], repo),
        "default_branch_protection": branch_protection,
        "environments": environments,
    }


def enrich_pull_request_files(repo: Path, gh_state: dict[str, object] | None) -> None:
    if not gh_state:
        return
    pull_requests = gh_state.get("pull_requests")
    if not isinstance(pull_requests, list):
        return
    for pull_request in pull_requests:
        number = pull_request.get("number")
        if not number:
            continue
        files = run_gh(
            [
                "pr",
                "view",
                str(number),
                "--json",
                "files",
            ],
            repo,
        )
        if isinstance(files, dict):
            pull_request["files"] = files.get("files") or []


def write_jsonl(path: Path, findings: list[Finding]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for finding in findings:
            handle.write(json.dumps(finding.as_dict(), sort_keys=True) + "\n")


def write_csv(path: Path, findings: list[Finding]) -> None:
    fieldnames = list(findings[0].as_dict().keys()) if findings else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for finding in findings:
            writer.writerow(finding.as_dict())


def counts(findings: list[Finding], field_name: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for finding in findings:
        value = getattr(finding, field_name)
        if isinstance(value, list):
            for item in value:
                result[item] = result.get(item, 0) + 1
        else:
            result[value] = result.get(value, 0) + 1
    return dict(sorted(result.items(), key=lambda item: (-item[1], item[0])))


def write_lines(path: Path, lines: list[str]) -> None:
    while lines and lines[-1] == "":
        lines.pop()
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def source_fingerprint(
    repo_root: Path,
    policy_path: Path | None,
    baseline_path: Path | None = None,
    owner_suggestions_path: Path | None = None,
    control_remediation_path: Path | None = None,
    false_positive_review_path: Path | None = None,
) -> str:
    hasher = hashlib.sha256()
    source_paths = [Path(__file__).resolve(), *included_policy_paths(policy_path)]
    for optional_path in (
        baseline_path,
        owner_suggestions_path,
        control_remediation_path,
        false_positive_review_path,
    ):
        if optional_path is not None:
            source_paths.append(optional_path.resolve())
    for source_path in sorted(set(source_paths), key=lambda item: item.as_posix()):
        hasher.update(relative_or_absolute(source_path, repo_root).encode())
        hasher.update(b"\0")
        if source_path.exists():
            hasher.update(source_path.read_bytes())
        hasher.update(b"\0")
    return hasher.hexdigest()


def finding_family(finding: Finding) -> str:
    path = finding.path.lower()
    mutation_types = set(finding.mutation_types)
    if finding.artifact_type == "workflow" and "deploy" in path:
        return "deploy_workflows"
    if "configuration" in mutation_types or "secret" in path or "config" in path:
        return "config_secret_scripts"
    if "database" in mutation_types or "migration" in path or "migrate" in path:
        return "db_migration_scripts"
    if "broker_order" in mutation_types or "broker" in path or "order" in path:
        return "broker_order_scripts"
    if "backup" in path or "restore" in path:
        return "backup_restore"
    if "governance" in path or "probe" in path:
        return "governance_probes"
    if "qa/" in path or finding.intent == "validation_or_reporting":
        return "qa_readiness_checks"
    if "ai_agent" in mutation_types or "agent" in path or "codex" in path or "claude" in path:
        return "ai_agent_tooling"
    if finding.artifact_type == "workflow":
        return "other_workflows"
    return "other_scripts"


def remediation_playbook(finding: Finding) -> str:
    if finding.exception_status == "accepted_exception":
        return PLAYBOOKS["accepted_exception"]
    if finding.artifact_type == "workflow" and "prod" in finding.environments and finding.autonomy_mode == "blocked":
        return PLAYBOOKS["direct_prod_deploy"]
    if "database" in finding.mutation_types:
        return PLAYBOOKS["db_migration"]
    if finding.owner_status == "missing_or_unknown" and finding.risk_level in {"critical", "high"}:
        return PLAYBOOKS["ownerless_high_risk"]
    return ""


def decision_priority(finding: Finding) -> str:
    if finding.risk_level == "critical" and "prod" in finding.environments:
        return "P0"
    if finding.risk_level == "critical":
        return "P1"
    if finding.risk_level == "high" and finding.owner_status == "missing_or_unknown":
        return "P2"
    if finding.evidence_status == "missing" and finding.risk_level in {"high", "medium"}:
        return "P2"
    if finding.exception_status == "accepted_exception":
        return "P3"
    if finding.risk_level == "high":
        return "P3"
    if finding.intent == "validation_or_reporting":
        return "P4"
    if finding.autonomy_mode == "observe":
        return "P4"
    if finding.risk_level == "medium":
        return "P4"
    return "P5"


def decision_reason(finding: Finding) -> str:
    if decision_priority(finding) == "P0":
        return "blocked production mutation"
    if finding.risk_level == "critical":
        return "critical mutation path"
    if finding.owner_status == "missing_or_unknown" and finding.risk_level == "high":
        return "ownerless high-risk automation"
    if finding.evidence_status == "missing" and finding.risk_level in {"high", "medium"}:
        return "missing evidence"
    if finding.exception_status == "accepted_exception":
        return "accepted exception renewal"
    if finding.intent == "validation_or_reporting":
        return "read-only or validation path"
    return finding.next_action


def policy_coverage(finding: Finding) -> list[str]:
    coverage: list[str] = []
    if finding.owner:
        coverage.append("owner_map")
    if finding.exception_status == "accepted_exception":
        coverage.append("accepted_exception")
    if finding.canonical_status in {"canonical", "uses_canonical_command", "accepted_exception"}:
        coverage.append("canonical_artifact")
    if finding.intent == "validation_or_reporting":
        coverage.append("readonly_pattern")
    if finding.evidence_status == "present":
        coverage.append("evidence_reference")
    return coverage or ["uncovered"]


def gh_environment_entries(gh_state: dict[str, object] | None) -> list[dict[str, Any]]:
    if not gh_state:
        return []
    environments = gh_state.get("environments")
    if not isinstance(environments, dict):
        return []
    entries = environments.get("environments") or []
    return [entry for entry in entries if isinstance(entry, dict)]


def workflow_paths_from_findings(findings: list[Finding]) -> set[str]:
    return {finding.path for finding in findings if finding.artifact_type == "workflow"}


def github_workflow_paths(gh_state: dict[str, object] | None) -> set[str]:
    if not gh_state or not isinstance(gh_state.get("workflows"), list):
        return set()
    return {
        str(workflow.get("path"))
        for workflow in gh_state["workflows"]
        if isinstance(workflow, dict) and workflow.get("path")
    }


def write_github_protection_findings(
    path: Path,
    findings: list[Finding],
    gh_state: dict[str, object] | None,
    generated_at: str,
) -> None:
    lines = [
        "# GitHub Protection Findings",
        "",
        f"Generated: `{generated_at}`",
        "",
        "| Severity | Finding | Evidence | Decision |",
        "| --- | --- | --- | --- |",
    ]

    if not gh_state:
        lines.append("| P2 | GitHub state unavailable | Scanner ran without GitHub enrichment | Run with `--github` |")
        write_lines(path, lines)
        return

    protection = gh_state.get("default_branch_protection")
    if not protection:
        lines.append(
            "| P1 | Default branch protection not visible | GitHub API returned no protection payload | Review branch protection for default branch |"
        )

    prod_envs = [
        env
        for env in gh_environment_entries(gh_state)
        if str(env.get("name", "")).lower() in {"prod", "production"}
    ]
    for env in prod_envs:
        name = env.get("name", "unknown")
        protection_rules = env.get("protection_rules") or []
        if not protection_rules:
            lines.append(
                f"| P0 | `{name}` environment has no protection rules | `protection_rules` is empty | Add required reviewers or deployment protection |"
            )
        if env.get("can_admins_bypass"):
            lines.append(
                f"| P1 | `{name}` allows admin bypass | `can_admins_bypass=true` | Review bypass policy for production environments |"
            )

    mutation_workflows = [
        finding
        for finding in findings
        if finding.artifact_type == "workflow"
        and finding.risk_level in {"critical", "high"}
        and finding.autonomy_mode in {"blocked", "prepare"}
    ]
    for finding in mutation_workflows[:30]:
        lines.append(
            f"| {decision_priority(finding)} | Mutation-capable workflow `{finding.path}` needs protection review | {finding.risk_level}/{finding.autonomy_mode} | Confirm branch and environment protection before execution |"
        )

    stale_remote = sorted(github_workflow_paths(gh_state) - workflow_paths_from_findings(findings))
    for workflow_path in stale_remote:
        lines.append(
            f"| P2 | GitHub workflow `{workflow_path}` is visible remotely but absent locally | workflow list divergence | Reconcile local branch with GitHub default branch |"
        )

    write_lines(path, lines)


def write_policy_coverage_report(path: Path, findings: list[Finding], generated_at: str) -> None:
    coverage_counts: dict[str, int] = {}
    for finding in findings:
        for coverage in policy_coverage(finding):
            coverage_counts[coverage] = coverage_counts.get(coverage, 0) + 1

    high_uncovered = [
        finding
        for finding in findings
        if finding.risk_level in {"critical", "high"} and policy_coverage(finding) == ["uncovered"]
    ]
    ownerless = [finding for finding in findings if finding.owner_status == "missing_or_unknown"]

    lines = [
        "# Policy Coverage Report",
        "",
        f"Generated: `{generated_at}`",
        "",
        "## Coverage Counts",
        "",
    ]
    for key, value in sorted(coverage_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- `{key}`: {value}")

    lines.extend(
        [
            "",
            "## Gaps",
            "",
            f"- Ownerless artifacts: `{len(ownerless)}`",
            f"- High/critical artifacts without policy coverage: `{len(high_uncovered)}`",
            "",
            "## High/Critical Without Policy Coverage",
            "",
            "| Path | Risk | Autonomy | Next Action |",
            "| --- | --- | --- | --- |",
        ]
    )
    for finding in sorted(high_uncovered, key=lambda f: (risk_sort(f.risk_level), f.path))[:100]:
        lines.append(
            f"| `{finding.path}` | {finding.risk_level} | {finding.autonomy_mode} | {finding.next_action} |"
        )
    write_lines(path, lines)


def write_evidence_quality_map(path: Path, findings: list[Finding], generated_at: str) -> None:
    lines = [
        "# Evidence Quality Map",
        "",
        f"Generated: `{generated_at}`",
        "",
        "## Quality Counts",
        "",
    ]
    for key, value in counts(findings, "evidence_quality").items():
        lines.append(f"- `{key}`: {value}")

    lines.extend(
        [
            "",
            "## High-Risk Missing Or Weak Evidence",
            "",
            "| Path | Risk | Evidence Quality | Next Action |",
            "| --- | --- | --- | --- |",
        ]
    )
    weak = [
        finding
        for finding in findings
        if finding.risk_level in {"critical", "high"}
        and finding.evidence_quality in {"missing", "referenced_only", "generated_report"}
    ]
    for finding in sorted(weak, key=lambda f: (risk_sort(f.risk_level), f.evidence_quality, f.path))[:150]:
        lines.append(
            f"| `{finding.path}` | {finding.risk_level} | {finding.evidence_quality} | {finding.next_action} |"
        )
    write_lines(path, lines)


def write_risk_explanation_map(path: Path, findings: list[Finding], generated_at: str) -> None:
    lines = [
        "# Risk Explanation Map",
        "",
        f"Generated: `{generated_at}`",
        "",
        "This view explains why each scanned artifact received its current risk and autonomy classification.",
        "",
        "| Path | Risk | Autonomy | Family | Explanation |",
        "| --- | --- | --- | --- | --- |",
    ]
    for finding in sorted(findings, key=lambda f: (risk_sort(f.risk_level), f.path)):
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{finding.path}`",
                    finding.risk_level,
                    finding.autonomy_mode,
                    finding_family(finding),
                    "<br>".join(finding.risk_reasons[:8]),
                ]
            )
            + " |"
        )
    write_lines(path, lines)


def write_executive_decision_summary(path: Path, findings: list[Finding], generated_at: str) -> None:
    priority_counts: dict[str, int] = {}
    for finding in findings:
        priority = decision_priority(finding)
        priority_counts[priority] = priority_counts.get(priority, 0) + 1

    lines = [
        "# Executive Decision Summary",
        "",
        f"Generated: `{generated_at}`",
        "",
        "## Priority Counts",
        "",
    ]
    for priority, count in sorted(priority_counts.items()):
        lines.append(f"- `{priority}`: {count}")

    lines.extend(
        [
            "",
            "## Top Decisions",
            "",
            "| Priority | Path | Reason | Owner | Decision |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    top = sorted(findings, key=lambda f: (decision_priority(f), risk_sort(f.risk_level), f.path))
    for finding in top[:40]:
        lines.append(
            "| "
            + " | ".join(
                [
                    decision_priority(finding),
                    f"`{finding.path}`",
                    decision_reason(finding),
                    owner_display(finding),
                    finding.next_action,
                ]
            )
            + " |"
        )
    write_lines(path, lines)


def pr_file_risk(filename: str, findings_by_path: dict[str, Finding]) -> tuple[str, str]:
    if filename in findings_by_path:
        finding = findings_by_path[filename]
        return decision_priority(finding), f"{finding.risk_level}/{finding.autonomy_mode}"
    if filename.startswith(".github/workflows/"):
        return "P1", "workflow change"
    if filename.startswith("policies/"):
        return "P1", "policy change"
    if filename.startswith("tools/"):
        return "P2", "scanner/tool change"
    if filename.startswith("reports/"):
        return "P4", "generated report change"
    return "P5", "no direct scanner finding"


def write_pr_risk_summary(
    path: Path,
    findings: list[Finding],
    gh_state: dict[str, object] | None,
    generated_at: str,
) -> None:
    lines = [
        "# Pull Request Risk Summary",
        "",
        f"Generated: `{generated_at}`",
        "",
    ]
    if not gh_state or not isinstance(gh_state.get("pull_requests"), list):
        lines.append("GitHub pull request state unavailable.")
        write_lines(path, lines)
        return

    pull_requests = gh_state.get("pull_requests") or []
    if not pull_requests:
        lines.append("No open pull requests detected.")
        write_lines(path, lines)
        return

    findings_by_path = {finding.path: finding for finding in findings}
    lines.extend(
        [
            "| PR | Title | Risk | Files | Review Needed |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for pull_request in pull_requests:
        files = pull_request.get("files") or []
        filenames = [str(file.get("path") or file.get("filename")) for file in files if isinstance(file, dict)]
        file_risks = [pr_file_risk(filename, findings_by_path) for filename in filenames]
        priority = sorted([risk[0] for risk in file_risks] or ["P5"])[0]
        review = "standard review"
        if priority in {"P0", "P1"}:
            review = "owner and governance review"
        elif priority == "P2":
            review = "scanner/policy review"
        lines.append(
            "| "
            + " | ".join(
                [
                    f"#{pull_request.get('number')}",
                    str(pull_request.get("title", "")),
                    priority,
                    ", ".join(filenames[:10]) or "none",
                    review,
                ]
            )
            + " |"
        )
    write_lines(path, lines)


def load_github_baseline(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_optional_json(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def owner_suggestion(finding: Finding, suggestions: dict[str, Any]) -> tuple[str, str]:
    path_rules = suggestions.get("path_rules") or []
    for rule in path_rules:
        pattern = str(rule.get("pattern", ""))
        if pattern and path_matches(pattern, finding.path):
            return str(rule.get("owner", "")), str(rule.get("boundary", ""))

    family_rules = suggestions.get("family_rules") or {}
    rule = family_rules.get(finding_family(finding)) or {}
    if isinstance(rule, dict):
        return str(rule.get("owner", "")), str(rule.get("boundary", ""))
    return "", ""


def owner_assignment(finding: Finding, suggestions: dict[str, Any]) -> dict[str, Any]:
    suggested_owner, suggested_boundary = owner_suggestion(finding, suggestions)
    if finding.owner:
        return {
            "owner": finding.owner,
            "boundary": finding.owner_boundary,
            "assignment_type": "declared_owner_map",
            "confidence": 1.0,
            "review_action": "confirm owner accepts operational boundary",
        }
    if finding.owner_status == "present":
        return {
            "owner": "embedded_owner_hint",
            "boundary": "owner text present without policy owner-map entry",
            "assignment_type": "embedded_hint",
            "confidence": 0.45,
            "review_action": "convert embedded owner hint into owner-map rule",
        }
    if suggested_owner:
        return {
            "owner": suggested_owner,
            "boundary": suggested_boundary,
            "assignment_type": "inferred_suggestion",
            "confidence": 0.65,
            "review_action": "owner review required before treating suggestion as approved",
        }
    return {
        "owner": "unassigned",
        "boundary": "missing owner boundary",
        "assignment_type": "missing_owner",
        "confidence": 0.0,
        "review_action": "assign accountable owner boundary",
    }


def owner_review_class(finding: Finding, suggestions: dict[str, Any]) -> str:
    assignment = owner_assignment(finding, suggestions)
    if assignment["assignment_type"] == "declared_owner_map" and finding.autonomy_mode not in {"blocked", "prepare"}:
        return "owner-confirmation"
    if assignment["assignment_type"] == "declared_owner_map":
        return "owner-approved-risk-review"
    if assignment["assignment_type"] == "inferred_suggestion":
        return "inferred-owner-review"
    if assignment["assignment_type"] == "embedded_hint":
        return "owner-map-normalization"
    return "missing-owner-assignment"


def false_positive_reason(finding: Finding) -> str:
    if finding.intent == "validation_or_reporting" and finding.risk_level in {"medium", "high"}:
        return "read-only naming or policy indicates validation/reporting"
    if finding.evidence_quality == "test_evidence" and finding.autonomy_mode == "prepare":
        return "test evidence present but mutation words triggered high risk"
    if finding.path.startswith("scripts/qa/") and finding.risk_level in {"high", "critical"}:
        return "QA path with high-risk terms may need review before blocking"
    if finding.exception_status == "accepted_exception":
        return "accepted exception should be periodically renewed, not silently blocked"
    return ""


def false_positive_status(finding: Finding, review: dict[str, Any]) -> str:
    entries = review.get("reviewed_findings") or []
    for entry in entries:
        pattern = str(entry.get("pattern", ""))
        if pattern and path_matches(pattern, finding.path):
            return str(entry.get("status", "reviewed"))
    return "candidate"


def risk_reduction_score(finding: Finding) -> int:
    score = {"critical": 100, "high": 40, "medium": 12, "low": 2}.get(finding.risk_level, 1)
    if finding.autonomy_mode == "blocked":
        score += 50
    if "prod" in finding.environments:
        score += 30
    if finding.owner_status == "missing_or_unknown":
        score += 20
    if finding.evidence_status == "missing":
        score += 15
    if finding.canonical_status == "non_canonical_or_unknown":
        score += 10
    if false_positive_reason(finding):
        score = max(1, score // 4)
    return score


def scanner_tuning_candidate(finding: Finding) -> bool:
    return bool(false_positive_reason(finding))


def operational_blocker(finding: Finding) -> bool:
    return not scanner_tuning_candidate(finding) and (
        finding.risk_level in {"critical", "high"}
        or finding.autonomy_mode in {"blocked", "prepare"}
        or finding.owner_status == "missing_or_unknown"
    )


def decision_cluster_id(finding: Finding) -> str:
    lane = re.sub(r"[^a-z0-9]+", "-", action_lane(finding).lower()).strip("-")
    return f"{finding_family(finding)}::{lane}"


def decision_cluster_record(cluster_id: str, cluster_findings: list[Finding]) -> dict[str, Any]:
    ordered = sorted(
        cluster_findings,
        key=lambda f: (-risk_reduction_score(f), decision_priority(f), risk_sort(f.risk_level), f.path),
    )
    return {
        "cluster_id": cluster_id,
        "family": finding_family(ordered[0]),
        "action_lane": action_lane(ordered[0]),
        "finding_count": len(cluster_findings),
        "risk_reduction_score": sum(risk_reduction_score(finding) for finding in cluster_findings),
        "scanner_tuning_candidates": sum(1 for finding in cluster_findings if scanner_tuning_candidate(finding)),
        "operational_blockers": sum(1 for finding in cluster_findings if operational_blocker(finding)),
        "risk": counts(cluster_findings, "risk_level"),
        "autonomy_mode": counts(cluster_findings, "autonomy_mode"),
        "ownerless_count": sum(1 for finding in cluster_findings if finding.owner_status == "missing_or_unknown"),
        "missing_evidence_count": sum(1 for finding in cluster_findings if finding.evidence_status == "missing"),
        "top_paths": [finding.path for finding in ordered[:10]],
        "top_next_actions": list(dict.fromkeys(finding.next_action for finding in ordered[:5])),
    }


def decision_clusters(findings: list[Finding]) -> list[dict[str, Any]]:
    groups: dict[str, list[Finding]] = {}
    for finding in findings:
        groups.setdefault(decision_cluster_id(finding), []).append(finding)
    clusters = [decision_cluster_record(cluster_id, cluster_findings) for cluster_id, cluster_findings in groups.items()]
    return sorted(
        clusters,
        key=lambda cluster: (
            -int(cluster["risk_reduction_score"]),
            -int(cluster["operational_blockers"]),
            str(cluster["cluster_id"]),
        ),
    )


def baseline_snapshot(findings: list[Finding], generated_at: str) -> dict[str, Any]:
    return {
        "generated_at": generated_at,
        "counts": {
            "artifacts": len(findings),
            "risk": counts(findings, "risk_level"),
            "autonomy_mode": counts(findings, "autonomy_mode"),
            "family": {family: len(items) for family, items in family_groups(findings).items()},
        },
        "blocked_paths": sorted(finding.path for finding in findings if finding.autonomy_mode == "blocked"),
        "critical_paths": sorted(finding.path for finding in findings if finding.risk_level == "critical"),
    }


def family_groups(findings: list[Finding]) -> dict[str, list[Finding]]:
    groups: dict[str, list[Finding]] = {}
    for finding in findings:
        groups.setdefault(finding_family(finding), []).append(finding)
    return groups


def write_github_control_baseline_assessment(
    path: Path,
    gh_state: dict[str, object] | None,
    baseline: dict[str, Any],
    generated_at: str,
) -> None:
    required = baseline.get("required_controls") or {}
    lines = [
        "# GitHub Control Baseline Assessment",
        "",
        f"Generated: `{generated_at}`",
        "",
        "| Control | Expected | Observed | Status | Decision |",
        "| --- | --- | --- | --- | --- |",
    ]
    if not gh_state:
        lines.append("| GitHub state | available | unavailable | fail | Run scanner with `--github` |")
        write_lines(path, lines)
        return

    protection = gh_state.get("default_branch_protection")
    expected_branch = bool(required.get("default_branch_protection_required", True))
    lines.append(
        "| Default branch protection | "
        + ("required" if expected_branch else "optional")
        + " | "
        + ("visible" if protection else "not visible")
        + " | "
        + ("pass" if protection or not expected_branch else "fail")
        + " | Review default branch protection |"
    )

    prod_names = set(required.get("production_environment_names") or ["prod", "production"])
    reviewers_required = bool(required.get("production_environment_reviewers_required", True))
    admin_bypass_allowed = bool(required.get("admin_bypass_allowed_for_production", False))
    for env in gh_environment_entries(gh_state):
        name = str(env.get("name", ""))
        if name.lower() not in {item.lower() for item in prod_names}:
            continue
        protection_rules = env.get("protection_rules") or []
        reviewers_present = bool(protection_rules)
        can_bypass = bool(env.get("can_admins_bypass"))
        lines.append(
            f"| `{name}` reviewers | required | {'present' if reviewers_present else 'missing'} | "
            f"{'pass' if reviewers_present or not reviewers_required else 'fail'} | Add deployment reviewers/protection |"
        )
        lines.append(
            f"| `{name}` admin bypass | disallowed | {'enabled' if can_bypass else 'disabled'} | "
            f"{'pass' if admin_bypass_allowed or not can_bypass else 'fail'} | Review production bypass policy |"
        )

    write_lines(path, lines)


def write_control_remediation_tracker(
    path: Path,
    gh_state: dict[str, object] | None,
    remediation_status: dict[str, Any],
    generated_at: str,
) -> None:
    status_map = remediation_status.get("controls") or {}
    lines = [
        "# Control Remediation Tracker",
        "",
        f"Generated: `{generated_at}`",
        "",
        "| Control | Observed Status | Tracking Status | Owner | Next Action |",
        "| --- | --- | --- | --- | --- |",
    ]

    controls: list[tuple[str, str, str]] = []
    if not gh_state or not gh_state.get("default_branch_protection"):
        controls.append(("default_branch_protection", "not visible", "Review default branch protection"))
    for env in gh_environment_entries(gh_state):
        name = str(env.get("name", "")).lower()
        if name not in {"prod", "production"}:
            continue
        if not (env.get("protection_rules") or []):
            controls.append((f"{name}_environment_reviewers", "missing", "Add deployment reviewers/protection"))
        if env.get("can_admins_bypass"):
            controls.append((f"{name}_admin_bypass", "enabled", "Review production bypass policy"))

    if not controls:
        controls.append(("github_controls", "no open generated control gaps", "Continue monitoring"))

    for control_id, observed, action in controls:
        status = status_map.get(control_id) or {}
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{control_id}`",
                    observed,
                    str(status.get("status", "open")),
                    str(status.get("owner", "unassigned")),
                    str(status.get("next_action", action)),
                ]
            )
            + " |"
        )
    write_lines(path, lines)


def write_finding_family_summary(path: Path, findings: list[Finding], generated_at: str) -> None:
    family_map = family_groups(findings)

    lines = [
        "# Finding Family Summary",
        "",
        f"Generated: `{generated_at}`",
        "",
        "| Family | Count | Critical | High | Blocked | Representative Next Action |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for family, family_findings in sorted(family_map.items()):
        critical = sum(1 for finding in family_findings if finding.risk_level == "critical")
        high = sum(1 for finding in family_findings if finding.risk_level == "high")
        blocked = sum(1 for finding in family_findings if finding.autonomy_mode == "blocked")
        representative = sorted(family_findings, key=lambda f: (risk_sort(f.risk_level), f.path))[0]
        lines.append(
            f"| `{family}` | {len(family_findings)} | {critical} | {high} | {blocked} | {representative.next_action} |"
        )

    lines.extend(["", "## Highest-Risk Examples By Family", ""])
    for family, family_findings in sorted(family_map.items()):
        lines.extend([f"### `{family}`", ""])
        for finding in sorted(family_findings, key=lambda f: (risk_sort(f.risk_level), f.path))[:10]:
            lines.append(f"- `{finding.path}`: {finding.risk_level}, {finding.autonomy_mode}")
        lines.append("")
    write_lines(path, lines)


def write_decision_insight_clusters(path: Path, findings: list[Finding], generated_at: str) -> None:
    clusters = decision_clusters(findings)
    tuning = [finding for finding in findings if scanner_tuning_candidate(finding)]
    blockers = [finding for finding in findings if operational_blocker(finding)]

    lines = [
        "# Decision Insight Clusters",
        "",
        f"Generated: `{generated_at}`",
        "",
        f"Findings grouped: `{len(findings)}`",
        f"Decision clusters: `{len(clusters)}`",
        f"Likely scanner tuning candidates: `{len(tuning)}`",
        f"Likely operational blockers: `{len(blockers)}`",
        "",
        "## Top Decision Clusters",
        "",
        "| Rank | Cluster | Findings | Risk Reduction Score | Scanner Tuning | Operational Blockers | Top Action |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for index, cluster in enumerate(clusters[:20], start=1):
        top_action = cluster["top_next_actions"][0] if cluster["top_next_actions"] else "review"
        lines.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    f"`{cluster['cluster_id']}`",
                    str(cluster["finding_count"]),
                    str(cluster["risk_reduction_score"]),
                    str(cluster["scanner_tuning_candidates"]),
                    str(cluster["operational_blockers"]),
                    str(top_action),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Scanner Tuning Candidates",
            "",
            "| Path | Risk | Family | Reason | Suggested Action |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for finding in sorted(tuning, key=lambda f: (risk_sort(f.risk_level), f.path))[:75]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{finding.path}`",
                    finding.risk_level,
                    finding_family(finding),
                    false_positive_reason(finding),
                    "review rule, read-only pattern, or accepted exception",
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Operational Blockers",
            "",
            "| Path | Risk | Autonomy | Family | Next Action |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for finding in sorted(blockers, key=lambda f: (-risk_reduction_score(f), risk_sort(f.risk_level), f.path))[:75]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{finding.path}`",
                    finding.risk_level,
                    finding.autonomy_mode,
                    finding_family(finding),
                    finding.next_action,
                ]
            )
            + " |"
        )
    write_lines(path, lines)


def write_false_positive_candidates(
    path: Path,
    findings: list[Finding],
    review: dict[str, Any],
    generated_at: str,
) -> None:
    candidates = [(finding, false_positive_reason(finding)) for finding in findings]
    candidates = [(finding, reason) for finding, reason in candidates if reason]
    lines = [
        "# False Positive Candidates",
        "",
        f"Generated: `{generated_at}`",
        "",
        "These findings should be reviewed before changing risk or autonomy rules.",
        "",
        "| Path | Risk | Autonomy | Status | Reason | Suggested Policy Action |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for finding, reason in sorted(candidates, key=lambda item: (risk_sort(item[0].risk_level), item[0].path))[:150]:
        action = "consider read-only pattern, accepted exception, or test fixture"
        lines.append(
            f"| `{finding.path}` | {finding.risk_level} | {finding.autonomy_mode} | "
            f"{false_positive_status(finding, review)} | {reason} | {action} |"
        )
    write_lines(path, lines)


def owner_workflow_record(finding: Finding, suggestions: dict[str, Any]) -> dict[str, Any]:
    assignment = owner_assignment(finding, suggestions)
    return {
        "path": finding.path,
        "artifact_type": finding.artifact_type,
        "risk_level": finding.risk_level,
        "autonomy_mode": finding.autonomy_mode,
        "family": finding_family(finding),
        "owner": assignment["owner"],
        "owner_boundary": assignment["boundary"],
        "owner_status": finding.owner_status,
        "assignment_type": assignment["assignment_type"],
        "assignment_confidence": assignment["confidence"],
        "review_class": owner_review_class(finding, suggestions),
        "review_action": assignment["review_action"],
        "blocked_claims": finding.blocked_claims,
        "next_action": finding.next_action,
    }


def owner_workflow_records(findings: list[Finding], suggestions: dict[str, Any]) -> list[dict[str, Any]]:
    return sorted(
        [owner_workflow_record(finding, suggestions) for finding in findings],
        key=lambda row: (
            float(row["assignment_confidence"]),
            risk_sort(str(row["risk_level"])),
            str(row["review_class"]),
            str(row["path"]),
        ),
    )


def write_owner_confidence_map(
    path: Path,
    findings: list[Finding],
    suggestions: dict[str, Any],
    generated_at: str,
) -> None:
    records = owner_workflow_records(findings, suggestions)
    assignment_counts: dict[str, int] = {}
    review_counts: dict[str, int] = {}
    for record in records:
        assignment_counts[str(record["assignment_type"])] = assignment_counts.get(str(record["assignment_type"]), 0) + 1
        review_counts[str(record["review_class"])] = review_counts.get(str(record["review_class"]), 0) + 1

    lines = [
        "# Owner Confidence Map",
        "",
        f"Generated: `{generated_at}`",
        "",
        f"Owner workflow records: `{len(records)}`",
        "",
        "## Assignment Types",
        "",
    ]
    for key, value in sorted(assignment_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Review Classes", ""])
    for key, value in sorted(review_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- `{key}`: {value}")
    lines.extend(
        [
            "",
            "## Lowest-Confidence Owner Decisions",
            "",
            "| Confidence | Review Class | Owner | Boundary | Path | Risk | Action |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for record in records[:150]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(record["assignment_confidence"]),
                    str(record["review_class"]),
                    str(record["owner"]),
                    str(record["owner_boundary"]),
                    f"`{record['path']}`",
                    str(record["risk_level"]),
                    str(record["review_action"]),
                ]
            )
            + " |"
        )
    write_lines(path, lines)


def write_owner_assignment_plan(
    path: Path,
    findings: list[Finding],
    suggestions: dict[str, Any],
    generated_at: str,
) -> None:
    ownerless = [finding for finding in findings if finding.owner_status == "missing_or_unknown"]
    lines = [
        "# Owner Assignment Plan",
        "",
        f"Generated: `{generated_at}`",
        "",
        f"Ownerless artifacts: `{len(ownerless)}`",
        "",
        "| Suggested Owner | Boundary | Family | Path | Risk | Next Action |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for finding in sorted(ownerless, key=lambda f: (risk_sort(f.risk_level), finding_family(f), f.path))[:200]:
        assignment = owner_assignment(finding, suggestions)
        lines.append(
            "| "
            + " | ".join(
                [
                    str(assignment["owner"]),
                    str(assignment["boundary"]),
                    finding_family(finding),
                    f"`{finding.path}`",
                    finding.risk_level,
                    str(assignment["review_action"]),
                ]
            )
            + " |"
        )
    write_lines(path, lines)


def write_remediation_playbook_map(path: Path, findings: list[Finding], generated_at: str) -> None:
    lines = [
        "# Remediation Playbook Map",
        "",
        f"Generated: `{generated_at}`",
        "",
        "| Path | Risk | Family | Playbook | Next Action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for finding in sorted(findings, key=lambda f: (decision_priority(f), risk_sort(f.risk_level), f.path)):
        playbook = remediation_playbook(finding)
        if not playbook and finding.risk_level not in {"critical", "high"}:
            continue
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{finding.path}`",
                    finding.risk_level,
                    finding_family(finding),
                    f"`{playbook}`" if playbook else "owner review",
                    finding.next_action,
                ]
            )
            + " |"
        )
    write_lines(path, lines)


def write_baseline_drift(
    path: Path,
    snapshot_path: Path,
    findings: list[Finding],
    generated_at: str,
) -> None:
    current = baseline_snapshot(findings, generated_at)
    previous = None
    if snapshot_path.exists():
        previous = json.loads(snapshot_path.read_text(encoding="utf-8"))

    lines = [
        "# Drift From Baseline",
        "",
        f"Generated: `{generated_at}`",
        "",
    ]
    if not previous:
        lines.extend(
            [
                "No previous baseline snapshot was found.",
                "",
                "The current run has been saved as the baseline.",
            ]
        )
    else:
        previous_blocked = set(previous.get("blocked_paths") or [])
        current_blocked = set(current.get("blocked_paths") or [])
        previous_critical = set(previous.get("critical_paths") or [])
        current_critical = set(current.get("critical_paths") or [])
        lines.extend(
            [
                "## Count Changes",
                "",
                "| Metric | Previous | Current | Delta |",
                "| --- | --- | --- | --- |",
            ]
        )
        for risk in ("critical", "high", "medium", "low"):
            old = int((previous.get("counts") or {}).get("risk", {}).get(risk, 0))
            new = int(current["counts"]["risk"].get(risk, 0))
            lines.append(f"| risk `{risk}` | {old} | {new} | {new - old:+d} |")
        for mode in ("blocked", "prepare", "controlled_execute", "recommend", "observe"):
            old = int((previous.get("counts") or {}).get("autonomy_mode", {}).get(mode, 0))
            new = int(current["counts"]["autonomy_mode"].get(mode, 0))
            lines.append(f"| autonomy `{mode}` | {old} | {new} | {new - old:+d} |")

        lines.extend(
            [
                "",
                "## Path Changes",
                "",
                f"- New blocked paths: `{len(current_blocked - previous_blocked)}`",
                f"- Resolved blocked paths: `{len(previous_blocked - current_blocked)}`",
                f"- New critical paths: `{len(current_critical - previous_critical)}`",
                f"- Resolved critical paths: `{len(previous_critical - current_critical)}`",
                "",
                "### New Blocked Paths",
                "",
            ]
        )
        for item in sorted(current_blocked - previous_blocked)[:100]:
            lines.append(f"- `{item}`")
        lines.extend(["", "### Resolved Blocked Paths", ""])
        for item in sorted(previous_blocked - current_blocked)[:100]:
            lines.append(f"- `{item}`")

    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_lines(path, lines)


def graph_node_id(kind: str, value: str) -> str:
    digest = hashlib.sha1(f"{kind}:{value}".encode()).hexdigest()[:12]
    return f"{kind}:{digest}"


def write_graph_outputs(
    out: Path,
    repo: Path,
    findings: list[Finding],
    generated_at: str,
    owner_suggestions: dict[str, Any] | None = None,
) -> None:
    entities: dict[str, dict[str, Any]] = {}
    relationships: list[dict[str, Any]] = []
    suggestions = owner_suggestions or {}

    repo_id = graph_node_id("repo", str(repo))
    entities[repo_id] = {
        "id": repo_id,
        "type": "repo",
        "name": repo.name,
        "path": str(repo),
        "generated_at": generated_at,
    }

    def add_entity(kind: str, key: str, **properties: Any) -> str:
        entity_id = graph_node_id(kind, key)
        if entity_id not in entities:
            entity = {"id": entity_id, "type": kind, "key": key}
            entity.update(properties)
            entities[entity_id] = entity
        return entity_id

    def add_relationship(source: str, relation: str, target: str, **properties: Any) -> None:
        relationship = {"source": source, "relation": relation, "target": target}
        relationship.update(properties)
        relationships.append(relationship)

    policy_nodes = {
        "canonical_policy": add_entity("policy", "canonical_policy", name="Canonical operating path policy"),
        "owner_policy": add_entity("policy", "owner_policy", name="Owner accountability policy"),
        "evidence_policy": add_entity("policy", "evidence_policy", name="Safety evidence policy"),
        "autonomy_policy": add_entity("policy", "autonomy_policy", name="Autonomy mode policy"),
    }
    control_nodes = {
        "non_canonical_control": add_entity("control", "non_canonical_control", name="Canonical path control"),
        "missing_owner_control": add_entity("control", "missing_owner_control", name="Owner boundary control"),
        "missing_evidence_control": add_entity("control", "missing_evidence_control", name="Evidence requirement control"),
        "autonomy_block_control": add_entity("control", "autonomy_block_control", name="Autonomous execution control"),
    }

    for finding in findings:
        artifact_id = graph_node_id("artifact", finding.path)
        entities[artifact_id] = {
            "id": artifact_id,
            "type": "artifact",
            "artifact_id": finding.artifact_id,
            "artifact_type": finding.artifact_type,
            "path": finding.path,
            "risk_level": finding.risk_level,
            "autonomy_mode": finding.autonomy_mode,
            "intent": finding.intent,
            "canonical_status": finding.canonical_status,
            "evidence_quality": finding.evidence_quality,
        }
        add_relationship(repo_id, "contains", artifact_id)

        decision_id = add_entity(
            "decision",
            finding.path,
            priority=decision_priority(finding),
            lane=action_lane(finding),
            next_action=finding.next_action,
            risk_level=finding.risk_level,
            autonomy_mode=finding.autonomy_mode,
        )
        add_relationship(artifact_id, "has_decision", decision_id, confidence=finding.confidence)
        add_relationship(decision_id, "governed_by", policy_nodes["autonomy_policy"])

        family_id = add_entity("finding_family", finding_family(finding), name=finding_family(finding))
        add_relationship(artifact_id, "classified_as", family_id)

        owner_key = finding.owner or finding.owner_status
        owner_id = add_entity(
            "owner",
            owner_key,
            name=owner_key,
            boundary=finding.owner_boundary or "unknown",
            status=finding.owner_status,
        )
        add_relationship(artifact_id, "owned_by", owner_id, status=finding.owner_status)
        suggested_owner, suggested_boundary = owner_suggestion(finding, suggestions)
        if suggested_owner and finding.owner_status == "missing_or_unknown":
            suggested_owner_id = add_entity(
                "owner",
                suggested_owner,
                name=suggested_owner,
                boundary=suggested_boundary or "unknown",
                status="suggested",
            )
            add_relationship(artifact_id, "suggested_owner", suggested_owner_id, boundary=suggested_boundary)

        for mutation_type in finding.mutation_types:
            mutation_id = add_entity("mutation_type", mutation_type, name=mutation_type)
            add_relationship(artifact_id, "has_mutation_type", mutation_id)
        for environment in finding.environments:
            environment_id = add_entity("environment", environment, name=environment)
            add_relationship(artifact_id, "references_environment", environment_id)
        for script in finding.called_scripts:
            script_id = add_entity("artifact_reference", script, path=script)
            add_relationship(artifact_id, "calls", script_id)
        if finding.exception_status == "accepted_exception":
            exception_id = add_entity("policy_exception", finding.path, reason=finding.exception_reason)
            add_relationship(artifact_id, "covered_by_exception", exception_id)
        if finding.evidence_status == "present":
            evidence_id = add_entity("evidence", f"{finding.path}:{finding.evidence_quality}", quality=finding.evidence_quality)
            add_relationship(artifact_id, "has_evidence", evidence_id)
            add_relationship(evidence_id, "supports_decision", decision_id)
        else:
            evidence_requirement_id = add_entity(
                "evidence",
                f"{finding.path}:required",
                quality="required",
                status="missing",
            )
            add_relationship(artifact_id, "requires_evidence", evidence_requirement_id, reason=finding.next_action)

        if finding.canonical_status == "non_canonical_or_unknown":
            add_relationship(
                artifact_id,
                "violates_policy",
                policy_nodes["canonical_policy"],
                reason="canonical operating path is unknown",
            )
            add_relationship(artifact_id, "blocked_by_control", control_nodes["non_canonical_control"])
        if finding.owner_status == "missing_or_unknown":
            add_relationship(
                artifact_id,
                "violates_policy",
                policy_nodes["owner_policy"],
                reason="owner boundary is missing or unknown",
            )
            add_relationship(artifact_id, "blocked_by_control", control_nodes["missing_owner_control"])
        if finding.evidence_status == "missing" and finding.risk_level in {"critical", "high", "medium"}:
            add_relationship(
                artifact_id,
                "violates_policy",
                policy_nodes["evidence_policy"],
                reason="safety evidence is missing",
            )
            add_relationship(artifact_id, "blocked_by_control", control_nodes["missing_evidence_control"])
        if finding.autonomy_mode == "blocked":
            add_relationship(
                artifact_id,
                "blocked_by_control",
                control_nodes["autonomy_block_control"],
                reason="autonomous execution is blocked",
            )

    graph_dir = out / "graph"
    graph_dir.mkdir(parents=True, exist_ok=True)
    (graph_dir / "entities.json").write_text(
        json.dumps(sorted(entities.values(), key=lambda item: (item["type"], item["id"])), indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    (graph_dir / "relationships.json").write_text(
        json.dumps(sorted(relationships, key=lambda item: (item["source"], item["relation"], item["target"])), indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )


def decision_export_record(finding: Finding) -> dict[str, Any]:
    return {
        "path": finding.path,
        "artifact_type": finding.artifact_type,
        "priority": decision_priority(finding),
        "action_lane": action_lane(finding),
        "risk_level": finding.risk_level,
        "autonomy_mode": finding.autonomy_mode,
        "owner": owner_display(finding),
        "owner_status": finding.owner_status,
        "canonical_status": finding.canonical_status,
        "evidence_status": finding.evidence_status,
        "evidence_quality": finding.evidence_quality,
        "next_action": finding.next_action,
        "blocked_claims": finding.blocked_claims,
        "risk_reasons": finding.risk_reasons,
    }


def write_owner_workflow_exports(out: Path, findings: list[Finding], suggestions: dict[str, Any], generated_at: str) -> None:
    export_dir = out / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    records = owner_workflow_records(findings, suggestions)
    assignment_counts: dict[str, int] = {}
    review_counts: dict[str, int] = {}
    for record in records:
        assignment_counts[str(record["assignment_type"])] = assignment_counts.get(str(record["assignment_type"]), 0) + 1
        review_counts[str(record["review_class"])] = review_counts.get(str(record["review_class"]), 0) + 1

    (export_dir / "owner-workflows.json").write_text(
        json.dumps(
            {
                "generated_at": generated_at,
                "record_count": len(records),
                "assignment_type_counts": dict(sorted(assignment_counts.items())),
                "review_class_counts": dict(sorted(review_counts.items())),
                "records": records,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def actionable_findings(findings: list[Finding]) -> list[Finding]:
    return [
        finding
        for finding in findings
        if finding.risk_level in {"critical", "high", "medium"}
        or finding.owner_status == "missing_or_unknown"
    ]


def write_decision_exports(out: Path, findings: list[Finding], generated_at: str) -> None:
    export_dir = out / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    actionable = sorted(
        actionable_findings(findings),
        key=lambda f: (decision_priority(f), risk_sort(f.risk_level), action_lane(f), owner_display(f), f.path),
    )

    owner_rows = [decision_export_record(finding) for finding in actionable]
    (export_dir / "owner-backlog.json").write_text(
        json.dumps(
            {
                "generated_at": generated_at,
                "record_count": len(owner_rows),
                "records": owner_rows,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    owner_csv_fields = [
        "priority",
        "action_lane",
        "owner",
        "owner_status",
        "risk_level",
        "autonomy_mode",
        "artifact_type",
        "path",
        "next_action",
    ]
    with (export_dir / "owner-backlog.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=owner_csv_fields, lineterminator="\n")
        writer.writeheader()
        for row in owner_rows:
            writer.writerow({field: row[field] for field in owner_csv_fields})

    lane_summaries: list[dict[str, Any]] = []
    remediation_packs: list[dict[str, Any]] = []
    for lane, lane_findings in action_summary(actionable):
        ordered = sorted(
            lane_findings,
            key=lambda f: (-risk_reduction_score(f), decision_priority(f), risk_sort(f.risk_level), f.path),
        )
        risk_score = sum(risk_reduction_score(finding) for finding in lane_findings)
        lane_summaries.append(
            {
                "lane": lane,
                "count": len(lane_findings),
                "highest_priority": decision_priority(ordered[0]),
                "highest_risk": ordered[0].risk_level,
                "risk_reduction_score": risk_score,
                "top_paths": [finding.path for finding in ordered[:10]],
            }
        )
        remediation_packs.append(
            {
                "lane": lane,
                "count": len(lane_findings),
                "risk_reduction_score": risk_score,
                "validation_focus": ordered[0].next_action,
                "records": [decision_export_record(finding) for finding in ordered[:25]],
            }
        )
    lane_summaries = sorted(lane_summaries, key=lambda row: (-int(row["risk_reduction_score"]), row["lane"]))
    remediation_packs = sorted(remediation_packs, key=lambda row: (-int(row["risk_reduction_score"]), row["lane"]))

    top_decisions = [decision_export_record(finding) for finding in actionable[:50]]
    (export_dir / "executive-decisions.json").write_text(
        json.dumps(
            {
                "generated_at": generated_at,
                "counts": {
                    "artifacts": len(findings),
                    "risk": counts(findings, "risk_level"),
                    "autonomy_mode": counts(findings, "autonomy_mode"),
                    "actionable": len(actionable),
                },
                "action_lanes": lane_summaries,
                "top_decisions": top_decisions,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    cluster_rows = decision_clusters(findings)
    tuning_findings = sorted(
        [finding for finding in findings if scanner_tuning_candidate(finding)],
        key=lambda f: (risk_sort(f.risk_level), f.path),
    )
    blocker_findings = sorted(
        [finding for finding in findings if operational_blocker(finding)],
        key=lambda f: (-risk_reduction_score(f), risk_sort(f.risk_level), f.path),
    )
    tuning = [decision_export_record(finding) for finding in tuning_findings]
    blockers = [decision_export_record(finding) for finding in blocker_findings]
    (export_dir / "decision-clusters.json").write_text(
        json.dumps(
            {
                "generated_at": generated_at,
                "counts": {
                    "artifacts": len(findings),
                    "cluster_count": len(cluster_rows),
                    "scanner_tuning_candidates": len(tuning),
                    "operational_blockers": len(blockers),
                },
                "clusters": cluster_rows,
                "scanner_tuning_candidates": tuning[:150],
                "operational_blockers": blockers[:150],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    (export_dir / "remediation-packs.json").write_text(
        json.dumps(
            {
                "generated_at": generated_at,
                "pack_count": len(remediation_packs),
                "packs": remediation_packs,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def write_report_index(path: Path, generated_at: str) -> None:
    lines = [
        "# ML Pilot Report Index",
        "",
        f"Generated: `{generated_at}`",
        "",
        "| Role | Start With | Use For |",
        "| --- | --- | --- |",
        "| Product owner | `executive-decision-summary.md` | Priority decisions and risk posture |",
        "| IT specialist | `github-protection-findings.md` | GitHub/environment control gaps |",
        "| Engineer | `decision-backlog.md` | Concrete remediation tasks |",
        "| Owner/service lead | `owner-review-queue.md` | Ownership assignment and review |",
        "| Owner/service lead | `owner-confidence-map.md` | Owner assignment confidence and review classes |",
        "| Auditor | `evidence-quality-map.md` | Evidence quality and missing proof |",
        "| Scanner maintainer | `risk-explanation-map.md` | Rule-level risk explanation and tuning |",
        "| GitHub admin | `github-control-baseline-assessment.md` | Branch/environment protection baseline |",
        "| Platform maintainer | `policy-coverage-report.md` | Policy coverage and unmapped risks |",
        "| Governance owner | `control-remediation-tracker.md` | Control remediation status |",
        "| Scanner maintainer | `false-positive-candidates.md` | Candidate rule tuning inputs |",
        "| Product owner | `decision-insight-clusters.md` | Clustered decisions, scanner tuning candidates, and operational blockers |",
        "| Automation/UI | `exports/` | Machine-readable owner, executive, and remediation exports |",
        "",
        "## Reports",
        "",
    ]
    for report in REPORT_FILES:
        if report != "README.md":
            lines.append(f"- `{report}`")
    write_lines(path, lines)


def owner_display(finding: Finding) -> str:
    if finding.owner:
        if finding.owner_boundary:
            return f"{finding.owner} ({finding.owner_boundary})"
        return finding.owner
    return finding.owner_status


def write_markdown(
    path: Path,
    repo: Path,
    findings: list[Finding],
    git_state: dict[str, object],
    gh_state: dict[str, object] | None,
    generated_at: str,
) -> None:
    risky = [f for f in findings if f.risk_level in {"critical", "high"}]
    blocked = [f for f in findings if f.autonomy_mode == "blocked"]
    lines = [
        "# Operational State Mutation Registry",
        "",
        f"Generated: `{generated_at}`",
        f"Pilot repository: `{repo}`",
        "",
        "This is a generated materialized view from local repository evidence.",
        "It is not an authoritative source of truth.",
        "",
        "## Local Git State",
        "",
        f"- Branch: `{git_state.get('branch') or 'unknown'}`",
        f"- Remote: `{git_state.get('remote') or 'unknown'}`",
        f"- Dirty file count: `{git_state.get('dirty_file_count')}`",
        f"- Ahead/behind: `{git_state.get('ahead_behind') or 'unknown'}`",
        "",
    ]
    if gh_state:
        repo_info = gh_state.get("repo") or {}
        pr_list = gh_state.get("pull_requests") or []
        workflows = gh_state.get("workflows") or []
        protection = gh_state.get("default_branch_protection")
        environments = gh_state.get("environments") or {}
        environment_count = "unknown"
        if isinstance(environments, dict):
            environment_count = str(len(environments.get("environments") or []))
        lines.extend(
            [
                "## GitHub State",
                "",
                f"- Repository: `{repo_info.get('nameWithOwner', 'unknown')}`",
                f"- Visibility: `{repo_info.get('visibility', 'unknown')}`",
                f"- Default branch: `{(repo_info.get('defaultBranchRef') or {}).get('name', 'unknown')}`",
                f"- Open pull requests: `{len(pr_list) if isinstance(pr_list, list) else 'unknown'}`",
                f"- Workflows visible to GitHub CLI: `{len(workflows) if isinstance(workflows, list) else 'unknown'}`",
                f"- Default branch protection visible: `{'yes' if protection else 'no'}`",
                f"- GitHub environments visible: `{environment_count}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Summary",
            "",
            f"- Artifacts scanned: `{len(findings)}`",
            f"- High or critical risk artifacts: `{len(risky)}`",
            f"- Blocked autonomy artifacts: `{len(blocked)}`",
            "",
            "### Risk Counts",
            "",
        ]
    )
    for key, value in counts(findings, "risk_level").items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "### Autonomy Mode Counts", ""])
    for key, value in counts(findings, "autonomy_mode").items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "### Mutation Type Counts", ""])
    for key, value in counts(findings, "mutation_types").items():
        lines.append(f"- `{key}`: {value}")

    lines.extend(
        [
            "",
            "## Highest-Risk Blocked Paths",
            "",
            "| Path | Type | Environments | Mutation | Blocked Claims | Next Action |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for finding in blocked[:40]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{finding.path}`",
                    finding.artifact_type,
                    ", ".join(finding.environments),
                    ", ".join(finding.mutation_types),
                    "<br>".join(finding.blocked_claims) or "none",
                    finding.next_action,
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Registry",
            "",
            "| Path | Type | Risk | Autonomy | Canonical | Owner | Evidence | Exception | Next Action |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for finding in sorted(findings, key=lambda f: (risk_sort(f.risk_level), f.path)):
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{finding.path}`",
                    finding.artifact_type,
                    f"{finding.risk_level} / {finding.confidence}",
                    f"{finding.autonomy_mode} / {finding.intent}",
                    finding.canonical_status,
                    owner_display(finding),
                    finding.evidence_status,
                    finding.exception_status,
                    finding.next_action,
                ]
            )
            + " |"
        )

    write_lines(path, lines)


def action_lane(finding: Finding) -> str:
    if finding.risk_level == "critical" and finding.autonomy_mode == "blocked":
        return "Block or certify critical operational mutation"
    if finding.owner_status == "missing_or_unknown" and finding.risk_level in {"critical", "high"}:
        return "Assign accountable owner boundary"
    if finding.evidence_status == "missing" and finding.risk_level in {"critical", "high", "medium"}:
        return "Attach safety and rollback evidence"
    if finding.canonical_status == "non_canonical_or_unknown" and finding.risk_level in {"critical", "high", "medium"}:
        return "Canonicalize or document exception"
    if finding.exception_status == "accepted_exception":
        return "Renew accepted exception"
    return "Review before autonomy expansion"


def action_summary(findings: list[Finding]) -> list[tuple[str, list[Finding]]]:
    groups: dict[str, list[Finding]] = {}
    for finding in findings:
        groups.setdefault(action_lane(finding), []).append(finding)
    return sorted(
        groups.items(),
        key=lambda item: (
            min(decision_priority(finding) for finding in item[1]),
            min(risk_sort(finding.risk_level) for finding in item[1]),
            item[0],
        ),
    )


def write_decision_backlog(path: Path, findings: list[Finding], generated_at: str) -> None:
    actionable = [
        finding
        for finding in findings
        if finding.risk_level in {"critical", "high", "medium"}
        or finding.owner_status == "missing_or_unknown"
    ]
    lines = [
        "# Decision Backlog",
        "",
        f"Generated: `{generated_at}`",
        "",
        "This backlog is generated from scanner findings. It is decision support, not source truth.",
        "",
        "## Action Lanes",
        "",
        "| Lane | Items | Highest Priority | Dominant Owner | First Decision |",
        "| --- | --- | --- | --- | --- |",
    ]
    for lane, lane_findings in action_summary(actionable):
        ordered = sorted(lane_findings, key=lambda f: (decision_priority(f), risk_sort(f.risk_level), f.path))
        owner_counts: dict[str, int] = {}
        for finding in lane_findings:
            owner_counts[owner_display(finding)] = owner_counts.get(owner_display(finding), 0) + 1
        owner = sorted(owner_counts.items(), key=lambda item: (-item[1], item[0]))[0][0]
        lines.append(
            "| "
            + " | ".join(
                [
                    lane,
                    str(len(lane_findings)),
                    decision_priority(ordered[0]),
                    owner,
                    ordered[0].next_action,
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Decisions",
            "",
            "| Priority | Lane | Path | Risk | Autonomy | Owner | Decision Needed |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for finding in sorted(actionable, key=lambda f: (decision_priority(f), risk_sort(f.risk_level), action_lane(f), f.path)):
        lines.append(
            "| "
            + " | ".join(
                [
                    decision_priority(finding),
                    action_lane(finding),
                    f"`{finding.path}`",
                    finding.risk_level,
                    finding.autonomy_mode,
                    owner_display(finding),
                    finding.next_action,
                ]
            )
            + " |"
        )
    write_lines(path, lines)


def write_owner_review_queue(
    path: Path,
    findings: list[Finding],
    suggestions: dict[str, Any],
    generated_at: str,
) -> None:
    records = owner_workflow_records(findings, suggestions)
    lines = [
        "# Owner Review Queue",
        "",
        f"Generated: `{generated_at}`",
        "",
        "| Review Class | Confidence | Owner | Boundary | Path | Risk | Autonomy | Blocked Claims | Next Action |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for record in records:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(record["review_class"]),
                    str(record["assignment_confidence"]),
                    str(record["owner"]),
                    str(record["owner_boundary"]),
                    f"`{record['path']}`",
                    str(record["risk_level"]),
                    str(record["autonomy_mode"]),
                    "<br>".join(record["blocked_claims"]) or "none",
                    str(record["next_action"]),
                ]
            )
            + " |"
        )
    write_lines(path, lines)


def write_autonomy_summary(path: Path, findings: list[Finding], generated_at: str) -> None:
    lines = [
        "# Autonomy Mode Summary",
        "",
        f"Generated: `{generated_at}`",
        "",
        "## Counts",
        "",
    ]
    for key, value in counts(findings, "autonomy_mode").items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Mode Details", ""])
    for mode in ("blocked", "prepare", "controlled_execute", "recommend", "observe"):
        mode_findings = [finding for finding in findings if finding.autonomy_mode == mode]
        if not mode_findings:
            continue
        lines.extend([f"### `{mode}`", ""])
        for finding in sorted(mode_findings, key=lambda f: (risk_sort(f.risk_level), f.path))[:50]:
            lines.append(f"- `{finding.path}`: {finding.risk_level}, {finding.next_action}")
        lines.append("")
    write_lines(path, lines)


def write_repository_state_summary(
    path: Path,
    git_state: dict[str, object],
    gh_state: dict[str, object] | None,
    generated_at: str,
) -> None:
    lines = [
        "# Repository State Summary",
        "",
        f"Generated: `{generated_at}`",
        "",
        "## Local State",
        "",
        f"- Branch: `{git_state.get('branch') or 'unknown'}`",
        f"- Remote: `{git_state.get('remote') or 'unknown'}`",
        f"- Dirty file count: `{git_state.get('dirty_file_count')}`",
        f"- Ahead/behind: `{git_state.get('ahead_behind') or 'unknown'}`",
        "",
    ]
    dirty_sample = git_state.get("dirty_sample") or []
    if dirty_sample:
        lines.extend(["### Dirty Sample", ""])
        for item in dirty_sample:
            lines.append(f"- `{item}`")
        lines.append("")

    if gh_state:
        repo_info = gh_state.get("repo") or {}
        workflows = gh_state.get("workflows") or []
        prs = gh_state.get("pull_requests") or []
        protection = gh_state.get("default_branch_protection")
        environments = gh_state.get("environments") or {}
        environment_list = []
        if isinstance(environments, dict):
            environment_list = environments.get("environments") or []
        lines.extend(
            [
                "## GitHub State",
                "",
                f"- Repository: `{repo_info.get('nameWithOwner', 'unknown')}`",
                f"- URL: `{repo_info.get('url', 'unknown')}`",
                f"- Visibility: `{repo_info.get('visibility', 'unknown')}`",
                f"- Default branch: `{(repo_info.get('defaultBranchRef') or {}).get('name', 'unknown')}`",
                f"- Pushed at: `{repo_info.get('pushedAt', 'unknown')}`",
                f"- Open pull requests: `{len(prs) if isinstance(prs, list) else 'unknown'}`",
                f"- Workflows: `{len(workflows) if isinstance(workflows, list) else 'unknown'}`",
                f"- Default branch protection visible: `{'yes' if protection else 'no'}`",
                f"- Environments: `{len(environment_list)}`",
                "",
            ]
        )
        if isinstance(workflows, list):
            lines.extend(["### Workflow Paths", ""])
            for workflow in workflows:
                lines.append(f"- `{workflow.get('path', 'unknown')}`: {workflow.get('state', 'unknown')}")
            lines.append("")
    write_lines(path, lines)


def risk_sort(level: str) -> int:
    return {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(level, 9)


def write_manifest(
    path: Path,
    repo: Path,
    findings: list[Finding],
    git_state: dict[str, object],
    gh_state: dict[str, object] | None,
    generated_at: str,
    policy_path: Path | None,
    baseline_path: Path | None,
    repo_root: Path,
    owner_suggestions_path: Path | None,
    control_remediation_path: Path | None,
    false_positive_review_path: Path | None,
) -> None:
    manifest = {
        "generated_at": generated_at,
        "pilot_repository": str(repo),
        "inputs": {
            "workflows": ".github/workflows/*.yml",
            "scripts": "scripts/**/*.sh, scripts/**/*.py",
            "tools": "tools/**/*.py" if any(f.artifact_type == "tool" for f in findings) else None,
            "local_git_state": True,
            "github_state": gh_state is not None,
            "policy_path": relative_or_absolute(policy_path, repo_root) if policy_path else "built-in defaults",
            "github_baseline_path": relative_or_absolute(baseline_path, repo_root) if baseline_path else "none",
            "owner_suggestions_path": (
                relative_or_absolute(owner_suggestions_path, repo_root) if owner_suggestions_path else "none"
            ),
            "control_remediation_path": (
                relative_or_absolute(control_remediation_path, repo_root) if control_remediation_path else "none"
            ),
            "false_positive_review_path": (
                relative_or_absolute(false_positive_review_path, repo_root) if false_positive_review_path else "none"
            ),
        },
        "counts": {
            "artifacts": len(findings),
            "risk": counts(findings, "risk_level"),
            "autonomy_mode": counts(findings, "autonomy_mode"),
            "mutation_types": counts(findings, "mutation_types"),
            "evidence_quality": counts(findings, "evidence_quality"),
        },
        "source_fingerprint": source_fingerprint(
            repo_root,
            policy_path,
            baseline_path,
            owner_suggestions_path,
            control_remediation_path,
            false_positive_review_path,
        ),
        "generated_outputs": REPORT_FILES,
        "local_git_state": git_state,
        "github_state": gh_state,
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path("/home/stocksadmin/workspace/ML"),
        help="Pilot repository to scan.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("reports/ml-pilot"),
        help="Output directory for generated materialized views.",
    )
    parser.add_argument(
        "--github",
        action="store_true",
        help="Include GitHub state through the gh CLI when available.",
    )
    parser.add_argument(
        "--policy",
        type=Path,
        default=None,
        help="Optional JSON policy file for canonical commands and autonomy modes.",
    )
    parser.add_argument(
        "--include-tools",
        action="store_true",
        help="Also scan tools/**/*.py. Useful for product self-governance.",
    )
    parser.add_argument(
        "--github-baseline",
        type=Path,
        default=None,
        help="Optional JSON policy file for GitHub control baseline assessment.",
    )
    parser.add_argument(
        "--owner-suggestions",
        type=Path,
        default=None,
        help="Optional JSON policy file for owner assignment suggestions.",
    )
    parser.add_argument(
        "--control-remediation",
        type=Path,
        default=None,
        help="Optional JSON policy file for control remediation status tracking.",
    )
    parser.add_argument(
        "--false-positive-review",
        type=Path,
        default=None,
        help="Optional JSON policy file for false-positive review status.",
    )
    parser.add_argument(
        "--generated-at",
        default=None,
        help="Override generated timestamp for reproducibility checks.",
    )
    args = parser.parse_args()

    repo = args.repo.resolve()
    out = args.out.resolve()
    policy_path = args.policy.resolve() if args.policy else None
    baseline_path = args.github_baseline.resolve() if args.github_baseline else None
    owner_suggestions_path = args.owner_suggestions.resolve() if args.owner_suggestions else None
    control_remediation_path = args.control_remediation.resolve() if args.control_remediation else None
    false_positive_review_path = args.false_positive_review.resolve() if args.false_positive_review else None
    policy = load_policy(policy_path)
    github_baseline = load_github_baseline(baseline_path)
    owner_suggestions = load_optional_json(owner_suggestions_path)
    control_remediation = load_optional_json(control_remediation_path)
    false_positive_review = load_optional_json(false_positive_review_path)
    out.mkdir(parents=True, exist_ok=True)

    generated_at = args.generated_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    findings = [
        scan_file(repo, artifact_type, path, policy)
        for artifact_type, path in discover_files(repo, include_tools=args.include_tools)
    ]
    git_state = local_git_state(repo)
    gh_state = github_state(repo) if args.github else None
    enrich_pull_request_files(repo, gh_state)

    write_jsonl(out / "findings.jsonl", findings)
    write_csv(out / "operational-state-mutation-registry.csv", findings)
    write_markdown(
        out / "operational-state-mutation-registry.md",
        repo,
        findings,
        git_state,
        gh_state,
        generated_at,
    )
    write_decision_backlog(out / "decision-backlog.md", findings, generated_at)
    write_owner_review_queue(out / "owner-review-queue.md", findings, owner_suggestions, generated_at)
    write_owner_confidence_map(out / "owner-confidence-map.md", findings, owner_suggestions, generated_at)
    write_autonomy_summary(out / "autonomy-mode-summary.md", findings, generated_at)
    write_repository_state_summary(
        out / "repository-state-summary.md",
        git_state,
        gh_state,
        generated_at,
    )
    write_github_protection_findings(
        out / "github-protection-findings.md",
        findings,
        gh_state,
        generated_at,
    )
    write_github_control_baseline_assessment(
        out / "github-control-baseline-assessment.md",
        gh_state,
        github_baseline,
        generated_at,
    )
    write_control_remediation_tracker(
        out / "control-remediation-tracker.md",
        gh_state,
        control_remediation,
        generated_at,
    )
    write_policy_coverage_report(out / "policy-coverage-report.md", findings, generated_at)
    write_evidence_quality_map(out / "evidence-quality-map.md", findings, generated_at)
    write_risk_explanation_map(out / "risk-explanation-map.md", findings, generated_at)
    write_executive_decision_summary(out / "executive-decision-summary.md", findings, generated_at)
    write_finding_family_summary(out / "finding-family-summary.md", findings, generated_at)
    write_decision_insight_clusters(out / "decision-insight-clusters.md", findings, generated_at)
    write_false_positive_candidates(
        out / "false-positive-candidates.md",
        findings,
        false_positive_review,
        generated_at,
    )
    write_owner_assignment_plan(out / "owner-assignment-plan.md", findings, owner_suggestions, generated_at)
    write_remediation_playbook_map(out / "remediation-playbook-map.md", findings, generated_at)
    write_baseline_drift(
        out / "drift-from-baseline.md",
        out / "baseline-history" / "latest.json",
        findings,
        generated_at,
    )
    write_pr_risk_summary(out / "pr-risk-summary.md", findings, gh_state, generated_at)
    write_graph_outputs(out, repo, findings, generated_at, owner_suggestions)
    write_owner_workflow_exports(out, findings, owner_suggestions, generated_at)
    write_decision_exports(out, findings, generated_at)
    write_report_index(out / "README.md", generated_at)
    write_manifest(
        out / "manifest.json",
        repo,
        findings,
        git_state,
        gh_state,
        generated_at,
        policy_path,
        baseline_path,
        Path.cwd(),
        owner_suggestions_path,
        control_remediation_path,
        false_positive_review_path,
    )

    print(f"Generated {len(findings)} findings in {out}")
    print(f"Risk counts: {counts(findings, 'risk_level')}")
    print(f"Autonomy counts: {counts(findings, 'autonomy_mode')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
