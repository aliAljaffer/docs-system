---
title: Vpc-service-controls
category: GCP Security
description: ==IAM + VPC SC = Defense in Depth==
tags:
- gcp
- security
---

<!-- imported from ObsidianVault/studies/cloud-architecht/gcp/security/vpc-service-controls.md. Edit the source, then run sync.py. -->

# Vpc-service-controls

`gcp` `security`

## VPC Service Controls
**AWS Equivalent:** VPC Endpoints + SCPs (combined functionality)

**Security perimeter to prevent data exfiltration** - Context-aware access control for GCP services
### Overview
- **Prevents data exfiltration** even with compromised credentials
- **Service perimeter** around GCP resources
- **Context-aware access** based on IP, device, user identity
- **Protects against insider threats** and credential leaks
- **No network changes required** (works at API layer)
- **Defense in depth with IAM**

### Core Concepts
#### Service Perimeter
- Virtual security boundary around GCP resources
- Defines which services and resources are protected
- Controls data movement across perimeter boundary
- **Like a firewall for GCP APIs**

#### Access Levels
- Conditions that must be met for access
- IP ranges, device policy, user identity
- Reusable across multiple perimeters
- Can be combined with AND/OR logic

#### Access Zones
**Inside the Perimeter:**
- Resources can communicate freely
- APIs work normally
- Data can move between resources

**Outside the Perimeter:**
- Access denied by default
- Even with valid IAM permissions
- Requires VPC SC bridge or egress policy

### Service Perimeter Types
#### Perimeter Bridge
- Connect two separate perimeters
- Allow communication between perimeters
- Bidirectional data flow
- Use case: Shared services across environments

#### Dry Run Mode
- Test perimeter configuration without enforcement
- Logs violations but doesn't block
- **Essential for testing before production**
- Identify unintended access blocks

### Supported Services
**Fully Protected Services (60+):**
- Cloud Storage
- BigQuery
- Cloud SQL
- Cloud Bigtable
- Cloud KMS
- Secret Manager
- Compute Engine
- GKE
- Pub/Sub
- Cloud Run
- Artifact Registry

**Not all GCP services support VPC SC**
- Check documentation for latest list

### Access Levels
#### IP-Based Access
```yaml
# Example: Allow only from corporate network
- ipSubnetworks:
  - "203.0.113.0/24"
  - "198.51.100.0/24"
```

#### Device Policy
```yaml
# Example: Require managed devices
- devicePolicy:
    requireScreenlock: true
    requireAdminApproval: true
    osConstraints:
      - osType: DESKTOP_CHROME_OS
        minimumVersion: "10.0.0"
```

#### User Identity
```yaml
# Example: Allow specific users or groups
- members:
  - "user:admin@example.com"
  - "group:security-team@example.com"
```

#### Region-Based Access
```yaml
# Example: Allow only from specific regions
- regions:
  - "US"
  - "EU"
```

### Access Context Manager
- Central management for access levels
- Create reusable access level policies
- Combine conditions with AND/OR
- Version control for policies

```bash
# Create access level
gcloud access-context-manager levels create LEVEL_NAME \
  --policy=POLICY_ID \
  --basic-level-spec=CONDITIONS_FILE.yaml
```

### Ingress and Egress Rules
#### Ingress Policy
- Control requests coming INTO the perimeter
- From outside perimeter to inside
- Default: Deny all ingress

**Ingress Rule Components:**
- **Source**: Identity and/or IP range
- **Target**: Service and method
- **Condition**: Access level requirements

```yaml
# Example: Allow BigQuery access from specific IPs
ingressPolicies:
  - ingressFrom:
      sources:
        - accessLevel: accessPolicies/POLICY_ID/accessLevels/CORPORATE_NETWORK
      identities:
        - "serviceAccount:analytics@project.iam.gserviceaccount.com"
    ingressTo:
      operations:
        - serviceName: bigquery.googleapis.com
          methodSelectors:
            - method: "*"
```

#### Egress Policy
- Control requests going OUT of the perimeter
- From inside perimeter to outside
- Default: Deny all egress

**Egress Rule Components:**
- **Source**: Identity inside perimeter
- **Target**: External resource or service
- **Condition**: Access level requirements

```yaml
# Example: Allow Cloud Storage writes to backup bucket
egressPolicies:
  - egressFrom:
      identities:
        - "serviceAccount:backup@project.iam.gserviceaccount.com"
    egressTo:
      operations:
        - serviceName: storage.googleapis.com
          methodSelectors:
            - method: "google.storage.objects.create"
      resources:
        - "projects/BACKUP_PROJECT_NUMBER"
```

