---
title: Cloud-storage
category: GCP
description: 'GCP note: Cloud-storage.'
tags:
- gcp
- storage
---


# Cloud-storage

`gcp` `storage`

## Cloud Storage
**AWS Equivalent:** [[storage-s3|S3]]
**Object storage** for unstructured data - fully managed, scalable, and durable

### Overview
- Store any amount of data, retrieve it any time
- **11 nines (99.999999999%) durability**
- Global unique bucket names across all GCP projects
- Unlimited objects, max single object size **5 TiB**
- No minimum object size, no limit on bucket size
- Regional, dual-regional, or multi-regional storage

### Storage Classes
**AWS Comparison:** Similar to S3 storage classes but different retrieval fees

| Storage Class | Use Case | Availability | Min Duration | Retrieval Cost |
|---------------|----------|--------------|--------------|----------------|
| **Standard** | Frequently accessed data | 99.99% (multi/dual) / 99.9% (regional) | None | None |
| **Nearline** | Data accessed ~once/month | 99.9% (multi/dual) / 99.0% (regional) | **30 days** | Yes |
| **Coldline** | Data accessed ~once/quarter | 99.9% (multi/dual) / 99.0% (regional) | **90 days** | Yes |
| **Archive** | Long-term backup, disaster recovery | 99.9% (multi/dual) / 99.0% (regional) | **365 days** | Yes |

**Key Differences from S3:**
- **No separate Glacier service - Archive is integrated**
- Retrieval is immediate for all classes (no restore time like Glacier)
- **Early deletion charges if deleted before minimum duration**
- Can change storage class without moving data

### Location Types
#### Regional
- Data stored in single GCP region
- **Lowest latency for in-region access**
- Lower cost than dual/multi
- Use case: Analytics, compute in same region

#### Dual-Regional
- Replicated across 2 specific regions within same geo
- Automatically replicates data
- Examples: `nam4` (us-central1 + us-east1)
- Use case: High availability for specific geo

#### Multi-Regional
- Replicated across multiple regions in geo (US, EU, ASIA)
- **Highest availability**
- Geo-redundancy
- Use case: Global content serving, websites

### Bucket Naming Rules
- **Globally unique** across all GCP projects
- 3-63 characters, lowercase letters, numbers, hyphens
- Cannot begin with "goog" or contain "google"
- **Cannot change bucket name after creation**
- Cannot contain dots if using SSL/TLS

### Object Versioning
**AWS Equivalent:** [[storage-s3|S3 Versioning]]
- **Disabled by default**
- When enabled, creates new version for each modification
- Deletes create delete marker (not permanent)
- Old versions retained until explicitly deleted
- **Non-current versions incur storage costs**
- **Cannot disable, only suspend** (keeps existing versions)
- List versions: `gsutil ls -a gs://BUCKET_NAME`

### Object Lifecycle Management
**AWS Equivalent:** [[storage-s3|S3 Lifecycle Policies]]
- Automate storage class transitions and deletions
- Conditions:
  - **Age**: Days since upload
  - **CreatedBefore**: Specific date
  - **IsLive**: Current vs noncurrent versions
  - **MatchesStorageClass**: Current storage class
  - **NumberOfNewerVersions**: For versioned objects
  - **DaysSinceNoncurrentTime**: For noncurrent versions
- Actions:
  - **Delete**: Remove object
  - **SetStorageClass**: Transition to another class
- **Runs once per day**
- No transition from Archive back to other classes

### Access Control
#### Uniform (Bucket-level) - Recommended
- **Uses only [[gcp/iam|Cloud IAM]]**
- Applies to all objects in bucket
- **Cannot be reverted to fine-grained for 90 days**
- Simpler, recommended for new buckets
- Required for some features (Bucket Lock, Pub/Sub notifications)

#### Fine-grained (Object-level)
- IAM + ACLs (Access Control Lists)
- Per-object permissions possible
- Legacy approach
- More complex to manage

**Common IAM Roles:**
- `roles/storage.objectViewer`: Read objects
- `roles/storage.objectCreator`: Create objects
- `roles/storage.objectAdmin`: Full control of objects
- `roles/storage.admin`: Full control of buckets and objects

