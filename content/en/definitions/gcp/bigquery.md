---
title: bigquery
category: GCP
description: 'GCP note: Bigquery.'
tags:
- gcp
- databases
---


# bigquery

## BigQuery
**Serverless, petabyte-scale data warehouse** for analytics and business intelligence

**AWS Equivalent:** [[analytics-redshift|Redshift]]

### Key Characteristics
- **Fully serverless** (no infrastructure management)
- **Petabyte-scale** storage and analytics
- **SQL interface** (Standard SQL, ANSI 2011)
- **Real-time analytics** with streaming inserts
- **Built-in ML** (BigQuery ML)
- **Automatic optimization** and query execution
- **Pay per query** or flat-rate pricing
- **Columnar storage** for fast analytics
- **Separation of compute and storage**

### BigQuery vs Redshift
| Feature | BigQuery | Redshift |
|---------|----------|----------|
| Architecture | Serverless | Cluster-based |
| Scaling | Automatic | Manual resize |
| Pricing | Per TB scanned + storage | Per node hour |
| Setup Time | Instant | Minutes (cluster provision) |
| SQL Dialect | Standard SQL | PostgreSQL-like |
| Minimum Cost | $0 (free tier) | ~$180/month (dc2.large) |
| ML Integration | Native (BQML) | Via SageMaker |
| Real-time Streaming | Native | Via Kinesis |
| Data Lake Query | Yes (external tables) | Redshift Spectrum |

**When to choose BigQuery:**
- **Serverless, zero-ops** preferred
- **Variable workloads** (pay per query)
- Need to query data in place (GCS, Bigtable, etc.)
- Rapid scaling without provisioning
- Built-in ML workflows

### Architecture
#### Separation of Storage and Compute
| Component | Role |
|---|---|
| Dremel | Query execution engine |
| Colossus | Distributed storage |
| Borg | Orchestration (resource management) |
| Jupiter | Network fabric (1 Petabit/sec bisection bandwidth) |

**Can query data without moving it** (federated queries)

### Storage
#### Native Tables
- **Columnar storage** (optimized for analytics)
- **Automatic compression** and encoding
- **Automatic partitioning** options
- **Automatic clustering** options
- Storage cost: $0.02 per GB/month (active), $0.01 per GB/month (long-term)

#### External Tables
- Query data in [[cloud-storage|Cloud Storage]], [[gcp/bigtable|Bigtable]], [[gcp/cloud-sql|Cloud SQL]]
- No data movement required
- **Lower performance** than native tables
- No storage cost in BigQuery (pay for source storage)
- Use cases: Data lake queries, federated queries

### Table Types
#### Standard Tables
- Regular tables with full DML support
- Best for most use cases

#### Partitioned Tables
**AWS Equivalent:** Redshift partition keys
- **Divide table into segments** based on column value
- **Reduce query costs and improve performance**
- Partition by:
  - **Date/Timestamp** (most common): Daily, hourly, monthly, yearly
  - **Integer range**: Custom ranges
  - **Ingestion time**: `_PARTITIONTIME` pseudo-column

```sql
-- Create partitioned table
CREATE TABLE mydataset.mytable (
  transaction_id INT64,
  transaction_date DATE,
  amount FLOAT64
)
PARTITION BY transaction_date;

-- Query specific partition (cost savings)
SELECT * FROM mydataset.mytable
WHERE transaction_date = '2024-01-01';
```

**Benefits:**
- **Query only relevant partitions** (cost reduction)
- Partition pruning (automatic)
- Easier data lifecycle management

#### Clustered Tables
- **Sort data by clustering columns**
- Up to 4 clustering columns
- **Works with partitioned tables**
- **Automatic re-clustering** (no manual maintenance)

```sql
CREATE TABLE mydataset.mytable (
  customer_id INT64,
  product_id INT64,
  transaction_date DATE,
  amount FLOAT64
)
PARTITION BY transaction_date
CLUSTER BY customer_id, product_id;
```

**Benefits:**
- Faster queries on clustering columns
- Reduced data scanned (cost savings)
- No additional cost

#### Materialized Views
**AWS Equivalent:** Redshift Materialized Views
- **Pre-computed query results**
- **Automatically refreshed** when base table changes
- **Query optimizer uses automatically** (smart tuning)
- Incremental refresh (only changed data)

