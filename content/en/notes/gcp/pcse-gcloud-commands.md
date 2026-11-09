---
title: Gcloud Commands
category: GCP
description: Part of [[pcse-home|PCSE Home]]. Command families to practice before
  the exam. Assume PCA-level gcloud fluency. Verify exact syntax against docs as you
  go; the exam is multiple choice, so recognizing
tags:
- gcp
- security
- pcse
---

<!-- imported from ObsidianVault/studies/PCSE/gcloud Commands.md. Edit the source, then run sync.py. -->

# Gcloud Commands

`gcp` `security` `pcse`

## gcloud Commands

Part of [[pcse-home|PCSE Home]]. Command families to practice before the exam. Assume PCA-level gcloud fluency. Verify exact syntax against docs as you go; the exam is multiple choice, so recognizing the right service and flag matters more than typing syntax.

```bash
# IAM conditions and deny
gcloud iam policies create --kind=denypolicies ...

# Access Context Manager
gcloud access-context-manager policies create
gcloud access-context-manager policies levels create
gcloud access-context-manager perimeters dry-run create

# Organization policies
gcloud org-policies describe
gcloud org-policies allow|enforce CONSTRAINT
gcloud org-policies set-policy POLICY.yaml   # supports dry-run spec

# Workload Identity Federation
gcloud iam workload-identity-pools create
gcloud iam workload-identity-pools providers create-oidc

# Keys (Cloud KMS)
gcloud kms keyrings create
gcloud kms keys create --rotation-period=30d
gcloud kms keys versions import

# Cloud Armor
gcloud compute security-policies create
gcloud compute security-policies rules create --expression=...

# NGFW policies (Cloud NGFW)
gcloud compute network-firewall-policies rules create
gcloud compute org-firewall-policies create

# SCC (Security Command Center)
gcloud scc findings list
gcloud scc muteconfigs create
gcloud scc notifications create

# Sensitive Data Protection
# Mostly API/console driven; know the resource shape: inspect templates,
# deidentify templates, job triggers, discovery profiles

# AI workload security (Model Armor, Vertex AI controls) is likewise
# API/console driven; know the resource shape: Model Armor templates,
# endpoints, and filters

# Binary Authorization
gcloud container binauthz policy import|export
gcloud container binauthz attestations create

# VM Manager / OS Config
gcloud compute os-config patch-jobs execute
gcloud compute os-config patch-deployments create

# DNSSEC and private zones (Cloud DNS)
gcloud dns managed-zones create --dnssec-state=on
gcloud dns managed-zones create --visibility=private
```

Related: Terraform commands if you manage config as code.