### Access Control Lists (ACLs)
**AWS Equivalent:** [[storage-s3|S3 ACLs]]
- Only with fine-grained access control
- Predefined ACLs:
  - `private`: Owner only
  - `projectPrivate`: Project team based on roles
  - `publicRead`: **All users can read**
  - `publicReadWrite`: All users can read/write (not recommended)
- Apply to bucket or individual objects
- `gsutil acl set public-read gs://bucket/object`

### Signed URLs (Presigned URLs)
**AWS Equivalent:** [[storage-s3|S3 Presigned URLs]]
- Time-limited access to specific objects
- No GCP account needed for the user
- **Valid from 1 second to 7 days**
- Uses service account credentials
- Supports GET, PUT, DELETE, POST
- Can restrict by IP address

```bash
# Generate signed URL
gsutil signurl -d 10m /path/to/key.json gs://bucket/object
```

### Signed Policy Documents
**AWS Equivalent:** [[storage-s3|S3 POST Policy]]
- Control uploads with specific conditions
- File size limits, content type restrictions
- Expiration time
- Use case: Allow users to upload directly to Cloud Storage from browser

### Requester Pays
**AWS Equivalent:** [[storage-s3|S3 Requester Pays]]
- Requester pays networking and operation costs
- Bucket owner pays storage costs
- Requester must include project ID in request
- **Requester must have billing enabled**
- Use case: Public datasets where users pay for their access

### Object Holds & Retention Policies
#### Retention Policy
- **Minimum retention duration** for all objects in bucket
- Objects cannot be deleted/modified until retention period met
- Can increase duration, but **cannot decrease or remove once locked**
- Use case: Compliance (HIPAA, SEC, FINRA)

#### Bucket Lock
- **Permanently locks retention policy**
- **Cannot be removed or reduced, even by Google**
- Required for regulatory compliance

#### Object Holds
- **Event-based hold**: Until event occurs (e.g., legal case closed)
- **Temporary hold**: Manually set/remove
- Prevents deletion even if retention period expired
- Use case: Legal holds, investigations

**AWS Comparison:** AWS has S3 Object Lock with similar WORM capabilities

### Encryption
#### Encryption at Rest (Automatic)
- **Google-managed keys**: Default, automatic, **no configuration needed**
- **Customer-managed keys (CMEK)**: Keys in [[security-kms|Cloud KMS]]
  - Rotate keys, audit usage
  - Regional KMS key must match bucket location
- **Customer-supplied keys (CSEK)**: You manage keys
  - **You provide encryption key with each request**
  - Google doesn't store your key
  - ==Higher risk - lose key = lose data==

#### Encryption in Transit
- **HTTPS/TLS by default**
- All data encrypted between client and Google

### Object Composition
**AWS Comparison:** S3 Multipart Upload (similar concept)
- Combine up to **32 objects** into single object
- Parallel uploads, then compose
- More efficient for large files
- Component objects can be deleted after composition

```bash
gsutil compose gs://bucket/part1 gs://bucket/part2 gs://bucket/final
```

### Object Change Notification
#### Pub/Sub Notifications (Recommended)
**AWS Equivalent:** [[storage-s3|S3 Event Notifications]]
- Send notifications to [[gcp/pub-sub|Pub/Sub]] topic
- Events: Object finalize, delete, archive, metadata update
- More reliable and scalable than legacy notifications
- Requires uniform bucket-level access
- Can filter by object name prefix/suffix

#### Legacy Object Change Notification
- Webhooks via HTTPS
- Less reliable, **deprecated - use Pub/Sub**

### CORS (Cross-Origin Resource Sharing)
**AWS Equivalent:** [[storage-s3|S3 CORS]]
- Allow browser-based apps to access bucket from different origin
- Configure allowed origins, methods, headers
- Set via JSON configuration file
- Required for direct browser uploads

```json
[
  {
    "origin": ["https://example.com"],
    "method": ["GET", "POST"],
    "responseHeader": ["Content-Type"],
    "maxAgeSeconds": 3600
  }
]
```

### Object Metadata
- **Standard metadata**: Content-Type, Cache-Control, etc.
- **Custom metadata**: Key-value pairs with `x-goog-meta-` prefix
- **Immutable after object creation** (must copy to new object to change)
- Set via `gsutil setmeta` or during upload

