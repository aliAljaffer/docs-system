---
title: iam
category: GCP
description: 'GCP note: Iam.'
tags:
- gcp
- security
---


# iam

## IAM (Identity and Access Management)
**Identity and Access Management** - Control who (identity) has what access (role) to which resources

**AWS Equivalent:** AWS IAM

### Core IAM Concepts
**Policy Binding Formula:**
==Member + Role + Resource = Policy Binding==

#### Members (WHO)

| Member | Meaning |
|---|---|
| **Google Account** | End user (consumer Gmail or Workspace) |
| **Service Account** | Application/workload identity |
| **Google Group** | Collection of Google accounts and service accounts |
| **Google Workspace domain** | All users in organization (example.com) |
| **Cloud Identity domain** | Like Workspace but without Google Workspace apps |
| **allAuthenticatedUsers** | Any authenticated Google account |
| **allUsers** | Anyone on the internet (public access) |

#### Roles (WHAT)
Three types of roles:

| Role type | Defined by | Details | Guidance |
|---|---|---|---|
| Primitive (Legacy - Avoid) | - | Owner: Full access + manage roles + billing. Editor: Modify access to resources. Viewer: Read-only access | **Too broad, not recommended for production** |
| Predefined | Google (created and maintained) | Granular permissions for specific services. Examples: `roles/compute.instanceAdmin.v1`, `roles/storage.objectViewer` | **Recommended for most use cases** |
| Custom | You (user-defined roles with specific permissions) | Created at organization or project level, not available at folder level. Lifecycle stages: ALPHA, BETA, GA, DEPRECATED, DISABLED | **Use when predefined roles are too permissive** |

#### Resources (WHERE)
- Organization
- Folders
- Projects
- Individual resources (VMs, buckets, etc.)

### IAM Hierarchy
```text
Organization (optional)
  └── Folders (optional, can be nested)
      └── Projects (required)
          └── Resources
```

- **Policies are inherited down the hierarchy**
- Child policies cannot remove access granted at parent level
- More permissive parent policy always overrides restrictive child policy
- Best practice: Grant least privilege at lowest level

