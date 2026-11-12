---
title: migration-framework
category: GCP
description: 'GCP note: Migration-framework.'
tags:
- gcp
- management
---


# migration-framework

`gcp` `management`

## Cloud Migration Framework
**Google's 4-Phase Methodology** for migrating to Google Cloud
**Critical for PCA exam** - case studies heavily feature migration scenarios

### Overview
Google Cloud migration follows **4 sequential phases**:
1. **Assess** - Inventory and prioritize workloads
2. **Plan** - Design foundation and environment
3. **Deploy** - Migrate workloads
4. **Optimize** - Improve and modernize

---

## Phase 1: Assess Workloads

### Objectives
- Take complete inventory of applications
- Calculate Total Cost of Ownership (TCO)
- Prioritize workloads for migration
- Identify dependencies
- Run proof-of-concept migrations

### Key Activities

#### 1. Application Discovery
- **Catalog all applications**:
  - Application name, owner, dependencies
  - Infrastructure (servers, storage, network)
  - Databases and data stores
  - Integration points
- **Tools**:
  - [[compute-engine|Migrate for Compute Engine]] discovery
  - Third-party tools (CloudPhysics, RiverMeadow)
  - Manual inventory for small environments

#### 2. TCO Analysis
**Components to calculate:**
- **On-Premises Costs**:
  - Hardware (servers, storage, network)
  - Licensing (OS, database, application)
  - Data center (power, cooling, space)
  - Personnel (admin, maintenance)
  - Network bandwidth
- **GCP Costs**:
  - [[compute-engine|Compute Engine]] / [[gke|GKE]] / [[cloud-run|Cloud Run]]
  - Storage ([[persistent-disk|Persistent Disk]], [[cloud-storage|Cloud Storage]])
  - Network egress
  - Licensing (BYOL vs Google-provided)
  - Support plans

**Pricing Calculator**: Use [[cloud-scheduler|GCP Pricing Calculator]]

#### 3. Workload Prioritization

**Prioritization Framework:**

| Factor | Questions | Impact |
|--------|-----------|--------|
| **Business Value** | Revenue impact? Strategic importance? | High priority = high value |
| **Team Readiness** | Team skills? Innovation appetite? | Start with ready teams |
| **Dependencies** | Tightly coupled? External dependencies? | ==Fewer dependencies = easier== |
| **Refactoring Effort** | Lift-and-shift vs rewrite? | Lower effort = faster wins |
| **Licensing** | BYOL possible? License restrictions? | Can affect cost/feasibility |
| **Compliance** | Regulatory requirements? Data residency? | May dictate timing/approach |
| **Availability/Reliability** | Current SLA? Downtime tolerance? | High SLA = more careful planning |

**Migration Complexity Matrix:**
```text
Low Complexity → High Complexity
- Stateless apps → Stateful apps
- Few dependencies → Many dependencies
- Standard stack → Custom/legacy stack
- BYOL → License restrictions
- Flexible SLA → Strict SLA
```

**Recommendation**: Start with **low complexity, high value** workloads for quick wins

#### 4. Proof of Concept (PoC)
- Migrate 1-2 non-critical applications
- Test migration process
- Validate performance
- Identify gaps in planning
- Build team confidence

---

## Phase 2: Plan Foundation

### Objectives
- Design landing zone (target environment)
- Configure identity and access management
- Plan network architecture
- Establish connectivity to on-premises
- Set up security and compliance guardrails
- Form migration team

### Key Activities

#### 1. Resource Organization
**Design hierarchy:**
```text
Organization (root)
└── Folders (by department, environment, or team)
    ├── Shared Services Folder
    │   ├── Networking Project (VPCs, VPNs)
    │   ├── Security Project (monitoring, logging)
    │   └── Identity Project (IAM, groups)
    └── Department/Team Folders
        ├── Production Project
        ├── Staging Project
        └── Development Project
```

**Best Practice**: **One project per application per environment**
- Example: `ecommerce-prod`, `ecommerce-staging`, `ecommerce-dev`

#### 2. Identity & Access Management
- **Cloud Identity**: Set up organization-wide identity
  - Sync with on-prem Active Directory
  - Or use Google Workspace
- **IAM Strategy**:
  - [[iam|IAM]] best practices
  - Use groups, not individual users
  - Principle of least privilege
  - Separation of duties
