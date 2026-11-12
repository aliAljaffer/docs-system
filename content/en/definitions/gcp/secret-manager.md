---
title: Secret-manager
category: GCP
description: 'GCP note: Secret-manager.'
tags:
- gcp
- security
---


# Secret-manager

`gcp` `security`

## Secret Manager
**AWS Equivalent:** AWS Secrets Manager

**Secure storage and management of sensitive data** - API keys, passwords, certificates, tokens

### Overview
- **Centralized secret storage** across GCP projects
- **Versioning** with automatic rotation support
- **Audit logging** for all access
- **IAM integration** for fine-grained access control
- **Encryption at rest** with Cloud KMS
- **Global availability** with regional replication options

### Core Concepts
#### Secret
- Container for secret versions
- Has a unique name within project
- Metadata: labels, replication policy, rotation config
- **Cannot store the secret data itself, only versions do**

#### Secret Version
- Actual secret data (payload)
- Immutable once created
- Max size: 64 KiB
- States: Enabled, Disabled, Destroyed
- Each version has a unique ID (numeric)

#### Secret Payload
- The actual sensitive data
- Base64 encoded
- Can be string or binary data
- Examples: Database password, API key, TLS certificate

### Secret States
**Version States:**
- **ENABLED**: Active, can be accessed
- **DISABLED**: Cannot be accessed, can be re-enabled
- **DESTROYED**: Permanently deleted, **cannot be recovered**

### Replication Policies
#### Automatic Replication (Default)
- Secret replicated to all GCP regions automatically
- **High availability**
- Global access with low latency
- Best for most use cases

#### User-Managed Replication
- Choose specific regions for secret storage
- **Data residency compliance** (GDPR, data sovereignty)
- Lower storage costs (fewer replicas)
- Must specify at least one region
- Can add Customer-Managed Encryption Keys (CMEK) per region

```bash
# Create secret with specific regions
gcloud secrets create SECRET_ID \
  --replication-policy="user-managed" \
  --locations="us-central1,europe-west1"
```

### Secret Versioning
- Each update creates a new version
- **Old versions retained by default**
- Can alias versions: "latest", "1", "2", etc.
- Rollback by accessing previous version
- Enable/disable specific versions

**Version Lifecycle:**
```text
Create (v1) -> Add (v2) -> Add (v3)
           -> latest = v3
           -> Can still access v1, v2
           -> Disable v2 (not accessible)
           -> Destroy v1 (permanent deletion)
```

### Rotation
#### Manual Rotation
```bash
# Add new version (rotates secret)
echo -n "new-secret-value" | gcloud secrets versions add SECRET_ID --data-file=-
```

#### Automatic Rotation
- Configure rotation schedule
- Requires Cloud Functions or Cloud Run to generate new secret
- **Secret Manager triggers rotation, doesn't generate new value**

**Rotation Flow:**
```text
1. Secret Manager: Time to rotate (based on schedule)
2. Pub/Sub: Publishes rotation event
3. Cloud Function: Generates new secret value
4. Cloud Function: Adds new version to Secret Manager
5. Application: Fetches latest version
```

**Example Rotation Config:**
```bash
# Set rotation schedule
gcloud secrets update SECRET_ID \
  --next-rotation-time="2026-03-01T00:00:00Z" \
  --rotation-period="30d" \
  --topics="projects/PROJECT_ID/topics/TOPIC_NAME"
```

### IAM Roles for Secret Manager
**Predefined Roles:**
- `roles/secretmanager.admin`: Full admin (create, delete, set IAM)
- `roles/secretmanager.secretAccessor`: Read secret values (most common for apps)
- `roles/secretmanager.secretVersionAdder`: Add new versions (rotation)
- `roles/secretmanager.secretVersionManager`: Manage version lifecycle (enable/disable/destroy)
- `roles/secretmanager.viewer`: View metadata only, **not secret values**

**Best Practice:**
- Grant `secretAccessor` to applications (read-only)
- Grant `secretVersionAdder` to rotation functions
- Limit `admin` to security team
- Use service accounts with least privilege

### Integration with GCP Services
#### Cloud Run
```bash
# Mount secret as environment variable
gcloud run deploy SERVICE \
  --update-secrets=ENV_VAR_NAME=SECRET_ID:latest

# Mount secret as volume
gcloud run deploy SERVICE \
  --update-secrets=/path/to/secret=SECRET_ID:latest
```

