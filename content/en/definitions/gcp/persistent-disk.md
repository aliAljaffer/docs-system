---
title: persistent-disk
category: GCP
description: 'GCP note: Persistent-disk.'
tags:
- gcp
- storage
---


# persistent-disk

`gcp` `storage`

## Persistent Disk
**Block storage** for [[gcp/compute-engine|Compute Engine]] and [[gcp/gke|GKE]] - network-attached, durable

**AWS Equivalent:** [[storage-ebs|EBS (Elastic Block Storage)]]

### Overview
- Network-attached block storage for VMs
- **Independent of VM lifecycle** (survives VM termination by default)
- Can attach to multiple VMs in **read-only mode**
- Automatic encryption at rest
- Regional or zonal availability
- **Performance scales with size**

### Disk Types
**AWS Comparison:** Similar to EBS volume types but different performance characteristics

| Type | GCP Name | AWS Equivalent | IOPS/GB | Throughput/GB | Max IOPS | Max Throughput | Use Case |
|------|----------|----------------|---------|---------------|----------|----------------|----------|
| **Standard PD** | `pd-standard` | gp2/st1 | N/A | N/A | 7,500 | 1,200 MB/s | Sequential workloads, big data |
| **Balanced PD** | `pd-balanced` | gp3 | 6 | 0.28 MB/s | 80,000 | 1,200 MB/s | **Most workloads (default)** |
| **SSD PD** | `pd-ssd` | io2 | 30 | 0.48 MB/s | 100,000 | 1,200 MB/s | High-performance databases |
| **Extreme PD** | `pd-extreme` | io2 Block Express | Custom | Custom | 120,000 | 2,400 MB/s | Highest performance, low latency |

**Key Differences from EBS:**
- **No separate PIOPS pricing** - performance scales with disk size
- **Can resize without detaching** (unlike most EBS)
- **No IO credits system** like gp2/gp3
- Multi-reader support built-in (read-only multi-attach)

### Disk Categories

| Category | Replication | Attaches to | Cost | Use case |
|---|---|---|---|---|
| Zonal Persistent Disk | Replicated within **single zone**. Lower latency (same zone as VM) | **Only VMs in same zone** | Lower cost than regional | Most workloads, boot disks |
| Regional Persistent Disk | Replicated across **2 zones in same region**. **Active-active replication**. Higher availability (zone failure protection) | **VMs in either replication zone** | 2x storage cost of zonal | HA databases, critical workloads |

**AWS Comparison:** EBS is always zonal; Regional PD is like EBS Multi-Attach + synchronous cross-AZ replication

### Performance Characteristics
#### IOPS (Input/Output Operations Per Second)
- **Read IOPS**: 0.75 IOPS per GB (up to max)
- **Write IOPS**: 1.5 IOPS per GB (up to max)
- **Extreme PD**: Provisioned IOPS (up to 120,000)
- **Performance scales linearly with disk size** (except Extreme)

#### Throughput
- Scales with disk size up to per-disk limits
- Also scales with number of vCPUs on VM
- ==More vCPUs = higher throughput potential==
- Per-VM limits: Depends on machine type

#### Latency
- **Single-digit millisecond latency** for SSD
- Extreme PD: <1 ms typical
- Standard PD: Higher latency (HDD)

### Disk Size Limits

| Disk type | Min size | Max size |
|---|---|---|
| Standard PD | 10 GB | 64 TB |
| Balanced PD | 10 GB | 64 TB |
| SSD PD | 10 GB | 64 TB |
| Extreme PD | 500 GB | 64 TB |

- **Boot disk minimum: 10 GB**
- **Can resize up without downtime**
- **Cannot shrink disks**

