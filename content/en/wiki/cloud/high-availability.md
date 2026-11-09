---
title: High availability
category: Cloud
description: ''
tags:
- cloud
- fundamentals
- reliability
---

<!-- imported from ObsidianVault/studies/definitions/high availability.md. Edit the source, then run sync.py. -->

# High availability

`cloud` `fundamentals` `reliability`

- Your services should be able to remain highly available by having no single point of failure
- This is primarily done by having cloud workloads running in multiple  [[region|regions]] and/or [[availability-zones|availability zones]]
- You can use Elastic Load Balancer to distribute traffic and automatically re-route in case of failures
