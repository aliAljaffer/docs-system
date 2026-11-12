# 3. Data protection

**Goal:** Find sensitive data, control access to data services, and manage encryption keys.

## Sensitive Data Protection

Sensitive Data Protection was formerly Cloud DLP.

- **Inspection templates:** Set infoTypes (built-in, custom dictionaries, or regex), likelihood thresholds, and result limits.
- **Scan targets:** [[bigquery]], [[cloud-storage]], [[pub-sub]], and streaming content.
- **Job triggers:** Schedule inspections. Store findings in BigQuery for alerts.
- **Discovery:** Profile BigQuery and Cloud Storage at the organization, folder, or project level. Profiles show sensitivity and risk scores. Profiles can feed [[security-command-center]].

Exam pattern: "Scan stored data for PII on a schedule and redact before export." Answer: an inspection template, a job trigger, and a de-identify template.

### De-identification methods

| Method | What it does |
|---|---|
| Redaction | Removes the value |
| Masking | Replaces each character with a fixed character. Keeps the length. |
| Replacement | Replaces the value with its infoType label, such as `[CREDIT_CARD_NUMBER]` |
| Bucketing | Replaces values with ranges |
| Date shifting | Shifts dates using `dateShiftConfig` |
| Crypto hash | HMAC-SHA-256. Irreversible. |
| Format-preserving encryption (FPE) | FFX. Reversible with a KMS-wrapped key. Keeps format and length. |
| Deterministic encryption | AES-SIV. Reversible. Works with any character set. Values can be joined. |

- Tokenization keeps referential integrity. `GROUP BY` still counts per user without showing identity. Protect the token key more strictly than the data.
- FPE needs at least 2 characters. Use ASCII. The alphabet has 2 to 95 characters.
- The KMS key ring must be global or in the same region as Sensitive Data Protection. Otherwise the calls fail.
- `surrogateInfoType` labels the token. Use `reidentifyConfig` to reverse it.
- Hotword rules raise likelihood. Exclusion rules reduce matches.
- Likelihood values: VERY_LIKELY, LIKELY, POSSIBLE, UNLIKELY, VERY_UNLIKELY.
- De-identified data is real data with values hidden. Synthetic data is generated.

## Restricting access to data services

| Service | Controls |
|---|---|
| [[bigquery]] | IAM at dataset and table level. Policy tags for column-level security. Row-level security filters. Authorized views, datasets, and routines. CMEK. [[vpc-service-controls]] for exfiltration. |
| [[cloud-storage]] | Uniform bucket-level access. Public access prevention. Retention policies and bucket lock. Object versioning. CMEK. Signed URLs. ACLs only when UBLA is off. |
| [[cloud-sql]] | Private IP (with Private Services Access or PSC). IAM database authentication. CMEK. Encrypted connections. No public IP. |
| [[secret-manager]] | Versions (enable, disable, destroy). Replication (automatic or user-managed with `--locations`). CMEK. Rotation. Per-secret IAM. Audit logging. |

- Column security for BigQuery needs the Data Catalog API and the BigQuery Data Policy API.
- BigQuery dynamic masking rules: hash, year-only dates, masked email prefix, last four of SSN.
- The role `roles/datacatalog.categoryFineGrainedReader` exempts a principal from masking.
- Querying BigQuery also needs `bigquery.jobs.create`.
- Secret Manager versions are immutable. Rotation creates a new version.
- Use `--out-file` for binary secrets.

Exam pattern: "Database credentials must rotate quarterly and never appear in code." Answer: Secret Manager with rotation, plus an identity for the app through WIF or impersonation.

### Instance metadata

- Restrict guest attributes with `compute.disableGuestAttributesAccess`.
- Require OS Login with `compute.requireOsLogin`. SSH keys then come from [[iam|IAM]].
- Disable serial ports with `compute.disableSerialPortAccess`.
- Disable legacy metadata server endpoints.
- Keep secrets out of metadata and startup scripts. Put them in Secret Manager.

## Encryption at rest

| Option | Who controls keys | Choose when |
|---|---|---|
| Google default encryption | Google | Default. Always on. AES-256. |
| CMEK with [[cloud-kms]] (software) | You, in Cloud KMS | You need control, rotation, or revocation |
| CMEK with Cloud KMS HSM | You, in hardware (FIPS 140-2 Level 3) | Compliance requires hardware keys |
| Cloud External Key Manager (EKM) | You, in an external key manager | Keys must stay outside Google |
| CSEK | You, sent with each request | Legacy or specific compliance cases. Rare. |
| Confidential Computing | Google and TEE hardware | Data must be protected in use |

See [[cryptography]] for the underlying concepts.

- CMEK is envelope encryption. Your key wraps the service's data keys. CMEK adds control, not baseline strength. It also adds KMS cost.
- CSEK works only with Cloud Storage and Compute Engine. The AES-256 key is wrapped with RSA-OAEP. Pass it with `--csek-key-file`.
- A disk shows `kmsKeyName` for CMEK and `sha256` for CSEK.
- Asymmetric keys: callers get `getPublicKey` and `asymmetricDecrypt`. Encryption happens on the client.
- EKM: Google never stores or caches the external keys. If the external manager is unreachable, data access fails. [[vpc|VPC]] endpoints keep traffic private. Key Access Justifications limit the partner to allowed justification codes.
- Some services do not support CMEK. Use `gcp.restrictNonCmekServices` to require CMEK where it works.