### Disk Resizing
**AWS Equivalent:** [[compute-ec2#EBS Volume|EBS Volume Modification]]
- Increase size without detaching
- **Automatically replicates additional capacity**
- Resize file system after disk resize:
  - Linux: `sudo resize2fs /dev/sdb`
  - Windows: Disk Management or `diskpart`
- **No performance impact during resize**
- **Cannot decrease size**

### Multi-Attach (Read-Only)
**AWS Equivalent:** [[compute-ec2#EBS Multi-Attach - io1/io2 family|EBS Multi-Attach]] (but different)
- Attach single disk to **multiple VMs in read-only mode**
- Up to **10 VMs** can read simultaneously
- All VMs must be in same zone (zonal) or replication zones (regional)
- Use case: Shared static data, distributed file systems
- **Cannot write from multiple VMs** (unlike EBS Multi-Attach io2)

### Snapshots
**AWS Equivalent:** [[compute-ec2#EBS Snapshots|EBS Snapshots]]
- Point-in-time backup of persistent disk
- **Incremental and automatic** (only changed blocks)
- **Global resource** - can restore to any zone/region
- Stored in [[cloud-storage|Cloud Storage]] (durable, cheap)
- **Can create disk from snapshot in any zone**
- Can create snapshots while disk is attached and in use
- VSS snapshots for Windows (application-consistent)

#### Snapshot Features
- **Snapshot schedules**: Automated daily/weekly/monthly backups
- **Snapshot retention**: Automatic deletion of old snapshots
- **Machine images**: Snapshot + VM configuration
- **Cross-region copy**: Automatically stored globally
- **Incremental forever**: Each snapshot only stores changes

#### Snapshot Best Practices
- Schedule regular snapshots for critical data
- **Snapshots are global - excellent for DR**
- Tag snapshots for organization
- Use snapshot schedules vs manual snapshots
- Clean up old snapshots to save costs

### Encryption
#### Encryption at Rest (Automatic)

| Option | Who manages keys | Notes |
|---|---|---|
| **Google-managed keys** | Google | **Default, automatic, no configuration** |
| **Customer-managed keys (CMEK)** | You, in [[security-kms|Cloud KMS]] | Regional key must match disk region. Can't convert existing disks to CMEK |
| **Customer-supplied keys (CSEK)** | You manage and provide keys | Provide key with every request. **If you lose key, data is unrecoverable** |

#### Encryption in Transit
- Automatically encrypted between VM and storage
- No configuration required

### Boot Disks vs Data Disks
#### Boot Disk
- Contains OS and boot loader
- **One per VM** (cannot have multiple boot disks)
- Can be Standard, Balanced, or SSD PD
- Default size: 10 GB (minimum for most images)
- **Auto-deleted by default when VM deleted**
- Can preserve on delete: `--no-auto-delete`

#### Data Disk
- Additional storage attached to VM
- Up to **128 disks per VM** (zonal or regional)
- Can be any disk type
- **Not auto-deleted** when VM deleted (by default)
- Can attach/detach while VM running (except boot disk)
- Can attach to another VM after detachment

### Local SSD vs Persistent Disk
**Comparison with [[compute-engine#local ssds|Local SSDs]]:**

| Feature | Persistent Disk | Local SSD |
|---------|-----------------|-----------|
| Location | Network-attached | Physically attached |
| Durability | Durable (replicated) | Ephemeral |
| Survives VM stop | ✓ Yes | No (data lost) |
| Size per disk | Up to 64 TB | 375 GB fixed |
| Max disks | 128 | 24 |
| IOPS | Up to 120,000 | Up to 2.4M |
| Multi-attach | ✓ Read-only | No |
| Snapshots | ✓ Yes | No |
| Use case | Boot, data, databases | Cache, scratch, temporary |

### Disk Performance Optimization
#### Choosing Disk Type
- **Standard PD**: Large sequential reads, big data, low cost
- **Balanced PD**: **Default choice for most workloads**
- **SSD PD**: High random IOPS, databases
- **Extreme PD**: Highest performance, low latency critical apps

#### Sizing for Performance
- ==Larger disks = better performance== (up to limits)
- Calculate required IOPS/throughput
- Size disk to meet performance needs, not just capacity
- Example: 1000 IOPS needed → Balanced PD needs ~167 GB minimum

#### VM Considerations
- ==More vCPUs = higher throughput limits==
- Machine type affects maximum disk performance
- Balance disk type and VM size
- Use [[gcp/cloud-monitoring|Cloud Monitoring]] to monitor disk utilization

### Disk Images
**AWS Equivalent:** [[compute-ec2#Amazon Machine Image (AMI)|AMI]]
- Template for creating boot disks
- Public images: Google, OS vendors, community
- Custom images: Created from your disks/snapshots
- **Images are global** - use in any region
- Can deprecate/delete custom images
- Image families: Always get latest image in family

### Machine Images
**AWS Equivalent:** [[compute-ec2#Amazon Machine Image (AMI)|AMI + Launch Template combined]]
- **Complete VM configuration** (disks, metadata, permissions)
- Includes boot disk + data disks
- Preserves machine type, labels, metadata
- Use for instance cloning, backup, DR
- Regional or global
- **Best for full VM backup/restore**

### Persistent Disk Pricing
- **Storage**: Per GB-month by disk type
  - Standard PD: Lowest
  - Balanced PD: Mid
  - SSD PD: Higher
  - Extreme PD: Highest + provisioned IOPS cost
- **Regional**: **2x cost of zonal** (replicated across 2 zones)
- **Snapshots**: Per GB-month (cheaper than disks)
  - Incremental storage only
  - Stored in [[cloud-storage|Cloud Storage]]
- **Operations**: No per-IOPS charges (unlike AWS)
- **Free tier**: 30 GB zonal Standard PD per month

### Use Cases by Disk Type

| Disk type | Use cases |
|---|---|
| Standard PD | Log files, backups, archives. Big data sequential scans. Cost-sensitive workloads |
| Balanced PD | **General purpose workloads**. Web servers, app servers. Development/test environments. Boot disks |
| SSD PD | Transactional databases (MySQL, PostgreSQL). High-performance NoSQL. Random I/O intensive apps |
| Extreme PD | SAP HANA, Oracle RAC. SQL Server with very high IOPS needs. Ultra-low latency requirements |

---

## ACE Level

### Essential gcloud Commands
```bash
# Create zonal disk
gcloud compute disks create DISK_NAME \
  --size=SIZE_GB \
  --type=DISK_TYPE \
  --zone=ZONE

# Create regional disk
gcloud compute disks create DISK_NAME \
  --size=SIZE_GB \
  --type=DISK_TYPE \
  --region=REGION \
  --replica-zones=ZONE1,ZONE2

# List disks
gcloud compute disks list

# Describe disk
gcloud compute disks describe DISK_NAME --zone=ZONE

# Resize disk
gcloud compute disks resize DISK_NAME \
  --size=NEW_SIZE_GB \
  --zone=ZONE

# Delete disk
gcloud compute disks delete DISK_NAME --zone=ZONE

# Create snapshot
gcloud compute disks snapshot DISK_NAME \
  --snapshot-names=SNAPSHOT_NAME \
  --zone=ZONE

# List snapshots
gcloud compute snapshots list

# Create disk from snapshot
gcloud compute disks create DISK_NAME \
  --source-snapshot=SNAPSHOT_NAME \
  --zone=ZONE

# Delete snapshot
gcloud compute snapshots delete SNAPSHOT_NAME

# Create snapshot schedule
gcloud compute resource-policies create snapshot-schedule POLICY_NAME \
  --region=REGION \
  --max-retention-days=DAYS \
  --on-source-disk-delete=keep-auto-snapshots \
  --daily-schedule \
  --start-time=02:00

# Attach snapshot schedule to disk
gcloud compute disks add-resource-policies DISK_NAME \
  --resource-policies=POLICY_NAME \
  --zone=ZONE

# Attach disk to VM
gcloud compute instances attach-disk INSTANCE_NAME \
  --disk=DISK_NAME \
  --zone=ZONE

# Detach disk from VM
gcloud compute instances detach-disk INSTANCE_NAME \
  --disk=DISK_NAME \
  --zone=ZONE

# Create image from disk
gcloud compute images create IMAGE_NAME \
  --source-disk=DISK_NAME \
  --source-disk-zone=ZONE

# Create machine image
gcloud compute machine-images create IMAGE_NAME \
  --source-instance=INSTANCE_NAME \
  --source-instance-zone=ZONE
```

### Disk Type Values
```bash
# Disk types for --type parameter
pd-standard     # Standard PD (HDD)
pd-balanced     # Balanced PD (SSD) - DEFAULT
pd-ssd          # SSD PD
pd-extreme      # Extreme PD
```

### Format and Mount Disk (Linux)
```bash
# After attaching disk to VM, SSH and run:

# Find the disk
lsblk

# Format disk (one-time, first use)
sudo mkfs.ext4 -m 0 -E lazy_itable_init=0,lazy_journal_init=0,discard /dev/sdb

# Mount directory
sudo mkdir -p /mnt/disks/DISK_NAME
sudo mount -o discard,defaults /dev/sdb /mnt/disks/DISK_NAME
sudo chmod a+w /mnt/disks/DISK_NAME

# Auto-mount on reboot (add to /etc/fstab)
echo UUID=$(sudo blkid -s UUID -o value /dev/sdb) /mnt/disks/DISK_NAME ext4 discard,defaults,nofail 0 2 | sudo tee -a /etc/fstab

# After resize, expand filesystem
sudo resize2fs /dev/sdb
```

### Key Concepts for ACE
- Understanding disk types and when to use each
- Creating and attaching disks to VMs
- Resizing disks without downtime
- Creating and managing snapshots for backups
- Setting up snapshot schedules for automated backups
- Creating images and machine images
- Formatting and mounting disks in Linux
- Understanding zonal vs regional disks
- Encryption options (Google-managed, CMEK, CSEK)
- Monitoring disk performance with [[gcp/cloud-monitoring|Cloud Monitoring]]

---

## PCA Level

### Architectural Considerations
#### High Availability
- **Regional Persistent Disks**: Automatic cross-zone replication
  - **Active-active: both copies always accessible**
  - Automatic failover to other zone
  - 2x cost, but no downtime on zone failure
- **Snapshots**: Regular backups for disaster recovery
  - Global resource, restore anywhere
  - Automated snapshot schedules
- **Machine Images**: Full VM configuration backup
  - Faster recovery than snapshots + manual config

#### Disaster Recovery
- **RTO/RPO Planning**:
  - Snapshots: Low cost, higher RPO (schedule-dependent)
  - Regional PD: Higher cost, near-zero RPO/RTO
  - Cross-region snapshots: Geographic DR
- **Recovery Strategies**:
  - Pilot light: Snapshots + scripts to recreate
  - Warm standby: Regional PD + failover
  - Hot standby: Regional PD + Regional MIG
- **Backup Testing**: Regularly test snapshot restore process

### Performance Architecture
#### Database Performance
- **Sizing methodology**:
  1. Estimate required IOPS/throughput
  2. Calculate minimum disk size for performance
  3. Choose appropriate disk type
  4. Monitor and adjust
- **Example**: MySQL needs 10,000 IOPS
  - Balanced PD: 10,000 / 6 = ~1,667 GB minimum
  - SSD PD: 10,000 / 30 = ~334 GB minimum
  - Consider cost vs capacity trade-off

#### Multi-Disk Striping
- **Not recommended in GCP** (unlike AWS)
- Single large disk often better than multiple small
- Exceptions:
  - Need >64 TB (stripe multiple 64 TB disks)
  - Need >120,000 IOPS (multiple Extreme disks)
- Use RAID 0 for striping (performance), RAID 1 for mirroring (redundancy)

#### Performance Monitoring
- [[gcp/cloud-monitoring|Cloud Monitoring]] metrics (see the table below)
- Set alerts for throttling
- Right-size based on actual usage

| Metric | Measures |
|---|---|
| `disk.read_bytes_count` | Read throughput |
| `disk.write_bytes_count` | Write throughput |
| `disk.read_ops_count` | Read IOPS |
| `disk.write_ops_count` | Write IOPS |
| `disk.throttled_read_ops_count` | Throttled operations |

### Cost Optimization
#### Disk Type Selection
- **Over-provisioning**: Size for performance, accept higher capacity cost
- **Monitoring**: Downsize if consistently underutilized

**Decision matrix:**

| Workload | Disk type |
|---|---|
| Sequential I/O, cost-sensitive | Standard PD |
| General purpose | Balanced PD |
| High IOPS database | SSD PD |
| Ultra-high IOPS | Extreme PD |

#### Regional vs Zonal
- Zonal: 50% cost of regional
- Use zonal unless:
  - Need zone failure protection
  - Running HA database
  - Critical workload requiring near-zero downtime
- Alternative: Zonal + frequent snapshots (lower cost, higher RPO)

#### Snapshot Management
- **Retention policies**: Delete old snapshots automatically
- **Incremental storage**: Only pay for changed blocks
- **Snapshot location**: Stored globally in [[cloud-storage|Cloud Storage]]
- **Cost**: ~$0.026/GB-month (cheaper than disk storage)
- Clean up snapshots no longer needed for recovery

#### Committed Use Discounts
- 1 or 3 year commitment
- Up to **70% discount** on persistent disk
- Purchase in GB increments
- Applies to all disks of same type in region

### Security Best Practices
#### Encryption
- **Default**: Google-managed encryption (no effort)
- **CMEK**: When audit requirements or key rotation needed
  - Centralized key management
  - Audit key usage via [[gcp/cloud-logging|Cloud Logging]]
  - Can disable/revoke keys
- **CSEK**: Only for regulatory requirement to control keys
  - High operational overhead
  - ==Risk: Lost key = lost data==

#### Access Control
- **IAM roles**:
  - `roles/compute.storageAdmin`: Full disk management
  - `roles/compute.instanceAdmin.v1`: Attach/detach disks
- **Service accounts**: Minimal permissions
- **Snapshot access**: Separate permissions for snapshot creation/deletion
- **Organization policies**:
  - Enforce CMEK encryption
  - Restrict allowed disk types
  - Require deletion protection

### Migration Strategies
#### From AWS EBS
- **Method 1**: Import machine image
  - Export AWS AMI
  - Upload to [[cloud-storage|Cloud Storage]]
  - Import as GCP image
- **Method 2**: Migrate for Compute Engine
  - Automated migration tool
  - Minimal downtime
- **Performance mapping**: see the table below

| AWS type | GCP type |
|---|---|
| gp2/gp3 | pd-balanced |
| io1/io2 | pd-ssd or pd-extreme |
| st1/sc1 | pd-standard |

#### From On-Premises
- **Small (<1 TB)**: Upload disk image to Cloud Storage, import
- **Large**: Physical Transfer Appliance
- **Continuous replication**: Migrate for Compute Engine

### Advanced Features
#### Disk Sharing Patterns
- **Read-only multi-attach**:
  - Shared reference data across VMs
  - Static content serving
  - Distributed caching tier
- **Limitations**:
  - **Cannot write from multiple VMs**
  - All VMs must be in same zone (zonal) or replica zones (regional)
  - Use [[filestore|Filestore]] for read-write sharing

#### Asynchronous Replication
- Not built-in (unlike AWS EBS with cross-region snapshots)
- Implement via:
  - Scheduled snapshots + cross-region restore
  - Application-level replication
  - Database native replication

#### Persistent Disk CSI Driver
- For [[gke|GKE]] workloads
- Kubernetes-native disk provisioning
- StorageClass for automatic provisioning
- Volume snapshots via VolumeSnapshot API
- Regional PD support for HA stateful apps

### Persistent Disk vs Alternatives

| Requirement | Persistent Disk | [[cloud-storage|Cloud Storage]] | [[filestore|Filestore]] | Local SSD |
|-------------|-----------------|-----------------|----------|-----------|
| Type | Block | Object | File (NFS) | Block |
| Durability | 5-6 nines | 11 nines | 5-6 nines | Ephemeral |
| Shared access | Read-only | ✓ Unlimited | ✓ Multiple VMs | No |
| Max IOPS | 120,000 | Lower | 100,000+ | 2.4M |
| Latency | Single-digit ms | Higher | Single-digit ms | <1 ms |
| Use case | VM disks, databases | Unstructured data | Shared files | Cache, scratch |

### Well-Architected Considerations
- **Operational Excellence**:
  - Automated snapshot schedules
  - Machine images for full backup
  - Monitoring disk performance and utilization
- **Reliability**:
  - Regional PD for zone failure protection
  - Regular snapshots for data recovery
  - Snapshot testing for verified backups
- **Security**:
  - Encryption at rest (default)
  - CMEK for compliance requirements
  - IAM-based access control
  - Audit logging enabled
- **Performance**:
  - Right disk type for workload
  - Size for performance requirements
  - Monitor for throttling
  - Multiple disks for extreme performance
- **Cost**:
  - Appropriate disk type (don't over-provision)
  - Zonal vs regional trade-off
  - Snapshot lifecycle management
  - Committed use discounts for predictable workloads
  - Delete unused disks
- **Sustainability**:
  - Right-size disks (avoid over-provisioning)
  - Clean up unused disks and snapshots
  - Use Standard PD where performance allows
