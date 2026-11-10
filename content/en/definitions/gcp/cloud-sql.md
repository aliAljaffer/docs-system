---
title: Cloud-sql
category: GCP
description: 'GCP note: Cloud-sql.'
tags:
- gcp
- databases
---

<!-- imported from ObsidianVault/studies/cloud-architecht/gcp/databases/cloud-sql.md. Edit the source, then run sync.py. -->

# Cloud-sql

`gcp` `databases`

## Cloud SQL
**AWS Equivalent:** RDS
**Fully managed relational database** service for MySQL, PostgreSQL, and SQL Server

### Supported Database Engines
- **MySQL**: 5.6, 5.7, 8.0
- **PostgreSQL**: 9.6 through 16
- **SQL Server**: 2017, 2019, 2022 (Standard, Enterprise, Express, Web)

### Key Features
- **Automatic backups and point-in-time recovery**
- Automatic storage increase (up to configured limit)
- High availability with automatic failover
- Read replicas for read scaling
- Integrated with Cloud Monitoring and Cloud Logging
- **Serverless export to BigQuery and Cloud Storage**
- Private IP (VPC) and public IP support
- Managed security patches and updates

### Instance Types
#### Machine Types
- **Shared-core**: 1 vCPU shared, 0.614-3.75 GB RAM
  - Use cases: Development, testing, light workloads
  - **Up to 90% cheaper than dedicated**
- **Dedicated-core**: 1-96 vCPUs, up to 624 GB RAM
  - Production workloads
  - Custom machine types available

#### Storage Types
- **SSD (default)**: Low latency, high IOPS
- **HDD**: Cost-effective for large, infrequently accessed data
- **Auto-resize storage** up to configured limit
- Storage ranges: 10 GB - 64 TB (PostgreSQL/MySQL), 10 GB - 30 TB (SQL Server)

### High Availability (HA)
**AWS Equivalent:** Multi-AZ RDS
- **Primary and standby instances in different zones**
- **Synchronous replication**
- **Automatic failover in ~60 seconds**
- **99.95% SLA** for HA instances (vs 99.5% for standalone)
- Standby is not readable (unlike read replicas)
- Costs ~2x of standalone instance
- **Regional persistent disk** for storage replication

### Read Replicas
**AWS Comparison:** Similar to RDS Read Replicas
- **Asynchronous replication** from primary
- Can be in different region (cross-region replica)
- Up to 10 read replicas per instance
- Eventually consistent
- Can promote to standalone instance
- Use cases: Read scaling, analytics, disaster recovery
- Billed separately from primary

**Cascade Replicas:**
- Read replica of a read replica
- Reduces replication load on primary
- Max 3 levels deep

### Connection Methods
#### Public IP
- Internet-accessible with SSL/TLS
- Requires authorized networks (IP allowlist)
- SSL certificates for encrypted connections
- **Not recommended for production**

#### Private IP (VPC)
- **Recommended for production**
- Instance gets private IP from VPC
- No internet exposure
- Requires [[networking-vpc|VPC peering]] setup
- Better security and performance
- Lower latency from Compute Engine and GKE

#### Cloud SQL Proxy
**AWS Equivalent:** IAM Database Authentication (similar concept)
- **Recommended connection method**
- Automatic SSL/TLS encryption
- IAM-based authentication
- No need to manage IP allowlists
- Works with public or private IP
- Client-side proxy that forwards connections

```bash
# Start Cloud SQL Proxy
./cloud-sql-proxy PROJECT:REGION:INSTANCE
```

### Backup and Recovery
#### Automated Backups
- Daily backups during backup window
- Transaction logs for point-in-time recovery
- **Retained for 1-365 days** (default 7)
- Stored in multi-regional Cloud Storage
- **Incremental** (only changes after first full backup)

#### On-Demand Backups
- Manual backups, retained until deleted
- Useful before major changes
- Don't count toward automated backup limit

