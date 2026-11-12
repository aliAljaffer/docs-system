---
title: Dataproc
category: GCP
description: 'GCP note: Dataproc.'
tags:
- gcp
- data
---


# Dataproc

`gcp` `data`

## Cloud Dataproc
**Managed Apache Spark and Hadoop** clusters

**AWS Equivalent:** Amazon EMR

### Overview
- Fast cluster provisioning (**90 seconds**)
- Pay-per-minute billing
- Autoscaling clusters
- **Integrated with GCP ecosystem**
- Supports Spark, Hadoop, Hive, Pig, Presto

### Use Cases
- Migrate existing Spark/Hadoop workloads
- Data lake processing
- ETL pipelines
- Machine learning with Spark MLlib
- When you need Spark ecosystem (not Beam)

### Cluster Types

| Cluster type | Layout | Use |
|---|---|---|
| Standard | 1 master, N workers | General-purpose, most common |
| High Availability | **3 masters** for HA | Recommended for production, automatic failover |
| Single Node | 1 node (master + worker) | Development and testing, lowest cost |

### Cluster Components
- **Master nodes**: Manage cluster (YARN, HDFS NameNode)
- **Worker nodes**: Execute tasks
- **Preemptible workers**: Low-cost, interruptible
- **Initialization actions**: Scripts run at cluster start

### Ephemeral vs Long-Running Clusters
#### Ephemeral (Recommended)
- Create for job, delete after
- **Lower cost**
- Cleaner separation
- No state management

#### Long-Running
- Persistent cluster
- Multiple jobs
- Interactive development
- Higher cost

### Autoscaling
- **Graceful decommissioning** (finish tasks before shutdown)
- Scale on YARN metrics
- Primary and secondary workers
- Scale up/down based on workload

### Preemptible Workers
**AWS Equivalent:** Spot Instances for EMR
- **Up to 80% discount**
- Can be terminated anytime
- **Recommended for secondary workers only** (not primary)
- HDFS data not stored on preemptible (unsafe)

### Storage Options

