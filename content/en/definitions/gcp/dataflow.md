---
title: Dataflow
category: GCP
description: 'GCP note: Dataflow.'
tags:
- gcp
- data
---

<!-- imported from ObsidianVault/studies/cloud-architecht/gcp/data-analytics/dataflow.md. Edit the source, then run sync.py. -->

# Dataflow

`gcp` `data`

## Cloud Dataflow
**AWS Equivalent:** AWS Glue + Amazon Kinesis Data Analytics
**Fully managed** stream and batch data processing

### Overview
- **Based on Apache Beam**
- Unified batch and streaming processing
- Serverless, auto-scaling
- **Exactly-once processing** for streams
- Supports Java, Python, Go

### Apache Beam
- **Open-source** unified programming model
- **Portable** across Dataflow, Spark, Flink
- Write once, run anywhere
- Beam SDK → Dataflow Runner

### Pipeline Concepts
- **Pipeline**: End-to-end processing workflow
- **PCollection**: Distributed dataset
- **Transform**: Operation on PCollections
- **I/O Connectors**: Read/write data (Pub/Sub, BigQuery, Cloud Storage, etc.)

### Batch vs Streaming
#### Batch Processing
- Bounded data (finite dataset)
- Process historical data
- Higher throughput
- Use cases: ETL, data migration, backfill

#### Streaming Processing
- Unbounded data (continuous stream)
- Process real-time data
- Watermarks and windowing
- Use cases: Real-time analytics, monitoring, alerting

### Windowing
- **Fixed windows**: Tumbling windows (e.g., 1 hour)
- **Sliding windows**: Overlapping windows
- **Session windows**: Activity-based (gap detection)
- **Global window**: All data in one window (default for batch)

### Watermarks
- Track event time progress
- Handle late data
- Trigger window completion
- **Essential for streaming**

### Triggers
- When to emit results
- **Default**: Watermark passes window end
- **Early**: Emit speculative results
- **Late**: Handle late-arriving data
- **Accumulation**: Discarding, accumulating, retracting

### Autoscaling
- **Automatic worker scaling** based on CPU, throughput
- Horizontal scaling (add/remove workers)
- Vertical scaling (change machine types)
- No manual intervention needed

### Templates
**Pre-built pipelines**
- Classic templates: Word Count, Pub/Sub to BigQuery, etc.
- Flex templates: Custom Docker containers
- Parameterized execution
- Reusable across projects

### Dataflow SQL
- Write pipelines using SQL
- No code required
- Limited to specific sources (Pub/Sub, BigQuery, Pub/Sub Lite)
- **Easier than Beam SDK** for simple cases

### Exactly-Once Processing
- **Guaranteed for supported I/O** (Pub/Sub to BigQuery)
- Deduplication built-in
- Critical for financial, transactional data
- Not available in all AWS streaming services

### Shuffle Service
- **Managed shuffle** for GroupByKey operations
- Faster than worker-based shuffle
- Reduces costs
- **Enabled by default** for batch

### Streaming Engine
- Offload state/timer management to service backend
- Reduced worker CPU/memory
- Lower costs
- Faster pipeline startup

### Pricing
- **vCPU**: Per second
- **Memory**: Per GB-second
- **Persistent Disk**: Per GB-hour
- **Shuffle service**: Per GB shuffled
- **Streaming Engine**: Additional fee
- **No free tier**

---

## ACE Level

### Essential Commands
```bash
# Run template (Pub/Sub to BigQuery)
gcloud dataflow jobs run my-job \
  --gcs-location=gs://dataflow-templates/latest/PubSub_to_BigQuery \
  --region=us-central1 \
  --parameters=inputTopic=projects/PROJECT/topics/TOPIC,outputTableSpec=PROJECT:DATASET.TABLE

# List jobs
gcloud dataflow jobs list --region=us-central1

# Describe job
gcloud dataflow jobs describe JOB_ID --region=us-central1

# Cancel job
gcloud dataflow jobs cancel JOB_ID --region=us-central1

# Run Python pipeline
python my_pipeline.py \
  --runner=DataflowRunner \
  --project=PROJECT \
  --region=us-central1 \
  --temp_location=gs://BUCKET/temp

# Create Flex template
gcloud dataflow flex-template build gs://BUCKET/template.json \
  --image=gcr.io/PROJECT/my-template \
  --sdk-language=PYTHON
```

