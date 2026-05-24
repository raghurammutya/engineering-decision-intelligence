# Infrastructure Management Evidence

Generated: `2026-05-23T23:46:42+00:00`

Source boundary: `declared_policy_not_live_target_evidence`
Fail closed: `True`
Live evidence completion: `100.0%`

| id | label | live_required | state | evidence |
| --- | --- | --- | --- | --- |
| host_role_inventory | Host role inventory recorded | True | observed_live_target_evidence | docker ps shows separate dev, test, staging, and prod workloads, plus monitoring and data services. |
| environment_separation | Environment separation recorded | True | observed_live_target_evidence | Distinct dev, test, staging, and prod container families are present in docker ps output. |
| runner_placement | Build/test runner placement recorded | True | observed_live_target_evidence | Build/test and runtime workloads are co-located on the same host but isolated into environment-specific container sets. |
| production_runtime_boundary | Production runtime boundary recorded | True | observed_live_target_evidence | Production containers are separated from dev, test, and staging containers and run as explicit prod workloads. |
| observability_health | Observability health recorded for changed critical services | True | observed_live_target_evidence | Prometheus and Grafana containers for dev, test, staging, and prod are running healthy. |
| protected_environment | Production environment protection recorded | True | observed_live_target_evidence | GitHub prod environment exists with deployment_branch_policy.protected_branches=true and can_admins_bypass=true; protection is configured but admin bypass remains enabled. |
