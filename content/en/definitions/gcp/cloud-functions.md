---
title: Cloud-functions
category: GCP
description: Process one event, trigger multiple downstream processes
tags:
- gcp
- compute
---

<!-- imported from ObsidianVault/studies/cloud-architecht/gcp/compute/cloud-functions.md. Edit the source, then run sync.py. -->

# Cloud-functions

`gcp` `compute`

## Cloud Functions
**AWS Equivalent:** [[compute-lambda|AWS Lambda]]
**Event-driven serverless** compute for lightweight functions

### Generations
#### 1st Gen
- Original Cloud Functions
- Node.js, Python, Go, Java, .NET, Ruby, PHP
- Max 540 seconds (9 min) timeout
- Limited features

#### 2nd Gen (Recommended)
- **Built on [[cloud-run|Cloud Run]] infrastructure**
- Longer timeouts: **up to 60 minutes**
- Larger instances: up to 16 GiB memory, 4 vCPUs
- **Concurrency** up to 1000 concurrent requests per instance
- Traffic splitting, Eventarc triggers
- Better performance, more features

### Trigger Types
#### HTTP Triggers
- Invoke via HTTP request
- GET, POST, etc.
- Can be authenticated or unauthenticated
- Returns HTTP response

#### Event Triggers
- **Cloud Storage**: Object finalize, delete, archive, metadata update
- **Pub/Sub**: Message published to topic
- **Firestore**: Document create, update, delete
- **Firebase**: Real-time Database, Authentication, Analytics
- **Eventarc**: 100+ event sources (2nd gen only)

### Runtime Environment
- Temporary file system at `/tmp` (**ephemeral, not persisted across invocations**)
- Environment variables and secrets from Secret Manager
- No state preserved between invocations
- **Each invocation is isolated**

### Execution Environment Lifecycle
1. **Cold start**: New instance initialization
2. **Function execution**: Your code runs
3. **Warm**: Instance may be reused for subsequent invocations
4. **Instance shutdown**: After idle period

### Global Variables for Performance
```python
# BAD: Creates new client every invocation
def my_function(request):
    client = create_expensive_client()
    return client.query()

# GOOD: Reuses client across invocations (if instance is warm)
client = create_expensive_client()

def my_function(request):
    return client.query()
```

### Concurrency (2nd Gen)
- **1st gen**: 1 request per instance
- **2nd gen**: Up to 1000 concurrent requests per instance
- Reduces cold starts
- Lower costs (fewer instances)
- Requires thread-safe code

### Timeout & Limits
- **1st gen max timeout**: 540 seconds
- **2nd gen max timeout**: 3600 seconds (60 min)
- **Max payload**: 10 MB
- **Max concurrent invocations**: 1000 (can request increase)

### Memory & CPU
- **Memory**: 128 MB to 32 GB (2nd gen), 128 MB to 8 GB (1st gen)
- CPU scales with memory
- More memory = faster execution but higher cost

### Networking
- **VPC Connector** (1st gen): Connect to [[networking-vpc|VPC]] resources
- **Direct VPC egress** (2nd gen): Simpler [[networking-vpc|VPC]] connectivity
- Access Cloud SQL via Unix sockets or [[networking-vpc|VPC]]
- Static IP via Cloud NAT

### Security
- **Authentication**:
  - HTTP: `roles/cloudfunctions.invoker` for authenticated
  - Service-to-service: [[security-iam|Service account]] tokens
- **Secrets**: Secret Manager integration
- **[[security-iam|Service Account]]**: Function runs with associated service account identity
- **VPC Service Controls**: Prevent data exfiltration

### Cloud Functions vs Cloud Run vs App Engine
| Feature | Cloud Functions | [[cloud-run|Cloud Run]] | [[app-engine|App Engine]] |
|---------|----------------|----------|------------|
| Code unit | Function | Container | Application |
| Languages | Limited runtimes | Any (via container) | Multiple runtimes |
| Max duration | 60 min (2nd gen) | 60 min | 60 min (Flex) |
| Concurrency | 1000 (2nd gen) | 1000 | Configurable |
| Triggers | Events + HTTP | HTTP + Events | HTTP |
| Complexity | Simple functions | More complex | Full apps |
| Cold starts | Yes | Yes | Flex: Yes, Std: Minimal |

### Pricing
- **Invocations**: $0.40 per million (2nd gen)
- **Compute time**: Billed per 100ms
- **Networking**: Outbound data
- **Free tier** (2nd gen):
  - 2 million invocations/month
  - 400,000 GB-seconds
  - 200,000 GHz-seconds

---

## ACE Level

### Essential gcloud Commands
```bash
# Deploy HTTP function (2nd gen)
gcloud functions deploy FUNCTION_NAME \
  --gen2 \
  --runtime=python312 \
  --entry-point=my_function \
  --source=. \
  --trigger-http \
  --allow-unauthenticated

# Deploy event-driven function (2nd gen)
gcloud functions deploy FUNCTION_NAME \
  --gen2 \
  --runtime=nodejs20 \
  --entry-point=myFunction \
  --source=. \
  --trigger-bucket=BUCKET_NAME

# Deploy Pub/Sub triggered function
gcloud functions deploy FUNCTION_NAME \
  --gen2 \
  --runtime=go121 \
  --entry-point=ProcessMessage \
  --source=. \
  --trigger-topic=TOPIC_NAME

# List functions
gcloud functions list

# Describe function
gcloud functions describe FUNCTION_NAME --gen2 --region=REGION

# View logs
gcloud functions logs read FUNCTION_NAME --gen2

# Delete function
gcloud functions delete FUNCTION_NAME --gen2 --region=REGION

# Set environment variables
gcloud functions deploy FUNCTION_NAME \
  --gen2 \
  --set-env-vars=KEY1=VALUE1,KEY2=VALUE2

# Mount secret
gcloud functions deploy FUNCTION_NAME \
  --gen2 \
  --set-secrets=ENV_VAR=SECRET_NAME:latest
```

