---
title: Security-command-center
category: GCP
description: 'GCP note: Security-command-center.'
tags:
- gcp
- security
---


# Security-command-center

`gcp` `security`

## Security Command Center (SCC)
**AWS Equivalent:** AWS Security Hub + GuardDuty

**Centralized security and risk management** - Vulnerability scanning, threat detection, and compliance monitoring

### Overview
- **Unified security dashboard** for GCP resources
- **Asset inventory** across organization
- **Vulnerability detection** and remediation
- **Threat detection** using Google's threat intelligence
- **Compliance monitoring** against standards
- **Security posture management** (CSPM)

### Tiers
#### Standard (Free)
- Asset discovery and inventory
- Basic security findings
- Vulnerability scanning for web apps
- Limited integrations
- Single project visibility

#### Premium (Paid)
- **Organization-level visibility**
- **Event Threat Detection** (ETD)
- **Container Threat Detection** (CTD)
- **Virtual Machine Threat Detection** (VMTD)
- **Security Health Analytics**
- **Web Security Scanner**
- Compliance monitoring (CIS, PCI-DSS, NIST, ISO)
- Integration with third-party tools (Palo Alto, Qualys, etc.)
- Export to SIEM (Splunk, Chronicle)
- **Recommended for production environments**

### Core Features
#### Asset Discovery & Inventory
- Automatic discovery of all GCP resources
- Asset relationships and dependencies
- Asset properties and metadata
- Search and filter capabilities
- Export to BigQuery for analysis

**Supported Asset Types:**
- Compute Engine VMs, disks, snapshots
- Cloud Storage buckets
- BigQuery datasets
- Cloud SQL instances
- GKE clusters
- IAM policies
- Service accounts
- 100+ resource types

#### Security Health Analytics
**Detectors (80+):**
- Open firewall rules
- Public Cloud Storage buckets
- Unencrypted resources
- Overly permissive IAM roles
- Disabled security features
- Missing security controls

**Categories:**
- **PUBLIC_IP_ADDRESS**: Resources with public IPs
- **OPEN_FIREWALL**: Overly permissive firewall rules
- **WEAK_PASSWORD_POLICY**: Weak IAM policies
- **AUDIT_LOGGING_DISABLED**: Missing audit logs
- **SSL_NOT_ENFORCED**: Unencrypted connections

#### Event Threat Detection (Premium)
**Uses Google threat intelligence to detect:**
- Malware
- Cryptomining
- Brute force SSH attacks
- Leaked credentials
- Data exfiltration
- Anomalous IAM activity
- Privilege escalation

**Detection Sources:**
- Cloud Logging
- VPC Flow Logs
- DNS logs
- Threat intelligence feeds

#### Container Threat Detection (Premium)
**GKE security monitoring:**
- Added malicious binary
- Added malicious library
- Reverse shell
- Execution of privileged container
- Execution of non-standard interpreter
#### Virtual Machine Threat Detection (Premium)
**Detects threats on Compute Engine VMs:**
- Malware execution
- Coin mining
- Outbound DDoS
- Unauthorized network scanning
**Requires:** OS Config agent installed
### Findings
#### Finding Structure
- **Category**: Type of security issue
- **Severity**: Critical, High, Medium, Low
- **State**: Active, Inactive, Muted
- **Resource**: Affected GCP resource
- **Source**: Detector that generated finding
- **Event Time**: When issue was detected
#### Finding Sources
**Built-in Sources:**
- Security Health Analytics
- Event Threat Detection
- Container Threat Detection
- VM Threat Detection
- Web Security Scanner
**Third-Party Integrations:**
- Palo Alto Networks (Prisma Cloud)
- Qualys
- Tenable
- Rapid7
- RedLock
- Twistlock

#### Finding States
- **ACTIVE**: Issue exists and needs attention
- **INACTIVE**: Issue resolved automatically
- **MUTED**: Manually marked as non-issue

### Notifications
**Export Options:**
- **Pub/Sub**: Real-time notifications
- **Email**: Alerts to security team
- **SIEM**: Export to Splunk, Chronicle, etc.
- **Cloud Functions**: Automated remediation

