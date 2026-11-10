---
title: Final Week Checklist
category: GCP
description: Part of PCSE Home. Work through this the week before the exam. Check
  items off in Obsidian.
tags:
- gcp
- security
- pcse
---

<!-- imported from ObsidianVault/studies/PCSE/Final Week Checklist.md. Edit the source, then run sync.py. -->

# Final Week Checklist

`gcp` `security` `pcse`

## Final Week Checklist

Part of [[pcse-home|PCSE Home]]. Work through this the week before the exam. Check items off in Obsidian.

- [ ] Can explain GCDS vs SSO vs WIF vs Cloud Identity accounts, and when super admins bypass SSO. See [[1-configuring-access|1 - Configuring Access]].
- [ ] Can build (on paper) a WIF provider config: pool, provider, attribute mapping, attribute condition.
- [ ] Can recite the SA decision tree and the Token Creator vs Service Account User distinction.
- [ ] Know 5 org policy constraints by name plus dry-run behavior.
- [ ] Can trace an access decision through allow binding, deny policy, [[iam|IAM]] condition, and [[vpc-service-controls|VPC-SC]] in order.
- [ ] Know the three firewall configuration layers and where L7/TLS inspection lives. See [[cloud-ngfw|Cloud NGFW]].
- [ ] Can configure VPC-SC in dry run, write an ingress and egress rule, and explain bridges.
- [ ] Know the PGA/restricted VIP/PSC/[[cloud-nat|NAT]] matrix and the DNS zone pattern for [[private-google-access-vs-psc|private Google access]].
- [ ] Know CMEK key states, rotation semantics, and the EKM decision trigger. See [[cloud-kms|Cloud KMS]].
- [ ] Know SDP inspection vs de-identify templates, FPE, and discovery profiles.
- [ ] Know all audit log types, which are on by default, and how to sink logs with aggregated sinks. See [[cloud-logging|Cloud Logging]].
- [ ] Know SCC tiers, the built-in detectors, and continuous export targets. See [[security-command-center|Security Command Center]].
- [ ] Know [[binary-authorization|Binary Authorization]] policy structure for [[gke|GKE]] and [[cloud-run|Cloud Run]].
- [ ] Know Assured Workloads, Access Transparency vs Access Approval, and the shared responsibility split. See [[5-compliance|5 - Compliance]].
- [ ] Know encryption in transit: SSL policies, IPsec on HA VPN, MACsec on Dedicated Interconnect.
- [ ] Can name the three AI layers (data, model, interaction) and the control for each, the IaaS vs PaaS training split, and the Model Armor use cases for [[gemini|Gemini]] Enterprise Agent Platform.
- [ ] Know the Vertex AI specifics: dedicated VPC-SC perimeters, public endpoint gated by an access level, PSC endpoints, custom route exports.
- [ ] Can recite the decision rules in [[cheat-sheets|Cheat Sheets]] without looking.
- [ ] Practiced the command families in [[gcloud-commands|gcloud Commands]].
- [ ] Completed 2 timed practice exams at 80%+.

Then book the exam. Good luck.