```sql
CREATE MATERIALIZED VIEW mydataset.daily_sales AS
SELECT
  DATE(order_timestamp) as date,
  product_id,
  SUM(amount) as total_sales
FROM mydataset.orders
GROUP BY date, product_id;
```

### Query Types
| Query type | Behavior | Cost | Use when |
|---|---|---|---|
| Interactive (on-demand) | Standard queries with automatic scaling. 100 concurrent queries per project | Charged per TB scanned | Ad-hoc analysis |
| Batch | Queued queries with lower priority. Can queue thousands of queries | Same as interactive | Results are not needed immediately |
| Scheduled | Run queries on schedule (cron format). Write results to table | **Free** (only pay for query costs) | Data pipelines, reports, dashboards |

### Pricing
#### Storage Pricing
| Item | Price | Condition |
|---|---|---|
| Active storage | $0.02 per GB/month | Tables modified in last 90 days |
| Long-term storage | $0.01 per GB/month | Tables not modified for 90 days (automatic) |
| Streaming inserts | $0.01 per 200 MB | - |

#### Query Pricing (On-Demand)
- **Analysis**: $6.25 per TB scanned (first 1 TB free per month)
- **Streaming inserts**: $0.01 per 200 MB
- **Only charged for data scanned, not returned**
- **Cached queries are free**

#### Flat-Rate Pricing
- Reserve dedicated slots (processing capacity)
- 100 slots = $2,000/month (annual commitment)
- 500 slots = $10,000/month
- **Predictable costs for heavy usage**
- **Use when >$2,000/month on on-demand**

**Cost Optimization Tips:**
- Use partitioned tables
- Use clustered tables
- Select only needed columns (not `SELECT *`)
- Use preview for data exploration
- Cache query results (24 hours)
- Use BI Engine for sub-second queries

### Data Ingestion
#### Batch Loading
- Load from [[cloud-storage|Cloud Storage]] (CSV, JSON, Avro, Parquet, ORC)
- Load from local files (via CLI)
- **Free** (no load cost)
- Formats: CSV, JSON, Avro, Parquet, ORC, Cloud Datastore backup

```bash
# Load CSV from Cloud Storage
bq load --source_format=CSV mydataset.mytable gs://bucket/file.csv schema.json

# Load Parquet (schema auto-detected)
bq load --source_format=PARQUET mydataset.mytable gs://bucket/*.parquet
```

#### Streaming Inserts
**AWS Equivalent:** Kinesis Data Firehose to Redshift
- Real-time data ingestion
- **Available for queries immediately**
- $0.01 per 200 MB
- Use for: Logs, events, sensor data

```python
from google.cloud import bigquery

client = bigquery.Client()
table = client.get_table("project.dataset.table")

rows_to_insert = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
]

errors = client.insert_rows_json(table, rows_to_insert)
```

#### BigQuery Data Transfer Service
- **Automated data loads** from external sources
- Sources: Google Ads, Google Analytics, YouTube, AWS S3, Teradata, Amazon Redshift
- Schedule-based transfers
- Managed by Google (no code required)

#### Dataflow / Dataproc
- For complex ETL pipelines
- Transform data before loading
- Batch or streaming

### Query Optimization
#### Best Practices
```sql
-- GOOD: Select only needed columns
SELECT user_id, amount FROM orders WHERE date = '2024-01-01';

-- BAD: Select all columns
SELECT * FROM orders WHERE date = '2024-01-01';

-- GOOD: Filter partitioned column
SELECT * FROM partitioned_table WHERE date BETWEEN '2024-01-01' AND '2024-01-31';

-- GOOD: Use approximate aggregation for large datasets
SELECT APPROX_COUNT_DISTINCT(user_id) FROM large_table;

-- GOOD: Pre-aggregate with materialized views
CREATE MATERIALIZED VIEW daily_stats AS
SELECT DATE(timestamp) as date, COUNT(*) as count
FROM events
GROUP BY date;
```

#### Query Execution Plan
```sql
-- View execution plan
EXPLAIN SELECT * FROM mydataset.mytable WHERE date = '2024-01-01';
```

Shows:
- Stages and steps
- Data scanned
- Shuffle operations
- Estimated cost

### BigQuery ML (BQML)
**AWS Equivalent:** SageMaker (more complex setup)
- **Train ML models using SQL**
- No need to export data
- Model types: Linear regression, logistic regression, K-means, time series, deep neural networks, XGBoost, AutoML
- **Serverless** (no infrastructure)

