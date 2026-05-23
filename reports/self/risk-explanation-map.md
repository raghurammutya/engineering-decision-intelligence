# Risk Explanation Map

Generated: `2026-05-23T03:22:58+00:00`

This view explains why each scanned artifact received its current risk and autonomy classification.

| Path | Risk | Autonomy | Family | Explanation |
| --- | --- | --- | --- | --- |
| `tools/operational_state_scan.py` | high | controlled_execute | config_secret_scripts | mutation capability detected: deployment, database, configuration, broker_order, queue_stream, ai_agent<br>environment evidence: prod, staging, test, dev<br>canonical evidence: uses_canonical_command<br>evidence reference is present<br>intent inference: operational_mutation<br>matched scanner terms: deployment:deploy, deployment:promote_by_environment, database:migration, database:db, database:TRUNCATE |
| `tools/acceptance_gates.py` | medium | recommend | other_scripts | mutation capability detected: deployment<br>canonical operating path is unknown<br>evidence reference is present<br>intent inference: operational_mutation<br>matched scanner terms: deployment:deployment |
| `.github/workflows/ci.yml` | low | observe | other_workflows | no operational-state mutation capability detected<br>environment evidence: test, dev<br>owner boundary is missing or unknown<br>evidence reference is present |
| `tools/autopilot_progress.py` | low | observe | other_scripts | no operational-state mutation capability detected<br>owner boundary is missing or unknown<br>evidence reference is present |
| `tools/check_report_drift.py` | low | observe | other_scripts | no operational-state mutation capability detected<br>owner boundary is missing or unknown<br>safety or rollback evidence is missing |
