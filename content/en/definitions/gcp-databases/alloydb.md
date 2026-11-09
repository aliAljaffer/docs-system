---
title: Alloydb
category: GCP Databases
description: 'GCP Databases note: Alloydb.'
tags:
- gcp
- databases
---

<!-- imported from ObsidianVault/studies/cloud-architecht/gcp/databases/alloydb.md. Edit the source, then run sync.py. -->

# Alloydb

`gcp` `databases`

## AlloyDB
**AWS Equivalent:** Aurora PostgreSQL
**Fully managed PostgreSQL-compatible database** optimized for demanding enterprise workloads

### Key Characteristics
- **100x faster analytics** than standard PostgreSQL
- **4x faster transactions** than standard PostgreSQL
- **Fully PostgreSQL compatible** (100% compatibility)
- **Columnar engine** for analytics (unique to AlloyDB)
- **99.99% SLA** (multi-zone clusters)
- **Automated backups and PITR** (point-in-time recovery)
- **Horizontal read scaling** with read pools
- **AI/ML integration** (built-in vector search)
- **Separation of compute and storage** (up to 64 TB)

### AlloyDB vs Aurora vs Cloud SQL
| Feature | AlloyDB | Aurora PostgreSQL | Cloud SQL PostgreSQL |
|---------|---------|-------------------|----------------------|
| Performance | Highest | High | Standard |
| Transactional | 4x faster | 3x faster | 1x (baseline) |
| Analytical | 100x faster | 2-5x faster | 1x (baseline) |
| PostgreSQL Compat | 100% | 99%+ | 100% |
| Columnar Engine | Yes (unique) | No | No |
| Max Storage | 64 TB | 128 TB | 64 TB |
| Read Replicas | Read pools (auto-scale) | Up to 15 | Up to 10 |
| Price | Highest | High | Lowest |
| Best For | Enterprise, hybrid OLTP/OLAP | High performance OLTP | General purpose |

**When to choose AlloyDB:**
- Need **PostgreSQL + analytics** on same database
- **Enterprise-grade performance** required
- Want to **consolidate OLTP + OLAP** workloads
- Migrating from Oracle or commercial databases
- Need predictable, low-latency performance

### Architecture
#### Compute and Storage Separation
- **Compute (instances)**: Primary and read pools
- **Storage**: Distributed, automatically scaling up to 64 TB
- **Columnar engine**: Automatic caching of hot data in columnar format
- **Intelligent caching**: ML-based prediction of data access patterns

#### Cluster Components
```
AlloyDB Cluster
├── Primary Instance (read-write)
├── Read Pool Instances (read-only, auto-scale)
├── Shared Storage Layer (up to 64 TB)
└── Columnar Engine Cache
```

### Instance Types
#### Primary Instance
- **Read-write** operations
- Single primary per cluster
- **Automatic failover** to standby (if configured)
- All writes go through primary

#### Read Pool Instances
**AWS Equivalent:** Aurora Read Replicas
- **Read-only** operations
- **Auto-scaling** (2-20 instances)
- **Load balanced** automatically
- **Same storage** as primary (no replication lag)
- Offload analytics and reporting

**Unique feature:** Read pools share same storage, so **zero replication lag**

### Machine Types
#### Predefined Configurations
- **2 vCPUs**: 16 GB RAM (dev/test)
- **4 vCPUs**: 32 GB RAM (small production)
- **8 vCPUs**: 64 GB RAM (medium production)
- **16 vCPUs**: 128 GB RAM (large production)
- **32 vCPUs**: 256 GB RAM (very large production)
- **64 vCPUs**: 512 GB RAM (enterprise workloads)

#### Custom Configurations
- Choose vCPUs and memory independently
- 2-64 vCPUs
- Up to 8 GB RAM per vCPU

