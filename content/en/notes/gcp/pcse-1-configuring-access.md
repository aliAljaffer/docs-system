---
title: 1 - Configuring Access
category: GCP
description: Part of [[pcse-home|PCSE Home]]. Official exam guide sections 1.1 to
  1.5.
tags:
- gcp
- security
- pcse
---

<!-- imported from ObsidianVault/studies/PCSE/1 - Configuring Access.md. Edit the source, then run sync.py. -->

# 1 - Configuring Access

`gcp` `security` `pcse`

## 1 - Configuring Access (~25%)

Part of [[pcse-home|PCSE Home]]. Official exam guide sections 1.1 to 1.5.

### 1.1 Managing Cloud Identity

**Key concepts:**

- **Google Cloud Directory Sync (GCDS):** on-prem tool that syncs users and groups from AD/LDAP into Cloud Identity using the Admin SDK. Runs on a schedule (Task Scheduler/cron). It syncs identity data, not passwords by default; password sync is a separate tool (Google Password Sync). GCDS maps AD groups to Cloud Identity groups, and you schedule it, you do not make it event-driven.
- **SSO with a third-party IdP:** SAML profile configuration in the Admin console. You can enable SSO for specific org units or groups. Critical trap: **super admins always authenticate with Google credentials, not the third-party IdP** (they bypass SSO by design). Keep the local password store for super admins.
- **Super administrator account hygiene:** maintain at least 2 (break-glass), but no more than a handful. Protect with hardware security keys and enrollment-conditional 2SV. Store recovery codes offline. Do not use super admins for day-to-day work. Exempt them from any "lost access" cleanup automation.
- **User lifecycle automation:** onboarding via GCDS or Admin SDK/Cloud Identity API; offboarding via Workforce Identity Federation invalidation, suspension, and eventually deletion. Drive permissions through group membership so that removing membership revokes access everywhere.
- **Programmatic administration:** Cloud Identity API and Admin SDK Directory API for user/group management at scale.
- **Workforce Identity Federation (external IdP):** lets an external IdP (Okta, Azure AD/Entra, ADFS) authenticate users who then get federated into Google Cloud without creating Cloud Identity accounts. Key pieces: workforce identity pool, OIDC or SAML provider, attribute mapping, attribute conditions (filter which users can federate). WIF avoids managing duplicate identities and bypasses the Cloud Identity per-user cost, but it does not support features tied to Cloud Identity accounts (2SV policies, password policies, super admin model). Session duration and employee_vs_workforce principal type matter for questions.

**Traps:**
- "Which identity strategy avoids duplicating users in Cloud Identity?" -> Workforce Identity Federation.
- "Users from the IdP cannot sign in after configuration" -> check attribute conditions and attribute mappings.
- "Admin wants password sync from AD" -> GCDS alone does not sync passwords; Google Password Sync does.

**Additional facts:**
- Cloud Identity Free vs Premium: Premium adds endpoint management (device approval, block/wipe, context-aware access).
- A managed account has exactly one identity, the organization-domain email; alias and recovery emails cannot sign in.
- Federation: Google is the service provider; the IdP only authenticates, Google authorizes. Cloud Identity can act as IdP and SP at the same time.
- GCDS is one-way (AD/LDAP stays authoritative), supports a dry run before executing, and uses a dedicated Google identity with Super Admin for separation of duties.
- The organization resource is created automatically at the first project or billing account; one organization per Cloud Identity account, bound to one domain.
- On organization creation, all domain users automatically get `projectCreator` and `billing.creator` at org level.
- User lifecycle: provisioning connectors (full lifecycle) vs JIT provisioning (sign-in only, no deprovisioning).
- Super admin setup order: enforce 2SV, add a non-personal recovery email, delegate Organization Admins plus a group, keep the super admin out of that group.
- Super Admin (Cloud Identity/Workspace) and Organization Administrator (IAM) are deliberately separate roles: separation of duties.

### 1.2 Managing service accounts

This is a favorite exam topic. Know the decision tree cold:

| Scenario | Best practice answer |
|---|---|
| Workload on GKE needs Google API access | Workload Identity Federation for GKE (Kubernetes SA binding) |
| Workload on another cloud or on-prem needs access | Workload Identity Federation (keyless, STS token exchange) |
| Human or workload temporarily needs a SA's identity | Impersonation (`roles/iam.serviceAccountTokenCreator`) |
| Short-term credential needed for signing URLs/JWTs | Short-lived credentials via Token Creator + `signBlob`/`signJwt` |
| Legacy system cannot use any of the above | User-managed key, but: restrict with org policy `iam.disableServiceAccountKeyCreation`, rotate, monitor with SCC and Cloud Audit Logs |