```sql
-- Create model
CREATE OR REPLACE MODEL mydataset.churn_model
OPTIONS(model_type='logistic_reg', input_label_cols=['churned']) AS
SELECT
  age,
  total_spend,
  months_active,
  churned
FROM mydataset.customers;

-- Evaluate model
SELECT * FROM ML.EVALUATE(MODEL mydataset.churn_model);

-- Make predictions
SELECT * FROM ML.PREDICT(MODEL mydataset.churn_model,
  (SELECT age, total_spend, months_active FROM mydataset.new_customers)
);
```

### BI Engine
- **In-memory analysis service**
- **Sub-second query response** for dashboards
- Integrates with Looker, Data Studio, Tableau
- Reserve memory capacity (1 GB = $0.04/hour)
- Automatic caching and optimization

### Geographic and Time-Based Features
#### Geographic Functions
```sql
-- Calculate distance between points
SELECT ST_DISTANCE(
  ST_GEOGPOINT(-73.935242, 40.730610),  -- NYC
  ST_GEOGPOINT(-118.243683, 34.052235)  -- LA
) / 1000 as distance_km;

-- Find points within radius
SELECT * FROM locations
WHERE ST_DISTANCE(location, ST_GEOGPOINT(lon, lat)) < 1000;
```

#### Time Travel
- **Query historical data** (up to 7 days)
- No additional cost
- Point-in-time snapshots

```sql
-- Query table as it was 1 hour ago
SELECT * FROM `mydataset.mytable`
FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR);

-- Query deleted table (within 7 days)
SELECT * FROM `mydataset.mytable`
FOR SYSTEM_TIME AS OF '2024-01-15 12:00:00 UTC';
```

### Data Governance
#### Column-Level Security
```sql
-- Create policy tag taxonomy
-- Apply to sensitive columns
-- Control access with IAM
```

#### Row-Level Security
```sql
-- Create row access policy
CREATE ROW ACCESS POLICY sales_filter
ON mydataset.sales
GRANT TO ('user:analyst@example.com')
FILTER USING (region = 'US');
```

#### Data Catalog
- Automatic metadata discovery
- Search across datasets
- Tag and annotate data
- Data lineage tracking

### Federated Queries
**AWS Equivalent:** Redshift Spectrum
- **Query external data sources without moving data**
- Sources: Cloud Storage, Bigtable, Cloud SQL, Sheets
- Use cases: Data lake queries, one-time analysis, cost optimization

```sql
-- Query data in Cloud Storage
SELECT * FROM EXTERNAL_QUERY(
  "us.cloud-sql-instance",
  "SELECT * FROM mysql_table WHERE date > '2024-01-01'"
);

-- Query Cloud Storage (Parquet)
CREATE EXTERNAL TABLE mydataset.external_table
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bucket/data/*.parquet']
);
```

### Monitoring and Optimization
#### Information Schema
```sql
-- View table metadata
SELECT * FROM mydataset.INFORMATION_SCHEMA.TABLES;

-- View column metadata
SELECT * FROM mydataset.INFORMATION_SCHEMA.COLUMNS;

-- View partition metadata
SELECT * FROM mydataset.INFORMATION_SCHEMA.PARTITIONS;
```

#### Query History
```sql
-- Analyze query performance
SELECT
  job_id,
  user_email,
  total_bytes_processed,
  total_slot_ms,
  creation_time
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
ORDER BY total_bytes_processed DESC
LIMIT 10;
```

### Security
**IAM roles:**

| Role | Grants |
|---|---|
| `roles/bigquery.dataViewer` | Read data |
| `roles/bigquery.dataEditor` | Read, write, delete data |
| `roles/bigquery.user` | Run queries |
| `roles/bigquery.admin` | Full control |

- **VPC Service Controls**: Prevent data exfiltration
- **CMEK**: Customer-managed encryption keys via [[gcp/cloud-kms|Cloud KMS]]
- **Authorized views**: Share subset of data without full table access
- **Column-level security**: Restrict sensitive columns
- **Row-level security**: Filter rows based on user
- **Audit logging**: All queries and data access logged

### Use Cases
- **Business intelligence**: Dashboards, reports, ad-hoc analysis
- **Data warehousing**: Centralized analytics repository
- **Log analytics**: Application logs, security logs, audit logs
- **IoT analytics**: Sensor data, telemetry analysis
- **Marketing analytics**: Campaign performance, attribution
- **Fraud detection**: Real-time anomaly detection with BQML
- **Predictive analytics**: Forecasting with BigQuery ML
- **Data lake analytics**: Query data in Cloud Storage

