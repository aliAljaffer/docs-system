---
title: Cloud-kms
category: GCP
description: 'GCP note: Cloud-kms.'
tags:
- gcp
- security
---


# Cloud-kms

`gcp` `security`

## Cloud KMS (Key Management Service)
**AWS Equivalent:** AWS KMS

**Managed cryptographic key management** - Create, use, rotate, and destroy cryptographic keys

### Overview
- **Centralized key management** for cloud services and applications
- **HSM-backed keys** for hardware security
- **Automated rotation** with version control
- **Fine-grained IAM control** per key
- **Audit logging** for all key operations
- **Global availability** with regional key storage

### Key Concepts
| Term | Meaning | Rule |
|------|---------|------|
| Key Ring | Logical grouping of keys in a specific location, used for organization (prod-keys, dev-keys) | **Cannot be deleted** (can delete keys inside). Location is permanent (cannot change after creation) |
| Key (CryptoKey) | Named encryption key with one or more key versions. Defines purpose (encryption, signing, MAC) and rotation schedule | **Cannot be deleted, only disabled** |
| Key Version | Actual cryptographic material. Each rotation creates a new version. Primary version used for new operations | Can have multiple versions (for decryption of old data). Can be destroyed (after 24-hour grace period) |

### Key Purposes
| Purpose | API value | Use for |
|---------|-----------|---------|
| Encryption/Decryption | `ENCRYPT_DECRYPT` | Symmetric encryption (AES-256). Most common use case. Encrypt data at application level |
| Digital Signatures | `ASYMMETRIC_SIGN` | Sign and verify data (RSA, ECDSA). Code signing, document signing |
| Message Authentication | `MAC` | Generate and verify MACs (HMAC). Data integrity verification |
| Asymmetric Encryption | `ASYMMETRIC_DECRYPT` | Public/private key encryption. Encrypt with public key, decrypt with private key |

### Protection Levels
| Level | Key storage | Notes |
|-------|-------------|-------|
| Software | Keys protected by software | **Default and most common**. Lower cost. FIPS 140-2 Level 1 validated |
| Hardware (HSM) | Keys stored in Cloud HSM (Hardware Security Module). Private keys never leave HSM | **FIPS 140-2 Level 3 validated**. Higher cost (10x more than software). Required for compliance (PCI-DSS, HIPAA strict requirements) |
| External | Keys stored in external key management partner (Thales, Fortanix, etc.) | Bring Your Own Key (BYOK). Hybrid cloud scenarios |
| External VPC | Keys managed externally but within your VPC | More control over key access paths. Data sovereignty requirements |

### Key Algorithms
| Type | Algorithms |
|------|------------|
| Symmetric encryption | AES-256-GCM (default), AES-128-GCM, AES-256-CBC, AES-128-CBC |
| Asymmetric signing | RSA (2048, 3072, 4096 bits), ECDSA (P256, P384) |
| Asymmetric encryption | RSA (2048, 3072, 4096 bits) |
| MAC | HMAC-SHA256 |

### Key Rotation
| Aspect | Automatic | Manual |
|--------|-----------|--------|
| Schedule | Configurable (30, 90, 365 days) | On demand |
| New version | Created automatically and becomes primary | Created by you, then set as primary manually |
| Old versions | **Retained for decryption** | - |
| Key type | Only symmetric encryption keys | Asymmetric keys (no auto-rotation) |

**Best Practices:**
- Enable automatic rotation for symmetric keys
- 90-day rotation for sensitive data
- Keep old versions for data encrypted with them
- Test rotation process before production

### Envelope Encryption
**How Cloud KMS Works:**
1. **Data Encryption Key (DEK)**: Encrypts your data
2. **Key Encryption Key (KEK)**: Encrypts the DEK
3. KEK is managed by Cloud KMS

**Benefits:**
- Decrypt only metadata (DEK), not entire dataset
- Faster encryption/decryption (local DEK usage)
- Reduce Cloud KMS API calls
- Better performance for large datasets

**Example Flow:**
```text
1. Generate DEK locally (AES-256)
2. Encrypt data with DEK
3. Send DEK to KMS for encryption (wrap)
4. Store encrypted DEK with encrypted data
5. To decrypt: Send encrypted DEK to KMS (unwrap)
6. Use decrypted DEK to decrypt data
```

