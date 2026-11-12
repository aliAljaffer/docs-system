---
title: Ec2-ccp
category: AWS
description: EC2 is the flagship AWS compute service that allows to launch virtual
  machines, called instances.
tags:
- aws
- services
---


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

| Tenancy | Hardware | Note |
|---|---|---|
| Shared **(default)** | Multiple AWS accounts are using the same physical hardware | - |
| Dedicated instance | Instance runs on a single-tenant hardware | - |
| Dedicated host | Instance runs on its own physical server that you can control and configure | Most expensive |

## Pricing models

| Model | Billing and commitment | Best for | Notes |
|---|---|---|---|
| **On-demand** **(default)** | Pay as you go, hourly rate | - | - |
| **Reserved instances** | Commit to 1 or 3 years of usage. Pay upfront, partial upfront, or no upfront | Apps with steady, predictable usage | Can be shared between accounts. If not used, you can sell your reserved instance on AWS [[financial-management-marketplace|marketplace]] |
| **Spot instances** | Unused compute capacity you can buy from AWS | Workloads that have flexible start and end times | Up to 90% savings when compared to on demand. **AWS can take back spot computing capacity at any time if its needed by other on-demand services** |
