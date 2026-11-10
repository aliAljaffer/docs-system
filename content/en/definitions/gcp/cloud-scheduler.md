---
title: Cloud-scheduler
category: GCP
description: 'GCP note: Cloud-scheduler.'
tags:
- gcp
- management
---

<!-- imported from ObsidianVault/studies/cloud-architecht/gcp/management/cloud-scheduler.md. Edit the source, then run sync.py. -->

# Cloud-scheduler

`gcp` `management`

## Cloud Scheduler
**AWS Equivalent:** Amazon EventBridge Scheduler (formerly CloudWatch Events)
**Fully managed cron job scheduler**

### Overview
- Schedule tasks on cron schedule
- Target: HTTP endpoint, [[gcp/pub-sub|Pub/Sub]], [[app-engine|App Engine]]
- **Serverless**, no infrastructure
- Retry logic built-in

### Targets
- **HTTP/HTTPS**: POST to any endpoint
- **Pub/Sub**: Publish message to topic
- **App Engine HTTP**: Invoke App Engine app

### Cron Syntax
```
* * * * *
│ │ │ │ │
│ │ │ │ └─ Day of week (0-6, Sun-Sat)
│ │ │ └─── Month (1-12)
│ │ └───── Day of month (1-31)
│ └─────── Hour (0-23)
└───────── Minute (0-59)
```

Examples:
- `0 9 * * 1-5`: Every weekday at 9am
- `*/10 * * * *`: Every 10 minutes
- `0 0 1 * *`: First of every month

### Time Zones
- Specify timezone (e.g., `America/New_York`)
- Important for DST handling

### Retry Configuration
- Max retry attempts
- Retry deadline
- Min/max backoff duration

### Pricing
- **3 free jobs**
- $0.10 per job per month (beyond free tier)
- Very cheap

---

## ACE Level

### Essential Commands
```bash
# Create job (HTTP target)
gcloud scheduler jobs create http my-job \
  --schedule="0 9 * * *" \
  --uri="https://example.com/endpoint" \
  --http-method=POST

# Create job (Pub/Sub target)
gcloud scheduler jobs create pubsub my-pubsub-job \
  --schedule="*/10 * * * *" \
  --topic=my-topic \
  --message-body="Run batch job"

# List jobs
gcloud scheduler jobs list

# Run job immediately
gcloud scheduler jobs run my-job

# Delete job
gcloud scheduler jobs delete my-job
```

### Key Concepts for ACE
- Creating scheduled jobs
- Understanding cron syntax
- Triggering Pub/Sub, HTTP endpoints
- Running jobs manually for testing

---

## PCA Level

### Use Cases
- Trigger [[gcp/cloud-functions|Cloud Functions]] or [[gcp/cloud-run|Cloud Run]] on schedule
- Daily backups
- Periodic data exports
- Batch job orchestration
- Report generation

### Integration Patterns
```
Cloud Scheduler → Pub/Sub → Cloud Function → BigQuery (export)
                         → Dataflow (batch job)
```

### Well-Architected
- **Operational Excellence**: Automated scheduling
- **Reliability**: Retry logic, managed service
- **Cost**: Very cheap, pay-per-job