### Transfer Methods
#### gsutil
- Command-line tool for Cloud Storage
- Supports parallel composite uploads
- Rsync functionality for sync operations
- **Fastest for large transfers from on-prem**

#### Storage Transfer Service
**AWS Equivalent:** [[storage-s3|AWS DataSync]]
- **Transfer from AWS S3, Azure, HTTP/HTTPS sources**
- Scheduled or one-time transfers
- **Managed service, no infrastructure needed**
- Filters by prefix, suffix, modification time
- Use case: Cloud-to-cloud migrations

#### Transfer Appliance
**AWS Equivalent:** [[storage-s3|AWS Snowball]]
- Physical device shipped to your datacenter
- Up to **1 PB capacity**
- Encrypted transfer
- Use case: Offline large data transfers (>20 TB)

#### Cloud Storage Connector for Apache Hadoop
- Access Cloud Storage from Hadoop/Spark
- Works with [[dataproc|Cloud Dataproc]]
- GCS appears as HDFS

### Object Naming Best Practices
- **Sequential names**: Avoid sequential prefixes for high throughput
- **Date-based**: Reverse order (YYYY-MM-DD → DD-MM-YYYY) for better distribution
- **Random prefix**: Better performance for high request rates
- **No slashes needed - flat namespace with delimiter appearance**

### Cloud Storage FUSE
- Mount Cloud Storage buckets as file systems
- Linux/macOS support
- **Not suitable for high-performance workloads**
- Writes are not visible until file is closed
- Use case: Legacy apps expecting file system interface

### Pricing
- **Storage**: Per GB-month by storage class
- **Operations**: Class A (writes), Class B (reads)
- **Network egress**: Data leaving GCP
  - Same region: Free
  - Different region same continent: Lower cost
  - Inter-continental: Higher cost
  - **To Google services (BigQuery, etc): Often free**
- **Retrieval**: Nearline, Coldline, Archive have retrieval costs
- **Early deletion**: Charged if deleted before minimum duration
- **Free tier**: 5 GB Standard storage per month (us-west1, us-central1, us-east1)

### Use Cases by Storage Class
- **Standard**: Active data, websites, streaming, analytics
- **Nearline**: Backups, long-tail multimedia, data analytics
- **Coldline**: Disaster recovery, quarterly backups
- **Archive**: Compliance archives, legal/regulatory data

---

## ACE Level

### Essential gsutil Commands
```bash
# Create bucket
gsutil mb -l LOCATION -c STORAGE_CLASS gs://BUCKET_NAME

# List buckets
gsutil ls

# List objects in bucket
gsutil ls gs://BUCKET_NAME
gsutil ls -r gs://BUCKET_NAME/**  # Recursive

# Upload object
gsutil cp LOCAL_FILE gs://BUCKET_NAME/
gsutil cp -r LOCAL_DIR gs://BUCKET_NAME/  # Recursive

# Download object
gsutil cp gs://BUCKET_NAME/OBJECT LOCAL_PATH

# Delete object
gsutil rm gs://BUCKET_NAME/OBJECT
gsutil rm -r gs://BUCKET_NAME/**  # Delete all

# Delete bucket
gsutil rb gs://BUCKET_NAME

# Make object public
gsutil acl ch -u AllUsers:R gs://BUCKET_NAME/OBJECT

# Enable versioning
gsutil versioning set on gs://BUCKET_NAME

# Set lifecycle policy
gsutil lifecycle set lifecycle.json gs://BUCKET_NAME

# Sync directories
gsutil rsync -r LOCAL_DIR gs://BUCKET_NAME/

# Set storage class
gsutil rewrite -s STORAGE_CLASS gs://BUCKET_NAME/OBJECT

# Get object metadata
gsutil stat gs://BUCKET_NAME/OBJECT

# Set CORS configuration
gsutil cors set cors.json gs://BUCKET_NAME

# Generate signed URL
gsutil signurl -d DURATION key.json gs://BUCKET_NAME/OBJECT
```

