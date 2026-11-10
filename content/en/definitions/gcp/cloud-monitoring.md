---
title: Cloud-monitoring
category: GCP
description: 'GCP note: Cloud-monitoring.'
tags:
- gcp
- operations
---

<!-- imported from ObsidianVault/studies/cloud-architecht/gcp/operations/cloud-monitoring.md. Edit the source, then run sync.py. -->

# Cloud-monitoring

`gcp` `operations`

## Cloud Monitoring
**AWS Equivalent:** [[management-and-governance-cloudwatch|CloudWatch]]
**Observability and monitoring** for Google Cloud and AWS

### Overview
- **Formerly Stackdriver Monitoring**
- Collects metrics, events, and metadata
- Dashboards, charts, alerts
- **Can monitor AWS and on-premises** resources
- Built-in monitoring for GCP services
- Custom metrics support

### Metrics
#### Built-in Metrics
- Automatically collected from GCP resources
- CPU, memory, disk, network for Compute Engine
- Request count, latency for Cloud Run, [[app-engine|App Engine]]
- Query metrics for [[bigquery|BigQuery]], Cloud SQL
- No configuration needed

#### Custom Metrics
- Application-specific metrics
- Use OpenTelemetry or Cloud Monitoring API
- Example: Business KPIs, custom latency, queue depth
- Charged per metric ingestion

### Workspaces
- **Scoping project** that contains dashboards, alerts, uptime checks
- Can monitor metrics from:
  - Host project
  - Up to 375 monitored projects
  - AWS accounts
- One workspace per scoping project

### Dashboards
- **Predefined dashboards**: Auto-created for GCP services
- **Custom dashboards**: Create charts, tables, scorecards
- **Charts types**: Line, stacked area, bar, heatmap
- **Filters**: Group by resource labels, metadata
- **Share**: JSON export/import, public or private

### Alerting
#### Alerting Policies
- **Condition**: Metric threshold, absence, forecast
- **Notification channels**: Email, SMS, PagerDuty, Slack, webhooks, [[pub-sub|Pub/Sub]]
- **Documentation**: Custom message with alert
- **Auto-close duration**: When condition no longer met

#### Alert Conditions
- **Metric threshold**: CPU > 80%
- **Metric absence**: No data for X minutes
- **Forecast**: Predict breach in future
- **Process health**: Compute Engine process monitoring
- **Uptime check**: Endpoint availability

### Uptime Checks
**AWS Equivalent:** CloudWatch Synthetics / Route 53 Health Checks
- Monitor endpoint availability from multiple locations
- **HTTP, HTTPS, TCP**
- **Check frequency: 1, 5, 10, 15 minutes**
- Global locations (us, europe, asia, south-america)
- Alert on failure
- Free tier: 1 million uptime checks/month

### Service Monitoring (SLO)
- Define Service Level Objectives (SLOs)
- Track Service Level Indicators (SLIs)
- Alert when error budget exhausted
- Availability-based or latency-based SLIs
- Error budget burn rate alerts

### Managed Service for Prometheus
- **Fully managed Prometheus-compatible monitoring**
- Collect metrics from GKE clusters
- PromQL query language
- Global query across regions/projects
- No operational overhead

### Ops Agent
**Successor to Monitoring Agent and Logging Agent**
- **Single agent** for metrics and logs
- Install on Compute Engine or on-prem VMs
- Collects system metrics (CPU, memory, disk, network)
- Collects application logs (Apache, NGINX, MySQL, etc.)
- OpenTelemetry-based

```bash
# Install Ops Agent
curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
sudo bash add-google-cloud-ops-agent-repo.sh --also-install
```

### Metrics Explorer
- Query and visualize metrics
- Filter, group, aggregate
- PromQL and MQL (Monitoring Query Language)
- Ad-hoc analysis without creating dashboards

### Pricing
- **GCP metrics**: Free for built-in metrics
- **Custom metrics**: $0.258 per metric per month (first 150 MB free)
- **AWS metrics**: $0.258 per metric per month
- **API calls**: $0.01 per 1,000 read calls
- **Uptime checks**: Free tier, then $0.30 per 1,000 checks

---

## ACE Level

### Essential Commands
```bash
# Install Ops Agent on Compute Engine
curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
sudo bash add-google-cloud-ops-agent-repo.sh --also-install

# Create uptime check
gcloud monitoring uptime create my-uptime-check \
  --resource-type=uptime-url \
  --resource-labels=host=example.com,path=/health \
  --period=60

# List alert policies
gcloud alpha monitoring policies list

# Create alert policy (YAML file)
gcloud alpha monitoring policies create --policy-from-file=policy.yaml

# List dashboards
gcloud monitoring dashboards list

# Create dashboard from JSON
gcloud monitoring dashboards create --config-from-file=dashboard.json
```