**Example Workflow:**
```
Finding Created -> Pub/Sub -> Cloud Function -> Automated Fix
                             -> Email -> Security Team
```

### Compliance Monitoring (Premium)
**Supported Standards:**
- CIS Google Cloud Computing Platform Foundation Benchmark
- PCI-DSS v3.2.1
- NIST 800-53
- ISO 27001
- HIPAA
- GDPR

**Compliance Dashboard:**
- Overall compliance score
- Failing controls
- Remediation guidance
- Historical trends

### Web Security Scanner
- Automatic vulnerability scanning for web applications
- Detects: XSS, SQL injection, outdated libraries, mixed content
- Scan types: Light, normal, deep
- **Standard tier: Limited scans**
- **Premium tier: Unlimited scans**

### Security Marks
- Custom labels on assets and findings
- Used for: Environment tagging, ownership, risk classification
- Searchable and filterable
- Integration with automation

```bash
# Add security mark to finding
gcloud scc findings update FINDING_ID \
  --source=SOURCE_ID \
  --security-marks="environment=production,owner=security-team"
```

### SIEM Integration
**Export to Chronicle (Google's SIEM):**
- Native integration
- Real-time threat detection
- Historical analysis
- Correlation with other security data

**Export to Splunk/Other SIEM:**
```bash
# Create Pub/Sub topic
gcloud pubsub topics create scc-findings

# Create SCC notification config
gcloud scc notifications create siem-export \
  --organization=ORG_ID \
  --pubsub-topic=projects/PROJECT_ID/topics/scc-findings \
  --filter="state=\"ACTIVE\""

# Splunk consumes from Pub/Sub
```

### Remediation Workflows
#### Automated Remediation
```python
# Cloud Function triggered by SCC finding
def remediate_public_bucket(event, context):
    import base64
    import json
    from google.cloud import storage

    # Parse Pub/Sub message
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    finding = json.loads(pubsub_message)

    # Check if public bucket finding
    if finding['category'] == 'PUBLIC_BUCKET_ACL':
        bucket_name = finding['resourceName'].split('/')[-1]

        # Remove public access
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        bucket.make_private()

        print(f"Remediated public bucket: {bucket_name}")
```

#### Manual Remediation
- SCC provides remediation guidance
- Step-by-step instructions
- Linked to affected resources
- gcloud commands for fixes

### Asset Groups
- Logical grouping of assets
- Filter by project, resource type, labels
- Monitor specific subsets
- Custom dashboards per group

### Pricing (Premium Tier)
- **Security Health Analytics**: Free
- **Event Threat Detection**: $5 per project per month
- **Container Threat Detection**: $5 per GKE node per month
- **VM Threat Detection**: $0.015 per VM per hour
- **Web Security Scanner**: $0.015 per scan

**Free Trial:** 90 days for Premium tier

### SCC vs AWS Security Hub Comparison
| Feature | SCC | AWS Security Hub |
|---------|-----|------------------|
| Asset inventory | Yes | Yes |
| Threat detection | Yes (ETD, CTD, VMTD) | Yes (GuardDuty integration) |
| Compliance monitoring | Yes (CIS, PCI, NIST, etc.) | Yes (multiple standards) |
| Third-party integrations | Yes | Yes (AWS Partner integrations) |
| Pricing model | Per project/node/VM | Per finding ingestion |
| Automatic remediation | Manual setup (Cloud Functions) | Manual (Lambda, Systems Manager) |
| SIEM export | Pub/Sub | EventBridge |
| Organization-wide | Yes (Premium) | Yes |

---

## ACE Level

### Essential gcloud Commands
```bash
# Enable Security Command Center API
gcloud services enable securitycenter.googleapis.com

# List all assets (organization level)
gcloud scc assets list ORGANIZATION_ID

# List assets for specific project
gcloud scc assets list ORGANIZATION_ID \
  --filter="securityCenterProperties.resourceProject=projects/PROJECT_ID"

# List findings
gcloud scc findings list ORGANIZATION_ID \
  --source=SOURCE_ID

# List active findings
gcloud scc findings list ORGANIZATION_ID \
  --source=SOURCE_ID \
  --filter="state=\"ACTIVE\""

# Describe a finding
gcloud scc findings describe FINDING_ID \
  --source=SOURCE_ID

# Update finding state (mute)
gcloud scc findings update FINDING_ID \
  --source=SOURCE_ID \
  --state=MUTED

# Create notification config
gcloud scc notifications create NOTIFICATION_ID \
  --organization=ORG_ID \
  --pubsub-topic=projects/PROJECT_ID/topics/TOPIC_NAME \
  --filter="severity=\"HIGH\" OR severity=\"CRITICAL\""

# List notification configs
gcloud scc notifications list ORGANIZATION_ID

# Delete notification
gcloud scc notifications delete NOTIFICATION_ID \
  --organization=ORG_ID

# List sources
gcloud scc sources list ORGANIZATION_ID

# Describe source
gcloud scc sources describe SOURCE_ID \
  --organization=ORG_ID
```

### Key Concepts for ACE
- Understanding SCC Standard vs Premium tiers
- Viewing asset inventory across projects
- Understanding security findings and severities
- Creating and managing notification configs
- Filtering findings by state, severity, category
- Muting false positive findings
- Understanding Security Health Analytics detectors
- Viewing compliance status (Premium)
- Basic remediation of common findings (public buckets, open firewalls)
- Integrating SCC with Pub/Sub for notifications

---

## PCA Level

### Architectural Patterns
#### Centralized Security Monitoring
```
Architecture:
- Organization-level SCC (Premium)
- All projects report findings
- Central security team monitors dashboard
- Automated remediation via Cloud Functions
- SIEM integration for correlation

Benefits:
- Single pane of glass
- Consistent security posture
- Faster incident response
- Compliance visibility
```

#### Multi-Tier Security Response
```
Severity-Based Response:
- Critical/High: Immediate Pub/Sub -> PagerDuty -> On-call engineer
- Medium: Email to security team + ticket (JIRA/ServiceNow)
- Low: Weekly digest report

Automated Response:
- Public buckets: Auto-remediate (Cloud Function)
- Open SSH (0.0.0.0/0): Alert + auto-block after confirmation
- Malware detected: Isolate VM (remove from network)
```

#### Compliance-Driven Architecture
```
For PCI-DSS Compliance:
1. Enable SCC Premium
2. Enable PCI-DSS compliance monitoring
3. Create security marks for CDE (Cardholder Data Environment)
4. Filter findings for CDE assets
5. Automated remediation for CDE violations
6. Export compliance reports to auditors

Continuous Compliance:
- Daily compliance scans
- Auto-remediation of known issues
- Quarterly compliance reports
- Audit trail in Cloud Logging
```

### Advanced Finding Management
#### Custom Finding Filters
```bash
# Critical findings in production
gcloud scc findings list ORG_ID \
  --source=SOURCE_ID \
  --filter="severity=\"CRITICAL\" AND securityMarks.marks.environment=\"production\""

# Findings for specific asset type
gcloud scc findings list ORG_ID \
  --source=SOURCE_ID \
  --filter="resourceName:\"//storage.googleapis.com/\""

# Findings created in last 24 hours
gcloud scc findings list ORG_ID \
  --source=SOURCE_ID \
  --filter="eventTime>\"$(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%S)Z\""
```

#### Bulk Finding Operations
```python
# Python script to mute low-severity findings in dev
from google.cloud import securitycenter

client = securitycenter.SecurityCenterClient()
org_name = f"organizations/{org_id}"

# List findings
findings = client.list_findings(
    request={
        "parent": f"{org_name}/sources/{source_id}",
        "filter": "severity=\"LOW\" AND securityMarks.marks.environment=\"dev\""
    }
)

# Mute findings
for finding in findings:
    finding.finding.state = securitycenter.Finding.State.MUTED
    client.set_finding_state(
        request={
            "name": finding.finding.name,
            "state": securitycenter.Finding.State.MUTED
        }
    )
    print(f"Muted: {finding.finding.name}")
```

### Automated Remediation Patterns
#### Public Cloud Storage Bucket
```python
# Cloud Function triggered by SCC finding
def remediate_public_bucket(data, context):
    import base64
    import json
    from google.cloud import storage

    # Decode Pub/Sub message
    finding = json.loads(base64.b64decode(data['data']).decode('utf-8'))

    if finding['finding']['category'] == 'PUBLIC_BUCKET_ACL':
        bucket_name = finding['finding']['resourceName'].split('/')[-1]

        # Remove public access
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        bucket.make_private()

        # Update finding to inactive
        # (SCC will auto-update on next scan)

        return f"Remediated: {bucket_name}"
```

#### Open Firewall Rule
```python
# Cloud Function to remediate open SSH rule
def remediate_open_ssh(data, context):
    import base64
    import json
    from googleapiclient import discovery

    finding = json.loads(base64.b64decode(data['data']).decode('utf-8'))

    if finding['finding']['category'] == 'OPEN_FIREWALL':
        # Extract firewall rule details
        rule_name = finding['finding']['sourceProperties']['firewall_rule_name']
        project_id = finding['finding']['resourceName'].split('/')[1]

        # Update firewall rule to restrict source
        compute = discovery.build('compute', 'v1')
        firewall = compute.firewalls().get(project=project_id, firewall=rule_name).execute()

        # Replace 0.0.0.0/0 with corporate IP range
        firewall['sourceRanges'] = ['203.0.113.0/24']  # Corporate network

        compute.firewalls().update(
            project=project_id,
            firewall=rule_name,
            body=firewall
        ).execute()

        return f"Remediated firewall rule: {rule_name}"
```

### SIEM Integration Architecture
```
SCC Findings -> Pub/Sub -> Dataflow -> BigQuery -> Data Studio Dashboard
                         -> Cloud Function -> JIRA ticket
                         -> Splunk HEC (HTTP Event Collector)
                         -> Chronicle SIEM
```

**Example Dataflow Pipeline:**
```python
# Ingest SCC findings into BigQuery
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

def run():
    options = PipelineOptions()

    with beam.Pipeline(options=options) as p:
        (p
         | 'Read from Pub/Sub' >> beam.io.ReadFromPubSub(topic='projects/PROJECT/topics/scc-findings')
         | 'Parse JSON' >> beam.Map(lambda x: json.loads(x))
         | 'Transform' >> beam.Map(transform_finding)
         | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
             'PROJECT:DATASET.scc_findings',
             schema=TABLE_SCHEMA
         ))

def transform_finding(finding):
    return {
        'finding_id': finding['finding']['name'],
        'category': finding['finding']['category'],
        'severity': finding['finding']['severity'],
        'resource': finding['finding']['resourceName'],
        'timestamp': finding['finding']['eventTime']
    }
```

### Threat Detection Configuration
#### Event Threat Detection Settings
```bash
# Enable specific ETD detectors
gcloud scc settings services modules update \
  --service=event-threat-detection \
  --module=malware \
  --enablement-state=ENABLED \
  --organization=ORG_ID

# Enable all ETD modules
for module in malware cryptomining brute_force leaked_credentials; do
  gcloud scc settings services modules update \
    --service=event-threat-detection \
    --module=$module \
    --enablement-state=ENABLED \
    --organization=ORG_ID
done
```

#### Container Threat Detection Setup
```bash
# Enable Container Threat Detection for GKE cluster
gcloud container clusters update CLUSTER_NAME \
  --enable-security-posture \
  --zone=ZONE

# SCC automatically detects container threats
# No additional configuration needed
```

### Compliance Reporting Automation
```bash
# Export compliance report to BigQuery
bq mk --dataset compliance_reports

# Create scheduled query for daily compliance report
bq query --use_legacy_sql=false --schedule="every 24 hours" \
--display_name="Daily PCI-DSS Compliance" \
--destination_table=compliance_reports.pci_dss_daily \
--replace \
'SELECT
  category,
  severity,
  state,
  COUNT(*) as finding_count
FROM `PROJECT.scc_findings.findings`
WHERE compliance_standard = "PCI-DSS"
  AND DATE(event_time) = CURRENT_DATE()
GROUP BY category, severity, state'
```

### Security Posture Dashboard
**Custom Dashboard in Looker/Data Studio:**
- Total assets by type
- Active findings by severity
- Compliance score trends
- Top 10 vulnerable resources
- MTTR (Mean Time To Remediation)
- Finding velocity (new vs resolved)

**BigQuery Views:**
```sql
-- Asset inventory summary
CREATE VIEW scc_views.asset_summary AS
SELECT
  asset_type,
  security_center_properties.resource_project,
  COUNT(*) as count
FROM `PROJECT.scc_assets.assets`
GROUP BY asset_type, security_center_properties.resource_project;

-- Critical findings by project
CREATE VIEW scc_views.critical_findings AS
SELECT
  security_center_properties.resource_project,
  category,
  COUNT(*) as count
FROM `PROJECT.scc_findings.findings`
WHERE severity = 'CRITICAL'
  AND state = 'ACTIVE'
GROUP BY security_center_properties.resource_project, category;
```

### Third-Party Integration Examples
#### Palo Alto Prisma Cloud
```bash
# Add Prisma Cloud as finding source
# Prisma findings appear alongside GCP native findings
# Unified view of cloud security posture
```

#### Qualys VMDR
```bash
# Integrate Qualys vulnerability scans
# VM vulnerabilities appear in SCC
# Correlate with GCP-native findings
```

### Multi-Organization Strategy
**For holding companies with multiple GCP orgs:**
```
Challenge: Each org has separate SCC
Solution:
1. Enable SCC Premium on each org
2. Export findings to central Pub/Sub (each org)
3. Dataflow aggregates findings
4. Central BigQuery dataset
5. Unified dashboard across all orgs
```

### Cost Optimization
**Premium Tier Costs:**
- Enable selectively: Premium for production org only
- Standard for dev/test orgs
- Use project-level Event Threat Detection (not org-wide)
- Disable VM Threat Detection on non-critical VMs
- Use Web Security Scanner judiciously

**Reduce Finding Noise:**
- Mute low-severity dev environment findings
- Use security marks to exclude test resources
- Focus on high-value assets

### Migration from AWS Security Hub
**Comparison:**
```
AWS Security Hub Findings -> GCP SCC Findings
AWS GuardDuty -> GCP Event Threat Detection
AWS Inspector -> GCP Security Health Analytics
AWS Config -> GCP Asset Inventory
```

**Migration Steps:**
1. Enable SCC Premium in GCP organization
2. Map AWS Security Hub findings to SCC categories
3. Recreate automation (Lambda -> Cloud Functions)
4. Update SIEM integrations (EventBridge -> Pub/Sub)
5. Train security team on SCC interface
6. Parallel run for 30 days
7. Cutover to SCC as primary tool

### Advanced Use Cases
#### Insider Threat Detection
```
Monitoring:
- Unusual IAM activity (Event Threat Detection)
- Data exfiltration attempts (VPC Flow Logs + ETD)
- After-hours access (IAM conditions + SCC findings)
- Privilege escalation (IAM policy changes)

Response:
- Alert security team (Pub/Sub -> Email/Slack)
- Automatically revoke elevated permissions
- Isolate affected resources
- Create incident ticket
```

#### Supply Chain Security
```
For container workloads:
1. Binary Authorization: Only signed images
2. Container Threat Detection: Monitor running containers
3. SCC findings: Vulnerable base images
4. Automated remediation: Update to patched base image

Integration:
- Artifact Registry vulnerability scanning
- Container Analysis API
- SCC findings for outdated images
- Cloud Build auto-rebuild on CVE detection
```

### Well-Architected Considerations
- **Operational Excellence**: Automated finding triage, playbooks for common findings, regular security reviews, IaC for SCC configuration
- **Reliability**: Multi-region SIEM export, redundant notification channels, regular compliance scans, backup of security configurations
- **Security**: Enable all Premium features, automated remediation for critical findings, VPC SC integration, regular access reviews, continuous compliance monitoring
- **Performance**: Efficient finding filters, BigQuery for large-scale analysis, caching for dashboards, batch remediation scripts
- **Cost**: Selective Premium enablement, mute non-actionable findings, optimize Web Security Scanner usage, use free Standard tier for non-critical projects
