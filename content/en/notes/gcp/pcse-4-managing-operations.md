---
title: 4 - Managing Operations
category: GCP
description: 'Part of [[pcse-home|PCSE Home]]. Official exam guide sections 4.1 to
  4.2: managing operations. Ties into [[attack-detection|Attack detection]] and [[respond-to-attacks|Respond
  to attacks]].'
tags:
- gcp
- security
- pcse
---

<!-- imported from ObsidianVault/studies/PCSE/4 - Managing Operations.md. Edit the source, then run sync.py. -->

# 4 - Managing Operations

`gcp` `security` `pcse`

## 4 - Managing Operations (~19%)

Part of [[pcse-home|PCSE Home]]. Official exam guide sections 4.1 to 4.2: managing operations. Ties into [[attack-detection|Attack detection]] and [[respond-to-attacks|Respond to attacks]].

### 4.1 Automating infrastructure and application security

- **CVE scanning in CI/CD:** Artifact Registry automatic OS vulnerability scanning on push; **on-demand scanning** for any image; results in Artifact Analysis (formerly Container Analysis), surfaced in SCC. Gate pipelines on critical CVEs.
- **Binary Authorization:**
	- Policy: default admission rule + cluster-specific rules; enforcement modes (always allow, require attestations, never allow/block all); attestors backed by PKIX keys or Cloud KMS; attestations created in the pipeline (e.g., Cloud Build + Kritis signer).
	- Works for GKE and Cloud Run (same policy API).
	- "Only images signed by our CI can deploy to prod GKE" -> Binary Authorization with attestor + attestation in Cloud Build.
- **VM and container image hardening:** Container-Optimized OS or hardened images via Image Builder; Shielded VM (secure boot, vTPM, integrity monitoring; org policy `compute.requireShieldedVm`); regular rebuilds; Artifact Registry image retention.
- **VM patch management:** **VM Manager** (OS Config agent): patch jobs (one-off) and patch policies (recurring, window-based), inventory and CVE reporting feeding SCC (OS Management). Also OS Login for access control.
- **CSPM at scale:** SCC security posture management; **custom modules for Security Health Analytics** and **custom org policies**; drift detection = comparing deployed config to policy (Terraform plan/validation, SCC posture dashboards, and org policy dry-run exports).

**Additional facts:**
- Scan results update continuously as new CVEs are discovered, not only at push; on-demand severity values: CRITICAL, HIGH, MEDIUM, LOW, MINIMAL.
- Cloud Build gate: `_SEVERITY` substitution with a regex like `"CRITICAL|HIGH"`; the build SA needs `roles/ondemandscanning.admin`.
- Gotcha: a VPC-SC perimeter restricting Cloud Storage breaks `gcloud builds submit` with PERMISSION_DENIED.
- Binary Authorization cluster flag: `--binauthz-evaluation-mode=PROJECT_SINGLETON_POLICY_ENFORCE`; policy YAML: `defaultAdmissionRule` with `evaluationMode` (ALWAYS_DENY, REQUIRE_ATTESTATION) + `enforcementMode`; dry-run audits violations while pods still run.
- The global policy allows `gcr.io/google-containers` by default; everything else hits the default admission rule.
- Each attestor requires an Artifact Analysis note; attestations are stored as note occurrences; the Binary Authorization service SA needs `roles/containeranalysis.notes.occurrences.viewer` on the note.
- Attestor signing: Cloud KMS asymmetric key `ec-sign-p256-sha256`; sign with `binauthz attestations sign-and-create --artifact-url=IMAGE@DIGEST`.
- **With attestations required, deploy by digest; mutable tags like `latest` are rejected**.
- Images: a bootable image needs a partition table plus bootable partition; imported disks must be `disk.raw`, tarred, gzip; RHEL/Windows are premium (billed hourly); `compute.trustedImageProjects` restricts sources; share via `roles/compute.imageUser`.
- Artifact Registry: regional repositories per project, repo-level IAM, put repositories inside a VPC-SC perimeter.
- Custom SHA modules (Enterprise tier only): YAML + CEL declaring scanned resources, detection logic, response (recommendation or automatic remediation); real-time mode triggers on config change, batch runs daily; uploading a module does not itself trigger a scan; the display name becomes the finding category.

### 4.2 Configuring logging, monitoring, and detection

**Network logging stack (know what each does and its config knobs):**

| Tool | What it captures | Key config points |
|---|---|---|
| VPC Flow Logs | L3/L4 flows (5-tuple, bytes/packets) | Enable per subnet (all-or-nothing); aggregation interval default 5s (5s to 15 min); sampling 0.0 to 1.0, default 0.5, cost lever |
| Cloud NGFW logs | Firewall allow/deny events with rule name | Enable per rule or policy; log to Cloud Logging |
| Packet Mirroring | Full packet copy of VM traffic | Mirror source (subnet, tags, or instance) + collector behind internal LB (`--is-mirroring-collector`) |
| Cloud IDS | Managed IDS verdicts on mirrored traffic | Create endpoint in VPC; requires Packet Mirroring; Palo Alto threat signatures |
| Log Analytics | SQL queries over log buckets | Enable on a log bucket; query in Cloud Logging UI (BigQuery engine) |

