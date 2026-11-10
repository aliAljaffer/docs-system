---
title: Cloud-logging
category: GCP
description: 'GCP note: Cloud-logging.'
tags:
- gcp
- operations
---


# Cloud-logging

`gcp` `operations`

## Cloud Logging
**AWS Equivalent:** [[management-and-governance-cloudtrail|CloudTrail]] + [[management-and-governance-cloudwatch|CloudWatch Logs]]
**Centralized logging** for Google Cloud

### Overview
- **Formerly Stackdriver Logging**
- Stores, searches, analyzes, and alerts on log data
- **Automatically collects** logs from GCP services
- Custom logs via API or agents
- **400 days retention** by default (configurable)

### Log Types
#### Platform Logs (Automatic)
- **Admin Activity logs**: Who did what, when (400-day retention, **free**)
- **Data Access logs**: Who accessed what data (30-day default, **not free**, **disabled by default**)
- **System Event logs**: GCP system events (400-day retention, free)
- **Policy Denied logs**: Security policy violations (30-day default)

#### Component Logs
- Application logs from [[app-engine|App Engine]], [[gcp/cloud-run|Cloud Run]], [[gcp/gke|GKE]]
- [[gcp/compute-engine|Compute Engine]] logs via Ops Agent
- Container logs from GKE
- Load balancer logs

### Log Router
- **Default sink**: Stores logs in Cloud Logging
- **Custom sinks**: Route logs to:
  - [[gcp/cloud-storage|Cloud Storage]] (archival)
  - [[bigquery|BigQuery]] (analysis)
  - [[pub-sub|Pub/Sub]] (streaming)
  - Another project (centralized logging)
- **Inclusion filters**: Which logs to route
- **Exclusion filters**: Which logs to drop (cost savings)

### Log Buckets
- **Storage location for logs**
- Regional or global
- Custom retention (1 day - 3650 days)
- Two default buckets:
  - `_Required`: Audit logs, 400-day retention, **cannot delete**
  - `_Default`: All other logs, 30-day retention
- Custom buckets for different retention needs

### Log-Based Metrics
**AWS Equivalent:** CloudWatch Logs Metric Filters
- Create metrics from log entries
- **System-defined metrics** (error count, bytes) - free
- **User-defined metrics** (custom patterns) - charged
- Use in [[cloud-monitoring|Cloud Monitoring]] alerts
- Example: Count 5xx errors, track specific user actions

### Structured Logging
- JSON-formatted logs
- Better filtering and analysis
- Severity levels: DEFAULT, DEBUG, INFO, NOTICE, WARNING, ERROR, CRITICAL, ALERT, EMERGENCY
- Special fields: `message`, `severity`, `timestamp`, `httpRequest`

### Log Explorer
- **Query logs** with filters
- **Time range** selection
- **Resource type** filtering
- **Severity** filtering
- **Advanced filters**: Regular expressions, field comparisons
- **Histogram**: Log volume over time
- **Save queries**: Reuse common queries

### Query Language
```
# Find errors in a specific service
resource.type="cloud_run_revision"
resource.labels.service_name="my-service"
severity>=ERROR

# Find slow requests
resource.type="http_load_balancer"
httpRequest.latency>5s

# Exclude health check logs
NOT httpRequest.requestUrl=~"/health"
```

### Logs Analytics
- **BigQuery-style SQL queries** on logs
- Join with BigQuery datasets
- **Upgraded log buckets** required
- Create views, run complex analytics
- More powerful than Log Explorer

### Error Reporting
[[error-reporting]]
- Automatic error grouping
- Stack trace analysis
- Email/mobile notifications
- Integrated with Cloud Logging
- Supports multiple languages

### Pricing
- **Ingestion**: $0.50 per GB (first 50 GB/project/month free)
- **Storage**: $0.01 per GB/month
- **Logs Analytics**: Additional charges for upgraded buckets
- **Admin Activity logs**: **Always free**
- **Exclusion filters**: Reduce costs by dropping unnecessary logs

---

## ACE Level

### Essential Commands
```bash
# Read logs
gcloud logging read "resource.type=gce_instance" --limit=10

# Read logs with filter
gcloud logging read \
  "resource.type=cloud_run_revision AND severity>=ERROR" \
  --limit=50 \
  --format=json

# List log buckets
gcloud logging buckets list

# Create log bucket
gcloud logging buckets create my-bucket \
  --location=us-central1 \
  --retention-days=365

# Create log sink to Cloud Storage
gcloud logging sinks create my-sink \
  storage.googleapis.com/my-bucket \
  --log-filter='resource.type="gce_instance"'

# Create log sink to BigQuery
gcloud logging sinks create bq-sink \
  bigquery.googleapis.com/projects/PROJECT/datasets/DATASET \
  --log-filter='severity>=ERROR'

# Create log sink to Pub/Sub
gcloud logging sinks create pubsub-sink \
  pubsub.googleapis.com/projects/PROJECT/topics/TOPIC \
  --log-filter='resource.type="cloud_run_revision"'

# Create exclusion filter
gcloud logging sinks update _Default \
  --add-exclusion=name=health-checks,filter='httpRequest.requestUrl="/health"'

# Write log entry
gcloud logging write my-log "Test message" --severity=INFO

# List log-based metrics
gcloud logging metrics list
```

### Key Concepts for ACE
- Understanding default log buckets (_Required, _Default)
- Creating log sinks to export logs
- Using Log Explorer to search and filter logs
- Configuring log retention via log buckets
- Creating exclusion filters to reduce costs
- Enabling Data Access audit logs
- Installing Ops Agent for Compute Engine logs
- Creating basic log-based metrics

