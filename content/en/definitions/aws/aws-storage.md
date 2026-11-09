---
title: Aws storage
category: AWS
description: 'AWS note: Aws storage.'
tags:
- gcp
---

<!-- imported from ObsidianVault/studies/cloud-architecht/unsorted/aws storage.md. Edit the source, then run sync.py. -->

# Aws storage

`gcp`

- Storage is different from database in that with storage, you have more flexibility on how data you store is formatted.
- Best way to keep and analyze log files is in a storage solution like S3.
- Can **automate** uploads/removals of objects to your storage.
## Types of storage services
- Elastic Block Storage (EBS)
	- Block storage
	- Most compatible with ec2-ccp instances
- Elastic File System (EFS)
	- File storage
	- **Useful when multiple users need access to the same drive**
- Simple Storage Service (S3)
	- Object storage
	- Offers virtually unlimited amounts of storage
	- Most widely used AWS storage service
- AWS Snow family
	- Used to migrate data in or out of AWS cloud.
- storage gateway
