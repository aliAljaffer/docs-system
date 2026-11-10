---
title: Cheat Sheets
category: GCP
description: 'Part of PCSE Home. Decision rules for scenario questions. Used with
  the scenario-question technique: the constraint keywords pick the answer.'
tags:
- gcp
- security
- pcse
---

<!-- imported from ObsidianVault/studies/PCSE/Cheat Sheets.md. Edit the source, then run sync.py. -->

# Cheat Sheets

`gcp` `security` `pcse`

## Cheat Sheets

Part of [[pcse-home|PCSE Home]]. Decision rules for scenario questions. Used with the scenario-question technique: the constraint keywords pick the answer.

### Service account authentication
1. [[gke|GKE]] workload -> Workload Identity Federation for GKE.
2. External cloud/on-prem workload -> Workload Identity Federation (keyless).
3. Human/admin temp access -> impersonation with Token Creator, TTL'd.
4. Sign URL/JWT -> signBlob/signJwt with Token Creator.
5. Everything else failed -> user-managed key + org policy + rotation + monitoring. See [[1-configuring-access|1 - Configuring Access]].

### Encryption
1. Just need encryption at rest -> default.
2. Need control/rotation/revocation -> CMEK (software). See [[cloud-kms|Cloud KMS]].
3. Compliance requires FIPS hardware -> CMEK with HSM.
4. Keys must stay outside Google -> Cloud EKM.
5. Must protect memory/in-use -> Confidential Computing.
6. Per-request legacy -> CSEK. See [[3-data-protection|3 - Data Protection]].

### Private access
1. VM to Google APIs -> PGA on subnet.
2. On-prem to Google APIs -> PGA for on-prem hosts + VIP routes + DNS.
3. Only-Google-APIs network -> restricted.googleapis.com VIP.
4. Private connection to a specific managed service -> PSC endpoint. See [[private-google-access-vs-psc|PGA vs PSC]].
5. VPC-to-VPC within org with central control -> Shared [[vpc|VPC]].
6. VPC-to-VPC without shared host -> VPC peering.
7. Outbound internet only -> [[cloud-nat|Cloud NAT]]. See [[2-network-security|2 - Network Security]].

### Data exfiltration / sharing control
1. [[iam|IAM]] wrong principal -> org policy domain-restricted sharing.
2. Public data -> storage.publicAccessPrevention.
3. Service-level exfiltration -> [[vpc-service-controls|VPC-SC]] + gcp.resourceRestrictions.
4. Fine-grained column/row -> [[bigquery|BigQuery]] policy tags / RLS.
5. Temporary safe sharing -> signed URLs, authorized views.

### Detection
1. Known-bad IP/domain/crypto-mining -> Event Threat Detection ([[security-command-center|SCC]]).
2. Misconfiguration (public bucket, permissive SA) -> Security Health Analytics.
3. Web app vulnerabilities -> Web Security Scanner.
4. Network intrusion (malware in packets) -> Cloud IDS.
5. Who did what -> Cloud Audit Logs (+ Data Access).
6. Lateral movement in containers -> Container Threat Detection.
7. Malware or ransomware running on VMs -> VM Threat Detection (SCC). See [[attack-detection|Attack detection]], [[4-managing-operations|4 - Managing Operations]].

### AI workload security
1. Prompt or response filtering (PII, injection, jailbreak) -> Model Armor.
2. Shadow AI / unsanctioned model usage -> SCC AI inventory.
3. Training data confidentiality in use -> Confidential Computing (Confidential VM/GKE).
4. Data exfiltration from AI data projects -> VPC Service Controls.
5. Model artifact integrity -> [[artifact-registry|Artifact Registry]] scanning + [[binary-authorization|Binary Authorization]].
6. IaaS training -> you secure the stack. PaaS training -> you configure access, data, perimeter. See [[3-data-protection|3 - Data Protection]].
