# 7. Cheat sheet

**Goal:** Answer scenario questions fast with decision rules.

Use these rules with the scenario technique in the [course index](index.md). The constraint keyword picks the answer.

## Service account authentication

1. [[gke]] workload: Workload Identity Federation for GKE.
2. External cloud or on-premises workload: Workload Identity Federation (keyless).
3. Human or admin needs temporary access: impersonation with Token Creator and a short lifetime.
4. Sign a URL or JWT: `signBlob` or `signJwt` with Token Creator.
5. All options fail: user-managed key with org policy, rotation, and monitoring.

## Encryption

1. Encryption at rest only: Google default.
2. Control, rotation, and revocation: CMEK with [[cloud-kms]] (software).
3. Compliance requires FIPS hardware: CMEK with Cloud KMS HSM.
4. Keys must stay outside Google: Cloud EKM.
5. Protect data in memory: Confidential Computing.
6. Per-request legacy keys: CSEK.

## Private access

1. VM to Google APIs: Private Google Access on the subnet.
2. On-premises to Google APIs: Private Google Access for on-premises hosts, VIP routes, and DNS.
3. Network that allows only Google APIs: `restricted.googleapis.com` VIP.
4. Private connection to one managed service: PSC endpoint. See [[private-google-access-vs-psc]].
5. VPC to VPC within one organization, with central control: Shared [[vpc]].
6. VPC to VPC without a shared host: VPC peering.
7. Outbound internet only: [[cloud-nat]].

## Data exfiltration and sharing

1. Wrong principal gets access: org policy for domain-restricted sharing.
2. Public data: `storage.publicAccessPrevention`.
3. Service-level exfiltration: [[vpc-service-controls]] with `gcp.resourceRestrictions`.
4. Column or row access: [[bigquery|BigQuery]] policy tags or row-level security.
5. Temporary safe sharing: signed URLs or authorized views.

## Detection

1. Known-bad IP, domain, or crypto-mining: Event Threat Detection in [[security-command-center]].
2. Misconfiguration, such as a public bucket or permissive service account: Security Health Analytics.
3. Web app vulnerabilities: Web Security Scanner.
4. Network intrusion, such as malware in packets: Cloud IDS.
5. Who did what: Cloud Audit Logs with Data Access.
6. Lateral movement in containers: Container Threat Detection.
7. Malware or ransomware on VMs: VM Threat Detection.

## AI workload security

1. Filter prompts or responses for PII, injection, or jailbreaks: Model Armor.
2. Shadow AI or unsanctioned model use: SCC AI inventory.
3. Training data confidentiality in use: Confidential Computing (Confidential VM or GKE nodes).
4. Data exfiltration from AI data projects: [[vpc-service-controls]].
5. Model artifact integrity: [[artifact-registry]] scanning and [[binary-authorization]].
6. IaaS training: you secure the stack. PaaS training: you configure access, data, and perimeter.

!!! tip "Exam tips"
    - Draw the key options table (default, CMEK, HSM, EKM, CSEK, Confidential Computing) from memory before exam day.
    - Match the rule to the constraint word in the question.
    - When two options both work, pick the more native and more managed one.

[Next: Final week checklist](08-final-week-checklist.md)
