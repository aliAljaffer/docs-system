---
title: App-engine
category: GCP
description: '✗ Consider alternatives:'
tags:
- gcp
- compute
---

<!-- imported from ObsidianVault/studies/cloud-architecht/gcp/compute/app-engine.md. Edit the source, then run sync.py. -->

# App-engine

`gcp` `compute`

## App Engine
**AWS Equivalent:** [[compute-beanstalk|Elastic Beanstalk]]
**Fully managed PaaS** for web applications and APIs

### Environments
#### Standard Environment
- **Sandbox execution** with runtime restrictions
- **Second-level granular scaling**
- **Scales to zero** (no instances when no traffic)
- **Faster startup** (milliseconds)
- **Free tier eligible**
- Specific runtime versions
- Some limitations (no SSH, limited system access)
- Better for: Web apps, APIs, mobile backends
#### Flexible Environment
- **Docker containers** on [[compute-engine|Compute Engine]]
- **Minute-level granular scaling**
- **Minimum 1 instance always running**
- Slower startup (minutes)
- No free tier
- Any runtime (custom Docker)
- Full system access, SSH available
- Better for: Containerized apps, background workers, existing Docker apps

### Standard vs Flexible Comparison
| Feature | Standard | Flexible |
|---------|----------|----------|
| Instance startup | Milliseconds | Minutes |
| Scale to zero | ✓ | ✗ (min 1) |
| Free tier | ✓ | ✗ |
| SSH access | ✗ | ✓ |
| Custom runtimes | Limited | ✓ (Docker) |
| Pricing | Instance hours | vCPU/memory |
| Write to disk | /tmp only | ✓ |
| Background threads | Limited | ✓ |

### Application Structure
```
my-app/
├── app.yaml          # Configuration file
├── main.py           # Application code
├── requirements.txt  # Dependencies (Python)
└── static/          # Static files
```

### app.yaml Configuration
```yaml
runtime: python312
entrypoint: gunicorn -b :$PORT main:app

env_variables:
  KEY: "value"

automatic_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.65

handlers:
- url: /static
  static_dir: static
- url: /.*
  script: auto
```

### Scaling Types
#### Automatic Scaling
- Based on request rate, latencies, or other metrics
- **Default for Standard environment**
- Scale to zero in Standard, min 1 in Flexible
- Target CPU utilization, requests per second

#### Manual Scaling
- Fixed number of instances
- No automatic scaling
- You control instance count
- Good for: Background workers, predictable load

#### Basic Scaling
- Dynamic based on requests
- Instances created on-demand
- Idle instances shut down
- Max instance limit

### Versions & Traffic Splitting
- Each deployment creates a **version**
- Multiple versions can run simultaneously
- **Traffic splitting**: Route percentage of traffic to versions
  - IP splitting
  - Cookie splitting
  - Random splitting
- Blue/green deployments
- Canary testing
- A/B testing

### Services (Microservices)
- App Engine app can have multiple **services** (formerly modules)
- Each service can have multiple versions
- Independent scaling per service
- Different runtimes per service
- Example: `default` service, `api` service, `admin` service

### Routing
- Default: `https://PROJECT_ID.REGION_ID.r.appspot.com`
- Service: `https://SERVICE-dot-PROJECT_ID.REGION_ID.r.appspot.com`
- Version: `https://VERSION-dot-SERVICE-dot-PROJECT_ID.REGION_ID.r.appspot.com`
- Custom domains via [[gcp/cloud-load-balancing|Cloud Load Balancing]]

### Runtimes
**Standard Environment:**
- Python 3.7-3.12
- Java 11, 17, 21
- Node.js 16, 18, 20
- Go 1.16-1.21
- PHP 7.4, 8.1-8.2
- Ruby 3.0-3.2

**Flexible Environment:**
- Any language via custom Docker

### Static Files
- Served directly from edge caches
- No instance processing required
- Configured in app.yaml handlers
- Faster, cheaper than dynamic

### Cron Jobs
- Schedule tasks via `cron.yaml`
- HTTP GET/POST to your app URLs
- Max frequency: every 1 minute
- Timezone support
- **Runs even if no instances** (Standard)

