---
title: Cloud-interconnect
category: GCP
description: 'GCP note: Cloud-interconnect.'
tags:
- gcp
- networking
---


# Cloud-interconnect

`gcp` `networking`

## Cloud Interconnect
**Dedicated private connection** between on-premises network and Google Cloud [[vpc|VPC]]

**AWS Equivalent:** AWS Direct Connect

### Key Differences from AWS Direct Connect
| Feature | GCP Cloud Interconnect | AWS Direct Connect |
|---------|----------------------|-------------------|
| Minimum bandwidth | **10 Gbps or 100 Gbps** (Dedicated) | 1 Gbps, 10 Gbps, 100 Gbps |
| Lower bandwidth | Partner Interconnect (50 Mbps - 50 Gbps) | Hosted connection (50 Mbps - 10 Gbps) |
| SLA | **99.99%** with redundancy | 99.95% |
| Encryption | **MACsec** (Layer 2) | MACsec |
| Locations | 100+ PoPs worldwide | 100+ locations |
| Setup time | Weeks (provisioning) | Weeks (provisioning) |

### Cloud Interconnect Types
#### Dedicated Interconnect
- **Direct physical connection** to Google's network
- 10 Gbps or 100 Gbps per link
- Co-location in Google PoP required
- Up to **8 links (800 Gbps)** for 100 Gbps, 8 links (80 Gbps) for 10 Gbps
- Higher bandwidth, lower latency
- More expensive, longer setup

#### Partner Interconnect
- Connection via supported service provider
- **50 Mbps to 50 Gbps** per connection
- No co-location required
- Easier setup, faster provisioning
- Lower cost for smaller bandwidth
- **Recommended for <10 Gbps**

---

## Dedicated Interconnect

### Architecture
```text
On-Premises ↔ Your Router ↔ Cross-Connect ↔ Google Edge Router ↔ Cloud Router ↔ VPC
```

### VLAN Attachments
- **VLAN attachment**: **Logical connection** over physical link
- Up to 16 VLAN attachments per Interconnect connection
- Each attachment connects to one [[vpc|VPC]] via Cloud Router
- **802.1Q VLAN tagging**
- Bandwidth capacity shared across attachments on same link

### Connection Capacity
- **10 Gbps link**: Up to 8 links = 80 Gbps total
- **100 Gbps link**: Up to 8 links = 800 Gbps total
- Each link supports up to 16 VLAN attachments

### BGP Configuration
- Requires Cloud Router in target [[vpc|VPC]]
- **BGP required** for route exchange
- Supports IPv4 (IPv6 in preview)
- Private ASN: 64512-65534 or 4200000000-4294967294
- BFD for fast failure detection

### MACsec Encryption
- **Layer 2 encryption** for Dedicated Interconnect
- Protects data in transit to Google PoP
- 128-bit or 256-bit AES encryption
- Requires compatible hardware
- Minimal performance impact

### Redundancy for 99.99% SLA
**Requirements:**
- **2 Interconnect connections** in different metros
- **4 VLAN attachments** (2 per connection)
- 2 Cloud Routers (one per region or both in same region)
- 2 on-premises routers

**Topology:**

| Connection | VLAN attachment | Cloud Router |
|------------|-----------------|--------------|
| Connection 1 | VLAN Attachment 1 | Cloud Router 1 |
| Connection 1 | VLAN Attachment 2 | Cloud Router 2 |
| Connection 2 | VLAN Attachment 3 | Cloud Router 1 |
| Connection 2 | VLAN Attachment 4 | Cloud Router 2 |

All four paths lead to the VPC.

### Setup Process
1. **Choose co-location facility** (Google PoP)
2. **Order Dedicated Interconnect** in Cloud Console
3. **Receive LOA-CFA** (Letter of Authorization and Connecting Facility Assignment)
4. **Establish cross-connect** with co-lo provider
5. **Create VLAN attachments** and Cloud Routers
6. **Configure BGP** sessions
7. **Test connectivity** and monitor

---

## Partner Interconnect

### Architecture
```text
On-Premises ↔ Service Provider Network ↔ Google Edge ↔ Cloud Router ↔ VPC
```

### Partner Interconnect Connections
- Provisioned by supported service provider
- Bandwidth: **50 Mbps, 100 Mbps, 200 Mbps, 300 Mbps, 400 Mbps, 500 Mbps, 1 Gbps, 2 Gbps, 5 Gbps, 10 Gbps, 20 Gbps, 50 Gbps**
- **Layer 2** or **Layer 3** connectivity
- No co-location needed
- Faster setup than Dedicated Interconnect

