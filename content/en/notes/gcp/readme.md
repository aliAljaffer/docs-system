---
title: Readme
category: GCP
description: Study notes for Google Cloud Associate Cloud Engineer (ACE) and Professional
  Cloud Architect (PCA) exams
tags:
- gcp
---


# Readme

`gcp`

## GCP Certification Study Notes

Study notes for **Google Cloud Associate Cloud Engineer (ACE)** and **Professional Cloud Architect (PCA)** exams

### Directory Structure

```
gcp/
├── compute/         # Compute services
├── storage/         # Storage services
├── databases/       # Database services
├── networking/      # Networking services
├── security/        # Security & IAM services
├── operations/      # Monitoring, Logging, Trace
├── data-analytics/  # Pub/Sub, Dataflow, Dataproc
├── ai-ml/           # Vertex AI, Gemini, ML services
├── devops/          # Cloud Build, Artifact Registry
└── management/      # Scheduler, Workflows
```

---

## Service Notes Format

Each service note contains:

- **AWS Equivalent**: Maps to your AWS knowledge
- ****Highlights****: Key exam points
- **## ACE Level**: Essential commands & concepts for Associate exam
- **## PCA Level**: Architectural patterns & Well-Architected for Professional exam

---

## ACE Exam Coverage

### Section 1: Setting up a cloud solution environment (~20%)

**Security & IAM:**

- [[iam|IAM]] - Roles, policies, service accounts, conditions
- [[gcp/cloud-kms|Cloud KMS]] - Key management

**Management:**

- Resource hierarchy (Organizations, Folders, Projects)
- Billing configuration
- [[gcp/cloud-monitoring|Cloud Monitoring]] - Ops Agent

### Section 2: Planning and configuring a cloud solution (~17.5%)

**Compute:**

- [[gcp/compute-engine|Compute Engine]] - Machine types, preemptible VMs
- [[gcp/gke|GKE]] - Autopilot vs Standard, node pools
- [[gcp/cloud-run|Cloud Run]] - Services vs Jobs
- [[gcp/cloud-functions|Cloud Functions]] - Event-driven functions
- [[gcp/app-engine|App Engine]] - Standard vs Flexible

**Storage:**

- [[gcp/cloud-storage|Cloud Storage]] - Storage classes
- [[gcp/persistent-disk|Persistent Disk]] - Zonal vs Regional
- [[gcp/filestore|Filestore]] - NFS file system

**Databases:**

- [[gcp/cloud-sql|Cloud SQL]] - MySQL, PostgreSQL, SQL Server
- [[gcp/bigquery|BigQuery]] - Data warehouse
- [[gcp/firestore|Firestore]] - NoSQL document database
- [[gcp/cloud-spanner|Cloud Spanner]] - Globally distributed SQL
- [[gcp/bigtable|Cloud Bigtable]] - NoSQL wide-column

**Networking:**

- [[vpc|VPC]] - Subnets, firewall rules, Private Google Access
- [[gcp/cloud-load-balancing|Cloud Load Balancing]] - HTTP(S), Network, Internal

**AI/ML:**

- [[gcp/vertex-ai|Vertex AI]] - Unified ML platform, AutoML
- [[gcp/gemini|Gemini]] - Foundation models (basic usage)

### Section 3: Deploying and implementing a cloud solution (~25%)

**Compute:**

- Compute Engine - Launching instances, autoscaling, instance groups
- GKE - Deploying clusters and workloads
- Cloud Run - Deploying containerized apps
- Cloud Functions - Deploying functions

**Databases:**

- Deploying Cloud SQL, Firestore, BigQuery, Spanner
- Loading data via Cloud Storage, [[gcp/cloud-build|Cloud Build]]

**Networking:**

- Creating VPCs, subnets, firewall rules
- VPC Peering, Shared VPC
- [[gcp/cloud-vpn|Cloud VPN]], [[gcp/cloud-interconnect|Cloud Interconnect]]

**DevOps:**

