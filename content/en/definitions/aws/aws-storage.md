---
title: Aws storage
category: AWS
description: 'AWS note: Aws storage.'
tags:
- gcp
---


# Aws storage

`gcp`

- Storage is different from database in that with storage, you have more flexibility on how data you store is formatted.
- Best way to keep and analyze log files is in a storage solution like [[storage-s3|S3]].
- Can **automate** uploads/removals of objects to your storage.
## Types of storage services
- Elastic Block Storage ([[storage-ebs|EBS]])
	- Block storage
	- Most compatible with [[compute-ec2-ccp|ec2-ccp]] instances
- Elastic File System ([[storage-efs|EFS]])
	- File storage
	- **Useful when multiple users need access to the same drive**
- Simple Storage Service ([[storage-s3|S3]])
	- Object storage
	- Offers virtually unlimited amounts of storage
	- Most widely used AWS storage service
- [[migration-aws-snow-family|AWS Snow family]]
	- Used to migrate data in or out of AWS cloud.
- [[storage-storage-gateway|storage gateway]]