### Integration with GCP Services
**Automatic Encryption at Rest:**
- [[gcp/cloud-storage|Cloud Storage]]: CMEK (Customer-Managed Encryption Keys)
- [[gcp/compute-engine|Compute Engine]]: Encrypted persistent disks
- [[gcp/cloud-sql|Cloud SQL]]: Encrypted database instances
- [[bigquery|BigQuery]]: Encrypted datasets and tables
- [[gcp/gke|GKE]]: Encrypted secrets and persistent volumes

**No additional code required - managed by GCP**

### CMEK (Customer-Managed Encryption Keys)
**AWS Equivalent:** Customer Managed Keys in KMS

- You control the key lifecycle
- You control access via IAM
- Audit all key usage
- **Encryption/decryption still performed by Google**
- Use cases: Compliance, data sovereignty, separation of duties

**CMEK vs Google-Managed Keys:**
| Feature | CMEK | Google-Managed |
|---------|------|----------------|
| Key management | You manage | Google manages |
| Rotation control | You control | Automatic |
| Access control | Your IAM policies | Google controls |
| Audit logging | Yes, detailed | Limited |
| Cost | Additional cost | Included |
| Compliance | Better for regulated industries | Standard |

### CSEK (Customer-Supplied Encryption Keys)
**You manage keys completely outside GCP**
- Provide key with each API request
- GCP never stores your key
- **Not integrated with Cloud KMS**
- Higher management overhead
- Use case: Strictest data sovereignty requirements

**CSEK Workflow:**
```bash
# Compute Engine disk encryption with CSEK
gcloud compute disks create encrypted-disk \
  --csek-key-file=key.json

# Must provide key for ALL operations
gcloud compute instances create vm \
  --disk=name=encrypted-disk,csek-key-file=key.json
```

### IAM Roles for Cloud KMS
**Predefined Roles:**

| Role | Grants |
|------|--------|
| `roles/cloudkms.admin` | Full admin (create keys, set IAM) |
| `roles/cloudkms.cryptoKeyEncrypterDecrypter` | Encrypt and decrypt |
| `roles/cloudkms.cryptoKeyEncrypter` | Encrypt only |
| `roles/cloudkms.cryptoKeyDecrypter` | Decrypt only |
| `roles/cloudkms.signer` | Sign data |
| `roles/cloudkms.signerVerifier` | Sign and verify |
| `roles/cloudkms.viewer` | View keys (no crypto operations) |

**Best Practices:**
- Grant least privilege (encrypter vs encrypterDecrypter)
- Separate encryption and decryption permissions
- Use service accounts for application access
- Separate admin and usage permissions

### Key States
| State | Meaning |
|-------|---------|
| ENABLED | Active, can be used for crypto operations |
| DISABLED | Cannot be used, can be re-enabled |
| DESTROY_SCHEDULED | Scheduled for destruction (24-hour grace period) |
| DESTROYED | Permanently destroyed, **cannot be recovered** |

### Import External Keys
- Import existing keys into Cloud KMS
- Must use import job with protection level
- Wrapped with Google's public key
- **One-way import (cannot export)**
- Use case: Migrate from on-prem HSM

### Pricing
| Key type | Key version | Operations |
|----------|-------------|------------|
| Software | $0.06/month per active key version | $0.03 per 10,000 operations |
| HSM | $1/month per active key version | $0.03 per 10,000 operations |
| External | $2.50/month per key version | $0.03 per 10,000 operations |

Free tier: first 20,000 operations per month free (worldwide).

### Limitations
- 15,000 key versions per key
- 500 requests per second per key
- Key ring and key names cannot be reused (even after deletion)
- Cannot move keys between regions
- Cannot export private keys (by design)

### Cloud KMS vs AWS KMS Comparison
| Feature | Cloud KMS | AWS KMS |
|---------|-----------|---------|
| Key hierarchy | Key Ring > Key > Version | Single key with rotation |
| Automatic rotation | Yes (symmetric only) | Yes |
| HSM support | Cloud HSM (FIPS 140-2 L3) | CloudHSM (FIPS 140-2 L3) |
| External keys | Yes (External KMS) | Yes (Custom Key Store) |
| Asymmetric keys | Yes | Yes |
| Regional keys | Yes | Yes |
| Global keys | No (key ring region) | Multi-region keys |
| Import keys | Yes (one-way) | Yes (one-way) |
| Free tier | 20K ops/month | 20K ops/month |

