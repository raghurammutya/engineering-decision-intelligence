#!/usr/bin/env python3
"""Minimal CLI for Engineering Decision Intelligence."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from edi.product_api import write_snapshot
from edi.product_ui import write_operator_view
from edi.v2 import build_v2_outputs, check_v2_outputs
from edi.v3 import build_v3_outputs, check_v3_outputs
from edi.v4 import build_v4_outputs, check_v4_outputs


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
        [
            sys.executable,
            "-m",
            "py_compile",
            "tools/operational_state_scan.py",
            "tools/check_report_drift.py",
            "tools/autopilot_progress.py",
            "tools/acceptance_gates.py",
            "edi/__main__.py",
            "edi/product_api.py",
            "edi/product_ui.py",
            "edi/v2.py",
            "edi/v3.py",
            "edi/v4.py",
        ],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
        [sys.executable, "tools/check_report_drift.py", "--reports", "reports/ml-pilot", "--repo-root", str(ROOT)],
        [sys.executable, "tools/check_report_drift.py", "--reports", "reports/self", "--repo-root", str(ROOT)],
        [sys.executable, "tools/autopilot_progress.py", "--check"],
        [sys.executable, "-m", "edi", "v2", "build", "--check"],
        [sys.executable, "-m", "edi", "v3", "build", "--check"],
        [sys.executable, "-m", "edi", "v4", "build", "--check"],
        [sys.executable, "tools/acceptance_gates.py"],
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


def progress(args: argparse.Namespace) -> int:
    command = [sys.executable, "tools/autopilot_progress.py"]
    if args.check:
        command.append("--check")
    if args.backlog:
        command.extend(["--backlog", args.backlog])
    if args.out:
        command.extend(["--out", args.out])
    return run(command, dry_run=args.dry_run)


def autopilot(args: argparse.Namespace) -> int:
    command = [sys.executable, "tools/autopilot_progress.py"]
    if args.autopilot_command == "next":
        command.append("--next-json" if args.json else "--next")
    elif args.autopilot_command == "checklist":
        command.append("--checklist")
    else:
        raise SystemExit(f"unsupported autopilot command: {args.autopilot_command}")
    if args.backlog:
        command.extend(["--backlog", args.backlog])
    if args.out:
        command.extend(["--out", args.out])
    return run(command, dry_run=args.dry_run)


def api(args: argparse.Namespace) -> int:
    if args.api_command != "snapshot":
        raise SystemExit(f"unsupported api command: {args.api_command}")
    out = Path(args.out) if args.out else ROOT / "reports" / "product" / "api-snapshot.json"
    if args.dry_run:
        print(f"write product API snapshot to {out}")
        return 0
    write_snapshot(ROOT, out)
    print(f"Wrote product API snapshot to {out}")
    return 0


def ui(args: argparse.Namespace) -> int:
    if args.ui_command != "build":
        raise SystemExit(f"unsupported ui command: {args.ui_command}")
    out = Path(args.out) if args.out else ROOT / "reports" / "product" / "operator-view.html"
    if args.dry_run:
        print(f"write operator UI view to {out}")
        return 0
    write_operator_view(ROOT, out)
    print(f"Wrote operator UI view to {out}")
    return 0


def v2(args: argparse.Namespace) -> int:
    if args.v2_command != "build":
        raise SystemExit(f"unsupported v2 command: {args.v2_command}")
    out = Path(args.out) if args.out else ROOT / "reports" / "product" / "v2"
    if args.dry_run:
        action = "check" if args.check else "write"
        print(f"{action} v2 operational intelligence outputs at {out}")
        return 0
    if args.check:
        check_v2_outputs(ROOT, out)
        print(f"V2 report drift check passed for {out}")
        return 0
    result = build_v2_outputs(ROOT, out)
    print(f"Wrote v2 operational intelligence outputs to {out}")
    print(f"V2 acceptance: {result['acceptance']['acceptance_state']}")
    return 0


def v3(args: argparse.Namespace) -> int:
    if args.v3_command != "build":
        raise SystemExit(f"unsupported v3 command: {args.v3_command}")
    out = Path(args.out) if args.out else ROOT / "reports" / "product" / "v3"
    if args.dry_run:
        action = "check" if args.check else "write"
        print(f"{action} v3 operationalization outputs at {out}")
        return 0
    if args.check:
        check_v3_outputs(ROOT, out)
        print(f"V3 report drift check passed for {out}")
        return 0
    result = build_v3_outputs(ROOT, out)
    print(f"Wrote v3 operationalization outputs to {out}")
    print(f"V3 acceptance: {result['acceptance']['acceptance_state']}")
    return 0


def v4(args: argparse.Namespace) -> int:
    if args.v4_command != "build":
        raise SystemExit(f"unsupported v4 command: {args.v4_command}")
    out = Path(args.out) if args.out else ROOT / "reports" / "product" / "v4"
    if args.dry_run:
        action = "check" if args.check else "write"
        print(f"{action} v4 live enforcement readiness outputs at {out}")
        return 0
    if args.check:
        check_v4_outputs(ROOT, out)
        print(f"V4 report drift check passed for {out}")
        return 0
    result = build_v4_outputs(ROOT, out)
    print(f"Wrote v4 live enforcement readiness outputs to {out}")
    print(f"V4 acceptance: {result['acceptance']['acceptance_state']}")
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

    progress_parser = subparsers.add_parser("progress", help="Generate or check product progress reports.")
    progress_parser.add_argument("--check", action="store_true", help="Fail if committed progress reports are stale.")
    progress_parser.add_argument("--backlog", help="Autopilot backlog JSON path.")
    progress_parser.add_argument("--out", help="Progress report output directory.")
    progress_parser.add_argument("--dry-run", action="store_true", help="Print commands without executing them.")
    progress_parser.set_defaults(func=progress)

    autopilot_parser = subparsers.add_parser("autopilot", help="Plan safe autopilot missions without executing them.")
    autopilot_subparsers = autopilot_parser.add_subparsers(dest="autopilot_command", required=True)

    next_parser = autopilot_subparsers.add_parser("next", help="Show the next safe autopilot mission.")
    next_parser.add_argument("--json", action="store_true", help="Print machine-readable mission details.")
    next_parser.add_argument("--backlog", help="Autopilot backlog JSON path.")
    next_parser.add_argument("--out", help="Progress report output directory.")
    next_parser.add_argument("--dry-run", action="store_true", help="Print command without executing it.")
    next_parser.set_defaults(func=autopilot)

    checklist_parser = autopilot_subparsers.add_parser("checklist", help="Show the next mission checklist.")
    checklist_parser.add_argument("--backlog", help="Autopilot backlog JSON path.")
    checklist_parser.add_argument("--out", help="Progress report output directory.")
    checklist_parser.add_argument("--dry-run", action="store_true", help="Print command without executing it.")
    checklist_parser.set_defaults(func=autopilot)

    api_parser = subparsers.add_parser("api", help="Materialize stable product API outputs.")
    api_subparsers = api_parser.add_subparsers(dest="api_command", required=True)

    snapshot_parser = api_subparsers.add_parser("snapshot", help="Write product API snapshot JSON.")
    snapshot_parser.add_argument("--out", help="Snapshot output path.")
    snapshot_parser.add_argument("--dry-run", action="store_true", help="Print command without executing it.")
    snapshot_parser.set_defaults(func=api)

    ui_parser = subparsers.add_parser("ui", help="Materialize static product UI outputs.")
    ui_subparsers = ui_parser.add_subparsers(dest="ui_command", required=True)

    build_parser = ui_subparsers.add_parser("build", help="Write static operator UI HTML.")
    build_parser.add_argument("--out", help="Operator view output path.")
    build_parser.add_argument("--dry-run", action="store_true", help="Print command without executing it.")
    build_parser.set_defaults(func=ui)

    v2_parser = subparsers.add_parser("v2", help="Materialize v2 operational intelligence outputs.")
    v2_subparsers = v2_parser.add_subparsers(dest="v2_command", required=True)

    v2_build_parser = v2_subparsers.add_parser("build", help="Write or check v2 operational intelligence reports.")
    v2_build_parser.add_argument("--out", help="V2 report output directory.")
    v2_build_parser.add_argument("--check", action="store_true", help="Fail if committed v2 reports are stale.")
    v2_build_parser.add_argument("--dry-run", action="store_true", help="Print command without executing it.")
    v2_build_parser.set_defaults(func=v2)

    v3_parser = subparsers.add_parser("v3", help="Materialize v3 operationalization outputs.")
    v3_subparsers = v3_parser.add_subparsers(dest="v3_command", required=True)

    v3_build_parser = v3_subparsers.add_parser("build", help="Write or check v3 operationalization reports.")
    v3_build_parser.add_argument("--out", help="V3 report output directory.")
    v3_build_parser.add_argument("--check", action="store_true", help="Fail if committed v3 reports are stale.")
    v3_build_parser.add_argument("--dry-run", action="store_true", help="Print command without executing it.")
    v3_build_parser.set_defaults(func=v3)

    v4_parser = subparsers.add_parser("v4", help="Materialize v4 live enforcement readiness outputs.")
    v4_subparsers = v4_parser.add_subparsers(dest="v4_command", required=True)

    v4_build_parser = v4_subparsers.add_parser("build", help="Write or check v4 readiness reports.")
    v4_build_parser.add_argument("--out", help="V4 report output directory.")
    v4_build_parser.add_argument("--check", action="store_true", help="Fail if committed v4 reports are stale.")
    v4_build_parser.add_argument("--dry-run", action="store_true", help="Print command without executing it.")
    v4_build_parser.set_defaults(func=v4)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
