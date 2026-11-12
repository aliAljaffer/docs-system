---
title: Binary-authorization
category: GCP
description: 'GCP note: Binary-authorization.'
tags:
- gcp
- security
---


# Binary-authorization

`gcp` `security`

## Binary Authorization
**AWS Equivalent:** AWS Signer + ECR Image Scanning (partial equivalence)

**Deploy-time security control** - Ensures only trusted container images are deployed to GKE and Cloud Run

### Overview
- **Enforcement point** at deployment time
- **Attestation-based** verification
- **Policy-driven** allow/deny decisions
- **Integration** with CI/CD pipelines
- **Cryptographic signatures** for image verification
- **Prevents deployment of unauthorized or vulnerable containers**

### How It Works
```text
1. Build container image
2. Scan for vulnerabilities (Container Analysis)
3. Sign image if scan passes (create attestation)
4. Deploy to GKE/Cloud Run
5. Binary Authorization checks policy
6. If attestation present and valid -> Allow deployment
7. If not -> Deny deployment
```

### Core Concepts
#### Attestation
- **Cryptographic signature** on a container image
- Confirms that image passed certain checks
- Created by **attestors** (trusted parties)
- Stored in Container Analysis
- Multiple attestations per image (build, scan, QA approval)

#### Attestor
- **Entity that vouches for an image**
- Backed by cryptographic keys (PGP or PKIX)
- Examples: CI/CD system, security scanner, manual approver
- Can have multiple attestors per policy

#### Policy
- **Rules for deployment**
- Requires attestations from specific attestors
- Can have exceptions (allowlist/denylist)
- Project-level enforcement
- Dry run mode for testing

#### Note
- Metadata about container image
- Created by Container Analysis API
- Includes: Vulnerabilities, attestations, build info
- Referenced by Binary Authorization

### Attestor Types
#### PKIX (Public Key Infrastructure)
- Uses X.509 certificates
- **Recommended for production**
- Easier key rotation
- Better integration with enterprise PKI

#### PGP (Pretty Good Privacy)
- Uses PGP keys
- Simpler setup
- Legacy option

### Policy Structure
**Default Rule:**
- Applies to all images
- Most restrictive

**Cluster-Specific Rules:**
- Override default for specific GKE clusters
- More permissive for dev clusters

**Image Allowlist:**
- Bypass policy for specific images
- Example: Google-provided system images

**Policy Modes:**
- **Enforcement**: Block non-compliant deployments (production)
- **Dry Run**: Log violations, allow deployment (testing)

### Example Policy
```yaml
defaultAdmissionRule:
  evaluationMode: REQUIRE_ATTESTATION
  enforcementMode: ENFORCED_BLOCK_AND_AUDIT_LOG
  requireAttestationsBy:
    - projects/PROJECT_ID/attestors/build-attestor
    - projects/PROJECT_ID/attestors/vulnerability-attestor

clusterAdmissionRules:
  us-central1-a.dev-cluster:
    evaluationMode: ALWAYS_ALLOW
    enforcementMode: ENFORCED_BLOCK_AND_AUDIT_LOG

admissionWhitelistPatterns:
  - namePattern: "gcr.io/google-containers/*"  # GKE system images
  - namePattern: "gcr.io/cloudsql-docker/*"   # Cloud SQL proxy
```

### Integration with CI/CD
**Typical Pipeline:**
```text
1. Code commit
2. Cloud Build: Build container image
3. Cloud Build: Push to Artifact Registry
4. Container Analysis: Vulnerability scan (automatic)
5. Cloud Build: Check scan results
6. If vulnerabilities > threshold: FAIL
7. If scan passes: Create attestation
8. Deploy to GKE/Cloud Run
9. Binary Authorization: Verify attestation
10. Deployment allowed/denied
```

### Creating Attestations
#### Manual Attestation
```bash
# Create attestation
gcloud beta container binauthz attestations create \
  --artifact-url="ARTIFACT_URL" \
  --attestor="projects/PROJECT_ID/attestors/ATTESTOR_NAME" \
  --signature-file=signature.pgp \
  --public-key-id=PGP_KEY_ID
```

