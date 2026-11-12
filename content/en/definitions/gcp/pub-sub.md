---
title: Pub-sub
category: GCP
description: 'GCP note: Pub-sub.'
tags:
- gcp
- data
---


# Pub-sub

`gcp` `data`

## Cloud Pub/Sub
**AWS Equivalent:** [[application-integration-sns|SNS]] + [[application-integration-sqs|SQS]] combined
**Fully managed** messaging and event streaming

### Overview
- **Global, durable** message queuing service
- **Asynchronous** communication between services
- **At-least-once delivery** guarantee
- Ordered delivery (with ordering keys)
- Push and pull subscriptions

### Core Concepts
- **Topic**: Named resource to which messages are sent
- **Subscription**: Named resource representing stream from topic
- **Message**: Data payload + attributes
- **Publisher**: Sends messages to topic
- **Subscriber**: Receives messages from subscription

### Architecture Pattern
```text
Publishers → Topic → Subscription A (pull) → Service A
                  → Subscription B (push) → Service B
                  → Subscription C (pull) → Service C
```
- **One topic, multiple subscriptions** (fan-out)
- Each subscription gets all messages (unlike SQS)

### Delivery Methods
#### Pull Subscription
- Subscriber explicitly pulls messages
- **Streaming pull**: Long-lived connection, low latency
- **Synchronous pull**: One-time request
- Subscriber controls rate
- Good for: Batch processing, variable load

#### Push Subscription
- Pub/Sub sends HTTP POST to endpoint
- Endpoint must return 200 OK
- Automatic retries on failure
- Good for: Webhooks, [[cloud-functions|Cloud Functions]], [[gcp/cloud-run|Cloud Run]]

### Message Delivery Guarantees
- **At-least-once delivery** (may receive duplicates)
- **No exactly-once delivery** (application must handle deduplication)
- **Ordering with ordering keys** (per key)
- **Retention**: 7 days default, up to 31 days

### Message Acknowledgement
- **Pull**: Explicit ack required
- **Push**: 200/201/202/204 status code = ack
- **Ack deadline**: 10-600 seconds (configurable)
- **Nack**: Negative acknowledgement (redelivers immediately)
- **Extend deadline**: ModifyAckDeadline for slow processing

### Message Ordering
- **Not guaranteed by default**
- **Ordering keys**: Enable ordered delivery per key
- Messages with same key delivered in order
- Example: `user-123` as ordering key for all user's messages

### Message Attributes
- Key-value metadata
- Up to 100 attributes per message
- Filter subscriptions based on attributes
- Example: `"region": "us-west"`, `"priority": "high"`

### Subscription Filters
```text
attribute.region = "us-west" AND attribute.priority = "high"
```
- Filter messages at subscription level
- Reduce network traffic
- Reduce processing costs
- Only matching messages delivered

### Dead Letter Topics
- Messages that can't be processed after retries
- Forward to dead letter topic after X delivery attempts
- Investigate failed messages
- Prevent message loss

### Message Schemas
**Avro or Protocol Buffers**
- Validate message structure
- Enforce data contracts
- Version compatibility
- Schema Registry integration

### Snapshots
- Point-in-time capture of subscription state
- Replay messages from specific point
- Debug, recovery, testing
- Expire after 7 days

### Exactly-Once Processing (with Dataflow)
- **Cloud Dataflow + Pub/Sub** provides exactly-once
- Deduplication in Dataflow
- Use for critical workflows

### Throughput & Limits
- **Unlimited throughput** (scales automatically)
- **10 MB/second per partition** (configurable)
- Max message size: 10 MB
- Max retention: 31 days
- Max attributes: 100 per message

### Pricing
- **Message ingestion**: $0.04 per GB
- **Delivery**: $0.04 per GB
- **Snapshots**: $0.27 per GB-month
- **Seeks**: $0.01 per 1,000 seeks
- **Free tier**: 10 GB/month

---

## ACE Level

### Essential Commands
```bash
# Create topic
gcloud pubsub topics create my-topic

# List topics
gcloud pubsub topics list

# Publish message
gcloud pubsub topics publish my-topic --message="Hello World"

# Publish with attributes
gcloud pubsub topics publish my-topic \
  --message="Order placed" \
  --attribute=region=us-west,priority=high

# Create pull subscription
gcloud pubsub subscriptions create my-sub --topic=my-topic

# Create push subscription
gcloud pubsub subscriptions create my-push-sub \
  --topic=my-topic \
  --push-endpoint=https://example.com/push

# Pull messages
gcloud pubsub subscriptions pull my-sub --auto-ack --limit=5

# Delete subscription
gcloud pubsub subscriptions delete my-sub

# Delete topic
gcloud pubsub topics delete my-topic
```

### Key Concepts for ACE
- Creating topics and subscriptions
- Understanding pull vs push subscriptions
- Publishing messages to topics
- Pulling messages from subscriptions
- Understanding message acknowledgement
- Creating subscriptions with filters
- Understanding at-least-once delivery
- Configuring dead letter topics

---

## PCA Level

