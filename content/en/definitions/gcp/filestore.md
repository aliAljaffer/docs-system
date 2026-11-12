---
title: Filestore
category: GCP
description: 'GCP note: Filestore.'
tags:
- gcp
- storage
---


# Filestore

`gcp` `storage`

## Filestore
**Fully managed Network File System (NFS) storage** for [[gcp/compute-engine|Compute Engine]] and [[gcp/gke|GKE]]

**AWS Equivalent:** [[storage-efs|EFS (Elastic File System)]]

### Overview
- Managed Network File System (NFS)
- **NFSv3 protocol** (industry-standard)
- Shared file storage for multiple VMs/containers
- **Low latency, high throughput**
- No minimum file size or file count
- Automatic replication within zone
- Integrates with Compute Engine, GKE, on-premises

### Service Tiers
**AWS Comparison:** Similar to EFS storage classes but different performance/pricing model

| Tier | Performance | Capacity | IOPS | Throughput | Use Case | Price |
|------|-------------|----------|------|------------|----------|-------|
| **Basic HDD** | Standard | 1-10 TiB | Up to 3,000 | Up to 180 MB/s | File shares, web serving | Lowest |
| **Basic SSD** | High | 2.5-10 TiB | Up to 60,000 | Up to 1,200 MB/s | Latency-sensitive apps | Higher |
| **High Scale SSD** | Very High | 10-100 TiB | Up to 100,000 | Up to 2,400 MB/s | High-performance workloads | Highest |
| **Enterprise** | Very High + HA | 1-10 TiB | Up to 100,000 | Up to 1,200 MB/s | **Regional HA, critical apps** | Premium |
| **Zonal** | Balanced | 1-100 TiB | Varies | Varies | General purpose, dev/test | Mid |

**Key Differences from EFS:**
- **No automatic tiering** like EFS Infrequent Access
- Performance scales with tier, not capacity (EFS scales with usage)
- **Enterprise tier provides regional HA** (EFS is always multi-AZ)
- Pricing based on provisioned capacity, not usage

### Service Tier Details
#### Basic HDD
- **1 TiB to 10 TiB** provisioned capacity
- HDD-based storage
- **Up to 3,000 IOPS** for reads
- Up to 180 MB/s throughput
- **Zonal** (single zone replication)
- Use cases: File shares, web content, general purpose

#### Basic SSD
- **2.5 TiB to 10 TiB** provisioned capacity
- SSD-based storage
- **Up to 60,000 IOPS** for reads
- Up to 1,200 MB/s throughput
- **Zonal** (single zone replication)
- Use cases: Latency-sensitive apps, databases on file storage

#### High Scale SSD
- **10 TiB to 100 TiB** provisioned capacity
- **Ultra-high performance**
- Up to 100,000 IOPS for reads
- Up to 2,400 MB/s throughput
- **Zonal** (single zone replication)
- Use cases: Render farms, genomics, EDA, HPC

#### Enterprise (Recommended for Production)
- **1 TiB to 10 TiB** provisioned capacity
- **Regional high availability** (replicated across zones)
- Up to 100,000 IOPS for reads
- Up to 1,200 MB/s throughput
- **99.99% SLA** (vs 99.9% for other tiers)
- Automatic failover between zones
- Use cases: Critical production workloads, databases

#### Zonal
- **1 TiB to 100 TiB** provisioned capacity
- Flexible capacity and performance
- Performance scales with capacity
- **Zonal** (single zone replication)
- Use cases: Dev/test, general purpose file shares

### Filestore Features
#### Network Connectivity
- Accessible via **VPC network**
- Requires [[gcp/vpc|VPC]] with Private Services Access
- Can access from:
  - [[gcp/compute-engine|Compute Engine]] VMs in same [[gcp/vpc|VPC]]
  - [[gcp/gke|GKE]] clusters in same [[gcp/vpc|VPC]]
  - On-premises via [[gcp/cloud-vpn|Cloud VPN]] or [[gcp/cloud-interconnect|Cloud Interconnect]]
- **Cannot access from internet directly**

