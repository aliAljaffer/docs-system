---
title: Cloud-profiler
category: GCP
description: 'GCP note: Cloud-profiler.'
tags:
- gcp
- operations
---

<!-- imported from ObsidianVault/studies/cloud-architecht/gcp/operations/cloud-profiler.md. Edit the source, then run sync.py. -->

# Cloud-profiler

`gcp` `operations`

## Cloud Profiler
**AWS Equivalent:** No direct equivalent (closest: CodeGuru Profiler)
**Continuous CPU and memory profiling** for production apps

### Overview
- **Low-overhead profiling** (< 0.5% CPU)
- Continuous profiling in production
- Identify performance bottlenecks
- Optimize resource usage and costs
- Supports multiple languages

### Supported Platforms
- Compute Engine
- GKE
- [[app-engine|App Engine]]
- Cloud Run
- Cloud Functions (2nd gen)
- On-premises via agent

### Supported Languages
- **Go**: CPU, heap, contention, thread
- **Java**: CPU, heap, contention, wall time
- **Python**: CPU, wall time
- **Node.js**: Heap, wall time
- **.NET**: CPU, heap

### Profile Types
#### CPU Profile
- Where CPU time is spent
- Hot functions
- Optimization opportunities
- **Most common profile type**

#### Heap Profile
- Memory allocation patterns
- Memory leaks
- Large object allocations
- Garbage collection pressure

#### Contention Profile
- Lock contention in multi-threaded apps
- Thread synchronization issues
- Parallelism bottlenecks

#### Wall Time Profile
- Time including I/O waits
- Blocking operations
- Network/disk latency

### How It Works
1. Agent instruments application code
2. **Statistical sampling** (not exhaustive tracing)
3. Samples sent to Cloud Profiler service
4. Aggregated into flame graphs
5. Analyze in Cloud Console

### Flame Graphs
- Visual representation of call stacks
- Width = time/memory consumed
- Click to zoom into specific functions
- Compare time periods
- Filter by service, version, zone

### Enable Profiling
#### App Engine
```yaml
# app.yaml (Python)
runtime: python312
entrypoint: gunicorn -b :$PORT main:app

# Install profiler
# requirements.txt
google-cloud-profiler
```

```python
# main.py
import googlecloudprofiler

googlecloudprofiler.start(
    service='my-app-engine-service',
    service_version='1.0.0',
)
```

#### Cloud Run / Cloud Functions
```python
import googlecloudprofiler

try:
    googlecloudprofiler.start(
        service='my-cloud-run-service',
        service_version='1.0.0',
    )
except (ValueError, NotImplementedError) as exc:
    print(exc)
```

#### GKE
```yaml
# Deployment manifest
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: app
        env:
        - name: GOOGLE_CLOUD_PROFILER_ENABLE
          value: "1"
```

#### Compute Engine
```bash
# Install profiler library for your language
pip install google-cloud-profiler  # Python
```

### Pricing
- **Completely free** (no charges)
- No data ingestion costs
- No storage costs
- Unlimited profiles

---

## ACE Level

### Key Concepts for ACE
- Understanding what Cloud Profiler does (CPU/memory profiling)
- Enabling profiler in App Engine, Cloud Run, Cloud Functions
- Basic flame graph interpretation
- Understanding profile types (CPU, heap, wall time)
- Viewing profiles in Cloud Console
- Understanding low-overhead nature (safe for production)

### Using Cloud Profiler Console
1. Navigate to Cloud Profiler in console
2. Select service and version
3. Choose profile type (CPU, heap, etc.)
4. View flame graph
5. Click on functions to zoom in
6. Identify hot paths (wide sections)

---

## PCA Level

### Architectural Use Cases
#### Cost Optimization
- Identify CPU-intensive functions
- Reduce compute costs by optimizing hot paths
- Right-size instances based on actual usage
- Eliminate wasteful allocations

#### Performance Optimization
- Find slow database queries
- Optimize serialization/deserialization
- Reduce GC pressure (Java, Go)
- Eliminate unnecessary computations

#### Memory Leak Detection
- Heap profiles over time
- Growing allocations
- Unreleased resources
- Connection pool leaks

### Analysis Patterns
#### Finding CPU Bottlenecks
1. **Select CPU profile**
2. **Identify widest flame**
3. **Drill down**: Click to expand
4. **Compare**: Before/after optimization
5. **Measure impact**: Real-world latency improvement

#### Memory Optimization
1. **Heap profile**: See allocations
2. **Large objects**: Optimize or cache
3. **Allocation rate**: Reduce garbage
4. **Object lifecycle**: Reuse pools
5. **Compare versions**: Track improvements