---

## PCA Level

### Architectural Patterns
#### Centralized Logging
```
Production Project → Aggregator Sink → Central Logging Project
Staging Project    → Aggregator Sink → Central Logging Project
Dev Project        → Aggregator Sink → Central Logging Project
```
- **One project for all logs**
- Centralized access control
- Unified log analysis
- Cost attribution per source project

#### Log Archival Strategy
```
All Logs → Exclusion Filter (drop debug) → _Default Bucket (30 days)
                                         → Cloud Storage Sink (long-term)
Critical Logs → Custom Bucket (1 year)
Audit Logs → _Required Bucket (400 days, automatic)
```

#### Real-Time Log Processing
```
Logs → Pub/Sub Sink → Dataflow → BigQuery/Bigtable
                    → Cloud Function → Alert/Action
```

### Security & Compliance
#### Audit Logging Best Practices
- **Enable Data Access logs for sensitive resources** (GCS, BigQuery)
- **Admin Activity**: Always enabled, can't disable
- **System Events**: Always enabled
- **Data Access**: Enable per-service, understand costs
- **Policy Denied**: Enable for security monitoring

#### Log Access Control
- **Roles**:
  - `logging.viewer`: Read logs
  - `logging.privateLogViewer`: Read all logs including Data Access
  - `logging.admin`: Full access
- **Bucket-level permissions**: Restrict access to specific buckets
- **VPC Service Controls**: Prevent log exfiltration

### Cost Optimization Strategies
#### Exclusion Filters
```yaml
# Exclude health checks
filter: 'httpRequest.requestUrl="/health"'

# Exclude successful requests
filter: 'httpRequest.status<400'

# Exclude debug logs
filter: 'severity<WARNING'

# Sampling (keep 10%)
filter: 'sample(insertId, 0.1)'
```

#### Tiered Retention
- **_Default bucket**: 30 days for most logs
- **Cloud Storage**: Long-term archival, cheapest
- **BigQuery**: Logs needing analysis
- **Custom buckets**: Different retention per log type

### Analytics Patterns
#### Security Analysis
```sql
-- Find failed login attempts (Logs Analytics)
SELECT
  timestamp,
  protopayload_auditlog.authenticationInfo.principalEmail,
  protopayload_auditlog.status.code
FROM `PROJECT.BUCKET._AllLogs`
WHERE protopayload_auditlog.status.code != 0
  AND protopayload_auditlog.methodName LIKE '%login%'
ORDER BY timestamp DESC
```

#### Cost Analysis
```sql
-- Find top storage users by request volume
SELECT
  resource.labels.bucket_name,
  COUNT(*) as request_count
FROM `PROJECT.BUCKET._AllLogs`
WHERE resource.type = 'gcs_bucket'
GROUP BY bucket_name
ORDER BY request_count DESC
```

### Integration Patterns
#### SIEM Integration
```
Cloud Logging → Pub/Sub → Splunk/Chronicle/Datadog
```
- Export to security information systems
- Correlation with other data sources
- Advanced threat detection

#### Incident Response
```
Error Logs → Log-based Alert → Pub/Sub → Cloud Function → PagerDuty
```
- Automated incident creation
- Context-rich alerts
- Runbook automation

### High Availability
- **Regional buckets**: Store logs in specific region
- **Multi-region sinks**: Export to multi-region Cloud Storage
- **Redundant sinks**: Multiple destinations for critical logs
- **Cross-project sinks**: Survive project deletion

### Performance Optimization
- **Structured logging**: Easier to query, faster searches
- **Log sampling**: Reduce volume for high-frequency logs
- **Appropriate retention**: Don't over-retain
- **Logs Analytics**: For complex queries, use SQL instead of filters

### Compliance Requirements
#### GDPR/PII Handling
- **De-identify logs**: Remove PII before storing
- **Access control**: Restrict Data Access log viewing
- **Retention limits**: Don't exceed required retention
- **Right to deletion**: Process for log deletion requests

#### Industry-Specific
- **HIPAA**: Enable Data Access logs, encrypt sinks
- **PCI DSS**: Enable all audit logs, 1-year retention minimum
- **SOC 2**: Admin Activity logs, change tracking

### Migration from CloudWatch Logs
| CloudWatch Logs | Cloud Logging |
|-----------------|---------------|
| Log Groups | Log names |
| Log Streams | Not required (resources auto-tagged) |
| Metric Filters | Log-based metrics |
| Subscriptions | Log sinks |
| Insights | Logs Analytics |
| Retention | Log buckets |

### Troubleshooting Patterns
#### Application Debugging
1. **Log Explorer**: Find relevant logs
2. **Correlation**: Use trace ID to link requests
3. **Severity filtering**: Focus on errors/warnings
4. **Time correlation**: Compare with metrics/traces

#### Performance Investigation
1. **Latency logs**: HTTP request duration
2. **Resource logs**: CPU/memory from VMs
3. **Custom metrics**: Application-specific timing
4. **Distributed tracing**: Use Cloud Trace for multi-service

### Well-Architected Considerations
- **Operational Excellence**: Centralized logging, structured logs, automated analysis
- **Reliability**: Redundant sinks, multi-region storage, log-based alerts
- **Security**: Data Access logs, IAM controls, VPC SC, log immutability
- **Performance**: Appropriate retention, exclusion filters, Logs Analytics for complex queries
- **Cost**: Exclusion filters, sampling, right-sized retention, archive to Cloud Storage
- **Sustainability**: Only log what's needed, aggregate/sample high-volume logs