### Key Concepts for ACE
- Deploying functions from local code or Cloud Source Repositories
- Understanding trigger types (HTTP vs event-driven)
- Configuring environment variables and secrets
- Viewing function logs and execution history
- Setting appropriate memory and timeout values
- Understanding cold starts and warming strategies
- Managing function access with [[security-iam|IAM]]

---

## PCA Level

### Architectural Use Cases
#### API Backend
- Lightweight REST APIs
- Microservices endpoints
- Webhook receivers
- **Use [[cloud-run|Cloud Run]] for more complex APIs**

#### Event Processing
- **Cloud Storage**: Image resizing, file processing
- **Pub/Sub**: Async message processing, event handling
- **Firestore**: Real-time data processing, triggers
- ETL pipelines with Dataflow triggers

#### Scheduled Tasks
- Cloud Scheduler + HTTP trigger
- Periodic data cleanup, backups
- Report generation
- Health checks

#### IoT & Real-time
- Process Pub/Sub messages from IoT devices
- Real-time analytics
- Alerting and notifications
- Stream processing

### Performance Optimization
- **Min instances** (2nd gen): Keep instances warm for latency-sensitive apps
- **Concurrency** (2nd gen): Increase for I/O-bound functions
- **Global variables**: Initialize expensive resources outside function
- **Connection pooling**: For database connections
- **Memory sizing**: More memory = more CPU = faster execution
- **Code optimization**: Minimize dependencies, lazy loading

### Cold Start Mitigation
- **Use min instances (costs even when idle)**
- Reduce deployment package size
- Use global variables for initialization
- Consider [[cloud-run|Cloud Run]] for always-on requirements
- 2nd gen has faster cold starts than 1st gen

### Error Handling & Retries
- **Event-driven functions**: Automatic retries for failures
  - Exponential backoff
  - **Max retry period: 7 days**
  - Use dead letter queues for failed events
- **HTTP functions**: No automatic retries, client handles
- Idempotent function design for event triggers

### Cost Optimization
- **Right-size memory**: Balance performance vs cost
- **Timeout**: Set as low as possible
- **Concurrency** (2nd gen): Reduce instance count
- **Min instances**: Use sparingly
- **2nd gen vs 1st gen**: 2nd gen more cost-effective for concurrent workloads

### Security Best Practices
- **Authentication**: Require for sensitive functions
- **[[security-iam|Service Account]]**: Minimal permissions, unique per function
- **Secrets**: Use Secret Manager, not environment variables
- **VPC Service Controls**: Prevent data exfiltration
- **Input validation**: Always validate and sanitize
- **Rate limiting**: Prevent abuse (use Cloud Armor if exposed)

### Monitoring & Observability
- Cloud Monitoring: Invocations, errors, duration
- Cloud Logging: Function logs, structured logging
- Cloud Trace: Request latency tracking
- Error Reporting: Automatic error aggregation
- Custom metrics for business KPIs

### When to Use Cloud Functions
✓ **Good for:**
- Event-driven workflows
- Lightweight processing
- Simple APIs
- Glue code between services
- Scheduled tasks

✗ **Not ideal for:**
- Long-running processes (>60 min)
- Complex orchestration (use [Workflows](https://cloud.google.com/workflows) or [Cloud Composer](https://cloud.google.com/composer))
- Stateful applications
- Predictable high traffic (use [[cloud-run|Cloud Run]] or [[app-engine|App Engine]])
- Large deployments (50 MB limit)

### Integration Patterns
#### Fan-out Pattern
```
Cloud Storage → Function → Multiple Pub/Sub topics → Multiple Functions
```
Process one event, trigger multiple downstream processes

#### Aggregation Pattern
```
Multiple sources → Pub/Sub → Function → BigQuery/Cloud Storage
```
Collect and aggregate data from multiple sources

#### ETL Pipeline
```
Cloud Storage upload → Function → Transform data → Load to BigQuery
```

### Migration Strategies
#### From Lambda to Cloud Functions
- Similar event model
- Runtime differences (check compatibility)
- VPC connectivity differs
- [[security-iam|IAM]] model differences
- Consider 2nd gen for Lambda parity

#### When to Migrate to Cloud Run
- Need more control over environment
- Larger deployment packages
- More complex dependencies
- Always-on requirements

### Well-Architected Considerations
- **Operational Excellence**: Managed infrastructure, automatic scaling
- **Reliability**: Automatic retries, multi-region deployment option
- **Security**: [[security-iam|IAM]], secrets management, VPC connectivity, least privilege
- **Performance**: Right-size memory, connection pooling, global variables
- **Cost**: Pay-per-invocation, concurrency optimization, right-sizing
- **Sustainability**: Efficient resource use, scale to zero when idle