- [[gcp/cloud-build|Cloud Build]] - CI/CD
- [[gcp/artifact-registry|Artifact Registry]] - Container images

### Section 4: Ensuring successful operation (~20%)

**Compute Management:**

- Managing Compute Engine (snapshots, images, SSH)
- Managing GKE (viewing inventory, autoscaling)
- Managing Cloud Run (versions, traffic splitting)

**Storage & Database:**

- [[gcp/cloud-storage|Cloud Storage]] - Lifecycle policies, versioning
- Database management (backups, queries)

**Networking:**

- [[gcp/cloud-dns|Cloud DNS]]
- [[gcp/cloud-nat|Cloud NAT]]

**Operations:**

- [[gcp/cloud-monitoring|Cloud Monitoring]] - Alerts, uptime checks, dashboards
- [[gcp/cloud-logging|Cloud Logging]] - Log buckets, sinks, filters

### Section 5: Configuring access and security (~17.5%)

**Security:**

- [[iam|IAM]] - Roles (basic, predefined, custom), service accounts
- [[gcp/cloud-kms|Cloud KMS]] - Encryption keys
- [[gcp/secret-manager|Secret Manager]] - Secrets management

---

## PCA Exam Coverage

### Section 1: Designing and planning a cloud solution architecture (~24%)

**All services - Architectural considerations:**

- Business requirements mapping
- [[cost-optimization-pillar|Cost optimization]] strategies
- Performance requirements
- Compliance and data residency
- Migration planning
- **[[generative-ai|Generative AI]] integration** (NEW in 2026)

**Key Services:**

- All Compute options: [[gcp/compute-engine|Compute Engine]], [[gcp/gke|GKE]], [[gcp/cloud-run|Cloud Run]], [[gcp/app-engine|App Engine]]
- Storage architecture: [[gcp/cloud-storage|Cloud Storage]], [[gcp/persistent-disk|Persistent Disk]], [[gcp/filestore|Filestore]]
- Database selection: [[gcp/cloud-sql|Cloud SQL]], [[gcp/cloud-spanner|Spanner]], [[gcp/bigtable|Bigtable]], [[gcp/firestore|Firestore]], [[gcp/bigquery|BigQuery]], [[gcp/alloydb|AlloyDB]]
- Network topology: [[vpc|VPC]], [[gcp/cloud-load-balancing|Load Balancing]], hybrid connectivity
- **AI/ML architecture**: [[gcp/vertex-ai|Vertex AI]], [[gcp/gemini|Gemini]], RAG patterns, MLOps

### Section 2: Managing and provisioning solution infrastructure (~15%)

**Networking:**

- VPC design, Shared VPC, VPC Peering
- Hybrid connectivity ([[gcp/cloud-vpn|VPN]], [[gcp/cloud-interconnect|Interconnect]])
- [[gcp/cloud-load-balancing|Load Balancing]] architecture

**Compute:**

- Instance groups, autoscaling
- GKE cluster design (Autopilot vs Standard, multi-zone, regional)
- [[serverless|Serverless]] patterns (Cloud Run, Cloud Functions)

**Storage:**

- Storage classes and lifecycle
- Persistent Disk (Regional HA)
- Database replication and HA

### Section 3: Designing for security and compliance (~18%)

**Security:**

- [[iam|IAM]] - Resource hierarchy, conditions, [[principle-of-least-privilege|least privilege]]
- [[gcp/cloud-kms|Cloud KMS]] - CMEK, encryption strategies
- [[gcp/secret-manager|Secret Manager]] - Secret rotation
- [[gcp/vpc-service-controls|VPC Service Controls]] - Perimeter security
- [[gcp/security-command-center|Security Command Center]] - Threat detection
- [[gcp/binary-authorization|Binary Authorization]] - Image verification
- [[gcp/identity-aware-proxy|Identity-Aware Proxy]] - Zero-trust access

**Networking:**

- [[gcp/cloud-armor|Cloud Armor]] - DDoS protection, WAF
- Private Google Access, Private Service Connect

### Section 4: Analyzing and optimizing technical and business processes (~18%)

