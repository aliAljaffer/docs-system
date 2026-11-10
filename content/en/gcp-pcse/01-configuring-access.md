# 1. Configuring access

**Goal:** Control who signs in, what each identity can do, and how workloads get credentials.

## Cloud Identity and sign-in

- **Google Cloud Directory Sync (GCDS):** Syncs users and groups from AD or LDAP into [[iam]] identities in Cloud Identity. It is one way, and you schedule it. It supports a dry run. It uses a dedicated Google identity with Super Admin rights.
- **Passwords:** GCDS does not sync passwords by default. Google Password Sync does.
- **SSO with a third-party IdP:** Configure a SAML profile in the Admin console. Apply it to org units or groups.
- **Workforce Identity Federation (WIF):** An external IdP, such as Okta or Microsoft Entra ID, authenticates users. Google grants access without creating Cloud Identity accounts. WIF uses a workforce identity pool, an OIDC or SAML provider, attribute mapping, and attribute conditions. WIF does not support features tied to Cloud Identity accounts, such as 2SV policies, password policies, or the super admin role.

| Need | Answer |
|---|---|
| Avoid duplicate users in Cloud Identity | Workforce Identity Federation |
| Sync AD users and groups on a schedule | GCDS |
| Sync AD passwords | Google Password Sync |
| Sign users in with a corporate IdP | SAML SSO |

### Super admin accounts

1. Keep at least 2 super admins for break-glass access. Keep no more than a handful.
2. Protect each one with a hardware security key and 2SV.
3. Store recovery codes offline.
4. Do not use super admins for daily work.

Super Admin (Cloud Identity) and Organization Administrator (IAM) are separate roles. Keep them separate.

### Users and groups

- Grant roles to groups. Manage membership in Cloud Identity. Removing a user from a group removes that access.
- A managed account has one identity: the organization domain email.
- Federation: Google is the service provider. The IdP authenticates. Google authorizes.

## Authentication

- Default password minimum length is 8.
- Default web session length is 14 days. The admin console session is fixed at 1 hour.
- 2SV methods, most secure first: security key, Google prompt, Authenticator codes, backup codes, text or voice.
- 2SV enforcement options: Any, Any except verification codes, Only security key.
- SAML needs the IdP Entity ID, the SSO URL, and a certificate. The response must include `saml:Subject` and `saml:NameID`.
- Use SAML for SSO into Cloud Identity. Use OAuth for app access with scoped tokens.

## Service accounts

| Scenario | Answer |
|---|---|
| Workload on [[gke]] needs Google API access | Workload Identity Federation for GKE |
| Workload on another cloud or on-premises needs access | Workload Identity Federation (keyless) |
| Human or workload needs a service account identity for a short time | Impersonation with Service Account Token Creator |
| Short-lived credential to sign URLs or JWTs | `signBlob` or `signJwt` with Token Creator |
| Legacy system cannot use any option above | User-managed key, with org policy, rotation, and monitoring |

### Roles

- **Service Account User:** Acts as the service account. Attach it to a resource or run a job as it.
- **Service Account Token Creator:** Mints tokens for the service account. Used for impersonation.

### Keys and impersonation

- A new service account has no permissions. Grant it roles.
- Keys never expire. Rotate keys yourself or by script. Rotate every 90 days or sooner. There is no built-in rotation.
- Audit key use in Data Access logs. The `serviceAccountKeyName` field identifies the key.
- `iam.disableServiceAccountKeyCreation` blocks new keys. It does not delete existing keys. Prefer `iam.disableServiceAccountKeyUpload` for uploads.
- Impersonation chains work. Service account A can impersonate B, which impersonates C. Each hop needs Token Creator on the next account.
- Impersonated tokens have no refresh token. Lifetimes run from about 1 minute to 12 hours. Chains shorten the maximum per hop.
- Use the `--impersonate-service-account` flag. A comma-separated list defines a chain. The console cannot impersonate.

```bash
gcloud config set auth/impersonate_service_account SA_EMAIL
```

### Default service accounts

- The Compute Engine and [[app-engine]] default service accounts have the Editor role on the project.
- Org policy `iam.automaticIamGrantsForDefaultServiceAccounts` stops the automatic Editor grant for new default accounts. It is not retroactive.
- Replace default accounts with purpose-built accounts.

### Workload Identity Federation setup

- Create a workload identity pool at the global location.
- Create an OIDC provider with `--issuer-uri` and `--attribute-mapping`.
- Grant `roles/iam.workloadIdentityUser` to a `principalSet://` identity, such as one scoped by `attribute.repository`.
- Attribute changes take up to 5 minutes.

### Other service account rules

- Never store service account keys in [[secret-manager]]. An app that can call Secret Manager does not need a key.
- Domain-wide delegation uses the `signJwt` API, not keys.
- Disable a service account before you delete it. Disabling blocks token minting and API calls. Role bindings stay.
- Editor cannot change IAM policies. Editor can create or upload service account keys. That is a privilege escalation path.
- Limits: 100 service accounts per project. Names are immutable and have 6 to 30 characters. An account cannot move to another project.
- Org policy `iam.disableCrossProjectServiceAccountUsage` is enforced by default.

