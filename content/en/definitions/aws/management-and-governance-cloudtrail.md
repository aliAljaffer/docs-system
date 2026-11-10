---
title: Cloudtrail
category: AWS
description: '"Track user activity and API usage on AWS and in hybrid and multicloud
  environments"'
tags:
- aws
- services
---


# Cloudtrail

`aws` `services`

"Track user activity and ****API**** usage on AWS and in hybrid and multicloud environments"
**AWS CloudTrail** is a service that enables governance, compliance, operational **auditing**, and auditing of your AWS account.
If asked how to track API calls or user access => CloudTrail
Monitors API calls:
- Where - source IP
- When - event time
- Who - user
- What - [[region|Region]]/Resource/Action
Trails are stored in [[storage-s3|S3]] and are analyzed with Amazon [[analytics-athena|Athena]]
