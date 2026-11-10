---
title: Efs
category: AWS
description: Elastic File System - a file system that grows or shrinks based on usage.
  Commonly mounted on ec2-ccp, but can also be mounted on containers or Lambda functions.
tags:
- aws
- services
---

<!-- imported from ObsidianVault/studies/cloud-architecht/services/storage/efs.md. Edit the source, then run sync.py. -->

# Efs

`aws` `services`

Elastic File System - a file system that grows or shrinks based on usage. Commonly mounted on [[compute-ec2-ccp|ec2-ccp]], but can also be mounted on containers or [[compute-lambda|Lambda]] functions.

## Storage classes
- Standard - regularly accessed files, most expensive
- Standard IA - Infrequently accessed files
- One zone - Frequently accessed, but doesn't need [[high-durability|high durability]]
- One zone IA - Infrequent access, less durable, cheapest