---

## ACE Level

### Essential bq CLI Commands
```bash
# List datasets
bq ls

# List tables in dataset
bq ls mydataset

# Show table schema
bq show mydataset.mytable

# Query (interactive)
bq query --use_legacy_sql=false 'SELECT * FROM mydataset.mytable LIMIT 10'

# Query and save results
bq query --use_legacy_sql=false --destination_table=mydataset.results 'SELECT * FROM mydataset.mytable'

# Load data from Cloud Storage
bq load --source_format=CSV mydataset.mytable gs://bucket/file.csv

# Load with schema auto-detect
bq load --autodetect --source_format=CSV mydataset.mytable gs://bucket/file.csv

# Extract data to Cloud Storage
bq extract mydataset.mytable gs://bucket/output.csv

# Create dataset
bq mk --dataset --location=US mydataset

# Delete dataset
bq rm -r -f mydataset

# Create table
bq mk --table mydataset.mytable schema.json

# Delete table
bq rm -f mydataset.mytable

# Copy table
bq cp mydataset.source_table mydataset.destination_table

# Show query cost estimate
bq query --dry_run --use_legacy_sql=false 'SELECT * FROM mydataset.mytable'
```

### Essential SQL Operations
```sql
-- Create dataset
CREATE SCHEMA IF NOT EXISTS mydataset
OPTIONS(location="us");

-- Create table
CREATE TABLE mydataset.customers (
  customer_id INT64,
  name STRING,
  email STRING,
  created_at TIMESTAMP
);

-- Insert data
INSERT INTO mydataset.customers (customer_id, name, email, created_at)
VALUES (1, 'Alice', 'alice@example.com', CURRENT_TIMESTAMP());

-- Update data
UPDATE mydataset.customers
SET email = 'newemail@example.com'
WHERE customer_id = 1;

-- Delete data
DELETE FROM mydataset.customers
WHERE customer_id = 1;

-- Select with aggregation
SELECT
  DATE(order_date) as date,
  COUNT(*) as order_count,
  SUM(amount) as total_amount
FROM mydataset.orders
WHERE order_date >= '2024-01-01'
GROUP BY date
ORDER BY date DESC;

-- Join tables
SELECT
  c.name,
  o.order_id,
  o.amount
FROM mydataset.customers c
JOIN mydataset.orders o ON c.customer_id = o.customer_id
WHERE o.order_date > '2024-01-01';

-- Window functions
SELECT
  customer_id,
  order_date,
  amount,
  SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date) as running_total
FROM mydataset.orders;
```

### Key Concepts for ACE
- Creating and managing datasets and tables
- Loading data from Cloud Storage
- Writing basic to intermediate SQL queries
- Understanding partitioned and clustered tables
- Estimating query costs with dry-run
- Exporting query results
- Understanding pricing (storage + queries)
- Using the BigQuery console
- Monitoring query history and performance
- Setting up scheduled queries

---

## PCA Level

### Architectural Patterns
#### Lambda Architecture (Batch + Streaming)
```text
[Real-time Events] → [Pub/Sub] → [Dataflow] → [BigQuery Streaming]
                                                       ↓
                                              [Real-time View]

[Batch Data] → [Cloud Storage] → [Dataflow] → [BigQuery Batch Load]
                                                       ↓
                                               [Batch View]

[BigQuery] → [Combine Views] → [Unified Analytics]
```

#### Data Lake Pattern
```text
[Raw Data Sources]
       ↓
[Cloud Storage (Data Lake)]
  - Parquet/Avro files
  - Partitioned by date
       ↓
[BigQuery External Tables] ← [Query in place]
       ↓
[Curated Tables] ← [ETL via Dataflow]
       ↓
[BI Tools / Dashboards]
```

#### Hub and Spoke Pattern
```text
[Source Systems]
  ↓  ↓  ↓
[BigQuery (Central Hub)]
  - Raw layer
  - Staging layer
  - Curated layer
  ↓  ↓  ↓
[Consumers: BI, ML, Apps]
```

