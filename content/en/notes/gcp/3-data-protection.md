---
title: 3 - Data Protection
category: GCP
description: 'Part of PCSE Home. Official exam guide sections 3.1 to 3.3: ensuring
  data protection.'
tags:
- gcp
- security
- pcse
---

<!-- imported from ObsidianVault/studies/PCSE/3 - Data Protection.md. Edit the source, then run sync.py. -->

# 3 - Data Protection

`gcp` `security` `pcse`

## 3 - Data Protection (~23%)

Part of [[pcse-home|PCSE Home]]. Official exam guide sections 3.1 to 3.3: ensuring data protection.

### 3.1 Protecting sensitive data and preventing data loss

**Sensitive Data Protection (formerly Cloud DLP), config-level:**

- **Inspection templates:** infoTypes (built-in + custom dictionaries/regex), scan sets ([[bigquery|BigQuery]], [[cloud-storage|Cloud Storage]], [[pub-sub|Pub/Sub]], streaming), likelihood thresholds, result limits.
- **De-identification:** redaction, masking, replacement, **pseudonymization** (crypto hash or deterministic token), **format-preserving encryption (FPE, FF1/AES-256)** with a KMS-wrapped key. FPE preserves format and length, reversible with the wrapped key; tokenization can be deterministic for joinability.
- **Discovery:** data profiling for BigQuery and Cloud Storage at org/folder/project level; profiles surface sensitivity and risk scores; can feed [[security-command-center|SCC]].
- **Job triggers:** schedule inspections; store findings to BigQuery for alerting.
- Exam pattern: "analyze stored data for PII on a schedule and redact before export" -> inspection template + job trigger + de-identify template.

**Restricting access to data services:**

- **[[bigquery|BigQuery]]:** [[iam|IAM]] at dataset/table level, **policy tags** + column-level security (Data Catalog / Dataplex policy tags), **row-level security** filter expressions, authorized views/datasets/routines to share without table access, CMEK, [[vpc-service-controls|VPC-SC]] for exfiltration. Know the difference: column ACLs (policy tags) vs row filters vs authorized views.
- **[[cloud-storage|Cloud Storage]]:** UBLA, public access prevention (org policy + bucket level), retention policies + bucket lock (WORM, irreversible), object versioning, CMEK, signed URLs for temporary access, ACLs only when UBLA off.
- **[[cloud-sql|Cloud SQL]]:** private IP (with PSA or PSC), IAM database authentication, CMEK, encrypted connections, no public IP flag.
- **[[secret-manager|Secret Manager]]:** versions (enable/disable/destroy), replication policy (auto or user-managed regions), CMEK, rotation (manual + [[cloud-scheduler|Cloud Scheduler]]/Function pattern or terraform), per-secret IAM, audit logging. "Database credentials for an app, must rotate quarterly and never appear in code" -> Secret Manager + rotation + WIF/impersonation for app identity.

**Protecting instance metadata:**
- Restrict guest attribute access (`compute.disableGuestAttributesAccess`), require OS Login (`compute.requireOsLogin`) so SSH keys are IAM-managed, disable serial ports (`compute.disableSerialPortAccess`), and disable legacy metadata server endpoints. Treat the metadata server as a secrets surface: put secrets in Secret Manager, not startup scripts or metadata.

**Additional facts:**
- Transformation picks: masking (fixed character per character, preserves length), replacement (value -> infoType label like `[CREDIT_CARD_NUMBER]`), bucketing (generalized ranges for usability), `dateShiftConfig`.
- Tokenization preserves referential integrity: `GROUP BY` still counts per user without revealing identity; protect the token key more strictly than the data.
- De-identified data is obfuscated real data; synthetic data is artificially generated.
- Inspection rules: hotword rules raise likelihood; exclusion rules reduce matches; config shapes: `redactConfig`, `replaceConfig`, `characterMaskConfig`, `cryptoHashConfig`.
- `minLikelihood` values: VERY_LIKELY, LIKELY, POSSIBLE, UNLIKELY, VERY_UNLIKELY.
- Tokenization types: crypto hash (HMAC-SHA-256, irreversible), FPE (FFX, reversible), deterministic encryption (AES-SIV, reversible, any character set, joinable).
- FPE needs 2+ characters, ASCII, alphabet of 2-95 characters; **the KMS key ring must be global or in the SDP region or calls fail**; `surrogateInfoType` labels the token; re-identify with `reidentifyConfig`.
- BigQuery column security needs the Data Catalog API + BigQuery Data Policy API; dynamic data masking rules: hash, year-only dates, masked email prefix, last-four SSN; `roles/datacatalog.categoryFineGrainedReader` exempts a principal from masking; querying also needs `bigquery.jobs.create`.
- Secret Manager: versions are immutable (rotation = new version); user-managed replication via `--locations`; `--out-file` for binary secrets; per-environment projects; VPC-SC perimeter around Secret Manager; monitor via Cloud Asset Inventory + Data Access logs.

