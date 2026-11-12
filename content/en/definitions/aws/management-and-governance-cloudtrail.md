---
title: cloudtrail
category: AWS
description: '"Track user activity and API usage on AWS and in hybrid and multicloud
  environments"'
tags:
- aws
- services
---


# cloudtrail

"Track user activity and ****API**** usage on AWS and in hybrid and multicloud environments"
**AWS CloudTrail** is a service that enables governance, compliance, operational **auditing**, and auditing of your AWS account.
If asked how to track API calls or user access => CloudTrail
Monitors API calls:

| Question | CloudTrail field |
|---|---|
| Where | Source IP |
| When | Event time |
| Who | User |
| What | [[region|Region]]/Resource/Action |

Trails are stored in [[storage-s3|S3]] and are analyzed with Amazon [[analytics-athena|Athena]]
