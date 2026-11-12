---
title: cloud-run
category: GCP
description: 'GCP note: Cloud-run.'
tags:
- gcp
- compute
---


# cloud-run

`gcp` `compute`

## Cloud Run
**Fully managed** serverless platform for **containerized applications**

**AWS Equivalent:** AWS Fargate + AWS App Runner (combined)

### Overview
- Deploy containers without managing infrastructure
- **Automatic scaling from 0 to N**
- **Pay only when requests are being processed**
- Built on Knative (open-source Kubernetes extension)
- Supports any language, any library, any binary

### Cloud Run Services vs Jobs
| Attribute | Services | Jobs |
|-----------|----------|------|
| Workload | **HTTP-triggered** applications | **Task-based** workloads |
| Behavior | Responds to web requests. Each instance can handle multiple concurrent requests | Run to completion then exit. Can run on schedule, manually, or via events |
| Scaling | Auto-scales based on incoming traffic | Parallel execution support |
| Use cases | APIs, web apps, webhooks | Batch processing, data transformations, scheduled tasks |

### Deployment Regions
- **Multi-region**: `us`, `europe`, `asia` (higher availability)
- **Single region**: Specific regions like `us-central1`
- **Multi-region not available for Jobs**

### Container Requirements
- Listen on `$PORT` environment variable (default 8080)
- Stateless (request-scoped only)
- **Container must start within 4 minutes** (configurable up to 60 min)
- Image in [[gcp/artifact-registry|Artifact Registry]] or Container Registry

### Scaling Configuration
- **Min instances**: Keep instances warm, **costs even at 0 requests**
- **Max instances**: Control costs and concurrency
- **Concurrency**: Requests per instance (1-1000, default 80)
  - Higher concurrency = fewer instances = lower cost
  - Lower concurrency = more instances = better isolation

### Cold Starts
- Occur when scaling from 0 or no warm instances available
- **Minimize by:**
  - Setting min instances > 0 (costs more)
  - Optimizing container startup time
  - Using startup CPU boost
- Startup CPU boost: Allocate extra CPU during startup (enabled by default)

### Request Timeout
- Default: 5 minutes
- Max: **60 minutes**
- Set based on longest expected request

### Memory & CPU Allocation
- **Memory**: 128 MiB to 32 GiB
- **CPU**: 0.08 to 8 vCPUs
- CPU allocation:
  - **During request processing only** (default): CPU throttled when no requests
  - **Always allocated**: CPU always available, **required for background tasks**

### Ingress Control
| Setting | Accepts traffic from |
|---------|----------------------|
| **All** (default) | Anywhere |
| **Internal** | Only from [[gcp/vpc|VPC]] or [[gcp/cloud-load-balancing|Cloud Load Balancing]] |
| **Internal and Cloud Load Balancing** | More restrictive internal |

### Networking
#### VPC Connector
- Connect Cloud Run to [[gcp/vpc|VPC]] resources
- Access [[gcp/cloud-sql|Cloud SQL]], [[compute-engine|Compute Engine]], etc. via private IPs
- **Serverless VPC Access** connector required
- Traffic can be:
  - **All traffic** through VPC (higher security, higher cost)
  - **Private ranges only** (default)

#### Direct VPC Egress
- **New feature, simpler than VPC Connector**
- No connector resource needed
- Provides private connectivity to [[gcp/vpc|VPC]]

### Authentication
#### Allow Unauthenticated (Public)
- Anyone can invoke the service
- No authentication required
- Use for public websites, webhooks