### Columnar Engine
**Unique to AlloyDB (AWS Aurora doesn't have this)**
- **Automatically caches hot data in columnar format**
- **Transparent to applications** (no code changes)
- **100x faster analytics** on transactional data
- Works alongside row-based storage
- ML-driven prediction of columnar candidates

**How it works:**
1. Primary stores data in row format (PostgreSQL)
2. Columnar engine identifies frequently scanned columns
3. Automatically creates columnar cache
4. Analytics queries use columnar format (faster)
5. Transactional queries use row format (ACID)

**Use cases:**
- Real-time analytics on operational data
- Eliminate separate data warehouse for many use cases
- Run reports without impacting OLTP performance

### High Availability
#### Multi-Zone Configuration (Recommended)
- Primary in one zone
- Standby in another zone (same region)
- **Automatic failover in ~60 seconds**
- **99.99% SLA**
- **Synchronous replication** to standby
- No data loss on failover (RPO = 0)

#### Single-Zone Configuration
- Primary only
- 99.9% SLA
- Lower cost (no standby)
- Use for dev/test only

### Backup and Recovery
#### Automated Backups
- **Continuous backups** to Cloud Storage
- **Retention: 1-35 days** (configurable)
- **Point-in-time recovery (PITR)** to any second within retention
- **Incremental backups** (efficient storage)
- **No performance impact** on production

#### On-Demand Backups
- Manual backups retained until deleted
- Useful before major changes
- Independent of automated backup retention

#### Recovery
```bash
# Restore to point in time
gcloud alloydb backups create BACKUP_ID \
  --cluster=CLUSTER_ID \
  --region=REGION

# Restore cluster from backup
gcloud alloydb clusters restore CLUSTER_ID \
  --source-backup=BACKUP_ID \
  --region=REGION
```

### Connection Pooling
#### Built-in PgBouncer
- **Native connection pooling** (no external tool needed)
- Transaction-level pooling
- Reduces connection overhead
- **Recommended for applications with many short connections**

**AWS Aurora:** Requires RDS Proxy (separate service, additional cost)

### AI and ML Features
#### Vector Search (Embeddings)
**AWS Aurora:** Not available natively
- **Built-in vector similarity search**
- Store and query ML embeddings
- Use cases: Recommendation engines, semantic search, image similarity

```sql
-- Create table with vector column
CREATE TABLE items (
  id SERIAL PRIMARY KEY,
  embedding vector(128)
);

-- Create vector index
CREATE INDEX ON items USING ivfflat (embedding vector_cosine_ops);

-- Query similar vectors
SELECT id FROM items
ORDER BY embedding <-> '[0.1, 0.2, ..., 0.128]'::vector
LIMIT 10;
```

#### Integration with Vertex AI
- Deploy ML models alongside database
- Invoke models from SQL queries
- Real-time predictions

### Query Insights
**AWS Equivalent:** Performance Insights
- **Query performance monitoring**
- Identify slow queries and bottlenecks
- Wait event analysis
- Top queries by CPU, I/O, latency
- Historical performance data

### Database Flags
- Configure PostgreSQL settings
- Examples: `max_connections`, `shared_buffers`, `work_mem`
- Some flags require restart
- Custom flags per cluster

### Networking
#### Private IP (VPC)
- **Recommended for production**
- Instance gets private IP from VPC
- No internet exposure
- Low-latency from [[compute-engine|Compute Engine]] and [[gke|GKE]]

#### Public IP
- Internet-accessible (with SSL/TLS)
- **Not recommended for production**
- Use for development or migration

#### AlloyDB Auth Proxy
**AWS Equivalent:** IAM Database Authentication
- **IAM-based authentication**
- Automatic SSL/TLS encryption
- No need to manage IP allowlists
- Similar to Cloud SQL Proxy

### Pricing
#### Compute (Instances)
- **Primary instance**: $0.227 per vCPU/hour (~$164/vCPU/month)
- **Read pool instance**: $0.227 per vCPU/hour
- Example: 4 vCPU primary + 2x2 vCPU read pool = 8 vCPUs = ~$1,312/month

#### Storage
- **Active storage**: $0.35 per GB/month
- **Backup storage**: $0.10 per GB/month
- Example: 1 TB storage + 1 TB backup = $350 + $100 = $450/month

#### Network
- Standard GCP egress rates
- No charge for VPC traffic

**Minimum cost (HA):**
- 2 vCPU primary + 100 GB storage ≈ $350-400/month

**Compared to Cloud SQL:**
- **~2-3x more expensive** than Cloud SQL
- **Worth it for performance-critical workloads**

### Use Cases
- **Enterprise applications**: ERP, CRM, core banking
- **Real-time analytics**: Operational dashboards, BI on live data
- **SaaS platforms**: Multi-tenant applications
- **E-commerce**: Product catalogs, inventory, orders
- **Financial services**: Trading platforms, risk analytics
- **Gaming**: Player profiles, leaderboards
- **IoT**: Device data with real-time analytics

### When to Use AlloyDB
- **High-performance PostgreSQL** required
- **Analytics on transactional data** (hybrid OLTP/OLAP)
- Migrating from Oracle/SQL Server (PostgreSQL compatible)
- Need predictable low-latency performance
- Enterprise SLA requirements (99.99%)
- Can justify higher cost for performance

### When NOT to Use AlloyDB
- **Budget constraints** → Use Cloud SQL (2-3x cheaper)
- **Simple workloads** → Use Cloud SQL
- **Global distribution** required → Use [[cloud-spanner|Cloud Spanner]]
- **NoSQL better fit** → Use Firestore or Bigtable
- **Pure analytics** → Use BigQuery
- **MySQL or SQL Server** required → Use Cloud SQL
- Small datasets (<100 GB) with low traffic → Use Cloud SQL

### Migration Strategies
#### Database Migration Service (DMS)
**AWS Equivalent:** AWS DMS
- **Serverless, minimal downtime migration**
- Source: On-prem PostgreSQL, Cloud SQL, AWS RDS
- Continuous replication (CDC)
- Automated schema conversion

#### Manual Migration
- **pg_dump/pg_restore**: Small to medium databases
- **Streaming replication**: Minimal downtime for large databases
- **Third-party tools**: Striim, Attunity

#### From Oracle
- Oracle to PostgreSQL conversion tools
- Schema and code conversion required
- Test thoroughly (syntax differences)

---

## ACE Level

### Essential gcloud Commands
```bash
# Create cluster (HA configuration)
gcloud alloydb clusters create CLUSTER_ID \
  --region=REGION \
  --network=VPC_NETWORK \
  --password=PASSWORD

# Create primary instance
gcloud alloydb instances create PRIMARY_INSTANCE_ID \
  --cluster=CLUSTER_ID \
  --region=REGION \
  --instance-type=PRIMARY \
  --cpu-count=4

# Create read pool
gcloud alloydb instances create READ_POOL_ID \
  --cluster=CLUSTER_ID \
  --region=REGION \
  --instance-type=READ_POOL \
  --read-pool-node-count=2 \
  --cpu-count=2

# List clusters
gcloud alloydb clusters list --region=REGION

# Describe cluster
gcloud alloydb clusters describe CLUSTER_ID --region=REGION

# Update instance (scale up/down)
gcloud alloydb instances update INSTANCE_ID \
  --cluster=CLUSTER_ID \
  --region=REGION \
  --cpu-count=8

# Create backup
gcloud alloydb backups create BACKUP_ID \
  --cluster=CLUSTER_ID \
  --region=REGION

# List backups
gcloud alloydb backups list --region=REGION

# Restore from backup
gcloud alloydb clusters restore CLUSTER_ID \
  --source-backup=BACKUP_ID \
  --region=REGION

# Delete instance
gcloud alloydb instances delete INSTANCE_ID \
  --cluster=CLUSTER_ID \
  --region=REGION

# Delete cluster
gcloud alloydb clusters delete CLUSTER_ID --region=REGION
```

### Connecting to AlloyDB
```bash
# Install AlloyDB Auth Proxy
curl -o alloydb-auth-proxy https://storage.googleapis.com/alloydb-auth-proxy/alloydb-auth-proxy.linux.amd64
chmod +x alloydb-auth-proxy

# Start proxy
./alloydb-auth-proxy \
  --address 0.0.0.0 \
  --port 5432 \
  projects/PROJECT_ID/locations/REGION/clusters/CLUSTER_ID/instances/INSTANCE_ID

# Connect with psql
psql -h 127.0.0.1 -p 5432 -U postgres
```

### Basic PostgreSQL Operations
```sql
-- Create database
CREATE DATABASE mydb;

-- Connect to database
\c mydb

-- Create table
CREATE TABLE customers (
  customer_id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100) UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert data
INSERT INTO customers (name, email) VALUES
  ('Alice', 'alice@example.com'),
  ('Bob', 'bob@example.com');

-- Query data
SELECT * FROM customers WHERE name = 'Alice';

-- Update data
UPDATE customers SET email = 'newalice@example.com' WHERE customer_id = 1;

-- Delete data
DELETE FROM customers WHERE customer_id = 2;

-- Create index
CREATE INDEX idx_customers_email ON customers(email);

-- View table schema
\d customers

-- List all tables
\dt

-- Show database size
SELECT pg_size_pretty(pg_database_size('mydb'));
```

### Key Concepts for ACE
- Creating and managing AlloyDB clusters
- Understanding primary and read pool instances
- Configuring high availability
- Creating and restoring backups
- Connecting via AlloyDB Auth Proxy
- Basic PostgreSQL operations (DDL, DML)
- Scaling instances (CPU/memory)
- Monitoring instance metrics
- Understanding pricing model
- Difference between AlloyDB and Cloud SQL

---

## PCA Level

### Architectural Patterns
#### High Availability Architecture
```
[Application Tier - GKE/Compute Engine]
         |
  [AlloyDB Auth Proxy]
         |
    [AlloyDB Cluster]
    /              \
Primary (Zone A) → Standby (Zone B)
    |                  |
[Shared Storage Layer - up to 64 TB]
         |
  [Columnar Engine Cache]
```

**Benefits:**
- 99.99% SLA
- Automatic failover
- Zero data loss (RPO = 0)
- ~60 second RTO

#### Read Scaling Architecture
```
[Application - Write Path] → [Primary Instance]
                                     ↓
                            [Shared Storage]
                                     ↑
[Application - Read Path] → [Read Pool - Auto-scale 2-20 nodes]
                             [Load Balanced]
```

**Benefits:**
- Horizontal read scaling
- Zero replication lag (shared storage)
- Automatic load balancing
- Auto-scaling based on CPU

#### Hybrid OLTP/OLAP Architecture
```
[Transactional Workload] → [Primary Instance - Row Storage]
                                     ↓
                            [Shared Storage]
                                     ↑
[Analytics Workload] → [Read Pool - Columnar Engine]
                       [100x faster analytics]
```

**Benefits:**
- Eliminate separate data warehouse
- Real-time analytics on operational data
- No ETL required for many use cases

### Schema Design Best Practices
#### Partitioning (Declarative)
```sql
-- Range partitioning by date
CREATE TABLE orders (
  order_id BIGSERIAL,
  order_date DATE,
  customer_id INT,
  amount DECIMAL(10,2)
) PARTITION BY RANGE (order_date);

-- Create partitions
CREATE TABLE orders_2024_01 PARTITION OF orders
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE orders_2024_02 PARTITION OF orders
  FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Query automatically routes to correct partition
SELECT * FROM orders WHERE order_date = '2024-01-15';
```

#### Indexing Strategies
```sql
-- B-tree index (default, most common)
CREATE INDEX idx_customers_email ON customers(email);

-- Partial index (smaller, faster)
CREATE INDEX idx_active_users ON users(created_at)
WHERE status = 'active';

-- Covering index (index-only scans)
CREATE INDEX idx_orders_customer ON orders(customer_id)
INCLUDE (order_date, amount);

-- Multi-column index (order matters)
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- GiST index for full-text search
CREATE INDEX idx_products_search ON products USING GiST (to_tsvector('english', name));
```

### Performance Optimization
#### Query Optimization
```sql
-- Use EXPLAIN ANALYZE to understand query plans
EXPLAIN ANALYZE
SELECT c.name, o.amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date > '2024-01-01';

-- Key metrics to look at:
-- - Seq Scan vs Index Scan
-- - Nested Loop vs Hash Join
-- - Rows estimated vs actual
-- - Execution time
```

#### Connection Pooling
```python
# Use built-in PgBouncer or application-level pooling
from psycopg2 import pool

connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=20,
    host="127.0.0.1",
    port=5432,
    database="mydb",
    user="postgres",
    password="password"
)

# Get connection from pool
conn = connection_pool.getconn()
# Use connection
# Return to pool
connection_pool.putconn(conn)
```

#### Vacuum and Analyze
```sql
-- Regular maintenance (automatic by default)
VACUUM ANALYZE customers;

-- Check table bloat
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Monitoring and Observability
#### Query Insights Usage
```sql
-- View top queries by total time
SELECT
  query,
  calls,
  total_time,
  mean_time,
  max_time
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- Identify slow queries
SELECT
  query,
  mean_time,
  stddev_time
FROM pg_stat_statements
WHERE mean_time > 1000  -- Queries slower than 1 second
ORDER BY mean_time DESC;
```

#### Key Metrics to Monitor
- **Connection count**: Monitor vs max_connections
- **CPU utilization**: Target <75%
- **Memory usage**: Monitor for OOM
- **Disk I/O**: Read/write throughput
- **Replication lag**: Should be 0 (read pools use shared storage)
- **Query latency**: P50, P95, P99
- **Transaction rate**: Commits/second
- **Cache hit ratio**: Target >99%

#### Alerting Setup
```
Alerts:
- CPU >80% for 5 minutes
- Memory >90%
- Connection count >80% of max
- Slow query >10 seconds
- Backup failure
- High replication lag (if using external replicas)
```

### Cost Optimization Strategies
#### Right-Sizing Instances
```bash
# Monitor CPU and memory usage
# Scale down if consistently <50% utilized
gcloud alloydb instances update INSTANCE_ID \
  --cpu-count=2  # Scale down from 4 to 2 vCPUs
```

#### Read Pool Auto-Scaling
```bash
# Configure auto-scaling to match demand
gcloud alloydb instances update READ_POOL_ID \
  --read-pool-node-count=2 \
  --read-pool-min-node-count=2 \
  --read-pool-max-node-count=10
```

#### Storage Optimization
- Monitor storage growth
- Archive old data to [[cloud-storage|Cloud Storage]]
- Implement data retention policies
- Use partitioning to drop old partitions

#### When to Use Cloud SQL Instead
```
Decision Matrix:
- Workload is not performance-critical → Cloud SQL
- Budget <$500/month → Cloud SQL
- Simple CRUD operations → Cloud SQL
- Analytics on transactional data → AlloyDB
- Need 99.99% SLA → AlloyDB
- PostgreSQL performance bottleneck → AlloyDB
```

### Security Best Practices
#### IAM and Authentication
```bash
# Use IAM database authentication
gcloud alloydb instances describe INSTANCE_ID \
  --cluster=CLUSTER_ID \
  --region=REGION

# Grant IAM roles
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member='user:analyst@example.com' \
  --role='roles/alloydb.viewer'
```

#### Encryption
- **At-rest**: Default encryption or CMEK via Cloud KMS
- **In-transit**: SSL/TLS required (enforced)
- **Column-level**: Use pgcrypto extension

```sql
-- Enable pgcrypto extension
CREATE EXTENSION pgcrypto;

-- Encrypt sensitive data
INSERT INTO customers (name, ssn)
VALUES ('Alice', pgp_sym_encrypt('123-45-6789', 'encryption_key'));

-- Decrypt
SELECT name, pgp_sym_decrypt(ssn, 'encryption_key')::text as ssn
FROM customers;
```

#### Network Security
- Use Private IP (VPC) for production
- VPC Service Controls to prevent data exfiltration
- Firewall rules to restrict access
- AlloyDB Auth Proxy for secure connections

#### Audit Logging
```sql
-- Enable pgaudit extension
CREATE EXTENSION pgaudit;

-- Configure audit logging
ALTER SYSTEM SET pgaudit.log = 'all';
SELECT pg_reload_conf();

-- View audit logs in Cloud Logging
```

### Disaster Recovery Strategies
#### Backup Strategy
```bash
# Automated daily backups with 35-day retention
gcloud alloydb clusters update CLUSTER_ID \
  --region=REGION \
  --automated-backup-retention-period=35d

# On-demand backup before major changes
gcloud alloydb backups create pre-migration-backup \
  --cluster=CLUSTER_ID \
  --region=REGION
```

#### Cross-Region DR
```bash
# Export database
pg_dump -h ALLOYDB_IP -U postgres -d mydb > backup.sql

# Transfer to DR region Cloud Storage
gsutil cp backup.sql gs://dr-bucket/

# Create AlloyDB cluster in DR region
gcloud alloydb clusters create dr-cluster --region=DR_REGION ...

# Restore
psql -h DR_ALLOYDB_IP -U postgres -d mydb < backup.sql
```

#### RTO/RPO Considerations
- **Multi-zone HA**: RPO = 0, RTO = ~60 seconds
- **Automated backups + PITR**: RPO = <1 second, RTO = minutes
- **Cross-region DR**: RPO = minutes to hours, RTO = hours

### Advanced Features
#### Logical Replication (External)
```sql
-- For replicating to external PostgreSQL or other AlloyDB clusters
-- Create publication on primary
CREATE PUBLICATION my_publication FOR ALL TABLES;

-- Create subscription on replica
CREATE SUBSCRIPTION my_subscription
  CONNECTION 'host=primary_ip dbname=mydb user=repl_user password=pass'
  PUBLICATION my_publication;
```

#### Extensions
```sql
-- Popular PostgreSQL extensions available
CREATE EXTENSION postgis;        -- Geographic data
CREATE EXTENSION pg_trgm;        -- Fuzzy text matching
CREATE EXTENSION hstore;         -- Key-value store
CREATE EXTENSION uuid-ossp;      -- UUID generation
CREATE EXTENSION pg_stat_statements;  -- Query statistics
CREATE EXTENSION pgcrypto;       -- Cryptographic functions
CREATE EXTENSION vector;         -- Vector similarity search
```

#### Columnar Engine Optimization
```sql
-- Query to verify columnar engine usage
EXPLAIN (ANALYZE, BUFFERS)
SELECT category, SUM(amount)
FROM orders
WHERE order_date > '2024-01-01'
GROUP BY category;

-- Look for "Columnar Scan" in execution plan
-- Indicates columnar engine is being used (100x faster)
```

### Migration Best Practices
#### Pre-Migration Assessment
```sql
-- Assess database size
SELECT pg_size_pretty(pg_database_size('mydb'));

-- Identify largest tables
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;

-- Check for unsupported features (if migrating from other DB)
-- Review extensions usage
SELECT * FROM pg_extension;
```

#### Migration Execution
1. **Test in non-production**: Create test AlloyDB cluster
2. **Schema migration**: Use pg_dump for schema only
3. **Data migration**: Use DMS or pg_dump/pg_restore
4. **Validation**: Compare row counts, sample queries
5. **Performance testing**: Run production-like workload
6. **Cutover**: Planned maintenance window or dual-write

### Integration Patterns
#### With GKE
```yaml
# Use Workload Identity + AlloyDB Auth Proxy sidecar
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  serviceAccountName: ksa
  containers:
  - name: app
    image: myapp
    env:
    - name: DB_HOST
      value: "127.0.0.1"
    - name: DB_PORT
      value: "5432"
  - name: alloydb-proxy
    image: gcr.io/alloydb-connectors/alloydb-auth-proxy:latest
    args:
      - "--structured-logs"
      - "--port=5432"
      - "projects/PROJECT/locations/REGION/clusters/CLUSTER/instances/INSTANCE"
```

#### With Cloud Run
```yaml
# Cloud Run service with AlloyDB
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: myservice
spec:
  template:
    metadata:
      annotations:
        run.googleapis.com/vpc-access-connector: vpc-connector
    spec:
      containers:
      - image: gcr.io/project/image
        env:
        - name: DB_HOST
          value: "ALLOYDB_PRIVATE_IP"
        - name: DB_PORT
          value: "5432"
```

#### With BigQuery (Analytics)
```sql
-- Use federated queries to query AlloyDB from BigQuery
SELECT *
FROM EXTERNAL_QUERY(
  'projects/PROJECT/locations/REGION/connections/CONNECTION',
  'SELECT * FROM orders WHERE order_date > ''2024-01-01'''
);

-- Or export to BigQuery periodically for analytics
```

### Well-Architected Considerations
- **Operational Excellence**:
  - Automated backups and PITR
  - Query Insights for performance monitoring
  - Infrastructure as Code (Terraform)
- **Reliability**:
  - Multi-zone HA for 99.99% SLA
  - Automatic failover
  - Regular backup and restore testing
- **Security**:
  - Private IP and VPC Service Controls
  - CMEK for encryption
  - IAM and AlloyDB Auth Proxy for authentication
  - Audit logging
- **Performance**:
  - Columnar engine for analytics
  - Read pools for horizontal scaling
  - Proper indexing and query optimization
  - Connection pooling
- **Cost**:
  - Right-sizing based on metrics
  - Auto-scaling read pools
  - Consider Cloud SQL for non-critical workloads
- **Sustainability**:
  - Efficient resource utilization
  - Right-size to reduce waste
  - Use columnar engine to consolidate workloads
