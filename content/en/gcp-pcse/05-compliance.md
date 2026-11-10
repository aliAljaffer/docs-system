# 5. Compliance

**Goal:** Map a compliance requirement to a Google control and to the right responsibility.

## Shared responsibility

| Google is responsible for | You are responsible for |
|---|---|
| Physical facilities and hardware | [[iam]] and access |
| Hypervisor and infrastructure | Data classification and protection |
| Managed service internals | Configuration and usage of services |

- Use this split to answer "who does what" questions.
- Using a compliant service does not make your operations compliant. You stay responsible for how you use the service and your data.
- Evaluate the split against regulations, security standards, customer or vendor requirements, and the workload type.
- Choosing HIPAA-eligible services is your job.

## Assured Workloads

- Assured Workloads creates a folder with a compliance regime enforced on it. Regimes include FedRAMP Moderate and High, IL2, IL4, IL5, CJIS, HIPAA-style controls, and US or EU regions and support (Data Boundary).
- It restricts Google personnel access, data location, and allowed services. It blocks non-compliant regions and products.
- It works at the folder level. Create it with the wizard. Create other projects inside that folder.
- Blueprints are Policy-as-Code templates for each regime.
- Setup steps: select the regime, set data location with org policies, and choose key management.

## Access Transparency and Access Approval

| | Access Transparency | Access Approval |
|---|---|---|
| What it does | Logs, with a justification, each time Google support accesses your content. Logs arrive in near real time. | Requires your approval before Google can act on an access request. |
| Requirements | An organization, an eligible support tier, linked billing, and `roles/axt.admin` | Access Transparency enabled, and `roles/accessapproval.configEditor` |
| Notes | Disabling it needs Google support. | Requests arrive by email or [[pub-sub|Pub/Sub]]. Approve in the console or API. Requests are signed with a Google-managed key by default, or a customer-managed key from Cloud KMS or EKM. |

- Access Transparency is set on a project page, but it applies to the whole organization.
- Access Transparency logs include the resource, action, time, reason, accessor location, and job category.
- Enable Access Approval per service or for all services. Set it at the project, folder, or organization level.
- Approve time-sensitive requests quickly.

## Regionalization

- Use the resource location constraints `gcp.resourceLocations` and `gcp.resourceRestrictions`. Combine `gcp.resourceRestrictions` with [[vpc-service-controls]].
- Use regional buckets, datasets, and [[cloud-kms]] keys.
- Data residency regimes include the EU Data Boundary.

## Scope and evidence

1. Decide which organization nodes fall under each regulation.
2. Isolate in-scope data with folders, Assured Workloads, and perimeters.
3. Map your audit log coverage to the evidence the regulation needs.
4. Keep logs long enough. Use sinks and bucket lock for retention. See [[cloud-logging]].
5. Use Compliance Manager for audit reports, statements of applicability, and certificates. Filter offerings by country and industry.

## Requirement to control map

| Requirement | Google control |
|---|---|
| Data residency | Assured Workloads and resource location org policy |
| Oversight of Google personnel access | Access Transparency and Access Approval |
| Evidence and audit | [[cloud-logging]] audit logs (including Data Access), log sinks with long retention, and bucket lock |
| Segmentation | [[vpc-service-controls]], Shared [[vpc]], network firewall policies, and Access Context Manager |
| Regime-specific guarantees | Assured Workloads regime |

!!! tip "Exam tips"
    - A compliant service does not make you compliant. The customer still owns use and data.
    - Assured Workloads is set at the folder level.
    - Access Transparency shows access after it happens. Access Approval asks you before it happens.
    - Disabling Access Transparency needs Google support.
    - Regulation questions usually point to one control in the map above. Pick the control that matches the requirement.

Labs: [[security-labs]].

[Next: gcloud commands](06-gcloud-commands.md)
