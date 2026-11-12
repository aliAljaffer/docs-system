---
title: Cloud-composer
category: GCP
description: 'GCP note: Cloud-composer.'
tags:
- gcp
- data
---


# Cloud-composer

`gcp` `data`

## Cloud Composer
**AWS Equivalent:** Amazon Managed Workflows for Apache Airflow (MWAA)
**Managed Apache Airflow** for orchestrating data pipelines

### Overview
- Fully managed Apache Airflow service
- Workflow orchestration for **batch data pipelines**
- **DAG-based** (Directed Acyclic Graph) workflows
- Python-based workflow definitions
- Integrates with all GCP services

### Key Concepts
#### DAG (Directed Acyclic Graph)
- Defines workflow dependencies
- Tasks execute in order based on dependencies
- Written in Python
- Version-controlled

#### Operators
- **BashOperator**: Run bash commands
- **PythonOperator**: Execute Python functions
- **BigQueryOperator**: Run BigQuery queries
- **DataflowOperator**: Launch Dataflow jobs
- **GCSOperator**: Cloud Storage operations
- 100+ operators for GCP and external services

### Components
- **Airflow Web Server**: UI for monitoring
- **Airflow Scheduler**: Triggers task execution
- **Workers**: Execute tasks
- **Cloud SQL**: Metadata database
- **Cloud Storage**: DAG storage, logs
- **GKE**: Underlying infrastructure (managed by Google)

### Use Cases
✓ **ETL pipelines**: Extract, transform, load workflows
✓ **Data lake management**: Orchestrate data ingestion
✓ **ML pipelines**: Training, evaluation, deployment
✓ **Batch processing**: Scheduled data processing
✓ **Multi-cloud workflows**: Orchestrate AWS + GCP + on-prem

### Cloud Composer vs Workflows
| Feature | Cloud Composer | [[workflows|Workflows]] |
|---------|----------------|----------|
| Complexity | Complex (Apache Airflow) | Simple (YAML/JSON) |
| Learning curve | Steeper | Easier |
| Use case | Data pipelines, batch | Service orchestration |
| Language | Python (DAGs) | YAML/JSON |
| Cost | Higher (GKE cluster) | Lower (serverless) |
| Best for | Data engineering teams | Serverless orchestration |

### Pricing
- Based on underlying resources:
  - GKE cluster (workers)
  - Cloud SQL (metadata DB)
  - Cloud Storage (logs, DAGs)
- Small environment: ~$300/month
- Medium: ~$500-1000/month
- **Always running** (not serverless)

---

## ACE Level

### Essential Commands
```bash
# Create environment
gcloud composer environments create my-env \
  --location=us-central1 \
  --machine-type=n1-standard-1 \
  --node-count=3

# List environments
gcloud composer environments list --locations=us-central1

# Upload DAG
gcloud composer environments storage dags import \
  --environment=my-env \
  --location=us-central1 \
  --source=my_dag.py

# Run DAG
gcloud composer environments run my-env \
  --location=us-central1 \
  dags trigger -- my_dag_id

# Delete environment
gcloud composer environments delete my-env --location=us-central1
```

### Sample DAG
```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'etl_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    extract = BashOperator(
        task_id='extract_data',
        bash_command='gsutil cp gs://source-bucket/* /tmp/data/'
    )

    transform = BigQueryExecuteQueryOperator(
        task_id='transform_data',
        sql='SELECT * FROM dataset.table WHERE date = CURRENT_DATE()',
        use_legacy_sql=False
    )

    extract >> transform  # Define dependency
```

### Key Concepts for ACE
- Understanding DAG structure
- Creating and uploading DAGs
- Basic operators (Bash, Python, BigQuery)
- Triggering DAGs manually
- Viewing execution logs in Airflow UI
- Accessing Airflow web UI

---

## PCA Level

### Architectural Patterns
#### Daily ETL Pipeline
```text
Cloud Scheduler → Trigger DAG → Extract (Cloud Storage)
                              → Transform (Dataflow)
                              → Load (BigQuery)
                              → Data Quality Checks
                              → Notify (Pub/Sub)
```

#### ML Training Pipeline
```text
DAG → Data Prep (Dataproc)
   → Feature Engineering (Dataflow)
   → Train Model (Vertex AI)
   → Evaluate Model
   → Deploy if improved (Vertex AI Endpoint)
   → Notify team (email)
```

#### Multi-Cloud Data Pipeline
```text
DAG → Extract from AWS S3 (boto3)
   → Process in GCP (Dataflow)
   → Load to Snowflake
   → Archive to Cloud Storage
```