### 3.2 Managing encryption at rest, in transit, and in use

Decision table (memorize):

| Option | Who controls keys | When to choose |
|---|---|---|
| Google default encryption | Google | Default; always on, AES-256 |
| CSEK (customer-supplied, passed per request) | You (per request, not stored, or stored wrapped) | Legacy/specific compliance patterns, rare |
| CMEK via [[cloud-kms|Cloud KMS]] (software) | You (in Cloud KMS) | Need key control, rotation, revocation (access revoked by disabling key) |
| CMEK with Cloud KMS HSM (hardware) | You (FIPS 140-2 L3) | Compliance requires hardware keys |
| Cloud EKM | You (external key manager: Fortanix, Thales, etc.) | Keys must live outside Google; via [[vpc|VPC]] endpoints to EKM |
| Confidential Computing | Google + TEE hardware | Protect data *in use* (memory encryption) |

See [[cryptography|Cryptography]] for the underlying concepts.

**Encryption in transit:**
- Google encrypts traffic between its data centers by default; services expose TLS endpoints.
- Your controls: SSL policies on load balancers (minimum TLS version and ciphers), VPC-SC so API traffic stays on Google's network, and encrypted hybrid paths.
- Hybrid: HA VPN encrypts with IPsec by default; Dedicated Interconnect can be encrypted with MACsec (also IPsec over Interconnect). "Regulatory requirement to encrypt all traffic between on-prem and VPC" -> HA VPN (IPsec) or MACsec on Dedicated Interconnect.

**Key management specifics:**
- Hierarchy: key ring (regional) > key (with purpose) > key version (state: enabled, disabled, scheduled destroy, destroyed). Rotation via schedule creates new versions; old versions remain for decryption (rotation does not re-encrypt existing data by default).
- Revocation: disable a key version to immediately block decryption; destroy is scheduled (minimum 24 hours before the version is destroyed) and destroyed versions are irreversible.
- Key import: import jobs with wrapping method (RSA-OAEP), import only into keys marked import-only; imported versions cannot be backed up/exported.
- CMEK gaps: some services do not support CMEK (use `gcp.restrictNonCmekServices` org policy to enforce CMEK-only where supported).
- EKM: key availability matters (if EKM is unreachable, data access fails), VPC EKM endpoints keep traffic private.
- **Auditing key usage: enable Data Access logs on Cloud KMS (`cryptoKeyVersions.decrypt` events) to prove who decrypted what**; pairs with CMEK for evidence questions.

**[[cloud-storage|Cloud Storage]] lifecycle policies:** transition to Coldline/Archive and delete; retention policies and bucket lock for immutability (once locked, the retention policy cannot be removed until it expires).

**Confidential Computing:**
- Confidential VM (AMD SEV/SEV-SNP, Intel TDX): memory encrypted, host/Google staff cannot read.
- Confidential GKE / Confidential Space (TEE-based workloads, data collaboration between parties without sharing raw data).
- Use case wording on the exam: "regulatory requirement that no one, including Google, can inspect memory" or "multi-party data collaboration".

