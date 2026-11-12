---
title: Migration strategies
category: AWS
description: 'Cloud note: Migration strategies.'
tags:
- aws
---


# Migration strategies

`gcp`

Migration strategies, also called "the 6 R's", are six approaches for moving an application to the cloud: rehost, replatform, repurchase, refactor, retire, and retain.
### 1 - Rehosting ("Lift-and-shift")
Can be automated with tools like [[customer-enablement-aws-vm-import-export|AWS VM Import Export]].
"We’ve also found that applications are easier to optimize/re-architect once they’re already running in the cloud. Partly because your organization will have developed better skills to do so, and partly because the hard part  -  migrating the application, data, and traffic  -  has already been done."
### 2 - Replatforming ("Lift-tinker-and-shift")
Optimizations for the cloud on your application to achieve some benefit, like performance or lower costs, but you aren't changing the core architecture of the application. You may be looking to reduce the amount of time you spend managing database instances by migrating to a database as a service platform like [[database-aws-database#DB Services|RDS]] or migrating your application to a fully managed platform like [[compute-beanstalk|beanstalk]]
### 3 - Repurchasing - Moving to a different product
A move to a SaaS platform.
### 4 - Refactoring / Re-architecting - Re-imagining how the application is architected and developed, typically using cloud-native features.
Driven by a business need to add features, scale, or performance that would otherwise be difficult in the application's current environment.
### 5 - Retire - Get rid of (X)
Turning off now-useless features can cut on costs and security.
### 6 - Retain - Revisit or do nothing for now
"Maybe you’re still riding out some depreciation, aren’t ready to prioritize an application that was recently upgraded, or are otherwise not inclined to migrate some applications. You should only migrate what makes sense for the business; and, as the gravity of your portfolio changes from on-premises to the cloud, you’ll probably have fewer reasons to retain."