#### Require Authentication
- Callers must provide valid credentials
- [[gcp/iam|IAM]] role: `roles/run.invoker`
- Methods:
  - Service-to-service: [[gcp/iam#service accounts|Service account]] identity tokens
  - User: Google Sign-In or [[gcp/iam|Cloud IAM]]

### Traffic Management
- **Revisions**: Each deployment creates a new immutable revision
- **Traffic splitting**: Route % of traffic to different revisions
  - [[gcp/deployment-strategies#5. blue/green deployment|Blue/green deployments]]
  - [[gcp/deployment-strategies#4. canary deployment|Canary testing]]
  - [[gcp/deployment-strategies#2. rolling update (rolling deployment)|Gradual rollouts]]
- **Tags**: Assign names to revisions for testing
  - Each tag gets a unique URL

### Environment Variables & Secrets
- Set environment variables via console, gcloud, YAML
- Integrate with [[gcp/secret-manager|Secret Manager]]:
  - Mount secrets as environment variables
  - Mount secrets as files (volume mounts)
  - **Automatically rotated when secret updates**

### Cloud Run Execution Environments
#### First Generation
- Based on Google Cloud infrastructure
- Some limitations

#### Second Generation (Recommended)
- **Based on Cloud Run on [[gke|GKE]] infrastructure**
- Better performance, faster startup
- More features: network file systems, larger instances, background threads

### Pricing
- **Requests**: $0.40 per million
- **CPU**: Per vCPU-second while processing requests
- **Memory**: Per GiB-second while processing requests
- **Networking**: Outbound data
- **Free tier**: 2 million requests/month, 360,000 vCPU-seconds, 180,000 GiB-seconds

---

## ACE Level

### Essential gcloud Commands
```bash
# Deploy service
gcloud run deploy SERVICE_NAME \
  --image=IMAGE_URL \
  --region=REGION \
  --platform=managed \
  --allow-unauthenticated

# Deploy with environment variables
gcloud run deploy SERVICE_NAME \
  --image=IMAGE_URL \
  --set-env-vars="KEY1=VALUE1,KEY2=VALUE2"

# Deploy with secrets
gcloud run deploy SERVICE_NAME \
  --image=IMAGE_URL \
  --update-secrets=ENV_VAR_NAME=SECRET_NAME:VERSION

# List services
gcloud run services list

# Describe service
gcloud run services describe SERVICE_NAME --region=REGION

# Update traffic split
gcloud run services update-traffic SERVICE_NAME \
  --to-revisions=REVISION1=50,REVISION2=50

# Delete service
gcloud run services delete SERVICE_NAME --region=REGION

# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=SERVICE_NAME"

# Deploy job
gcloud run jobs deploy JOB_NAME \
  --image=IMAGE_URL \
  --region=REGION

# Execute job
gcloud run jobs execute JOB_NAME --region=REGION
```

### Key Concepts for ACE
- Deploying containerized applications to Cloud Run
- Understanding the difference between Services and Jobs
- Configuring scaling parameters (min/max instances, concurrency)
- Managing revisions and traffic splitting
- Setting environment variables and secrets
- Configuring authentication and access control
- Connecting to VPC resources via VPC Connector
- Viewing logs and monitoring Cloud Run services

---

## PCA Level

### Architectural Patterns
#### API Gateway Pattern
- Cloud Run for backend services
- [API Gateway](https://cloud.google.com/api-gateway) or [[gcp/cloud-load-balancing|Cloud Load Balancing]] for routing
- **Automatic scaling based on request volume**
- [[gcp/cloud-armor|Cloud Armor]] for DDoS protection

#### Event-Driven Architecture
- Trigger Cloud Run from [[gcp/pub-sub|Pub/Sub]] messages
- [[gcp/eventarc|Eventarc]] for event routing from 100+ sources
- [[gcp/cloud-storage|Cloud Storage]] events, [[gcp/cloud-scheduler|Cloud Scheduler]]
- Async processing, decoupled services

#### Microservices
- Each microservice as separate Cloud Run service
- Service-to-service authentication with [[gcp/iam#service accounts|service accounts]]
- [[gcp/cloud-trace|Cloud Trace]] for distributed tracing
- Internal ingress for inter-service communication

### High Availability Design
- **Multi-region deployment** for global availability
- [[cloud-load-balancing#Global HTTP(S) Load Balancer|Global HTTP(S) Load Balancing]] for multi-region routing
- Health checks and automatic traffic failover
- Regional redundancy

### Security Best Practices
- **Authentication**: Always enable unless truly public
- **Service Identity**: Unique [[gcp/iam#service accounts|service account]] per service
- **[[gcp/iam|IAM]]**: Principle of least privilege
- **[[gcp/vpc-service-controls|VPC Service Controls]]**: Prevent data exfiltration
- **[[gcp/binary-authorization|Binary Authorization]]**: Only deploy verified images
- **Secrets**: Use [[gcp/secret-manager|Secret Manager]], never hardcode
- **Ingress**: Restrict to internal/load balancer when possible

### Cost Optimization
- **Right-size**: Choose appropriate CPU/memory
- **Concurrency**: Increase to reduce instance count
- **Min instances**: Use sparingly, only for latency-sensitive apps
- **Request timeout**: Set as low as possible
- **CPU allocation**: "During request" for request-only processing
- **Startup CPU boost**: Enable for faster cold starts without ongoing cost

### Performance Optimization
- **Cold start reduction**:
  - Minimize container image size
  - Multi-stage Docker builds
  - Use distroless or Alpine base images
  - Min instances for critical paths
  - Startup CPU boost
- **Request latency**:
  - Increase concurrency if I/O-bound
  - Optimize app code
  - Use caching ([[gcp/memorystore|Memorystore]])
  - Connection pooling for databases

### Cloud Run vs. Other Compute Options
| Use Case | Cloud Run | [[gke|GKE]] | [[compute-engine|Compute Engine]] | [[cloud-functions|Cloud Functions]] |
|----------|-----------|-----|----------------|-----------------|
| HTTP workloads | ✓ Best | ✓ | ✓ | Limited |
| Containers | ✓ | ✓ | ✓ | No |
| Pay-per-use | ✓ | No | No | ✓ |
| Complex orchestration | No | ✓ Best | No | No |
| Stateful apps | Limited | ✓ | ✓ Best | No |
| Max request duration | 60 min | Unlimited | Unlimited | 60 min |
| Cold starts | Yes | No | No | Yes |
| Auto-scaling to 0 | ✓ | No | No | ✓ |

### Database Connections
- **Connection pooling**: Required for [[gcp/cloud-sql|Cloud SQL]]
- **Cloud SQL Proxy**: Automatic with Cloud Run
  - Add Cloud SQL connection in service config
  - No VPC Connector needed
  - Automatic [[gcp/iam|IAM]] authentication option
- **[[gcp/firestore|Firestore]]/[[gcp/bigtable|Bigtable]]**: Direct connection via APIs
- **Connection limits**: Consider serverless nature

### Observability & Monitoring
- [[gcp/cloud-monitoring|Cloud Monitoring]]: Request count, latency, instance count
- [[gcp/cloud-logging|Cloud Logging]]: Application and system logs
- [[gcp/cloud-trace|Cloud Trace]]: Request latency breakdown
- [[gcp/cloud-profiler|Cloud Profiler]]: CPU and memory profiling
- Custom metrics for business KPIs

### CI/CD Strategies
- [[gcp/cloud-build|Cloud Build]] for container builds
- [[gcp/artifact-registry|Artifact Registry]] for image storage
- [Cloud Deploy](https://cloud.google.com/deploy) for deployment pipelines
- [[gcp/deployment-strategies#4. canary deployment|Canary deployments]] with traffic splitting
- [[gcp/deployment-strategies#5. blue/green deployment|Blue/green]] with revision management
- Automated rollbacks on errors

### Migration to Cloud Run
#### From [[app-engine|App Engine]]
- Containerize the application
- Similar scaling behavior
- More control over environment

#### From [[gke|GKE]]
- Simpler operations, less control
- Suitable for stateless HTTP workloads
- Reduce operational overhead

#### From [[compute-engine|Compute Engine]]
- Containerize application
- Eliminate server management
- Auto-scaling benefits

### Well-Architected Considerations
- **Operational Excellence**: Fully managed, automated updates, simplified operations
- **Reliability**: Multi-region deployment, automatic scaling, health checks
- **Security**: IAM authentication, [[gcp/vpc-service-controls|VPC SC]], secret management, least privilege
- **Performance**: Automatic scaling, startup CPU boost, connection pooling
- **Cost**: Pay-per-request, auto-scale to zero, committed use for high-traffic
- **Sustainability**: Efficient resource utilization, scale to zero when idle
