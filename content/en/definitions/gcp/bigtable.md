---
title: Bigtable
category: GCP
description: 'GCP note: Bigtable.'
tags:
- gcp
- databases
---


# Bigtable

`gcp` `databases`

## Cloud Bigtable
**AWS Equivalent:** DynamoDB (NoSQL), Keyspaces (Cassandra-compatible)
**Fully managed, scalable NoSQL wide-column database** for massive workloads

### Key Characteristics
- **Petabyte-scale** with sub-10ms latency
- **Wide-column NoSQL** (based on original Google Bigtable paper)
- **High throughput**: Millions of QPS
- **No-downtime cluster resizing**
- **HBase API compatible** (easy migration from Hadoop)
- **Low latency** for both reads and writes
- **Fully managed** (no server maintenance)
- **Linear scalability** by adding nodes

### Bigtable vs DynamoDB
| Feature | Cloud Bigtable | AWS DynamoDB |
|---------|----------------|--------------|
| Data Model | Wide-column | Key-value, Document |
| API | HBase, Native | AWS SDK, PartiQL |
| Pricing | Per node + storage | Per RCU/WCU or on-demand |
| Minimum Cost | ~$390/month (1 node) | Pay per request (can be $0) |
| Scaling | Add nodes (manual/auto) | Auto-scale or on-demand |
| Latency | Sub-10ms | Single-digit ms |
| Best For | High throughput, analytics | Serverless, variable workload |
| Global Tables | Replication available | Native global tables |

**When to choose Bigtable over DynamoDB:**
- Need HBase compatibility
- Consistent high throughput (millions QPS)
- Analytical workloads with Dataflow/Hadoop integration
- Time-series or IoT data with high write rates

### Data Model
#### Structure
- **Instance**: Container for clusters
- **Cluster**: Set of nodes in specific zone
- **Table**: Contains column families
- **Row**: Identified by unique row key (byte string)
- **Column Family**: Group of columns
- **Column Qualifier**: Individual column within family
- **Cell**: Intersection of row and column, can have multiple timestamped versions

#### Row Key Design (Critical!)
```text
Row Key: user#timestamp#device
Column Families: cf1
Columns: cf1:temperature, cf1:humidity, cf1:pressure
```

**Row Key Best Practices:**
- **Most important design decision**
- Determines data distribution and query performance
- **Avoid monotonically increasing keys** (hotspots)
- Use reverse domain names, hash prefixes, field promotion
- Design based on query patterns

**Anti-patterns:**
- Sequential timestamp as row key (all writes to one node)
- User IDs if users created sequentially
- Auto-incrementing values

**Good patterns:**
- `hash(user_id)#user_id` - Distributes users
- `reverse_timestamp#device_id` - Recent data first
- `bucket#timestamp` - Sharded time series
- `device_id#reverse_timestamp` - Device-specific queries

### Instance Types
#### Production Instance
- **Minimum 3 nodes** for SLA
- **99.9% SLA** for single-cluster
- **99.99% SLA** for multi-cluster (2+ clusters in different zones)
- Suitable for production workloads
- Supports replication

#### Development Instance
- **Single-node cluster**
- **No SLA**
- **No replication**
- **Up to 75% cheaper** than production
- Use for testing and development only
- **Cannot upgrade to production** (must recreate)

### Storage Types
#### SSD Storage (Default)
- Low latency (<10ms)
- High throughput
- **Recommended for most workloads**
- $0.17 per GB/month

#### HDD Storage
- Higher latency (200ms typical)
- **Lower cost** ($0.026 per GB/month)
- Good for batch workloads, cold data
- **Minimum 10 TB storage** required
- Use cases: Archival, infrequent access, batch analytics

### Replication
#### Multi-Cluster Replication
- **Eventual consistency** across clusters
- Automatic routing to nearest cluster
- Automatic failover to another cluster
- **Replication profiles**:
  - **Single-cluster**: No replication
  - **Multi-cluster**: Replicate to all clusters (default)
  - **Single-cluster routing**: Send requests to specific cluster

#### Use Cases for Replication
- **High availability**: Failover across zones/regions
- **Low latency**: Read from nearest cluster
- **Disaster recovery**: Geographic redundancy
- **Workload isolation**: Separate batch from real-time traffic

### Column Families
- Container for columns
- **Configure garbage collection policies per family**
- **Set at table creation, can modify later**
- Keep number of families small (<100, ideally <10)

