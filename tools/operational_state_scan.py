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
    if finding.risk_level == "medium":
        return "P3"
    return "P4"


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
        "| Priority | Path | Risk | Autonomy | Owner | Decision Needed |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for finding in sorted(actionable, key=lambda f: (decision_priority(f), risk_sort(f.risk_level), f.path)):
        lines.append(
            "| "
            + " | ".join(
                [
                    decision_priority(finding),
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


def write_owner_review_queue(path: Path, findings: list[Finding], generated_at: str) -> None:
    needs_owner = [
        finding
        for finding in findings
        if finding.owner_status == "missing_or_unknown"
        or finding.autonomy_mode in {"blocked", "prepare"}
    ]
    lines = [
        "# Owner Review Queue",
        "",
        f"Generated: `{generated_at}`",
        "",
        "| Owner | Path | Risk | Autonomy | Blocked Claims | Next Action |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for finding in sorted(needs_owner, key=lambda f: (owner_display(f), risk_sort(f.risk_level), f.path)):
        lines.append(
            "| "
            + " | ".join(
                [
                    owner_display(finding),
                    f"`{finding.path}`",
                    finding.risk_level,
                    finding.autonomy_mode,
                    "<br>".join(finding.blocked_claims) or "none",
                    finding.next_action,
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
            "policy_path": str(policy_path) if policy_path else "built-in defaults",
        },
        "counts": {
            "artifacts": len(findings),
            "risk": counts(findings, "risk_level"),
            "autonomy_mode": counts(findings, "autonomy_mode"),
            "mutation_types": counts(findings, "mutation_types"),
            "evidence_quality": counts(findings, "evidence_quality"),
        },
        "generated_outputs": [
            "findings.jsonl",
            "operational-state-mutation-registry.csv",
            "operational-state-mutation-registry.md",
            "decision-backlog.md",
            "owner-review-queue.md",
            "autonomy-mode-summary.md",
            "repository-state-summary.md",
            "github-protection-findings.md",
            "policy-coverage-report.md",
            "evidence-quality-map.md",
            "executive-decision-summary.md",
            "pr-risk-summary.md",
        ],
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
    args = parser.parse_args()

    repo = args.repo.resolve()
    out = args.out.resolve()
    policy_path = args.policy.resolve() if args.policy else None
    policy = load_policy(policy_path)
    out.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
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
    write_owner_review_queue(out / "owner-review-queue.md", findings, generated_at)
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
    write_policy_coverage_report(out / "policy-coverage-report.md", findings, generated_at)
    write_evidence_quality_map(out / "evidence-quality-map.md", findings, generated_at)
    write_executive_decision_summary(out / "executive-decision-summary.md", findings, generated_at)
    write_pr_risk_summary(out / "pr-risk-summary.md", findings, gh_state, generated_at)
    write_manifest(
        out / "manifest.json",
        repo,
        findings,
        git_state,
        gh_state,
        generated_at,
        policy_path,
    )

    print(f"Generated {len(findings)} findings in {out}")
    print(f"Risk counts: {counts(findings, 'risk_level')}")
    print(f"Autonomy counts: {counts(findings, 'autonomy_mode')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