### gcloud Commands
```bash
# Create bucket (alternative)
gcloud storage buckets create gs://BUCKET_NAME \
  --location=LOCATION \
  --storage-class=STORAGE_CLASS

# List buckets
gcloud storage buckets list

# Describe bucket
gcloud storage buckets describe gs://BUCKET_NAME

# Add IAM policy binding
gcloud storage buckets add-iam-policy-binding gs://BUCKET_NAME \
  --member=user:EMAIL \
  --role=roles/storage.objectViewer

# Set retention policy
gcloud storage buckets update gs://BUCKET_NAME \
  --retention-period=SECONDS

# Lock retention policy
gcloud storage buckets update gs://BUCKET_NAME --lock-retention-period
```

### Key Concepts for ACE
- Creating and managing buckets in different locations
- Uploading and downloading objects using gsutil
- Understanding storage classes and when to use each
- Setting appropriate access controls (IAM vs ACLs)
- Enabling and managing object versioning
- Configuring lifecycle policies for cost optimization
- Generating signed URLs for temporary access
- Enabling Pub/Sub notifications
- Configuring CORS for web applications
- Understanding encryption options
- Monitoring storage usage and costs

---

## PCA Level

### Architectural Patterns
#### Static Website Hosting
**AWS Equivalent:** [[storage-s3|S3 Static Website Hosting]]
- Cloud Storage + Cloud CDN + [[gcp/cloud-load-balancing|Load Balancing]]
- **No native website hosting mode** (unlike S3)
- Requires Load Balancer backend bucket
- Custom domain via CNAME or Load Balancer
- SSL/TLS via Load Balancer

#### Data Lake Architecture
- Cloud Storage as central repository
- Standard for hot data, Nearline/Coldline for warm/cold
- [[bigquery|BigQuery]] for analytics (query in-place)
- [[gcp/dataflow|Dataflow]] for ETL
- Organize by zone: raw, curated, analytics-ready

#### Backup & Disaster Recovery
- Multi-regional for geo-redundancy
- Versioning for protection against accidental deletion
- Lifecycle policies to transition to Archive
- [[cloud-scheduler|Cloud Scheduler]] + [[cloud-functions|Cloud Functions]] for automated backups
- Cross-region replication via Storage Transfer Service

#### Content Delivery
- Cloud Storage + Cloud CDN
- Multi-regional buckets for global access
- Signed URLs for protected content
- Cache-Control headers for CDN optimization
- **Cloud CDN can cache public objects automatically**

### High Availability Design
- **Multi-regional buckets**: Automatic geo-replication
- **Dual-regional**: HA within geo at lower cost
- **Turbo replication**: **Replication in under 15 minutes** (multi/dual-regional)
  - Default is eventual consistency
  - Add-on feature for RPO < 15 min
- **Versioning**: Protection against accidental deletion
- **Object holds**: Prevent data loss during incidents

### Security Best Practices
- **Access Control**:
  - **Uniform access (IAM only) for all new buckets**
  - Principle of least privilege
  - Service accounts for application access
  - Signed URLs for temporary external access
- **Encryption**:
  - Default encryption at rest with Google-managed keys
  - CMEK for regulatory compliance
  - CSEK only when absolute key control required
- **[[vpc|VPC Service Controls]]**:
  - **Prevent data exfiltration**
  - Restrict bucket access to specific VPC
  - Control data movement between projects
- **Bucket Lock**: For compliance (WORM)
- **Public access prevention**: Org policy to block public access
- **Audit logging**: [[gcp/cloud-logging|Cloud Logging]] for all access

### Cost Optimization
- **Storage class selection**:
  - Standard: Accessed >1/month
  - Nearline: Accessed ~1/month
  - Coldline: Accessed ~1/quarter
  - Archive: Accessed <1/year
- **Lifecycle policies**:
  - Auto-transition to cheaper classes
  - Delete old versions after X days
  - Delete incomplete multipart uploads
- **Regional vs multi-regional**:
  - Regional 30-40% cheaper
  - Use regional if data accessed primarily in one region
- **Network costs**:
  - Keep compute and storage in same region
  - Use Cloud CDN to reduce egress
  - Cloud Interconnect for high-volume on-prem access