#### Cloud Functions
```python
# Access secret in code
from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()
name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
response = client.access_secret_version(request={"name": name})
secret_value = response.payload.data.decode("UTF-8")
```

#### GKE (Kubernetes)
```yaml
# Using Workload Identity and CSI Driver
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: app-secrets
spec:
  provider: gcp
  parameters:
    secrets: |
      - resourceName: "projects/PROJECT_ID/secrets/SECRET_ID/versions/latest"
        path: "db-password"
```

#### Cloud Build
```yaml
# Access secrets in build steps
steps:
  - name: 'gcr.io/cloud-builders/gcloud'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        gcloud secrets versions access latest --secret=SECRET_ID > /workspace/secret.txt
availableSecrets:
  secretManager:
    - versionName: projects/PROJECT_ID/secrets/SECRET_ID/versions/latest
      env: 'SECRET_ENV_VAR'
```

#### Compute Engine
```bash
# Startup script to fetch secret
gcloud compute instances create INSTANCE \
  --metadata=startup-script='#!/bin/bash
    SECRET=$(gcloud secrets versions access latest --secret=SECRET_ID)
    echo $SECRET > /etc/app/secret.txt'
```

### Encryption
**Default Encryption:**
- All secrets encrypted at rest with Google-managed keys
- Automatic, no configuration needed

**Customer-Managed Encryption Keys (CMEK):**
```bash
# Create secret with CMEK
gcloud secrets create SECRET_ID \
  --replication-policy="user-managed" \
  --locations="us-central1" \
  --kms-key-name="projects/PROJECT/locations/us-central1/keyRings/KEYRING/cryptoKeys/KEY"
```

### Audit Logging
**Available Logs:**
- **Admin Activity**: Secret creation, deletion, IAM changes (always on)
- **Data Access**: Read secret values (must enable)

```bash
# View who accessed a secret
gcloud logging read "resource.type=secretmanager.googleapis.com/Secret \
  AND protoPayload.methodName=AccessSecretVersion \
  AND resource.labels.secret_id=SECRET_ID"
```

### Secret Manager vs AWS Secrets Manager
| Feature | Secret Manager | AWS Secrets Manager |
|---------|----------------|---------------------|
| Versioning | Numeric versions | Automatic labels (AWSCURRENT) |
| Rotation | Manual + Pub/Sub trigger | Built-in rotation for RDS/others |
| Replication | Automatic or user-managed | Single region or multi-region |
| Max size | 64 KiB | 65,536 bytes (64 KiB) |
| Encryption | Google-managed or CMEK | AWS-managed or CMK |
| Pricing | Per secret + versions | Per secret + API calls |
| Binary secrets | Yes | Yes |
| Cross-region | Yes (automatic replication) | Multi-region secrets |

### Secret Manager vs Cloud KMS
**When to Use Secret Manager:**
- Store passwords, API keys, certificates
- Frequent rotation of credentials
- Application configuration secrets
- Integration with Cloud Run, GKE, Cloud Functions

**When to Use Cloud KMS:**
- Encryption key management
- Envelope encryption patterns
- Digital signatures
- High-volume crypto operations
- FIPS 140-2 Level 3 compliance (HSM)

### Pricing
- **Secret versions**: $0.06 per month per active version
- **Access operations**: $0.03 per 10,000 accesses
- **Replication**: Included (no additional cost for regions)
- **CMEK**: Additional Cloud KMS charges apply

**Free Tier:**
- First 6 secret versions free per month
- First 10,000 access operations free per month

**Cost Optimization:**
- Destroy old secret versions (keep only necessary)
- Use automatic replication unless data residency required
- Cache secrets in application (reduce API calls)
- Delete unused secrets

### Best Practices
#### Secret Naming
- Use descriptive names: `prod-db-password`, `stripe-api-key`
- Include environment: `prod-`, `dev-`, `staging-`
- Use labels for organization: `env:prod`, `team:platform`

#### Secret Rotation
- Rotate secrets regularly (30-90 days)
- Automate rotation for database credentials
- Test rotation process in dev/staging first
- Keep at least 2 versions during rotation (old + new)

#### Access Control
- Grant least privilege (`secretAccessor` not `admin`)
- Separate service accounts per application
- Use Workload Identity for GKE workloads
- Audit secret access regularly

#### Secret Lifecycle
- Create secrets in separate "secrets project"
- Cross-project access via IAM
- Destroy old versions after rotation
- Document secret owners and rotation schedules