### Layer 2 vs Layer 3
| Aspect | Layer 2 | Layer 3 |
|--------|---------|---------|
| BGP | You configure BGP with Google Cloud Router | Service provider manages BGP to Google. You configure BGP with the service provider |
| VLAN attachment | Direct VLAN attachment to [[vpc|VPC]] | - |
| Control | More control over routing. Similar to Dedicated Interconnect experience | Abstracted from Google's network. Simpler for customers |

### VLAN Attachments
- Each Partner Interconnect connection = 1 VLAN attachment
- Multiple connections for redundancy
- Connects to one VPC via Cloud Router

### Redundancy for 99.99% SLA
**Requirements:**
- **2 Partner Interconnect connections** via different edge Availability Domains
- 2 VLAN attachments (one per connection)
- 2 Cloud Routers (can be in same region)
- Service provider redundancy

**Edge Availability Domains:**
- domain-1, domain-2 (metro-specific)
- Ensures physical separation

### Setup Process
1. **Choose service provider** (e.g., Equinix, Megaport, AT&T)
2. **Request connection** from provider
3. **Create VLAN attachment** in Cloud Console (pairing key)
4. **Provide pairing key** to service provider
5. **Provider provisions** connection
6. **Configure Cloud Router** and BGP
7. **Activate** and test connectivity

---

## Cloud Router (Required)

**AWS Equivalent:** Virtual Private Gateway (for BGP)
- Managed BGP service for dynamic routing
- Regional resource
- Required for both Dedicated and Partner Interconnect
- **Automatically propagates routes** between VPC and on-premises
- Supports custom route advertisements

### Dynamic Routing Modes
Configured at [[vpc|VPC]] level:
- **Regional**: Routes stay within region
- **Global**: Routes propagate to **all regions** in VPC
  - **Required for multi-region Interconnect**
  - Enables cross-region traffic via Interconnect

### BGP Sessions
- One BGP session per VLAN attachment
- Configure peer ASN and IP addresses
- BFD for fast failure detection (300ms-30s)
- MD5 authentication supported

---

## Interconnect Comparison

| Feature | Dedicated Interconnect | Partner Interconnect |
|---------|----------------------|---------------------|
| Bandwidth | 10 or 100 Gbps per link | 50 Mbps - 50 Gbps |
| Max capacity | 800 Gbps (8x100G) | 50 Gbps per connection |
| Co-location | **Required** | Not required |
| Setup time | Weeks | Days to weeks |
| Cost | Higher (port fees + egress) | Lower (connection + egress) |
| Best for | >10 Gbps sustained | <10 Gbps, simpler setup |
| Encryption | MACsec | Via VPN on top |
| SLA | 99.9% (single), 99.99% (dual) | 99.9% (single), 99.99% (dual) |

---

## Interconnect vs Cloud VPN

| Feature | Cloud Interconnect | [[cloud-vpn|Cloud VPN]] |
|---------|-------------------|----------|
| Connection type | **Private dedicated** | Encrypted over internet |
| Bandwidth | 50 Mbps - 800 Gbps | 3 Gbps per tunnel (15 Gbps max/gateway) |
| Latency | **Lowest** | +10-30ms |
| Setup time | Days to weeks | Minutes |
| Cost | High (port/connection + egress) | Low (tunnel + egress) |
| Encryption | Optional (MACsec) | **IPsec required** |
| Best for | High bandwidth, low latency | Quick setup, <10 Gbps |
| SLA | 99.9%-99.99% | 99.9%-99.99% |

---

## Pricing

| Connection type | Fees | Egress | Ingress |
|-----------------|------|--------|---------|
| Dedicated Interconnect | Port fees per 10 Gbps or 100 Gbps port per month (~$1,700 for 10 Gbps, ~$8,500 for 100 Gbps). No charge for VLAN attachments | Discounted rates (vs internet egress) | Free |
| Partner Interconnect | Connection fees per connection capacity per month (via provider). Provider fees set by service provider | Discounted rates | Free |

### Egress Pricing (vs Internet)
- Interconnect egress: ~60-70% cheaper than internet egress
- Higher savings for larger volumes
- Pricing varies by region

---

## ACE Level