### VPC Accessible Services
- Restrict which GCP services can be accessed from VPC
- Even inside perimeter, limit service access
- Prevent lateral movement

```yaml
vpcAccessibleServices:
  enableRestriction: true
  allowedServices:
    - "storage.googleapis.com"
    - "bigquery.googleapis.com"
    - "cloudsql.googleapis.com"
```

### Common Use Cases
#### Prevent Cloud Storage Exfiltration
```
Problem: Malicious actor copies data to their bucket
Solution: VPC SC prevents storage.objects.create outside perimeter
Result: Data cannot leave protected buckets
```

#### Protect Sensitive BigQuery Datasets
```
Problem: Analyst exports data to personal project
Solution: Create perimeter around analytics project
Result: Cannot query from outside perimeter, even with IAM
```

#### Secure Multi-Project Architecture
```
Architecture:
- Production perimeter: prod-project-1, prod-project-2
- Staging perimeter: staging-project
- Perimeter bridge: Allow prod to read from shared-data project
```

#### Secure CI/CD Pipeline
```
Problem: CI/CD needs to access production resources
Solution:
- Create access level for CI/CD IP ranges
- Ingress policy allows Cloud Build from that access level
- Egress policy allows deployment to Artifact Registry
```

### VPC SC vs IAM
| Aspect | IAM | VPC SC |
|--------|-----|--------|
| Controls | Who has access | Where access happens |
| Scope | Identity-based | Context-aware |
| Data exfiltration | No protection | Prevents |
| Credential compromise | Vulnerable | Protected |
| Granularity | Permission-level | Service/project-level |
| Enforcement | Resource level | API level |

==IAM + VPC SC = Defense in Depth==
- IAM: Who can do what
- VPC SC: Where they can do it from

### VPC SC vs AWS VPC Endpoints
| Feature | VPC SC | VPC Endpoints |
|---------|--------|---------------|
| Scope | Project/org-wide | VPC-specific |
| Network changes | No | Yes (routing) |
| Data exfiltration | Prevents | Limits |
| Context-aware | Yes | No |
| Dry run mode | Yes | No |
| Cross-project | Yes | Requires peering |

### Limitations
- Not all GCP services supported
- Increases complexity
- **Can break existing workflows** (test in dry run first)
- Ingress/egress rules can be complex
- Cannot be applied retroactively without planning
- May require network architecture changes

### Pricing
- **VPC Service Controls is free**
- No additional charges for perimeters or access levels
- May incur costs for underlying services (Cloud Logging for audit)

---

## ACE Level

### Essential gcloud Commands
```bash
# List access policies
gcloud access-context-manager policies list

# Create access level (basic)
gcloud access-context-manager levels create LEVEL_NAME \
  --title="Corporate Network" \
  --policy=POLICY_ID \
  --basic-level-spec=level.yaml

# level.yaml example
combiningFunction: AND
conditions:
  - ipSubnetworks:
      - "203.0.113.0/24"

# List access levels
gcloud access-context-manager levels list --policy=POLICY_ID

# Describe access level
gcloud access-context-manager levels describe LEVEL_NAME --policy=POLICY_ID

# Create service perimeter (dry run)
gcloud access-context-manager perimeters create PERIMETER_NAME \
  --title="Production Perimeter" \
  --resources=projects/PROJECT_NUMBER \
  --restricted-services=storage.googleapis.com,bigquery.googleapis.com \
  --policy=POLICY_ID \
  --perimeter-type=regular \
  --enable-vpc-accessible-services \
  --vpc-allowed-services=storage.googleapis.com,bigquery.googleapis.com

# Update perimeter to enforced mode (from dry run)
gcloud access-context-manager perimeters update PERIMETER_NAME \
  --set-enforced-config-from-dry-run \
  --policy=POLICY_ID

# List service perimeters
gcloud access-context-manager perimeters list --policy=POLICY_ID

# Describe perimeter
gcloud access-context-manager perimeters describe PERIMETER_NAME --policy=POLICY_ID

# Add project to perimeter
gcloud access-context-manager perimeters update PERIMETER_NAME \
  --add-resources=projects/PROJECT_NUMBER \
  --policy=POLICY_ID

# Remove project from perimeter
gcloud access-context-manager perimeters update PERIMETER_NAME \
  --remove-resources=projects/PROJECT_NUMBER \
  --policy=POLICY_ID

# Add restricted service
gcloud access-context-manager perimeters update PERIMETER_NAME \
  --add-restricted-services=cloudsql.googleapis.com \
  --policy=POLICY_ID

# Create perimeter bridge
gcloud access-context-manager perimeters create BRIDGE_NAME \
  --perimeter-type=bridge \
  --add-resources=projects/PROJECT1_NUMBER,projects/PROJECT2_NUMBER \
  --policy=POLICY_ID

# Delete perimeter
gcloud access-context-manager perimeters delete PERIMETER_NAME --policy=POLICY_ID
```