---

## ACE Level

### Essential gcloud Commands
```bash
# Create a secret
gcloud secrets create SECRET_ID \
  --replication-policy="automatic"

# Add secret version (initial value)
echo -n "my-secret-value" | gcloud secrets versions add SECRET_ID --data-file=-

# Add secret from file
gcloud secrets versions add SECRET_ID --data-file=/path/to/secret.txt

# List secrets
gcloud secrets list

# Describe secret
gcloud secrets describe SECRET_ID

# List secret versions
gcloud secrets versions list SECRET_ID

# Access secret value
gcloud secrets versions access latest --secret=SECRET_ID

# Access specific version
gcloud secrets versions access 3 --secret=SECRET_ID

# Disable a version
gcloud secrets versions disable 2 --secret=SECRET_ID

# Enable a version
gcloud secrets versions enable 2 --secret=SECRET_ID

# Destroy a version (permanent)
gcloud secrets versions destroy 1 --secret=SECRET_ID

# Delete a secret (all versions)
gcloud secrets delete SECRET_ID

# Grant access to service account
gcloud secrets add-iam-policy-binding SECRET_ID \
  --member='serviceAccount:sa@project.iam.gserviceaccount.com' \
  --role='roles/secretmanager.secretAccessor'

# View IAM policy
gcloud secrets get-iam-policy SECRET_ID

# Update secret labels
gcloud secrets update SECRET_ID \
  --update-labels=env=prod,team=backend

# Create secret with user-managed replication
gcloud secrets create SECRET_ID \
  --replication-policy="user-managed" \
  --locations="us-central1,us-east1"
```

### Key Concepts for ACE
- Creating and managing secrets
- Adding and accessing secret versions
- Understanding automatic vs user-managed replication
- Granting IAM permissions to access secrets
- Integrating secrets with Cloud Run and Cloud Functions
- Viewing secret access in audit logs
- Understanding secret states (enabled, disabled, destroyed)
- Managing secret lifecycle (create, rotate, destroy)
- Using labels for secret organization
- Accessing secrets from Compute Engine and GKE

---

## PCA Level

### Architectural Patterns
#### Centralized Secrets Management
```text
Architecture:
- Shared "secrets" project
- Secrets created in central project
- Applications in separate projects access via IAM
- Separation of duties: Security team manages secrets

Benefits:
- Single source of truth
- Centralized rotation
- Easier audit and compliance
- Cost optimization (fewer duplicates)
```

#### Multi-Environment Strategy
```text
Option 1: Separate projects per environment
- dev-secrets project
- staging-secrets project
- prod-secrets project
- Complete isolation

Option 2: Same project, naming convention
- dev-db-password
- staging-db-password
- prod-db-password
- Simpler management, IAM for separation
```

#### Secret Rotation Architecture
```text
1. Cloud Scheduler triggers rotation (schedule)
2. Pub/Sub topic receives rotation event
3. Cloud Function generates new credential
4. Cloud Function updates secret version
5. Applications fetch latest version automatically
6. Optional: Notify on-call team (Cloud Monitoring alert)
```

### Database Credentials Management
**Pattern 1: Dual-Write Rotation**
```text
1. Generate new password
2. Create new DB user or update password
3. Add new secret version
4. Wait for applications to pick up new version (grace period)
5. Optionally disable old secret version
```

**Pattern 2: Cloud SQL IAM Authentication**
```bash
# Instead of passwords, use IAM
gcloud sql users create SERVICE_ACCOUNT_EMAIL \
  --instance=INSTANCE_NAME \
  --type=CLOUD_IAM_SERVICE_ACCOUNT

# Application authenticates with service account
# No password to rotate
```

**Pattern 3: Connection Pooling with Secret Refresh**
```python
# Application code
import time
from google.cloud import secretmanager

class SecretRefresher:
    def __init__(self, secret_id, refresh_interval=300):
        self.secret_id = secret_id
        self.refresh_interval = refresh_interval
        self.last_refresh = 0
        self.cached_secret = None

    def get_secret(self):
        now = time.time()
        if now - self.last_refresh > self.refresh_interval:
            client = secretmanager.SecretManagerServiceClient()
            name = f"projects/{project}/secrets/{self.secret_id}/versions/latest"
            response = client.access_secret_version(request={"name": name})
            self.cached_secret = response.payload.data.decode("UTF-8")
            self.last_refresh = now
        return self.cached_secret
```

