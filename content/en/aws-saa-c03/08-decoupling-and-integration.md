# 8. Decoupling and Integration: SQS, SNS, Kinesis, EventBridge

**Goal:** Connect application parts with queues, topics, streams, and events.

## Amazon SQS

[[application-integration-sqs|SQS]] decouples application tiers. Producers send messages to a queue. Consumers poll the queue for messages.

| | Standard | FIFO |
|---|---|---|
| Throughput | Unlimited | Limited to 300 messages per second |
| Delivery | At least once. Duplicates are possible. | Exactly-once sending |
| Order | Messages can arrive out of order | Messages are processed in order |
| Ordering key | Not used | Message group ID (required) |

Standard queues also have these limits:

- Retention: 4 days. Maximum: 14 days.
- Latency: under 10 milliseconds.
- Maximum message size: 1 MiB (raised from 256 KiB in August 2025).

### Visibility timeout

After a consumer polls a message, other consumers cannot see it. When the visibility timeout ends, the message is visible again. A consumer can call `ChangeMessageVisibility` to get more time.

### Long polling

A consumer can wait for messages to arrive when the queue is empty.

### Security

- In-flight encryption: HTTPS API
- At-rest encryption: KMS keys

### Buffering

Use SQS as a buffer for database writes. The queue absorbs sudden spikes in load.

## Amazon SNS

[[application-integration-sns|SNS]] is a publish and subscribe service. A publisher sends a message to a topic. Every subscriber to the topic receives it.

- Limits: 12.5 million subscriptions per topic. 100,000 topics.
- Subscribers: HTTP endpoints, email, SMS and mobile, SQS, [[compute-lambda|Lambda]], and Data Firehose.
- Publishers: [[management-and-governance-cloudwatch|CloudWatch]] alarms, AWS Budgets, Lambda, Auto Scaling, S3, DynamoDB, CloudFormation, DMS, RDS, and others.
- Security: HTTPS API for in-flight encryption, KMS keys for at-rest encryption, and [[security-iam|IAM]] policies for access control.

### Fan-out

Publish to one SNS topic. Subscribe one SQS queue for each consumer. Each queue gets its own copy of the message. Fan-out works across Regions. Use an SNS FIFO topic with SQS FIFO queues to keep order.

Subscribers can filter messages with a JSON filter policy.

## Amazon Kinesis Data Streams

[[analytics-kinesis|Kinesis Data Streams]] collects and stores streaming data in real time.

- Retention: up to 1 year.
- Consumers can replay data.
- Records cannot be deleted before they expire.
- Maximum record size: 1 MB.
- Records with the same partition key stay in order.

| Capacity mode | How it works | Cost |
|---|---|---|
| Provisioned | You choose shards. Each shard gives 1 MB/s in and 2 MB/s out. You scale shards manually. | Pay per shard per hour |
| On-demand | No provisioning. Autoscales. Default capacity: 4 MB/s in. | Not in the note |

## Data Firehose

Data Firehose delivers streaming data to destinations in near real time.

- Fully managed, autoscaling, and [[serverless|serverless]]. Pay as you go.
- Formats: CSV, JSON, binary, and text. Use Lambda for custom transformations.
- Producers include clients, SDKs, the Kinesis agent, applications, IoT, CloudWatch, and Data Streams.

## Amazon MSK

Amazon MSK is fully managed Apache Kafka. You can create, update, and delete clusters. It deploys in a VPC across multiple AZs and recovers from failures automatically. Data is stored on [[storage-ebs|EBS]] for as long as you want. MSK Serverless runs Kafka without capacity management.

Consumers include Glue, Managed Service for Apache Flink, Lambda, and apps on EC2, ECS, or EKS.

## Amazon MQ

Amazon MQ is a managed message broker for RabbitMQ and ActiveMQ. It offers queues and topics. It does not scale like SQS and SNS.

## Managed Service for Apache Flink

Runs Apache Flink applications written in Java, Scala, or SQL. It reads from Data Streams, not Data Firehose.

## Choosing a messaging or streaming service

| Service | Model | Use it for |
|---|---|---|
| SQS | Queue. Consumers poll. | Decoupling tiers and absorbing spikes |
| SNS | Topic. Pushes to subscribers. | Notifications and fan-out |
| Kinesis Data Streams | Real-time stream with replay | Real-time data that consumers read and replay |
| Data Firehose | Near real-time delivery | Loading streams into destinations |
| MSK | Managed Apache Kafka | Kafka workloads |
| Amazon MQ | Managed RabbitMQ and ActiveMQ | Queues and topics from a managed broker |

## AWS Step Functions

[[application-integration-step-functions|Step Functions]] is a visual workflow builder.

- Supports sequences, parallel steps, conditions, and timeouts.
- Integrates with EC2, ECS, on-premises systems, and APIs.

## Amazon EventBridge

[[application-integration-eventbridge|EventBridge]] routes events.

- Schedules run cron jobs.
- Event patterns react when a service changes state.
- A rule sends the matching event, as JSON, to a target.
- You can replay events to check that a bug is fixed.
- The schema registry stores event schemas.
- Cross-account event buses send events between accounts.

## Exam tips

- Standard SQS delivers at least once. Messages can repeat or arrive out of order.
- Choose FIFO when order matters. FIFO allows 300 messages per second.
- SNS plus SQS fan-out gives each subscriber its own queue.
- Kinesis Data Streams supports replay. Choose it when consumers must read the same data again.
- Use Managed Service for Apache Flink with Data Streams, not Data Firehose.
- Amazon MQ does not scale like SQS and SNS.
- Records with the same partition key keep their order in Kinesis.
- The visibility timeout hides a message while a consumer works on it.

[Next: Security and Monitoring](09-security-and-monitoring.md)