### Key Concepts for ACE
- Understanding workspace and monitored projects
- Installing Ops Agent on Compute Engine instances
- Creating and managing uptime checks
- Setting up basic alerting policies
- Using Metrics Explorer to visualize metrics
- Creating notification channels (email, SMS)
- Viewing predefined dashboards for GCP services
- Understanding built-in vs custom metrics

---

## PCA Level

### Architectural Patterns
#### Multi-Project Monitoring
```
Scoping Project (Workspace)
├── Monitored Project A (Production)
├── Monitored Project B (Staging)
└── Monitored Project C (Development)
```
- **One workspace, multiple monitored projects**
- Centralized dashboards and alerts
- Role-based access to metrics

#### Hybrid Monitoring
- Monitor GCP, AWS, and on-premises in **single pane of glass**
- Install Ops Agent on AWS EC2 or on-prem VMs
- Unified alerting across clouds
- Migration monitoring

### SLO-Based Alerting
- **Define SLO**: 99.9% availability
- **Error budget**: 0.1% = 43 minutes/month
- **Alert on burn rate**: 50% budget consumed in 1 hour
- **Proactive vs reactive**: Alert before SLO breach

#### Example SLI/SLO
```
SLI: Ratio of successful requests to total requests
SLO: 99.9% of requests succeed
Error Budget: 0.1% = ~43 minutes/month of downtime
Burn Rate Alert: 10x normal burn rate triggers page
```

### Custom Metrics Strategies
- **Use case**: Business metrics, application performance
- **OpenTelemetry**: Industry standard, portable
- **Cloud Monitoring API**: Direct API calls
- **Prometheus**: For GKE workloads
- **Cost**: Monitor metric cardinality

### Integration Patterns
#### Pub/Sub Integration
```
Alert → Pub/Sub → Cloud Function → Custom Action
```
- Programmatic alert handling
- Auto-remediation
- Ticket creation
- ChatOps integration

#### Incident Management
```
Alert → PagerDuty/Splunk On-Call → On-call engineer
```
- Escalation policies
- Incident tracking
- Integration with ITSM tools

### Performance Optimization
- **Metrics retention**: 6 weeks for most metrics
- **Aggregation**: Align metrics to reduce cardinality
- **Filters**: Use resource labels efficiently
- **Sampling**: For high-volume custom metrics

### Cost Optimization
- **Built-in metrics**: Free, use when possible
- **Custom metrics**: Monitor cardinality, aggregate
- **Uptime checks**: Use sparingly, leverage free tier
- **Logs-based metrics**: Alternative to custom metrics
- **Prometheus**: More cost-effective for GKE

### High Availability Monitoring
- **Multi-region uptime checks**: Detect regional outages
- **Redundant notification channels**: Multiple channels per alert
- **Workspace redundancy**: Backup dashboards/alerts as code
- **Avoid single points of failure**: Monitor the monitors

### Compliance & Audit
- **Audit logs**: Who created/modified alerts and dashboards
- **Access control**: [[iam|IAM]] roles for monitoring
  - `monitoring.viewer`: Read-only
  - `monitoring.editor`: Create/edit dashboards and alerts
  - `monitoring.admin`: Full access
  - `monitoring.metricWriter`: Write custom metrics

### Migration from CloudWatch
| CloudWatch | Cloud Monitoring |
|------------|------------------|
| Metrics | Metrics |
| CloudWatch Logs | [[cloud-logging|Cloud Logging]] |
| Alarms | Alert Policies |
| Dashboards | Dashboards |
| Synthetics | Uptime Checks |
| Contributor Insights | Metrics Explorer |
| Metric Streams | Pub/Sub Integration |

### Observability Triad
- **Metrics**: Cloud Monitoring
- **Logs**: [[cloud-logging|Cloud Logging]]
- **Traces**: [[cloud-trace|Cloud Trace]]
- Use together for complete observability

### Well-Architected Considerations
- **Operational Excellence**: Automated monitoring, SLO-based alerting, dashboards as code
- **Reliability**: Multi-region uptime checks, redundant notifications, proactive alerts
- **Security**: IAM-based access, audit logs, VPC SC for metrics API
- **Performance**: Right metric granularity, efficient queries, Managed Prometheus for GKE
- **Cost**: Use built-in metrics, optimize custom metrics, aggregate high-cardinality
- **Sustainability**: Monitor efficiency metrics, right-size resources based on metrics