- **Service Accounts**: Plan for application identities

#### 3. Network Architecture
**Design VPC topology:**
- **Shared VPC** (recommended for enterprises):
  - Host project owns VPC
  - Service projects use VPC subnets
  - Centralized network management
- **VPC Peering**: For cross-project connectivity
- **Subnets**: Plan IP ranges (avoid overlap with on-prem)
- **Firewall Rules**: Default deny, explicit allows

**Hybrid Connectivity:**

| Option | Bandwidth | Encryption | Best for |
|---|---|---|---|
| [[cloud-vpn|Cloud VPN]] (HA VPN for 99.99% SLA) | 1.5-3 Gbps per tunnel | Encrypted | Low-moderate bandwidth, encrypted requirement |
| [[cloud-interconnect|Cloud Interconnect]] (Dedicated) | 10-100 Gbps | - | High bandwidth, low latency, predictable performance |
| [[cloud-interconnect|Cloud Interconnect]] (Partner) | 50 Mbps - 10 Gbps | - | High bandwidth, low latency, predictable performance |

**Decision Matrix:**

| Bandwidth Need | Encryption Required | Recommendation |
|----------------|---------------------|----------------|
| < 3 Gbps | Yes | **HA VPN** |
| > 3 Gbps | Yes | Dedicated Interconnect + VPN |
| > 3 Gbps | No | **Dedicated Interconnect** |
| 50 Mbps - 10 Gbps | Either | **Partner Interconnect** |

#### 4. Security & Compliance
- **Logging & Monitoring**:
  - Enable all [[cloud-logging|audit logs]]
  - Set up [[cloud-monitoring|Cloud Monitoring]] alerts
  - Export logs to [[cloud-storage|Cloud Storage]] for compliance
- **Encryption**:
  - [[cloud-kms|Cloud KMS]] for encryption keys
  - CMEK for compliance requirements
- **Security Controls**:
  - [[vpc-service-controls|VPC Service Controls]] perimeter
  - Organization policies (constraints)
  - [[security-command-center|Security Command Center]] for threat detection

#### 5. Migration Team
**Roles needed:**

| Role | Responsibility |
|---|---|
| Migration Lead | Overall coordination |
| Network Architect | VPC, connectivity design |
| Security Specialist | IAM, compliance |
| Application Owners | Subject matter experts |
| Cloud Engineers | Hands-on migration work |
| Project Manager | Timeline, dependencies |

---

## Phase 3: Deploy Workloads

### Objectives
- Migrate data
- Deploy applications
- Validate functionality
- Cut over to production

### Migration Strategies

#### 1. Lift and Shift (Rehost)
**Approach**: Move as-is to GCP
- Minimal changes
- Fastest migration
- Use [[compute-engine|Migrate for Compute Engine]]

**Best for:**
- Quick migration needed
- Limited resources for refactoring
- Complex legacy applications

**Process:**
1. Create machine image of source VM
2. Import to Compute Engine
3. Test functionality
4. Switch traffic

#### 2. Improve and Move (Replatform)
**Approach**: Minor optimization during migration
- Move to managed services where possible
- Example: Database → [[cloud-sql|Cloud SQL]]

**Best for:**
- Want some cloud benefits
- Minimal code changes acceptable
- Reduce operational overhead

**Process:**
1. Identify opportunities for managed services
2. Migrate data to managed service
3. Update application connection strings
4. Test and validate

#### 3. Rip and Replace (Refactor)
**Approach**: Redesign for cloud-native
- Containers ([[gke|GKE]], [[cloud-run|Cloud Run]])
- Serverless ([[cloud-functions|Cloud Functions]])
- Fully managed services

**Best for:**
- Maximum cloud benefits desired
- Application needs modernization anyway
- Team has cloud-native skills

**Process:**
1. Redesign architecture
2. Containerize or rewrite
3. Deploy to GKE/Cloud Run
4. Migrate data
5. Gradual traffic cutover

### Data Migration