#### Garbage Collection Policies
```bash
# Max number of versions
cbt createfamily table-id cf1 maxversions=3

# Max age
cbt createfamily table-id cf1 maxage=7d

# Combined
cbt createfamily table-id cf1 maxversions=3 maxage=7d
```

### Performance and Scalability
#### Scaling
- **Add/remove nodes without downtime**
- Each node: ~10,000 QPS (reads or writes)
- Storage: 8 TB per SSD node, 16 TB per HDD node
- **Linear scalability** (2x nodes = 2x throughput)

#### Autoscaling
- Based on CPU or storage utilization
- Configure min/max nodes and target CPU
- Recommended for variable workloads
- Cooldown period to prevent thrashing

#### Performance Factors
- **Node count**: More nodes = more throughput
- **Row key design**: Even distribution prevents hotspots
- **Number of rows read**: Fewer rows = faster queries
- **Request size**: Larger requests may reduce QPS
- **Column families**: More families = more overhead

### Access Patterns
#### Point Reads
```python
# Read single row
row = table.read_row(row_key)
```

#### Range Scans
```python
# Read rows with prefix
rows = table.read_rows(row_set=RowSet.from_rows_or_ranges(
    RowRange(start_key=b"user#", end_key=b"user#~")
))
```

#### Filters
```python
# Read with filter
row_filter = RowFilterChain([
    FamilyNameRegexFilter("cf1"),
    ColumnQualifierRegexFilter("temp.*"),
    TimestampRangeFilter(TimestampRange(start=timestamp))
])
```

### Integration with GCP Services
#### Cloud Dataflow
- Read/write Bigtable at scale
- ETL pipelines
- Batch and streaming

#### Cloud Dataproc (Hadoop/Spark)
- HBase API compatibility
- Run existing HBase workloads
- Migrate from HBase to Bigtable

#### BigQuery
- Export Bigtable data for analytics
- Not direct integration (use Dataflow)

#### Cloud Functions
- Lightweight data access
- Event-driven processing
- Use connection pooling

### Backups
- **On-demand backups**: Manual, retained until deleted
- **Scheduled backups**: Not available (use external tools)
- Backups stored in same instance
- Restore creates new table
- **No point-in-time recovery**
- Use for disaster recovery, not archival

### Monitoring and Observability
#### Key Metrics
- **CPU utilization**: Target **<70% for single-cluster**, <90% for multi-cluster
- **Storage utilization**: <70% per node
- **Latency**: P50, P99 read/write latency
- **QPS**: Queries per second
- **Error rate**: Failed requests

#### Key Visualizer
- **Visual tool to analyze row key distribution**
- Identifies hotspots and access patterns
- Shows read/write patterns over time
- Critical for debugging performance issues

### Pricing
#### Nodes
- **SSD node**: $0.65/hour (~$470/month)
- **HDD node**: $0.65/hour (~$470/month)
- **Minimum 1 node for dev, 3 nodes for production SLA**

#### Storage
- **SSD**: $0.17 per GB/month
- **HDD**: $0.026 per GB/month

#### Network
- Standard GCP egress rates
- Replication across regions: Egress charges apply

**Example costs:**
- **Dev instance**: 1 SSD node + 100 GB = ~$487/month
- **Prod instance**: 3 SSD nodes + 1 TB = ~$1,580/month
- **Large instance**: 30 SSD nodes + 100 TB = ~$31,200/month

### Use Cases
- **Time-series data**: IoT, monitoring, financial ticks
- **Marketing data**: User events, clickstreams
- **Financial data**: Stock prices, trading data
- **Graph data**: Social networks, recommendation engines
- **IoT data**: Sensor data, device telemetry
- **AdTech**: User profiles, real-time bidding
- **Personalization**: User preferences, behavior tracking

### When to Use Bigtable
- **High throughput** (>100,000 QPS)
- **Large datasets** (>1 TB)
- **Time-series data** with high write rates
- Need HBase compatibility
- Consistent high load
- Analytical workloads with Hadoop/Spark

