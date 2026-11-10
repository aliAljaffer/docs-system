# 7. Databases: Relational, NoSQL, Cache, and Analytics

**Goal:** Match a workload to the right database service.

| Service | Type | Choose it for |
|---|---|---|
| RDS | Managed SQL database | Standard SQL engines with managed operations |
| Aurora | Cloud-optimized SQL (MySQL and PostgreSQL compatible) | Higher performance and availability than RDS |
| ElastiCache | In-memory cache | Fast reads and less load on a database |
| DynamoDB | NoSQL | Single-digit millisecond latency at high scale |

## Amazon RDS

RDS is a managed SQL database service. Supported engines: PostgreSQL, MySQL, MariaDB, Oracle, Microsoft SQL Server, IBM DB2, and Aurora.

### What AWS manages

- Provisioning and OS patching
- Continuous backups and restores
- Monitoring dashboards
- Maintenance windows
- Vertical and horizontal scaling

You cannot SSH into an RDS instance, except with RDS Custom.

### Storage autoscaling

Set a maximum storage threshold. RDS adds storage when all three conditions are true:

1. Free storage is below 10% of allocated storage.
2. The low-storage condition lasts at least 5 minutes.
3. At least 6 hours have passed since the last storage change.

Storage autoscaling suits unpredictable workloads. It supports all RDS engines.

### Read replicas

!!! warning "Read replicas are read only"
    Read replicas serve `SELECT` queries only. Send `INSERT`, `UPDATE`, and `DELETE` to the primary database.

- Create up to 15 read replicas.
- Replicas can run in the same AZ, in another AZ, or in another Region.
- Replication is asynchronous. Reads can be eventually consistent.
- The application must update its connection string to use a replica.
- Use case: give an analytics team a replica, so the production database stays fast.
- Traffic within a Region is free. Cross-Region traffic costs money.

### Multi-AZ

- Multi-AZ is for [[disaster-recovery|disaster recovery]]. It uses synchronous replication to a standby. Every change on the primary also applies to the standby.
- You get one DNS name, so the application needs no change at failover.
- Multi-AZ is not used for scaling.
- Read replicas can run as Multi-AZ.
- To convert a Single-AZ database to Multi-AZ, select Modify. The change has zero downtime. AWS takes a snapshot, restores it to a new database, and synchronizes the two.

### Backups

- Automated backups: a daily full backup and transaction logs every 5 minutes. Retention: 1 to 35 days. Set 0 to disable.
- The newest automated backup can be 5 minutes old.
- Manual snapshots: you start them. Keep them as long as you need.
- A stopped database still pays for storage. For a long stop, take a snapshot and restore it later.

### RDS Custom

RDS Custom supports Oracle and Microsoft SQL Server with access to the underlying OS and database. You can SSH into it. Turn off automation mode before you customize it.

### RDS Proxy

- Pools and shares database connections.
- Reduces stress on the database and the number of open connections.
- Is [[serverless|serverless]], autoscaling, and highly available (Multi-AZ).
- Reduces failover time by up to 66%.
- Most apps need no code change.
- Enforces [[security-iam|IAM]] authentication. Stores credentials in Secrets Manager.
- Is never publicly accessible. Access it from a [[networking-vpc|VPC]].

## Amazon Aurora

- Aurora supports PostgreSQL and MySQL. The course note says it performs 5x MySQL on RDS and 3x PostgreSQL on RDS.
- Aurora costs 20% more than RDS. The note says it is more efficient.
- Storage grows in 10 GB steps, up to 128 TB.
- Up to 15 replicas. Replica lag is under 10 milliseconds.

### High availability and reads

- Aurora stores 6 copies of data across 3 AZs.
- Writes need 4 of 6 copies. Reads need 3 of 6.
- Storage heals itself with peer-to-peer replication.
- One instance accepts writes (the primary). Failover takes under 30 seconds.
- Up to 15 Aurora replicas serve reads.

### Endpoints

- The writer endpoint points to the primary instance.
- The reader endpoint balances connections across replicas.
- A custom endpoint points to instances you choose, such as larger instances for analytics. If a custom endpoint exists, the reader endpoint is not used.

### Global Aurora

- Cross-Region read replicas are simple to set up and useful for disaster recovery.
- Aurora Global Database is the recommended option:
  - One primary Region (reads and writes)
  - Up to 5 secondary Regions (reads only), with replication lag under 1 second
  - Up to 16 read replicas per secondary Region
  - Promoting a secondary Region for disaster recovery takes under 1 minute ([[rto|RTO]]).

### Serverless, ML, backups, and cloning