### High Availability
- **Multi-zone GKE cluster** (managed by Composer)
- Cloud SQL with HA configuration
- **Regional Cloud Storage** for DAG/logs
- Automatic failover for workers

### Performance Optimization
- **Worker autoscaling**: Scale based on task queue
- **Parallel tasks**: Design DAGs for parallelism
- **Task prioritization**: Airflow priority weights
- **SubDAGs**: Reusable workflow components
- **XCom**: Efficient inter-task communication

### Cost Optimization
- **Right-size environment**: Small for dev, medium for prod
- **Autoscaling workers**: Scale down when idle
- **Use Cloud Scheduler + Cloud Functions** for simple workflows (cheaper)
- **Consider Workflows** for service orchestration (serverless, cheaper)
- **Committed Use Discounts**: For GKE nodes

### Security Best Practices
- **Private IP**: Environment in private VPC
- **IAM**: Least privilege for service account
- **Secrets**: Use Secret Manager, not variables
- **VPC Service Controls**: Prevent data exfiltration
- **Workload Identity**: For GKE pods
- **Access control**: Airflow RBAC for UI access

### Integration Patterns
#### With BigQuery
```python
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyTableOperator,
    BigQueryInsertJobOperator,
)

create_table = BigQueryCreateEmptyTableOperator(
    task_id='create_table',
    dataset_id='my_dataset',
    table_id='my_table',
    schema_fields=[...]
)

load_data = BigQueryInsertJobOperator(
    task_id='load_data',
    configuration={...}
)
```

#### With Dataflow
```python
from airflow.providers.google.cloud.operators.dataflow import DataflowTemplatedJobStartOperator

run_dataflow = DataflowTemplatedJobStartOperator(
    task_id='run_dataflow',
    template='gs://dataflow-templates/latest/GCS_Text_to_BigQuery',
    parameters={...}
)
```

#### With Vertex AI
```python
from airflow.providers.google.cloud.operators.vertex_ai import (
    CreateCustomTrainingJobOperator
)

train_model = CreateCustomTrainingJobOperator(
    task_id='train_model',
    display_name='my-training-job',
    container_uri='gcr.io/my-project/training:latest',
    ...
)
```

### Monitoring & Observability
- **Airflow UI**: Task status, logs, DAG visualization
- **[[cloud-monitoring|Cloud Monitoring]]**: Environment health, worker CPU/memory
- **[[cloud-logging|Cloud Logging]]**: Airflow logs, task logs
- **Email alerts**: On task failure, SLA miss
- **Slack integration**: Workflow notifications

### Best Practices
1. **Idempotent tasks**: Tasks can run multiple times safely
2. **Error handling**: Proper retries and failure callbacks
3. **SLAs**: Set task execution time limits
4. **Testing**: Test DAGs locally before deployment
5. **Version control**: Store DAGs in Git
6. **Dependencies**: Pin Python package versions
7. **Secrets management**: Use Secret Manager
8. **Modularity**: Reusable components, SubDAGs

### Migration Strategies
#### From Self-Managed Airflow
- Export existing DAGs
- Modify for Cloud Composer operators
- Upload to Cloud Storage
- Test in Composer environment
- Gradual migration DAG-by-DAG

#### From AWS Step Functions / MWAA
- Rewrite Step Functions as Airflow DAGs
- MWAA DAGs mostly compatible
- Update AWS operators to GCP operators
- Test thoroughly

### Use Case Decision Matrix
| Use Case | Cloud Composer | [[workflows|Workflows]] | [[cloud-scheduler|Cloud Scheduler]] |
|----------|----------------|----------|------------------|
| Complex data pipelines | ✓ Best | ✗ | ✗ |
| Simple service orchestration | Overkill | ✓ Best | ✗ |
| Scheduled jobs | ✓ | ✓ | ✓ Best |
| ML pipelines | ✓ | Limited | ✗ |
| Multi-cloud orchestration | ✓ | Limited | ✗ |
| Cost-sensitive | ✗ (expensive) | ✓ (cheap) | ✓ (cheapest) |

### Well-Architected Considerations
- **Operational Excellence**: DAG version control, monitoring, automated testing
- **Reliability**: Multi-zone deployment, retries, SLAs, backfill capability
- **Security**: VPC, Workload Identity, Secret Manager, IAM, RBAC
- **Performance**: Parallel tasks, worker autoscaling, efficient operators
- **Cost**: Right-size environment, autoscaling, consider Workflows for simple cases
- **Sustainability**: Autoscaling reduces idle resources, efficient task execution
