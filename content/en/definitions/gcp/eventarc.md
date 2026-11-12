---
title: Eventarc
category: GCP
description: 'GCP note: Eventarc.'
tags:
- gcp
- data
---


# Eventarc

`gcp` `data`

## Eventarc
**Event routing service** that connects Google Cloud services, software as a service (SaaS), and custom applications using **events**

**AWS Equivalent:** Amazon EventBridge

### Overview
- Centralized event routing for event-driven architectures
- **100+ event sources** (Google Cloud services, custom apps, SaaS)
- Route events to **Cloud Run, Cloud Functions, GKE, Workflows**
- Built on [[pub-sub|Cloud Pub/Sub]] infrastructure
- **CloudEvents standard** format (industry standard)
- No infrastructure to manage

### Key Differences from AWS EventBridge

| Feature | GCP Eventarc | AWS EventBridge |
|---------|--------------|-----------------|
| Event format | **CloudEvents standard** | AWS event schema |
| Infrastructure | Built on Pub/Sub | AWS-managed buses |
| Targets | Cloud Run, Functions, GKE, Workflows | Lambda, Step Functions, SQS, etc. |
| Event sources | 100+ Google services + custom | AWS services + SaaS partners |
| Filtering | Attribute-based filtering | Content-based filtering |
| Pricing | Based on Pub/Sub (per event) | Per event published |

---

## Event Sources

### Google Cloud Service Events
**Direct events** (no [[pub-sub|Pub/Sub]] topic needed):

| Service | Example events |
|---|---|
| **[[gcp/cloud-storage|Cloud Storage]]** | Object finalize, delete, archive, metadata update |
| **[[gcp/pub-sub|Pub/Sub]]** | Message published to topic |
| **[[gcp/firestore|Firestore]]** | Document create, update, delete |
| **[[gcp/artifact-registry|Artifact Registry]]** | Image push, delete |
| **[[gcp/compute-engine|Compute Engine]]** | Instance start, stop, delete |
| **[[gcp/cloud-sql|Cloud SQL]]** | Instance creation, backup complete |
| **[[gcp/cloud-build|Cloud Build]]** | Build status changes |
| **BigQuery** | Job complete, dataset changes |

- **50+ more Google Cloud services**

### Audit Log Events
- **Cloud Audit Logs** as event source
- Track API calls across Google Cloud
- Examples:
  - [[gcp/iam|IAM]] policy changes
  - [[gcp/vpc|VPC]] firewall rule modifications
  - [[gcp/cloud-sql|Cloud SQL]] instance deletions
- Filter by service, method, resource type
- Use case: Automated remediation, compliance monitoring

### Custom Application Events
- Publish custom events to Eventarc
- Uses [[pub-sub|Pub/Sub]] topics
- **CloudEvents format** required
- Use case: Integrate your apps into event-driven workflows

### Third-Party SaaS Events (Preview)
- Integrate with external SaaS providers
- Examples: Datadog, PagerDuty, GitHub (via Pub/Sub)
- Requires Pub/Sub integration
- Use case: Multi-cloud event routing

---

## Event Targets

### Supported Targets

| Target | Use Case | Invocation |
|--------|----------|------------|
| **[[gcp/cloud-run|Cloud Run]]** | HTTP services, APIs, web apps | **Recommended** |
| **[[gcp/cloud-functions|Cloud Functions]]** | Simple event processing | Good for small functions |
| **[[gcp/gke|GKE]]** | Complex workloads, stateful apps | Advanced use cases |
| **Workflows** | Multi-step orchestration | Coordinate services |

### Cloud Run as Target (Recommended)
- **Most common target** for Eventarc
- Automatic scaling (0 to N)
- Receives events as HTTP POST requests
- Event delivered in CloudEvents format
- Example: Image processing on [[gcp/cloud-storage|Cloud Storage]] upload

### Cloud Functions as Target
- 2nd gen [[gcp/cloud-functions|Cloud Functions]] required
- Event-driven function invocation
- Simpler than Cloud Run for basic tasks
- Event automatically parsed

### GKE as Target
- Deploy event handler as Kubernetes Service
- Suitable for complex, stateful processing
- Requires [[gcp/gke|GKE]] cluster
- Event delivered to Service endpoint