#### Automated Attestation (Cloud Build)
```yaml
# cloudbuild.yaml
steps:
  # Build image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/app:$SHORT_SHA', '.']

  # Push image
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/app:$SHORT_SHA']

  # Wait for vulnerability scan
  - name: 'gcr.io/$PROJECT_ID/check-vulnerabilities'
    args: ['gcr.io/$PROJECT_ID/app:$SHORT_SHA']

  # Create attestation if scan passes
  - name: 'gcr.io/$PROJECT_ID/create-attestation'
    args:
      - '--artifact-url=gcr.io/$PROJECT_ID/app:$SHORT_SHA'
      - '--attestor=projects/$PROJECT_ID/attestors/vulnz-attestor'
      - '--keyversion=projects/$PROJECT_ID/locations/global/keyRings/binauthz/cryptoKeys/attestor-key/cryptoKeyVersions/1'
```

### Vulnerability-Based Attestation
**Container Analysis Integration:**
- Automatic vulnerability scanning
- CVE detection (Low, Medium, High, Critical)
- Policy based on severity threshold

**Example Policy:**
```text
Deny deployment if:
- Critical vulnerabilities > 0
- High vulnerabilities > 5
- Medium vulnerabilities > 20

Create attestation only if thresholds met
```

**Implementation:**
```python
# Check vulnerabilities before attestation
from google.cloud import containeranalysis_v1

client = containeranalysis_v1.ContainerAnalysisClient()
resource_url = f"https://{image_url}"

# Get vulnerability occurrences
occurrences = client.list_occurrences(
    parent=f"projects/{project_id}",
    filter=f'resourceUrl="{resource_url}" AND kind="VULNERABILITY"'
)

critical = sum(1 for o in occurrences if o.vulnerability.severity == 'CRITICAL')
high = sum(1 for o in occurrences if o.vulnerability.severity == 'HIGH')

if critical > 0 or high > 5:
    raise Exception("Too many vulnerabilities, blocking attestation")

# Create attestation (scan passed)
create_attestation(image_url)
```

### Deploying with Binary Authorization
#### GKE
```bash
# Enable Binary Authorization on cluster
gcloud container clusters update CLUSTER_NAME \
  --enable-binauthz \
  --zone=ZONE

# Deploy (will be checked by Binary Authorization)
kubectl apply -f deployment.yaml
```

**If deployment denied:**
```text
Error from server: admission webhook "imagepolicywebhook.image-policy.k8s.io" denied the request:
Image gcr.io/project/app:latest denied by Binary Authorization
```

#### Cloud Run
```bash
# Enable Binary Authorization on service
gcloud run services update SERVICE_NAME \
  --binary-authorization=default \
  --region=REGION

# Deploy (will be checked)
gcloud run deploy SERVICE_NAME \
  --image=gcr.io/PROJECT/app:latest
```

### Policy Evaluation Modes
**ALWAYS_ALLOW**
- Allow all images (no attestation required)
- Use for dev/test environments

**ALWAYS_DENY**
- Deny all images (rarely used)
- Use for temporarily blocking all deployments

**REQUIRE_ATTESTATION**
- Require attestations from specified attestors
- **Production mode**

**ALLOW_UNATTESTED_IMAGES** (deprecated)
- Legacy mode, don't use

### Enforcement Modes
**ENFORCED_BLOCK_AND_AUDIT_LOG**
- **Block deployment if policy violated**
- Log violation to Cloud Logging
- Recommended for production

**DRYRUN_AUDIT_LOG_ONLY**
- Allow deployment even if policy violated
- Log violation (for testing)
- Use during policy development

### Exemptions and Allowlists
**Image Allowlist Patterns:**
```yaml
admissionWhitelistPatterns:
  # Allow all GKE system images
  - namePattern: "gcr.io/google-containers/*"

  # Allow specific registry
  - namePattern: "gcr.io/my-project/trusted-images/*"

  # Allow specific image
  - namePattern: "gcr.io/my-project/legacy-app:v1.2.3"
```

**Use Cases:**
- System containers (GKE add-ons)
- Trusted base images
- Emergency hotfixes
- Legacy images being phased out