---

## ACE Level

### Essential gcloud Commands
```bash
# Create key ring
gcloud kms keyrings create KEY_RING_NAME \
  --location=LOCATION

# List key rings
gcloud kms keyrings list --location=LOCATION

# Create symmetric encryption key
gcloud kms keys create KEY_NAME \
  --keyring=KEY_RING_NAME \
  --location=LOCATION \
  --purpose=encryption \
  --rotation-period=90d \
  --next-rotation-time=2026-03-01T00:00:00Z

# Create asymmetric signing key
gcloud kms keys create SIGN_KEY_NAME \
  --keyring=KEY_RING_NAME \
  --location=LOCATION \
  --purpose=asymmetric-signing \
  --default-algorithm=rsa-sign-pkcs1-4096-sha256

# Create HSM-protected key
gcloud kms keys create HSM_KEY_NAME \
  --keyring=KEY_RING_NAME \
  --location=LOCATION \
  --purpose=encryption \
  --protection-level=hsm

# List keys
gcloud kms keys list --keyring=KEY_RING_NAME --location=LOCATION

# Describe key
gcloud kms keys describe KEY_NAME \
  --keyring=KEY_RING_NAME \
  --location=LOCATION

# Encrypt data
gcloud kms encrypt \
  --key=KEY_NAME \
  --keyring=KEY_RING_NAME \
  --location=LOCATION \
  --plaintext-file=plaintext.txt \
  --ciphertext-file=ciphertext.enc

# Decrypt data
gcloud kms decrypt \
  --key=KEY_NAME \
  --keyring=KEY_RING_NAME \
  --location=LOCATION \
  --ciphertext-file=ciphertext.enc \
  --plaintext-file=decrypted.txt

# Disable key
gcloud kms keys update KEY_NAME \
  --keyring=KEY_RING_NAME \
  --location=LOCATION \
  --primary-version=VERSION_NUMBER \
  --disable-key

# Enable key
gcloud kms keys update KEY_NAME \
  --keyring=KEY_RING_NAME \
  --location=LOCATION \
  --enable-key

# Set primary version
gcloud kms keys set-primary-version KEY_NAME \
  --keyring=KEY_RING_NAME \
  --location=LOCATION \
  --version=VERSION_NUMBER

# Grant IAM permissions
gcloud kms keys add-iam-policy-binding KEY_NAME \
  --keyring=KEY_RING_NAME \
  --location=LOCATION \
  --member='serviceAccount:sa@project.iam.gserviceaccount.com' \
  --role='roles/cloudkms.cryptoKeyEncrypterDecrypter'

# View audit logs
gcloud logging read "resource.type=cloudkms_cryptokey"
```

### Key Concepts for ACE
- Understanding key rings, keys, and key versions
- Creating and managing encryption keys
- Encrypting and decrypting data with KMS
- Understanding key purposes (encrypt, sign, MAC)
- Configuring automatic key rotation
- Granting IAM permissions on keys
- Software vs HSM protection levels
- Using CMEK with Cloud Storage and Compute Engine
- Viewing key usage in audit logs
- Understanding envelope encryption concept

---

## PCA Level

### Architectural Patterns
#### Defense in Depth
```text
Layer 1: IAM (Who can access)
Layer 2: VPC Service Controls (Network perimeter)
Layer 3: Cloud KMS (Data encryption)
Layer 4: Application-level encryption
```

#### Multi-Region Key Strategy
- **Regional keys**: Lower latency, data residency
- **Multi-region approach**: Separate key rings per region
- Replicate encrypted data with region-specific keys
- Disaster recovery: Cross-region key backups (encrypted)

#### Separation of Duties
```text
Role separation:
- Security team: Create and manage keys (cloudkms.admin)
- Application team: Encrypt/decrypt (cloudkms.cryptoKeyEncrypterDecrypter)
- Audit team: View only (cloudkms.viewer)

Key separation:
- Production keys: Separate key ring, strict IAM
- Development keys: Separate key ring, relaxed IAM
- Different projects: Complete isolation
```

