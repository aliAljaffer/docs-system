---
title: compute-engine
category: GCP
description: 'GCP note: Compute-engine.'
tags:
- gcp
- compute
---


# compute-engine

## Compute Engine
**IaaS** (infrastructure as a service) - virtual machines running in Google's data centers

**AWS Equivalent:** [[compute-ec2|EC2]]

### Machine Types
#### Predefined Machine Types
- **General Purpose (E2, N2, N2D, N1)**
  - E2: Cost-optimized, burstable, 0.25-32 vCPUs
  - N2: Balanced price/performance, Intel Cascade Lake, up to 128 vCPUs
  - N2D: AMD EPYC, better price/performance than N2
  - N1: Previous generation, still supported
- **Compute-Optimized (C2, C2D, C3)**
  - Highest performance per core
  - HPC, gaming servers, CPU-intensive workloads
  - C2: Intel Cascade Lake, up to 60 vCPUs
  - C2D: AMD EPYC Milan, better value
  - C3: Intel Sapphire Rapids, latest gen
- **Memory-Optimized (M1, M2, M3)**
  - High memory-to-vCPU ratios
  - In-memory databases, SAP HANA
  - M3: up to 14 TB of memory
- **Accelerator-Optimized (A2, G2)**
  - GPU-attached instances
  - ML training, inference, video processing
  - A2: NVIDIA A100 GPUs
  - G2: NVIDIA L4 GPUs

#### Custom Machine Types
- Create VMs with specific vCPU and memory combinations
- Must be between 0.9 GB and 8 GB per vCPU (or up to 6.5 GB for E2)
- **Costs more than predefined but better resource optimization**

### Machine Images vs. Images vs. Snapshots
| Resource | Contains | AWS equivalent |
|----------|----------|----------------|
| **Image** | Boot disk only, OS and software | AMI |
| **Snapshot** | Point-in-time copy of [[gcp/persistent-disk|Persistent Disk]], incremental | EBS Snapshot |
| **Machine Image** | Complete VM config (disks, metadata, permissions, instance properties). Best for instance cloning and backups. Can include multiple disks | AMI + complete instance config |

### Instance Lifecycle
- **Provisioning** → **Staging** → **Running** → **Stopping** → **Terminated**

| State | Behavior |
|-------|----------|
| **Suspended** | Preserves VM state (RAM), fast resume, charged for storage |
| **Stopped** | Preserves disks only, no RAM state |
| **Preemptible/Spot** | Can be terminated any time |