- Aurora Serverless scales capacity with usage. It suits infrequent, intermittent, or unpredictable workloads. It needs no capacity planning. You pay per second.
- Aurora Machine Learning adds predictions to SQL queries. It uses [[machine-learning-sagemaker|SageMaker]] and [[machine-learning-comprehend|Comprehend]]. Use cases: fraud detection, ad targeting, sentiment analysis, and recommendations.
- Automated backups keep 1 to 35 days. You cannot disable them. Point-in-time recovery works within that window.
- Backtrack restores data to a point in time without using backups.
- Restoring a backup or snapshot creates a new database.
- Cloning creates a new cluster from an existing one. It uses copy-on-write, so it is faster than snapshot restore. It suits staging databases.

## Amazon ElastiCache

ElastiCache is an in-memory cache. It reduces load on RDS. It needs heavy application code changes.

| | Redis | Memcached |
|---|---|---|
| [[high-availability|High availability]] | Multi-AZ with auto-failover, plus read replicas | Not highly available |
| Scaling | Read replicas | Multi-node partitioning (sharding) |
| Persistence | AOF persistence | Non-persistent |
| Authentication | IAM authentication, AUTH token, and SSL | SASL |

- Redis supports sets and sorted sets. Sorted sets suit gaming leaderboards, because each new element is ranked in real time.
- Memcached is multi-threaded.
- Memcached Auto Discovery finds all nodes in a cluster. Failed nodes are detected and replaced.

### Loading patterns

| Pattern | How it works | Trade-off |
|---|---|---|
| Lazy loading | Caches data when it is read | Cached data can become stale |
| Write-through | Writes to the cache when data is written to the database | No stale data |
| Session store | Stores temporary session data with a time-to-live (TTL) | Expires data automatically |

## Amazon DynamoDB

- NoSQL, fully managed, and highly available across AZs.
- Scales to millions of requests per second. Single-digit millisecond latency.
- Integrates with IAM.
- Maximum item (row) size: 400 KB.

| Capacity mode | How it works | Cost |
|---|---|---|
| Provisioned (default) | You set read and write capacity per second. Autoscaling is optional. | Pay for RCUs and WCUs |
| On-demand | Scales with the workload. No planning. | Pay per use. The note calls it expensive. |

- DAX is a managed in-memory cache. It reduces read congestion. Cached reads take microseconds.
- DynamoDB Streams capture item changes. Enable them before you create global tables.
- Global tables give low-latency access in several Regions.
- TTL expires items automatically. Use case: web session handling.
- You can export to [[storage-s3|S3]] (enable point-in-time recovery first). You can import CSV, DynamoDB JSON, or Amazon Ion.

## Other database services

| Service | Type | Notes |
|---|---|---|
| DocumentDB | MongoDB-compatible | Deploys like Aurora |
| Neptune | Graph | Stores billions of relationships. Millisecond queries. Replicates across 3 AZs, with up to 15 read replicas. Good for knowledge graphs. |
| Keyspaces | Apache Cassandra | Replicates 3 times across AZs. Provisioned or on-demand. |
| QLDB | Ledger of financial transactions | Immutable history. Has a central authority. |
| Managed Blockchain | Decentralized ledger | No central authority |
| Timestream | Time series | Serverless, autoscaling, built-in analytics, encrypted. Suits IoT and operational data. |

## Analytics: Athena and Redshift

| | [[analytics-athena|Athena]] | [[analytics-redshift|Redshift]] |
|---|---|---|
| Model | Serverless SQL on data in S3 | Data warehouse |
| Best for | Ad hoc queries, log analysis, [[management-and-governance-cloudtrail|CloudTrail]] logs | Joins and aggregations |
| Cost | $5 per TB scanned | Not in the note |

- Athena: store data in columnar formats (Apache Parquet or ORC) and compress it. Athena then scans less data. [[machine-learning-glue|Glue]] can convert data to Parquet.
- Athena federated queries run SQL against other sources through data source connectors on [[compute-lambda|Lambda]].
- Redshift is a columnar data warehouse for OLAP. It is not for OLTP. It runs provisioned or serverless clusters, and it integrates with QuickSight and Tableau.
- Redshift Spectrum queries data in S3 without loading it. It needs a Redshift cluster.
- Redshift snapshots can be automatic or manual. You can copy them to another Region. Some clusters run Multi-AZ.
- Load Redshift in large batches.

## Exam tips

- RDS read replicas serve `SELECT` only. Multi-AZ is for failover, not scaling.
- Aurora supports up to 15 replicas. Aurora Global Database promotes a secondary Region in under 1 minute.
- ElastiCache needs code changes. Choose Redis for high availability and persistence. Choose Memcached for sharding, with no high availability.
- Lazy loading can serve stale data. Write-through does not.
- DynamoDB items can be at most 400 KB.
- QLDB has a central authority. Managed Blockchain is decentralized.
- Athena runs ad hoc SQL on S3. Redshift handles warehouse joins and aggregations.
- Send analytics to a read replica, not the production primary.

[Next: Decoupling and Integration](08-decoupling-and-integration.md)