### Multi-Attestor Policies
**Require multiple attestations:**
```yaml
# Require BOTH build attestation AND security review
defaultAdmissionRule:
  evaluationMode: REQUIRE_ATTESTATION
  requireAttestationsBy:
    - projects/PROJECT/attestors/build-attestor
    - projects/PROJECT/attestors/security-attestor
```

**Use Cases:**
- Separation of duties
- Build + vulnerability scan + QA approval
- Compliance requirements (4-eyes principle)

### Break-Glass Procedure
**Emergency deployments:**
```bash
# Temporarily disable Binary Authorization
gcloud container clusters update CLUSTER_NAME \
  --no-enable-binauthz \
  --zone=ZONE

# Deploy emergency fix
kubectl apply -f emergency-fix.yaml

# Re-enable Binary Authorization
gcloud container clusters update CLUSTER_NAME \
  --enable-binauthz \
  --zone=ZONE
```

**Better approach:**
```yaml
# Add temporary allowlist for emergency image
admissionWhitelistPatterns:
  - namePattern: "gcr.io/project/emergency-fix:hotfix-123"
```

### Audit Logging
**All policy decisions logged:**
- Allowed deployments
- Denied deployments
- Dry run violations
- Policy changes

```bash
# View Binary Authorization logs
gcloud logging read "resource.type=k8s_cluster \
  AND protoPayload.methodName=\"io.k8s.core.v1.pods.create\" \
  AND protoPayload.response.status.message:\"Binary Authorization\""
```

### Limitations
- Only for container workloads (GKE, Cloud Run)
- Does not verify image content (only signatures)
- Requires Container Registry/Artifact Registry for best integration
- Learning curve for attestation setup
- **Does not prevent attacks after deployment** (runtime protection needed)

### Binary Authorization vs AWS Signer
| Feature | Binary Authorization | AWS Signer |
|---------|---------------------|------------|
| Scope | GKE, Cloud Run | ECR, Lambda |
| Attestation | Multiple attestors | Single signature |
| Policy enforcement | Project-level | Service-specific |
| Dry run mode | Yes | No |
| CI/CD integration | Cloud Build native | CodePipeline integration |
| Vulnerability integration | Container Analysis | ECR scanning |
| Free tier | Yes | Pay per signature |

### Pricing
- **Binary Authorization is free**
- No charge for policy evaluation
- Underlying costs: Container Analysis (free tier available), Cloud KMS for key management

---

## ACE Level

### Essential gcloud Commands
```bash
# Enable Binary Authorization API
gcloud services enable binaryauthorization.googleapis.com

# Get current policy
gcloud container binauthz policy export

# Import policy from file
gcloud container binauthz policy import policy.yaml

# Create attestor
gcloud beta container binauthz attestors create ATTESTOR_NAME \
  --attestation-authority-note=NOTE_ID \
  --attestation-authority-note-project=PROJECT_ID

# List attestors
gcloud beta container binauthz attestors list

# Describe attestor
gcloud beta container binauthz attestors describe ATTESTOR_NAME

# Add public key to attestor (PGP)
gcloud beta container binauthz attestors public-keys add \
  --attestor=ATTESTOR_NAME \
  --pgp-public-key-file=pubkey.pgp

# Add public key to attestor (PKIX)
gcloud beta container binauthz attestors public-keys add \
  --attestor=ATTESTOR_NAME \
  --pkix-public-key-file=cert.pem \
  --pkix-public-key-algorithm=rsa-sign-pkcs1-4096-sha512

# Create attestation
gcloud beta container binauthz attestations create \
  --artifact-url="gcr.io/PROJECT/image@sha256:DIGEST" \
  --attestor="projects/PROJECT/attestors/ATTESTOR_NAME" \
  --signature-file=signature.pgp \
  --public-key-id=KEY_ID

# List attestations
gcloud beta container binauthz attestations list \
  --attestor="projects/PROJECT/attestors/ATTESTOR_NAME"

# Validate policy
gcloud beta container binauthz policy validate policy.yaml

# Enable Binary Authorization on GKE cluster
gcloud container clusters update CLUSTER_NAME \
  --enable-binauthz \
  --zone=ZONE

# Check if Binary Authorization is enabled
gcloud container clusters describe CLUSTER_NAME \
  --zone=ZONE \
  --format="value(binaryAuthorization.enabled)"
```