**Operations:**

- [[gcp/cloud-monitoring|Cloud Monitoring]] - SLO/SLI, error budgets
- [[gcp/cloud-logging|Cloud Logging]] - Log analytics, centralized logging
- [[gcp/cloud-trace|Cloud Trace]] - Distributed tracing, bottleneck analysis
- [[gcp/cloud-profiler|Cloud Profiler]] - CPU/memory optimization
- [[gcp/error-reporting|Error Reporting]] - Proactive error detection

**Data Analytics:**

- [[gcp/pub-sub|Cloud Pub/Sub]] - Event-driven architecture
- [[gcp/dataflow|Cloud Dataflow]] - Stream/batch processing
- [[gcp/dataproc|Cloud Dataproc]] - Spark/Hadoop workloads
- [[gcp/cloud-composer|Cloud Composer]] - Apache Airflow orchestration

**Caching:**

- [[gcp/memorystore|Memorystore]] - Redis vs Memcached selection, caching patterns

**AI/ML & Generative AI:** **NEW FOCUS AREA in 2026**

- [[gcp/vertex-ai|Vertex AI]] - ML platform architecture
- [[gcp/gemini|Gemini]] - Foundation model selection (Pro vs Flash)
- RAG (Retrieval-Augmented Generation) patterns
- Context caching for cost optimization
- Model deployment and monitoring
- Responsible AI practices

**Cost Optimization:**

- Committed Use Discounts, Sustained Use Discounts
- Preemptible/Spot instances
- Right-sizing with Cloud Monitoring
- Storage class optimization

### Section 5: Managing implementation (~11%)

**DevOps:**

- [[gcp/cloud-build|Cloud Build]] - CI/CD pipelines
- [[gcp/artifact-registry|Artifact Registry]] - Image management
- [[gcp/deployment-strategies|Deployment Strategies]] - **6 strategies (Recreate, Rolling, Canary, Blue/Green, Shadow, A/B)**
- [[infrastructure-as-code|Infrastructure as Code]] (Deployment Manager, Terraform)

**Management:**

- [[gcp/cloud-scheduler|Cloud Scheduler]] - Scheduled tasks
- [[gcp/workflows|Workflows]] - Service orchestration
- [[gcp/cloud-composer|Cloud Composer]] - Apache Airflow for complex data pipelines
- [[gcp/migration-framework|Migration Framework]] - **4-phase methodology (Assess, Plan, Deploy, Optimize)**

### Section 6: Ensuring solution and operations reliability (~14%)

**Reliability Patterns:**

- Multi-zone, multi-region deployment
- Health checks, autoscaling, auto-healing
- Disaster recovery strategies
- Chaos engineering principles

**Monitoring:**

- Comprehensive observability (metrics, logs, traces)
- SLO-based alerting
- Incident management integration

---

---

## 🎯 Critical PCA Topics (Heavily Emphasized in Videos)

### 1. Deployment Strategies (MUST KNOW)

**[[gcp/deployment-strategies|Full Guide]]**

Exam tests you on **selecting the right strategy** for scenarios:

- **Recreate**: Downtime acceptable, dev/test only
- **Rolling**: Zero downtime, cost-effective, slower rollout
- **Canary**: **10-20% traffic test, minimal risk, best for critical apps**
- **Blue/Green**: **Instant rollback, double infrastructure, mission-critical**
- **Shadow**: Testing only, zero user impact, high complexity
- **A/B Testing**: Feature testing vs canary (stability testing)

**Exam tip**: "Minimize user impact" = **Canary**, "Instant rollback" = **Blue/Green**

### 2. Migration Framework (CASE STUDY CRITICAL)

**[[gcp/migration-framework|Full Guide]]**

**4 Phases** (know them cold):

1. **Assess**: TCO calculation, workload prioritization (low complexity + high value first)
2. **Plan**: Landing zone, Shared VPC, VPN vs Interconnect, IAM setup
3. **Deploy**: Lift-and-shift vs replatform vs refactor, data migration methods
4. **Optimize**: Managed services, auto-scaling, cost optimization