### API Key Management
**Pattern: Scoped API Keys**
```text
1. Create separate secret per external service
   - stripe-api-key
   - sendgrid-api-key
   - github-token

2. Grant access per service account
   - payment-service: stripe-api-key only
   - email-service: sendgrid-api-key only

3. Rotate independently
   - Different schedules per key
   - Minimize blast radius
```

### Certificate Management
**TLS Certificates:**
```bash
# Store certificate and private key separately
gcloud secrets create tls-cert --data-file=cert.pem
gcloud secrets create tls-key --data-file=key.pem

# Or combined (PKCS12)
openssl pkcs12 -export -out cert.p12 -inkey key.pem -in cert.pem
gcloud secrets create tls-bundle --data-file=cert.p12
```

**Auto-Renewal with Let's Encrypt:**
```text
1. Cloud Scheduler: Trigger renewal (monthly)
2. Cloud Function: Run certbot/acme.sh
3. Cloud Function: Upload new cert to Secret Manager
4. Cloud Run/GKE: Auto-reload with new version
```

### High Availability Design
**Multi-Region Secrets:**
```bash
# User-managed replication for data residency
gcloud secrets create global-secret \
  --replication-policy="user-managed" \
  --locations="us-central1,europe-west1,asia-east1"

# Applications in each region access local replica
# Low latency, high availability
```

**Fallback Strategy:**
```python
# Application code with fallback
def get_secret_with_fallback(primary_secret_id, fallback_secret_id):
    try:
        return access_secret(primary_secret_id)
    except Exception as e:
        logger.warning(f"Primary secret failed: {e}, using fallback")
        return access_secret(fallback_secret_id)
```

### Security Controls
**VPC Service Controls Integration:**
```bash
# Prevent secret exfiltration
# Create perimeter around projects with sensitive secrets
# Block access from outside perimeter
# Even with valid IAM, cannot access from outside VPC SC perimeter
```

**IAM Conditions for Temporary Access:**
```bash
# Grant access only during business hours
gcloud secrets add-iam-policy-binding SECRET_ID \
  --member='user:contractor@external.com' \
  --role='roles/secretmanager.secretAccessor' \
  --condition='expression=request.time.getHours("America/New_York") >= 9 && request.time.getHours("America/New_York") < 17,title=business-hours'
```

**IP-Based Restrictions:**
```bash
# Grant access only from corporate VPN
gcloud secrets add-iam-policy-binding SECRET_ID \
  --member='user:employee@company.com' \
  --role='roles/secretmanager.secretAccessor' \
  --condition='expression=origin.ip in ["10.0.0.0/8"],title=vpn-only'
```

### Audit & Compliance
**Comprehensive Audit Logging:**
```bash
# Enable Data Access logs
gcloud projects get-iam-policy PROJECT_ID > policy.yaml

# Edit policy.yaml to add:
auditConfigs:
- auditLogConfigs:
  - logType: DATA_READ
  - logType: DATA_WRITE
  service: secretmanager.googleapis.com

gcloud projects set-iam-policy PROJECT_ID policy.yaml

# Query access logs
gcloud logging read "resource.type=secretmanager.googleapis.com/Secret \
  AND protoPayload.methodName=AccessSecretVersion" \
  --limit=50 \
  --format=json
```

**Access Review:**
```bash
# List who has access to secrets
for secret in $(gcloud secrets list --format="value(name)"); do
  echo "Secret: $secret"
  gcloud secrets get-iam-policy $secret
done
```

**Compliance Reports:**
- Export audit logs to BigQuery
- Create dashboard for secret access patterns
- Alert on unusual access (off-hours, high volume)
- Regular access certification (quarterly)

### Cost Optimization
**Version Management:**
```bash
# Destroy old versions after rotation
# Keep only last 2 versions

# List all versions
gcloud secrets versions list SECRET_ID --format="value(name)"

# Destroy old versions (keep latest 2)
gcloud secrets versions list SECRET_ID \
  --format="value(name)" \
  --sort-by="~createTime" \
  --limit=100 | tail -n +3 | while read version; do
    gcloud secrets versions destroy $version --secret=SECRET_ID
  done
```

