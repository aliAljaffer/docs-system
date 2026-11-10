---
title: PCSE Home
category: GCP
description: 'Study project for the Professional Cloud Security Engineer exam. Tailored
  for a PCA-certified reader: PCA-level service knowledge is assumed. The official
  exam guide is the source of truth for scope;'
tags:
- gcp
- security
- pcse
---

<!-- imported from ObsidianVault/studies/PCSE/PCSE Home.md. Edit the source, then run sync.py. -->

# PCSE Home

`gcp` `security` `pcse`

## PCSE Exam - Home

Study project for the **Professional Cloud Security Engineer** exam. Tailored for a PCA-certified reader: PCA-level service knowledge is assumed. The official exam guide is the source of truth for scope; the Udemy course outline sets the study order; gaps are filled from Google's official documentation. The guide is standalone: all content is inline.

## Section map

| # | Section | Weight | Note |
|---|---|---|---|
| 1 | Configuring access | ~25% | [[1-configuring-access|1 - Configuring Access]] |
| 2 | Securing communications and boundary protection | ~22% | [[2-network-security|2 - Network Security]] |
| 3 | Ensuring data protection | ~23% | [[3-data-protection|3 - Data Protection]] |
| 4 | Managing operations | ~19% | [[4-managing-operations|4 - Managing Operations]] |
| 5 | Supporting compliance requirements | ~11% | [[5-compliance|5 - Compliance]] |

Sections 1 through 3 are about 70% of the exam. Do not skip operations or compliance: together they still account for about 30%.

Support notes: [[cheat-sheets|Cheat Sheets]], [[gcloud-commands|gcloud Commands]], [[final-week-checklist|Final Week Checklist]].

## Exam facts

| Item | Detail |
|---|---|
| Length | 2 hours |
| Questions | 50 to 60, multiple choice and multiple select (no partial credit on select-all); 2025 takers report forms as short as 40, expect variance |
| Cost | $200 USD |
| Delivery | Online proctored or test center; online proctoring needs a second camera (phone behind you), no breaks, no food or drinks |
| Languages | English, Japanese |
| Validity | 2 years (retake the full exam to renew) |
| Retake policy | 14 days after fail #1, 60 days after fail #2, 365 days after fail #3 |
| Recommended background | 3+ years industry, 1+ year on Google Cloud |
| Case studies | None. Unlike PCA, there are no case study questions |

Official page: https://cloud.google.com/learn/certification/cloud-security-engineer

**Time budget:** roughly 2 minutes per question. Apply PCA service knowledge quickly, then focus on the security control, its scope, and the operational detail the scenario asks for.

## Scope and priorities

| Exam domain | Course topics to master first | Course gaps (fill from official docs) |
|---|---|---|
| 1. Configuring access | Cloud Identity and Admin console; users, groups, 2-Step Verification; GCDS and SAML SSO; organization/folder/project hierarchy; organization policies; IAM roles and custom roles; service accounts, keys, scopes, and impersonation; PAM | Workforce Identity Federation, IAM Conditions and deny policies, Policy Intelligence, IAM and Cloud Storage ACL behavior, hierarchy inheritance |
| 2. Network security | VPCs, subnets, firewalls, IP addressing; Shared VPC and peering; Interconnect options; DNSSEC and Private Google Access; IAP; Cloud Armor; multi-tier and hybrid-network role plays | VPC Service Controls, restricted Google access, Private Service Connect, Cloud NAT, Cloud DNS security, Cloud NGFW application-layer inspection, Certificate Authority Service, Secure Web Proxy |
| 3. Data protection | Sensitive Data Protection (formerly DLP): infoTypes, inspection templates/jobs, de-identification; default encryption, CMEK, CSEK; Cloud Storage lifecycle; Secret Manager | BigQuery and Cloud SQL access controls, instance metadata, EKM, Confidential Computing, encryption in transit, securing AI workloads (objective 3.3) |
| 4. Operations | RPO/RTO and backups; Web Security Scanner; Security Command Center; Cloud Logging and sinks; container vulnerability scanning; Binary Authorization | Current network detection and logging options, log access controls, aggregated sinks, image hardening and VM patch management, current SCC capabilities. Forseti is retired; know it only as the predecessor of SCC policy and audit tooling |
| 5. Compliance | Shared responsibility; data location and service controls; audit evidence; compliance scenarios | Assured Workloads, Access Transparency, Access Approval, regionalization, mapping controls to requirements |

### Securing AI workloads is in scope

