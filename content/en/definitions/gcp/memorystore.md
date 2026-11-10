---
title: Memorystore
category: GCP
description: 'GCP note: Memorystore.'
tags:
- gcp
- databases
---

<!-- imported from ObsidianVault/studies/cloud-architecht/gcp/databases/memorystore.md. Edit the source, then run sync.py. -->

# Memorystore

`gcp` `databases`

## Memorystore
**AWS Equivalent:** Amazon ElastiCache
**Fully managed** in-memory data store for Redis and Memcached

### Overview
- High-performance caching and session store
- Sub-millisecond latency
- Two engines: **Redis** and **Memcached**
- **No persistence with Memcached** (ephemeral)
- **Persistence with Redis** (Standard tier)

### Memorystore for Redis
#### Tiers
**Basic Tier**
- Single Redis instance
- No replication
- **No SLA**
- Lower cost
- Use for: Dev/test, cache-only workloads

**Standard Tier**
- Automatic failover replica in separate zone
- **99.9% SLA**
- Cross-zone replication
- Use for: Production, HA required

#### Features
- **Persistence**: RDB snapshots, AOF logs
- **High availability**: Automatic failover (Standard tier)
- **Scaling**: Vertical scaling (change memory size)
- **Import/Export**: From/to Cloud Storage
- **Versions**: Redis 4.0, 5.0, 6.x, 7.x

#### Use Cases
✓ Low-latency access WITH persistence
✓ Gaming leaderboards
✓ Session store with HA requirements
✓ Real-time analytics
✓ Pub/Sub messaging
✓ Sorted sets, lists, hashes

### Memorystore for Memcached
#### Features
- Pure caching (no persistence)
- **Multi-node clusters** (1-20 nodes)
- Automatic node discovery
- **Data lost on node failure** (ephemeral)
- Lower cost than Redis

#### Use Cases
✓ Pure caching (no persistence needed)
✓ Session store (short-lived)
✓ Database query caching
✓ Reference data (states, countries, config)
✓ Object caching

### Redis vs Memcached
| Feature | Redis | Memcached |
|---------|-------|-----------|
| Persistence | ✓ (Standard tier) | ✗ |
| Replication | ✓ (Standard tier) | ✗ |
| HA/Failover | ✓ (Standard tier) | ✗ (use multiple nodes) |
| Data structures | Rich (lists, sets, sorted sets) | Simple (key-value) |
| Use case | Persistent cache, HA | Ephemeral cache, session store |
| Cost | Higher | Lower |

### Integration
- [[gcp/compute-engine|Compute Engine]]
- [[app-engine|App Engine]] (Standard & Flexible)
- [[gcp/gke|GKE]]
- [[gcp/cloud-functions|Cloud Functions]]
- Must be in same [[gcp/vpc|VPC]] region

### Networking
- **Private IP only** (within VPC)
- **Serverless VPC Access** required for Cloud Functions, App Engine, Cloud Run
- VPC Peering supported
- No public IP option

### Security
- **VPC**: Private network access only
- **IAM**: Control who can manage instances
- **Auth**: Redis AUTH supported
- **Transit encryption**: TLS/SSL (Redis)
- **Encryption at rest**: Automatic

### Pricing
**Redis:**
- Basic: ~$0.05 per GB-hour
- Standard: ~$0.08 per GB-hour (includes replica)
- Network egress charges

**Memcached:**
- ~$0.025 per GB-hour (cheaper than Redis)
- Per-node pricing

---

## ACE Level

### Essential Commands
```bash
# Create Redis instance (Basic tier)
gcloud redis instances create my-redis \
  --size=1 \
  --region=us-central1 \
  --tier=basic

# Create Redis instance (Standard tier with HA)
gcloud redis instances create my-redis-ha \
  --size=5 \
  --region=us-central1 \
  --tier=standard \
  --redis-version=redis_6_x

# List instances
gcloud redis instances list --region=us-central1

# Describe instance
gcloud redis instances describe my-redis --region=us-central1

# Delete instance
gcloud redis instances delete my-redis --region=us-central1

# Create Memcached instance
gcloud memcache instances create my-memcache \
  --node-count=3 \
  --node-cpu=1 \
  --node-memory=1GB \
  --region=us-central1

# List Memcached instances
gcloud memcache instances list --region=us-central1
```

### Connecting from Applications
```python
# Python example (Redis)
import redis

# Get connection info from Memorystore
redis_host = 'REDIS_IP'
redis_port = 6379

# Connect
client = redis.Redis(host=redis_host, port=redis_port)

# Set/Get
client.set('key', 'value')
value = client.get('key')
```