| Option | Persistence | Notes |
|---|---|---|
| HDFS | Lost when cluster deleted | Ephemeral storage on cluster, fast, but not durable |
| Cloud Storage | Persists after cluster deletion | **Recommended for durability**, **Cloud Storage Connector** (gs://), Hive metastore on Cloud SQL |
| Persistent Disk | Persists after cluster stop | Block storage attached to workers, more expensive than Cloud Storage |

### Metastore Integration
- **Cloud SQL**: Hive metastore persistence
- **Dataproc Metastore**: Managed Hive metastore service
- Share metastore across clusters
- Persist metadata after cluster deletion

### Initialization Actions
- Scripts run on all nodes at cluster creation
- Install additional packages
- Configure software
- Set environment variables

```bash
# Example: Install Python package
#!/bin/bash
pip install pandas
```

### Component Gateway
- Web UIs for Spark, Hadoop, YARN
- **Secure access via IAM** (no SSH tunneling needed)
- Spark History Server, YARN Resource Manager

### Dataproc Workflow Templates
- **DAG of Dataproc jobs**
- Define dependencies
- Parameterized execution
- Reusable workflows

### Dataproc Serverless
- **No cluster management**
- Auto-provisioning
- Run Spark workloads without clusters
- **Simpler than traditional Dataproc**
- **Batches**: Spark batch jobs
- **Sessions**: Interactive Spark

### Pricing
- **Cluster**: Per-second billing (1 minute minimum)
- **Dataproc fee**: $0.01 per vCPU/hour (on top of Compute Engine costs)
- **Preemptible workers**: Compute Engine preemptible pricing
- ==Total cost = Compute Engine + Dataproc fee==

---

## ACE Level

### Essential Commands
```bash
# Create cluster
gcloud dataproc clusters create my-cluster \
  --region=us-central1 \
  --zone=us-central1-a \
  --num-workers=2 \
  --worker-machine-type=n1-standard-4

# Create cluster with preemptible workers
gcloud dataproc clusters create my-cluster \
  --region=us-central1 \
  --num-workers=2 \
  --num-secondary-workers=4 \
  --secondary-worker-type=preemptible

# List clusters
gcloud dataproc clusters list --region=us-central1

# Delete cluster
gcloud dataproc clusters delete my-cluster --region=us-central1

# Submit Spark job
gcloud dataproc jobs submit spark \
  --cluster=my-cluster \
  --region=us-central1 \
  --jar=gs://BUCKET/my-jar.jar \
  --class=com.example.Main

# Submit PySpark job
gcloud dataproc jobs submit pyspark \
  --cluster=my-cluster \
  --region=us-central1 \
  gs://BUCKET/my-script.py

# Submit Hive job
gcloud dataproc jobs submit hive \
  --cluster=my-cluster \
  --region=us-central1 \
  --file=gs://BUCKET/my-query.hql

# List jobs
gcloud dataproc jobs list --region=us-central1

# Enable autoscaling
gcloud dataproc clusters update my-cluster \
  --region=us-central1 \
  --autoscaling-policy=my-policy
```

### Key Concepts for ACE
- Creating and deleting Dataproc clusters
- Understanding fast provisioning (90 seconds)
- Submitting Spark, PySpark, Hive jobs
- Using Cloud Storage instead of HDFS
- Configuring preemptible workers
- Understanding ephemeral vs long-running clusters
- Viewing job outputs and logs
- Enabling autoscaling

---

## PCA Level

### Architectural Patterns
#### Data Lake Processing
```text
Cloud Storage (data lake) → Dataproc (Spark ETL) → BigQuery (warehouse)
                                                  → Cloud Storage (curated)
```

#### Migration from On-Prem Hadoop
```text
On-prem HDFS → Cloud Storage (migrate data)
On-prem Hive → Dataproc + Cloud SQL Metastore
Existing Spark jobs → Dataproc (minimal changes)
```

#### Hybrid Analytics
```text
Dataproc (Spark processing) → BigQuery (SQL analytics)
                            → Bigtable (operational data)
                            → Cloud Storage (archival)
```

### High Availability Design
- **3 masters**: Automatic failover
- **Persistent metastore**: Cloud SQL or Dataproc Metastore
- **Cloud Storage**: Data survives cluster failure
- **Regional clusters**: Zone failure tolerance

### Cost Optimization
- **Ephemeral clusters**: Delete after job
- **Preemptible workers**: 50-80% of workers
- **Autoscaling**: Scale down idle clusters
- **Dataproc Serverless**: No idle costs
- **Per-second billing**: Minimize idle time
- **Committed Use Discounts**: For long-running clusters

### Performance Optimization
- **Local SSDs**: Faster than persistent disks
- **Preemptible workers**: More compute for same cost
- **Right-size masters**: Don't over-provision
- **HDFS for temp**: Faster than Cloud Storage for intermediate data
- **Cloud Storage for final**: Durable output

### Spark on Dataproc vs Spark on Dataflow

| Consideration | Dataproc | Dataflow |
|---------------|----------|----------|
| Existing Spark code | ✓ (minimal changes) | Rewrite to Beam |
| Spark ecosystem | ✓ (MLlib, GraphX) | No |
| Autoscaling | Good | Better |
| Management overhead | Some | None |
| Pricing | Per-second + fee | Per-second only |
| Best for | Spark workloads, migrations | New pipelines |

### Dataproc vs BigQuery

| Use Case | Dataproc | BigQuery |
|----------|----------|----------|
| SQL analytics | No | ✓ Best |
| Spark jobs | ✓ Best | No |
| ETL | ✓ | ✓ (SQL-based) |
| Machine learning | Spark MLlib | BQML |
| Existing Spark code | ✓ | No |
| Serverless | Dataproc Serverless | ✓ |

### Security Best Practices
- **VPC**: Run clusters in private VPC
- **Private Google Access**: Access GCS without external IPs
- **Encryption**: Default encryption at rest and in transit
- **CMEK**: Customer-managed encryption keys
- **[[gcp/iam|IAM]]**: Service accounts per cluster
- **Component Gateway**: Secure web UI access

### Monitoring & Observability
- **[[cloud-monitoring|Cloud Monitoring]]**: Cluster metrics (CPU, memory, HDFS)
- **Spark UI**: Via Component Gateway
- **YARN Resource Manager**: Job tracking
- **[[cloud-logging|Cloud Logging]]**: Driver and executor logs

### Migration Strategies
#### From On-Prem Hadoop
1. **Assess**: Inventory jobs, dependencies
2. **Data migration**: HDFS → Cloud Storage
3. **Metastore**: Hive metastore to Cloud SQL
4. **Test**: Run jobs on Dataproc
5. **Optimize**: Use preemptible workers, autoscaling
6. **Cutover**: Decommission on-prem

#### From EMR to Dataproc
- Very similar architectures

| EMR | Dataproc |
|---|---|
| s3:// | gs:// |
| EC2 instance types | GCE machine types |
| EMR steps | Dataproc jobs |
| S3 metastore | Cloud SQL metastore |

### Advanced Features
#### Workflow Templates
```text
Job A (Spark) → Job B (Hive) → Job C (Spark)
```
- Define dependencies as DAG
- Parameterized workflows
- Scheduled execution via [[cloud-scheduler|Cloud Scheduler]]

#### Personal Cluster
- One cluster per user
- Development and testing
- Automatic deletion after idle period

### Use Cases
✓ **Good for:**
- Migrating Spark/Hadoop workloads
- Spark MLlib, GraphX, Streaming
- Existing Spark code
- Data lake processing
- Complex ETL with Spark

✗ **Not ideal for:**
- SQL-only analytics (use [[bigquery|BigQuery]])
- New stream processing (use [[dataflow|Dataflow]])
- Long-running persistent clusters (consider Dataproc Serverless)

### Well-Architected Considerations
- **Operational Excellence**: Ephemeral clusters, workflow templates, monitoring
- **Reliability**: HA clusters, metastore persistence, Cloud Storage for data
- **Security**: VPC, CMEK, IAM, private Google access, Component Gateway
- **Performance**: Preemptible workers, autoscaling, local SSDs, right-sizing
- **Cost**: Ephemeral clusters, preemptible workers, per-second billing, autoscaling
- **Sustainability**: Autoscaling reduces waste, preemptible workers efficient