**Data migration selection**:

- < 1 TB → **gsutil or Storage Transfer Service**
- 1-20 TB → **Storage Transfer Service**
- \> 20 TB → **Transfer Appliance** (offline)
- Databases → **Database Migration Service**

**Connectivity**: < 3 Gbps = **VPN**, > 3 Gbps = **Interconnect**

### 3. IAM Best Practices (HEAVILY TESTED)

- **Principle of Least Privilege**: Minimum access needed
- **Separation of Duties**: 2+ people for sensitive operations
- **Use Groups**: Never bind roles to individual users
- **Service Accounts**: Different account per app/purpose
- **Cloud Audit Logs**: Always enabled, export to Cloud Storage
- **ACL vs IAM vs Signed URLs**:
  - ACL = permanent access to subset of bucket objects
  - IAM = permanent access to entire bucket
  - Signed URL = time-limited access to specific object

### 4. Data Lifecycle & Architectures

**4-Stage Model**:

1. **Ingest**: Pub/Sub (stream), Transfer services (batch), Database Migration Service
2. **Store**: Cloud Storage, BigQuery, Bigtable, Cloud SQL, Spanner
3. **Process/Analyze**: Dataflow, Dataproc, BigQuery
4. **Visualize**: Looker, Data Studio

**IoT Pattern** (common case study):

```
IoT Core → Pub/Sub → Dataflow → BigQuery (ad-hoc)
                              → Bigtable (time-series)
                              → Datastore (web/mobile)
                              → Cloud Functions (alerts)
```

### 5. Caching Architecture

**[[gcp/memorystore|Memorystore]]**: Redis vs Memcached

- **Memcached**: Pure cache, no persistence, session store, reference data
- **Redis Standard**: Persistence + HA + failover, gaming leaderboards, critical sessions
- **Cloud CDN**: External HTTPS Load Balancer + backends (GCS, GCE, Cloud Run)

### 6. Architecture Framework (5 Pillars)

1. **Operational Excellence**: 4 golden signals (latency, traffic, errors, saturation), SLI/SLO/error budgets
2. **Security**: Covered extensively
3. **Reliability**: **Most important** - Multi-region, graceful degradation, rollback capability, blameless postmortems
4. **Performance**: Right-sizing, auto-scaling
5. **Cost Optimization**: CUD, sustained use, preemptible VMs

**Incident metrics**: MTTD, MTTM, MTTR, MTBF

### 7. HIPAA Compliance (Common Case Study)

- **BAA** (Business Associate Agreement) from Google
- Enable **object versioning** on buckets
- Export audit logs to Cloud Storage AND BigQuery
- **Disable request caching for PHI**
- All IAM best practices apply

---

## 📚 Study Order Guide

### Recommended Section Order

Study sections in this order based on service dependencies and complexity:

1. ✅ **Compute** (foundation)
2. **Networking** (builds on compute, foundational for everything)
3. **Storage** (needed for databases)
4. **Security** (applies to all services - IAM is critical)
5. **Databases** (builds on storage + networking)
6. **Operations** (monitoring/logging for production patterns)
7. **Data Analytics** (builds on storage, databases, messaging)
8. **AI/ML** (leverages data analytics and storage)
9. **DevOps** (deployment patterns synthesize compute + networking)
10. **Management** (migration framework ties everything together)

### Within Each Section: Reading Order

#### Networking (Current Focus)

1. `vpc.md` - Foundation, start here
2. `cloud-load-balancing.md` - Core primitive
3. `cloud-dns.md` - Simple, foundational
4. `cloud-nat.md` - Builds on VPC
5. `cloud-vpn.md` - Hybrid connectivity basics
6. `cloud-interconnect.md` - Advanced hybrid
7. `private-google-access-vs-psc.md` - Critical PCA topic
8. `cloud-armor.md` - Layer 7 security
9. `cloud-ngfw.md` - Advanced (builds on firewall concepts)

#### Storage

