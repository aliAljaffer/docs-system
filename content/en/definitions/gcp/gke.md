---
title: Gke
category: GCP
description: 'GCP note: Gke.'
tags:
- gcp
- compute
---


# Gke

`gcp` `compute`

## Google Kubernetes Engine (GKE)
**Managed Kubernetes** service for containerized applications

**AWS Equivalent:** [[containers-eks|EKS]]

### GKE Cluster Modes
#### Autopilot Mode (Recommended)
- **Fully managed**: Google manages nodes, node pools, and infrastructure
- **Per-pod billing** (not per-node)
- Automatic scaling, security, and operations
- **Opinionated configuration** following GKE best practices
- **No node management required**
- Higher pod resource efficiency
- Cannot SSH into nodes
- Some restrictions (DaemonSets, privileged containers require specific config)

#### Standard Mode
- **More control**: You manage nodes and node pools
- Per-node billing
- Can customize node OS, machine types, GPUs
- Can run DaemonSets, privileged containers freely
- More configuration options but more operational overhead

### Cluster Types

| Type | Control plane | SLA | Nodes | Notes |
|---|---|---|---|---|
| Zonal | Single control plane in one zone | 99.5% | Single zone (default) or multiple zones | Cheapest option, control plane downtime during upgrades |
| Regional (**recommended for production**) | **Replicated across 3 zones** | **99.95%** | Distributed across multiple zones | Higher availability, no control plane downtime, ~3x cost of zonal for control plane |
| Private | Private or public endpoint | - | Only private IP addresses | Improved security, no direct internet access, requires [[gcp/cloud-nat|Cloud NAT]] for outbound traffic |

### Node Pools
- Group of nodes within a cluster with same configuration
- Each node pool can have different machine types, disk sizes
- Can add/remove node pools without affecting cluster
- Autoscaling per node pool
- Use cases: Separate workload types (CPU vs GPU), cost optimization

### GKE Autopilot vs Standard Comparison

| Feature | Autopilot | Standard |
|---------|-----------|----------|
| Node management | Google manages | You manage |
| Billing | Per pod | Per node |
| Scaling | Automatic | Configure autoscaling |
| Security | Hardened by default | You configure |
| Best for | Hands-off, cost-optimized | Control, customization |

### Cluster Autoscaling
**Node Autoscaling (Standard mode)**
- Automatically adds/removes nodes based on pod resource requests
- Per node pool configuration
- Scale up: When pods are unschedulable
- Scale down: When nodes are underutilized

**Vertical Pod Autoscaling (VPA)**
- Automatically adjusts CPU/memory requests based on usage
- Learns from historical resource consumption
- Can run in recommendation mode (no auto-update)

**Horizontal Pod Autoscaling (HPA)**
- Scales number of pod replicas based on metrics
- CPU, memory, custom metrics from [[gcp/cloud-monitoring|Cloud Monitoring]]
- Native Kubernetes feature

### Workload Identity
**AWS Equivalent:** IRSA (IAM Roles for Service Accounts)
- **Recommended way to access Google Cloud services from GKE**
- Maps Kubernetes Service Accounts to [[gcp/iam|Google Service Accounts]]
- No need to store credentials in pods
- Fine-grained [[gcp/iam|IAM]] access control

```bash
# Enable Workload Identity on cluster
gcloud container clusters update CLUSTER --workload-pool=PROJECT_ID.svc.id.goog

# Link K8s SA to Google SA
gcloud iam service-accounts add-iam-policy-binding GSA@PROJECT.iam.gserviceaccount.com \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:PROJECT.svc.id.goog[K8S_NAMESPACE/K8S_SA]"
```