| Size | Tool | Notes |
|---|---|---|
| < 1 TB | **gsutil** | Command-line upload to [[cloud-storage|Cloud Storage]] |
| < 1 TB | **Console upload** | For very small files |
| < 1 TB | **Storage Transfer Service** | Online transfer from other clouds |
| 1-20 TB | **Storage Transfer Service** | Online from AWS S3, Azure Blob, HTTP/HTTPS. Scheduled recurring transfers. Bandwidth throttling |
| > 20 TB | **Transfer Appliance** | Physical device shipped to you. Load data locally (fast). Ship back to Google. Google uploads to Cloud Storage. Offline transfer (no bandwidth cost) |

#### Database Migration
- **[[cloud-sql|Database Migration Service]]**:
  - Migrate to Cloud SQL
  - Minimal downtime
  - Continuous replication until cutover
  - Supports MySQL, PostgreSQL

**Process:**
1. Set up replication from source to Cloud SQL
2. Validate data consistency
3. Switch application to Cloud SQL (brief downtime)
4. Decommission source database

### Deployment Automation

**Configuration Management:**
- Ansible, Chef, Puppet
- Ensure consistent configuration

**CI/CD Pipelines:**
- [[cloud-build|Cloud Build]] for builds
- [[artifact-registry|Artifact Registry]] for images
- Automated testing

**Infrastructure as Code:**
- **Terraform** (preferred):
  - Multi-cloud
  - Large community
  - Version control friendly
- **Cloud Deployment Manager** (GCP-native):
  - YAML/Jinja2/Python
  - Prevents configuration drift

---

## Phase 4: Optimize

### Objectives
- Improve performance
- Reduce costs
- Increase reliability
- Adopt cloud-native features

### Optimization Areas

#### 1. Logging, Monitoring, Alerting
- **Comprehensive observability**:
  - [[cloud-monitoring|Cloud Monitoring]]: Metrics, uptime checks
  - [[cloud-logging|Cloud Logging]]: Centralized logs
  - [[cloud-trace|Cloud Trace]]: Distributed tracing
  - [[cloud-profiler|Cloud Profiler]]: Performance optimization
  - [[error-reporting|Error Reporting]]: Proactive error detection
- **SLOs & Error Budgets**:
  - Define SLIs (latency, availability, error rate)
  - Set SLOs (99.9% availability)
  - Track error budget burn rate

#### 2. Managed Services
**Replace self-managed with managed:**

| Self-managed | Managed option |
|---|---|
| VMs with databases | [[cloud-sql|Cloud SQL]], [[cloud-spanner|Cloud Spanner]] |
| Self-managed Kubernetes | [[gke|GKE Autopilot]] |
| Message queues | [[pub-sub|Cloud Pub/Sub]] |
| File servers | [[filestore|Filestore]] |
| Monitoring stack | Cloud Operations Suite |

**Benefits:**
- Reduced operational overhead
- Automatic updates, backups
- Built-in HA
- Pay-per-use

#### 3. Auto-Scaling
**Scale infrastructure to application load:**
- **Compute Engine**: [[compute-engine|Managed Instance Groups]] with autoscaling
- **GKE**: Cluster Autoscaler + Horizontal Pod Autoscaler
- **Cloud Run**: Automatic (scale to zero)
- **App Engine**: Automatic

**Scaling policies:**
- CPU utilization
- Request rate
- Custom metrics (queue depth, etc.)

**Benefits:**
- Cost savings (scale down when idle)
- Performance (scale up for traffic spikes)
- Reliability (handle unexpected load)

#### 4. Cost Optimization

| Option | Saving | Notes |
|---|---|---|
| **Right-sizing** | - | Use [[cloud-monitoring|Monitoring]] recommendations. Downsize over-provisioned VMs. Delete unused resources |
| **Committed Use Discounts** | Up to 57% | 1-year or 3-year commitment. For predictable workloads |
| **Preemptible/Spot VMs** | Up to 91% | For fault-tolerant batch workloads |
| **Storage class optimization** | - | Nearline (< 30 days access), Coldline (< 90 days), Archive (< 365 days), lifecycle policies |
| **Sustained Use Discounts** | Up to 30% for running > 25% of month | Automatic |

#### 5. Adopt Cloud-Native Features
- **Serverless**:
  - [[cloud-run|Cloud Run]] for containers
  - [[cloud-functions|Cloud Functions]] for event-driven
- **Containers**:
  - [[gke|GKE]] for orchestration
  - [[cloud-run|Cloud Run]] for simplicity
