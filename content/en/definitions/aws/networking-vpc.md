---
title: vpc
category: AWS
description: 'AWS note: Vpc.'
tags:
- aws
- services
---


# vpc

### Virtual Private Cloud (VPC)
A Virtual Private Cloud (VPC) is a logically isolated section of the AWS network where you launch your AWS resources. It uses Classless Inter-Domain Routing ([[cidr|CIDR]]) notation to specify a range of IP addresses.

**Subnets** are smaller partitions within your VPC's that also utilize IP address ranges. Must have smaller IP range than your VPC. **Can be either public or private.**
