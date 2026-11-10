# 6. gcloud commands

**Goal:** Recognize the command families for security tasks.

The exam is multiple choice. Recognize the right service and flag more than exact syntax. Verify syntax in the official docs when you practice.

## IAM deny policies

```bash
gcloud iam policies create --kind=denypolicies ...
```

## Access Context Manager

```bash
gcloud access-context-manager policies create
gcloud access-context-manager policies levels create
gcloud access-context-manager perimeters dry-run create
```

## Organization policies

```bash
gcloud org-policies describe
gcloud org-policies allow|enforce CONSTRAINT
gcloud org-policies set-policy POLICY.yaml
```

`set-policy` accepts a dry-run spec.

## Workload Identity Federation

```bash
gcloud iam workload-identity-pools create
gcloud iam workload-identity-pools providers create-oidc
```

## Cloud KMS

```bash
gcloud kms keyrings create
gcloud kms keys create --rotation-period=30d
gcloud kms keys versions import
```

## Cloud Armor

```bash
gcloud compute security-policies create
gcloud compute security-policies rules create --expression=...
```

## Cloud NGFW

```bash
gcloud compute network-firewall-policies rules create
gcloud compute org-firewall-policies create
```

## Security Command Center

```bash
gcloud scc findings list
gcloud scc muteconfigs create
gcloud scc notifications create
```

## Sensitive Data Protection

Sensitive Data Protection is mostly API and console driven. Know the resource types: inspect templates, de-identify templates, job triggers, and discovery profiles.

## AI workload security

Model Armor and [[vertex-ai|Vertex AI]] controls are also mostly API and console driven. Know the resource types: Model Armor templates, endpoints, and filters.

## Binary Authorization

```bash
gcloud container binauthz policy import|export
gcloud container binauthz attestations create
```

## VM Manager

```bash
gcloud compute os-config patch-jobs execute
gcloud compute os-config patch-deployments create
```

## Cloud DNS

```bash
gcloud dns managed-zones create --dnssec-state=on
gcloud dns managed-zones create --visibility=private
```

!!! tip "Exam tips"
    - Know which service owns each command family.
    - Know the flag that turns on a feature, such as `--dnssec-state=on` or `--rotation-period`.
    - Sensitive Data Protection and Model Armor use the API and console more than gcloud.

[Next: Cheat sheet](07-cheat-sheet.md)