### GKE Networking Modes
#### VPC-Native (IP Aliasing) - **Recommended**
- Pods get IPs from [[gcp/vpc|VPC]] subnet ranges
- **Better integration with Google Cloud services**
- Required for [[gcp/private-google-access-vs-psc#Private Google Access (PGA)|Private Google Access]], [[gcp/vpc-service-controls|VPC Service Controls]]
- Required for [[gcp/vpc#shared vpc|Shared VPC]]
- Pods are routable within VPC

#### Routes-Based (Legacy)
- Pods get IPs from non-VPC range
- Uses routes for pod networking
- Less efficient IP usage
- Not recommended for new clusters

### GKE Release Channels

| Channel | Characteristics |
|---|---|
| **Rapid** | Cutting-edge features, frequent updates, less stable |
| **Regular** | Balanced, **default and recommended** |
| **Stable** | Production-ready, tested features, infrequent updates |
| **No channel** | Manual version management |

### GKE Sandbox
- Runs pods in isolated sandboxes using gVisor
- **Second layer of defense beyond container isolation**
- Use cases: Untrusted code, multi-tenant workloads
- Performance overhead (~10-15%)

### Binary Authorization
- Deploy-time security control
- Enforces that only trusted container images are deployed
- Integrates with [[gcp/artifact-registry|Artifact Registry]], Container Analysis
- Attestation-based policy enforcement
- See [[gcp/binary-authorization|Binary Authorization]] for details

### Config Connector
- Manage Google Cloud resources using Kubernetes manifests
- Declarative resource management
- GitOps workflows for infrastructure
- Example: Create [[gcp/cloud-sql|Cloud SQL]] instance via K8s manifest

### Multi-Cluster Management
#### GKE Enterprise (formerly Anthos)
- Unified management for GKE clusters
- Multi-cluster and multi-cloud
- Config Management, Service Mesh, Policy Controller
- Additional cost per vCPU

#### GKE Hub (Connect)
- Register external K8s clusters
- Unified view of all clusters
- Free for GKE clusters, costs for external clusters

### Maintenance Windows
- Control when cluster/node upgrades happen
- Exclusions: Block upgrades during critical periods
- Maintenance windows: Specify allowed time windows
- **Regional clusters: Rolling upgrades, no downtime**

### Cost Optimization
- **Autopilot**: Pay only for requested pod resources
- **[[compute-engine#preemptible & spot vms|Spot nodes]]**: Up to 91% discount, for fault-tolerant workloads
- **Cluster autoscaler**: Scale down unused nodes
- **Bin packing**: Efficient pod placement to minimize nodes
- **[[compute-engine#committed use discounts (cud)|Committed Use Discounts]]**: 1 or 3 year, applies to GKE nodes

---

## ACE Level

### Essential kubectl Commands
```bash
# Connect to cluster
gcloud container clusters get-credentials CLUSTER_NAME --zone=ZONE

# View cluster info
kubectl cluster-info
kubectl get nodes
kubectl get pods --all-namespaces

# Deploy application
kubectl create deployment nginx --image=nginx
kubectl expose deployment nginx --port=80 --type=LoadBalancer

# Scale deployment
kubectl scale deployment nginx --replicas=3

# View services
kubectl get services

# View logs
kubectl logs POD_NAME

# Exec into pod
kubectl exec -it POD_NAME -- /bin/bash

# Delete resources
kubectl delete deployment nginx
kubectl delete service nginx
```

### Essential gcloud Commands
```bash
# Create cluster (Autopilot)
gcloud container clusters create-auto CLUSTER_NAME --region=REGION

# Create cluster (Standard)
gcloud container clusters create CLUSTER_NAME \
  --zone=ZONE \
  --num-nodes=3 \
  --machine-type=e2-medium

# List clusters
gcloud container clusters list

# Describe cluster
gcloud container clusters describe CLUSTER_NAME --zone=ZONE

# Delete cluster
gcloud container clusters delete CLUSTER_NAME --zone=ZONE

# Resize node pool
gcloud container clusters resize CLUSTER_NAME --num-nodes=5 --zone=ZONE

# Enable autoscaling
gcloud container clusters update CLUSTER_NAME \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=10 \
  --zone=ZONE
```

### Key Concepts for ACE
- Creating and managing GKE clusters (Autopilot vs Standard)
- Deploying containerized applications to GKE
- Understanding Kubernetes objects: Pods, Deployments, Services
- Configuring autoscaling (HPA and cluster autoscaling)
- Viewing cluster and workload inventory
- Working with [[gcp/artifact-registry|Artifact Registry]] for container images
- Basic kubectl operations
- Connecting to clusters with `gcloud container clusters get-credentials`

---

## PCA Level

### Architectural Patterns
#### Stateless Applications
- Deploy with Deployments
- Use [[gcp/cloud-load-balancing|Cloud Load Balancing]] for ingress
- Horizontal scaling with HPA
- Store state in external services ([[gcp/cloud-sql|Cloud SQL]], [[gcp/firestore|Firestore]], [[gcp/cloud-storage|Cloud Storage]])
#### Stateful Applications
- Use StatefulSets
- [[gcp/persistent-disk|Persistent Disks]] for storage
- Consider [[gcp/filestore|Filestore]] for shared storage
- Backup strategies for stateful data
#### Batch Processing
- Use Jobs or CronJobs
- [[compute-engine#preemptible & spot vms|Spot nodes]] for cost savings
- Resource requests/limits to ensure scheduling
- Consider [[cloud-run#Cloud Run Services vs Jobs|Cloud Run Jobs]] for simpler use cases

### Multi-Tenancy Strategies
- **Namespace isolation**: Soft multi-tenancy
- **Node pools**: Dedicated nodes per tenant
- **GKE Sandbox**: gVisor for stronger isolation
- **Separate clusters**: Strongest isolation, higher cost
- **Network Policies**: Control pod-to-pod communication
### High Availability Design
- **Regional clusters** for control plane HA
- **Multi-zone node pools** for workload HA
- Pod Disruption Budgets (PDB) to maintain availability during updates
- Readiness and liveness probes
- Anti-affinity rules to spread pods across nodes/zones
### Security Best Practices
- **Workload Identity** for cloud service access
- **[[gcp/binary-authorization|Binary Authorization]]** for image verification
- **GKE Sandbox** for untrusted workloads
- **Private clusters** with authorized networks
- **[[gcp/vpc-service-controls|VPC Service Controls]]** for data exfiltration prevention
- **[[compute-engine#shielded vms|Shielded]] GKE nodes** (default)
- **Pod Security Standards** (Restricted, Baseline, Privileged)

### Cost Optimization Strategies
- **Autopilot** for optimal resource utilization
- **[[compute-engine#preemptible & spot vms|Spot nodes]]** for fault-tolerant workloads (up to 91% savings)
- **Cluster autoscaler** to scale nodes based on demand
- **VPA** for rightsizing pod requests
- **[[compute-engine#committed use discounts (cud)|Committed Use Discounts]]** for predictable workloads
- **Bin packing**: Set appropriate resource requests/limits
- **[[compute-engine#preemptible & spot vms|Preemptible nodes]]** in Standard mode

### Observability
- [[gcp/cloud-monitoring|Cloud Monitoring]] for metrics
- [[gcp/cloud-logging|Cloud Logging]] for logs
- GKE Dashboard in Cloud Console
- [[gcp/cloud-trace|Cloud Trace]] for distributed tracing
- Prometheus integration via Managed Service for Prometheus

### CI/CD Integration
- [[gcp/cloud-build|Cloud Build]] for container image building
- [[gcp/artifact-registry|Artifact Registry]] for image storage
- [Cloud Deploy](https://cloud.google.com/deploy) for deployment pipelines
- [[gcp/binary-authorization|Binary Authorization]] for security gates
- GitOps with Config Sync

### Networking Considerations
- **VPC-native clusters** for better integration
- **Network policies** for pod-to-pod security
- **Ingress controllers**: GKE Ingress ([[gcp/cloud-load-balancing#http(s) load balancing|HTTP(S) Load Balancer]]), NGINX, Istio
- **Service mesh**: Anthos Service Mesh for mTLS, traffic management
- **Pod IP address ranges**: Plan carefully to avoid IP exhaustion

### Migration to GKE
- Migrate for Anthos: Automated migration from [[compute-engine|VMs]] to containers
- Multi-cluster migration strategies
- Stateful workload migration considerations
- Testing in non-production clusters first

### Well-Architected Considerations
- **Operational Excellence**: Automated upgrades via release channels, Config Sync
- **Reliability**: Regional clusters, PDBs, health checks, multi-zone node pools
- **Security**: Workload Identity, [[gcp/binary-authorization|Binary Authorization]], private clusters, least privilege
- **Performance**: Appropriate machine types, GPUs for ML, local SSDs for high I/O
- **Cost**: Autopilot, [[compute-engine#preemptible & spot vms|Spot nodes]], autoscaling, rightsizing
- **Sustainability**: Efficient resource utilization, carbon-aware scheduling
