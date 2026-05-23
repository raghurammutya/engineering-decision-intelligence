#!/usr/bin/env python3
"""Minimal CLI for Engineering Decision Intelligence."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ML_REPO = Path("/home/stocksadmin/workspace/ML")


def run(args: list[str], dry_run: bool = False) -> int:
    if dry_run:
        print(" ".join(args))
        return 0
    result = subprocess.run(args, cwd=ROOT, check=False)
    return result.returncode


def scanner_command(
    repo: Path,
    out: Path,
    policy: Path | None,
    github: bool,
    include_tools: bool,
    github_baseline: Path | None = None,
    owner_suggestions: Path | None = None,
    control_remediation: Path | None = None,
    false_positive_review: Path | None = None,
) -> list[str]:
    command = [
        sys.executable,
        "tools/operational_state_scan.py",
        "--repo",
        str(repo),
        "--out",
        str(out),
    ]
    if github:
        command.append("--github")
    if policy:
        command.extend(["--policy", str(policy)])
    if include_tools:
        command.append("--include-tools")
    if github_baseline:
        command.extend(["--github-baseline", str(github_baseline)])
    if owner_suggestions:
        command.extend(["--owner-suggestions", str(owner_suggestions)])
    if control_remediation:
        command.extend(["--control-remediation", str(control_remediation)])
    if false_positive_review:
        command.extend(["--false-positive-review", str(false_positive_review)])
    return command


def scan_ml_pilot(args: argparse.Namespace) -> int:
    return run(
        scanner_command(
            Path(args.repo),
            Path(args.out),
            Path("policies/ml-pilot-policy.json"),
            github=not args.no_github,
            include_tools=False,
            github_baseline=Path("policies/github-control-baseline.json"),
            owner_suggestions=Path("policies/ml-owner-suggestions.json"),
            control_remediation=Path("policies/control-remediation-status.json"),
            false_positive_review=Path("policies/ml-false-positive-review.json"),
        ),
        dry_run=args.dry_run,
    )


def scan_custom(args: argparse.Namespace) -> int:
    if args.repo is None or args.out is None:
        raise SystemExit("custom scans require --repo and --out")
    return run(
        scanner_command(
            Path(args.repo),
            Path(args.out),
            Path(args.policy) if args.policy else None,
            github=args.github,
            include_tools=args.include_tools,
            github_baseline=Path(args.github_baseline) if args.github_baseline else None,
            owner_suggestions=Path(args.owner_suggestions) if args.owner_suggestions else None,
            control_remediation=Path(args.control_remediation) if args.control_remediation else None,
            false_positive_review=Path(args.false_positive_review) if args.false_positive_review else None,
        ),
        dry_run=args.dry_run,
    )


def scan(args: argparse.Namespace) -> int:
    if args.target == "ml-pilot":
        if args.repo is None:
            args.repo = str(ML_REPO)
        if args.out is None:
            args.out = "reports/ml-pilot"
        return scan_ml_pilot(args)
    return scan_custom(args)


def self_scan(args: argparse.Namespace) -> int:
    return run(
        scanner_command(
            ROOT,
            Path("reports/self"),
            Path("policies/autonomy-policy.json"),
            github=False,
            include_tools=True,
            github_baseline=Path("policies/github-control-baseline.json"),
        ),
        dry_run=args.dry_run,
    )


def check_drift(args: argparse.Namespace) -> int:
    first = run(
        [sys.executable, "tools/check_report_drift.py", "--reports", "reports/ml-pilot", "--repo-root", str(ROOT)],
        dry_run=args.dry_run,
    )
    second = run(
        [sys.executable, "tools/check_report_drift.py", "--reports", "reports/self", "--repo-root", str(ROOT)],
        dry_run=args.dry_run,
    )
    return first or second


def validate(args: argparse.Namespace) -> int:
    commands = [
        [sys.executable, "-m", "py_compile", "tools/operational_state_scan.py", "tools/check_report_drift.py", "edi/__main__.py"],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
        [sys.executable, "tools/check_report_drift.py", "--reports", "reports/ml-pilot", "--repo-root", str(ROOT)],
        [sys.executable, "tools/check_report_drift.py", "--reports", "reports/self", "--repo-root", str(ROOT)],
        ["git", "diff", "--check"],
    ]
    for command in commands:
        status = run(command, dry_run=args.dry_run)
        if status:
            return status
    policy_dir = ROOT / "policies"
    for policy in sorted(policy_dir.glob("*.json")):
        status = run([sys.executable, "-c", "import json,sys; json.load(open(sys.argv[1]))", str(policy)], dry_run=args.dry_run)
        if status:
            return status
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Generate scanner reports.")
    scan_parser.add_argument("target", nargs="?", choices=["ml-pilot"], help="Optional preset target.")
    scan_parser.add_argument("--repo", help="Repository to scan.")
    scan_parser.add_argument("--out", help="Output directory for generated reports.")
    scan_parser.add_argument("--policy", help="Policy JSON for custom scans.")
    scan_parser.add_argument("--github", action="store_true", help="Include GitHub state for custom scans.")
    scan_parser.add_argument("--no-github", action="store_true", help="Disable GitHub enrichment for preset scans.")
    scan_parser.add_argument("--include-tools", action="store_true", help="Include tools/**/*.py in custom scans.")
    scan_parser.add_argument("--github-baseline", help="GitHub control baseline policy JSON.")
    scan_parser.add_argument("--owner-suggestions", help="Owner suggestion policy JSON.")
    scan_parser.add_argument("--control-remediation", help="Control remediation status JSON.")
    scan_parser.add_argument("--false-positive-review", help="False-positive review status JSON.")
    scan_parser.add_argument("--dry-run", action="store_true", help="Print commands without executing them.")
    scan_parser.set_defaults(func=scan)

    self_parser = subparsers.add_parser("self-scan", help="Generate product self-governance reports.")
    self_parser.add_argument("--dry-run", action="store_true", help="Print commands without executing them.")
    self_parser.set_defaults(func=self_scan)

    drift_parser = subparsers.add_parser("check-drift", help="Check generated report fingerprints.")
    drift_parser.add_argument("--dry-run", action="store_true", help="Print commands without executing them.")
    drift_parser.set_defaults(func=check_drift)

    validate_parser = subparsers.add_parser("validate", help="Run the safe local validation chain.")
    validate_parser.add_argument("--dry-run", action="store_true", help="Print commands without executing them.")
    validate_parser.set_defaults(func=validate)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