### Key Concepts for ACE
- Understanding Redis vs Memcached differences
- Creating instances (Basic vs Standard tier)
- Understanding VPC networking requirements
- Connecting from Compute Engine, App Engine, GKE
- Basic Redis operations
- Understanding ephemeral nature of Memcached

---

## PCA Level

### Architectural Patterns
#### Web Application Caching
```
User → Load Balancer → Compute Engine/GKE
                     → Check Memorystore (cache hit = fast)
                     → Cloud SQL (cache miss = slower)
                     → Write to Memorystore for next request
```

#### Session Store
```
User Login → App Engine → Memorystore (session data)
                       → Share sessions across instances
                       → Fast session lookup
```

#### Database Query Caching
```
Application → Memorystore (check cache)
           → Cache hit: Return cached result
           → Cache miss: Query Cloud SQL → Cache result → Return
```

### High Availability Design
#### Redis Standard Tier
- Automatic failover to replica
- **Cross-zone replication** within region
- RTO: ~1 minute
- RPO: Minimal (replication is synchronous)

#### Memcached HA
- **Deploy multiple nodes** (3+ recommended)
- Client-side consistent hashing
- Node failure: Only that node's cache lost
- Application must handle cache misses

### Performance Optimization
- **Right-size memory**: Monitor eviction rate
- **Connection pooling**: Reuse connections
- **Pipelining**: Batch multiple commands (Redis)
- **TTL strategy**: Set appropriate expiration
- **Read replicas**: Standard tier for read-heavy workloads

### Cost Optimization
- **Memcached** for pure caching (cheaper)
- **Redis Basic** for dev/test
- **Redis Standard** only when HA needed
- Right-size instances (monitor memory usage)
- Use Committed Use Discounts

### Security Best Practices
- **Private IP only** (no internet exposure)
- VPC firewall rules
- [[gcp/vpc|VPC Service Controls]] for data protection
- Redis AUTH for authentication
- TLS/SSL for transit encryption
- IAM roles:
  - `redis.admin`: Full access
  - `redis.editor`: Manage instances
  - `redis.viewer`: Read-only

### Caching Strategies
#### Cache-Aside (Lazy Loading)
```
1. Check cache
2. If miss: Query database
3. Write to cache
4. Return result
```
- Most common pattern
- Cache populated on-demand

#### Write-Through
```
1. Write to database
2. Write to cache simultaneously
3. Return success
```
- Cache always fresh
- Higher write latency

#### Write-Behind (Write-Back)
```
1. Write to cache
2. Asynchronously write to database
3. Return success immediately
```
- Fastest writes
- Risk of data loss if cache fails

### Integration Patterns
#### With Cloud Functions
```python
# Requires Serverless VPC Access connector
from google.cloud import redis_v1

# Use VPC connector to access Memorystore
connector = 'projects/PROJECT/locations/REGION/connectors/CONNECTOR'
```

#### With GKE
```yaml
# Use private IP from within cluster
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-config
data:
  redis_host: "10.0.0.3"  # Memorystore private IP
  redis_port: "6379"
```

### Monitoring & Alerts
- **[[cloud-monitoring|Cloud Monitoring]] metrics**:
  - CPU utilization
  - Memory usage
  - Evicted keys (cache full indicator)
  - Hit ratio (effectiveness)
  - Connected clients
  - Network throughput
- **Alerts**:
  - Memory usage > 80%
  - Eviction rate spike
  - High CPU (Redis commands expensive)

### Migration Strategies
#### From ElastiCache to Memorystore
- Export Redis data to S3
- Transfer to Cloud Storage
- Import to Memorystore
- Update application connection strings
- Test failover behavior

#### From Self-Managed Redis
- Use Redis MIGRATE command
- Or: RDB snapshot → Cloud Storage → Memorystore import
- Minimal downtime with replication

### Use Case Selection
| Requirement | Choose |
|-------------|--------|
| Simple key-value cache | Memcached |
| Persistence required | Redis Standard |
| HA required | Redis Standard |
| Complex data structures | Redis |
| Lowest cost | Memcached |
| Session store (ephemeral OK) | Memcached |
| Session store (HA needed) | Redis Standard |
| Gaming leaderboard | Redis (sorted sets) |
| Pub/Sub messaging | Redis |

### Well-Architected Considerations
- **Operational Excellence**: Fully managed, automatic updates, monitoring
- **Reliability**: Redis Standard for HA, multi-node Memcached, automatic failover
- **Security**: VPC-only, AUTH, TLS, VPC SC, IAM
- **Performance**: Sub-millisecond latency, connection pooling, right-sizing
- **Cost**: Memcached cheaper, right-size instances, committed use discounts
- **Sustainability**: Efficient caching reduces database load, energy-efficient infrastructure
