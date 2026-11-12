---
title: Private-google-access-vs-psc
category: GCP
description: 1. Private Google Access = Simple, free, uses Google public IPs
tags:
- gcp
- networking
---


# Private-google-access-vs-psc

`gcp` `networking`

Private Google Access lets virtual machine (VM) instances with only private IP addresses reach Google APIs, and you enable it per subnet. Private Service Connect creates a private endpoint with an IP address from your own Virtual Private Cloud (VPC) to reach services.

## Private Google Access vs Private Service Connect
**Critical distinction** for PCA exam - know when to use each

---

## Quick Comparison

| Feature | Private Google Access | Private Service Connect |
|---------|----------------------|------------------------|
| **Purpose** | Access Google APIs without external IP | Private consumption of services with VPC IPs |
| **IP Addresses Used** | **Google's public IPs** (199.36.153.8/30) | **Your VPC private IPs** (RFC 1918) |
| **Scope** | Subnet-level | Endpoint-level |
| **Configuration** | Simple toggle on subnet | Create PSC endpoint |
| **Cost** | **Free** | Endpoint charges (~$0.01/hour) |
| **Traffic Path** | Google network (not internet) | Direct VPC routing |
| **DNS** | Uses public DNS names | Uses private DNS names or IPs |
| **Use Cases** | VMs without external IPs accessing Google services | Consuming services as if in your VPC |
| **Introduced** | 2016 (older) | 2021 (newer, more advanced) |

---

## Private Google Access (PGA)

### What It Is
- Allows instances with **only private IP addresses** to reach Google APIs
- Enabled per **subnet**
- Traffic stays on Google's network (doesn't traverse public internet)
- Uses Google's **public IP ranges** but routes through Google backbone

### How It Works
```text
VM (private IP only) → VPC Subnet (PGA enabled)
                    → Google's public IP (199.36.153.8/30)
                    → Google API (storage.googleapis.com)
                    → Response back to VM
```

### Configuration
```bash
# Enable on subnet
gcloud compute networks subnets update SUBNET \
  --region=REGION \
  --enable-private-ip-google-access

# VM accesses Cloud Storage normally
gsutil cp file.txt gs://bucket/  # Works even without external IP!
```

### DNS Resolution
```text
storage.googleapis.com → 199.36.153.8/30 (Google's public IP range)
bigquery.googleapis.com → 199.36.153.8/30
```

### Use Cases
- **[[gcp/gke|GKE private clusters]]** accessing Google services
- **[[gcp/compute-engine|Compute Engine]] VMs without external IPs** reading from [[gcp/cloud-storage|Cloud Storage]]
- **Data processing** ([[gcp/dataflow|Dataflow]], Dataproc) accessing [[bigquery|BigQuery]]
- **Cost savings** (no [[cloud-nat|NAT Gateway]] needed for Google API access)
- **Security** (no internet exposure)

### Limitations
- ✗ Still uses Google's **public IP addresses** (might conflict with firewall rules expecting private IPs)
- ✗ Doesn't work for third-party services
- ✗ Can't customize the IP addresses used
- ✗ Less control over traffic routing

### Pricing
**Completely free**

---

## Private Service Connect (PSC)

### What It Is
- **Newer, more advanced** private connectivity solution
- Consumes services using **private IP addresses from your VPC**
- Creates **endpoints** in your VPC
- Services appear as if they're running **inside your VPC**

### Types of PSC

#### 1. PSC for Google APIs
**Replaces/enhances Private Google Access**
```text
VM (private IP) → PSC Endpoint (10.0.0.5 in your VPC)
               → Private connection to Google API
               → Cloud Storage, BigQuery, etc.
```

**Benefits over PGA:**
- Uses **VPC private IPs** instead of Google public IPs
- More compatible with on-prem firewalls (RFC 1918 ranges)
- Better for hybrid environments
- More control over DNS

#### 2. PSC for Published Services
**Connect to third-party services privately**
```text
Your VPC → PSC Endpoint → Partner's service in Service Directory
                       → (e.g., Confluent Kafka, MongoDB Atlas)
```

**Use case:** Consume SaaS services as if they're in your VPC

#### 3. PSC for Service Producers
**Publish your own services**
```text
Your service in VPC A → PSC Published
                     → Consumed from VPC B via endpoint
                     → No VPC Peering needed!
```

**Use case:** Share services across VPCs/organizations without peering

### How PSC for Google APIs Works

#### Setup
```bash
# 1. Reserve internal IP address for endpoint
gcloud compute addresses create psc-endpoint-ip \
  --region=us-central1 \
  --subnet=my-subnet \
  --addresses=10.0.1.5

# 2. Create PSC endpoint for all Google APIs
gcloud compute forwarding-rules create psc-endpoint \
  --region=us-central1 \
  --network=my-vpc \
  --address=psc-endpoint-ip \
  --target-google-apis-bundle=all-apis

# 3. Configure DNS (Private DNS zone)
# Create private zone for *.googleapis.com
# Point to PSC endpoint IP (10.0.1.5)
```

#### DNS Resolution (After PSC)
```text
storage.googleapis.com → 10.0.1.5 (YOUR VPC private IP!)
bigquery.googleapis.com → 10.0.1.5
```

### Use Cases
- **Hybrid cloud** with strict firewall rules (only allow RFC 1918)
- **Multi-region** private access to Google APIs
- **Service mesh** architectures
- **Consuming third-party SaaS** privately
- **Publishing services** across VPCs without peering
- **Replacing VPC Peering** for service sharing (more scalable)