### When NOT to Use Bigtable
- Small datasets (<1 TB) → Use [[gcp/firestore|Firestore]] or [[gcp/cloud-sql|Cloud SQL]]
- Transactional workloads → Use [[cloud-spanner|Cloud Spanner]] or [[gcp/cloud-sql|Cloud SQL]]
- Complex SQL queries → Use [[gcp/cloud-sql|Cloud SQL]] or [[bigquery|BigQuery]]
- Serverless/variable workload → Use [[gcp/firestore|Firestore]] (pay per request)
- Document database → Use [[gcp/firestore|Firestore]]
- Low throughput → DynamoDB on-demand more cost-effective

### Migration Strategies
#### From HBase
- HBase API compatible
- Use HBase client libraries
- Migrate data with Dataflow
- Test thoroughly (some HBase features not supported)

#### From Cassandra
- Data model similar (wide-column)
- Rewrite application code (different API)
- Use Dataflow for data migration

#### From DynamoDB
- Data model conversion required
- Use AWS Data Pipeline + Dataflow
- Redesign row keys for Bigtable patterns

---

## ACE Level

### Essential cbt Commands
```bash
# Install cbt CLI
gcloud components install cbt

# Configure .cbtrc
echo project = PROJECT_ID > ~/.cbtrc
echo instance = INSTANCE_ID >> ~/.cbtrc

# List instances
cbt listinstances

# Create table
cbt createtable table-id

# List tables
cbt ls

# Create column family
cbt createfamily table-id cf1

# Set garbage collection policy
cbt setgcpolicy table-id cf1 maxversions=3
cbt setgcpolicy table-id cf1 maxage=7d

# Write data
cbt set table-id row-key cf1:column1=value1 cf1:column2=value2

# Read row
cbt read table-id

# Read specific row
cbt lookup table-id row-key

# Read with prefix
cbt read table-id prefix="user#"

# Count rows
cbt count table-id

# Delete row
cbt deleterow table-id row-key

# Delete column
cbt deletecolumn table-id row-key cf1:column1

# Delete table
cbt deletetable table-id
```

### Essential gcloud Commands
```bash
# Create production instance with SSD
gcloud bigtable instances create INSTANCE_ID \
  --display-name="My Instance" \
  --cluster=CLUSTER_ID \
  --cluster-zone=us-central1-a \
  --cluster-num-nodes=3 \
  --cluster-storage-type=SSD

# Create development instance
gcloud bigtable instances create INSTANCE_ID \
  --display-name="Dev Instance" \
  --cluster=CLUSTER_ID \
  --cluster-zone=us-central1-a \
  --instance-type=DEVELOPMENT

# Update nodes (scale)
gcloud bigtable clusters update CLUSTER_ID \
  --instance=INSTANCE_ID \
  --num-nodes=5

# Enable autoscaling
gcloud bigtable clusters update CLUSTER_ID \
  --instance=INSTANCE_ID \
  --autoscaling-min-nodes=3 \
  --autoscaling-max-nodes=10 \
  --autoscaling-cpu-target=70

# Create backup
gcloud bigtable backups create BACKUP_ID \
  --instance=INSTANCE_ID \
  --cluster=CLUSTER_ID \
  --table=TABLE_ID \
  --retention-period=7d

# Restore from backup
gcloud bigtable backups restore BACKUP_ID \
  --instance=INSTANCE_ID \
  --cluster=CLUSTER_ID \
  --new-table=RESTORED_TABLE_ID

# List clusters
gcloud bigtable clusters list --instances=INSTANCE_ID

# Delete instance
gcloud bigtable instances delete INSTANCE_ID
```

### Client Library Example (Python)
```python
from google.cloud import bigtable
from google.cloud.bigtable import column_family

# Create client
client = bigtable.Client(project=PROJECT_ID, admin=True)
instance = client.instance(INSTANCE_ID)

# Create table
table = instance.table(TABLE_ID)
cf1 = table.column_family("cf1")
cf1.max_versions_gc_rule(3)
table.create()

# Write data
row = table.direct_row("user#12345")
row.set_cell("cf1", "username", "alice")
row.set_cell("cf1", "email", "alice@example.com")
row.commit()

# Read data
row_key = "user#12345"
row = table.read_row(row_key)
for cf, col, value in row.cells["cf1"].items():
    print(f"{cf}:{col} = {value}")

# Scan with prefix
rows = table.read_rows(row_set=RowSet.from_rows_or_ranges(
    RowRange(start_key=b"user#", end_key=b"user#~")
))
for row in rows:
    print(row.row_key)
```

