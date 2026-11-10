---
title: Ec2-ccp
category: AWS
description: EC2 is the flagship AWS compute service that allows to launch virtual
  machines, called instances.
tags:
- aws
- services
---

<!-- imported from ObsidianVault/studies/cloud-architecht/services/compute/ec2-ccp.md. Edit the source, then run sync.py. -->

# Ec2-ccp

`aws` `services`

EC2 is the flagship [[aws-compute|AWS compute]] service that allows to launch virtual machines, called instances.

- A VM is an emulation of a physical computer using software
- Multiple VM's can run on the same physical server, allowing you to share costs of that server with other customers
You can configure EC2 instances to meet any business requirements.

**Amazon Machine Images (AMI)** are templates for creating EC2 instances.

Configurable components:
- RAM
- CPU
- Network Bandwidth
- OS

## Instance Types

- General Purpose
- Compute optimized (High processing power needed)
- Memory optimized (Large data sets in memory needed)
- Accelerated optimized (Machine Learning)
- Storage optimized (Fast speeds for read/write on the local storage)

## Tenancy Types

What allows for cost savings between customers.

1. Shared **(default)**- Multiple AWS accounts are using the same physical hardware
2. Dedicated instance - Instance runs on a single-tenant hardware
3. Dedicate host (Most expensive) - Instance runs on its own physical server that you can control and configure

## Pricing models

1. **On-demand** **(default)** - Pay as you go, hourly rate
2. **Reserved instances**
	1. Best for apps with steady, predictable usage
	2. Can commit to 1 or 3 years of usage
	3. Can pay upfront, partial upfront, or no upfront.
	4. Can be shared between accounts, and if not being used you can sell your reserves instance on AWS [[financial-management-marketplace|marketplace]].
3. **Spot instances**
	1. Unused compute capacity you can buy from AWS with up to 90% savings when compared to on demand
	2. Designed for workloads that have flexible start and end times because **AWS can take back spot computing capacity at any time if its needed by other on-demand services**.