## Authorization

### Roles

- Custom roles exist at the organization or project level. They cannot include `*` in permissions. Use `gcloud iam roles describe` to list permissions.
- Basic, predefined, and custom roles all exist. Prefer predefined roles over basic roles.

### IAM Conditions

- A condition is a CEL expression on a binding. It can use `resource.name`, `resource.type`, or `request.time`.
- Each binding takes one condition.
- The condition runs on each access check.
- Conditions do not work on all roles. The basic Owner role has a restriction.

### Deny policies (IAM v3)

- Deny policies take precedence over allow bindings.
- Attach them at the organization, folder, or project. Not at the resource level.
- Principals use this form: `principal://goog/subject/EMAIL` for a user, `principalSet://goog/group/GROUP` for a group, and `principalSet://goog/cloudIdentityCustomerId/ID` for all users in a customer.
- You can deny individual users.
- Permissions use the v2 form, such as `storage.googleapis.com/buckets.create`.
- Management roles: `roles/iam.denyAdmin` to manage, `roles/iam.denyReviewer` to view.
- If a deny rule and an allow rule both match, access is denied.

### Access Context Manager

- Access levels are basic (IP ranges, device policy, region) or custom (CEL).
- Service perimeters belong to [[vpc-service-controls]]. Test them in dry run first.
- Ingress rules control who can enter a perimeter. Egress rules control what can leave. Bridges connect two perimeters.
- Access Context Manager defines the rules. VPC Service Controls, [[identity-aware-proxy]], and IAM Conditions enforce them.

### Inheritance and least privilege

- Policies inherit down the hierarchy: organization, folder, project, resource. A binding at a parent applies to all children.
- Resource-level bindings do not reach up.
- The effective allow policy is the union of the node's policy and all ancestor policies.
- IAM policy updates use an `etag` to prevent overwrites from concurrent changes.
- Apply [[principle-of-least-privilege]] at every level.
- Separate admin duties across people: organization admin, security admin, billing admin, and network admin.

### Policy Intelligence and related tools

| Tool | Question it answers |
|---|---|
| Policy Troubleshooter | Why did this principal get, or not get, this permission? |
| Policy Analyzer | Who has access to this resource? |
| IAM Recommender | Which over-granted roles can I remove, based on use? |
| Condition Simulator | What does this policy change do before I apply it? |
| Essential Contacts | Who receives critical notifications? |

Also know: Activity Analyzer (last use of a service account or key), service account insights (unused for 90 days), and lateral movement insights (cross-project impersonation).

### Privileged Access Manager (PAM)

- PAM grants time-bound, just-in-time access. It replaces standing admin access.
- A grant names the principal, role, duration, and justification. Multi-step approval is optional.
- Deploy PAM at the organization, folder, or project level.

### Cloud Storage access

- Uniform bucket-level access (UBLA) turns off ACLs. Enforce it with org policy `storage.uniformBucketLevelAccess`.
- After you enable UBLA, you have 90 days to revert. After that, the change is permanent.
- IAM and ACLs do not know about each other. Either one that grants access is enough. A public-read object ACL exposes that object.
- Signed URLs give temporary access either way.

## Resource hierarchy and org policies

- Use one organization. Keep the hierarchy shallow: organization, folders, projects.
- Folders can represent environments (small organizations), products (agile at scale), or geographies (multi-region compliance). Do not copy the corporate org chart.
- Org policies control what resources may do. IAM controls who may act.
- Constraints inherit down. A child can tighten a policy but not relax it. Exception: list constraints can reset values. `inheritFromParent` defaults to true.
- Dry run mode tests a policy in audit mode before enforcement. Pre-built and custom constraints both support it.
- Custom constraints use CEL.
- Tags group resources for org policy targeting. Tags do not apply to IAM allow policies.

Constraints to know by name:

- `iam.disableServiceAccountKeyCreation`
- `iam.allowedPolicyMemberDomains` (domain-restricted sharing)
- `compute.skipDefaultNetworkCreation`
- `compute.vmExternalIpAccess`
- `compute.requireOsLogin`
- `compute.requireShieldedVm`
- `compute.disableSerialPortAccess`
- `storage.publicAccessPrevention`
- `storage.uniformBucketLevelAccess`
- `gcp.restrictNonCmekServices`
- `gcp.resourceRestrictions`

!!! tip "Exam tips"
    - "Avoid duplicating users in Cloud Identity" points to Workforce Identity Federation.
    - GCDS alone does not sync passwords.
    - Super admins always sign in with Google credentials, not the IdP.
    - Users from the IdP cannot sign in after setup. Check attribute conditions and mappings.
    - If a workload option uses Workload Identity Federation, the answer that downloads keys is usually wrong.
    - `iam.disableServiceAccountKeyCreation` does not delete existing keys.
    - A deny policy beats an allow binding.
    - Editor can create service account keys. Do not give it to workloads.

Labs: [[security-labs]] (Implement Cloud Security Fundamentals, Managing Security in Google Cloud).

[Next: Network security](02-network-security.md)