### Essential gcloud Commands
```bash
# Create Cloud Router (required)
gcloud compute routers create ROUTER_NAME \
  --network=VPC_NAME \
  --region=REGION \
  --asn=65001

# Create VLAN attachment (Dedicated Interconnect)
gcloud compute interconnects attachments dedicated create ATTACHMENT_NAME \
  --router=ROUTER_NAME \
  --interconnect=INTERCONNECT_NAME \
  --region=REGION \
  --vlan=VLAN_ID

# Create VLAN attachment (Partner Interconnect)
gcloud compute interconnects attachments partner create ATTACHMENT_NAME \
  --router=ROUTER_NAME \
  --region=REGION \
  --edge-availability-domain=AVAILABILITY_DOMAIN

# Get pairing key (Partner Interconnect)
gcloud compute interconnects attachments describe ATTACHMENT_NAME \
  --region=REGION \
  --format="get(pairingKey)"

# List interconnect connections
gcloud compute interconnects list

# List VLAN attachments
gcloud compute interconnects attachments list

# Describe VLAN attachment
gcloud compute interconnects attachments describe ATTACHMENT_NAME \
  --region=REGION

# View Cloud Router status (BGP sessions)
gcloud compute routers get-status ROUTER_NAME \
  --region=REGION

# Add BGP peer to Cloud Router
gcloud compute routers add-interface ROUTER_NAME \
  --interface-name=INTERFACE_NAME \
  --interconnect-attachment=ATTACHMENT_NAME \
  --region=REGION

gcloud compute routers add-bgp-peer ROUTER_NAME \
  --peer-name=PEER_NAME \
  --peer-asn=PEER_ASN \
  --interface=INTERFACE_NAME \
  --region=REGION
```

### Key Concepts for ACE
- Understanding difference between Dedicated and Partner Interconnect
- When to use Interconnect vs Cloud VPN
- Creating VLAN attachments for VPC connectivity
- Configuring Cloud Router and BGP for dynamic routing
- Understanding bandwidth requirements and capacity planning
- Obtaining and sharing pairing keys for Partner Interconnect
- Monitoring interconnect status and BGP sessions
- Calculating redundancy requirements for 99.99% SLA

---

## PCA Level

### Architectural Patterns
#### Hybrid Cloud with Dedicated Interconnect
- **High-bandwidth connection** (10-800 Gbps) to on-premises
- Multiple VLAN attachments for different VPCs
- Global routing mode for multi-region access
- MACsec encryption for data in transit
- Backup [[cloud-vpn|Cloud VPN]] for failover

#### Multi-Cloud Interconnect
- Partner Interconnect to connect GCP, AWS, Azure
- Service provider manages cross-cloud routing
- Layer 3 for simplicity
- Use cases: Data synchronization, multi-cloud apps

#### Hub-and-Spoke with Interconnect
- Central hub VPC with Interconnect to on-premises
- Spoke VPCs connected via [[vpc|VPC Peering]] or Network Connectivity Center
- Centralized egress to on-premises
- Global routing for cross-region communication

#### Disaster Recovery with Interconnect
- Primary Interconnect to main datacenter
- Secondary Interconnect or VPN to DR site
- Active/passive or active/active routing
- BGP route priorities for failover

### High Availability Design
- **99.99% SLA Requirements**:
  - 2 Interconnect connections in different metros
  - 4 VLAN attachments (Dedicated) or 2 (Partner)
  - 2 Cloud Routers (redundancy)
  - 2 on-premises routers
- **Multi-Region Redundancy**:
  - Interconnect connections in different regions
  - Global routing mode
  - Cross-region failover
- **BFD**: Fast failure detection (300ms intervals)
- **Monitoring**: Alert on BGP session down, packet loss

### Performance Optimization
- **Bandwidth Planning**:
  - Dedicated: 10 Gbps minimum, 100 Gbps for high throughput
  - Partner: Start with lower bandwidth, scale up
  - Multiple links for >100 Gbps
- **Latency**:
  - **Lowest latency option** for hybrid connectivity
  - Choose co-lo closest to datacenter
  - Premium network tier
- **VLAN Attachment Distribution**:
  - Spread across multiple links for load balancing
  - Each attachment can use full link capacity if needed