### Key Concepts for ACE
- Understanding attestation-based deployment control
- Creating and managing attestors
- Understanding policy structure (default rule, cluster rules)
- Enabling Binary Authorization on GKE clusters
- Creating basic policies (allow all, require attestation)
- Using dry run mode to test policies
- Understanding image allowlist patterns
- Viewing Binary Authorization logs in Cloud Logging
- Integrating with Cloud Build for attestation
- Basic vulnerability-based attestation

---

## PCA Level

### Architectural Patterns
#### Secure Software Supply Chain
```text
Architecture:
1. Source Code (Cloud Source Repositories)
2. Build (Cloud Build with provenance)
3. Scan (Container Analysis for vulnerabilities)
4. Sign (Create attestation)
5. Store (Artifact Registry)
6. Deploy (Binary Authorization enforcement)
7. Runtime (GKE Sandbox, Workload Identity)

Security Gates:
- Code review (GitHub/GitLab)
- Build attestation (Cloud Build)
- Vulnerability scan (< Critical, < 5 High)
- Security review attestation (manual)
- Binary Authorization enforcement
- Runtime protection (GKE Sandbox)
```

#### Multi-Environment Strategy
```text
Dev Environment:
- Policy: ALWAYS_ALLOW
- Fast iteration, no attestation required

Staging Environment:
- Policy: REQUIRE_ATTESTATION (build only)
- Test attestation workflow

Production Environment:
- Policy: REQUIRE_ATTESTATION (build + scan + security review)
- Strict enforcement
- Image allowlist for trusted base images
```

#### Separation of Duties
```text
Attestors:
1. build-attestor: Automated (Cloud Build)
2. vulnerability-attestor: Automated (scan threshold)
3. security-attestor: Manual (security team approval)
4. compliance-attestor: Manual (compliance team)

Production requires all 4 attestations
Staging requires 1 & 2
Dev requires none
```

### Advanced Policy Configuration
#### Time-Based Policies
```python
# Cloud Function to enforce time-based policies
def update_binauthz_policy(event, context):
    from google.cloud import binaryauthorization_v1beta1
    import datetime

    client = binaryauthorization_v1beta1.BinauthzManagementServiceV1Beta1Client()
    policy = client.get_policy(name="projects/PROJECT_ID/policy")

    # More permissive during maintenance window
    if is_maintenance_window():
        policy.default_admission_rule.evaluation_mode = \
            binaryauthorization_v1beta1.AdmissionRule.EvaluationMode.ALWAYS_ALLOW
    else:
        policy.default_admission_rule.evaluation_mode = \
            binaryauthorization_v1beta1.AdmissionRule.EvaluationMode.REQUIRE_ATTESTATION

    client.update_policy(policy=policy)

def is_maintenance_window():
    now = datetime.datetime.now()
    # Maintenance window: 2-4 AM UTC
    return 2 <= now.hour < 4
```

#### CVE-Based Attestation
```python
# Advanced vulnerability checking
def create_attestation_if_safe(image_url, project_id):
    from google.cloud import containeranalysis_v1
    from google.cloud import binaryauthorization_v1beta1

    # Get vulnerabilities
    client = containeranalysis_v1.ContainerAnalysisClient()
    resource_url = f"https://{image_url}"
    occurrences = client.list_occurrences(
        parent=f"projects/{project_id}",
        filter=f'resourceUrl="{resource_url}" AND kind="VULNERABILITY"'
    )

    # Count by severity
    vuln_counts = {
        'CRITICAL': 0,
        'HIGH': 0,
        'MEDIUM': 0,
        'LOW': 0
    }

    cves_found = []
    for occ in occurrences:
        severity = occ.vulnerability.severity
        vuln_counts[severity] += 1
        cves_found.append({
            'cve': occ.vulnerability.short_description,
            'severity': severity,
            'fixable': bool(occ.vulnerability.fix_available)
        })

    # Policy: Block if any critical, or >5 high, or >10 medium
    if vuln_counts['CRITICAL'] > 0:
        raise Exception(f"CRITICAL vulnerabilities found: {cves_found}")
    if vuln_counts['HIGH'] > 5:
        raise Exception(f"Too many HIGH vulnerabilities: {vuln_counts['HIGH']}")
    if vuln_counts['MEDIUM'] > 10:
        raise Exception(f"Too many MEDIUM vulnerabilities: {vuln_counts['MEDIUM']}")

    # Safe to create attestation
    create_attestation(image_url, project_id)
    print(f"Attestation created. Vulnerabilities: {vuln_counts}")
```

