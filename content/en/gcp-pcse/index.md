# Professional Cloud Security Engineer (PCSE) course

This short course covers the Google Cloud Professional Cloud Security Engineer exam. It explains which control solves a security problem, where you configure it, and how it fails.

## What the certification covers

The PCSE exam tests how you design, deploy, and operate secure Google Cloud environments. The course assumes Professional Cloud Architect (PCA) level knowledge of [[vpc]], IAM, and core services. It tests Google product names and configuration options, not general security theory.

## Exam facts

| Item | Detail |
|---|---|
| Length | 2 hours |
| Questions | 50 to 60, multiple choice and multiple select |
| Cost | $200 USD |
| Delivery | Online proctored or test center |
| Languages | English, Japanese |
| Validity | 2 years. Retake the full exam to renew. |
| Retake policy | 14 days after fail 1, 60 days after fail 2, 365 days after fail 3 |
| Recommended background | 3+ years in industry, 1+ year on Google Cloud |
| Case studies | None |

- Select-all questions give no partial credit.
- Test takers report forms as short as 40 questions in 2025.
- Online proctoring needs a second camera, such as a phone behind you.
- You get no breaks, food, or drinks.

Official page: https://cloud.google.com/learn/certification/cloud-security-engineer

Time budget: about 2 minutes per question.

## Exam domains

| # | Domain | Weight | Lesson |
|---|---|---|---|
| 1 | Configuring access | About 25% | [Lesson 1](01-configuring-access.md) |
| 2 | Securing communications and boundary protection | About 22% | [Lesson 2](02-network-security.md) |
| 3 | Ensuring data protection | About 23% | [Lesson 3](03-data-protection.md) |
| 4 | Managing operations | About 19% | [Lesson 4](04-managing-operations.md) |
| 5 | Supporting compliance requirements | About 11% | [Lesson 5](05-compliance.md) |

Domains 1 to 3 make up about 70% of the exam. Domains 4 and 5 make up about 30%. Do not skip them.

Weights are approximate. The official exam guide is the source of truth for scope and current weights.

### Priority topics

The official exam guide covers these topics. This course covers them only in outline. Read the official docs for each one.

- **Domain 1:** Workforce Identity Federation, [[iam|IAM]] Conditions and deny policies, Policy Intelligence.
- **Domain 2:** VPC Service Controls, Private Service Connect, Cloud NAT, [[cloud-dns|Cloud DNS]] security, Cloud NGFW application-layer inspection, Certificate Authority Service, Secure Web Proxy.
- **Domain 3:** [[bigquery|BigQuery]] and Cloud SQL access controls, instance metadata, external key manager (EKM), Confidential Computing, encryption in transit, securing AI workloads.
- **Domain 4:** current network detection and logging options, log access controls, aggregated sinks, image hardening, VM patch management, current [[security-command-center|Security Command Center]] capabilities.
- **Domain 5:** Assured Workloads, Access Transparency, Access Approval, regionalization, mapping controls to requirements.

### Securing AI workloads is in scope

Objective 3.3 has three parts: security and privacy controls for AI and ML systems, security requirements for IaaS-hosted and PaaS-hosted training, and security controls for the Gemini Enterprise Agent Platform. This course gives an overview in [Lesson 3](03-data-protection.md). Use the official docs for [[vertex-ai]] and [[gemini]].

Test takers report that AI and Vertex AI content makes up to a quarter of some exam forms. Treat objective 3.3 as a priority.

## Study plan

1. Study lessons 1 to 5 in order.
2. For each control, learn three things: how you configure it, what it protects, and how it fails.
3. For each role-play scenario, state the threat, the control, where to apply it, and how to verify it.
4. Read the official docs for each priority topic.
5. Practice the scenario technique below and the decision rules in [Lesson 7](07-cheat-sheet.md).
6. Take a timed 2-hour practice exam.
7. Review every wrong or guessed answer against the current exam guide.
8. Repeat weak topics. Take another timed exam only after you close the gaps.
9. Finish with the [final week checklist](08-final-week-checklist.md).

## Scenario questions

- Several options often work. A constraint keyword picks the answer, such as "most secure", "minimizes cost", or "least operational overhead".
- Find the ask first. Then match the exact Google product, feature, role, or constraint name.
- Remove wrong options first. When two remain, the more specific, more managed, or more native control is often correct.

## Lessons

| # | Lesson | Goal |
|---|---|---|
| 1 | [Configuring access](01-configuring-access.md) | Control identities, roles, service accounts, and the resource hierarchy. |
| 2 | [Network security](02-network-security.md) | Control traffic with firewalls, load balancers, [[cloud-armor|Cloud Armor]], and private access. |
| 3 | [Data protection](03-data-protection.md) | Find sensitive data, control data access, and manage encryption keys. |
| 4 | [Managing operations](04-managing-operations.md) | Scan and gate workloads, collect logs, and detect threats. |
| 5 | [Compliance](05-compliance.md) | Map regulations to Google controls and responsibilities. |
| 6 | [gcloud commands](06-gcloud-commands.md) | Recognize the command families for security tasks. |
| 7 | [Cheat sheet](07-cheat-sheet.md) | Apply decision rules to scenario questions. |
| 8 | [Final week checklist](08-final-week-checklist.md) | Confirm key facts before exam day. |

[Next: Configuring access](01-configuring-access.md)