- **Data Analytics**:
  - [[bigquery|BigQuery]] for analytics
  - [[dataflow|Cloud Dataflow]] for ETL
  - [[pub-sub|Pub/Sub]] for event streaming
- **AI/ML**:
  - [[vertex-ai|Vertex AI]] for ML workloads
  - [[gemini|Gemini]] for generative AI

---

## Migration Patterns by Workload Type

### Web Applications
1. **Assess**: Identify web servers, app servers, databases, dependencies
2. **Plan**: VPC, Load Balancer, Cloud CDN
3. **Deploy**:
   - Lift-and-shift VMs → Compute Engine
   - Or containerize → GKE/Cloud Run
   - Database → Cloud SQL
4. **Optimize**: Auto-scaling, CDN, managed services

### Databases
1. **Assess**: Database type, size, IOPS, replication
2. **Plan**: Choose managed service (Cloud SQL, Spanner, etc.)
3. **Deploy**: [[cloud-sql|Database Migration Service]] for minimal downtime
4. **Optimize**: Read replicas, automatic backups, point-in-time recovery

### Batch Processing
1. **Assess**: Spark/Hadoop workloads, data volume, schedule
2. **Plan**: [[dataproc|Cloud Dataproc]] or [[dataflow|Cloud Dataflow]]
3. **Deploy**: Migrate jobs to Dataproc, data to Cloud Storage
4. **Optimize**: Preemptible VMs, autoscaling, lifecycle policies

### File Servers
1. **Assess**: File size, access patterns, performance requirements
2. **Plan**: [[filestore|Filestore]] or [[cloud-storage|Cloud Storage]]
3. **Deploy**: [[migration-framework|Storage Transfer Service]] or Transfer Appliance
4. **Optimize**: Lifecycle policies, nearline/coldline storage

---

## Migration Timeline Example

**Typical enterprise migration:**

| Phase | Duration |
|---|---|
| Phase 1 (Assess) | 1-2 months |
| Phase 2 (Plan) | 1-2 months |
| Phase 3 (Deploy) | 3-12 months (depends on # of workloads) |
| Phase 4 (Optimize) | Ongoing |

- **Pilot project**: 1-2 months
- **Wave migration**: Migrate workloads in batches (10-20 apps per wave)

---

## Risk Mitigation

### Testing Strategy
- **Functionality testing**: All features work
- **Performance testing**: Meet SLAs
- **Failover testing**: DR procedures work
- **Security testing**: No vulnerabilities introduced

### Rollback Plan
- Keep source environment running during stabilization (1-4 weeks)
- Document rollback procedure
- Test rollback in non-prod first
- Have clear rollback decision criteria

### Communication Plan
- Stakeholder updates (weekly)
- User notifications (pre-migration, post-migration)
- Support team training
- Runbooks for common issues

---

## Well-Architected Alignment

- **Operational Excellence**: Automation (IaC, CI/CD), monitoring, logging
- **Reliability**: HA design, DR planning, testing, gradual rollouts
- **Security**: IAM, encryption, VPC SC, compliance validation
- **Performance**: Right-sizing, auto-scaling, managed services, CDN
- **Cost**: TCO analysis, CUD, preemptible VMs, lifecycle policies
- **Sustainability**: Rightsizing reduces carbon footprint, managed services efficient

---

## PCA Exam Tips

**Case studies will test:**
1. **Prioritization**: Which workloads to migrate first and why
2. **Strategy selection**: Lift-and-shift vs refactor
3. **Data migration**: Transfer Appliance vs Storage Transfer Service
4. **Connectivity**: VPN vs Interconnect
5. **Phased approach**: Don't migrate everything at once
6. **Risk mitigation**: Testing, rollback plans
7. **Cost optimization**: Identify opportunities during migration

**Common scenarios:**

| Scenario | Recommendation |
|---|---|
| Large on-prem data center (100+ applications) | **Phased migration, start with low complexity** |
| 20 TB database, minimal downtime | **Database Migration Service with replication** |
| 100 TB data, slow internet | **Transfer Appliance** |
| Need hybrid for 6 months during migration | **VPN or Interconnect** |
| Legacy app, hard to modify | **Lift-and-shift to Compute Engine** |
| Modern app, containerized | **Refactor to GKE or Cloud Run** |