```yaml
# cron.yaml
cron:
- description: "daily summary"
  url: /tasks/summary
  schedule: every 24 hours
```

### Task Queues & Cloud Tasks
- Cloud Tasks for asynchronous work
- Background processing
- Rate limiting
- Retry logic

### Memcache (Standard Only)
- Shared in-memory cache
- **Shared memcache**: Free, no guarantee
- **Dedicated memcache**: Guaranteed space, paid
- **Deprecated, use [[gcp/memorystore|Memorystore]] instead**

### Security
- **[[gcp/iam|Cloud IAM]]** for access control
- **App Engine firewall**: IP allowlist/denylist
- **SSL/TLS**: Automatic for `.appspot.com` domains
- **[[gcp/iam|Service accounts]]**: Each app runs with service account
- **Identity-Aware Proxy**: User authentication

### Regional Deployment
- **App Engine app is regional** (not global, not zonal)
- Cannot change region after creation
- Multi-region not supported
- Choose region at app creation

---

## ACE Level

### Essential gcloud Commands
```bash
# Deploy application
gcloud app deploy

# Deploy to specific version without promoting
gcloud app deploy --no-promote --version=v2

# View app
gcloud app browse

# View logs
gcloud app logs tail -s default

# Describe app
gcloud app describe

# List services
gcloud app services list

# List versions
gcloud app versions list

# Split traffic
gcloud app services set-traffic default --splits=v1=0.5,v2=0.5

# Migrate traffic
gcloud app services set-traffic default --splits=v2=1 --migrate

# Delete version
gcloud app versions delete v1

# Deploy cron jobs
gcloud app deploy cron.yaml

# Deploy dispatch rules
gcloud app deploy dispatch.yaml
```

### Key Concepts for ACE
- Deploying applications to App Engine
- Understanding Standard vs Flexible environments
- Managing versions and traffic splitting
- Configuring app.yaml for scaling and environment
- Using services for microservices architecture
- Setting up cron jobs with cron.yaml
- Viewing application logs and metrics
- Managing environment variables and runtime configuration

---

## PCA Level

### Architectural Considerations
#### When to Choose App Engine
✓ **Good for:**
- Traditional web applications
- Rapid prototyping
- Simple deployment without infrastructure management
- Applications with variable traffic
- Multi-service (microservices) apps

✗ **Consider alternatives:**
- Complex container orchestration → [[gke|GKE]]
- Simple HTTP containers → [[cloud-run|Cloud Run]]
- Event-driven → [[cloud-functions|Cloud Functions]]
- Full VM control → [[compute-engine|Compute Engine]]

### Multi-Service Architecture
```
default service (frontend)
api service (REST API)
admin service (admin panel)
worker service (background tasks)
```
- Each service scales independently
- Different runtimes per service
- Dispatch rules for routing

### Traffic Management Patterns
#### Blue/Green Deployment
```bash
# Deploy new version without traffic
gcloud app deploy --no-promote --version=blue

# Test new version
curl https://blue-dot-default-dot-PROJECT.r.appspot.com

# Migrate all traffic at once
gcloud app services set-traffic default --splits=blue=1 --migrate
```

#### Canary Deployment
```bash
# Gradually shift traffic
gcloud app services set-traffic default --splits=v1=90,v2=10
# Monitor, then increase v2
gcloud app services set-traffic default --splits=v1=50,v2=50
# Full migration
gcloud app services set-traffic default --splits=v2=1
```

#### A/B Testing
- Cookie-based splitting for consistent user experience
- Random splitting for statistical A/B tests

### Cost Optimization
- **Standard environment** for cost efficiency (scales to zero)
- **Automatic scaling**: Set appropriate min/max instances
- **Static files**: Serve from App Engine, not instances
- **Caching**: Use Cloud CDN or [[gcp/memorystore|Memorystore]]
- **Right-size instances**: Balance cost vs performance
- **Traffic splitting**: Test with minimal traffic first

### Performance Optimization
#### Standard Environment
- **Warmup requests**: Pre-initialize instances
- **Min idle instances**: Reduce cold start impact (costs more)
- **Pending latency**: Time before spinning new instance
- **Static content**: CDN for global distribution