### Service Accounts
**AWS Equivalent:** [[security-iam#IAM Roles|IAM Roles]]

**Application/workload identity** - Not for end users

#### Types of Service Accounts

| Type | Created by | Format | Notes |
|---|---|---|---|
| User-managed | You create and manage | `sa-name@project-id.iam.gserviceaccount.com` | Up to 100 per project (can request increase) |
| Default | - | Compute Engine default: `PROJECT_NUMBER-compute@developer.gserviceaccount.com`. App Engine default: `PROJECT_ID@appspot.gserviceaccount.com` | **Highly privileged (Editor role), disable if not needed** |
| Google-managed | Google | `@PROJECT_ID.iam.gserviceaccount.com` | Used by Google services on your behalf |

#### Service Account Keys
**Two types:**
- **GCP-managed keys**: Rotated automatically, cannot download
- **User-managed keys**: You create and manage, **security risk if compromised**

**Best Practice: Avoid user-managed keys**
- Use Workload Identity (GKE)
- Use Workload Identity Federation (external workloads)
- Use service account impersonation
- Use short-lived credentials

#### Service Account Impersonation
- One service account acts as another
- Grant `roles/iam.serviceAccountTokenCreator`
- No need to download keys
- Better auditability and security

### IAM Conditions
**AWS Equivalent:** IAM Policy Conditions

**Conditional access based on attributes**

**Common Condition Attributes:**

| Attribute | Example |
|---|---|
| **Time/Date** | `request.time < timestamp("2026-01-01T00:00:00Z")` |
| **IP Address** | `origin.ip in ["203.0.113.0/24"]` |
| **Resource attributes** | `resource.name.startsWith("projects/_/buckets/prod-")` |
| **Resource tags** | `resource.hasTagValue("tagKeys/123", "tagValues/456")` |

**Use Cases:**
- Temporary access (intern accounts expire)
- IP-based restrictions (VPN-only access)
- Time-based access (business hours only)
- Resource-based access (prod vs dev environments)

```bash
# Example: Grant storage access only during business hours
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member='user:user@example.com' \
  --role='roles/storage.objectViewer' \
  --condition='expression=request.time.getHours("America/New_York") >= 9 && request.time.getHours("America/New_York") < 17,title=business-hours-only'
```

### IAM Policy Structure
```json
{
  "bindings": [
    {
      "role": "roles/storage.objectViewer",
      "members": [
        "user:user@example.com",
        "serviceAccount:sa@project.iam.gserviceaccount.com"
      ],
      "condition": {
        "title": "Expires_January_2026",
        "expression": "request.time < timestamp('2026-01-01T00:00:00Z')"
      }
    }
  ],
  "etag": "BwXY...",
  "version": 3
}
```

### Policy Versions
- **Version 1**: Basic bindings (legacy)
- **Version 3**: Supports conditions and multiple bindings for same role
- **Always use version 3 for new policies**

### Organization Policies
**AWS Equivalent:** [[management-and-governance-organizations#Organizations vs. SCPs|AWS SCPs]]

**Centralized constraints across organization**

**Two types:**
- **List constraints**: Allowed/denied values
  - Example: Restrict VM locations to specific regions
- **Boolean constraints**: Enforce or disable a feature
  - Example: Require OS Login on all VMs

**Common Organization Policies:**

| Constraint | Effect |
|---|---|
| `constraints/compute.vmExternalIpAccess` | Restrict external IPs |
| `constraints/iam.disableServiceAccountKeyCreation` | Prevent service account keys |
| `constraints/compute.restrictSharedVpcSubnetworks` | Control Shared VPC usage |
| `constraints/sql.restrictPublicIp` | Prevent public Cloud SQL instances |

### IAM Recommender
- AI-powered recommendations to remove excessive permissions
- Analyzes last 90 days of usage
- Side-by-side comparison of current vs recommended roles
- **Helps implement least privilege**

### Policy Troubleshooter
- Debug why a user does/doesn't have access
- Shows complete permission evaluation path
- Explains inherited policies
- **Essential tool for IAM debugging**

### Workload Identity Federation
**AWS Equivalent:** [[security-iam#IAM Roles|OIDC/SAML Federation]]

**Access GCP from external workloads without service account keys**

**Supported Identity Providers:**
- AWS IAM
- Azure Active Directory
- OIDC providers (GitHub Actions, GitLab, etc.)
- SAML 2.0 providers

**Benefits:**
- No service account keys to manage
- Short-lived credentials
- Better security posture
- Seamless multi-cloud integration

### Resource Hierarchy Best Practices

| Level | Use for |
|---|---|
| **Organization level** | Org-wide policies (security, compliance) |
| **Folder level** | Department/environment grouping (prod, dev, staging) |
| **Project level** | Application workloads |
| **Resource level** | Specific overrides (avoid when possible) |

### IAM vs AWS IAM Comparison

| Feature | GCP IAM | AWS IAM |
|---------|---------|---------|
| Policy attachment | Resource-centric | Identity-centric |
| Inheritance | Top-down hierarchy | No inheritance |
| Deny policies | Yes (Deny policies) | Yes (explicit deny) |
| Conditions | Yes, attribute-based | Yes, condition keys |
| Service accounts | First-class identities | IAM Roles for services |
| Temporary credentials | Workload Identity Federation | STS, OIDC, SAML |
| Policy evaluation | Allow by default if granted | Deny by default |
| Max policy size | No strict limit | 6,144 chars (managed), 10,240 (inline) |

### Audit Logging for IAM

| Log | Records | Default |
|---|---|---|
| **Admin Activity logs** | Who changed IAM policies | Always on, free |
| **Data Access logs** | Who accessed what data | Disabled by default, costs |
| **System Event logs** | Automated system changes | - |
| **Policy Denied logs** | Denied access attempts | - |

### Common IAM Patterns
#### Least Privilege
```bash
# Grant minimal role for specific task
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member='user:dev@example.com' \
  --role='roles/compute.instanceAdmin.v1'
```

#### Service Account Impersonation
```bash
# Allow user to act as service account
gcloud iam service-accounts add-iam-policy-binding SA_EMAIL \
  --member='user:admin@example.com' \
  --role='roles/iam.serviceAccountTokenCreator'
```

#### Cross-Project Access
```bash
# Grant service account in Project A access to Project B
gcloud projects add-iam-policy-binding PROJECT_B_ID \
  --member='serviceAccount:sa@project-a.iam.gserviceaccount.com' \
  --role='roles/storage.objectViewer'
```

### Pricing
- IAM is free
- No charge for policy evaluations
- Audit logging has storage costs (Cloud Logging pricing)

---

## ACE Level

### Essential gcloud Commands
```bash
# View project IAM policy
gcloud projects get-iam-policy PROJECT_ID

# Add IAM policy binding
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member='user:user@example.com' \
  --role='roles/viewer'

# Remove IAM policy binding
gcloud projects remove-iam-policy-binding PROJECT_ID \
  --member='user:user@example.com' \
  --role='roles/viewer'

# List all roles
gcloud iam roles list

# Describe a role
gcloud iam roles describe roles/compute.instanceAdmin.v1

# Create service account
gcloud iam service-accounts create SA_NAME \
  --display-name="My Service Account"

# List service accounts
gcloud iam service-accounts list

# Create service account key (avoid in production)
gcloud iam service-accounts keys create ~/key.json \
  --iam-account=SA_EMAIL

# Grant role to service account
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member='serviceAccount:SA_EMAIL' \
  --role='roles/storage.objectViewer'

# Impersonate service account
gcloud compute instances list --impersonate-service-account=SA_EMAIL

# Test IAM permissions
gcloud projects get-iam-policy PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:user@example.com"
```

### Key Concepts for ACE
- Understanding members, roles, and resources
- Difference between primitive, predefined, and custom roles
- Creating and managing service accounts
- Granting and revoking IAM permissions
- Understanding policy inheritance
- Using predefined roles (avoid primitive roles)
- Service account best practices (avoid user-managed keys)
- Viewing effective permissions using Cloud Console
- Basic IAM troubleshooting with Policy Troubleshooter
- Understanding default service accounts and their risks

---

## PCA Level

### Architectural Considerations
#### Identity Management Strategy
- Use Cloud Identity or Google Workspace for centralized user management
- Sync with on-prem Active Directory using Google Cloud Directory Sync (GCDS)
- Implement SSO with external IdP via SAML or OIDC
- Plan for identity lifecycle (joiners, movers, leavers)

#### Resource Hierarchy Design
- Organization for billing and centralized policies
- Folders for environment separation (prod, staging, dev)
- Folders for team/department isolation
- Projects for workload boundaries
- **Design hierarchy before implementation, hard to change later**

#### Service Account Management
- One service account per application/service
- Dedicated projects for shared service accounts
- Rotate service account keys (if using them) every 90 days
- Use Workload Identity for GKE workloads
- Use Workload Identity Federation for external workloads (AWS, Azure, GitHub)
- Implement service account impersonation over key downloads

#### Least Privilege Implementation
- Start with viewer, grant incrementally
- Use predefined roles over primitive roles
- Create custom roles for specific use cases
- Regular access reviews (quarterly)
- Use IAM Recommender for permission rightsizing
- Implement time-based access with IAM Conditions

### Multi-Cloud IAM Integration
**AWS Integration**
```bash
# Workload Identity Federation for AWS
# 1. Create Workload Identity Pool
gcloud iam workload-identity-pools create aws-pool \
  --location="global" \
  --display-name="AWS Pool"

# 2. Create AWS provider
gcloud iam workload-identity-pools providers create-aws aws-provider \
  --location="global" \
  --workload-identity-pool="aws-pool" \
  --account-id="AWS_ACCOUNT_ID"

# 3. Bind to service account
gcloud iam service-accounts add-iam-policy-binding SA_EMAIL \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/aws-pool/attribute.aws_role/arn:aws:sts::AWS_ACCOUNT_ID:assumed-role/ROLE_NAME"
```

**Azure Integration**
- Use Workload Identity Federation with Azure AD
- OIDC-based authentication
- No need for service account keys

**GitHub Actions Integration**
- OIDC provider for GitHub
- Authenticate without storing credentials
- Repository-specific access control

### Organization Policy Strategy
**Preventive Controls**
```bash
# Restrict VM external IPs
gcloud resource-manager org-policies set-policy policy.yaml

# policy.yaml
constraint: constraints/compute.vmExternalIpAccess
listPolicy:
  deniedValues:
    - "projects/PROJECT_ID/zones/*/instances/*"

# Disable service account key creation
constraint: constraints/iam.disableServiceAccountKeyCreation
booleanPolicy:
  enforced: true

# Restrict resource locations (data residency)
constraint: constraints/gcp.resourceLocations
listPolicy:
  allowedValues:
    - "in:us-locations"
    - "in:eu-locations"
```

### Security Controls & Compliance
#### Access Control Policies
- Implement separation of duties (SoD)
- Break glass procedures for emergency access
- Privileged access management (PAM)
- Regular access certification

#### Audit & Compliance
- Enable Admin Activity logs (always on)
- Enable Data Access logs for sensitive resources
- Export logs to BigQuery for long-term retention
- Use Access Transparency for Google employee access visibility
- Cloud Audit Logs for compliance (SOC 2, ISO, HIPAA, PCI-DSS)

#### VPC Service Controls Integration
- Combine with IAM for defense-in-depth
- Prevent data exfiltration even with compromised credentials
- Create security perimeters around sensitive projects

### Advanced IAM Patterns
#### Service Account Chaining
```bash
# User -> SA1 -> SA2 -> Resource
# User impersonates SA1
gcloud iam service-accounts add-iam-policy-binding SA1_EMAIL \
  --member='user:admin@example.com' \
  --role='roles/iam.serviceAccountTokenCreator'

# SA1 impersonates SA2
gcloud iam service-accounts add-iam-policy-binding SA2_EMAIL \
  --member='serviceAccount:SA1_EMAIL' \
  --role='roles/iam.serviceAccountTokenCreator'
```

#### Just-in-Time Access
- Use IAM Conditions with time constraints
- Temporary elevated access for incidents
- Automatic revocation after time window
- Integrate with ticketing systems (JIRA, ServiceNow)

#### Federated Identity for B2B
- SAML 2.0 for partner organizations
- Partner access to specific projects
- Automated provisioning/deprovisioning
- Audit trail for external access

### Custom Roles Design
```bash
# Create custom role
gcloud iam roles create customComputeRole \
  --project=PROJECT_ID \
  --title="Custom Compute Role" \
  --description="Custom role for compute operations" \
  --permissions=compute.instances.get,compute.instances.list,compute.instances.start,compute.instances.stop \
  --stage=GA

# Update custom role
gcloud iam roles update customComputeRole \
  --project=PROJECT_ID \
  --add-permissions=compute.instances.reset

# Disable custom role
gcloud iam roles update customComputeRole \
  --project=PROJECT_ID \
  --stage=DISABLED
```

### IAM Limits & Quotas

| Limit | Value |
|---|---|
| **Policy size** | 64 KB per resource |
| **Bindings per policy** | 1,500 |
| **Members per binding** | 1,500 |
| **Conditional role bindings** | 100 per policy |
| **Service accounts per project** | 100 (default) |
| **Service account keys** | 10 per service account |

### Migration from AWS IAM
**Mapping AWS Concepts to GCP:**

| AWS concept | GCP equivalent |
|---|---|
| AWS IAM User | Google Account or Service Account |
| AWS IAM Role | Service Account |
| AWS IAM Group | Google Group |
| AWS IAM Policy | IAM Role (predefined or custom) |
| AWS SCP | Organization Policy |
| AWS STS | Workload Identity Federation |
| AWS AssumeRole | Service Account Impersonation |

**Migration Strategy:**
1. Map existing AWS policies to GCP predefined roles
2. Create custom roles for gaps
3. Establish resource hierarchy (organization/folders/projects)
4. Implement Workload Identity Federation for cross-cloud access
5. Set up organization policies for guardrails
6. Enable audit logging
7. Conduct access review and cleanup

### Cost Optimization
- Use groups instead of individual users (easier management, same cost)
- Avoid excessive service accounts (consolidate where appropriate)
- Regular access reviews to remove unused permissions
- Centralize audit logs export to avoid duplication
- Use IAM Recommender to reduce over-provisioned roles

### Well-Architected Considerations
- **Operational Excellence**: Automate IAM changes via Terraform, document role assignments, regular access reviews
- **Reliability**: Design for principal of least privilege, implement redundancy in access paths, avoid single user dependencies
- **Security**: Enforce MFA, eliminate long-lived credentials, use Workload Identity, implement organization policies, enable audit logging
- **Performance**: Use groups for bulk operations, cache role lookups in applications, optimize service account usage
- **Cost**: Consolidate service accounts, use groups, automate access removal, regular cleanup of unused identities
