# 7. Cheat sheet

**Goal:** Answer scenario questions fast with decision rules.

Use these rules with the scenario technique in the [course index](index.md). The constraint keyword picks the answer.

## Service account authentication

| Scenario | Answer |
|---|---|
| [[gke]] workload | Workload Identity Federation for GKE |
| External cloud or on-premises workload | Workload Identity Federation (keyless) |
| Human or admin needs temporary access | Impersonation with Token Creator and a short lifetime |
| Sign a URL or JWT | `signBlob` or `signJwt` with Token Creator |
| All options fail | User-managed key with org policy, rotation, and monitoring |

## Encryption

| Scenario | Answer |
|---|---|
| Encryption at rest only | Google default |
| Control, rotation, and revocation | CMEK with [[cloud-kms]] (software) |
| Compliance requires FIPS hardware | CMEK with Cloud KMS HSM |
| Keys must stay outside Google | Cloud EKM |
| Protect data in memory | Confidential Computing |
| Per-request legacy keys | CSEK |

## Private access

| Scenario | Answer |
|---|---|
| VM to Google APIs | Private Google Access on the subnet |
| On-premises to Google APIs | Private Google Access for on-premises hosts, VIP routes, and DNS |
| Network that allows only Google APIs | `restricted.googleapis.com` VIP |
| Private connection to one managed service | PSC endpoint. See [[private-google-access-vs-psc]] |
| VPC to VPC within one organization, with central control | Shared [[vpc]] |
| VPC to VPC without a shared host | VPC peering |
| Outbound internet only | [[cloud-nat]] |

## Data exfiltration and sharing

| Scenario | Answer |
|---|---|
| Wrong principal gets access | Org policy for domain-restricted sharing |
| Public data | `storage.publicAccessPrevention` |
| Service-level exfiltration | [[vpc-service-controls]] with `gcp.resourceRestrictions` |
| Column or row access | [[bigquery|BigQuery]] policy tags or row-level security |
| Temporary safe sharing | Signed URLs or authorized views |

## Detection

| Scenario | Answer |
|---|---|
| Known-bad IP, domain, or crypto-mining | Event Threat Detection in [[security-command-center]] |
| Misconfiguration, such as a public bucket or permissive service account | Security Health Analytics |
| Web app vulnerabilities | Web Security Scanner |
| Network intrusion, such as malware in packets | Cloud IDS |
| Who did what | Cloud Audit Logs with Data Access |
| Lateral movement in containers | Container Threat Detection |
| Malware or ransomware on VMs | VM Threat Detection |

## AI workload security

| Scenario | Answer |
|---|---|
| Filter prompts or responses for PII, injection, or jailbreaks | Model Armor |
| Shadow AI or unsanctioned model use | SCC AI inventory |
| Training data confidentiality in use | Confidential Computing (Confidential VM or GKE nodes) |
| Data exfiltration from AI data projects | [[vpc-service-controls]] |
| Model artifact integrity | [[artifact-registry]] scanning and [[binary-authorization]] |
| IaaS training | You secure the stack. |
| PaaS training | You configure access, data, and perimeter. |

!!! tip "Exam tips"
    - Draw the key options table (default, CMEK, HSM, EKM, CSEK, Confidential Computing) from memory before exam day.
    - Match the rule to the constraint word in the question.
    - When two options both work, pick the more native and more managed one.

[Next: Final week checklist](08-final-week-checklist.md)
