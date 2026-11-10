---
title: Logging
category: Cloud
description: 'Remember: Things WILL go wrong.'
tags:
- gcp
---

<!-- imported from ObsidianVault/studies/cloud-architecht/unsorted/logging.md. Edit the source, then run sync.py. -->

# Logging

`gcp`

Remember: Things WILL go wrong.

Logging helps the process of pinpointing where the failure occurred in the system, so that it can be fixed.

"Commonly logged actions include user logins and logouts, failed login attempts, system configuration changes, packet traffic, and process or service initiation. Also, logs often record alterations to files or databases."

AWS has a few types of logging services, but there are two primary areas you monitor:
- Your infrastructure itself (**What is happening**)
- Any changes and access to your infrastructure (**Who did what**)
## Services
- [[tagging]]
- [[analytics-athena|athena]]
- [[management-and-governance-cloudwatch|cloudwatch]]
- [[management-and-governance-cloudtrail|cloudtrail]]
