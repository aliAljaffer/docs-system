---
title: Aws security
category: AWS
description: An effictively secured application has security at multiple layers. For
  appilications in the cloud, we can consider 7 layers of security.
tags:
- gcp
---


# Aws security

`gcp`

AWS security is the set of practices and services that protect applications and data in the AWS cloud.

An effictively secured application has security at multiple layers. For appilications in the cloud, we can consider 7 layers of security.
1. Data - access to business/customer data, encryption
2. Application - No vulns
3. Compute - Controlled access to instances
4. Network - Control access to and communication with resources
5. Perimeter - Filter large scale attacks
6. Identity and Access - Control access to infrastructure and change management
7. Physical - Limiting access to a data center (not applicable in aws/cloud)
## Encryption
- In transit - SSL/TLS
- At rest - [[storage-s3|S3]] SSE, RDS DB instances
One of the most popular and secure types of encryption is AES-256

## AWS services related to security
- [[security-inspector|AWS Inspector]]
- [[security-shield|AWS Shield]]
- [[security-guardduty|AWS GuardDuty]]
- [[networking-vpn|Virtual Private Networks]]
- [[security-waf|AWS WAF]]
- [[security-kms|AWS Key Management Service]]
- [[security-artifact|artifact]]
- [[security-cognito|cognito]]
- [[security-user-and-identity-management|user and identity management]]
