---
title: Vpc
category: AWS
description: 'AWS note: Vpc.'
tags:
- aws
- services
---


# Vpc

`aws` `services`

### Virtual Private Cloud (VPC)
...is logically isolated section of the AWS network where you launch your AWS resources. Uses [[cidr|CIDR]] notation to specify a range of IPs to be used.

**Subnets** are smaller partitions within your VPC's that also utilize IP address ranges. Must have smaller IP range than your VPC. **Can be either public or private.**
