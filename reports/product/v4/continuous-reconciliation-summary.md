# Continuous Reconciliation Summary

Generated: `2026-05-23T05:46:03+00:00`

| id | cadence | source | fail_closed |
| --- | --- | --- | --- |
| github-policy-vs-observed | hourly | github-org | True |
| deploy-policy-vs-events | on_deployment_event | deployment-events | True |
| runtime-architecture-vs-telemetry | hourly | runtime-telemetry | False |
| ownership-policy-vs-activity | daily | ownership | False |
| remediation-state-vs-verification | daily | remediation-reviews | True |
