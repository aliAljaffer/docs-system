---
title: Aws networking
category: AWS
description: 'AWS note: Aws networking.'
tags:
- gcp
---

<!-- imported from ObsidianVault/studies/cloud-architecht/unsorted/aws networking.md. Edit the source, then run sync.py. -->

# Aws networking

`gcp`

## Security Groups and NACLs
**Security groups** work at the __instance__ level ([[compute-ec2-ccp|ec2-ccp]])
- Implicitly **denies** all traffic (DENY ONLY)
- **Work off of allow rules only** (stateful)
Network Access Control List work at **subnet** level. ([[vpc|VPC]])
- Virtual firewall at the **network** level
- **Uses allow and deny rules** (stateless)
**Deny rules have higher precedence than allow.**
## [[networking-vpn|VPN]] and [[networking-direct-connect|Direct Connect]]
Virtual Private Network (VPN) is generally the equivalent to an on-premise version of VPC. Provides an isolated secure environment to access resources. Can also establish a VPN between your on-premise resources and the AWS cloud.

**[[networking-direct-connect|AWS Direct Connect]]** allows you to create a direct, **physical** connection to AWS from on-premise where your traffic never touches the public internet.

[[networking-api-gateway|api gateway]]
[[networking-cloudfront|cloudfront]]
[[networking-route53|route53]]
[[vpc]]