- **Versioning overhead**: Monitor and clean up old versions
- **Compression**: Compress before upload (GCS doesn't auto-compress)

### Performance Optimization
- **Request rate distribution**:
  - Avoid sequential naming for high throughput
  - Add random prefix for >1000 write requests/sec
- **Parallel composite uploads**:
  - Split large files, upload in parallel, compose
  - gsutil `-m` flag for parallel operations
- **gsutil configuration**:
  - Adjust parallel thread count
  - Enable sliced object downloads for large files
- **Cloud CDN**: Reduce latency for global users
- **Colocation**: Keep compute and storage in same region
- **Connection pooling**: Reuse HTTP connections

### Data Migration Strategies
#### Cloud-to-Cloud
- **Storage Transfer Service**: AWS S3 → Cloud Storage
  - Automated, scheduled transfers
  - Incremental sync support
  - Deletion sync option
  - Filters for selective transfer

#### On-Premises
- **Small (<1 TB)**: gsutil rsync
- **Medium (1-20 TB)**: Storage Transfer Service via HTTP/HTTPS
- **Large (>20 TB)**: Transfer Appliance

#### Application Integration
- **Cloud Storage libraries**: Java, Python, Node.js, Go, etc.
- **REST API**: Direct HTTP access
- **gRPC API**: Higher performance
- **Cloud Storage FUSE**: For legacy file-based apps (limited performance)

### Integration Patterns
#### BigQuery External Tables
- Query Cloud Storage data without loading into BigQuery
- Supports CSV, JSON, Avro, Parquet, ORC
- Lower cost but slower than native tables
- Use case: Infrequently queried historical data

#### Dataflow/Dataproc
- Cloud Storage as input/output for data processing
- Temporary storage for shuffle operations
- Use regional buckets in same location as jobs

#### Cloud Functions/Cloud Run
- Process files uploaded to Cloud Storage
- Pub/Sub notifications trigger function
- Use case: Image processing, file validation, ETL

#### Cloud SQL/Spanner
- Import/export data via Cloud Storage
- Backup storage location
- Large data loads

### Compliance & Governance
- **Retention policies**: Minimum retention duration
- **Bucket Lock**: Immutable retention (WORM)
- **Audit logs**: Track all access and modifications
- **Data residency**: Regional buckets for data sovereignty
- **Organization policies**:
  - Restrict resource locations
  - Enforce uniform access
  - Prevent public access
- **Cloud DLP**: Scan for sensitive data (PII, PCI)

### Monitoring & Observability
- **[[gcp/cloud-monitoring|Cloud Monitoring]] metrics**:
  - Request count (by method, response code)
  - Bucket total bytes
  - Object count
  - Network bytes sent/received
- **[[gcp/cloud-logging|Cloud Logging]]**:
  - Admin activity logs (bucket operations)
  - Data access logs (object operations - must enable)
- **Storage Insights**: Inventory and metadata insights
  - Object age distribution
  - Storage class distribution
  - Unused objects
- **Alerts**: Set up for unusual access patterns, cost spikes

### Cloud Storage vs Other Options

| Requirement | Cloud Storage | [[persistent-disk|Persistent Disk]] | [[filestore|Filestore]] |
|-------------|---------------|----------------------|-----------|
| Object/file storage | ✓ Object | Block | File (NFS) |
| Shared access | ✓ Unlimited | Limited (read-only multi-attach) | ✓ Multiple VMs |
| Maximum size | Unlimited | 64 TB | 100 TB |
| Access method | HTTP/API | Mounted to VM | Mounted (NFS) |
| Performance | Good | ✓ Excellent | ✓ Excellent |
| Durability | 11 nines | 5-6 nines | 5-6 nines |
| Use case | Unstructured data, backups, archives | VM boot/data disks | Shared file access |

### Well-Architected Considerations
- **Operational Excellence**:
  - Lifecycle policies for automated management
  - Versioning for easy rollback
  - Object Change Notifications for event-driven workflows
- **Reliability**:
  - Multi-regional for geo-redundancy
  - Versioning and object holds for data protection
  - 11 nines durability
- **Security**:
  - Uniform IAM access control
  - Encryption at rest and in transit
  - VPC SC for data exfiltration prevention
  - Bucket Lock for compliance
- **Performance**:
  - Regional buckets for low-latency access
  - Cloud CDN for global content delivery
  - Parallel composite uploads for large files
- **Cost**:
  - Appropriate storage class selection
  - Lifecycle policies for auto-tiering
  - Regional over multi-regional when possible
  - Monitor and delete unused data
- **Sustainability**:
  - Use coldest storage class suitable for access pattern
  - Clean up unused data
  - Optimize data formats (compression, columnar)