### Key Concepts for ACE
- Understanding service perimeters and their purpose
- Creating access levels (IP-based, device-based)
- Creating and configuring service perimeters
- Adding projects and services to perimeters
- Using dry run mode to test configurations
- Understanding ingress and egress policies (basic)
- Differentiating VPC SC from IAM
- Viewing VPC SC violations in logs
- Creating perimeter bridges for cross-perimeter access
- Understanding VPC Accessible Services

---

## PCA Level

### Architectural Patterns
#### Hub and Spoke Perimeter Design
```
Architecture:
- Central "hub" perimeter: Shared services (logging, monitoring, secrets)
- Spoke perimeters: prod, staging, dev
- Perimeter bridges connect spokes to hub
- Each spoke isolated from others

Benefits:
- Centralized shared services
- Environment isolation
- Easier compliance auditing
- Reduced complexity
```

#### Defense in Depth Strategy
```
Layer 1: Organization Policies (prevent external IPs, enforce regions)
Layer 2: IAM (least privilege, service accounts)
Layer 3: VPC Firewall Rules (network-level)
Layer 4: VPC Service Controls (API-level data exfiltration prevention)
Layer 5: Encryption (CMEK, data at rest and in transit)
```

#### Zero Trust Architecture
```
Components:
1. VPC Service Controls: Perimeter around sensitive data
2. Identity-Aware Proxy: Context-aware access to applications
3. BeyondCorp Enterprise: Device and user identity verification
4. Access Levels: IP, device posture, user attributes
5. Binary Authorization: Only verified containers deployed

Result: Never trust, always verify
```

### Advanced Perimeter Configuration
#### Multi-Environment Perimeter Strategy
```bash
# Production perimeter
gcloud access-context-manager perimeters create prod-perimeter \
  --title="Production Environment" \
  --resources=projects/PROD_PROJECT_1,projects/PROD_PROJECT_2 \
  --restricted-services=storage.googleapis.com,bigquery.googleapis.com,cloudsql.googleapis.com \
  --access-levels=accessPolicies/POLICY/accessLevels/prod-access \
  --policy=POLICY_ID

# Staging perimeter
gcloud access-context-manager perimeters create staging-perimeter \
  --title="Staging Environment" \
  --resources=projects/STAGING_PROJECT \
  --restricted-services=storage.googleapis.com,bigquery.googleapis.com \
  --access-levels=accessPolicies/POLICY/accessLevels/dev-access \
  --policy=POLICY_ID

# Bridge for shared data
gcloud access-context-manager perimeters create shared-data-bridge \
  --perimeter-type=bridge \
  --resources=projects/SHARED_DATA_PROJECT \
  --policy=POLICY_ID

# Connect perimeters via bridge
gcloud access-context-manager perimeters update prod-perimeter \
  --add-perimeter-bridges=shared-data-bridge \
  --policy=POLICY_ID
```

#### Complex Access Level Configuration
```yaml
# access-level-advanced.yaml
title: "Advanced Access Level"
basic:
  combiningFunction: AND
  conditions:
    # Corporate network OR VPN
    - ipSubnetworks:
        - "203.0.113.0/24"  # Corporate office
        - "198.51.100.0/24" # VPN range

    # Managed devices only
    - devicePolicy:
        requireScreenlock: true
        requireCorpOwned: true
        osConstraints:
          - osType: DESKTOP_CHROME_OS
          - osType: DESKTOP_MAC
            minimumVersion: "12.0.0"
          - osType: DESKTOP_WINDOWS
            minimumVersion: "10.0.19041"

    # During business hours only (example for contractors)
    - regions:
        - "US"
        - "EU"
```

### Ingress/Egress Policy Patterns
#### Allow CI/CD Access
```yaml
# Ingress: Allow Cloud Build to access production
ingressPolicies:
  - ingressFrom:
      sources:
        - accessLevel: accessPolicies/POLICY/accessLevels/cicd-access
      identities:
        - "serviceAccount:cloud-build@project.iam.gserviceaccount.com"
    ingressTo:
      operations:
        - serviceName: "storage.googleapis.com"
          methodSelectors:
            - method: "google.storage.objects.get"
            - method: "google.storage.objects.create"
        - serviceName: "artifactregistry.googleapis.com"
          methodSelectors:
            - method: "*"
      resources:
        - "projects/PROD_PROJECT_NUMBER"
```

