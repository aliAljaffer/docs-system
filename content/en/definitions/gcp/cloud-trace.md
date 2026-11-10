---
title: Cloud-trace
category: GCP
description: 'GCP note: Cloud-trace.'
tags:
- gcp
- operations
---

<!-- imported from ObsidianVault/studies/cloud-architecht/gcp/operations/cloud-trace.md. Edit the source, then run sync.py. -->

# Cloud-trace

`gcp` `operations`

## Cloud Trace
**AWS Equivalent:** AWS X-Ray
**Distributed tracing** for microservices and applications

### Overview
- **Analyze latency** in distributed systems
- Trace requests across services
- Identify performance bottlenecks
- Automatic integration with [[app-engine|App Engine]], Cloud Run, GKE
- OpenTelemetry support

### Traces and Spans
- **Trace**: End-to-end request journey
- **Span**: Single operation within a trace
- **Parent-child spans**: Call hierarchy
- **Span attributes**: Metadata (HTTP method, status code, etc.)

### Automatic Tracing
- **App Engine**: Automatically enabled
- **Cloud Run**: Automatically enabled
- **Cloud Functions**: Automatically enabled (via HTTP headers)
- **GKE**: Via OpenTelemetry or Istio service mesh
- **[[cloud-load-balancing|Load Balancers]]**: Propagate trace context

### Custom Tracing
- **OpenTelemetry** (recommended): Industry standard
- **Cloud Trace API**: Direct API calls
- **Trace client libraries**: Language-specific SDKs
- Use for: Custom applications, microservices, on-prem

### Trace Context Propagation
- **HTTP headers**: `X-Cloud-Trace-Context` or W3C Trace Context
- Must propagate between services for end-to-end tracing
- Format: `TRACE_ID/SPAN_ID;o=TRACE_TRUE`

```python
# Python example
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider

# Set up tracing
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(
    BatchSpanProcessor(CloudTraceSpanExporter())
)
trace.set_tracer_provider(tracer_provider)

# Create span
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("my-operation"):
    # Your code here
    pass
```

### Trace List View
- Overview of all traces
- Filter by:
  - Time range
  - Latency
  - HTTP method
  - URI
- Identify slow requests
- Drill down into specific traces

### Trace Details View
- **Waterfall diagram**: Visual span timeline
- **Span details**: Duration, attributes, events
- **RPC calls**: Service-to-service communication
- **Database queries**: SQL query timing
- Identify bottlenecks in request flow

### Analysis Reports
- **Latency distribution**: Percentiles (p50, p95, p99)
- **Request rate**: Requests per second
- **Most frequent URIs**: Top endpoints by volume
- **Daily latency**: Latency trends over time
- **Compare time periods** for regression detection

### Integration with Other Services
- **[[cloud-logging|Cloud Logging]]**: Jump from trace to logs
- **[[cloud-monitoring|Cloud Monitoring]]**: Metrics correlation
- **[[cloud-profiler|Cloud Profiler]]**: CPU/memory profiling
- Complete observability when combined

### Sampling
- **Automatic sampling**: ~1 request per 10 seconds per instance
- **Custom sampling**: Control sampling rate
- **Force trace**: Override sampling for specific requests
- Balance: Coverage vs cost

### Pricing
- **First 2.5 million spans/month: Free**
- Additional spans: $0.20 per million spans
- Retention: 30 days
- Very cost-effective compared to commercial APM tools

---

## ACE Level

### Key Concepts for ACE
- Understanding distributed tracing concepts (traces, spans)
- Viewing traces in Cloud Trace console
- Understanding automatic tracing for App Engine, Cloud Run
- Basic trace analysis and latency identification
- Understanding trace context propagation between services
- Using Trace List to find slow requests
- Viewing waterfall diagrams for request breakdown

### Using Cloud Trace Console
1. Navigate to Cloud Trace in console
2. Select time range
3. View trace list (all captured requests)
4. Click on a trace to see details
5. Analyze waterfall diagram
6. Check span details for specific operations

---

## PCA Level

### Architectural Patterns
#### Microservices Tracing
```
API Gateway → Auth Service → User Service → Database
           → Product Service → Inventory Service
           → Notification Service → Email Provider
```
- **Trace context propagated across all services**
- Identify bottlenecks in call chain
- Detect cascading failures
- Optimize critical paths

#### Hybrid Tracing
- On-prem service → GCP service tracing
- Multi-cloud tracing
- OpenTelemetry for portability
- Unified view across environments

