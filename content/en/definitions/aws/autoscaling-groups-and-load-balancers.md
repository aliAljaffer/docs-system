---
title: autoscaling groups and load balancers
category: AWS
description: These two services together are what allows you to achieve high elasticity
  and scalability for compute workloads.
tags:
- gcp
---


# autoscaling groups and load balancers

`gcp`

These two services together are what allows you to achieve high [[elasticity]] and [[scalability]] for [[aws-compute|compute]] workloads.

- Autoscaling groups: Can automatically add/remove instances to meet performance requirements. Allows min/desired/max instances.
- Elastic Load Balancers ([[aws-saa-c03/03-compute#Elastic Load Balancing|ELB]]): Distribute traffic between instances to achieve best possible latency.
	- Application Load Balancer - **Used for distributing traffic from the web to targets in your network.** HTTP/S trafic
	- Network Load Balancer - **Used to handle millions of requests per second.** TCP traffic.