#### Contention Issues
1. **Contention profile**: Lock waiting
2. **Identify hot locks**: Widest flames
3. **Optimize**: Reduce critical sections
4. **Consider alternatives**: Lock-free structures
5. **Verify**: Re-profile after changes

### Comparison Across Versions
```
Version 1.0 CPU profile vs Version 1.1 CPU profile
- Identify performance regressions
- Validate optimizations
- A/B test different implementations
```

### Multi-Service Analysis
- Profile each microservice independently
- Identify service-level bottlenecks
- Correlate with [[cloud-trace|Cloud Trace]] for end-to-end view
- Optimize highest-impact services first

### Best Practices
1. **Always profile production**: Real workload, real patterns
2. **Service labels**: Unique per service for clarity
3. **Version labels**: Track changes over time
4. **Compare wisely**: Same time of day, similar load
5. **Low-hanging fruit**: Optimize widest flames first
6. **Measure results**: Use monitoring to verify impact
7. **Continuous profiling**: Don't profile once and forget

### Integration with Observability
```
Performance Issue Workflow:
1. Cloud Monitoring: Identify latency spike
2. Cloud Trace: Find slow service
3. Cloud Profiler: Identify hot function
4. Cloud Logging: Check error logs
5. Fix, deploy, verify
```

### Language-Specific Considerations
#### Java
- **Heap profile**: GC overhead, object lifecycle
- **Contention**: Synchronization bottlenecks
- **JVM tuning**: Based on profile insights

#### Python
- **GIL contention**: Multi-threading limitations
- **I/O waits**: Consider async/await
- **C extensions**: Native code profiling limited

#### Go
- **Goroutine profiles**: Concurrency patterns
- **Memory allocations**: Reduce GC pressure
- **Escape analysis**: Keep on stack vs heap

#### Node.js
- **Event loop blocking**: Identify synchronous code
- **Memory leaks**: Closure issues
- **Buffer usage**: Large object allocations

### Cost Reduction Case Studies
#### Example: E-commerce API
- **Before**: 100 vCPUs, high CPU usage
- **Profiled**: Found JSON serialization bottleneck
- **Optimized**: Used faster library
- **After**: 60 vCPUs, same performance
- **Savings**: 40% reduction in compute costs

#### Example: Data Processing Pipeline
- **Before**: 200 GB memory instances
- **Profiled**: Memory leak in connection pool
- **Fixed**: Properly closed connections
- **After**: 100 GB memory instances
- **Savings**: 50% reduction in memory costs

### Security Considerations
- **No sensitive data in profiles**: Function names, not data
- **Access control**: [[security-iam|IAM]] roles
  - `cloudprofiler.user`: View profiles
  - `cloudprofiler.admin`: Full access
- **VPC Service Controls**: Prevent profile data exfiltration
- **Production profiling**: Safe, low overhead

### Debugging Workflows
#### Out of Memory (OOM) Errors
1. **Enable heap profiling**
2. **Identify large allocations**
3. **Check for leaks**: Growing over time
4. **Optimize**: Reduce footprint, add limits
5. **Verify**: Monitor memory usage

#### High CPU Usage
1. **Enable CPU profiling**
2. **Find hot functions**
3. **Optimize algorithms**: O(n²) → O(n log n)
4. **Cache results**: Avoid recomputation
5. **Verify**: Monitor CPU metrics

### Comparison with Commercial Profilers
| Feature | Cloud Profiler | Commercial APM |
|---------|----------------|----------------|
| Cost | Free | $$$ expensive |
| Overhead | < 0.5% | Variable |
| Production-safe | ✓ | Depends |
| Multi-language | ✓ | ✓ |
| Flame graphs | ✓ | ✓ |
| Integration | GCP services | Multi-cloud |

### Migration from AWS
- **No equivalent to Cloud Profiler in AWS** (basic alternative: CodeGuru Profiler, limited availability)
- CodeGuru Profiler: Java/Python only, higher cost
- Cloud Profiler: More languages, free, lower overhead

### Well-Architected Considerations
- **Operational Excellence**: Continuous profiling, proactive optimization
- **Reliability**: Identify issues before they cause outages, low-overhead
- **Security**: No data exposure, IAM controls, safe for production
- **Performance**: Direct CPU/memory optimization, real-world profiling
- **Cost**: Free tool, enables significant cost reductions through optimization
- **Sustainability**: Optimize resource usage, reduce waste, smaller carbon footprint