#### Allow Backup to External Project
```yaml
# Egress: Allow backup to separate backup project
egressPolicies:
  - egressFrom:
      identities:
        - "serviceAccount:backup-service@prod.iam.gserviceaccount.com"
    egressTo:
      operations:
        - serviceName: "storage.googleapis.com"
          methodSelectors:
            - method: "google.storage.objects.create"
            - method: "google.storage.objects.get"
      resources:
        - "projects/BACKUP_PROJECT_NUMBER"
```

#### Restrict BigQuery Data Export
```yaml
# Prevent BigQuery export outside perimeter
# No egress policy = default deny
# Only allow export to Cloud Storage buckets inside perimeter
ingressPolicies:
  - ingressFrom:
      identities:
        - "user:data-analyst@example.com"
    ingressTo:
      operations:
        - serviceName: "bigquery.googleapis.com"
          methodSelectors:
            - method: "google.cloud.bigquery.v2.JobService.Query"
            # Deny: google.cloud.bigquery.v2.JobService.ExtractTable
```

### Dry Run to Production Migration
**Phase 1: Dry Run (Test)**
```bash
# Create perimeter in dry run mode
gcloud access-context-manager perimeters create test-perimeter \
  --title="Test Perimeter" \
  --resources=projects/TEST_PROJECT \
  --restricted-services=storage.googleapis.com \
  --policy=POLICY_ID \
  --perimeter-type=regular

# Monitor logs for violations
gcloud logging read "protoPayload.metadata.dryRun=true \
  AND protoPayload.metadata.@type=\"type.googleapis.com/google.cloud.audit.VpcServiceControlAuditMetadata\"" \
  --limit=100
```

**Phase 2: Analyze Violations**
```bash
# Export to BigQuery for analysis
gcloud logging sinks create vpc-sc-violations \
  bigquery.googleapis.com/projects/PROJECT/datasets/vpc_sc_logs \
  --log-filter="protoPayload.metadata.dryRun=true"

# Analyze in BigQuery
SELECT
  protopayload_auditlog.authenticationInfo.principalEmail,
  protopayload_auditlog.serviceName,
  protopayload_auditlog.methodName,
  COUNT(*) as violation_count
FROM `project.vpc_sc_logs.cloudaudit_googleapis_com_data_access_*`
WHERE protopayload_auditlog.metadata.dryRun = true
GROUP BY 1, 2, 3
ORDER BY violation_count DESC
```

**Phase 3: Add Ingress/Egress Rules**
```bash
# Create ingress/egress rules for legitimate traffic
# Update perimeter with rules
gcloud access-context-manager perimeters update test-perimeter \
  --set-ingress-policies=ingress-policy.yaml \
  --set-egress-policies=egress-policy.yaml \
  --policy=POLICY_ID
```

**Phase 4: Enforce**
```bash
# Switch from dry run to enforced
gcloud access-context-manager perimeters update test-perimeter \
  --set-enforced-config-from-dry-run \
  --policy=POLICY_ID
```

### Monitoring & Alerting
**VPC SC Violation Monitoring:**
```bash
# Create log-based metric
gcloud logging metrics create vpc-sc-violations \
  --description="Count of VPC SC violations" \
  --log-filter="protoPayload.metadata.@type=\"type.googleapis.com/google.cloud.audit.VpcServiceControlAuditMetadata\" \
    AND protoPayload.metadata.violationReason!=\"\""

# Create alert policy
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="VPC SC Violations Alert" \
  --condition-display-name="High Violation Rate" \
  --condition-threshold-value=10 \
  --condition-threshold-duration=300s \
  --condition-filter="resource.type=\"audited_resource\" \
    AND metric.type=\"logging.googleapis.com/user/vpc-sc-violations\""
```

**Dashboard for VPC SC:**
- Violations by service
- Violations by user/service account
- Ingress/egress policy hits
- Perimeter access patterns
- Failed access attempts

### Compliance & Audit
**Data Residency Enforcement:**
```yaml
# Restrict Cloud Storage to US regions only
vpcAccessibleServices:
  enableRestriction: true
  allowedServices:
    - "storage.googleapis.com"

# In organization policy
constraints/gcp.resourceLocations:
  values:
    allowedValues:
      - "in:us-locations"

# VPC SC perimeter around US projects
# Prevents data from leaving US
```