### Performance Optimization
#### Identifying Bottlenecks
1. **Analyze percentiles**: Focus on p95, p99
2. **Waterfall analysis**: Find longest spans
3. **Compare time periods**: Detect regressions
4. **Group by URI**: Identify slow endpoints
5. **Database queries**: Optimize N+1 queries

#### Common Issues
- **Serial calls**: Convert to parallel
- **Database queries**: Add indexes, optimize SQL
- **External APIs**: Cache responses, use async
- **Cold starts**: Minimize for serverless
- **Network latency**: Co-locate services, use CDN

### Sampling Strategies
#### Fixed-Rate Sampling
```go
// Sample 10% of requests
sampler := trace.TraceIDRatioBased(0.1)
```

#### Adaptive Sampling
- Sample errors at 100%
- Sample slow requests at higher rate
- Sample fast, successful requests at lower rate
- Balance cost vs visibility

#### Force Tracing
```bash
# Include header in request to force tracing
X-Cloud-Trace-Context: TRACE_ID/SPAN_ID;o=1
```

### OpenTelemetry Implementation
**Recommended over proprietary libraries**
- Vendor-neutral, portable
- Auto-instrumentation for common frameworks
- Manual instrumentation for custom spans
- Export to Cloud Trace or other backends

```python
# OpenTelemetry setup
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configure provider
provider = TracerProvider()
processor = BatchSpanProcessor(CloudTraceSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Create custom spans
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("database-query") as span:
    span.set_attribute("query.type", "SELECT")
    result = db.query("SELECT * FROM users")
```

### Service Mesh Integration
#### Istio with GKE
- Automatic sidecar injection
- No code changes required
- Full trace visibility
- Service-to-service tracing

```yaml
# Enable Istio tracing
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  meshConfig:
    defaultConfig:
      tracing:
        stackdriver: {}
```

### Compliance & Security
- **PII in traces**: Avoid logging sensitive data in span attributes
- **Access control**: IAM roles
  - `cloudtrace.user`: Read traces
  - `cloudtrace.admin`: Full access
- **Trace data retention**: 30 days, cannot extend
- **VPC Service Controls**: Prevent trace data exfiltration

### Troubleshooting Workflows
#### Latency Spike Investigation
1. **Time range**: Select spike period
2. **Filter**: High-latency traces only
3. **Compare**: Normal vs spike traces
4. **Identify**: New spans or slower spans
5. **Correlate**: Check logs, metrics
6. **Root cause**: Database, external API, code change

#### Error Investigation
1. **Filter**: Error status codes
2. **Trace details**: Find failing span
3. **Span attributes**: Error message, stack trace
4. **Logs**: Jump to Cloud Logging for details
5. **Fix**: Deploy corrected code, verify with tracing

### Cost Optimization
- **Sampling**: Don't trace 100% of requests
- **Retention**: 30 days only, archive if needed
- **Span attributes**: Don't over-instrument
- **Free tier**: 2.5M spans/month usually sufficient
- **Compare vs commercial APM**: Cloud Trace much cheaper

### Migration from AWS X-Ray
| AWS X-Ray | Cloud Trace |
|-----------|-------------|
| Traces | Traces |
| Segments | Spans |
| Subsegments | Child spans |
| Annotations | Span attributes |
| Metadata | Span attributes |
| X-Ray daemon | OpenTelemetry Collector |
| Service map | Trace waterfall |

### Multi-Cloud Tracing
- OpenTelemetry for portability
- Export to multiple backends
- Unified view across clouds
- Flexible migration path

### Best Practices
1. **Always propagate trace context**: Ensure end-to-end visibility
2. **Use OpenTelemetry**: Future-proof, vendor-neutral
3. **Meaningful span names**: Descriptive, not generic
4. **Add attributes**: HTTP method, status, user ID (non-PII)
5. **Error tracking**: Mark failed spans
6. **Sampling strategy**: Balance cost vs coverage
7. **Combine with logs**: Use trace ID in log messages

### Well-Architected Considerations
- **Operational Excellence**: Proactive latency monitoring, automated analysis
- **Reliability**: Identify failures, cascade detection, SLO tracking
- **Security**: No PII in traces, IAM controls, VPC SC
- **Performance**: Bottleneck identification, query optimization, p99 latency
- **Cost**: Sampling, free tier optimization, compare to commercial APM
- **Sustainability**: Optimize inefficient code paths, reduce waste