### Workflows as Target
- Orchestrate multi-step processes
- Example: Storage upload → Workflow → Cloud Run → [[bigquery|BigQuery]]
- YAML-based workflow definition
- Built-in error handling, retries

---

## Event Format

### CloudEvents Standard
- **Industry-standard event format**
- JSON structure with metadata + data
- Portable across platforms
- Required for custom events

### CloudEvents Example
```json
{
  "specversion": "1.0",
  "type": "google.cloud.storage.object.v1.finalized",
  "source": "//storage.googleapis.com/projects/_/buckets/my-bucket",
  "subject": "objects/photo.jpg",
  "id": "unique-event-id",
  "time": "2024-01-15T10:00:00Z",
  "datacontenttype": "application/json",
  "data": {
    "bucket": "my-bucket",
    "name": "photo.jpg",
    "size": 524288,
    "contentType": "image/jpeg"
  }
}
```

### Event Attributes

| Attribute | Meaning |
|---|---|
| **type** | Event type (e.g., `google.cloud.storage.object.v1.finalized`) |
| **source** | Event source (service/resource) |
| **subject** | Specific resource (e.g., object name) |
| **id** | Unique event identifier |
| **time** | Event timestamp |
| **data** | Event payload (service-specific) |

---

## Event Triggers

### Creating Triggers
**Trigger** = Configuration that routes events from source to target

**Components:**
1. **Event provider**: Source service (e.g., [[gcp/cloud-storage|Cloud Storage]])
2. **Event type**: Specific event (e.g., object finalized)
3. **Event filters**: Attribute matching (optional)
4. **Target**: Destination service (e.g., [[gcp/cloud-run|Cloud Run]])
5. **Service account**: Identity for invoking target

### Event Filtering
Filter events by attributes before routing:

```yaml
# Example: Only process .jpg files from specific bucket
eventFilters:
  - attribute: bucket
    value: my-photos-bucket
  - attribute: name
    value: "*.jpg"
    operator: match
```

**Filter Operators:**
- **Exact match**: `value: "exact-string"`
- **Pattern match**: `operator: match` with wildcards
- **Path match**: Match resource paths

### Multiple Triggers
- **One event can trigger multiple targets**
- Each trigger independent
- Fan-out pattern for parallel processing
- Example: Storage upload → Cloud Run (resize) + Cloud Function (metadata) + Workflows (pipeline)

---

## Architecture Patterns

### Pattern 1: Event-Driven Data Processing
```text
Cloud Storage upload
  ↓ (Eventarc)
Cloud Run (process file)
  ↓
BigQuery (load data)
```
**Use case:** Automated ETL pipeline

### Pattern 2: Serverless Workflow Orchestration
```text
Pub/Sub message
  ↓ (Eventarc)
Workflows
  ↓
Cloud Run → Cloud Functions → BigQuery
```
**Use case:** Multi-step business process

### Pattern 3: Audit-Driven Automation
```text
Cloud Audit Logs (IAM change)
  ↓ (Eventarc)
Cloud Run (validate change)
  ↓
Send alert or auto-remediate
```
**Use case:** Security automation, compliance

### Pattern 4: Multi-Source Fan-Out
```text
Storage + Firestore + Pub/Sub
  ↓ (Eventarc - 3 triggers)
Cloud Run service
```
**Use case:** Unified event handler for multiple sources

---

## Eventarc vs Pub/Sub

### When to Use Eventarc
✓ **Event routing** from Google Cloud services
✓ **Declarative triggers** (no code for routing)
✓ **CloudEvents standard** format
✓ **Multiple event sources** to single target
✓ **Audit log events** as triggers
✓ **Simplified event-driven architectures**

**Example:** "Trigger Cloud Run when file uploaded to Cloud Storage"

### When to Use Pub/Sub Directly
✓ **Asynchronous messaging** between services
✓ **Custom message format** (not CloudEvents)
✓ **Message buffering** and replay
✓ **Push/pull subscriptions**
✓ **High-throughput streaming**
✓ **Dead letter queues** and retry policies

**Example:** "Microservices communicating via message queue"