- **MTU**: 1500 bytes (higher than VPN's 1460)

### Security Best Practices
- **MACsec Encryption**: Enable for Dedicated Interconnect
- **BGP MD5 Authentication**: Secure BGP sessions
- **Firewall Rules**: Restrict traffic from on-premises
- **Private IP Addressing**: Use RFC 1918 ranges only
- **VPC Service Controls**: Prevent data exfiltration
- **Least Privilege IAM**: Restrict Interconnect management
- **Monitoring**: Track BGP sessions, bandwidth usage

### Cost Optimization
- **Right-Size Bandwidth**:
  - Start with Partner Interconnect for <10 Gbps
  - Migrate to Dedicated when sustained >10 Gbps
- **Egress Optimization**:
  - 60-70% cheaper egress than internet
  - Route all on-premises traffic via Interconnect
- **Multi-VPC Sharing**:
  - Single Interconnect with multiple VLAN attachments
  - Share across VPCs to amortize port costs
- **Committed Use Discounts**:
  - Available for Dedicated Interconnect ports
  - 1 or 3 year commitments

### Migration Strategies
#### From AWS Direct Connect
- Similar architecture and BGP configuration
- AWS: 1-100 Gbps per connection
- GCP: 10 or 100 Gbps Dedicated, 50 Mbps-50 Gbps Partner
- Partner providers often support both GCP and AWS
- Plan for: Bandwidth mapping, BGP migration, testing

#### From VPN to Interconnect
- Establish Interconnect connection first
- Configure BGP with equal cost routes (ECMP)
- Gradually shift traffic by adjusting route priorities
- Monitor latency and throughput improvements
- Decommission VPN tunnels after validation
- Keep VPN as backup (lower cost)

#### From MPLS to Interconnect
- Replace MPLS with Partner or Dedicated Interconnect
- Work with service provider for migration plan
- Gradual cutover per application
- Cost savings: Interconnect often cheaper than MPLS

### Capacity Planning
- **Bandwidth Growth**:
  - Start with 50% headroom for growth
  - Monitor utilization (alert at >70%)
  - Plan for 3-5 year growth
- **VLAN Attachments**:
  - Max 16 per Dedicated Interconnect connection
  - Plan for multi-VPC requirements
- **BGP Routes**:
  - Cloud Router soft limit: 100-200 routes
  - Summarize routes when possible
- **Connection Count**:
  - 2 minimum for HA
  - 4+ for very high availability

### Compliance Considerations
- **Data Residency**: Private connection for regulated data
- **Encryption**: MACsec for data in transit
- **Audit Logging**: Track all configuration changes
- **Dedicated Resources**: No shared infrastructure with Dedicated Interconnect
- **Service Provider Compliance**: Verify provider certifications for Partner Interconnect

### BGP Design Considerations
- **ASN Planning**: Use private ASNs consistently
- **Route Filtering**: Advertise only necessary routes
- **Route Priorities**: Use MED and local preference for traffic engineering
- **AS Path Prepending**: Influence inbound traffic routing
- **Graceful Restart**: Minimize disruption during maintenance
- **BFD Timers**: Balance between fast detection and stability

### Advanced Configurations
#### ECMP (Equal-Cost Multi-Path)
- Multiple VLAN attachments with equal cost
- Load balancing across links
- Better bandwidth utilization
- Automatic failover

#### Active/Passive Failover
- Primary and backup VLAN attachments
- Different BGP priorities (MED)
- Backup remains idle until failure
- Lower bandwidth utilization but deterministic routing

#### Multi-Region Traffic Engineering
- Global routing mode
- Advertise region-specific routes
- Use BGP communities for route tagging
- Direct traffic to closest region

### Observability
- **[[gcp/cloud-monitoring|Cloud Monitoring]]**:
  - VLAN attachment throughput
  - BGP session status
  - Packet loss, errors
  - Link utilization
- **[[gcp/cloud-logging|Cloud Logging]]**:
  - BGP session events
  - Configuration changes
  - Interconnect provisioning events
- **Alerting**:
  - BGP session down
  - High link utilization (>70%)
  - Packet drops

### Troubleshooting
| Symptom | Check or fix |
|---------|--------------|
| BGP session issues | Verify ASN configuration on both sides. Check IP addressing (link-local IPs). Validate MD5 authentication. |
| Throughput issues | Check link utilization. Verify VLAN attachment capacity. Monitor for packet drops. |
| Routing issues | Check route propagation (global vs regional). Verify route priorities. Use `gcloud compute routers get-status` for BGP state. |

### Network Connectivity Center
- Centralized view of all Interconnect connections
- Visualize hybrid network topology
- Monitor connectivity across VPN and Interconnect
- Simplify complex hybrid architectures

### Well-Architected Considerations
- **Operational Excellence**: Managed BGP with Cloud Router, monitoring, automated failover
- **Reliability**: 99.99% SLA with dual connections, BFD for fast detection, multi-region redundancy
- **Security**: MACsec encryption, BGP MD5 auth, private connectivity, VPC Service Controls
- **Performance**: Lowest latency, high bandwidth (up to 800 Gbps), ECMP load balancing
- **Cost**: Lower egress costs, right-size bandwidth, multi-VPC sharing, committed use discounts
- **Sustainability**: Efficient routing, minimize unnecessary data transfer, shared infrastructure
