---
title: Efs
category: AWS
description: Elastic File System - a file system that grows or shrinks based on usage.
  Commonly mounted on ec2-ccp, but can also be mounted on containers or Lambda functions.
tags:
- aws
- services
---


# Efs

`aws` `services`

Elastic File System - a file system that grows or shrinks based on usage. Commonly mounted on [[compute-ec2-ccp|ec2-ccp]], but can also be mounted on containers or [[compute-lambda|Lambda]] functions.

## Storage classes

| Class | Access pattern | Durability | Cost |
|---|---|---|---|
| Standard | Regularly accessed files | - | Most expensive |
| Standard IA | Infrequently accessed files | - | - |
| One zone | Frequently accessed | Doesn't need [[high-durability|high durability]] | - |
| One zone IA | Infrequent access | Less durable | Cheapest |