### Key Concepts for ACE
- Creating and managing Bigtable instances
- Understanding production vs development instances
- Creating tables and column families
- Setting garbage collection policies
- Basic cbt CLI operations
- Writing and reading data
- Understanding row keys and column families
- Monitoring instance metrics (CPU, storage)
- Scaling clusters (adding nodes)

---

## PCA Level

### Row Key Design Patterns
#### Pattern 1: Salting/Hashing
```text
Bad:  timestamp#user_id  (hotspot on recent time)
Good: hash(user_id)#timestamp#user_id  (distributed)
```

#### Pattern 2: Field Promotion
```text
Bad:  user_id  (column: timestamp)
Good: user_id#timestamp  (timestamp in row key for time-range queries)
```

#### Pattern 3: Reverse Timestamp
```python
# For time-series where recent data accessed most
import sys
reverse_timestamp = sys.maxsize - int(time.time() * 1000)
row_key = f"device#{device_id}#{reverse_timestamp}"
```

#### Pattern 4: Bucketing
```python
# Distribute time-series writes
bucket = hash(device_id) % NUM_BUCKETS
row_key = f"{bucket:03d}#{device_id}#{timestamp}"
```

### Schema Design Best Practices
#### Tall and Narrow (Preferred)
```text
Row Key: user#12345#event#2024-01-01-12:00:00
cf:type = "click"
cf:page = "/products"
cf:duration = "5000"

Row Key: user#12345#event#2024-01-01-12:01:00
cf:type = "purchase"
cf:product = "item-123"
cf:price = "29.99"
```
- More rows, fewer columns
- Better distribution
- Better for time-series

#### Short and Wide (Use Sparingly)
```text
Row Key: user#12345
cf:event:2024-01-01-12:00:00:type = "click"
cf:event:2024-01-01-12:00:00:page = "/products"
cf:event:2024-01-01-12:01:00:type = "purchase"
```
- Fewer rows, many columns
- Can cause hotspots
- Limit on cell versions

### Performance Optimization
#### Monitoring and Tuning
```text
Key Metrics:
- CPU utilization: Target <70% (single-cluster), <90% (multi-cluster)
- Storage per node: <70% of limit
- Latency P99: <10ms for well-designed schema
- Error rate: <0.1%
```

**Key Visualizer Analysis:**
- Look for hotspots (red areas)
- Ensure even distribution (blue/green)
- Identify access patterns
- Optimize row keys based on visualization

#### Client-Side Optimization
- **Connection pooling**: Reuse connections
- **Batch mutations**: Group writes (up to 100,000 per batch)
- **Async operations**: Non-blocking I/O
- **Retry logic**: Exponential backoff for transient errors
- **Request rate limiting**: Avoid overwhelming cluster

### High Availability Architecture
```text
[Application - Global Load Balancer]
       |                    |
[Bigtable Cluster     Bigtable Cluster
 us-central1]         europe-west1]
       |                    |
[Multi-cluster Replication - Eventual Consistency]
```

**Configuration:**
- 2+ clusters in different regions
- Automatic routing to nearest cluster
- Automatic failover on cluster failure
- 99.99% SLA with multi-cluster

### Backup and Disaster Recovery Strategy
#### Backup Best Practices
- Create backups before schema changes
- Schedule backups via Cloud Scheduler + Cloud Functions
- Test restore procedures regularly
- Monitor backup age and size
- Consider cross-instance backups for DR

#### Disaster Recovery Scenarios
1. **Table corruption**: Restore from recent backup
2. **Cluster failure**: Multi-cluster routing (automatic)
3. **Region failure**: Manual failover to backup region
4. **Accidental deletion**: Restore from backup (no PITR)

### Cost Optimization Strategies
#### Right-Sizing Nodes
```text
Current: 10 nodes, 30% CPU average
Action: Reduce to 5 nodes (target 60% CPU)
Savings: ~$2,350/month
```

#### Autoscaling Configuration
```bash
# Set autoscaling with appropriate targets
gcloud bigtable clusters update CLUSTER_ID \
  --autoscaling-min-nodes=3 \
  --autoscaling-max-nodes=10 \
  --autoscaling-cpu-target=70
```

#### Storage Optimization
- Use HDD for cold data (75% storage savings)
- Set aggressive garbage collection policies
- Archive old data to [[gcp/cloud-storage|Cloud Storage]]
- Monitor storage growth trends