**Must-know details:**
- **Default service accounts** (Compute Engine default SA, App Engine default SA): have Editor on the project. Mitigation: org policy `iam.automaticIamGrantsForDefaultServiceAccounts` **prevents the automatic Editor grant for new default SAs, but is not retroactive**, existing grants remain; replace default SAs with purpose-built SAs; disable key creation for default SAs.
- **Key lifecycle:** keys never expire (rotation is manual or scripted). Audit key usage via Data Access logs and SCC findings (weak/unused keys). Prefer disabling key upload via `iam.disableServiceAccountKeyUpload`.
- **Impersonation chains:** you can chain (SA A impersonates B impersonates C). Keep the two roles straight: **Service Account User** = act as the SA (attach to resources, run as), **Token Creator** = mint tokens for the SA (impersonation). The caller needs Token Creator on the target SA, and anyone treating an SA as a resource (attaching it to a VM, running jobs as it) needs Service Account User on it.
- **Short-lived credentials:** token lifetimes from ~1 min up to 12 hours (delegated chains reduce the max per hop). Never a standing credential.

**Traps:**
- WIF for GKE eliminates keys AND eliminates the need for exported key files; any answer involving downloading keys is usually wrong when a WIF option exists.
- `iam.disableServiceAccountKeyCreation` blocks key creation org-wide but does not delete existing keys.

**Additional facts:**
- Limits: 100 SAs per project; SA names are immutable (6-30 chars); a SA cannot move to another project after creation.
- A new SA has zero permissions: grant it a role, then grant users `serviceAccountUser`/`serviceAccountTokenCreator` on it; creating SAs needs `serviceAccountCreator`.
- Design pattern: centralized SAs (simple, one audit trail, larger blast radius) vs distributed per-app SAs (isolation, granular permissions, cost tracking).
- **Never store SA keys in Secret Manager**: an app that can authenticate to Secret Manager does not need a key.
- Editor trap: Editor cannot change IAM policies but CAN create or upload SA keys (privilege escalation path).
- Domain-wide delegation uses the `signJwt` API, never SA keys.
- Disable a SA before deleting it: disabling blocks credential minting and API calls while preserving role bindings.
- Impersonation mechanics: `--impersonate-service-account` (comma list = chain), `gcloud config set auth/impersonate_service_account`, and the ADC `--impersonate-service-account` flag; the console cannot impersonate.
- Impersonation tokens ship without refresh tokens; each chain hop needs Token Creator on the next SA.
- VMs are the only resource whose attached SA can change (stop the VM first); prefer `--scopes cloud-platform` plus IAM for control.
- Cross-project SA use: org policy `iam.disableCrossProjectServiceAccountUsage` is enforced by default.
- Audit key usage: Data Access logs with `resource.type=service_account`; the `serviceAccountKeyName` field identifies which machine used a key.
- Rotate keys every 90 days or sooner; there is no built-in rotation automation.
- WIF: pool at global location, OIDC provider with `--issuer-uri` + `--attribute-mapping`; grant `roles/iam.workloadIdentityUser` to `principalSet://.../attribute.repository/REPO`; attribute changes take up to 5 minutes.

### 1.3 Managing authentication

- **Password policy:** Admin console: minimum length, strength enforcement, expiration, reuse restrictions.
- **Session management:** session length controls for Cloud console (including "sign the user out after X hours"), which pairs with 2SV frequency settings.
- **2SV enforcement:** org-wide or per org unit; enforce with hardware security keys for privileged users (phishing-resistant). Enforcement grace period. Contexts: you can require 2SV only for specific contexts. See [[multi-factor-authentication|MFA]].
- **SAML vs OAuth:** SAML for enterprise SSO into Cloud Identity; OAuth for app-level delegated access (scoped tokens, refresh vs access tokens).

**Additional facts:**
- Defaults: password minimum length 8; web session 14 days; admin console session fixed at 1 hour.
- 2SV method ranking, most to least secure: security keys, Google prompt, Authenticator codes, backup codes, text/voice.
- 2SV enforcement levels: Any, Any except verification codes, Only security key; security-key codes are valid 5 minutes.
- Grace: an admin-generated backup code lets a user who lost their security key sign in; enrollment reports lag 48 hours.
- SAML config needs the IdP Entity ID, SSO URL, and certificate; the response must include `saml:Subject` and `saml:NameID`.

**Workspace security (reported on 2025 exams):**
- Cloud Identity is the identity backend for Google Workspace; the Admin console, password, 2SV, and SSO controls above apply to both.
- Workspace-specific controls to know by name: Drive external sharing settings and Trust rules, context-aware access for Workspace apps (reuses ACM access levels), Workspace data regions, Vault holds and retention for eDiscovery.

### 1.4 Managing and implementing authorization controls

