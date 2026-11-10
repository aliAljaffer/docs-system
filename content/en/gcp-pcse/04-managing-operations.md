# 4. Managing operations

**Goal:** Scan and gate workloads, harden and patch systems, collect and route logs, and detect and respond to threats.

## Scan and gate workloads

- [[artifact-registry]] scans OS vulnerabilities automatically on push. You can also run on-demand scanning on any image.
- Results go to Artifact Analysis (formerly Container Analysis) and show in [[security-command-center]].
- Scan results update as new CVEs appear. They do not update only at push.
- Severity values: CRITICAL, HIGH, MEDIUM, LOW, MINIMAL.
- Gate pipelines on critical CVEs. In [[cloud-build]], use a `_SEVERITY` substitution with a regex such as `CRITICAL|HIGH`. The build service account needs `roles/ondemandscanning.admin`.
- A [[vpc-service-controls]] perimeter around Cloud Storage breaks `gcloud builds submit` with PERMISSION_DENIED.
- Put Artifact Registry inside a VPC Service Controls perimeter.

### Binary Authorization

[[binary-authorization]] allows only trusted images to deploy to [[gke]] and [[cloud-run]].

- A policy has a default admission rule and optional cluster-specific rules.
- Evaluation modes: ALWAYS_DENY and REQUIRE_ATTESTATION.
- Enforcement modes: enforce, or dry run. Dry run logs violations, and pods keep running.
- The global policy allows `gcr.io/google-containers` by default. Other images hit the default admission rule.
- Each attestor needs an Artifact Analysis note. Attestations are stored as note occurrences.
- Attestors use PKIX keys or a [[cloud-kms|Cloud KMS]] asymmetric key (`ec-sign-p256-sha256`).
- The Binary Authorization service account needs `roles/containeranalysis.notes.occurrences.viewer` on the note.
- When attestations are required, deploy by digest. Mutable tags such as `latest` are rejected.

```bash
gcloud container binauthz policy import|export
gcloud container binauthz attestations create
gcloud beta container binauthz attestations sign-and-create --artifact-url=IMAGE@DIGEST
gcloud container clusters create ... --binauthz-evaluation-mode=PROJECT_SINGLETON_POLICY_ENFORCE
```

## Harden and patch

- Use Container-Optimized OS or hardened images from Image Builder. Rebuild regularly. Set image retention in Artifact Registry.
- Shielded VM adds secure boot, vTPM, and integrity monitoring. Enforce it with `compute.requireShieldedVm`.
- `compute.trustedImageProjects` restricts which projects can supply images. Share images with `roles/compute.imageUser`.
- VM Manager (OS Config agent) runs one-off patch jobs and recurring patch policies with maintenance windows.
- VM Manager inventory and CVE reports feed SCC (OS Management). Use OS Login for access.
- Custom Security Health Analytics modules (Enterprise tier) use YAML and CEL. Real-time modules run on config change. Batch modules run daily. Uploading a module does not trigger a scan. The display name becomes the finding category.
- Use SCC posture management to find drift between deployed config and policy.

## Network logging

| Tool | Captures | Key settings |
|---|---|---|
| [[vpc]] Flow Logs | L3 and L4 flows (5-tuple, bytes, packets) | Per subnet, all or nothing. Aggregation interval from 5 seconds (default) to 15 minutes. Sampling from 0.0 to 1.0 (default 0.5). Sampling is a cost lever. |
| [[cloud-ngfw]] logs | Firewall allow and deny events with rule name | Per rule or per policy. Logs go to [[cloud-logging]]. |
| Packet Mirroring | Full copy of VM traffic | Source is a subnet, tags, or instances. Collector sits behind an internal load balancer (`--is-mirroring-collector`). |
| Cloud IDS | Managed IDS verdicts on mirrored traffic | Needs an endpoint in the VPC and Packet Mirroring. Uses Palo Alto threat signatures. |
| Log Analytics | SQL queries over log buckets | Enable on a log bucket. Query in the Logging UI with the [[bigquery|BigQuery]] engine. |

- Flow log protocols: TCP, UDP, ICMP, ESP, GRE.
- A multi-NIC VM needs flow logs on every attached subnet.
- Packet Mirroring copies headers and payloads. It uses VM bandwidth, not network bandwidth. Sources must be in the same region as the collector.
- Packet Mirroring roles: `compute.packetMirroringUser` in the collector project and `compute.packetMirroringAdmin` in the source project. A firewall rule must allow mirrored traffic.

## Audit logs

