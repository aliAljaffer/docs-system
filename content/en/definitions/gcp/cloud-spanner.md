---
title: cloud-spanner
category: GCP
description: 'GCP note: Cloud-spanner.'
tags:
- gcp
- databases
---


# cloud-spanner

## Cloud Spanner
**Globally distributed, horizontally scalable, strongly consistent** relational database

**AWS Equivalent:** Aurora Global Database / DynamoDB Global Tables (hybrid)

### Key Characteristics
- **Unlimited horizontal scalability** (petabytes of data)
- **Automatic sharding** and replication
- **Strong consistency** at global scale (ACID transactions)
- **99.999% SLA** for multi-region (5 nines)
- **SQL interface** (ANSI 2011 standard with extensions)
- **No planned downtime** for maintenance or schema changes
- Synchronous replication across regions
- **TrueTime**: Google's globally synchronized clock for consistency

### Cloud Spanner vs AWS Comparison
| Feature | Cloud Spanner | Aurora Global | DynamoDB Global |
|---------|---------------|---------------|-----------------|
| Consistency | Strong (sync) | Eventual (async) | Eventual (async) |
| SQL Support | Full SQL | Full SQL | NoSQL only |
| Scale Limit | Unlimited | 128 TB per region | Unlimited |
| Multi-region | Native, sync | Async replication | Async replication |
| Schema | Relational | Relational | Key-value/Document |
| Pricing | Per node + storage | Per instance/storage | Per RCU/WCU |

**Why Spanner is Unique:**
- Only database with **global strong consistency + SQL + horizontal scale**
- AWS Aurora Global is SQL + scale but eventually consistent across regions
- DynamoDB Global is eventually consistent + scale but NoSQL only

### Instance Configurations
| Aspect | Regional | Multi-region |
|--------|----------|--------------|
| Replication | Data replicated across **3 zones within 1 region** | Data replicated across **multiple regions** |
| SLA | 99.99% | **99.999%** (5 nines) |
| Latency | Lower latency (single region) | Read from nearest replica (low latency reads) |
| Cost | Lower cost than multi-region | - |
| Writes | - | Commit after majority quorum |
| Use case | Regional applications, data residency requirements | Global applications, disaster recovery |

Multi-region configurations:
- **nam3**: us-east1, us-central1, us-west1
- **nam6**: 6 US regions
- **eur3**: 3 Europe regions
- **nam-eur-asia1**: Global configuration

### Processing Units vs Nodes
| Aspect | Processing units (PUs) | Nodes |
|--------|------------------------|-------|
| Role | Smallest unit of compute (100 PUs = 1 Node) | Legacy pricing model |
| Size | Each PU: ~0.01 node. **Minimum 1000 PUs** for production (or 100 PUs for dev) | 1 Node = 1000 PUs |
| Scaling | Granular scaling | Less granular scaling |
| Status | **Recommended for most use cases** | Still supported but PUs preferred |

**Capacity:**
- 1 Node (1000 PUs): ~2 TB storage, ~10,000 QPS (reads), ~2,000 QPS (writes)
- Scale linearly by adding nodes/PUs

### Data Model
#### Schema Design
- **Interleaved tables** (parent-child co-location):
  ```sql
  CREATE TABLE Customers (
    CustomerId INT64 NOT NULL,
    Name STRING(100),
  ) PRIMARY KEY (CustomerId);

  CREATE TABLE Orders (
    CustomerId INT64 NOT NULL,
    OrderId INT64 NOT NULL,
    Amount FLOAT64,
  ) PRIMARY KEY (CustomerId, OrderId),
    INTERLEAVE IN PARENT Customers ON DELETE CASCADE;
  ```
  - **Child rows stored with parent** for performance
  - Reduces distributed joins
  - **Key Spanner optimization pattern**

#### Primary Keys
- **Critical for performance**: Determines data distribution
- **Avoid monotonically increasing keys** (hotspots)
- Use UUIDs, hash-based keys, or bit-reversed sequences
- Bad: Auto-increment, timestamp
- Good: UUID, hash(customer_id), reversed timestamp

#### Secondary Indexes
- Global indexes (distributed)
- **Storing clause** to include non-key columns (avoid table lookups)
  ```sql
  CREATE INDEX UsersByEmail ON Users(Email) STORING (Name, Created);
  ```
- Null-filtered indexes to reduce storage

