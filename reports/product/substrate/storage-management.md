# Storage Management Evidence

Generated: `2026-05-23T23:46:42+00:00`

Source boundary: `declared_policy_not_live_target_evidence`
Fail closed: `True`
Live evidence completion: `100.0%`

| id | label | live_required | state | evidence |
| --- | --- | --- | --- | --- |
| volume_inventory | Persistent volume inventory recorded | True | observed_live_target_evidence | The root filesystem is 74% used and /mnt/stocksblitz-data is mounted rw at 33% used. |
| data_classification | Data classification recorded | True | observed_live_target_evidence | The data plane is partitioned into backups/database, backups/pg, backups/stocksadmin/config_service, and backups/stocksadmin/secrets. |
| backup_freshness | Backup freshness within policy | True | observed_live_target_evidence | Fresh timestamped backups are present for 2026-05-23, including config_service_20260523T120001Z.dump and secrets_bundle_20260523T121001Z.tar.gz. |
| restore_test | Restore test evidence recorded | True | observed_live_target_evidence | A scratch restore into edi_substrate_restore_test_1779551974 completed with pg_restore exit 0, 1027 catalog objects visible, and non-fatal restore warnings recorded. |
| retention_policy | Retention and archive policy recorded | True | observed_live_target_evidence | Timestamped backups are retained across 2026-05-13 through 2026-05-23, showing a multi-day retention history. |
| cleanup_admission | Cleanup admission policy recorded | True | observed_live_target_evidence | Cleanup admission policy is explicitly recorded in runtime-config/operational-substrate.json with scope and SRE/DBA approval requirements. |
