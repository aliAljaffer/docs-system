---
title: 5 - Compliance
category: GCP
description: Part of PCSE Home. Official exam guide section 5.1. You know compliance
  concepts from PCA; PCSE adds Google-specific controls.
tags:
- gcp
- security
- pcse
---

<!-- imported from ObsidianVault/studies/PCSE/5 - Compliance.md. Edit the source, then run sync.py. -->

# 5 - Compliance

`gcp` `security` `pcse`

## 5 - Supporting Compliance Requirements (~11%)

Part of [[pcse-home|PCSE Home]]. Official exam guide section 5.1. You know compliance concepts from PCA; PCSE adds Google-specific controls.

- **Shared responsibility model (in depth):** map a control question ("who patches the OS on [[compute-engine|GCE]] vs [[cloud-run|Cloud Run]]?") to responsibility; be able to say what is Google's responsibility (physical, hypervisor, managed service internals) vs yours (IAM, data, config).
- **Assured Workloads:** creates a folder with enforced compliance regime (FedRAMP Moderate/High, IL2/4/5, CJIS, HIPAA-like controls, US/EU regions and support, Data Boundary): restricts Google personnel access, data location, and allowed services; blocks non-compliant regions/products automatically. It operates at the **folder** level and is created via a wizard; other projects must be created inside it.
- **Access Transparency:** logs (with justification) whenever Google support accesses your content; near real-time logs; available with eligible support tiers.
- **Access Approval:** you must approve access requests before Google can act; pairs with Access Transparency; control who receives approval requests.
- **Data and services regionalization:** resource location org policy (`gcp.resourceRestrictions` with [[vpc-service-controls|VPC-SC]], `gcp.resourceLocations`), regional buckets/datasets/keys; data residency regimes (EU Data Boundary etc.).
- **Determining scope:** which org nodes are in scope for a regulation; isolate with folders + Assured Workloads + perimeters; map audit log coverage to evidence needs.
- **Mapping requirements to controls:** exam questions give a regulation flavor (HIPAA, FedRAMP, CJIS, GDPR residency) and ask which Google control satisfies it. Quick map:
	- Data residency -> Assured Workloads + resource locations org policy.
	- Google personnel access oversight -> Access Transparency + Access Approval.
	- Evidence/audit -> Cloud Audit Logs (incl. Data Access) + log sinks with long retention + bucket lock. See [[cloud-logging|Cloud Logging]].
	- Segmentation -> [[vpc-service-controls|VPC-SC]], Shared VPC, NGFW policies, ACM.
	- Regime-specific guarantees -> Assured Workloads regime.

**Additional facts:**
- Trap: **using a compliant service does not make your operations compliant**; you stay responsible for usage and data.
- Evaluate the shared responsibility model against regulatory obligations, security standards and risk plan, customer/vendor requirements, and workload type.
- HIPAA example: choosing HIPAA-eligible services is the customer's job.
- Assured Workloads setup: select the regime, set data location with org policies, choose key management; enforces that data and resources stay in the selected region; blueprints are Policy-as-Code templates per regime.
- Access Transparency: configured on a project page but applies org-wide; needs an org, an eligible support tier, billing linked, `roles/axt.admin`; **disabling requires Google support**; log fields include resource, action, time, reason, accessor location and job category.
- Access Approval: requests arrive by email or Pub/Sub; approve via console or API; requests are signed, Google-managed key by default or customer-managed via [[cloud-kms|Cloud KMS]]/EKM; enable per service or all, at project/folder/org; requires AT enabled + `roles/accessapproval.configEditor`; approve time-sensitive requests promptly.
- Evidence: Compliance Reports Manager (now the Compliance Manager experience) provides audit reports, statements of applicability, certificates; filter offerings by country and industry to find in-scope services.