1. `cloud-storage.md` - Most fundamental
2. `persistent-disk.md` - VM storage
3. `filestore.md` - NFS (more specialized)

#### Security

1. `iam.md` - **START HERE** - absolutely foundational
2. `cloud-kms.md` - Encryption keys
3. `secret-manager.md` - Builds on KMS
4. `vpc-service-controls.md` - Requires VPC + IAM knowledge
5. `security-command-center.md` - Aggregates security findings
6. `binary-authorization.md` - Container security
7. `identity-aware-proxy.md` - Application access control

#### Databases

1. `cloud-sql.md` - Most familiar (like RDS)
2. `cloud-spanner.md` - Global SQL
3. `alloydb.md` - PostgreSQL-compatible
4. `firestore.md` - NoSQL document
5. `bigtable.md` - NoSQL wide-column
6. `bigquery.md` - Data warehouse
7. `memorystore.md` - Caching (read after understanding when to cache)

#### Operations

1. `cloud-monitoring.md` - Core observability - start here
2. `cloud-logging.md` - Pairs with monitoring
3. `cloud-trace.md` - Distributed tracing
4. `cloud-profiler.md` - Performance profiling
5. `error-reporting.md` - Error detection

#### Data Analytics

1. `pub-sub.md` - Foundational messaging
2. `dataflow.md` - Stream/batch processing
3. `dataproc.md` - Big data (Spark/Hadoop)
4. `cloud-composer.md` - Orchestration (most complex)

#### AI/ML

1. `gemini.md` - Foundation models (simpler)
2. `vertex-ai.md` - Full ML platform (more complex)

#### DevOps

1. `artifact-registry.md` - Simple - container/artifact storage
2. `cloud-build.md` - CI/CD pipelines
3. `deployment-strategies.md` - **CRITICAL for PCA** - read carefully

#### Management

1. `cloud-scheduler.md` - Simple cron jobs
2. `workflows.md` - Service orchestration
3. `migration-framework.md` - **Save for LAST** - synthesizes everything

### How to Read Each File (Given Your Background)

**You have AWS SA Associate + Azure + OCI + Alibaba experience:**

#### Read BOTH ACE and PCA Sections Together

1. **ACE section** (15-20 min): Learn GCP-specific syntax, gcloud commands
2. **PCA section** (30-40 min): Architectural patterns, Well-Architected considerations
3. This builds complete mental model in one sitting

#### Speed-Read vs Deep-Dive

**Speed-read (skim ACE, focus PCA on differences from AWS):**

- Cloud Storage (you know S3)
- Persistent Disk (you know EBS)
- Cloud SQL (you know RDS)
- Cloud Monitoring/Logging (you know CloudWatch)

**Deep-dive (PCA sections - architectural differences):**

- VPC (global, not regional like AWS)
- Cloud Spanner (no direct AWS equivalent)
- Cloud Load Balancing (different architecture than ELB/ALB)
- IAM (different model than AWS IAM)
- Deployment Strategies (critical for PCA case studies)
- Migration Framework (heavily tested on PCA)
- Vertex AI / Gemini (Gen AI is new PCA focus for 2026)

### Time Allocation (For PCA Prep)

**Week 1-2: Foundations**

- Compute (done ✓)
- Networking (5-6 hours)
- Storage (2 hours)
- Security (4-5 hours - IAM is critical)

**Week 3: Data Layer**

- Databases (4-5 hours)
- Operations (3-4 hours)

**Week 4: Advanced**

- Data Analytics (4-5 hours)
- AI/ML (3-4 hours - Gen AI is NEW for 2026)
- DevOps (3-4 hours - deployment strategies are **critical**)
- Management (3-4 hours - migration framework is **heavily tested**)

**Week 5: ACE Review** (if taking ACE)

- Practice exams
- gcloud command practice
- Hands-on labs

**Week 6: PCA Deep-Dive**

- Case study practice
- Architecture design patterns
- Migration scenarios
- Deployment strategies

---
### Recommended Learning Paths

#### For ACE Preparation