### Cloud Build Integration Patterns
#### Complete CI/CD with Attestation
```yaml
# cloudbuild.yaml - Full pipeline with attestation
steps:
  # 1. Run tests
  - name: 'gcr.io/cloud-builders/npm'
    args: ['test']

  # 2. Build container
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/app:$SHORT_SHA', '.']

  # 3. Push to Artifact Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/app:$SHORT_SHA']

  # 4. Wait for vulnerability scan (automatic)
  - name: 'gcr.io/cloud-builders/gcloud'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        # Wait up to 5 minutes for scan
        for i in {1..30}; do
          SCAN_STATUS=$(gcloud artifacts docker images describe \
            gcr.io/$PROJECT_ID/app:$SHORT_SHA \
            --format='value(image_summary.vulnerability_summary.scan_status)')
          if [ "$SCAN_STATUS" = "SCAN_STATUS_SUCCESS" ]; then
            echo "Scan complete"
            break
          fi
          echo "Waiting for scan... ($i/30)"
          sleep 10
        done

  # 5. Check vulnerabilities
  - name: 'gcr.io/$PROJECT_ID/vulnerability-checker'
    args: ['gcr.io/$PROJECT_ID/app:$SHORT_SHA']

  # 6. Create build attestation
  - name: 'gcr.io/$PROJECT_ID/create-attestation'
    env:
      - 'IMAGE_URL=gcr.io/$PROJECT_ID/app:$SHORT_SHA'
      - 'ATTESTOR_NAME=build-attestor'
      - 'KMS_KEY_NAME=projects/$PROJECT_ID/locations/global/keyRings/binauthz/cryptoKeys/build-key/cryptoKeyVersions/1'

  # 7. Deploy to GKE (Binary Authorization will verify)
  - name: 'gcr.io/cloud-builders/kubectl'
    args:
      - 'set'
      - 'image'
      - 'deployment/app'
      - 'app=gcr.io/$PROJECT_ID/app:$SHORT_SHA'
    env:
      - 'CLOUDSDK_COMPUTE_ZONE=us-central1-a'
      - 'CLOUDSDK_CONTAINER_CLUSTER=prod-cluster'

images:
  - 'gcr.io/$PROJECT_ID/app:$SHORT_SHA'

options:
  machineType: 'N1_HIGHCPU_8'
```

#### Attestation Creation Script
```python
# create-attestation.py
import base64
import json
from google.cloud import kms
from google.cloud import binaryauthorization_v1beta1

def create_attestation(image_url, attestor_name, kms_key_version):
    # Generate payload to sign
    payload = {
        "critical": {
            "identity": {
                "docker-reference": image_url
            },
            "image": {
                "docker-manifest-digest": get_image_digest(image_url)
            },
            "type": "Google cloud binauthz container signature"
        }
    }
    payload_json = json.dumps(payload)

    # Sign with Cloud KMS
    kms_client = kms.KeyManagementServiceClient()
    digest = hashlib.sha256(payload_json.encode()).digest()

    sign_response = kms_client.asymmetric_sign(
        request={
            "name": kms_key_version,
            "digest": {"sha256": digest}
        }
    )

    signature = base64.b64encode(sign_response.signature).decode()

    # Create attestation
    binauthz_client = binaryauthorization_v1beta1.BinauthzManagementServiceV1Beta1Client()

    attestation = {
        "serialized_payload": base64.b64encode(payload_json.encode()).decode(),
        "signatures": [
            {
                "public_key_id": get_kms_public_key_id(kms_key_version),
                "signature": signature
            }
        ]
    }

    binauthz_client.create_attestation(
        parent=f"projects/{project_id}/attestors/{attestor_name}",
        attestation=attestation
    )

    print(f"Attestation created for {image_url}")
```