### Key management

- Hierarchy: key ring (regional), then key (with a purpose), then key version.
- Key version states: PENDING_GENERATION, ENABLED, DISABLED, DESTROY_SCHEDULED, DESTROYED.
- Each key has exactly one primary version.
- Rotation does not start automatically. Set `--rotation-period` and `--next-rotation-time`.
- Rotation creates new versions. Old versions still decrypt existing data. Rotation does not re-encrypt data by default.
- Disable a key version to block decryption at once.
- Destroy is scheduled. The minimum wait is 24 hours. A destroyed version cannot be recovered.
- Import jobs wrap keys with RSA-OAEP. Import keys must be marked import-only. Imported versions cannot be backed up or exported.
- Audit key use with Data Access logs on Cloud KMS. The `cryptoKeyVersions.decrypt` events show who decrypted what.

## Encryption in transit

- Google encrypts traffic between its data centers by default. TLS ends at the Google Front End.
- VM-to-VM traffic is always encrypted, unless both VMs have external IPs.
- Use SSL policies on load balancers.
- Use VPC Service Controls to keep API traffic on Google's network.
- HA VPN encrypts with IPsec. Dedicated Interconnect can use MACsec.
- Other options: IPsec tunnels, managed SSL certificates, S/MIME, and Istio.

Exam pattern: "Encrypt all traffic between on-premises and the VPC." Answer: HA VPN (IPsec) or MACsec on Dedicated Interconnect.

## Cloud Storage lifecycle and retention

- Lifecycle has three actions: Delete, SetStorageClass, and AbortIncompleteMultipartUpload.
- If two rules conflict, Delete wins over SetStorageClass.
- Changes take up to 24 hours.
- Use `--lifecycle-file` with `buckets update` only.
- Retention policies block deletion until the retention period ends.
- Bucket lock makes the retention policy permanent. You cannot remove a locked policy before it expires.

## Confidential Computing

- Confidential VMs use AMD SEV, SEV-SNP, or Intel TDX. Memory is encrypted. Host and Google staff cannot read it.
- Confidential GKE nodes, Confidential Space, [[dataflow|Dataflow]], and Dataproc use the same family.
- SEV VMs on N2D support live migration.
- Exam wording: "No one, including Google, can inspect memory" or "Multiple parties collaborate without sharing raw data."

## Securing AI workloads (objective 3.3)

### Three layers

Scenarios name one layer. Pick the control for that layer.

| Layer | Controls |
|---|---|
| Data | Sensitive Data Protection on training data. CMEK on data and model artifacts. VPC Service Controls around data projects. IAM least privilege on datasets. |
| Model | Scanning and signed images in [[artifact-registry]]. [[binary-authorization]] for model serving. Per-endpoint IAM. Vertex AI Model Monitoring. |
| Interaction | Model Armor on endpoints screens prompts and responses. |

- The Secure AI Framework (SAIF) is Google's blueprint for AI security.
- SCC gives AI asset discovery and the Recommended AI Controls framework through Audit Manager.

### IaaS or PaaS training

| Model | Who secures what | Controls to set |
|---|---|---|
| IaaS ([[compute-engine]] or [[gke]] with GPUs or TPUs) | You secure the whole stack. | Hardened images, VM Manager patching, CMEK, private networking, Confidential VMs or nodes for sensitive data, and secure CI/CD |
| PaaS ([[vertex-ai]]) | Google secures the infrastructure. | IAM per ML role, data access, CMEK, VPC Service Controls, PSC endpoints, and Model Armor |

### Gemini Enterprise Agent Platform

- Model Armor applies runtime guardrails to Gemini models and to third-party or open models on the platform. It screens prompt injection, jailbreaks, PII, unsafe content, and malicious URLs.
- Prompts and responses are not used to train Google models. You control logging and retention.
- Agents are identities. Give them least-privilege IAM.

### Vertex AI specifics

- Use separate VPC Service Controls perimeters for training data projects and for serving endpoints.
- A public endpoint can sit behind a VPC Service Controls access level. A fully private endpoint is the alternative.
- PSC endpoints give private access from your VPC, including multicloud access.
- Custom route exports advertise your custom routes to the Google service network. Managed Vertex AI components can then reach back into your network.

Exam patterns:

| Scenario | Answer |
|---|---|
| Prevent sensitive data leaking through prompts or responses. | Model Armor |
| Discover unsanctioned AI usage. | SCC AI inventory |
| Protect training data in use. | Confidential Computing |

!!! tip "Exam tips"
    - Match the key option to the requirement: default, CMEK, HSM, EKM, CSEK, or Confidential Computing.
    - Destroy is scheduled and irreversible. Disable is immediate and reversible.
    - Rotation does not re-encrypt old data.
    - Locked bucket retention policies cannot be removed early.
    - FPE needs the right key location. Check the key ring region.
    - Know which option is HA VPN (IPsec) and which is Interconnect (MACsec, not default).
    - For objective 3.3, learn the three layers and the IaaS and PaaS split.

Labs: [[security-labs]].

[Next: Managing operations](04-managing-operations.md)