**Official Path**: [Cloud Engineer Learning Path](https://www.skills.google/paths/11)

- 14 activities including courses, hands-on labs, and skill badges
- Covers Essential Infrastructure, Kubernetes, Cloud Run, Logging & Monitoring
- Skill badges: Implementing Cloud Load Balancing, App Dev Environment, Network Development

#### For PCA Preparation

**Official Path**: [Cloud Architect Learning Path](https://www.skills.google/paths/12)

- Recommended: Complete 40-50 hands-on labs
- Focus on architectural design patterns and case studies
- Advanced topics: Multi-region deployments, hybrid architectures, migration strategies

### Lab Tips

1. **Start with Qwik Start labs** (Introductory, 30-40 min) to learn service basics
2. **Progress to Challenge Labs** to test knowledge without step-by-step instructions
3. **Complete Skill Badges** to demonstrate proficiency in specific skill areas
4. **Use temporary credentials** - no need for personal GCP account for most labs
5. **Take notes** - labs expire but your notes are permanent reference material

---

## Exam Comparison: ACE vs PCA

| Aspect           | ACE                       | PCA                              |
| ---------------- | ------------------------- | -------------------------------- |
| **Focus**        | Operational tasks         | Architectural design             |
| **Depth**        | Basic service usage       | Deep architectural patterns      |
| **Breadth**      | Core services             | All services + advanced features |
| **Commands**     | gcloud commands essential | Understanding, not memorizing    |
| **Case Studies** | None                      | 2 case studies (20-30% of exam)  |
| **Experience**   | 6+ months                 | 3+ years (1+ year GCP)           |
| **Difficulty**   | Associate level           | Professional level               |

---

## Study Approach (Given Your Background)

### For ACE:

1. **Skim ACE sections** for GCP-specific syntax/commands
2. **Focus on differences from AWS** (highlighted in notes)
3. **Key areas**:
   - gcloud command syntax (different from aws cli)
   - GCP networking (global VPC, regional subnets)
   - Service-specific nuances (e.g., Autopilot GKE, VPC-native clusters)
   - IAM model differences (roles vs policies)

### For PCA:

1. **Deep-dive PCA sections** - this is where architectural knowledge matters
2. **Well-Architected comparisons** - GCP vs AWS frameworks
3. ****Critical exam topics from videos**** (see section below)
4. **Key areas**:
   - Multi-region HA patterns
   - Cost optimization strategies (CUD, Spot, rightsizing)
   - Security architecture (VPC SC, IAP, Binary Authorization)
   - Observability (SLO/SLI/error budgets)
   - Data analytics architecture (Pub/Sub, Dataflow, BigQuery)

---

## Key GCP Differences from AWS

### Conceptual Differences

1. **VPC is global** (AWS VPC is regional)
2. **Subnets are regional** (AWS subnets are zonal)
3. **No NAT Gateway per AZ** (Cloud NAT is regional)
4. **Projects ≠ Accounts** (lighter weight organization)
5. **Service accounts everywhere** (IAM roles for services)
6. **Preemptible = Spot** (but different pricing model)

### Service Naming

- EC2 → Compute Engine
- ECS/Fargate → Cloud Run or GKE
- Lambda → Cloud Functions
- S3 → Cloud Storage
- EBS → Persistent Disk
- EFS → Filestore
- RDS → Cloud SQL
- Aurora → AlloyDB or Cloud Spanner
- DynamoDB → Firestore or Bigtable
- Redshift → BigQuery
- CloudWatch → Cloud Monitoring + Cloud Logging
- X-Ray → Cloud Trace
- CloudFormation → Deployment Manager (or Terraform)
- AWS WAF + Shield → Cloud Armor
- AWS Network Firewall → Cloud NGFW Enterprise

### Unique GCP Services (No AWS Equivalent)

- **Cloud Spanner**: Global strong consistency SQL
- **AlloyDB Columnar Engine**: OLTP + OLAP in one DB
- **BigQuery**: Truly serverless data warehouse
- **Firestore**: Real-time database with offline support
- **Cloud Profiler**: Free continuous profiling
- **GKE Autopilot**: Fully managed Kubernetes
- **VPC Service Controls**: Perimeter-based security
- **Gemini 2M context**: Longest context window in industry
- **Vertex AI unified platform**: One platform for all ML (AutoML, custom, gen AI)

---

## Quick Reference: Service Selection

### Compute

| Use Case                 | Service                                      |
| ------------------------ | -------------------------------------------- |
| VMs                      | [[gcp/compute-engine|Compute Engine]]   |
| Containers (managed K8s) | [[gcp/gke|GKE]]                         |
| Containers (serverless)  | [[gcp/cloud-run|Cloud Run]]             |
| Functions (event-driven) | [[gcp/cloud-functions|Cloud Functions]] |
| Full web apps (PaaS)     | [[gcp/app-engine|App Engine]]           |

### Storage

| Use Case           | Service                                      |
| ------------------ | -------------------------------------------- |
| Object storage     | [[gcp/cloud-storage|Cloud Storage]]     |
| Block storage (VM) | [[gcp/persistent-disk|Persistent Disk]] |
| File storage (NFS) | [[gcp/filestore|Filestore]]             |

### Database

| Use Case               | Service                                                     |
| ---------------------- | ----------------------------------------------------------- |
| Relational (regional)  | [[gcp/cloud-sql|Cloud SQL]]                          |
| Relational (global)    | [[gcp/cloud-spanner|Cloud Spanner]]                  |
| PostgreSQL (high perf) | [[gcp/alloydb|AlloyDB]]                              |
| NoSQL (document)       | [[gcp/firestore|Firestore]]                          |
| NoSQL (wide-column)    | [[gcp/bigtable|Cloud Bigtable]]                      |
| Data warehouse         | [[gcp/bigquery|BigQuery]]                            |
| In-memory cache        | [[gcp/memorystore|Memorystore]] (Redis or Memcached) |

### AI/ML

| Use Case                        | Service                                                     |
| ------------------------------- | ----------------------------------------------------------- |
| Generative AI (text/multimodal) | [[gcp/gemini|Gemini]] via [[gcp/vertex-ai|Vertex AI]] |
| No-code ML                      | [[gcp/vertex-ai|Vertex AI AutoML]]                       |
| Custom ML training              | [[gcp/vertex-ai|Vertex AI Custom Training]]              |
| ML pipelines (MLOps)            | [[gcp/vertex-ai|Vertex AI Pipelines]]                    |
| RAG / Vector search             | [[gcp/vertex-ai|Vertex AI Matching Engine]]              |

### Networking

| Use Case                              | Service                                                              |
| ------------------------------------- | -------------------------------------------------------------------- |
| Virtual network                       | [[vpc|VPC]]                                              |
| Load balancing                        | [[gcp/cloud-load-balancing|Cloud Load Balancing]]            |
| VPN                                   | [[gcp/cloud-vpn|Cloud VPN]]                                  |
| Dedicated connection                  | [[gcp/cloud-interconnect|Cloud Interconnect]]                |
| DNS                                   | [[gcp/cloud-dns|Cloud DNS]]                                  |
| NAT                                   | [[gcp/cloud-nat|Cloud NAT]]                                  |
| DDoS/WAF (Layer 7)                    | [[gcp/cloud-armor|Cloud Armor]]                              |
| Advanced firewall (Layer 3-7 IDS/IPS) | [[gcp/cloud-ngfw|Cloud NGFW Enterprise]]                     |
| Private API access (simple)           | Private Google Access (free)                                         |
| Private API access (advanced)         | [[gcp/private-google-access-vs-psc|Private Service Connect]] |

---

## Exam Resources

- **Official Exam Guides**: [ACE](https://cloud.google.com/learn/certification/cloud-engineer) | [PCA](https://cloud.google.com/learn/certification/cloud-architect)
- **Practice Exams**: Use official practice exams
- **Hands-on**: Free tier + Qwiklabs
- **Well-Architected Framework**: [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)

Good luck on your certifications! 🎯