**Additional facts:**
- CMEK is envelope encryption: your KEK wraps the service's DEKs; CMEK adds control (disable, rotate, locality) and KMS cost, not baseline strength; unlimited key versions.
- Exactly one primary version per key; ciphertext records the version used; states: PENDING_GENERATION -> ENABLED -> DISABLED -> DESTROY_SCHEDULED -> DESTROYED.
- Rotation is not automatic at creation: set `--rotation-period` plus `--next-rotation-time`.
- Asymmetric keys: callers only get `getPublicKey` + `asymmetricDecrypt`; encryption happens client-side.
- CSEK applies only to Cloud Storage and Compute Engine; AES-256 key wrapped RSA-OAEP with Google's ingress certificate; pass via `--csek-key-file`; a disk showing `kmsKeyName` = CMEK, `sha256` = CSEK.
- EKM: keys never stored or cached at Google; each version combines external key material, a key reference, and internal KMS material; Key Access Justifications restricts the partner to allowed justification codes.
- Storage lifecycle has only three actions: Delete, SetStorageClass, AbortIncompleteMultipartUpload; Delete beats SetStorageClass on conflict; changes take up to 24 hours; `--lifecycle-file` works only on `buckets update`.
- In transit: TLS terminates at the Google Front End; VM-to-VM traffic is always encrypted unless both VMs use external IPs; extra options: IPsec tunnels, managed SSL certificates, S/MIME, Istio.
- Confidential family: Confidential VM, GKE Nodes, [[dataflow|Dataflow]], [[dataproc|Dataproc]], Space; SEV VMs on N2D support live migration; GKE node keys are generated in hardware and never leave the processor.

### 3.3 Securing AI workloads

Objective 3.3 has three official bullets. Track them directly. See also [[vertex-ai]] and [[gemini]].

**1. Security and privacy controls for AI/ML systems (protect data and models from unintentional exploitation):**

- Think in three layers: the data, the model, and the user interaction layer. Exam scenarios name one of the three; pick the control that matches.
- Data: Sensitive Data Protection discovery and redaction on training data, CMEK on data and model artifacts, [[vpc-service-controls|VPC Service Controls]] perimeters around data projects, IAM [[principle-of-least-privilege|least privilege]] on datasets.
- Models: vulnerability scanning and signed images in [[artifact-registry|Artifact Registry]], [[binary-authorization|Binary Authorization]] for model-serving workloads, per-endpoint IAM, Vertex AI Model Monitoring for anomaly detection.
- Interaction: Model Armor on endpoints to screen prompts and responses.
- Governance: SAIF (Secure AI Framework) is Google's blueprint for AI security. SCC gives AI asset discovery (shadow AI visibility) and the Recommended AI Controls framework via Audit Manager.
- Exam patterns: "prevent sensitive data leaking through model prompts or responses" -> Model Armor. "discover unsanctioned AI usage" -> SCC AI inventory. "protect training data in use" -> Confidential Computing.

**2. Security requirements for IaaS-hosted vs PaaS-hosted training:**

- IaaS-hosted ([[compute-engine|Compute Engine]] or [[gke|GKE]] with GPUs/TPUs): you secure the whole stack. Hardened images, VM Manager patching, CMEK on data, private networking (no public IPs, PGA or PSC), Confidential VMs or Confidential GKE nodes for sensitive training data, secure CI/CD for training pipelines.
- PaaS-hosted ([[vertex-ai|Vertex AI]]): Google secures the infrastructure. You configure IAM per ML role (data scientist, trainer, deployer), data access controls, CMEK, VPC-SC perimeters, PSC private endpoints, and Model Armor.
- One-sentence exam answer: IaaS means you secure infrastructure and platform; PaaS means Google secures infrastructure and you configure access, data, and perimeter controls.

**3. Security controls for Gemini Enterprise Agent Platform:**

- Model Armor provides unified runtime guardrails for first-party Gemini models and third-party or open models on the platform: prompt injection and jailbreak filters, PII and unsafe content filters, malicious URL detection.
- Data controls for Gemini Enterprise: your prompts and responses are not used to train Google models, and you control logging and retention.
- Agents are identities: give agent principals least-privilege IAM on the resources they can reach.
- Exam pattern: "apply the same guardrails to Gemini and third-party models on the platform" -> Model Armor.

**Vertex AI specifics (2025 exams lean on these):**
- Dedicated VPC-SC perimeters for Vertex AI: separate perimeters for training data projects vs serving and model endpoints.
- Public endpoint, restricted: expose a public Vertex AI endpoint but gate it with a VPC-SC access level, vs fully private endpoints.
- [[private-google-access-vs-psc|Private Service Connect]] endpoints for Vertex AI give private access from your VPC, including multicloud access.
- Custom route exports: advertise your VPC's custom routes to Google's service network so managed Vertex AI components can reach back into your network (Private Services Access).
