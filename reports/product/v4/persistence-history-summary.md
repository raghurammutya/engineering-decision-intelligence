# Persistence History Summary

Generated: `2026-05-23T15:53:29+00:00`

Current backend: `timescaledb`
Backend observed: `timescaledb`
Backend observed at: `2026-05-23T00:00:00+00:00`

| id | type | retention_days |
| --- | --- | --- |
| event-store | append_only_jsonl_or_database | 365 |
| graph-store | json_graph_or_graph_database | 365 |
| decision-history | materialized_history | 730 |
| audit-log | append_only | 1095 |