### Relationship
- Eventarc **built on top of Pub/Sub**
- Eventarc creates [[pub-sub|Pub/Sub]] topics/subscriptions automatically
- Can use Pub/Sub for custom events in Eventarc
- Eventarc = higher-level abstraction for event routing

---

## Pricing
- **No charge for Eventarc service** itself
- Underlying costs:
  - **[[pub-sub|Pub/Sub]]**: $40 per TiB of data (first 10 GiB/month free)
  - **Target invocation**: [[gcp/cloud-run|Cloud Run]] or [[gcp/cloud-functions|Cloud Functions]] pricing
  - **Event egress**: Standard network egress rates
- **Audit log events**: Cloud Logging costs apply

**Example cost:**
- 1 million events/month (10 KB each) = ~10 GB
- Pub/Sub: ~$0.40
- Cloud Run invocations: Variable (see Cloud Run pricing)

---

## ACE Level

### Essential gcloud Commands
```bash
# List available event providers
gcloud eventarc providers list

# List event types for a provider
gcloud eventarc providers describe google.cloud.storage

# Create trigger for Cloud Storage → Cloud Run
gcloud eventarc triggers create TRIGGER_NAME \
  --location=REGION \
  --destination-run-service=SERVICE_NAME \
  --destination-run-region=REGION \
  --event-filters="type=google.cloud.storage.object.v1.finalized" \
  --event-filters="bucket=BUCKET_NAME" \
  --service-account=SERVICE_ACCOUNT@PROJECT.iam.gserviceaccount.com

# Create trigger for Pub/Sub → Cloud Run
gcloud eventarc triggers create TRIGGER_NAME \
  --location=REGION \
  --destination-run-service=SERVICE_NAME \
  --destination-run-region=REGION \
  --event-filters="type=google.cloud.pubsub.topic.v1.messagePublished" \
  --transport-topic=TOPIC_NAME

# Create trigger for Audit Logs → Cloud Run
gcloud eventarc triggers create TRIGGER_NAME \
  --location=REGION \
  --destination-run-service=SERVICE_NAME \
  --destination-run-region=REGION \
  --event-filters="type=google.cloud.audit.log.v1.written" \
  --event-filters="serviceName=compute.googleapis.com" \
  --event-filters="methodName=v1.compute.instances.delete"

# List triggers
gcloud eventarc triggers list --location=REGION

# Describe trigger
gcloud eventarc triggers describe TRIGGER_NAME --location=REGION

# Delete trigger
gcloud eventarc triggers delete TRIGGER_NAME --location=REGION
```

### Key Concepts for ACE
- Understanding event-driven architectures
- Creating Eventarc triggers for [[gcp/cloud-storage|Cloud Storage]] and [[pub-sub|Pub/Sub]] events
- Routing events to [[gcp/cloud-run|Cloud Run]] services
- Using event filters to process specific events
- Granting appropriate [[gcp/iam|IAM]] permissions for event routing
- Viewing trigger status and event logs
- Troubleshooting failed event deliveries

---

## PCA Level

### Architectural Design Patterns

#### Event-Driven Microservices
```text
Multiple Services → Pub/Sub Topics
                    ↓ (Eventarc)
                Cloud Run Services
                    ↓
        Process events independently
```
**Benefits:**
- Loose coupling between services
- Independent scaling per service
- Async communication
- Resilient to failures

#### Serverless ETL Pipeline
```text
Cloud Storage (raw data)
  ↓ (Eventarc)
Cloud Run (transform)
  ↓
Cloud Storage (processed)
  ↓ (Eventarc)
Cloud Run (load to BigQuery)
  ↓
BigQuery (analytics)
```
**Benefits:**
- Fully serverless (no infrastructure)
- Auto-scaling based on data volume
- Pay-per-use pricing
- Event-driven orchestration

#### Security Automation
```text
Cloud Audit Logs (security events)
  ↓ (Eventarc)
Cloud Run (analyze + respond)
  ↓
- Send alert (Pub/Sub → Cloud Monitoring)
- Auto-remediate (API call)
- Log to SIEM (Cloud Logging)
```
**Benefits:**
- Real-time security response
- Automated compliance enforcement
- Centralized security monitoring