#### Shared Access
- **Multiple clients can read/write simultaneously**
- Standard NFS file locking
- Up to **1,000 clients** per instance (recommended)
- POSIX-compliant permissions
- UID/GID-based access control

#### Snapshots
**AWS Equivalent:** [[storage-efs|EFS Backups]]
- Point-in-time copy of file share
- **On-demand or scheduled** snapshots
- **Incremental** (only changed data)
- Restore to new or existing instance
- Stored in same region as instance
- Up to **200 snapshots per instance**
- **Cannot move snapshots across regions**

#### Backups
- **Scheduled or on-demand**
- Stored in [[cloud-storage|Cloud Storage]] (regional or multi-regional)
- **Can restore to different region** (cross-region DR)
- Incremental backups
- Retention policies supported
- Use case: Disaster recovery, long-term retention

**Snapshots vs Backups:**
- **Snapshots**: Fast restore, same region only, **lower cost**
- **Backups**: Cross-region restore, Cloud Storage-based, **better DR**

#### File Locking
- **NFSv3 file locking supported**
- Advisory locks (not mandatory)
- Byte-range locking
- Prevents concurrent write conflicts

### Capacity and Scaling
#### Scaling Behavior
- **Manual scaling only** (not automatic like EFS)
- Increase or decrease capacity via console/gcloud
- **No downtime** during capacity changes
- Performance scales with capacity (except Enterprise/Zonal)
- Cannot scale below tier minimum

#### Performance Scaling
- **Basic/High Scale**: Fixed IOPS per tier
- **Zonal**: Performance increases with capacity
  - ~0.25 IOPS per GiB
  - ~0.25 MB/s per GiB
- Monitor usage to right-size capacity