### Key Concepts for ACE
- Understanding Dataflow as managed Apache Beam
- Deploying pipelines using templates
- Understanding batch vs streaming pipelines
- Monitoring job execution in console
- Canceling and restarting jobs
- Reading from [[pub-sub|Pub/Sub]], writing to [[bigquery|BigQuery]]
- Understanding autoscaling

---

## PCA Level

### Architectural Patterns
#### Streaming ETL
```
Pub/Sub → Dataflow → Transform → BigQuery
                   → Enrich (Cloud SQL lookup)
                   → Aggregate (windowing)
```

#### Real-Time Analytics
```
IoT Devices → Pub/Sub → Dataflow (windowing) → BigQuery (dashboard)
                                              → Bigtable (time-series)
                                              → Pub/Sub (alerts)
```

#### Batch Data Processing
```
Cloud Storage (daily files) → Dataflow → Transform → BigQuery (data warehouse)
                                       → Validate → Cloud Storage (errors)
```

### Performance Optimization
- **Worker machine types**: Balance cost vs performance
- **Streaming Engine**: Reduce worker overhead
- **Shuffle service**: Faster GroupByKey
- **Autoscaling**: Set appropriate max workers
- **Fusion optimization**: Combines operations
- **Side inputs**: Use sparingly (broadcast to all workers)

### Cost Optimization
- **Flex templates**: Custom machine types
- **Preemptible VMs**: Up to 80% savings (batch jobs)
- **Streaming Engine**: Reduce worker CPU/memory
- **Right-size workers**: Don't over-provision
- **Committed use discounts**: For predictable workloads

### Fault Tolerance
- **Automatic retries**: Transient failures
- **Checkpointing**: For streaming jobs
- **Exactly-once**: Deduplication for supported I/O
- **Dead letter queues**: Failed messages to separate topic

### State and Timers
- **Stateful processing**: Per-key state
- **Timers**: Event-time or processing-time
- Use cases: Sessionization, rate limiting, delayed events

### Side Inputs
- **Broadcast data** to all workers
- Slow-changing lookup data
- Small datasets only
- Example: Reference data, configuration

### Testing
- **DirectRunner**: Local testing
- **Unit tests**: Test transforms independently
- **Integration tests**: Full pipeline on Dataflow
- **Validates data quality**

### Monitoring
- **Job graph**: Visual pipeline structure
- **Metrics**: Throughput, latency, errors
- **Logs**: Worker logs in Cloud Logging
- **Alerts**: On failures, lag, throughput

### Security
- **Service account**: Pipeline execution identity
- **VPC**: Run workers in VPC
- **CMEK**: Customer-managed encryption
- **Private IPs**: No external IPs for workers

### Use Cases
✓ **Good for:**
- ETL pipelines
- Stream processing
- Real-time analytics
- Data enrichment
- Aggregations, windowing
- Exactly-once processing

✗ **Not ideal for:**
- Simple data movement (use [[gcp/cloud-storage|Storage Transfer Service]])
- SQL-only transformations (use BigQuery directly)
- Very low latency (<1 second) - consider Pub/Sub + Cloud Functions

### Comparison with AWS
| Feature | Dataflow | Glue + Kinesis |
|---------|----------|----------------|
| Model | Apache Beam | Spark/Scala or SQL |
| Batch | ✓ | Glue |
| Streaming | ✓ | Kinesis Analytics |
| Exactly-once | ✓ | Limited |
| Autoscaling | ✓ | Limited (Glue) |
| Serverless | ✓ | Glue: ✓, Kinesis: Partial |

### Well-Architected Considerations
- **Operational Excellence**: Managed service, templates, monitoring
- **Reliability**: Exactly-once, checkpointing, autoscaling, fault tolerance
- **Security**: VPC, CMEK, service accounts, IAM
- **Performance**: Streaming Engine, shuffle service, autoscaling, fusion
- **Cost**: Preemptible VMs, right-sizing, Streaming Engine, CUD
- **Sustainability**: Autoscaling reduces waste, efficient processing