#### Multi-Cloud Event Hub
```text
GCP Services + AWS (via Pub/Sub) + On-Prem (via Pub/Sub)
  ↓ (Eventarc)
Cloud Run / Workflows
  ↓
Process events from any source
```
**Benefits:**
- Unified event handling
- Cloud-agnostic event processing
- Simplified integration

### High Availability Design
- **Regional triggers**: Deployed in single region
- **Multi-region HA**: Deploy identical triggers in multiple regions
- **Event delivery**: At-least-once delivery guarantee
- **Retries**: Automatic retry with exponential backoff
- **Dead letter queues**: Use [[pub-sub|Pub/Sub]] DLQ for failed events
- **Idempotency**: Design targets to handle duplicate events

**HA Pattern:**
```text
Cloud Storage (global)
  ↓
Eventarc Trigger (us-central1) → Cloud Run (us-central1)
Eventarc Trigger (europe-west1) → Cloud Run (europe-west1)
```

### Security Best Practices
- **[[gcp/iam|Service Accounts]]**:
  - Unique service account per trigger
  - Minimal permissions (least privilege)
  - `roles/run.invoker` for Cloud Run targets
  - `roles/cloudfunctions.invoker` for Cloud Functions targets
- **Event authentication**:
  - Eventarc automatically includes auth tokens
  - Targets verify caller identity
  - No public endpoints required
- **[[gcp/vpc|VPC]] integration**:
  - Use [[gcp/cloud-run|Cloud Run internal ingress]]
  - Private event targets (no internet exposure)
- **[[gcp/vpc-service-controls|VPC Service Controls]]**:
  - Protect event data from exfiltration
  - Control cross-project event routing
- **Audit logging**:
  - All trigger operations logged to [[gcp/cloud-logging|Cloud Logging]]
  - Track event deliveries and failures

### Performance Optimization
- **Concurrency**:
  - [[gcp/cloud-run|Cloud Run]]: Up to 1000 concurrent requests
  - [[gcp/cloud-functions|Cloud Functions]]: Up to 1000 concurrent invocations
- **Cold starts**:
  - Use Cloud Run [[gcp/cloud-run|min instances]] for latency-sensitive
  - Optimize container startup time
- **Event filtering**:
  - Filter at trigger (reduce invocations)
  - More efficient than filtering in code
- **Batching**:
  - Not supported by Eventarc (one event = one invocation)
  - Use [[pub-sub|Pub/Sub]] directly for batching

### Cost Optimization
- **Event filtering**: Reduce unnecessary target invocations
- **Right-size targets**:
  - [[gcp/cloud-run|Cloud Run]]: Appropriate CPU/memory
  - [[gcp/cloud-functions|Cloud Functions]]: Minimize execution time
- **Avoid event storms**:
  - Use rate limiting on event sources
  - Implement circuit breakers
- **Shared triggers**: One trigger → multiple actions in single target
- **Monitoring**: Track invocation counts, identify wasteful events

### Observability & Monitoring
#### Cloud Monitoring Metrics
- `eventarc.googleapis.com/trigger/event_count`: Events received
- `eventarc.googleapis.com/trigger/event_count_by_response_code`: Success/failure rates
- `eventarc.googleapis.com/trigger/event_latencies`: End-to-end latency

#### Cloud Logging
```bash
# View Eventarc trigger activity
gcloud logging read "resource.type=eventarc.googleapis.com/Trigger" \
  --limit=100

# View failed event deliveries
gcloud logging read "resource.type=eventarc.googleapis.com/Trigger AND \
  jsonPayload.responseCode >= 400" \
  --limit=50

# View events for specific trigger
gcloud logging read "resource.labels.trigger_name=TRIGGER_NAME" \
  --format=json
```

#### Alerting Policies

| Alert | Condition |
|---|---|
| **Failed deliveries** | `event_count_by_response_code{code>=400} > threshold` |
| **High latency** | `event_latencies > 5s` |
| **No events** | `event_count == 0` for expected sources |
| **DLQ accumulation** | Monitor [[pub-sub|Pub/Sub]] DLQ message count |

### Error Handling & Retries
#### Automatic Retries
- Exponential backoff (1s, 2s, 4s, 8s, ...)
- Max retry duration: 24 hours