#### Development Instances
- Use dev instances for testing (<75% cost)
- Tear down when not in use
- Cannot upgrade to production (plan accordingly)

### Multi-Tenancy Patterns
#### Row Key Prefix (Recommended)
```text
Row Key: tenant_id#user_id#timestamp
- Efficient range scans per tenant
- Good distribution if tenants balanced
```

#### Separate Tables
```text
Tables: tenant1_data, tenant2_data
- Full isolation
- More operational overhead
- Better for large tenants
```

#### Separate Instances
```text
Instances: tenant1_instance, tenant2_instance
- Complete isolation
- Highest cost
- For regulated industries
```

### Integration Patterns
#### Real-Time Analytics Pipeline
```text
[IoT Devices] → [Pub/Sub] → [Dataflow] → [Bigtable]
                                              ↓
                              [Scheduled Export to BigQuery]
```

#### Serving Layer for ML
```text
[ML Training - BigQuery/Vertex AI]
              ↓
[Export Feature Store to Bigtable]
              ↓
[Real-time Prediction - Read from Bigtable]
```

#### Hybrid OLTP/OLAP
```text
[Application Writes] → [Bigtable] ← [Real-time Reads]
                            ↓
                    [Export to BigQuery]
                            ↓
                    [OLAP Queries/BI Tools]
```

### Security Best Practices
- **IAM roles**:
  - `roles/bigtable.user`: Read/write data
  - `roles/bigtable.reader`: Read-only
  - `roles/bigtable.admin`: Full control
- **VPC Service Controls**: Prevent data exfiltration
- **CMEK**: Customer-managed encryption keys
- **Audit logging**: Track all operations
- **Private Google Access**: No internet exposure
- **Application-level encryption**: For sensitive columns

### Capacity Planning
#### Storage Planning
```text
Calculation:
- Expected row count: 10 billion
- Avg row size: 1 KB
- Total storage: 10 TB
- Replication factor: 2 (multi-cluster)
- Total storage needed: 20 TB

SSD cost: 20,000 GB × $0.17/month = $3,400/month
HDD cost: 20,000 GB × $0.026/month = $520/month
```

#### Node Planning
```text
Calculation:
- Expected QPS: 500,000
- Per node capacity: 10,000 QPS
- Required nodes: 50
- Add 30% headroom: 65 nodes

Cost: 65 nodes × $470/month = $30,550/month
```

### Advanced Use Cases
#### Time-Series at Scale
```python
# Schema design for IoT sensor data
# Row key: sensor_id#reverse_timestamp
# Efficient for: "Latest readings for sensor X"

reverse_ts = sys.maxsize - int(time.time() * 1000)
row_key = f"{sensor_id}#{reverse_ts:020d}"

# Write
row = table.direct_row(row_key)
row.set_cell("metrics", "temperature", str(temp))
row.set_cell("metrics", "humidity", str(humidity))
row.commit()

# Read latest 100 readings
rows = table.read_rows(
    start_key=f"{sensor_id}#",
    end_key=f"{sensor_id}#~",
    limit=100
)
```

#### Graph Data
```text
# User relationships
Row Key: user#12345#follows
cf:users = {user#67890: timestamp, user#11111: timestamp}

# Efficient for: "Who does user X follow?"
# Less efficient for: "Who follows user X?" (requires index table)
```

### Migration Best Practices
#### Pre-Migration
- Analyze existing data model and access patterns
- Design optimal row key for Bigtable
- Create test instance and validate
- Plan for data volume and throughput
- Estimate costs

#### Migration Execution
- Use Dataflow for large-scale migration
- Implement dual-write during transition
- Validate data integrity
- Monitor performance
- Gradual cutover of read traffic

### Well-Architected Considerations
- **Operational Excellence**:
  - Automated backups via Cloud Scheduler
  - Monitoring with Cloud Monitoring
  - Key Visualizer for performance analysis
- **Reliability**:
  - Multi-cluster replication for HA
  - Automated failover
  - Regular backup testing
- **Security**:
  - VPC Service Controls
  - CMEK encryption
  - Least privilege IAM
- **Performance**:
  - Proper row key design (most critical)
  - Sufficient nodes for throughput
  - Efficient client libraries
- **Cost**:
  - Autoscaling for variable loads
  - HDD for cold data
  - Right-sizing nodes
- **Sustainability**:
  - Efficient row key distribution
  - Appropriate garbage collection
  - Right-sized clusters