### Consistency and Transactions
#### Read Types
- **Strong Read**: Latest committed data, uses leader replica
- **Stale Read**: May read slightly old data, can read from any replica
  - Exact staleness: Read data as of timestamp
  - Bounded staleness: Read data at most X seconds old
  - **Use stale reads for better performance and lower cost**

#### Transaction Types
| Transaction type | Behavior |
|------------------|----------|
| **Read-Write Transactions** | Full ACID, serializable isolation |
| **Read-Only Transactions** | Consistent snapshot, no locks |
| **Partitioned DML** | Large-scale updates, not transactional |

### Backup and Recovery
- **Automated backups**: Configurable retention (1 hour to 366 days)
- **On-demand backups**: Retained until deleted
- **Point-in-time recovery (PITR)**: Restore to any point within retention
- **Version retention**: Query historical data (up to 7 days default)
- Backups stored in multi-region by default
- Restore creates new instance (doesn't overwrite)

### Database Operations
#### Schema Changes
- **Online schema changes** (no downtime)
- Validates schema before applying
- Can take time for large tables
- Monitor with `INFORMATION_SCHEMA.DATABASE_OPTIONS`

#### Data Export/Import
| Tool | Use for |
|------|---------|
| **Cloud Dataflow** | Large-scale exports to Cloud Storage, BigQuery |
| **Cloud Data Fusion** | ETL pipelines |
| **Direct exports** | Native export to Cloud Storage (Avro format) |
| **Cloud Spanner emulator** | Local testing |

### Performance Optimization
#### Query Optimization
- **Query Insights**: Identify expensive queries
- **Execution plans**: `EXPLAIN` for query analysis
- Use indexes appropriately
- Minimize cross-region transactions
- Batch operations when possible

#### Hotspotting Avoidance
- **Avoid monotonically increasing primary keys**
- Use hash-based or UUID keys
- Monitor key visualizations in console
- Distribute writes across key space

#### Client Libraries Best Practices
- Use connection pooling
- Retry transient errors with exponential backoff
- Batch mutations (up to 20,000 per transaction)
- Use read-only transactions for queries

### Pricing
| Model | Regional | Multi-region |
|-------|----------|--------------|
| Processing Units (recommended) | $0.90 per 100 PUs per hour | $3.00-9.00 per 100 PUs per hour (varies by config) |
| Node (legacy) | $9.00 per node per hour | $30.00-90.00 per node per hour |

- **Storage**: $0.30 per GB/month (regional), $0.50 (multi-region)
- **Backup storage**: $0.036-0.054 per GB/month
- **Network egress**: Standard GCP rates
- **Node model**: Same storage and backup costs

**Minimum costs:**
- Regional: ~$650/month (1000 PUs)
- Multi-region: ~$2,200/month (1000 PUs, nam3)

**Cost optimization:**
- Start with regional configuration if global not required
- Use stale reads to reduce read costs
- Monitor CPU utilization (target 65% recommended high water mark)
- Autoscaling available (but manual monitoring recommended)

### When to Use Cloud Spanner
- **Global applications requiring strong consistency**
- **Need to scale beyond single-region database limits**
- Financial transactions (banking, payments)
- Inventory management across regions
- Gaming leaderboards and player data
- Supply chain and logistics
- SaaS applications with global customers
- Any workload requiring >2 TB and strong consistency

### When NOT to Use Cloud Spanner
| Situation | Use instead |
|-----------|-------------|
| Small databases (<100 GB) | [[gcp/cloud-sql|Cloud SQL]] |
| Don't need strong consistency | [[gcp/cloud-sql|Cloud SQL]] with replicas |
| NoSQL better fit | [[gcp/firestore|Firestore]] or [[gcp/bigtable|Bigtable]] |
| Analytical workloads | [[bigquery|BigQuery]] |
| Cost-sensitive with regional requirements | [[gcp/cloud-sql|Cloud SQL]] or [[alloydb|AlloyDB]] |
| Simple key-value access | [[gcp/firestore|Firestore]] |

### Migration to Spanner
#### HarbourBridge
- Open-source tool for schema conversion
- Supports PostgreSQL, MySQL, SQL Server, Oracle
- Converts schema and data
- Identifies potential issues

#### Dataflow + JdbcIO
- For large-scale data migration
- Parallel data loading
- Source: Cloud SQL, on-prem databases

#### Spanner Migration Tool
- Schema conversion and assessment
- Data migration via Datastream
- Validation and testing

---

## ACE Level

### Essential gcloud Commands
```bash
# List instances
gcloud spanner instances list

# Create regional instance
gcloud spanner instances create INSTANCE_NAME \
  --config=regional-us-central1 \
  --processing-units=1000 \
  --description="My Spanner Instance"

# Create multi-region instance
gcloud spanner instances create INSTANCE_NAME \
  --config=nam3 \
  --processing-units=1000 \
  --description="Multi-region instance"

# Update processing units
gcloud spanner instances update INSTANCE_NAME \
  --processing-units=2000

# Create database
gcloud spanner databases create DATABASE_NAME \
  --instance=INSTANCE_NAME

# Execute DDL
gcloud spanner databases ddl update DATABASE_NAME \
  --instance=INSTANCE_NAME \
  --ddl="CREATE TABLE Users (UserId INT64 NOT NULL, Name STRING(100)) PRIMARY KEY (UserId)"

# Query database
gcloud spanner databases execute-sql DATABASE_NAME \
  --instance=INSTANCE_NAME \
  --sql="SELECT * FROM Users"

# Create backup
gcloud spanner backups create BACKUP_NAME \
  --instance=INSTANCE_NAME \
  --database=DATABASE_NAME \
  --retention-period=7d

# Restore from backup
gcloud spanner databases restore \
  --source-instance=INSTANCE_NAME \
  --source-backup=BACKUP_NAME \
  --destination-database=NEW_DATABASE_NAME \
  --destination-instance=INSTANCE_NAME

# List backups
gcloud spanner backups list --instance=INSTANCE_NAME

# Delete instance
gcloud spanner instances delete INSTANCE_NAME
```

### Client Library Example (Python)
```python
from google.cloud import spanner

# Create client
client = spanner.Client()
instance = client.instance('instance-id')
database = instance.database('database-id')

# Read-write transaction
def update_user(transaction, user_id, name):
    transaction.execute_update(
        "UPDATE Users SET Name = @name WHERE UserId = @user_id",
        params={"name": name, "user_id": user_id},
        param_types={"name": spanner.param_types.STRING, "user_id": spanner.param_types.INT64}
    )

database.run_in_transaction(update_user, user_id=1, name="Alice")

# Read query
with database.snapshot() as snapshot:
    results = snapshot.execute_sql("SELECT * FROM Users")
    for row in results:
        print(row)
```

### Key Concepts for ACE
- Creating and managing Spanner instances
- Understanding regional vs multi-region configurations
- Processing units vs nodes
- Creating databases and executing DDL
- Basic SQL queries with Spanner dialect
- Creating and restoring backups
- Understanding Spanner's global consistency model
- Monitoring instance CPU and storage
- Basic schema design (primary keys)

---

## PCA Level

### Architectural Patterns
#### Global Active-Active Pattern
```text
[Users: Americas]     [Users: Europe]      [Users: Asia]
       |                    |                    |
[Cloud Load Balancer - Global]
       |                    |                    |
[App: us-central1]  [App: europe-west1]  [App: asia-east1]
       |                    |                    |
       +--------------------+--------------------+
                            |
                [Cloud Spanner - Multi-region nam-eur-asia1]
                [Strongly consistent across all regions]
```
- Users read/write to nearest replica
- Strong consistency guarantees
- Low-latency reads everywhere
- Writes coordinated globally

#### Microservices with Spanner
- Each service can have own Spanner database
- Or shared Spanner with separate schemas
- Use interleaved tables for service data locality
- Consider cost vs isolation trade-offs

### Schema Design Best Practices
#### Interleaving Strategy
```sql
-- Customer → Orders → LineItems (3-level interleaving)
CREATE TABLE Customers (
  CustomerId STRING(36) NOT NULL,
  Name STRING(100),
  Email STRING(100),
) PRIMARY KEY (CustomerId);

CREATE TABLE Orders (
  CustomerId STRING(36) NOT NULL,
  OrderId STRING(36) NOT NULL,
  OrderDate TIMESTAMP,
  Total FLOAT64,
) PRIMARY KEY (CustomerId, OrderId),
  INTERLEAVE IN PARENT Customers ON DELETE CASCADE;

CREATE TABLE LineItems (
  CustomerId STRING(36) NOT NULL,
  OrderId STRING(36) NOT NULL,
  LineItemId INT64 NOT NULL,
  ProductId STRING(36),
  Quantity INT64,
  Price FLOAT64,
) PRIMARY KEY (CustomerId, OrderId, LineItemId),
  INTERLEAVE IN PARENT Orders ON DELETE CASCADE;
```

**Benefits:**
- Related data co-located (customer + orders + line items)
- Single-shard transactions (very fast)
- Reduced distributed joins
- Better query performance

**When to Interleave:**
- Parent-child relationship (1:N)
- Frequently accessed together
- Updates happen in same transaction

#### Primary Key Design Patterns
##### Anti-pattern - Sequential Keys
```sql
-- BAD: All writes hit same split
CREATE TABLE Events (
  Timestamp TIMESTAMP NOT NULL,
  Data STRING(MAX),
) PRIMARY KEY (Timestamp);
```

##### Pattern 1 - UUID
```sql
-- GOOD: Random distribution
CREATE TABLE Events (
  EventId STRING(36) NOT NULL,  -- UUID
  Timestamp TIMESTAMP,
  Data STRING(MAX),
) PRIMARY KEY (EventId);
```

##### Pattern 2 - Hash + Sequential
```sql
-- GOOD: Distributed but maintains some ordering
CREATE TABLE Events (
  ShardId INT64 NOT NULL,  -- FARM_FINGERPRINT(user_id) % 100
  Timestamp TIMESTAMP NOT NULL,
  Data STRING(MAX),
) PRIMARY KEY (ShardId, Timestamp);
```

##### Pattern 3 - Bit-Reversed Timestamp
```sql
-- GOOD: Maintains ordering within shards
CREATE TABLE Events (
  ReversedTimestamp INT64 NOT NULL,  -- Bit-reverse timestamp
  EventId STRING(36) NOT NULL,
  Data STRING(MAX),
) PRIMARY KEY (ReversedTimestamp, EventId);
```

### Transaction Design
#### Minimize Transaction Scope
```python
# GOOD: Narrow transaction
def transfer_money(transaction, from_account, to_account, amount):
    # Only touch 2 accounts
    transaction.execute_update(
        "UPDATE Accounts SET Balance = Balance - @amount WHERE AccountId = @from",
        params={"amount": amount, "from": from_account}
    )
    transaction.execute_update(
        "UPDATE Accounts SET Balance = Balance + @amount WHERE AccountId = @to",
        params={"amount": amount, "to": to_account}
    )

# BAD: Wide transaction affecting many rows
def update_all_prices(transaction, multiplier):
    transaction.execute_update(
        "UPDATE Products SET Price = Price * @multiplier",
        params={"multiplier": multiplier}
    )  # Locks entire table, high contention
```

#### Use Stale Reads for Analytics
```python
# Use 15-second stale reads for reports (no locks, any replica)
with database.snapshot(exact_staleness=datetime.timedelta(seconds=15)) as snapshot:
    results = snapshot.execute_sql(
        "SELECT SUM(Amount) FROM Orders WHERE OrderDate > @start_date"
    )
```

### High Availability and Disaster Recovery
#### Multi-Region Failure Scenarios
| Failure | Outcome |
|---------|---------|
| **Single zone failure** | Automatic failover, no downtime |
| **Single region failure** | Continues operating (needs majority quorum) |
| **Multi-region failure** | Requires manual intervention if quorum lost |

#### Backup Strategy
- **Automated daily backups** with 7-365 day retention
- **On-demand backups** before major changes
- **Cross-region backup copies** for disaster recovery
- **PITR** for accidental data deletion recovery
- **Version retention** for time-travel queries

#### Testing Disaster Recovery
```bash
# Create backup
gcloud spanner backups create dr-backup \
  --instance=prod-instance \
  --database=prod-db \
  --retention-period=30d

# Restore to different region for DR testing
gcloud spanner databases restore \
  --source-backup=dr-backup \
  --source-instance=prod-instance \
  --destination-database=dr-test-db \
  --destination-instance=dr-instance
```

### Performance Tuning
#### Query Optimization
```sql
-- Use EXPLAIN to see execution plan
@{FORCE_INDEX=UsersByEmail}
SELECT * FROM Users WHERE Email = 'user@example.com';

-- Use query hints
@{JOIN_METHOD=HASH_JOIN}
SELECT o.OrderId, c.Name
FROM Orders o JOIN Customers c ON o.CustomerId = c.CustomerId;

-- Force index usage
@{FORCE_INDEX=OrdersByDate}
SELECT * FROM Orders WHERE OrderDate > '2024-01-01';
```

#### Monitoring Key Metrics
- **CPU utilization**: Target **<65% for multi-region**, <75% for regional
  - High CPU = need more PUs
  - Spiky CPU = consider autoscaling
- **Storage**: Monitor growth, plan capacity
- **Query latency**: P50, P95, P99 latencies
- **Lock wait time**: Indicates contention
- **Bytes read/written**: Traffic patterns

### Security Best Practices
- **IAM roles**:

| Role | Grants |
|------|--------|
| `roles/spanner.databaseReader` | Read-only access |
| `roles/spanner.databaseUser` | Read-write access |
| `roles/spanner.databaseAdmin` | Schema changes |
| `roles/spanner.admin` | Full instance management |

- **VPC Service Controls**: Prevent data exfiltration
- **CMEK**: Customer-managed encryption keys via [[gcp/cloud-kms|Cloud KMS]]
- **Audit logging**: Track all database operations
- **Private Google Access**: Access from VPC without internet
- **Fine-grained access control**: Row-level security via application layer

### Cost Optimization Strategies
#### Right-Sizing
- Monitor CPU utilization
- Regional CPU target: 65% (headroom for peaks)
- Multi-region CPU target: 45% (more headroom for cross-region txns)
- Scale up if consistently >target
- Scale down if consistently <50% of target

#### Autoscaling
```bash
# Set up autoscaling (via API or Console)
# Target CPU: 65%
# Min PUs: 1000
# Max PUs: 5000
# Cooldown: 5 minutes
```

#### Use Regional When Possible
- Multi-region is 3x+ cost
- Only use multi-region if truly need global strong consistency
- Regional + read replicas may suffice for many use cases

#### Optimize Queries
- Use stale reads for analytics (cheaper, no locking)
- Optimize indexes (reduce storage and query cost)
- Batch mutations (reduce transaction overhead)
- Use Partitioned DML for bulk updates

#### Storage Optimization
- Monitor storage growth
- Archive old data to [[gcp/cloud-storage|Cloud Storage]] or [[bigquery|BigQuery]]
- Use `BYTES(MAX)` only when necessary
- Consider data retention policies

### Migration Strategies
#### Phased Migration Approach
1. **Assessment**: Analyze schema, queries, transaction patterns
2. **Schema conversion**: Use HarbourBridge, manual adjustments
3. **Proof of concept**: Test with subset of data
4. **Dual-write period**: Write to both old and new database
5. **Data backfill**: Migrate historical data via Dataflow
6. **Cutover**: Switch reads to Spanner
7. **Decommission**: Remove old database

#### Spanner Emulator for Testing
```bash
# Run local emulator
gcloud emulators spanner start

# Set environment variable
export SPANNER_EMULATOR_HOST=localhost:9010

# Test application locally
python my_app.py
```

### Integration Patterns
#### With BigQuery (Analytics)
```sql
-- Query Spanner from BigQuery via Federated Query
SELECT o.OrderId, o.Total, c.Name
FROM EXTERNAL_QUERY(
  'projects/PROJECT/instances/INSTANCE/databases/DATABASE',
  'SELECT OrderId, CustomerId, Total FROM Orders'
) AS o
JOIN EXTERNAL_QUERY(
  'projects/PROJECT/instances/INSTANCE/databases/DATABASE',
  'SELECT CustomerId, Name FROM Customers'
) AS c ON o.CustomerId = c.CustomerId;
```

#### With Cloud Functions
- Use Spanner client libraries
- Connection pooling in global scope
- Keep functions warm to avoid cold starts

#### With GKE
- Use Workload Identity for authentication
- Connection pooling at application level
- Deploy Spanner client close to Spanner region

### Well-Architected Considerations
- **Operational Excellence**:
  - Automated backups and PITR
  - Online schema changes
  - Query insights for performance monitoring
- **Reliability**:
  - Multi-region for 99.999% SLA
  - Automatic replication and failover
  - Regular backup and restore testing
- **Security**:
  - VPC Service Controls
  - CMEK encryption
  - Fine-grained IAM roles
  - Audit logging
- **Performance**:
  - Proper primary key design
  - Interleaved tables for locality
  - Stale reads for non-critical queries
  - Query optimization with indexes
- **Cost**:
  - Right-size PUs based on CPU
  - Regional vs multi-region trade-off
  - Autoscaling for variable workloads
  - Stale reads to reduce costs
- **Sustainability**:
  - Efficient schema design
  - Right-sizing compute resources