**Incident response flow:** detect (Event Threat Detection, audit logs, SCC findings), notify (SCC notification configs to Pub/Sub or email), respond and remediate (Cloud Functions triggered on findings, e.g., disable a leaked SA key), investigate and correlate (Google SecOps). See [[respond-to-attacks|Respond to attacks]].

**Logging strategy design:**
- Log buckets per domain/env with retention settings (default 30 days in Cloud Logging; buckets can retain up to 3650 days); **log views** to scope what each team can read; exclusions to cut cost.
- **Aggregated export sinks** (org/folder level, include descendants) to route audit logs to central security project bucket/BigQuery/Pub/Sub; required because org-level Admin Activity cannot be sinked with project-level sinks.
- **Exporting to external SIEM:** Pub/Sub sink (streaming) or Cloud Storage sink (batch); Google SecOps (Chronicle) ingestion for native correlation. See [[threat-intelligence|threat intelligence]].
- **Secure access to logs:** separate logging project; IAM on log views (`roles/logging.viewAccessor` with viewId); restrict sink writers; log bucket retention is enforced, and for long-term immutable copies sink to a GCS bucket with a retention lock.

**Audit logs (know these cold):**

| Log type | Default | Notes |
|---|---|---|
| Admin Activity | Always on, free | Config changes |
| Data Access | **Off by default (except BigQuery)** | Must enable per service; billable; has ADMIN_READ, DATA_READ, DATA_WRITE streams |
| System Event | On | Google-initiated changes |
| Policy Denied | On | Blocked by IAM/VPC-SC/org policy, useful for perimeter tuning |
| Access Transparency (separate) | On for eligible tiers | Google personnel access to your content |

- "Need to know who read the secret" -> Data Access logs (ADMIN_READ) for Secret Manager, which requires explicit enabling.
- Cloud Audit Logs retention in Cloud Logging: Admin Activity/System Event 400 days; Data Access 30 days (sink to bucket for longer).

**Security Command Center:**
- Tiers: **Standard** (baseline posture and misconfiguration visibility), **Premium/Enterprise** (Event Threat Detection, Security Health Analytics full coverage, Web Security Scanner, VM Manager/OS Management, Sensitive Data Protection discovery and Google SecOps integration on Enterprise, posture management/CSPM).
- Components: findings from sources (ETD, SHA, WSS, Container Threat Detection, VM Threat Detection, Rapid Vulnerability Detection, custom sources), mute rules, **continuous exports** (to Pub/Sub, BigQuery, SecOps), queries, and the response pipeline (Cloud Functions on Pub/Sub findings).
- Exam patterns: "detect crypto-mining on VMs" -> Event Threat Detection; "flag IAM misconfigurations like public buckets" -> Security Health Analytics; "export all findings for SIEM" -> continuous export to Pub/Sub.

**Additional facts:**
- Every project gets `_Required` (400 days, locked, cannot be updated) and `_Default` (30 days); **bucket locking is irreversible**.
- Log categories: platform, component (Google software on your VMs), user-written (agent), security (audit logs + Access Transparency).
- Admin Activity logs are always written, even with the Cloud Logging API disabled.
- Data Access enablement is granular: org/folder/project/billing account/service/log type, and specific principals can be exempted.
- Policy Denied logs cannot be disabled; exclusion filters keep them out of buckets.
- Firewall logs: per rule, never on implied rules, unsampled; in Shared VPC they land in the host project; query `resource.type="gce_subnetwork"` + `logs/compute.googleapis.com%2Ffirewall`.
- Flow logs are per subnet, all-or-nothing (a multi-NIC VM needs them on every attached subnet); protocols TCP, UDP, ICMP, ESP, GRE.
- Packet Mirroring: copies headers plus payloads, consumes VM (not network) bandwidth; sources: subnets, tags, or instances (same region); one collector per policy; roles `compute.packetMirroringUser` (collector project) + `packetMirroringAdmin` (source project); a firewall rule must allow mirrored traffic.
- Log buckets are regional and the location is immutable; retention 1-3650 days; retention extensions apply forward only; CMEK on a log bucket must match its location.
- Field-level access: restricted fields (textPayload, jsonPayload, protoPayload, httpRequest, labels, sourceLocation) need explicit permission.
- Sinks: destinations are log buckets, Pub/Sub, BigQuery, Cloud Storage (cross-project OK); aggregated sinks need org/folder + `--include-children`; grant the sink writer identity per destination: objectCreator (GCS), dataEditor (BQ), publisher (Pub/Sub), bucketWriter (log bucket).
- BigQuery sink default: dated tables; `--use-partitioned-table` switches to partitioned.
- Splunk: export JSON to Pub/Sub (Dataflow onward); GCS exports: lifecycle to Nearline/Coldline then delete.
- SCC: activation at project or org level, requires an organization; built-in services enable at org/folder/project; Container Threat Detection also per cluster; settings inherit.
- Premium/Enterprise SHA adds compliance benchmarks, attack exposure scores, attack paths; detectors off by default include CMEK-disabled family, `SQL_NO_ROOT_PASSWORD`, `SQL_WEAK_ROOT_PASSWORD`, `VPC_FLOW_LOGS_SETTINGS_NOT_RECOMMENDED`.

**Labs:** Security Labs (SCC, DevSecOps, GKE Security).