### Pricing
- **PSC Endpoint**: ~$0.01 per hour per endpoint
- **Data processing**: $0.01 per GB (ingress/egress through endpoint)
- More expensive than PGA but provides more control

---

## When to Use Each

### Use Private Google Access When:

- Simple use case: VMs accessing Google APIs
- Cost is a concern (PGA is free)
- You're okay with Google's public IP ranges
- Single VPC, single region scenario
- Quick setup needed

**Example Scenario:**
> "GKE private cluster needs to pull container images from Artifact Registry"
> **Solution:** Enable Private Google Access on subnet ✓

### Use Private Service Connect When:

- Need **private IPs (RFC 1918)** for Google APIs
- Hybrid cloud with strict on-prem firewall rules
- Consuming third-party services from Service Directory
- Multi-region private access requirements
- Publishing your own services for private consumption
- Replacing VPC Peering (more scalable alternative)
- Advanced routing control needed

**Example Scenario:**
> "On-premises network has firewall rules that only allow RFC 1918 addresses. Need to access BigQuery from Interconnect."
> **Solution:** Private Service Connect with VPC endpoint ✓

---

## Architecture Patterns

### Pattern 1: Private Google Access (Simple)
```text
┌─────────────────────────────────┐
│         VPC (Subnet)            │
│  ┌─────────────────────┐        │
│  │ VM (no external IP) │        │
│  │  10.0.1.10          │        │
│  └──────────┬──────────┘        │
│             │ PGA enabled       │
└─────────────┼───────────────────┘
              │
    ┌─────────▼──────────┐
    │  Google Network    │
    │  199.36.153.8/30   │
    └─────────┬──────────┘
              │
    ┌─────────▼──────────┐
    │  Cloud Storage     │
    │  storage.googleapis.com
    └────────────────────┘
```

### Pattern 2: Private Service Connect (Advanced)
```text
┌─────────────────────────────────────┐
│            Your VPC                 │
│  ┌─────────────────────┐            │
│  │ VM (private IP)     │            │
│  │  10.0.1.10          │            │
│  └──────────┬──────────┘            │
│             │                       │
│  ┌──────────▼──────────────┐        │
│  │ PSC Endpoint            │        │
│  │ 10.0.1.5 (your VPC IP!) │        │
│  └──────────┬──────────────┘        │
└─────────────┼───────────────────────┘
              │ Private connection
    ┌─────────▼──────────┐
    │  Google APIs       │
    │  (or 3rd party)    │
    └────────────────────┘
```

### Pattern 3: Hybrid Cloud with PSC
```text
┌──────────────────────┐       ┌────────────────────────┐
│   On-Premises        │       │      GCP VPC           │
│   10.1.0.0/16        │       │   10.0.0.0/16          │
│                      │       │                        │
│  ┌────────────┐      │       │  ┌──────────────┐      │
│  │ Firewall   │      │       │  │ PSC Endpoint │      │
│  │ (RFC 1918  │      │       │  │ 10.0.1.5     │      │
│  │  only)     │      │       │  └──────┬───────┘      │
│  └─────┬──────┘      │       │         │              │
└────────┼─────────────┘       └─────────┼──────────────┘
         │                               │
         │   Cloud Interconnect          │
         └───────────────────────────────┘
                      │
            ┌─────────▼──────────┐
            │  BigQuery          │
            │  (via private IP!) │
            └────────────────────┘
```

---

## Migration Path

**Start:** Private Google Access
- Simple, free
- Works for most use cases

**Migrate to:** Private Service Connect when:
- You hit PGA limitations (hybrid, firewall rules)
- Need multi-region private access
- Want to consume third-party services
- Publishing your own services

---

## Common Exam Scenarios

### Scenario 1: Private Cluster
**Question:** "GKE private cluster can't pull images from Artifact Registry. What's the cheapest solution?"

**Answer:** **Enable Private Google Access on the subnet** (free)

**Why not PSC:** More expensive, overkill for this simple use case

---

### Scenario 2: Hybrid with Strict Firewall
**Question:** "On-prem firewall only allows RFC 1918. Need to query BigQuery via Interconnect."

**Answer:** **Private Service Connect endpoint** (provides VPC private IP)

**Why not PGA:** Uses Google public IPs (199.36.153.8/30), blocked by firewall

---

### Scenario 3: Multi-VPC Service Sharing
**Question:** "Share Cloud Run service from Production VPC with Staging VPC without VPC Peering"

**Answer:** **Publish via Private Service Connect**

**Why not PGA:** PGA is for Google APIs, not your own services

---

## Key Takeaways for PCA Exam

1. **Private Google Access** = Simple, free, uses Google public IPs
2. **Private Service Connect** = Advanced, paid, uses your VPC private IPs
3. **PGA** for simple Google API access without external IPs
4. **PSC** for hybrid clouds, third-party services, or service publishing
5. Exam will test: **Choosing the right one** based on requirements (especially hybrid scenarios)
6. Remember: PSC is **newer and more powerful**, but **costs more**

---

## Related Services

- **[[vpc|VPC]]**: Both features operate within VPC
- **[[cloud-vpn|Cloud VPN]]** / **[[cloud-interconnect|Cloud Interconnect]]**: PSC often used with hybrid connectivity
- **[[vpc#vpc service controls|VPC Service Controls]]**: Works with both PGA and PSC
- **[[gcp/gke|GKE Private Clusters]]**: Commonly use PGA
- **[[cloud-nat|Cloud NAT]]**: Alternative to PGA (but costs more, provides full internet access)