### Access Control
#### Network-Based
- **Private IP address only** (no public endpoint)
- [[vpc#Firewall Rules|VPC firewall rules]] control network access
- Default: Allow NFS (port 2049) within VPC
- Can restrict by source IP ranges

#### File-Level
- Standard POSIX permissions (chmod, chown)
- UID/GID mapping
- No built-in Kerberos (use third-party)
- **No integration with Cloud IAM for file permissions**
- NFSv3 AUTH_SYS authentication

### Encryption
#### At Rest
- **Automatic encryption with Google-managed keys**
- **CMEK (Customer-Managed Encryption Keys)** available
  - Encryption keys in [[security-kms|Cloud KMS]]
  - Audit key usage
  - Regional key required
- **No CSEK support**

#### In Transit
- **NFSv3 does not natively encrypt in transit**
- Secure via private VPC network
- For extra security:
  - Use [[networking-vpn|Cloud VPN]] for on-prem connections
  - Application-level encryption
  - VPC Service Controls

### Filestore Pricing
**Provisioned capacity**: Per GiB-month

| Tier | Price (per GiB-month) |
|---|---|
| Basic HDD | Lowest (~$0.20) |
| Basic SSD | Mid (~$0.30) |
| Enterprise | Premium (~$0.35) |
| High Scale SSD | Highest (~$0.35) |
| Zonal | Variable based on capacity |

- **Snapshots**: Per GiB-month of snapshot storage
- **Backups**: Cloud Storage pricing (cheaper than snapshots)
- **Network egress**: Standard egress charges
- **No per-operation charges** (unlike Cloud Storage)
- **No free tier**

### Use Cases

| Use case | Examples | Tier |
|---|---|---|
| Development Environments | Shared source code repositories, build artifacts, log aggregation | Basic HDD or Zonal |
| Content Management | Media files for web/mobile apps, WordPress shared storage, CMS file repositories | Basic HDD or Basic SSD |
| High-Performance Computing | Genomics data processing, rendering farms, financial modeling | High Scale SSD |
| Containerized Applications | [[gke|GKE]] persistent volumes (ReadWriteMany), shared configs across pods, multi-pod data sharing | Enterprise (for HA) or Basic SSD |
| Lift-and-Shift Migration | Applications requiring NFS, legacy apps with file dependencies, **direct replacement for on-prem NFS** | Based on performance needs |

### Limitations
- **No automatic tiering** to cheaper storage
- **NFSv3 only** (no NFSv4 support)
- **Regional/Zonal only** (no multi-regional like Cloud Storage)
- Cannot move instance to different VPC
- Cannot change tier after creation (must migrate)
- Minimum capacity based on tier
- **Snapshots cannot cross regions** (use backups instead)

---

## ACE Level

### Essential gcloud Commands
```bash
# Create Filestore instance (Basic SSD)
gcloud filestore instances create INSTANCE_NAME \
  --zone=ZONE \
  --tier=BASIC_SSD \
  --file-share=name=FILE_SHARE_NAME,capacity=2560GB \
  --network=name=VPC_NAME

# Create Enterprise tier (regional HA)
gcloud filestore instances create INSTANCE_NAME \
  --region=REGION \
  --tier=ENTERPRISE \
  --file-share=name=FILE_SHARE_NAME,capacity=1024GB \
  --network=name=VPC_NAME

# List instances
gcloud filestore instances list

# Describe instance
gcloud filestore instances describe INSTANCE_NAME \
  --zone=ZONE

# Update instance capacity
gcloud filestore instances update INSTANCE_NAME \
  --zone=ZONE \
  --file-share=name=FILE_SHARE_NAME,capacity=5120GB

# Delete instance
gcloud filestore instances delete INSTANCE_NAME \
  --zone=ZONE

# Create snapshot
gcloud filestore snapshots create SNAPSHOT_NAME \
  --instance=INSTANCE_NAME \
  --instance-zone=ZONE \
  --file-share=FILE_SHARE_NAME

# List snapshots
gcloud filestore snapshots list

# Restore from snapshot
gcloud filestore instances restore INSTANCE_NAME \
  --zone=ZONE \
  --file-share=FILE_SHARE_NAME \
  --source-snapshot=SNAPSHOT_NAME

# Create backup
gcloud filestore backups create BACKUP_NAME \
  --instance=INSTANCE_NAME \
  --instance-zone=ZONE \
  --file-share=FILE_SHARE_NAME \
  --region=REGION

# List backups
gcloud filestore backups list --region=REGION
```

### Mounting Filestore on Linux
```bash
# Install NFS client
sudo apt-get install nfs-common  # Debian/Ubuntu
sudo yum install nfs-utils        # RHEL/CentOS

# Create mount point
sudo mkdir -p /mnt/filestore

# Mount the file share
# Get IP address from: gcloud filestore instances describe
sudo mount FILESTORE_IP:/FILE_SHARE_NAME /mnt/filestore

# Verify mount
df -h | grep filestore

# Auto-mount on reboot (add to /etc/fstab)
echo "FILESTORE_IP:/FILE_SHARE_NAME /mnt/filestore nfs defaults,_netdev 0 0" | sudo tee -a /etc/fstab

# Mount with options
sudo mount -o rw,hard,timeo=600,retrans=2,_netdev FILESTORE_IP:/FILE_SHARE_NAME /mnt/filestore
```

### Mounting Filestore on GKE
```yaml
# PersistentVolume
apiVersion: v1
kind: PersistentVolume
metadata:
  name: filestore-pv
spec:
  capacity:
    storage: 1Ti
  accessModes:
  - ReadWriteMany
  nfs:
    path: /FILE_SHARE_NAME
    server: FILESTORE_IP
  mountOptions:
  - hard
  - nfsvers=3

---
# PersistentVolumeClaim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: filestore-pvc
spec:
  accessModes:
  - ReadWriteMany
  storageClassName: ""
  volumeName: filestore-pv
  resources:
    requests:
      storage: 1Ti

---
# Pod using the claim
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
spec:
  containers:
  - name: app
    image: nginx
    volumeMounts:
    - name: data
      mountPath: /data
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: filestore-pvc
```

### Filestore CSI Driver (GKE)
```yaml
# StorageClass for dynamic provisioning
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: filestore-sc
provisioner: filestore.csi.storage.gke.io
parameters:
  tier: enterprise
  network: VPC_NAME
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer

---
# PVC using StorageClass
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: filestore-dynamic-pvc
spec:
  accessModes:
  - ReadWriteMany
  storageClassName: filestore-sc
  resources:
    requests:
      storage: 1Ti
```

### Key Concepts for ACE
- Understanding Filestore tiers and when to use each
- Creating and managing Filestore instances
- Mounting NFS file shares on Linux VMs
- Integrating Filestore with GKE (PV/PVC)
- Creating and restoring snapshots
- Scaling Filestore capacity
- Configuring network access and firewall rules
- Understanding basic vs enterprise tier for HA
- Monitoring Filestore performance
- Cost estimation based on provisioned capacity

---

## PCA Level

### Architectural Patterns
#### High Availability Applications
- **Enterprise tier**: **Automatic regional HA**
  - Replicated across 2 zones
  - Automatic failover (<60 seconds typical)
  - 99.99% SLA
- **Application-level HA**: Basic tier + app failover
  - Backup/restore to different zone
  - Lower cost, higher RTO

#### Multi-Region Disaster Recovery
- **Cross-region backups**: Store backups in different region
  - Use Filestore backups (not snapshots)
  - Backups stored in Cloud Storage
  - Restore to any region
- **Pilot light**: Periodic backups, restore on disaster
- **Warm standby**: Pre-provisioned instance, sync via scripts/rsync

#### Hybrid Cloud Architecture
- On-premises to GCP via [[networking-vpn|Cloud VPN]] or Cloud Interconnect
- Filestore as cloud-side NFS
- Burst to cloud for additional capacity
- Gradual migration to cloud storage

### Performance Optimization
#### Tier Selection
**Decision matrix**:

| Need | Tier |
|---|---|
| <10 TiB, standard performance | Basic HDD |
| <10 TiB, low latency | Basic SSD |
| 10-100 TiB, high IOPS | High Scale SSD |
| Needs regional HA | Enterprise |
| Flexible capacity | Zonal |

- **Right-sizing**: Monitor IOPS and throughput utilization
- **Over-provisioning**: Performance tied to capacity (except Enterprise)

#### NFS Mount Options
```bash
# Recommended mount options
rw                  # Read-write access
hard                # Hard mount (recommended for production)
timeo=600          # Timeout (60 seconds)
retrans=2          # Number of retransmissions
_netdev            # Network device (wait for network)
nfsvers=3          # NFSv3 protocol
```

#### Performance Monitoring
[[gcp/cloud-monitoring|Cloud Monitoring]] metrics:

| Metric | Measures |
|---|---|
| `nfs/server/read_bytes` | Read throughput |
| `nfs/server/write_bytes` | Write throughput |
| `nfs/server/read_ops` | Read IOPS |
| `nfs/server/write_ops` | Write IOPS |
| `nfs/server/used_bytes_percent` | Capacity utilization |

- Set alerts for high utilization
- Scale capacity before hitting limits

#### Parallelism and Caching
- **Multiple NFS clients improve aggregate performance**
- Use application-level caching
- Read-heavy workloads: Cache frequently accessed files
- Write buffering: Application async writes

### Cost Optimization
#### Capacity Planning
- Provision based on actual needs + growth
- Monitor utilization: `nfs/server/used_bytes_percent`
- Scale down if consistently underutilized
- Use snapshots instead of over-provisioning for growth

#### Tier Selection for Cost
- Basic HDD: ~60% cost of Basic SSD
- Zonal: Cost varies, evaluate for your use case
- Enterprise: Premium for HA, evaluate necessity
- High Scale: Only if performance demands justify

#### Backup vs Snapshot Strategy
- **Snapshots**: Fast recovery, same region, **cheaper**
  - Use for short-term recovery (days to weeks)
- **Backups**: Cross-region DR, Cloud Storage cost
  - Use for long-term retention, DR
- Retention policies: Delete old snapshots/backups

#### Alternative Storage Considerations
- [[cloud-storage|Cloud Storage]]: Cheaper for infrequently accessed data
- [[persistent-disk|Persistent Disk]]: Better for single-VM workloads
- Filestore: Only when shared NFS access needed

### Security Best Practices
#### Network Isolation
- Deploy in **private VPC subnet**
- [[vpc#Firewall Rules|Firewall rules]]: Restrict to specific VMs/subnets
- No public IP (inherent security)
- [[vpc#vpc service controls|VPC Service Controls]]: Prevent data exfiltration

#### Encryption
- **At-rest**: Default Google-managed or CMEK
  - CMEK for compliance/audit requirements
  - Rotate keys in Cloud KMS
- **In-transit**: Private VPC network
  - **No native NFSv3 encryption**
  - VPN for on-prem connections
  - Application-level encryption if needed

#### Access Control
- **Network-level**: VPC firewall rules, Private Services Access
- **File-level**: POSIX permissions (UID/GID)
  - Implement consistent UID/GID across clients
  - Use [[iam#service accounts|service accounts]] for VM identity
- **Audit**: [[gcp/cloud-logging|Cloud Audit Logs]] for admin operations
  - Track instance creation/deletion
  - Snapshot/backup operations

### Migration Strategies
#### From On-Premises NFS
- **Assessment**: Measure current capacity, IOPS, throughput
- **Tier selection**: Map performance to Filestore tier
- **Migration methods**:
  - **rsync**: Good for <10 TB
  - **Cloud Storage Transfer Service**: For cloud NFS
  - **Transfer Appliance**: For offline large transfers
- **Cutover**: DNS/mount point change

#### From AWS EFS
- **Export EFS to S3**: Use AWS DataSync
- **Transfer to Cloud Storage**: Storage Transfer Service
- **Import to Filestore**: Mount Cloud Storage, copy to Filestore
- **Alternative**: Use Filestore backups if supported

### GKE Integration Patterns
#### StatefulSets with Filestore
- Shared storage across pods
- **ReadWriteMany (RWX) access mode**
- Config files, shared data
- Logs aggregation

#### Filestore CSI Driver
- **Dynamic provisioning** of Filestore instances
- StorageClass-based tier selection
- Automatic instance creation/deletion
- Volume expansion support

#### Multi-Zone GKE + Enterprise Filestore
- Regional GKE cluster
- Enterprise Filestore (regional HA)
- Pods in any zone can access
- Automatic failover on zone failure

### Filestore vs Alternatives

| Requirement | Filestore | [[cloud-storage|Cloud Storage]] | [[persistent-disk|Persistent Disk]] | On-Prem NFS |
|-------------|-----------|-----------------|------------------|-------------|
| Access pattern | Shared read-write | Object storage | Block, single-writer | Shared read-write |
| Protocol | NFS | HTTP/gRPC | Block device | NFS |
| Max clients | 1,000 | Unlimited | 1 writer (10 readers) | Varies |
| Performance | High (IOPS/throughput) | Moderate | Very High | Depends |
| HA (Enterprise) | ✓ Regional | ✓ Multi-regional | Regional PD only | Manual setup |
| Cost | Mid-High | Low (tiered) | Mid | Infrastructure cost |
| Use case | Shared files | Unstructured data | VM disks | Legacy apps |

### Well-Architected Considerations
- **Operational Excellence**:
  - Automated snapshot schedules
  - Backups to Cloud Storage for DR
  - Monitoring with Cloud Monitoring
  - Capacity planning and alerts
- **Reliability**:
  - Enterprise tier for regional HA
  - Regular snapshots for recovery
  - Cross-region backups for DR
  - Testing restore procedures
- **Security**:
  - Private VPC deployment
  - CMEK for encryption compliance
  - Firewall rules for network isolation
  - VPC Service Controls
  - Audit logging enabled
- **Performance**:
  - Right tier for workload
  - NFS mount options optimization
  - Monitor IOPS/throughput utilization
  - Scale capacity proactively
- **Cost**:
  - Right-size provisioned capacity
  - Use Basic HDD for non-latency-sensitive
  - Snapshot retention policies
  - Consider alternatives (Cloud Storage for object data)
  - Committed use discounts not available (fixed pricing)
- **Sustainability**:
  - Right-size to avoid over-provisioning
  - Use lower-tier storage where performance allows
  - Clean up unused snapshots/backups
