---
title: Reliability pillars
category: Cloud
description: 'Cloud note: Reliability pillars.'
tags:
- gcp
---

<!-- imported from ObsidianVault/studies/cloud-architecht/unsorted/reliability pillars.md. Edit the source, then run sync.py. -->

# Reliability pillars

`gcp`

- Automatically recover from failure
	- Monitor KPI and trigger automation when threshold is breached
- Test recovery procedures
	- Don't assume your procedures will work
- Scale horizontally to increase availability
	- Replace one large resource with multiple resources to reduce the impact of a single failure
- Stop guessing capacity
	- Utilize cloud flexibility to right size your resources
- Manage changes via automation
	- Use [[infrastructure-as-code|IaC]]
