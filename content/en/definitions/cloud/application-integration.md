---
title: Application integration
category: Cloud
description: Refers to letting multiple independent applications work and communicate
  with each other, while being facilitated by an intermediate system.
tags:
- gcp
---

<!-- imported from ObsidianVault/studies/cloud-architecht/unsorted/application integration.md. Edit the source, then run sync.py. -->

# Application integration

`gcp`

Refers to letting multiple independent applications work and communicate with each other, while being facilitated by an intermediate system.

By separating out apps into individual components, you reduce the risk of one thing breaking causing everything else to break. (Separation of concerns)

Most common systems utilized for application integration are:
- 
- 
- 
- 
## Queuing
A queueing system. is a non real-time messaging system, used to process messaging and events that will delete messages once consumed.

[[application-integration-sqs|SQS]]
## Publish/Subscribe (Pub/Sub)
Used for messaging and notifications.
[[application-integration-sns|SNS]] Flow:
- User subscribes to a topic to be notified by email when AWS account charges reach X dollars.
- When an account reaches X dollars, SNS sends a notification to that topic.
- The message is then filtered and sorted automatically emailed to the user notifying them of their charge.
## Streaming
Utilizes [[application-integration-sns|SNS]] and [[application-integration-sqs|SQS]], users or services can react to events/messages in real time as they are processed.
**[[analytics-kinesis|Amazon Kinesis]]** is the primary streaming service to handle analyzing real-time incoming events.
## API Gateways
APIs are the middlemen between an application and the backend systems. They contain information about a request, and once verified it sends back the appropriate information to load your profile.

[[networking-api-gateway|Amazon API Gateway]] handles APIs in your cloud environment context, and allows you to format requests and responses.