### CMEK Implementation Strategy
**Enabling CMEK for Cloud Storage:**
```bash
# Create bucket with CMEK
gsutil mb -l LOCATION -p PROJECT_ID gs://BUCKET_NAME

gsutil kms encryption -k \
  projects/PROJECT_ID/locations/LOCATION/keyRings/KEYRING/cryptoKeys/KEY \
  gs://BUCKET_NAME

# Upload object with CMEK
gsutil -o "GSUtil:encryption_key=projects/PROJECT_ID/locations/LOCATION/keyRings/KEYRING/cryptoKeys/KEY" \
  cp file.txt gs://BUCKET_NAME/
```

**CMEK for Compute Engine Disks:**
```bash
gcloud compute disks create DISK_NAME \
  --size=100GB \
  --kms-key=projects/PROJECT_ID/locations/LOCATION/keyRings/KEYRING/cryptoKeys/KEY
```

**CMEK for BigQuery:**
```bash
bq mk --dataset \
  --default_kms_key=projects/PROJECT_ID/locations/LOCATION/keyRings/KEYRING/cryptoKeys/KEY \
  PROJECT_ID:DATASET_NAME
```

**CMEK for GKE:**
```bash
# Create GKE cluster with CMEK for application-layer secrets
gcloud container clusters create CLUSTER_NAME \
  --database-encryption-key=projects/PROJECT_ID/locations/LOCATION/keyRings/KEYRING/cryptoKeys/KEY
```

### Key Lifecycle Management
**Key Creation:**
1. Define purpose and algorithm
2. Choose protection level (software vs HSM)
3. Set rotation schedule
4. Configure IAM permissions
5. Document key usage and owners

**Key Rotation:**
1. Automatic: Set rotation-period and next-rotation-time
2. Manual: Create new version, set as primary
3. Test with new version before promoting
4. **Keep old versions for at least data retention period**

**Key Retirement:**
1. Disable key (cannot encrypt new data)
2. Monitor for decrypt operations (old data access)
3. After retention period: Destroy key versions
4. **24-hour grace period before permanent destruction**

**Key Recovery:**
- Destroyed keys cannot be recovered
- Plan for accidental deletion: Use VPC Service Controls to prevent
- Keep encrypted backups with different keys

### High Availability Design
**Key Availability:**
- Cloud KMS SLA: 99.95% (global)
- Regional keys: Lower latency, data residency
- **No multi-region keys (unlike AWS)**
- Dual-region strategy: Replicate data with keys in each region

**Application Resilience:**
```python
# Retry logic for KMS operations
from google.api_core import retry

@retry.Retry(predicate=retry.if_exception_type(
    google.api_core.exceptions.ServiceUnavailable
))
def encrypt_data(plaintext):
    # KMS encrypt operation
    pass
```

**Caching Strategy:**
- Cache DEKs locally (envelope encryption)
- Reduce KMS API calls
- Set TTL on cached keys (e.g., 5 minutes)
- Refresh on rotation

### Security Best Practices
**Access Control:**
- Principle of least privilege (encrypt-only vs decrypt-only)
- Separate service accounts per application
- Use workload identity for GKE applications
- Conditions for time-based or IP-based access

**Audit & Monitoring:**
```bash
# Monitor key usage
gcloud logging read "resource.type=cloudkms_cryptokey \
  AND protoPayload.methodName=Encrypt \
  AND protoPayload.authenticationInfo.principalEmail=sa@project.iam.gserviceaccount.com"

# Alert on unusual key access
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="Unusual KMS Access" \
  --condition-display-name="High Decrypt Rate" \
  --condition-threshold-value=1000 \
  --condition-threshold-duration=60s
```

**Prevent Data Exfiltration:**
- Use [[vpc-service-controls|VPC Service Controls]] around KMS
- Prevent keys from being used outside perimeter
- **Block copy operations across perimeter boundaries**

### Compliance & Regulatory Requirements
**FIPS 140-2:**
- Software keys: Level 1
- HSM keys: Level 3
- Required for government, financial services

**Data Residency:**
- Choose regional key rings in compliant regions
- EU data: `europe-west1`, `europe-west4`
- US data: `us-central1`, `us-east1`
- Cannot move keys between regions

**Key Ownership:**
- CMEK: Google operates, you control
- External KMS: You own and operate
- Hybrid approach for multi-cloud

### External Key Manager Integration
**Supported Partners:**
- Thales CipherTrust
- Fortanix
- Ionic Security

