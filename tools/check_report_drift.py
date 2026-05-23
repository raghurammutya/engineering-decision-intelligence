#!/usr/bin/env python3
"""Validate generated report manifests against scanner and policy sources."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from operational_state_scan import source_fingerprint


def resolve_optional_path(repo_root: Path, value: str) -> Path | None:
    if value in {"", "none", "built-in defaults"}:
        return None
    path = Path(value)
    if path.is_absolute():
        return path
    return repo_root / path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reports", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    reports = args.reports.resolve()
    manifest_path = reports / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    inputs = manifest.get("inputs") or {}
    policy_path = resolve_optional_path(repo_root, str(inputs.get("policy_path", "")))
    baseline_path = resolve_optional_path(repo_root, str(inputs.get("github_baseline_path", "")))
    owner_suggestions_path = resolve_optional_path(repo_root, str(inputs.get("owner_suggestions_path", "")))
    control_remediation_path = resolve_optional_path(repo_root, str(inputs.get("control_remediation_path", "")))
    false_positive_review_path = resolve_optional_path(repo_root, str(inputs.get("false_positive_review_path", "")))

    expected = manifest.get("source_fingerprint")
    actual = source_fingerprint(
        repo_root,
        policy_path,
        baseline_path,
        owner_suggestions_path,
        control_remediation_path,
        false_positive_review_path,
    )
    if expected != actual:
        raise SystemExit(
            "Report drift detected: source_fingerprint does not match scanner/policy sources. "
            "Regenerate the reports."
        )

    missing = []
    for output in manifest.get("generated_outputs") or []:
        if not (reports / output).exists():
            missing.append(output)
    if missing:
        raise SystemExit(f"Report manifest lists missing outputs: {', '.join(missing)}")

    print(f"Report drift check passed for {reports}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