**PCI-DSS Compliance:**
```
Requirements:
1. Isolate cardholder data environment (CDE)
2. Restrict access to CDE

VPC SC Implementation:
1. Create perimeter around CDE projects
2. Restrict services: Storage, SQL, BigQuery, KMS
3. Access level: Corporate network + managed devices
4. Ingress: Only approved applications
5. Egress: Deny all (except approved backups)
6. Audit logging: All access attempts
```

**HIPAA Compliance:**
```
PHI Protection:
1. Perimeter around healthcare data projects
2. Device policy: Screen lock + admin approval
3. IP restriction: Healthcare facility networks only
4. No egress to personal projects
5. Encrypt at rest (CMEK)
6. Audit all access (Cloud Logging + BigQuery export)
```

### Troubleshooting VPC SC
**Common Issues:**

**Issue 1: Legitimate traffic blocked**
```bash
# Check audit logs
gcloud logging read "protoPayload.metadata.violationReason!=\"\" \
  AND protoPayload.authenticationInfo.principalEmail=\"user@example.com\"" \
  --limit=10

# Add ingress policy to allow
```

**Issue 2: Service not working inside perimeter**
```bash
# Check if service is supported
gcloud access-context-manager supported-services list

# Verify service is in restricted services list
gcloud access-context-manager perimeters describe PERIMETER_NAME \
  --policy=POLICY_ID
```

**Issue 3: Cross-project access not working**
```bash
# Create perimeter bridge
gcloud access-context-manager perimeters create bridge \
  --perimeter-type=bridge \
  --resources=projects/PROJECT1,projects/PROJECT2 \
  --policy=POLICY_ID
```

### Integration with Other Security Services
**VPC SC + Cloud KMS:**
- Prevent keys from being used outside perimeter
- Decrypt operations blocked from outside
- CMEK for data inside perimeter

**VPC SC + Secret Manager:**
- Secrets cannot be accessed outside perimeter
- Even with IAM permissions

**VPC SC + Identity-Aware Proxy:**
- IAP provides user authentication
- VPC SC provides context-aware access
- Combined: User must be authenticated AND within perimeter

**VPC SC + Binary Authorization:**
- Binary Authorization: Only verified images deployed
- VPC SC: Images cannot be copied outside perimeter
- Combined: Secure supply chain

### Cost Optimization
- VPC Service Controls is free
- Indirect costs: Engineering time for setup
- Reduce complexity: Start with broad perimeters, refine over time
- Use dry run extensively (prevents costly mistakes)
- Automate perimeter management (Terraform)

### Terraform Configuration Example
```hcl
# Access level
resource "google_access_context_manager_access_level" "corporate_network" {
  parent = "accessPolicies/${var.access_policy_id}"
  name   = "accessPolicies/${var.access_policy_id}/accessLevels/corporate_network"
  title  = "Corporate Network"

  basic {
    combining_function = "AND"
    conditions {
      ip_subnetworks = ["203.0.113.0/24"]
    }
  }
}

# Service perimeter
resource "google_access_context_manager_service_perimeter" "production" {
  parent = "accessPolicies/${var.access_policy_id}"
  name   = "accessPolicies/${var.access_policy_id}/servicePerimeters/production"
  title  = "Production Perimeter"

  status {
    resources = [
      "projects/${var.prod_project_number_1}",
      "projects/${var.prod_project_number_2}",
    ]

    restricted_services = [
      "storage.googleapis.com",
      "bigquery.googleapis.com",
      "cloudsql.googleapis.com",
    ]

    access_levels = [
      google_access_context_manager_access_level.corporate_network.name,
    ]

    vpc_accessible_services {
      enable_restriction = true
      allowed_services = [
        "storage.googleapis.com",
        "bigquery.googleapis.com",
      ]
    }

    ingress_policies {
      ingress_from {
        sources {
          access_level = google_access_context_manager_access_level.corporate_network.name
        }
        identities = [
          "serviceAccount:cicd@project.iam.gserviceaccount.com",
        ]
      }
      ingress_to {
        resources = ["*"]
        operations {
          service_name = "storage.googleapis.com"
          method_selectors {
            method = "*"
          }
        }
      }
    }
  }
}
```

### Well-Architected Considerations
- **Operational Excellence**: Infrastructure as code (Terraform), dry run before enforcement, comprehensive logging
- **Reliability**: Test perimeters in non-production first, gradual rollout, perimeter bridges for dependencies
- **Security**: Defense in depth with IAM, prevent data exfiltration, context-aware access, zero trust architecture
- **Performance**: VPC SC operates at API layer (no network latency), cached access level evaluations
- **Cost**: Free service, engineering cost for setup and maintenance, automation reduces ongoing costs