### Schema Design Best Practices
#### Denormalization
```sql
-- GOOD: Denormalized for analytics
CREATE TABLE sales_denormalized AS
SELECT
  o.order_id,
  o.order_date,
  o.amount,
  c.customer_name,
  c.customer_email,
  p.product_name,
  p.category
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id;

-- Query is simple and fast
SELECT category, SUM(amount) FROM sales_denormalized GROUP BY category;
```

**Trade-off:** Storage cost vs query performance and simplicity

#### Nested and Repeated Fields
**AWS Redshift doesn't have this**
```sql
-- Use STRUCT for nested data
CREATE TABLE orders (
  order_id INT64,
  customer STRUCT<
    id INT64,
    name STRING,
    email STRING
  >,
  items ARRAY<STRUCT<
    product_id INT64,
    quantity INT64,
    price FLOAT64
  >>
);

-- Query nested fields
SELECT
  order_id,
  customer.name,
  item.product_id,
  item.quantity
FROM orders,
UNNEST(items) as item;
```

**Benefits:**
- Reduce JOINs
- Keep related data together
- More efficient storage

### Partitioning Strategies
#### Date Partitioning (Most Common)
```sql
-- Partition by date column
CREATE TABLE events (
  event_id INT64,
  event_date DATE,
  user_id INT64,
  event_type STRING
)
PARTITION BY event_date;

-- Query single day (cost efficient)
SELECT * FROM events WHERE event_date = '2024-01-01';
-- Scans only 1 partition

-- Query range (still efficient)
SELECT * FROM events
WHERE event_date BETWEEN '2024-01-01' AND '2024-01-31';
-- Scans only 31 partitions
```

#### Ingestion-Time Partitioning
```sql
-- Partition by load time
CREATE TABLE events (
  event_id INT64,
  user_id INT64,
  event_type STRING
)
PARTITION BY _PARTITIONDATE;

-- Query by ingestion date
SELECT * FROM events WHERE _PARTITIONDATE = '2024-01-01';
```

#### Integer Range Partitioning
```sql
-- Partition by customer ID ranges
CREATE TABLE customer_events (
  customer_id INT64,
  event_data STRING
)
PARTITION BY RANGE_BUCKET(customer_id, GENERATE_ARRAY(0, 100000, 1000));
-- Creates 100 partitions (0-999, 1000-1999, etc.)
```

### Clustering Strategies
```sql
-- Partition + Cluster for optimal performance
CREATE TABLE orders (
  order_date DATE,
  customer_id INT64,
  product_id INT64,
  amount FLOAT64
)
PARTITION BY order_date
CLUSTER BY customer_id, product_id;

-- This query is highly optimized (partition pruning + clustering)
SELECT * FROM orders
WHERE order_date = '2024-01-01'
  AND customer_id = 12345;
```

**Clustering Best Practices:**
- Cluster by high-cardinality columns
- Cluster by commonly filtered columns
- Up to 4 clustering columns
- Order matters (most selective first)

### Performance Optimization
#### Query Performance Tuning
```sql
-- BAD: Full table scan
SELECT * FROM large_table WHERE non_partitioned_column = 'value';

-- GOOD: Partition pruning
SELECT * FROM large_table
WHERE partition_column = '2024-01-01'
  AND clustered_column = 'value';

-- BAD: SELECT *
SELECT * FROM large_table LIMIT 10;

-- GOOD: Select only needed columns
SELECT id, name, email FROM large_table LIMIT 10;

-- Use APPROX functions for large datasets
SELECT APPROX_COUNT_DISTINCT(user_id) FROM events;
-- Much faster and cheaper than COUNT(DISTINCT)
```

#### Caching Strategy
- **Query results cached for 24 hours**
- Cached queries are FREE
- Cache invalidated if table changes
- Use cache for repetitive queries
- Set query timeout for expensive queries

```sql
-- Disable cache for fresh data
SELECT * FROM table
OPTIONS(use_cache=false);
```

#### Materialized Views
```sql
-- Create materialized view for expensive aggregation
CREATE MATERIALIZED VIEW project.dataset.daily_revenue AS
SELECT
  DATE(order_timestamp) as date,
  product_category,
  SUM(amount) as revenue,
  COUNT(*) as order_count
FROM project.dataset.orders
GROUP BY date, product_category;

-- Query automatically uses MV (smart tuning)
SELECT date, SUM(revenue) FROM project.dataset.orders
WHERE DATE(order_timestamp) BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY DATE(order_timestamp);
-- BigQuery may use materialized view automatically
```

