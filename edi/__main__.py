#!/usr/bin/env python3
"""Minimal CLI for Engineering Decision Intelligence."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str]) -> int:
    result = subprocess.run(args, cwd=ROOT, check=False)
    return result.returncode


def scan_ml_pilot(args: argparse.Namespace) -> int:
    command = [
        "python3",
        "tools/operational_state_scan.py",
        "--repo",
        str(args.repo),
        "--out",
        "reports/ml-pilot",
        "--github",
        "--policy",
        "policies/ml-pilot-policy.json",
        "--github-baseline",
        "policies/github-control-baseline.json",
        "--owner-suggestions",
        "policies/ml-owner-suggestions.json",
        "--control-remediation",
        "policies/control-remediation-status.json",
        "--false-positive-review",
        "policies/ml-false-positive-review.json",
    ]
    return run(command)


def self_scan(_: argparse.Namespace) -> int:
    return run(
        [
            "python3",
            "tools/operational_state_scan.py",
            "--repo",
            str(ROOT),
            "--out",
            "reports/self",
            "--policy",
            "policies/autonomy-policy.json",
            "--github-baseline",
            "policies/github-control-baseline.json",
            "--include-tools",
        ]
    )


def check_drift(_: argparse.Namespace) -> int:
    first = run(["python3", "tools/check_report_drift.py", "--reports", "reports/ml-pilot", "--repo-root", str(ROOT)])
    second = run(["python3", "tools/check_report_drift.py", "--reports", "reports/self", "--repo-root", str(ROOT)])
    return first or second


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Generate reports for a known target.")
    scan_subparsers = scan_parser.add_subparsers(dest="target", required=True)
    ml_parser = scan_subparsers.add_parser("ml-pilot", help="Scan the ML pilot repository.")
    ml_parser.add_argument("--repo", default="/home/stocksadmin/workspace/ML")
    ml_parser.set_defaults(func=scan_ml_pilot)

    self_parser = subparsers.add_parser("self-scan", help="Generate product self-governance reports.")
    self_parser.set_defaults(func=self_scan)

    drift_parser = subparsers.add_parser("check-drift", help="Check generated report fingerprints.")
    drift_parser.set_defaults(func=check_drift)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
