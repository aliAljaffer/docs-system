---
title: Organizations
category: AWS
description: Automates account creation and assignment of permissions, as well as
  infrastructure deployment, when available.
tags:
- aws
- services
---

<!-- imported from ObsidianVault/studies/cloud-architecht/services/management-and-governance/organizations.md. Edit the source, then run sync.py. -->

# Organizations

`aws` `services`

**AWS Organizations** is a service that allows the creation of new AWS accounts tied to your business, and centrally manage billing, access, compliance, security, and share resources.
### Root master account
sits at the top of the organization.
### Organizational Units (OU)
Groups of AWS accounts that can be nested.
### Service Control Policies (SCP)
Act as guardrails for your organization, setting boundaries on what your accounts are able to do.
## Organizations vs. SCPs
Organizations are useful if you have a lot of different users or departments that need access to services. It can enable [[consolidated-billing|consolidated billing]]. Can see details pertaining to account costs. 

Automates account creation and assignment of permissions, as well as infrastructure deployment, when available.

SCPs set guardrails for all accounts in your organization (not users or roles.)

**They only filter, and never ADD permissions**, so still need to use [[security-user-and-identity-management|IAM policies]] as well. 

# ****Avoid attaching SCPs to the root account of the organization!****