### Cost Optimization Strategies
#### Storage Cost Reduction
```sql
-- Use long-term storage (50% discount)
-- Automatically applied to tables not modified in 90 days

-- Export old data to Cloud Storage
EXPORT DATA OPTIONS(
  uri='gs://bucket/archive/*.parquet',
  format='PARQUET'
) AS
SELECT * FROM mydataset.old_table
WHERE date < '2023-01-01';

-- Delete old partitions
DELETE FROM mydataset.partitioned_table
WHERE partition_date < '2023-01-01';
```

#### Query Cost Reduction
```sql
-- Use dry-run to estimate cost before running
bq query --dry_run 'SELECT * FROM large_table'

-- Partition pruning (massive savings)
SELECT * FROM partitioned_table
WHERE partition_column = 'specific_value';

-- Clustering (additional savings)
SELECT * FROM clustered_table
WHERE cluster_column = 'specific_value';

-- Avoid SELECT *
SELECT id, name FROM table;  -- Only scans 2 columns

-- Use table sampling for testing
SELECT * FROM large_table TABLESAMPLE SYSTEM (1 PERCENT);

-- Use preview (free, no query cost)
-- Available in console only
```

#### Flat-Rate vs On-Demand Decision
```text
Monthly On-Demand Cost Calculation:
- Average 10 TB scanned per day
- 10 TB × 30 days = 300 TB/month
- 300 TB × $6.25 = $1,875/month (minus 1 TB free = $1,850)

Flat-Rate Comparison:
- 100 slots = $2,000/month
- If usage >300 TB/month → Flat-rate is better
- If usage <280 TB/month → On-demand is better
```

### Data Quality and Validation
#### Data Quality Checks
```sql
-- Check for nulls
SELECT
  COUNTIF(customer_id IS NULL) as null_customer_ids,
  COUNTIF(amount IS NULL) as null_amounts,
  COUNT(*) as total_rows
FROM orders;

-- Check for duplicates
SELECT customer_id, COUNT(*) as count
FROM customers
GROUP BY customer_id
HAVING count > 1;

-- Validate referential integrity
SELECT COUNT(*) FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;
-- Should be 0 if integrity is maintained
```

#### Automated Data Quality with Dataform
```sql
-- Define assertions in Dataform
-- Fail pipeline if data quality issues found
```

### Disaster Recovery and Backup
#### Table Snapshots
```sql
-- Create snapshot (point-in-time copy)
CREATE SNAPSHOT TABLE mydataset.orders_snapshot
CLONE mydataset.orders
OPTIONS(expiration_timestamp=TIMESTAMP_ADD(CURRENT_TIMESTAMP(), INTERVAL 7 DAY));

-- Restore from snapshot
CREATE TABLE mydataset.orders_restored
CLONE mydataset.orders_snapshot;
```

#### Cross-Region Backup
```sql
-- Copy table to different region
bq cp --location=us mydataset.table us-backup:mydataset.table

-- Export to Cloud Storage (multi-region bucket)
EXPORT DATA OPTIONS(
  uri='gs://multi-region-bucket/backup/*.parquet',
  format='PARQUET'
) AS
SELECT * FROM mydataset.table;
```

#### Time Travel for Recovery
```sql
-- Recover deleted table (within 7 days)
SELECT * FROM `mydataset.deleted_table`
FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR);

-- Restore to new table
CREATE TABLE mydataset.recovered_table AS
SELECT * FROM `mydataset.deleted_table`
FOR SYSTEM_TIME AS OF '2024-01-15 12:00:00 UTC';
```

### Security and Compliance
#### Data Encryption
- **At-rest**: Default encryption or CMEK
- **In-transit**: TLS encryption
- **Column-level encryption**: Application-layer or AEAD functions

```sql
-- Use AEAD for column-level encryption
SELECT
  customer_id,
  KEYS.KEYSET_CHAIN('gcp-kms://...'),
  AEAD.ENCRYPT(KEYS.KEYSET_CHAIN('gcp-kms://...'), ssn, '') as encrypted_ssn
FROM customers;
```

#### Access Control Patterns
```sql
-- Authorized view (share subset without full access)
CREATE VIEW mydataset.public_orders AS
SELECT order_id, order_date, amount
FROM mydataset.orders
WHERE status = 'completed';

-- Grant access to view only
GRANT `roles/bigquery.dataViewer`
ON VIEW mydataset.public_views
TO 'user:analyst@example.com';
```