### Compliance & Audit
#### SOC 2 Compliance
```text
Controls:
- CC6.6: Logical and physical access controls

Implementation:
1. Binary Authorization ensures only authorized images deployed
2. Attestation requires cryptographic signatures
3. Audit logs track all deployment attempts
4. Separation of duties (multiple attestors)
5. Break-glass procedure documented

Evidence:
- Binary Authorization policy export
- Audit logs (allowed/denied deployments)
- Attestor configuration
- CI/CD pipeline documentation
```

#### PCI-DSS Compliance
```text
Requirement 6.3.2: Review of custom code prior to release

Implementation:
1. security-attestor requires manual security review
2. Only security team can create security attestations
3. Production deployment blocked without attestation
4. Audit trail in Cloud Logging

Policy:
defaultAdmissionRule:
  requireAttestationsBy:
    - build-attestor (automated)
    - vulnerability-attestor (automated)
    - security-attestor (manual code review)
```

### Monitoring & Alerting
```bash
# Create log-based metric for denied deployments
gcloud logging metrics create binauthz-denials \
  --description="Binary Authorization denials" \
  --log-filter='resource.type="k8s_cluster"
    AND protoPayload.methodName="io.k8s.core.v1.pods.create"
    AND protoPayload.response.status.message:"Binary Authorization"
    AND protoPayload.response.code="403"'

# Alert on denials
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="Binary Authorization Denials" \
  --condition-threshold-value=1 \
  --condition-threshold-duration=60s \
  --condition-filter='resource.type="k8s_cluster"
    AND metric.type="logging.googleapis.com/user/binauthz-denials"'
```

### Integration with Security Command Center
```text
Binary Authorization findings in SCC:
- Images deployed without attestation (if dry run)
- Policy violations
- Unauthorized deployment attempts
- Attestor key rotation needed

Automated remediation:
- SCC finding -> Pub/Sub -> Cloud Function -> Update policy
```

### Disaster Recovery
**Attestor Key Backup:**
```bash
# Export public keys
gcloud beta container binauthz attestors public-keys export \
  --attestor=ATTESTOR_NAME \
  --output-file=pubkey-backup.pem

# Store in Secret Manager
gcloud secrets create binauthz-pubkey-backup \
  --data-file=pubkey-backup.pem

# Restore if needed
gcloud beta container binauthz attestors public-keys add \
  --attestor=ATTESTOR_NAME \
  --pkix-public-key-file=pubkey-backup.pem
```

**Policy Backup:**
```bash
# Export policy
gcloud container binauthz policy export > policy-backup.yaml

# Store in Cloud Storage
gsutil cp policy-backup.yaml gs://binauthz-backups/$(date +%Y%m%d)/

# Restore if needed
gcloud container binauthz policy import policy-backup.yaml
```

### Cost Optimization
- Binary Authorization itself is free
- Costs from: Container Analysis scanning, Cloud KMS for signatures
- Optimize Container Analysis: Use free tier (first 50 images/month)
- Optimize KMS: Use single key for multiple attestors
- Cache vulnerability scan results (avoid re-scanning same digest)

### Migration from AWS Signer
**Comparison:**
```text
AWS Signer Profile -> GCP Attestor
AWS ECR Image Signing -> Container Analysis + Attestation
AWS Lambda deployment config -> Binary Authorization policy
```

**Migration Steps:**
1. Enable Binary Authorization in GCP
2. Create attestors equivalent to AWS Signer profiles
3. Update CI/CD pipelines (CodePipeline -> Cloud Build)
4. Recreate signing logic (AWS Signer SDK -> Cloud KMS)
5. Update policies (AWS IAM -> Binary Authorization policy)
6. Test in dry run mode
7. Enforce on production clusters

### Well-Architected Considerations
- **Operational Excellence**: Automated attestation in CI/CD, policy as code (Terraform), dry run testing before enforcement
- **Reliability**: Multiple attestors for redundancy, break-glass procedures, policy backups, key rotation
- **Security**: Cryptographic signatures, separation of duties, audit logging, vulnerability-based attestation, runtime protection (GKE Sandbox)
- **Performance**: Minimal deployment latency (<100ms policy evaluation), cached attestations, parallel attestation creation
- **Cost**: Free service, optimize Container Analysis and KMS usage, use free tiers where possible
