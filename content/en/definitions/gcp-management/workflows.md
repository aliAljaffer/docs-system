---
title: Workflows
category: GCP Management
description: 'GCP Management note: Workflows.'
tags:
- gcp
- management
---

<!-- imported from ObsidianVault/studies/cloud-architecht/gcp/management/workflows.md. Edit the source, then run sync.py. -->

# Workflows

`gcp` `management`

## Workflows
**AWS Equivalent:** AWS Step Functions
**Orchestrate** services with serverless workflows

### Overview
- Define workflows as YAML/JSON
- Orchestrate Google Cloud and HTTP APIs
- **Built-in error handling** and retries
- Pay per step execution

### Workflow Definition
```yaml
main:
  steps:
  - call_api:
      call: http.get
      args:
        url: https://api.example.com/data
      result: api_response
  - process_data:
      call: process_function
      args:
        data: ${api_response.body}
  - store_result:
      call: googleapis.bigquery.v2.datasets.tables.insertAll
      args:
        projectId: ${sys.get_env("GOOGLE_CLOUD_PROJECT_ID")}
        datasetId: my_dataset
        tableId: my_table
        rows: ${processed_data}
```

### Features
- **Conditional logic**: If/switch statements
- **Loops**: For/while loops
- **Error handling**: Try/catch/retry
- **Subworkflows**: Modular workflows
- **Parallel steps**: Concurrent execution
- **Wait**: Sleep between steps

### Use Cases
- **ETL orchestration**: Multiple data processing steps
- **API orchestration**: Chain multiple API calls
- **Batch processing**: Coordinate batch jobs
- **Human approval workflows**: Wait for manual approval

### Pricing
- **2,000 internal steps free/month**
- $0.01 per 1,000 internal steps
- External steps (API calls) free

---

## ACE Level

### Essential Commands
```bash
# Deploy workflow
gcloud workflows deploy my-workflow --source=workflow.yaml

# Execute workflow
gcloud workflows execute my-workflow

# List workflows
gcloud workflows list

# Describe workflow
gcloud workflows describe my-workflow
```

### Key Concepts for ACE
- Defining workflows in YAML
- Deploying and executing workflows
- Understanding steps and transitions

---

## PCA Level

### Orchestration Patterns
```
Workflows → Cloud Functions → Process data
         → Dataflow → Transform data
         → BigQuery → Load data
```

### Error Handling
- Try/catch blocks
- Retry policies
- Exponential backoff
- Dead letter handling

### vs Cloud Composer
| Feature | Workflows | Cloud Composer |
|---------|-----------|----------------|
| Complexity | Simple | Complex (Airflow DAGs) |
| Cost | Very cheap | More expensive |
| Overhead | None (serverless) | Managed Airflow cluster |
| Use case | Simple orchestration | Complex data pipelines |

### Well-Architected
- **Operational Excellence**: Declarative workflows, version control
- **Reliability**: Error handling, retries
- **Cost**: Pay-per-step, very cheap