#### Point-in-Time Recovery (PITR)
- Restore to any point within retention period
- Uses automated backups + transaction logs
- Creates new instance (doesn't overwrite existing)
- **Enabled by default** for MySQL and PostgreSQL

### Maintenance Windows
- Weekly 4-hour maintenance window
- Updates, patches, minor version upgrades
- Can specify day/time or let Google choose
- HA instances: Minimal downtime (failover)
- Standalone: Brief downtime during maintenance

### Database Flags
- Configure database engine settings
- Similar to parameter groups in RDS
- Some flags require restart
- Custom flags per instance
- Examples: `max_connections`, `slow_query_log`, `timezone`

### Cloud SQL Insights
**AWS Equivalent:** RDS Performance Insights
- **Query performance monitoring** (PostgreSQL and MySQL)
- Identify slow queries and bottlenecks
- Wait event analysis
- Top queries by latency, CPU, I/O
- Free for MySQL, **paid for PostgreSQL**

### Data Protection
- **Encryption at rest**: All data encrypted by default (AES-256)
- **Encryption in transit**: SSL/TLS connections
- **Customer-Managed Encryption Keys (CMEK)**: Use Cloud KMS keys
- **Deletion protection**: Prevent accidental deletion
- **IAM integration**: Fine-grained access control

### Limitations
- **Maximum 64 TB storage** (MySQL, PostgreSQL)
- **Maximum 96 vCPUs** per instance
- Cannot access underlying OS (fully managed)
- Some database extensions not supported
- No cross-region HA (only read replicas)
- Connection limits based on instance size

### Cloud SQL vs AWS RDS Comparison
| Feature | Cloud SQL | AWS RDS |
|---------|-----------|---------|
| HA Architecture | Regional disk + standby | Multi-AZ with sync replica |
| Failover Time | ~60 seconds | ~60-120 seconds |
| Storage Auto-resize | Yes, up to limit | Yes, up to limit |
| Read Replicas | Up to 10 | Up to 15 (varies by engine) |
| Connection Proxy | Cloud SQL Proxy | No equivalent |
| Private Connectivity | VPC peering | VPC, PrivateLink |
| PITR Retention | 1-365 days | Up to 35 days |

### Pricing
- **Instance**: Per vCPU and memory, per second billing
- **Storage**: Per GB/month (SSD more expensive than HDD)
- **Backups**: Free up to instance size, then per GB/month
- **Network egress**: Charged for internet egress
- **HA instances**: ~2x instance cost
- **Shared-core**: From ~$7/month
- **Dedicated-core**: From ~$25/month (db-f1-micro)

### Use Cases
- **Web and mobile applications**: CRUD operations, user data
- **E-commerce platforms**: Product catalogs, orders, inventory
- **Content management systems**: WordPress, Drupal
- **SaaS applications**: Multi-tenant data storage
- **Line-of-business apps**: ERP, CRM systems
- **Migrations from on-prem**: Lift-and-shift SQL databases

### When NOT to Use Cloud SQL
- Need global distribution → Use [[cloud-spanner|Cloud Spanner]]
- Need >64 TB storage → Use [[cloud-spanner|Cloud Spanner]] or Bigtable
- Need >96 vCPUs → Use [[cloud-spanner|Cloud Spanner]]
- NoSQL requirements → Use Firestore or Bigtable
- Analytical workloads → Use BigQuery
- Extremely high performance PostgreSQL → Use [[alloydb|AlloyDB]]

---

## ACE Level

### Essential gcloud Commands
```bash
# List instances
gcloud sql instances list

# Create MySQL instance
gcloud sql instances create INSTANCE_NAME \
  --database-version=MYSQL_8_0 \
  --tier=db-n1-standard-1 \
  --region=us-central1

# Create PostgreSQL instance with HA
gcloud sql instances create INSTANCE_NAME \
  --database-version=POSTGRES_15 \
  --tier=db-custom-2-8192 \
  --region=us-central1 \
  --availability-type=REGIONAL

# Describe instance
gcloud sql instances describe INSTANCE_NAME

# Create database
gcloud sql databases create DATABASE_NAME --instance=INSTANCE_NAME

# Create user
gcloud sql users create USERNAME \
  --instance=INSTANCE_NAME \
  --password=PASSWORD

# Connect to instance (Cloud SQL Proxy method)
gcloud sql connect INSTANCE_NAME --user=root

# Create backup
gcloud sql backups create --instance=INSTANCE_NAME

# List backups
gcloud sql backups list --instance=INSTANCE_NAME

# Restore from backup
gcloud sql backups restore BACKUP_ID \
  --backup-instance=SOURCE_INSTANCE \
  --backup-id=BACKUP_ID

# Create read replica
gcloud sql instances create REPLICA_NAME \
  --master-instance-name=PRIMARY_INSTANCE \
  --tier=db-n1-standard-1 \
  --region=us-east1

# Delete instance
gcloud sql instances delete INSTANCE_NAME

# Patch instance (update settings)
gcloud sql instances patch INSTANCE_NAME \
  --tier=db-n1-standard-2 \
  --enable-bin-log

# Export database
gcloud sql export sql INSTANCE_NAME gs://BUCKET/export.sql \
  --database=DATABASE_NAME

# Import database
gcloud sql import sql INSTANCE_NAME gs://BUCKET/import.sql \
  --database=DATABASE_NAME
```

### Key Concepts for ACE
- Creating and managing Cloud SQL instances
- Choosing appropriate machine types and storage
- Configuring backups and point-in-time recovery
- Creating databases and users
- Connecting to instances (public IP, private IP, Cloud SQL Proxy)
- Setting up read replicas
- Importing and exporting data
- Monitoring instance metrics
- Understanding pricing model
- Enabling high availability

---

## PCA Level

### Architectural Patterns
#### High Availability Architecture
```
[App Tier - GKE/Compute Engine]
         |
    [Cloud SQL Proxy]
         |
    [Cloud SQL HA]
    /           \
Primary (Zone A) → Standby (Zone B)
    |
[Regional Persistent Disk]
```

#### Read-Heavy Workload Pattern
- Primary for writes
- Multiple read replicas for read scaling
- Application-level read/write splitting
- Consider connection pooling (Cloud SQL Proxy, PgBouncer)

#### Disaster Recovery Pattern
- Cross-region read replica
- Automated backups to Cloud Storage (multi-region)
- Regular restore testing
- RPO: Minutes to hours (depending on replication lag)
- RTO: Minutes (replica promotion time)

### Migration Strategies
#### Database Migration Service (DMS)
**AWS Equivalent:** AWS DMS
- **Serverless, minimal downtime migration**
- Supports homogeneous (MySQL→MySQL) and heterogeneous migrations
- Continuous replication (CDC)
- Source: On-prem, AWS RDS, Cloud SQL, other clouds
- Automated schema conversion for some paths

#### Manual Migration
- **Export/Import**: Small databases, planned downtime
- **Replication**: Larger databases, minimal downtime
  - External primary replication (on-prem → Cloud SQL)
  - Cutover when caught up
- **Third-party tools**: Striim, Attunity, custom scripts

### Performance Optimization
#### Instance Sizing
- Monitor CPU, memory, disk I/O with Cloud Monitoring
- Use Cloud SQL Insights for query performance
- Vertical scaling: Change machine type (requires brief downtime)
- Horizontal scaling: Add read replicas

#### Storage Performance
- SSD for IOPS-intensive workloads
- Provision sufficient IOPS (scales with storage size)
- Monitor disk utilization and queue depth
- Consider [[alloydb|AlloyDB]] for extreme performance needs

#### Connection Management
- Use connection pooling (Cloud SQL Proxy, PgBouncer, ProxySQL)
- Monitor connection count vs max_connections
- Close idle connections
- Use persistent connections from application

#### Query Optimization
- Cloud SQL Insights for slow query identification
- Enable slow query log
- Create appropriate indexes
- Analyze query execution plans
- Consider materialized views for PostgreSQL

### Security Best Practices
- **Private IP only** for production workloads
- **Cloud SQL Proxy** for IAM-based authentication
- **CMEK** for regulatory compliance
- **Deletion protection** enabled
- **Automated backups** with appropriate retention
- **SSL/TLS enforcement** for all connections
- **Least privilege IAM roles**:
  - `roles/cloudsql.client` for applications
  - `roles/cloudsql.admin` for administrators
- **Audit logging** with Cloud Audit Logs
- **[[networking-vpc|VPC Service Controls]]** for data exfiltration prevention

### Cost Optimization Strategies
- **Committed Use Discounts**: 1 or 3 year, **up to 60% savings**
- **Shared-core instances** for dev/test (up to 90% cheaper)
- **HDD storage** for infrequently accessed data
- **Delete unused read replicas**
- **Schedule dev/test instance shutdowns** (use Cloud Scheduler)
- **Right-size instances** based on monitoring
- **Backup optimization**: Monitor backup storage costs
- **Cross-region replica only when needed** (egress costs)

### High Availability Design Considerations
- **Regional HA for production** (99.95% SLA)
- Configure maintenance windows during low-traffic periods
- Set up monitoring and alerting for failover events
- Test failover scenarios (trigger manual failover)
- Document RTO/RPO requirements
- Consider multi-region strategy for DR
- Application retry logic for transient failures

### Backup and DR Strategy
- **3-2-1 Rule**: 3 copies, 2 media types, 1 offsite
  - Automated daily backups
  - On-demand backups before changes
  - Cross-region read replica or exports
- **Retention policy**: Based on compliance requirements
- **Regular restore testing**: Automated or manual
- **Export to Cloud Storage**: For long-term archival
- **Point-in-time recovery**: Ensure enabled for critical databases

### Monitoring and Observability
**Key Metrics:**
- Database connections (active, idle)
- CPU and memory utilization
- Disk I/O (read/write IOPS, throughput)
- Replication lag (for replicas)
- Query latency (Cloud SQL Insights)
- Storage utilization and auto-resize events

**Alerting:**
- CPU >80% for sustained period
- Memory >90%
- Storage >85%
- Replication lag >5 minutes
- Failed connections
- Backup failures

### Integration Patterns
#### With GKE
```yaml
# Use Workload Identity + Cloud SQL Proxy sidecar
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  serviceAccountName: ksa
  containers:
  - name: app
    image: myapp
  - name: cloud-sql-proxy
    image: gcr.io/cloud-sql-connectors/cloud-sql-proxy
    args:
      - "--structured-logs"
      - "--port=5432"
      - "PROJECT:REGION:INSTANCE"
```

#### With Cloud Run
- Use Cloud SQL connections (built-in Cloud SQL Proxy)
- Set connection name in environment
- Use Secret Manager for credentials

#### With App Engine
- Built-in Cloud SQL connector
- Configure in app.yaml
- Automatic connection pooling

### Well-Architected Considerations
- **Operational Excellence**:
  - Automated backups and patching
  - Cloud SQL Insights for performance monitoring
  - Infrastructure as Code (Terraform, Deployment Manager)
- **Reliability**:
  - Regional HA for production
  - Cross-region replicas for DR
  - Regular backup and restore testing
- **Security**:
  - Private IP and VPC Service Controls
  - CMEK for encryption
  - IAM and Cloud SQL Proxy for authentication
- **Performance**:
  - Appropriate instance sizing
  - SSD storage for IOPS
  - Read replicas for scaling
  - Connection pooling
- **Cost**:
  - Committed use discounts
  - Right-sizing based on metrics
  - Shared-core for non-production
- **Sustainability**:
  - Right-size to reduce waste
  - Use sustained use discounts
