---
title: aws networking
category: AWS
description: 'AWS note: Aws networking.'
tags:
- gcp
---


# aws networking

`gcp`

AWS networking is the set of services and controls that connect, isolate, and secure AWS resources. This page covers security groups, network access control lists (network ACLs), Virtual Private Network (VPN), and Direct Connect.

## Security Groups and NACLs

| Attribute | Security group | Network ACL |
|---|---|---|
| Level | **Instance** ([[compute-ec2-ccp|ec2-ccp]]) | **Subnet** ([[vpc|VPC]]), virtual firewall at the **network** level |
| Rules | Allow rules only. Implicitly **denies** all other traffic | Allow and deny rules |
| State | Stateful | Stateless |

**Deny rules have higher precedence than allow.**
## [[networking-vpn|VPN]] and [[networking-direct-connect|Direct Connect]]
Virtual Private Network (VPN) is generally the equivalent to an on-premise version of VPC. Provides an isolated secure environment to access resources. Can also establish a VPN between your on-premise resources and the AWS cloud.

**[[networking-direct-connect|AWS Direct Connect]]** allows you to create a direct, **physical** connection to AWS from on-premise where your traffic never touches the public internet.

[[networking-api-gateway|api gateway]]
[[networking-cloudfront|cloudfront]]
[[networking-route53|route53]]
[[vpc]]