**Caching Strategy:**
```python
# Cache secrets to reduce API calls
import functools
import time

@functools.lru_cache(maxsize=128)
def get_secret_cached(secret_id, ttl_hash=None):
    # ttl_hash is used to invalidate cache
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def get_ttl_hash(seconds=300):
    # Cache TTL of 5 minutes
    return round(time.time() / seconds)

# Usage
secret = get_secret_cached("my-secret", ttl_hash=get_ttl_hash())
```

### Migration from AWS Secrets Manager
**Comparison & Mapping:**
```text
AWS Secrets Manager -> GCP Secret Manager
Secret Name -> Secret ID
Version Stages (AWSCURRENT) -> Version number (latest)
Rotation Lambda -> Cloud Function + Pub/Sub
Resource Policy -> IAM policy
KMS Encryption -> CMEK (optional)
```

**Migration Steps:**
1. Export secrets from AWS (manually or via API)
2. Create secrets in GCP Secret Manager
3. Update applications to use GCP client libraries
4. Set up rotation in GCP (Cloud Functions)
5. Test in dev/staging environments
6. Migrate production with rollback plan
7. Decommission AWS Secrets Manager

**Example Migration Script:**
```python
import boto3
import json
from google.cloud import secretmanager

# AWS client
aws_client = boto3.client('secretsmanager', region_name='us-east-1')

# GCP client
gcp_client = secretmanager.SecretManagerServiceClient()
parent = f"projects/{project_id}"

# List AWS secrets
response = aws_client.list_secrets()

for aws_secret in response['SecretList']:
    secret_name = aws_secret['Name']

    # Get secret value from AWS
    secret_value = aws_client.get_secret_value(SecretId=secret_name)
    secret_string = secret_value['SecretString']

    # Create secret in GCP
    gcp_secret = gcp_client.create_secret(
        request={
            "parent": parent,
            "secret_id": secret_name,
            "secret": {"replication": {"automatic": {}}},
        }
    )

    # Add version
    gcp_client.add_secret_version(
        request={
            "parent": gcp_secret.name,
            "payload": {"data": secret_string.encode("UTF-8")},
        }
    )

    print(f"Migrated: {secret_name}")
```

### Integration Patterns
**GitOps with Cloud Build:**
```yaml
# cloudbuild.yaml
steps:
  # Deploy to Cloud Run with secrets
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'my-service'
      - '--image=gcr.io/PROJECT/image'
      - '--update-secrets=DB_PASSWORD=db-password:latest'
      - '--update-secrets=API_KEY=api-key:latest'
```

**Terraform Integration:**
```hcl
# Create secret
resource "google_secret_manager_secret" "db_password" {
  secret_id = "db-password"

  replication {
    automatic = true
  }
}

# Add version
resource "google_secret_manager_secret_version" "db_password_v1" {
  secret = google_secret_manager_secret.db_password.id
  secret_data = var.db_password  # From Terraform variables
}

# Grant access
resource "google_secret_manager_secret_iam_member" "app_access" {
  secret_id = google_secret_manager_secret.db_password.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.app.email}"
}
```

### Advanced Rotation Patterns
**Zero-Downtime Database Rotation:**
```python
# Cloud Function for rotation
def rotate_db_password(event, context):
    import random
    import string
    import mysql.connector

    # 1. Generate new password
    new_password = ''.join(random.choices(
        string.ascii_letters + string.digits, k=32
    ))

    # 2. Update database user
    db = mysql.connector.connect(
        host=DB_HOST,
        user="admin",
        password=ADMIN_PASSWORD
    )
    cursor = db.cursor()
    cursor.execute(f"ALTER USER 'app_user' IDENTIFIED BY '{new_password}'")
    db.commit()

    # 3. Add new secret version
    client = secretmanager.SecretManagerServiceClient()
    parent = client.secret_path(PROJECT_ID, "db-password")
    client.add_secret_version(
        request={
            "parent": parent,
            "payload": {"data": new_password.encode("UTF-8")},
        }
    )

    print("Password rotated successfully")
```

### Well-Architected Considerations
- **Operational Excellence**: Automated rotation, centralized secrets management, IaC for secret creation
- **Reliability**: Multi-region replication, version rollback capability, caching with TTL
- **Security**: Least privilege IAM, audit logging, VPC SC perimeters, no hardcoded secrets, regular rotation
- **Performance**: Cache secrets locally, use regional replicas, batch secret access
- **Cost**: Destroy old versions, cache to reduce API calls, automatic replication unless compliance requires otherwise