### Architectural Patterns
#### Event-Driven Microservices
```text
Order Service → order.created topic → Inventory Service (update stock)
                                   → Notification Service (email customer)
                                   → Analytics Service (track metrics)
```
- Decoupled services
- Async processing
- Independent scaling

#### Stream Processing Pipeline
```text
IoT Devices → Pub/Sub → Dataflow → BigQuery
                      → Dataflow → Bigtable
                      → Cloud Functions → Alerts
```
- Real-time data processing
- Multiple consumers
- Scalable ingestion

#### Fan-Out Pattern
```text
Single Publisher → Topic → Sub A (priority) → Fast processing
                        → Sub B (batch) → Hourly aggregation
                        → Sub C (archive) → Cloud Storage
```
- Different processing speeds
- Different retention policies
- Same source data

### High Availability Design
- **Global service, no regional deployment**
- Messages replicated across zones
- No single point of failure
- 99.95% availability SLA

### Security Best Practices
- **[[gcp/iam|IAM]] roles**:
  - `pubsub.publisher`: Publish messages
  - `pubsub.subscriber`: Receive messages
  - `pubsub.viewer`: List topics/subscriptions
  - `pubsub.admin`: Full access
- **Service accounts**: Different account per publisher/subscriber
- **VPC Service Controls**: Prevent data exfiltration
- **CMEK**: Customer-managed encryption keys

### Idempotency Handling
**At-least-once delivery requires idempotent processing**
```python
# Example: Use message ID for deduplication
processed_ids = set()

def process_message(message):
    if message.message_id in processed_ids:
        return  # Already processed

    # Process message
    do_work(message.data)

    # Record as processed
    processed_ids.add(message.message_id)
```

### Ordering Strategies
#### With Ordering Keys
```python
# Publish with ordering key
publisher.publish(
    topic_path,
    data=b'Message data',
    ordering_key='user-123'
)
```
- All messages for `user-123` delivered in order
- Different ordering keys can be parallel

#### Without Ordering
- Higher throughput
- No ordering guarantees
- Use when order doesn't matter

### Performance Optimization
- **Batch publishing**: Up to 1,000 messages per request
- **Streaming pull**: Lower latency than sync pull
- **Client libraries**: Auto-batching and flow control
- **Regional endpoints**: Lower latency (e.g., `us-east1-pubsub.googleapis.com`)

### Cost Optimization
- **Subscription filters**: Reduce delivery costs
- **Message compression**: Reduce data size
- **Batch processing**: Lower function invocation costs
- **Pull vs Push**: Pull can be more cost-effective for high volume

### Error Handling
- **Exponential backoff**: Automatic retries
- **Dead letter topics**: Failed messages
- **Monitoring**: Track undelivered messages
- **Alerts**: On delivery failures

### Integration Patterns
#### With Cloud Functions
```text
Pub/Sub → Cloud Function (event-driven)
```
- Automatic triggering
- Parallel execution
- Scalable processing

#### With Dataflow
```text
Pub/Sub → Dataflow → BigQuery/Bigtable
```
- Streaming data pipelines
- Exactly-once processing (with Dataflow)
- Complex transformations

#### With GKE
```text
Pub/Sub → GKE workload (pull subscription)
```
- Kubernetes-native integration
- Horizontal Pod Autoscaling based on queue depth

### Monitoring & Observability
- **[[cloud-monitoring|Cloud Monitoring]] metrics**:
  - Publish rate, throughput
  - Undelivered messages
  - Oldest unacknowledged message age
  - Subscription backlog
- **Alerts**: On backlog growth, delivery failures
- **[[cloud-logging|Logs]]**: Publish/subscribe audit logs

### Comparison with AWS
| Feature | Cloud Pub/Sub | SNS + SQS |
|---------|---------------|-----------|
| Fan-out | Native (subscriptions) | SNS → multiple SQS |
| Ordering | With ordering keys | SQS FIFO queues |
| Delivery | At-least-once | At-least-once |
| Retention | Up to 31 days | Up to 14 days |
| Message size | 10 MB | 256 KB (SQS) |
| Pricing | Per GB | Per request |

### Migration from SNS/SQS
- **SNS topic** → Pub/Sub topic
- **SQS queue** → Pub/Sub subscription
- **SNS + SQS fan-out** → Single topic with multiple subscriptions
- **SQS FIFO** → Pub/Sub with ordering keys

### Use Cases
✓ **Good for:**
- Event-driven architectures
- Microservices communication
- IoT data ingestion
- Log aggregation
- Stream processing pipelines
- Real-time analytics

✗ **Not ideal for:**
- Request-response patterns (use HTTP instead)
- Large messages (>10 MB) - use Cloud Storage + Pub/Sub notification
- Exactly-once delivery without Dataflow

### Well-Architected Considerations
- **Operational Excellence**: Managed service, no infrastructure, automated scaling
- **Reliability**: Global replication, 99.95% SLA, dead letter topics, retries
- **Security**: IAM, VPC SC, CMEK, service accounts per publisher/subscriber
- **Performance**: Auto-scaling, streaming pull, regional endpoints, batch publishing
- **Cost**: Per-GB pricing, filters reduce costs, pay-per-use model
- **Sustainability**: Efficient message routing, filters reduce unnecessary processing