#### Audit Logging
```sql
-- Query audit logs
SELECT
  timestamp,
  protoPayload.authenticationInfo.principalEmail,
  protoPayload.serviceData.jobQueryResponse.job.jobConfiguration.query.query
FROM `project.dataset.cloudaudit_googleapis_com_data_access`
WHERE resource.type = 'bigquery_resource'
ORDER BY timestamp DESC;
```

### Advanced Analytics
#### Window Functions
```sql
-- Running total
SELECT
  order_date,
  amount,
  SUM(amount) OVER (ORDER BY order_date) as running_total
FROM orders;

-- Rank and percentile
SELECT
  product_id,
  revenue,
  RANK() OVER (ORDER BY revenue DESC) as rank,
  PERCENT_RANK() OVER (ORDER BY revenue) as percentile
FROM product_revenue;
```

#### User-Defined Functions (UDF)
```sql
-- JavaScript UDF
CREATE TEMP FUNCTION multiplyInputs(x FLOAT64, y FLOAT64)
RETURNS FLOAT64
LANGUAGE js AS """
  return x * y;
""";

SELECT multiplyInputs(3, 4);  -- Returns 12

-- SQL UDF
CREATE TEMP FUNCTION addTax(amount FLOAT64, tax_rate FLOAT64)
RETURNS FLOAT64 AS (
  amount * (1 + tax_rate)
);

SELECT addTax(100, 0.08);  -- Returns 108
```

### BigQuery ML Advanced
```sql
-- Time series forecasting
CREATE OR REPLACE MODEL mydataset.arima_model
OPTIONS(model_type='ARIMA_PLUS', time_series_timestamp_col='date', time_series_data_col='sales') AS
SELECT date, sales FROM mydataset.daily_sales;

-- Forecast next 30 days
SELECT * FROM ML.FORECAST(MODEL mydataset.arima_model, STRUCT(30 AS horizon));

-- Anomaly detection
CREATE OR REPLACE MODEL mydataset.anomaly_model
OPTIONS(model_type='AUTOML_REGRESSOR', input_label_cols=['value']) AS
SELECT timestamp, value FROM mydataset.metrics;

SELECT * FROM ML.DETECT_ANOMALIES(MODEL mydataset.anomaly_model, ..., STRUCT(0.95 as contamination));
```

### Integration Patterns
#### Streaming Analytics Pipeline
```text
[Application] → [Pub/Sub] → [Dataflow] → [BigQuery Streaming]
                                                  ↓
                                          [BI Dashboard]
                                          (BI Engine for sub-second)
```

#### Data Lakehouse Pattern
```text
[Raw Data] → [Cloud Storage (Parquet)]
                    ↓
          [BigQuery External Tables]
                    ↓
          [Curated BigQuery Tables] ← [dbt transformations]
                    ↓
          [Data Marts / BI]
```

### Migration Strategies
#### From Redshift to BigQuery
1. **Assessment**: Analyze Redshift usage, queries, schema
2. **Schema conversion**: Convert DDL (automated tools available)
3. **Data migration**:
   - Export Redshift to S3 (Parquet)
   - Transfer S3 to GCS (Storage Transfer Service)
   - Load GCS to BigQuery
4. **Query conversion**: Convert SQL (mostly compatible)
5. **Testing**: Validate data and performance
6. **Cutover**: Switch applications to BigQuery

#### From On-Prem Data Warehouse
- Use BigQuery Data Transfer Service
- Or Dataflow for complex ETL
- Incremental migration recommended

### Well-Architected Considerations
- **Operational Excellence**:
  - Serverless (no infrastructure management)
  - Automated optimization (clustering, caching)
  - Monitoring with Cloud Monitoring
- **Reliability**:
  - Automatic replication
  - Time travel for recovery
  - Table snapshots for backups
- **Security**:
  - VPC Service Controls
  - Column and row-level security
  - CMEK encryption
  - Comprehensive audit logging
- **Performance**:
  - Partitioning and clustering
  - Materialized views
  - BI Engine for dashboards
  - Query caching
- **Cost**:
  - Pay per query (on-demand)
  - Flat-rate for predictable costs
  - Long-term storage discounts
  - Partitioning to reduce scanned data
- **Sustainability**:
  - Serverless (efficient resource usage)
  - Automatic optimization
  - Query-based pricing incentivizes efficiency
