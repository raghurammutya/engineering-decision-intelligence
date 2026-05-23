# Connector SDK Summary

Generated: `2026-05-23T05:46:03+00:00`

SDK version: `connector-sdk-v1`
Dependency free: `True`
Validation command: `python3 -m edi v2 build --check`

| connector_type | input_contract | required_behavior |
| --- | --- | --- |
| repository | policies/portfolio-repositories.json | declare path, report_dir, owner, role, and evidence boundary |
| runtime | policies/runtime-connector-fixtures.json | declare source, timestamp, confidence, signal type, and related paths |
| incident | policies/incident-fixtures.json | declare incident id, severity, service, related paths, and evidence boundary |
| remediation | policies/v2-remediation-state.json | declare state, owner, expiry, evidence, and next action |