**Architecture:**
```text
Application -> Cloud KMS API -> EKM Endpoint -> External Key Manager
                                 (In your VPC)
```

**Use Cases:**
- Compliance requiring external key control
- Hybrid cloud with existing key infrastructure
- Separation of duties (different vendors)

### Cost Optimization
**Reduce Operation Costs:**
- Use envelope encryption (fewer KMS API calls)
- Cache DEKs with appropriate TTL
- Batch operations when possible
- Use software keys unless HSM required

**Key Version Management:**
- Destroy old key versions after retention period
- Each active version incurs monthly cost
- Monitor unused keys and disable

**Free Tier Utilization:**
- First 20K operations free per month
- Distribute workloads across projects for multiple free tiers (anti-pattern for compliance)

### Disaster Recovery Strategy
**Backup Encrypted Data:**
```bash
# Backup with same key
gsutil -m cp -r gs://prod-bucket gs://backup-bucket

# Backup with different key (re-encrypt)
gsutil rewrite -k gs://backup-bucket/object
```

**Key Recovery Plan:**
- Document all keys and their purposes
- Export public keys for asymmetric keys
- **Cannot export private keys (by design)**
- Plan for key recreation process

**Multi-Region DR:**
- Separate key rings in DR region
- Replicate encrypted data
- Test failover with DR keys
- Document key dependencies

### Advanced Use Cases
**Application-Level Encryption:**
```python
from google.cloud import kms
import base64

def encrypt_data(project_id, location, keyring, key, plaintext):
    client = kms.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location, keyring, key)

    plaintext_bytes = plaintext.encode('utf-8')
    response = client.encrypt(
        request={'name': key_name, 'plaintext': plaintext_bytes}
    )

    return base64.b64encode(response.ciphertext).decode('utf-8')
```

**Digital Signatures:**
```bash
# Sign a file
gcloud kms asymmetric-sign \
  --key=SIGNING_KEY \
  --keyring=KEY_RING \
  --location=LOCATION \
  --version=1 \
  --input-file=document.txt \
  --signature-file=signature.sig \
  --digest-algorithm=sha256

# Verify signature
gcloud kms asymmetric-verify \
  --key=SIGNING_KEY \
  --keyring=KEY_RING \
  --location=LOCATION \
  --version=1 \
  --input-file=document.txt \
  --signature-file=signature.sig \
  --digest-algorithm=sha256
```

**Envelope Encryption Pattern:**
```python
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from google.cloud import kms

# 1. Generate local DEK
dek = os.urandom(32)  # 256-bit AES key

# 2. Encrypt data with DEK
cipher = Cipher(algorithms.AES(dek), modes.GCM(iv), backend=default_backend())
# ... encrypt data ...

# 3. Encrypt DEK with KMS
kms_client = kms.KeyManagementServiceClient()
encrypted_dek = kms_client.encrypt(
    request={'name': key_name, 'plaintext': dek}
).ciphertext

# 4. Store encrypted_dek with encrypted data
```

### Migration from AWS KMS
**Mapping:**

| AWS KMS | Cloud KMS |
|---------|-----------|
| AWS KMS CMK | Cloud KMS CryptoKey |
| AWS KMS Alias | Key names (no aliases in GCP) |
| AWS KMS Grant | IAM roles on keys |
| AWS CloudHSM | Cloud HSM protection level |
| AWS Secrets Manager | [[gcp/secret-manager|Secret Manager]] (not KMS) |

**Migration Steps:**
1. Inventory AWS KMS keys and usage
2. Create equivalent key rings in Cloud KMS
3. Create keys with matching algorithms
4. Implement dual encryption during migration
5. Decrypt with AWS KMS, re-encrypt with Cloud KMS
6. Update applications to use Cloud KMS
7. Verify and decommission AWS KMS keys

### Well-Architected Considerations
- **Operational Excellence**: Automated key rotation, infrastructure as code (Terraform), documented key lifecycle
- **Reliability**: Regional key strategy, envelope encryption for performance, retry logic for API failures
- **Security**: CMEK for sensitive data, HSM for compliance, least privilege IAM, VPC SC for data exfiltration prevention
- **Performance**: Envelope encryption to reduce API calls, local DEK caching, appropriate TTLs
- **Cost**: Software keys by default, destroy old versions, optimize API calls, use free tier