- **Basic vs predefined vs custom roles:** you know this from PCA. PCSE adds: custom roles are org- or project-level, list permissions with `gcloud iam roles describe`, and cannot contain `*` in permissions.
- **Separation of duties:** split admin functions across distinct roles and people (Organization Admin, security admin, billing admin, network admin); keep Super Admin (Cloud Identity) and Organization Administrator (IAM) separate; PAM for time-bound elevation instead of standing admins.
- **IAM Conditions:** CEL expressions on bindings (`resource.name`, `resource.type`, `request.time`). One condition per binding; conditions do not work on all roles (basic owner role restriction); conditions evaluate on each access check.
- **IAM deny policies (v3):** take precedence over allow bindings. Attached at org, folder, or project level (not resource level). **Principals use v2-style identifiers: `principal://goog/subject/EMAIL` (individual user), `principalSet://goog/group/GROUP`, `principalSet://goog/cloudIdentityCustomerId/ID`. Individual users CAN be denied.** Permissions use the v2 format (`storage.googleapis.com/buckets.create`). "A deny rule and an allow rule both match" -> access denied.
- **ACLs vs IAM:** GCS legacy ACLs vs uniform bucket-level access (UBLA). Enforce UBLA via org policy `storage.uniformBucketLevelAccess`. Signed URLs work regardless.
- **Access Context Manager (ACM):** the backbone of context-aware access and VPC Service Controls.
	- *Access levels:* basic (IP ranges, device policy, region) and custom (CEL). Combined with IAP for context-aware access to apps.
	- *Service perimeters:* dry-run mode first, ingress rules (who can enter), egress rules (what can leave), perimeter bridges for cross-perimeter service communication.
- **Policy Intelligence tools (know them by name):**
	- *Policy Troubleshooter:* "why did principal X get Y on Z?" (allow and deny diagnosis).
	- *Policy Analyzer:* "who has access to what?" (effective access audit for a resource or principal).
	- *IAM Recommender:* suggests removing over-granted roles based on observed usage.
	- *Condition Simulator / role simulation:* validates proposed policy changes before applying.
	- *Essential Contacts:* route critical notifications to real people (security, technical, billing).
- **Privileged Access Manager (PAM):** just-in-time standing privilege removal. Grant = who + role + duration + justification, with optional multi-step approval workflows. Deployed at org/folder/project. "Organization wants to eliminate standing admin access but allow emergency elevation" -> PAM.
- **Group-based permissions:** grant roles to groups, never individuals; manage membership in Cloud Identity. Watch for questions about group nesting and external members.
- **Least privilege at each level:** org > folder > project > resource inheritance. Binding at a parent applies to all descendants; resource-level bindings do not propagate up. See [[principle-of-least-privilege|least privilege]].

**Additional facts:**
- IAM policy changes follow read-modify-write; the `etag` field prevents concurrent overwrites.
- Deny policy management roles: `roles/iam.denyAdmin` (manage), `roles/iam.denyReviewer` (view).
- **UBLA: after enabling, you have 90 days to revert before it becomes permanent**.
- IAM and ACLs are unaware of each other: either one granting access is enough; a single public-read object ACL exposes that object.
- ACM's access policy is the org-scoped container; ACM only describes rules, enforcement happens in VPC-SC, IAP, and IAM Conditions.
- Policy Intelligence extras: Activity Analyzer (last SA/key use), SA insights (unused 90 days), lateral movement insights (cross-project impersonation).

### 1.5 Defining the resource hierarchy

- **Folders and projects at scale:** naming conventions, automation via Terraform/Asset Inventory; keep the hierarchy shallow and purposeful (org > folders by business unit or environment > projects).
- **Organization policy service:** heavily tested.
	- Pre-built constraints to memorize: `iam.disableServiceAccountKeyCreation`, `iam.allowedPolicyMemberDomains` (domain-restricted sharing), `compute.skipDefaultNetworkCreation`, `compute.vmExternalIpAccess`, `compute.requireOsLogin`, `compute.requireShieldedVm`, `compute.disableSerialPortAccess`, `storage.publicAccessPrevention`, `storage.uniformBucketLevelAccess`, `gcp.restrictNonCmekServices`, `gcp.resourceRestrictions`.
	- **Custom organization policies:** CEL-based constraints defined with CustomConstraint, applied to supported services; use when no pre-built constraint fits.
	- **Dry run mode:** test org policy changes (audit mode) before enforcement; both pre-built and custom support it.
	- Hierarchy: constraints inherit down; cannot be relaxed by children (children can only tighten, except where list-constraint policy values allow reset). Know `enforce` vs `reset` vs `restoreDefault` semantics briefly.
- **Inheritance for access control:** IAM + org policy + VPC-SC all inherit differently; be able to reason about a three-level hierarchy (org/folder/project) and what applies at each level.

**Additional facts:**
- Org policies are resource-focused (what resources may do); IAM allow policies are identity-focused (who may act).
- Effective allow policy = union of the node's and all ancestors' policies; org policy inheritance is controlled by `inheritFromParent` (default true).
- Tags group resources for org-policy targeting; tags never apply to IAM allow policies.
- Hierarchy patterns: environment folders (small orgs), product folders (scaled agile), geography folders (multi-region compliance such as GDPR).
- Best practice: exactly one organization; do not map the corporate org chart onto the resource hierarchy.

**Labs:** Security Labs (Implement Cloud Security Fundamentals, Managing Security in Google Cloud).