| Target response | Retried? |
|---|---|
| 2xx (success) | No, stops retrying |
| 4xx (client error) | No, don't retry |
| 5xx (server error) | Yes |
| Network errors | Yes |
| Timeouts | Yes |

#### Dead Letter Queues
- Configure [[pub-sub|Pub/Sub]] DLQ on underlying subscription
- Failed events routed to DLQ after max retries
- Manual processing or alerting on DLQ messages
- Preserve failed events for analysis

#### Idempotency
**Critical for event-driven systems:**
- Events may be delivered multiple times
- Design targets to handle duplicates safely
- Use event ID for deduplication
- Example: Check if event already processed before acting

### Migration Strategies

#### From AWS EventBridge
**Mapping:**
- EventBridge rules → Eventarc triggers
- EventBridge buses → [[pub-sub|Pub/Sub]] topics
- EventBridge targets → Cloud Run/Cloud Functions
- Event schemas → CloudEvents format

**Process:**
1. Map event sources (AWS services → GCP services)
2. Convert event schemas to CloudEvents
3. Create Eventarc triggers for each EventBridge rule
4. Migrate targets (Lambda → Cloud Run/Cloud Functions)
5. Test event flow end-to-end
6. Cutover event sources

#### From Direct Pub/Sub Integration
**Before (manual):**
```text
Cloud Storage → Pub/Sub topic → Cloud Run
(Configure notification) (Manual subscription)
```

**After (Eventarc):**
```text
Cloud Storage → Eventarc trigger → Cloud Run
(Automatic routing, no manual Pub/Sub setup)
```

**Benefits:**
- Simplified configuration
- CloudEvents standard format
- Centralized trigger management

### Integration with GCP Services
- **[[gcp/cloud-run|Cloud Run]]**: Primary target (recommended)
- **[[gcp/cloud-functions|Cloud Functions]]**: Event-driven functions (2nd gen)
- **[[gcp/gke|GKE]]**: Complex workloads, stateful processing
- **Workflows**: Multi-step orchestration
- **[[pub-sub|Pub/Sub]]**: Underlying messaging, custom events
- **[[gcp/cloud-storage|Cloud Storage]]**: Object events (finalize, delete, archive)
- **[[gcp/firestore|Firestore]]**: Document events (create, update, delete)
- **[[gcp/cloud-build|Cloud Build]]**: Build status events
- **[[gcp/cloud-logging|Cloud Logging]]**: Audit log events
- **[[bigquery|BigQuery]]**: Job completion events

### Use Case Examples

#### Real-Time Image Processing
```yaml
# When image uploaded to Cloud Storage
Trigger:
  source: Cloud Storage
  event: object.finalized
  filter: contentType=image/*
  target: Cloud Run

Cloud Run Service:
  - Resize image
  - Generate thumbnails
  - Extract metadata
  - Store in Cloud Storage (processed bucket)
```

#### Automated Security Response
```yaml
# When firewall rule deleted (audit log)
Trigger:
  source: Cloud Audit Logs
  event: v1.compute.firewalls.delete
  target: Cloud Run

Cloud Run Service:
  - Validate deletion (authorized?)
  - If unauthorized: Recreate rule + Alert security team
  - Log to SIEM
```

#### Event-Driven Data Pipeline
```yaml
# When data file uploaded
Trigger 1: Storage → Cloud Run (validate)
Trigger 2: Pub/Sub (validated) → Cloud Run (transform)
Trigger 3: Pub/Sub (transformed) → Cloud Run (load to BigQuery)

Benefits:
  - Each stage independent
  - Automatic retries per stage
  - Parallel processing when possible
```

### Compliance Considerations
- **Event audit trail**: All events logged via [[gcp/cloud-logging|Cloud Logging]]
- **Data residency**: Events processed in trigger region
- **Encryption**: Events encrypted in transit (HTTPS)
- **Access control**: [[gcp/iam|IAM]]-based event routing
- **Retention**: Configure [[pub-sub|Pub/Sub]] message retention for compliance

### Troubleshooting