#### Flexible Environment
- **Readiness checks**: Ensure instances ready before traffic
- **Liveness checks**: Restart unhealthy instances
- **CPU/memory**: Allocate based on profiling

### Database Integration
- **[[gcp/cloud-sql|Cloud SQL]]**: Relational database
  - Standard: Use Cloud SQL Proxy
  - Flexible: Direct [[gcp/vpc|VPC]] connection
- **[[gcp/firestore|Firestore]]**: NoSQL, native integration
- **Datastore**: Legacy NoSQL (Firestore-compatible)
- **[[gcp/bigtable|Bigtable]]**: Wide-column NoSQL
- **[[gcp/cloud-storage|Cloud Storage]]**: Object storage

### Security Best Practices
- **App Engine Firewall**: Restrict source IPs
- **Identity-Aware Proxy**: User authentication and authorization
- **[[gcp/iam|Service account]]**: Minimal permissions
- **Secrets**: [[gcp/secret-manager|Secret Manager]], not environment vars
- **HTTPS only**: Enforce secure connections
- **Security scanning**: Web Security Scanner

### Monitoring & Observability
- [[gcp/cloud-monitoring|Cloud Monitoring]]: Requests, latency, errors
- [[gcp/cloud-logging|Cloud Logging]]: Application and request logs
- [[gcp/cloud-trace|Cloud Trace]]: Distributed tracing
- [[gcp/cloud-profiler|Cloud Profiler]]: CPU and memory profiling
- [[gcp/error-reporting|Error Reporting]]: Error aggregation
- Cloud Debugger: Live debugging (Standard only)

### Migration Strategies
#### From Elastic Beanstalk to App Engine
- Similar PaaS model
- app.yaml vs .ebextensions
- Traffic splitting similar
- Blue/green deployment support

#### From App Engine to Cloud Run
- More control, containerized
- Similar auto-scaling
- Better for modern architectures

#### From App Engine to GKE
- When outgrew App Engine constraints
- Need complex orchestration
- Multi-cloud requirements

### Limitations to Consider
- **Regional only**: Single region deployment
- **Vendor lock-in**: App Engine-specific APIs
- **Standard sandbox**: Runtime restrictions
- **Cold starts**: Standard environment
- **Always-on cost**: Flexible environment (min 1 instance)

### Advanced Features
#### Dispatch Rules
```yaml
# dispatch.yaml
dispatch:
- url: "*/api/*"
  service: api
- url: "*/admin/*"
  service: admin
- url: "*/*"
  service: default
```

#### VPC Connector (Flexible)
- Connect to [[gcp/vpc|VPC]] resources
- Private IP communication
- Access [[compute-engine|Compute Engine]], [[gcp/cloud-sql|Cloud SQL]] via private IP

#### Environment Variables & Secrets
```yaml
# app.yaml
env_variables:
  DB_HOST: "10.0.0.5"

# Use Secret Manager
beta_settings:
  cloud_sql_instances: PROJECT:REGION:INSTANCE
```

### Well-Architected Considerations
- **Operational Excellence**: Fully managed, automatic updates, traffic splitting
- **Reliability**: Multi-zone deployment, health checks, automatic instance replacement
- **Security**: [[gcp/iam|IAM]], App Engine firewall, IAP, HTTPS, [[gcp/secret-manager|secrets management]]
- **Performance**: Auto-scaling, caching, CDN integration, warmup requests
- **Cost**: Scale to zero (Standard), sustained use discounts, static file serving
- **Sustainability**: Efficient resource usage, scale to zero when idle

### App Engine vs Modern Alternatives
**Consider App Engine when:**
- Familiar with PaaS model
- Quick deployment without Docker knowledge
- Need built-in traffic splitting
- Multi-service architecture

**Consider [[cloud-run|Cloud Run]] when:**
- Containerized apps
- More control over environment
- Modern CI/CD workflows
- Lower cost for variable traffic

**Consider [[gke|GKE]] when:**
- Complex orchestration
- Stateful applications
- Multi-cloud portability
- Advanced networking requirements
