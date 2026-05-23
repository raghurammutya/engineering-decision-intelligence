#!/usr/bin/env python3
"""Scan a pilot repository for operational-state mutation capability."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CANONICAL_COMMANDS = (
    "scripts/envctl.sh",
    "scripts/governance/promote_by_environment.sh",
)

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
    evidence_status: str
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
            "evidence_status": self.evidence_status,
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


def discover_files(repo: Path) -> list[tuple[str, Path]]:
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

    return files


def read_text(path: Path, max_bytes: int = 400_000) -> str:
    data = path.read_bytes()[:max_bytes]
    return data.decode("utf-8", errors="replace")


def find_environments(text: str, relative_path: str) -> list[str]:
    source = f"{relative_path}\n{text}"
    found = [env for env, pattern in ENV_PATTERNS.items() if pattern.search(source)]
    return found or ["unknown"]


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


def strong_mutation_present(text: str, relative_path: str) -> bool:
    return has_any(STRONG_MUTATION_PATTERNS, text, relative_path)


def infer_intent(text: str, relative_path: str, mutation_types: list[str]) -> str:
    if relative_path in CANONICAL_COMMANDS:
        return "canonical_control"
    if not mutation_types:
        return "no_mutation_detected"
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


def canonical_status(text: str, relative_path: str, mutation_types: list[str]) -> str:
    normalized = text.replace("./", "")
    if relative_path in CANONICAL_COMMANDS:
        return "canonical"
    if any(command in normalized for command in CANONICAL_COMMANDS):
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
    if "prod" in envs and strong_intent and non_canonical:
        return "critical"
    if "prod" in envs and strong_intent and evidence == "missing" and non_canonical:
        return "critical"
    if high_impact.intersection(mutation_types):
        return "high"
    if "deployment" in mutation_types and envs.intersection({"staging", "prod"}):
        return "high"
    return "medium"


def autonomy_mode(level: str, canonical: str, evidence: str) -> str:
    if level == "critical":
        return "blocked"
    if level == "high" and canonical in {"canonical", "uses_canonical_command"} and evidence == "present":
        return "controlled_execute"
    if level == "high":
        return "prepare"
    if level == "medium":
        return "recommend"
    return "observe"


def blocked_claims(level: str, canonical: str, owner: str, evidence: str) -> list[str]:
    claims: list[str] = []
    if canonical == "non_canonical_or_unknown":
        claims.append("cannot claim canonical operating path")
    if owner == "missing_or_unknown":
        claims.append("cannot claim owner-approved")
    if evidence == "missing":
        claims.append("cannot claim evidence-backed safety")
    if level in {"high", "critical"}:
        claims.append("cannot claim autonomous execution readiness")
    return claims


def next_action(level: str, canonical: str, owner: str, evidence: str) -> str:
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


def scan_file(repo: Path, artifact_type: str, path: Path) -> Finding:
    relative_path = path.relative_to(repo).as_posix()
    text = read_text(path)
    mutation_types, matched_terms = find_mutations(text, relative_path)
    environments = find_environments(text, relative_path)
    evidence = "present" if has_any(EVIDENCE_PATTERNS, text, relative_path) else "missing"
    owner = "present" if has_any(OWNER_PATTERNS, text, relative_path) else "missing_or_unknown"
    canonical = canonical_status(text, relative_path, mutation_types)
    intent = infer_intent(text, relative_path, mutation_types)
    level = risk_level(mutation_types, environments, canonical, evidence, owner, intent)
    mode = autonomy_mode(level, canonical, evidence)
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
        evidence_status=evidence,
        blocked_claims=blocked_claims(level, canonical, owner, evidence),
        next_action=next_action(level, canonical, owner, evidence),
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
    return {
        "repo": run_gh(
            [
                "repo",
                "view",
                "--json",
                "nameWithOwner,visibility,defaultBranchRef,url,pushedAt",
            ],
            repo,
        ),
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
    }


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
        lines.extend(
            [
                "## GitHub State",
                "",
                f"- Repository: `{repo_info.get('nameWithOwner', 'unknown')}`",
                f"- Visibility: `{repo_info.get('visibility', 'unknown')}`",
                f"- Default branch: `{(repo_info.get('defaultBranchRef') or {}).get('name', 'unknown')}`",
                f"- Open pull requests: `{len(pr_list) if isinstance(pr_list, list) else 'unknown'}`",
                f"- Workflows visible to GitHub CLI: `{len(workflows) if isinstance(workflows, list) else 'unknown'}`",
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
            "| Path | Type | Risk | Autonomy | Canonical | Owner | Evidence | Next Action |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
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
                    finding.owner_status,
                    finding.evidence_status,
                    finding.next_action,
                ]
            )
            + " |"
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def risk_sort(level: str) -> int:
    return {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(level, 9)


def write_manifest(
    path: Path,
    repo: Path,
    findings: list[Finding],
    git_state: dict[str, object],
    gh_state: dict[str, object] | None,
    generated_at: str,
) -> None:
    manifest = {
        "generated_at": generated_at,
        "pilot_repository": str(repo),
        "inputs": {
            "workflows": ".github/workflows/*.yml",
            "scripts": "scripts/**/*.sh, scripts/**/*.py",
            "local_git_state": True,
            "github_state": gh_state is not None,
        },
        "counts": {
            "artifacts": len(findings),
            "risk": counts(findings, "risk_level"),
            "autonomy_mode": counts(findings, "autonomy_mode"),
            "mutation_types": counts(findings, "mutation_types"),
        },
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
    args = parser.parse_args()

    repo = args.repo.resolve()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    findings = [scan_file(repo, artifact_type, path) for artifact_type, path in discover_files(repo)]
    git_state = local_git_state(repo)
    gh_state = github_state(repo) if args.github else None

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
    write_manifest(out / "manifest.json", repo, findings, git_state, gh_state, generated_at)

    print(f"Generated {len(findings)} findings in {out}")
    print(f"Risk counts: {counts(findings, 'risk_level')}")
    print(f"Autonomy counts: {counts(findings, 'autonomy_mode')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
