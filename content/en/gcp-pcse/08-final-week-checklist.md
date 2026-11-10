# 8. Final week checklist

**Goal:** Confirm the key facts the week before the exam.

Work through this list in the final week. Check each item only when you can explain it without notes.

- [ ] Explain GCDS, SSO, Workforce Identity Federation, and Cloud Identity accounts. State when super admins bypass SSO. See [Lesson 1](01-configuring-access.md).
- [ ] Sketch a Workforce Identity Federation provider: pool, provider, attribute mapping, and attribute condition.
- [ ] Recite the service account decision tree. Explain Token Creator and Service Account User.
- [ ] Name 5 org policy constraints and explain dry run mode.
- [ ] Trace an access decision through an allow binding, a deny policy, an IAM condition, and [[vpc-service-controls|VPC Service Controls]], in that order.
- [ ] Name the three firewall layers. Say where L7 and TLS inspection live. See [Lesson 2](02-network-security.md).
- [ ] Configure [[vpc|VPC]] Service Controls in dry run. Write an ingress rule and an egress rule. Explain bridges.
- [ ] Explain the matrix of Private Google Access, the restricted VIP, PSC, and [[cloud-nat|Cloud NAT]]. Name the DNS zone pattern for private Google access. See [Lesson 2](02-network-security.md).
- [ ] Explain CMEK key states, rotation behavior, and when to choose EKM. See [Lesson 3](03-data-protection.md).
- [ ] Explain Sensitive Data Protection inspection and de-identify templates, FPE, and discovery profiles.
- [ ] Name all audit log types. State which are on by default. Explain how to sink logs with aggregated sinks. See [Lesson 4](04-managing-operations.md).
- [ ] Explain SCC tiers, the built-in detectors, and continuous export targets.
- [ ] Explain the Binary Authorization policy structure for GKE and [[cloud-run|Cloud Run]].
- [ ] Explain Assured Workloads, Access Transparency compared with Access Approval, and the shared responsibility split. See [Lesson 5](05-compliance.md).
- [ ] Explain encryption in transit: SSL policies, IPsec on HA VPN, and MACsec on Dedicated Interconnect.
- [ ] Name the three AI layers (data, model, interaction) and the control for each. State the IaaS and PaaS training split and the Model Armor use cases.
- [ ] Explain [[vertex-ai|Vertex AI]] controls: dedicated VPC Service Controls perimeters, a public endpoint behind an access level, PSC endpoints, and custom route exports.
- [ ] Recite the decision rules in the [cheat sheet](07-cheat-sheet.md) without notes.
- [ ] Practice the command families in [Lesson 6](06-gcloud-commands.md).
- [ ] Complete 2 timed practice exams at 80% or higher.

!!! tip "Exam tips"
    - Review every wrong or guessed answer before the exam. Check each one against the official exam guide.
    - Take another timed exam only after you close the gaps from the first one.

[Back to index](index.md)
