---
title: error-reporting
category: GCP
description: 'GCP note: Error-reporting.'
tags:
- gcp
- operations
---


# error-reporting

## Error Reporting
**Automatic error aggregation** and alerting

**AWS Equivalent:** CloudWatch Logs Insights + manual error grouping

### Overview
- Automatically groups similar errors
- Real-time notifications
- Integrated with [[cloud-logging|Cloud Logging]]
- Stack trace analysis
- Supports multiple languages and platforms

### Automatic Error Detection

| Platform | Error detection |
|---|---|
| [[app-engine|App Engine]] | Automatic |
| [[gcp/cloud-functions|Cloud Functions]] | Automatic |
| [[gcp/cloud-run|Cloud Run]] | Automatic |
| [[gcp/gke|GKE]] | Via logs |
| [[gcp/compute-engine|Compute Engine]] | Via client libraries or logs |

### Error Grouping
- **Groups similar errors automatically**
- Uses stack trace similarity
- Aggregates count, first/last seen
- Reduces noise
- Focuses on unique issues

### Supported Platforms
#### Automatic Support
- App Engine Standard
- App Engine Flexible
- Cloud Functions
- Cloud Run

#### Manual Instrumentation
- Compute Engine
- GKE
- On-premises
- AWS/Azure

### Supported Languages

| Language | How errors are reported |
|---|---|
| **Python** | Auto-detect exceptions |
| **Java** | Auto-detect exceptions |
| **Node.js** | Auto-detect errors |
| **Go** | Via error reporting library |
| **.NET** | Via error reporting library |
| **Ruby** | Via error reporting library |
| **PHP** | Via error reporting library |

### Error Details

| Field | Meaning |
|---|---|
| **Stack trace** | Full call stack |
| **Error message** | Exception text |
| **Affected users** | Approximate count |
| **First seen** | When error first occurred |
| **Last seen** | Most recent occurrence |
| **Occurrences** | Total count |
| **Versions** | Which app versions affected |

### Notifications
- **Email**: Alert on new errors
- **Mobile**: Push notifications
- **Frequency**: Real-time, hourly digest, daily digest
- Configure per user

### Integration with Logging
- Errors automatically linked to logs
- Click to view full log entry
- Context around error
- Correlate with other events

### Manual Error Reporting
```python
# Python example
from google.cloud import error_reporting

client = error_reporting.Client()

try:
    risky_operation()
except Exception as e:
    client.report_exception()
```

```javascript
// Node.js example
const {ErrorReporting} = require('@google-cloud/error-reporting');
const errors = new ErrorReporting();

try {
  riskyOperation();
} catch (err) {
  errors.report(err);
}
```

### Error Reporting via Logs
```json
{
  "severity": "ERROR",
  "message": "Error message",
  "@type": "type.googleapis.com/google.devtools.clouderrorreporting.v1beta1.ReportedErrorEvent",
  "context": {
    "httpRequest": {
      "method": "GET",
      "url": "http://example.com"
    }
  }
}
```

### Pricing
- **Completely free** (no charges)
- Unlimited errors
- No data retention limits

---

## ACE Level

### Key Concepts for ACE
- Understanding automatic error detection for App Engine, Cloud Run, Cloud Functions
- Viewing error groups in Error Reporting console
- Understanding error details (stack trace, count, first/last seen)
- Setting up email notifications for new errors
- Linking errors to Cloud Logging for context
- Understanding how errors are automatically grouped

### Using Error Reporting Console
1. Navigate to Error Reporting
2. View list of error groups
3. Click on error group for details
4. View stack trace
5. Click "View logs" to see full log entries
6. Set up notifications

---

## PCA Level

### Architectural Integration
#### Error Monitoring Pipeline
```text
Application → Error Reporting (auto-group)
           → Notifications (email/mobile)
           → Ticket System (via webhook)
           → Cloud Monitoring (metrics)
```

#### Incident Response Workflow
```text
1. Error Reporting: New error detected
2. Notification: Alert on-call engineer
3. Cloud Logging: Investigate context
4. Cloud Trace: Analyze request path
5. Cloud Profiler: Identify performance issue
6. Fix, deploy, verify
```

### Error Rate Monitoring
- Track error count over time
- Alert on error spike
- Correlate with deployments
- SLO tracking (error rate budget)

### Best Practices
1. **Structured logging**: Include context in error logs
2. **Version labels**: Track errors by deployment version
3. **User impact**: Include user ID (non-PII) in context
4. **Error messages**: Clear, actionable descriptions
5. **Stack traces**: Don't catch and swallow
6. **Notifications**: Set up for critical errors only
7. **Resolution**: Mark errors as resolved when fixed

### Integration Patterns
#### With Incident Management
```text
Error Reporting → Pub/Sub → Cloud Function → PagerDuty
                                           → Jira
                                           → Slack
```

#### With SLO Monitoring
- Use error rate in [[cloud-monitoring|SLO]] definitions
- Error budget alerts
- Automated rollback on error spike

### Multi-Service Error Tracking
- Each microservice reports separately
- Unified view in Error Reporting
- Service-specific error patterns
- Cross-service error correlation

### Compliance & Security
- **No PII in error messages**: Sanitize before logging
- **Access control**: [[gcp/iam|IAM]] roles
  - `errorreporting.user`: View errors
  - `errorreporting.admin`: Full access
- **VPC Service Controls**: Prevent data exfiltration

### Cost Optimization (N/A)
- Error Reporting is completely free
- No limits on errors or storage
- Use without concern for costs

### Comparison with AWS

| AWS | GCP |
|-----|-----|
| Manual CloudWatch Logs analysis | Automatic error grouping |
| CloudWatch Alarms | Built-in notifications |
| Third-party tools needed | Native Error Reporting |
| Costs | Free |

### Error Resolution Workflow
1. **Identify**: Error Reporting detects and groups
2. **Prioritize**: By frequency and user impact
3. **Investigate**: Stack trace, logs, traces
4. **Fix**: Deploy corrected code
5. **Verify**: Error count drops to zero
6. **Resolve**: Mark as resolved in console

### Proactive Error Handling
- Don't wait for users to report
- Real-time error detection
- Faster time to resolution
- Improved user experience

### Well-Architected Considerations
- **Operational Excellence**: Automated error detection, grouped errors, fast resolution
- **Reliability**: Proactive issue detection, error rate tracking, SLO integration
- **Security**: No PII exposure, IAM controls, secure error reporting
- **Performance**: Identify performance errors, correlate with profiler/trace
- **Cost**: Free service, reduces manual monitoring costs
- **Sustainability**: Identify waste (retry storms, resource leaks)