#### Events Not Triggering Target
**Check:**
1. Trigger active? `gcloud eventarc triggers describe TRIGGER_NAME`
2. Event filters correct? (bucket name, event type)
3. [[gcp/iam|IAM]] permissions: Service account has `run.invoker` or `cloudfunctions.invoker`
4. Target service deployed and healthy?
5. Event actually published? Check source service logs

#### High Latency
**Causes:**
- Cold starts on target ([[gcp/cloud-run|Cloud Run]]/[[gcp/cloud-functions|Cloud Functions]])
- Slow target processing
- Network issues

**Solutions:**
- Set min instances on Cloud Run
- Optimize target code
- Use [[gcp/cloud-trace|Cloud Trace]] to identify bottlenecks

#### Failed Event Deliveries
**Check [[gcp/cloud-logging|Cloud Logging]]:**
```bash
gcloud logging read "resource.type=eventarc.googleapis.com/Trigger AND \
  jsonPayload.responseCode >= 400"
```

**Common issues:**
- Target returning 4xx (fix target code)
- Target timeout (increase timeout)
- Target quota exceeded
- Network connectivity

### Well-Architected Considerations
- **Operational Excellence**: Managed service, no infrastructure, centralized trigger management, [[gcp/cloud-logging|Cloud Logging]] integration
- **Reliability**: At-least-once delivery, automatic retries, DLQ for failures, built on [[pub-sub|Pub/Sub]] (99.95% SLA)
- **Security**: [[gcp/iam|IAM]]-based access, service account identity, [[gcp/vpc-service-controls|VPC Service Controls]], [[gcp/cloud-logging|audit logging]]
- **Performance**: Low latency event routing, concurrent processing, filter at source, CloudEvents standard
- **Cost**: Pay-per-event ([[pub-sub|Pub/Sub]] costs), no idle charges, event filtering reduces costs, serverless targets
- **Sustainability**: Serverless architecture, auto-scaling (no idle resources), efficient event routing

---

## Common Exam Scenarios

### Scenario 1: Serverless Image Processing
**Question:** "Automatically resize images when uploaded to Cloud Storage. What's the simplest solution?"

**Answer:** **Eventarc trigger from Cloud Storage → [[gcp/cloud-run|Cloud Run]]**
- **Why**: No code for event routing, automatic scaling, fully serverless
- **Why not Pub/Sub directly**: More configuration (manual topic, subscription, notification)
- **Why not Cloud Functions**: Cloud Run more flexible (custom runtime, longer timeout)

---

### Scenario 2: Multi-Step Workflow
**Question:** "Process uploaded file: validate → transform → load to BigQuery. How to orchestrate?"

**Answer:** **Eventarc → Workflows → Multiple Cloud Run services**
- **Why**: Workflows orchestrates multi-step processes
- **Why not single Cloud Run**: Separation of concerns, easier to maintain
- **Why not multiple triggers**: Can't guarantee order, no built-in orchestration

---

### Scenario 3: Audit Log Automation
**Question:** "Alert when [[gcp/iam|IAM]] policy changed. Real-time automation needed."

**Answer:** **Eventarc trigger on Cloud Audit Logs → [[gcp/cloud-run|Cloud Run]]**
- **Why**: Real-time (no polling), audit logs as event source
- **Why not scheduled function**: Not real-time
- **Why not [[gcp/cloud-logging|Cloud Logging]] sink**: Eventarc more appropriate for triggering actions

---

## Related Services
- **[[pub-sub|Cloud Pub/Sub]]**: Underlying messaging infrastructure
- **[[gcp/cloud-run|Cloud Run]]**: Primary event target (recommended)
- **[[gcp/cloud-functions|Cloud Functions]]**: Serverless event handlers
- **[[gcp/gke|GKE]]**: Container-based event targets
- **[[gcp/cloud-storage|Cloud Storage]]**: Common event source (object events)
- **[[gcp/firestore|Firestore]]**: Document event source
- **[[gcp/cloud-build|Cloud Build]]**: Build event source
- **[[gcp/cloud-logging|Cloud Logging]]**: Audit log events, trigger logging
- **[[gcp/cloud-monitoring|Cloud Monitoring]]**: Event metrics and alerting
- **Workflows**: Event-driven orchestration