Objective 3.3 has three official bullets: security and privacy controls for AI/ML systems, security requirements for IaaS-hosted and PaaS-hosted training models, and security controls for Gemini Enterprise Agent Platform. The course does not cover them. Study them in [[3-data-protection|3 - Data Protection]] and the official documentation ([[vertex-ai]], [[gemini]], Model Armor). **2025 test-taker reports put AI and Vertex AI content at up to a quarter of some exam forms**, so treat objective 3.3 as a priority domain, not filler.

## Study Plan

Keep the course sequence as the spine of your schedule. Since you hold PCA, spend little time reviewing general service descriptions. Spend your time on how security controls are configured, what they protect, and how they fail.

### Pass 1: Course core

1. Complete the access modules. Practice hierarchy and policy inheritance, role selection, service account attachment, impersonation, and key-risk decisions. See [[1-configuring-access|1 - Configuring Access]].
2. Complete the networking modules. Practice firewall reasoning, Shared VPC subnet access, peering limits, IAP access, DNSSEC, Private Google Access, and the Cloud Armor scenario. See [[2-network-security|2 - Network Security]].
3. Complete the data-protection modules. Practice DLP inspection and de-identification, Secret Manager versioning, CMEK versus CSEK, and Cloud Storage lifecycle rules. See [[3-data-protection|3 - Data Protection]].
4. Complete the operations modules. Be able to explain RPO versus RTO, backup and restore choices, vulnerability scanning, Binary Authorization, audit logs, sinks, and SCC findings. See [[4-managing-operations|4 - Managing Operations]].
5. Review the role-play scenarios. For each one, state the threat, the control, where to apply it, and how to verify it.

### Pass 2: Official exam-guide gaps

Use the "Course gaps" column above. Read only the matching current exam objective and the relevant summary in these notes. Use the official documentation when you need more detail. Prioritize [[vpc-service-controls|VPC Service Controls]], current IAM controls, modern private connectivity, logging and detection, AI workload security, and compliance services.

### Final review

- Take a timed 2-hour practice exam.
- Review every wrong or guessed answer against the current official exam guide.
- Repeat weak course topics in a sandbox or by drawing the configuration from memory.
- Take another timed exam only after closing the specific gaps from the first attempt.
- Use the official exam guide's current domain weights to allocate any remaining study time.
- Finish with [[final-week-checklist|Final Week Checklist]].

### Scenario-question technique (from 2025 passers)

- Every option is usually a workable solution; **the constraint keywords pick the answer**"most secure", "minimizes cost", "least operational overhead".
- Extract the ask from the scenario first, then match Google's exact product, feature, role, or constraint name; the exam tests Google's names and config options, not general security theory.
- Eliminate the obviously wrong options first; when two viable options remain, the more specific, more managed, or more native control is usually correct.
- Draw the GMEK/CMEK/CSEK/EKM table from memory before exam day; 2025 passers report the key options blur under time pressure. See [[cheat-sheets|Cheat Sheets]].

## Related vault notes

- GCP security: [[iam|IAM]], [[cloud-kms|Cloud KMS]], [[secret-manager|Secret Manager]], [[binary-authorization|Binary Authorization]], [[identity-aware-proxy|Identity-Aware Proxy]], [[security-command-center|Security Command Center]], [[vpc-service-controls|VPC Service Controls]], [[security-labs|Security Labs]]
- GCP networking: [[vpc|VPC]], [[cloud-ngfw|Cloud NGFW]], [[cloud-armor|Cloud Armor]], [[cloud-dns|Cloud DNS]], [[cloud-load-balancing|Cloud Load Balancing]], [[cloud-vpn|Cloud VPN]], [[cloud-interconnect|Cloud Interconnect]], [[cloud-nat|Cloud NAT]], [[private-google-access-vs-psc|PGA vs PSC]], [[networking-labs|Networking Labs]]
- GCP services: [[gke|GKE]], [[compute-engine|Compute Engine]], [[cloud-run|Cloud Run]], [[bigquery|BigQuery]], [[cloud-sql|Cloud SQL]], [[cloud-storage|Cloud Storage]], [[pub-sub|Pub/Sub]], [[artifact-registry|Artifact Registry]], [[cloud-build|Cloud Build]], [[cloud-logging|Cloud Logging]], [[cloud-monitoring|Cloud Monitoring]], [[vertex-ai|Vertex AI]], [[gemini|Gemini]]
- Principles: [[principle-of-least-privilege|Least privilege]], [[multi-factor-authentication|MFA/2SV]], [[cryptography|Cryptography]], [[cidr|CIDR]], [[rto|RTO]], [[attack-detection|Attack detection]], [[attack-prevention-strategies|Attack prevention strategies]], [[respond-to-attacks|Respond to attacks]], [[threat-intelligence|Threat intelligence]]

Track progress on the Certification Journey board.