### Preemptible & Spot VMs
**AWS Equivalent:** [[compute-ec2#ec2 spot instance requests|EC2 Spot Instances]]
- **Up to 91% discount** compared to on-demand
- **Preemptible**: Max 24 hours, legacy option
- **Spot**: No max runtime, better than preemptible
- Can be terminated with 30-second warning
- No SLA, no live migrate
- Use cases: Batch jobs, fault-tolerant workloads, rendering

### Persistent Disks
See [[gcp/persistent-disk|Persistent Disk]] for full details

**AWS Equivalent:** [[storage-ebs|EBS]]
- Network-attached storage, **survives VM termination**
- Standard (HDD), Balanced (SSD), Performance (SSD), Extreme (SSD)
- **Can attach to multiple VMs in read-only mode**
- **Can resize without downtime**
- Zonal or Regional (replicated across 2 zones in same region)
- **Snapshots**: Incremental, global resource, can create across regions

### Local SSDs
**AWS Equivalent:** [[compute-ec2#ec2 instance store|EC2 Instance Store]]
- Physically attached to the server
- **375 GB per device, up to 24 devices (9 TB total)**
- **Ephemeral - data lost on VM stop/terminate**
- Very high IOPS and low latency
- Use cases: Scratch disk, cache, temporary storage

### Instance Groups
#### Managed Instance Groups (MIG)
**AWS Equivalent:** [[management-and-governance-auto-scaling|Auto Scaling Groups]]
- Identical VMs created from instance template
- **Autoscaling**: CPU, load balancing, custom metrics from [[gcp/cloud-monitoring|Cloud Monitoring]], schedules
- **Auto-healing**: Health checks, automatic recreation
- **Regional MIGs**: Multi-zone for high availability (**recommended**)
- **Zonal MIGs**: Single zone
- **Stateful MIGs**: Preserve instance names, disks, metadata

#### Unmanaged Instance Groups
- Heterogeneous VMs
- Manual management, no autoscaling
- Use case: When you need to load balance dissimilar instances

### Shielded VMs
- **Secure Boot**: Only signed OS images
- **vTPM**: Virtual Trusted Platform Module
- **Integrity Monitoring**: Detects rootkits, bootkit attacks
- **Default on for most images**

### Confidential VMs
- Encrypts data in-use (not just at-rest and in-transit)
- Uses AMD SEV (Secure Encrypted Virtualization)
- N2D machine types only
- Use cases: Sensitive data processing, regulatory compliance

### Sole-Tenant Nodes
**AWS Equivalent:** [[compute-ec2#ec2 instances purchasing options|Dedicated Hosts]]
- Physical Compute Engine server dedicated to your project
- Use cases: BYOL, compliance, performance isolation
- Can specify node affinity (which node a VM runs on)

### Live Migration
- Migrate running VMs between hosts with **zero downtime**
- Triggered by: Maintenance, hardware failure, datacenter needs
- **Not available** for Preemptible/Spot VMs, GPUs, local SSDs (in some cases)
- **AWS doesn't have this** - AWS stops/starts instances during maintenance

### OS Login
- Manage SSH access using [[gcp/iam|IAM]]
- No need to manage SSH keys manually
- OS Login 2FA available
- **Best practice for SSH access control**

### Metadata Server
- `http://metadata.google.internal/computeMetadata/v1/`
- Query instance metadata, project metadata
- Get access tokens for [[gcp/iam#service accounts|service accounts]]
- Similar to AWS Instance Metadata Service

### Startup Scripts & Metadata
**AWS Equivalent:** [[compute-ec2#automating boot tasks|EC2 User Data]]
- Run scripts on VM boot
- Can be in metadata or [[gcp/cloud-storage|Cloud Storage]]
- Keys: `startup-script`, `shutdown-script`

### Snapshots
- Point-in-time copies of [[gcp/persistent-disk|Persistent Disks]]
- Incremental (only changed data after first snapshot)
- Global resource (can be used across regions)
- Use for backups and disaster recovery
- Can schedule automatic snapshots
- Can create disk from snapshot in any region

### Committed Use Discounts (CUD)
- 1-year or 3-year commitment
- **Up to 57% discount** compared to on-demand
- Applied automatically to matching usage
- Types:
  - **Spend-based**: Commit to minimum spend
  - **Resource-based**: Commit to specific machine types/regions
- Can be sold in secondary market if not needed

### Pricing
| Option | Discount | Condition |
|--------|----------|-----------|
| **On-Demand** | - | Per-second billing (min 1 min) |
| **Committed Use Discounts** | **Up to 57%** | 1 or 3 year |
| **Sustained Use Discounts** | Up to 30% | Automatic, for running >25% of month |
| **Preemptible/Spot** | Up to 91% | - |
| **Free Tier** | - | 1 f1-micro instance per month (us-west1, us-central1, us-east1) |

---

## ACE Level

### Essential gcloud Commands
```bash
# Create instance
gcloud compute instances create INSTANCE_NAME \
  --zone=ZONE \
  --machine-type=MACHINE_TYPE \
  --image-family=IMAGE_FAMILY \
  --image-project=IMAGE_PROJECT

# List instances
gcloud compute instances list

# Start/stop instances
gcloud compute instances start INSTANCE_NAME
gcloud compute instances stop INSTANCE_NAME

# Delete instance
gcloud compute instances delete INSTANCE_NAME

# SSH into instance
gcloud compute ssh INSTANCE_NAME --zone=ZONE

# Create instance template
gcloud compute instance-templates create TEMPLATE_NAME

# Create managed instance group
gcloud compute instance-groups managed create GROUP_NAME \
  --base-instance-name=BASE_NAME \
  --template=TEMPLATE_NAME \
  --size=SIZE

# Set autoscaling
gcloud compute instance-groups managed set-autoscaling GROUP_NAME \
  --max-num-replicas=MAX \
  --min-num-replicas=MIN \
  --target-cpu-utilization=0.75

# Create snapshot
gcloud compute disks snapshot DISK_NAME \
  --snapshot-names=SNAPSHOT_NAME \
  --zone=ZONE

# Create disk from snapshot
gcloud compute disks create DISK_NAME \
  --source-snapshot=SNAPSHOT_NAME \
  --zone=ZONE
```

### Key Concepts for ACE
- Creating and managing VM instances
- Choosing appropriate machine types
- Working with instance templates and MIGs
- Configuring autoscaling and auto-healing
- Managing disks (attach, detach, snapshot)
- Using startup scripts
- Basic networking ([[gcp/vpc|VPC]], firewall rules)
- OS Login for SSH access
- Viewing instance inventory and logs

---

## PCA Level

### Architectural Considerations
- **High Availability**: Regional MIGs across multiple zones
- **Disaster Recovery**: Cross-region snapshots and images
- **Cost Optimization**:
  - Rightsizing using [[gcp/cloud-monitoring|Cloud Monitoring]] recommendations
  - Committed Use Discounts for predictable workloads
  - Preemptible/Spot for fault-tolerant batch processing
  - Custom machine types to avoid over-provisioning
- **Performance**:
  - Placement policies for low-latency workloads
  - Local SSDs for high IOPS requirements
  - Network tier selection (Premium vs Standard)
- **Security**:
  - Shielded VMs for secure boot
  - Confidential VMs for data encryption in-use
  - [[gcp/iam#service accounts|Service accounts]] with minimal permissions
  - [[gcp/vpc-service-controls|VPC Service Controls]] for data exfiltration prevention

### Migration Strategies
- **Lift and Shift**: Machine Images, import from AWS/Azure
- **Migrate for Compute Engine**: Automated VM migration from on-prem/other clouds
- **Containerization**: Migrate from VMs to [[gke|GKE]] or [[cloud-run|Cloud Run]]

### Capacity Planning
- Regional vs Zonal placement
- Quota management and increase requests
- Resource reservations for guaranteed capacity
- Committed Use Discounts planning (1yr vs 3yr)

### Placement Policies
- **Compact**: Pack VMs close together (low-latency)
- **Spread**: Distribute VMs across different hardware (fault isolation)
- Use with MIGs for optimal placement

### Advanced MIG Features
- **Rolling Updates**: Gradual instance template updates with canary deployments
- **Stateful Configuration**: Preserve specific disks, instance names, metadata
- **Autohealing Policies**: Custom health check intervals and grace periods
- **Update Policies**: Control rollout (opportunistic, proactive, max surge, max unavailable)

### Sole-Tenant Node Architectures
- Node templates and node groups
- Node affinity labels
- License optimization (BYOL)
- Workload isolation for compliance

### Integration Patterns
- **Load Balancing**: [[gcp/cloud-load-balancing|Cloud Load Balancing]] with MIGs
- **Storage**: [[gcp/persistent-disk|Persistent Disk]], [[gcp/filestore|Filestore]], [[gcp/cloud-storage|Cloud Storage]]
- **Databases**: [[gcp/cloud-sql|Cloud SQL]], [[gcp/cloud-spanner|Cloud Spanner]] for persistent data
- **Networking**: [[gcp/vpc|VPC]], [[gcp/cloud-vpn|Cloud VPN]], [[gcp/cloud-interconnect|Cloud Interconnect]]
- **Monitoring**: [[gcp/cloud-monitoring|Cloud Monitoring]], [[gcp/cloud-logging|Cloud Logging]]

### Well-Architected Considerations
- **Operational Excellence**: Automated patching, OS image management, [[gcp/cloud-monitoring|monitoring]]
- **Reliability**: Multi-zone/region deployment, health checks, backups, live migration
- **Security**: Least privilege [[gcp/iam|IAM]], Shielded VMs, encryption at-rest and in-transit
- **Performance**: Right machine type, local SSD, network throughput optimization
- **Cost**: Sustained use, committed use, preemptible VMs, rightsizing
- **Sustainability**: Choose efficient machine types, rightsize to reduce carbon footprint