| Log type | Default | Notes |
|---|---|---|
| Admin Activity | On, always. No charge. | Configuration changes. Written even if the Cloud Logging API is disabled. |
| Data Access | Off, except BigQuery | Billable. Streams: ADMIN_READ, DATA_READ, DATA_WRITE. Enable per service. |
| System Event | On | Changes that Google makes |
| Policy Denied | On | Denials from [[iam|IAM]], VPC Service Controls, or org policy. Cannot be disabled. Exclusion filters keep it out of buckets. Useful to tune perimeters. |
| Access Transparency | On for eligible tiers | Google staff access to your content. Covered in [Lesson 5](05-compliance.md). |

- Retention in Cloud Logging: Admin Activity and System Event logs keep 400 days. Data Access logs keep 30 days. Sink to a bucket for longer retention.
- To find who read a secret, enable Data Access logs (ADMIN_READ) on [[secret-manager]].
- Data Access logging can be set at the organization, folder, project, billing account, service, or log type level. You can exempt specific principals.

## Log buckets, views, and sinks

- Every project has `_Required` (400 days, locked, cannot be changed) and `_Default` (30 days).
- Bucket locking is irreversible.
- Log buckets are regional. The location cannot change. Retention runs from 1 to 3650 days. You can extend retention, but only forward.
- A CMEK key on a log bucket must match the bucket's location.
- Use log buckets per domain or environment. Use log views to limit what a team can read. Use exclusions to cut cost.
- Restricted fields (`textPayload`, `jsonPayload`, `protoPayload`, `httpRequest`, `labels`, `sourceLocation`) need explicit permission.
- Grant `roles/logging.viewAccessor` with a `viewId` to limit view access.

### Aggregated export sinks

- Create aggregated sinks at the organization or folder level with `--include-children`. Use them to route audit logs centrally.
- Org-level Admin Activity logs cannot be sent with project-level sinks.
- Sink destinations: log bucket, Pub/Sub, BigQuery, and [[cloud-storage|Cloud Storage]]. Cross-project destinations work.
- Grant the sink writer identity the role for its destination: `objectCreator` (Cloud Storage), `dataEditor` (BigQuery), `publisher` ([[pub-sub|Pub/Sub]]), or `bucketWriter` (log bucket).
- BigQuery sinks write dated tables by default. `--use-partitioned-table` writes partitioned tables.
- For a SIEM, export with a Pub/Sub sink for streaming or a Cloud Storage sink for batch. Google SecOps ingests logs for native correlation.

## Security Command Center (SCC)

- **Standard:** Baseline posture and misconfiguration visibility.
- **Premium and Enterprise:** Event Threat Detection, full Security Health Analytics, Web Security Scanner, VM Manager and OS Management, Sensitive Data Protection discovery, Google SecOps integration (Enterprise), and posture management.
- Components: findings from sources, mute rules, continuous exports to Pub/Sub, BigQuery, or SecOps, queries, and response pipelines. [[cloud-functions|Cloud Functions]] can respond to Pub/Sub findings.
- SCC needs an organization. Activate it at the project or organization level. Settings inherit.
- Container Threat Detection also turns on per cluster.
- Premium and Enterprise Security Health Analytics adds compliance benchmarks, attack exposure scores, and attack paths.
- Detectors that are off by default include the CMEK-disabled family, `SQL_NO_ROOT_PASSWORD`, `SQL_WEAK_ROOT_PASSWORD`, and `VPC_FLOW_LOGS_SETTINGS_NOT_RECOMMENDED`.

### Detection tools by threat

| Threat or question | Tool |
|---|---|
| Known-bad IP, domain, or crypto-mining | Event Threat Detection |
| Misconfiguration, such as a public bucket or a permissive service account | Security Health Analytics |
| Web app vulnerabilities | Web Security Scanner |
| Network intrusion, such as malware in packets | Cloud IDS |
| Who did what | Cloud Audit Logs (with Data Access) |
| Lateral movement in containers | Container Threat Detection |
| Malware or ransomware on VMs | VM Threat Detection |

### Incident response flow

1. Detect with Event Threat Detection, audit logs, and SCC findings.
2. Notify with SCC notification configs to Pub/Sub or email.
3. Respond with Cloud Functions triggered by findings. For example, disable a leaked service account key.
4. Investigate and correlate in Google SecOps.

### Retired tooling

Forseti is retired. Know it only as the predecessor of SCC policy and audit tooling.

!!! tip "Exam tips"
    - Data Access logs are off by default, except BigQuery. Turn them on when a question asks who read data.
    - Admin Activity logs are always on and free.
    - Policy Denied logs help tune VPC Service Controls perimeters.
    - Use an aggregated sink for org-wide audit logs.
    - Bucket locking cannot be reversed.
    - Dry run mode in Binary Authorization audits violations without blocking pods.
    - Map each threat to its detector. Event Threat Detection and Security Health Analytics answer different questions.
    - Continuous export to Pub/Sub is the answer for "export all findings to a SIEM."

Labs: [[security-labs]] (SCC, DevSecOps, GKE Security).

[Next: Compliance](05-compliance.md)
