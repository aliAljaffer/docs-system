---
title: Vpc
category: GCP
description: 'GCP note: Vpc.'
tags:
- gcp
- networking
---

<!-- imported from ObsidianVault/studies/cloud-architecht/gcp/networking/vpc.md. Edit the source, then run sync.py. -->

# Vpc

`gcp` `networking`

## Virtual Private Cloud (VPC)
**AWS Equivalent:** VPC
**Global resource** that spans all regions, providing **isolated network** for Google Cloud resources

### Key Differences from AWS VPC
| Feature | GCP VPC | AWS VPC |
|---------|---------|---------|
| Scope | **Global** (spans all regions) | Regional |
| Subnets | Regional (span zones) | Availability Zone specific |
| IP ranges | Can expand subnet ranges | Fixed CIDR blocks |
| Firewall | Network-level tags | Security Groups (instance-level) |
| DNS | Automatic internal DNS | Route 53 Private Hosted Zones |

### VPC Networks
- **Default VPC**: Automatically created, one subnet per region
- **Auto Mode VPC**: Automatically creates subnets in each region (10.128.0.0/9)
- **Custom Mode VPC**: Manual subnet creation, **recommended for production**
- Can convert Auto Mode to Custom Mode (one-way, irreversible)

### Subnets
- **Regional resource** that spans all zones in a region
- Each subnet has:
  - **Primary IP range**: Main CIDR block for resources
  - **Secondary IP ranges**: Additional ranges for GKE pods/services, alias IPs
- Can expand primary and secondary ranges **without downtime**
- **Cannot overlap with other subnets** in same VPC
- Cannot shrink subnet ranges
- Minimum /29 (8 IPs), maximum /8

#### Reserved IP Addresses (per subnet)
- **First IP** (.0): Network address
- **Second IP** (.1): Default gateway
- **Second-to-last IP**: Reserved by GCP
- **Last IP**: Broadcast address

### Routing
#### Routes
- **Implicit routes**: Automatically created
  - Default route to internet (0.0.0.0/0 → default-internet-gateway)
  - Subnet routes for internal communication
- **Custom static routes**: Manually defined
  - Next hop types: Instance, [[cloud-load-balancing|internal load balancer]], [[cloud-vpn|VPN tunnel]], [[cloud-interconnect|interconnect]]
- **Dynamic routes**: Learned via [[cloud-vpn|Cloud VPN]] or [[cloud-interconnect|Cloud Interconnect]]
  - BGP-based route exchange
  - Propagated based on dynamic routing mode

#### Dynamic Routing Modes
- **Regional**: Routes learned in one region stay in that region
- **Global**: Routes learned in one region propagate to **all regions**
  - Required for multi-region architectures
  - Slightly higher cost

### Firewall Rules
**AWS Equivalent:** Security Groups + Network ACLs (combined)
- **Network-level**, not instance-level like AWS Security Groups
- Stateful (return traffic automatically allowed)
- Applied via:
  - **Target tags**: Flexible, most common
  - **Target service accounts**: [[security-iam|IAM]]-based, more secure
  - **All instances**: Apply to entire VPC
  - **Specified instances**: By name

#### Rule Components
- **Direction**: Ingress or Egress
- **Priority**: 0-65535 (lower = higher priority, **default 1000**)
- **Action**: Allow or Deny
- **Source/Destination**:
  - IP ranges (CIDR)
  - Tags (for ingress)
  - [[security-iam|Service accounts]]
- **Protocols and ports**: TCP, UDP, ICMP, etc.

#### Implied Firewall Rules
- **Implied allow egress**: All outbound allowed (priority 65535)
- **Implied deny ingress**: All inbound denied (priority 65535)
- Can override with higher priority rules

#### Hierarchical Firewall Policies
- Apply firewall rules at **organization or folder level**
- **Enforced across all VPCs** in scope
- Cannot be overridden by VPC-level rules
- Use cases: Organization-wide security policies

### Private Google Access
- Allows VMs with **only private IPs** to access Google APIs and services
- Enabled **per subnet**
- Traffic stays within Google's network, doesn't traverse internet
- Required for:
  - Compute Engine instances without external IPs accessing Cloud Storage, Cloud SQL
  - GKE private clusters accessing Google APIs
- **Private Google Access for on-premises hosts**: Access Google APIs from on-prem via [[cloud-vpn|VPN]]/[[cloud-interconnect|Interconnect]]
- See [[private-google-access-vs-psc|Private Google Access vs Private Service Connect]] for detailed comparison

### Private Service Connection
- Connect to Google-managed services via private IP
- Uses VPC peering under the hood
- Examples: Cloud SQL, Memorystore
- Requires allocated IP range for service

### VPC Peering
**AWS Equivalent:** VPC Peering
- Connect two VPCs **privately** (within GCP or across organizations)
- Allows communication via **internal IPs**
- **Non-transitive**: If A peers with B and B peers with C, A cannot reach C
- **No overlapping IP ranges** allowed
- No additional charges for VPC peering traffic (only standard networking charges)
- Can peer across projects, organizations, GCP regions

#### VPC Peering Limitations
- Maximum 25 peered VPCs per VPC (can be increased)
- [[security-iam|IAM]] permissions required on both VPCs
- Firewall rules apply independently in each VPC

### Shared VPC
**AWS Equivalent:** AWS Resource Access Manager (similar concept)
- Share VPC network from **host project** to **service projects**
- Centralized network administration
- Service project resources use host project's VPC
- **Requires VPC-native clusters** for GKE

#### Use Cases
- Central IT manages networking
- Multiple teams/projects share common network
- Centralized firewall and routing policies
- Cost allocation per project

#### Roles
- **Host project**: Contains shared VPC network
  - Requires `compute.xpnAdmin` at organization level
- **Service project**: Uses shared VPC from host project
  - Requires `compute.networkUser` on host project subnets

### VPC Service Controls
**AWS Equivalent:** Similar to AWS Service Control Policies + VPC Endpoints
- Create **security perimeter** around Google Cloud resources
- Prevent data exfiltration
- Control access to resources based on:
  - IP address
  - VPC network
  - Identity context (user, [[security-iam|service account]], device)
- Supported services: Cloud Storage, Cloud SQL, BigQuery, etc.
- See VPC Service Controls for full details

### Flow Logs
**AWS Equivalent:** VPC Flow Logs
- Capture network traffic metadata
- **Per subnet** configuration
- Sampling rate: 0.0 to 1.0 (1.0 = 100%)
- Sent to Cloud Logging
- Use cases: Network monitoring, forensics, cost optimization

### Packet Mirroring
**AWS Equivalent:** VPC Traffic Mirroring
- Clone network traffic for security inspection
- Mirror traffic from specific instances or subnets
- Send to collector (typically IDS/IPS appliance like [[cloud-ngfw|Cloud NGFW]])
- Use cases: Security monitoring, threat detection, troubleshooting

### VPC Network Peering vs Shared VPC
| Feature       | VPC Peering | Shared VPC |
| ------------- | ------------------- | --------------- |
| Admin model   | Distributed         | Centralized     |
| IP management | Separate per VPC    | Single IP space |
| IAM           | Independent         | Centralized     |
| Use case      | Partner integration | Org internal    |
| Complexity    | Lower               | Higher          |

### Cloud Router
- Managed BGP service
- Required for [[cloud-vpn|Cloud VPN (HA mode)]] and [[cloud-interconnect|Cloud Interconnect]]
- **Dynamically exchanges routes** between VPC and on-premises
- Regional resource
- Supports custom BGP advertisements

### Bring Your Own IP (BYOIP)
- Use your own public IP addresses in GCP
- Requires validation of IP ownership
- Must be /24 or larger
- Use cases: IP reputation, migration from other clouds

### IP Addressing
#### Internal IP Addresses
- **Ephemeral** (released when resource deleted) or **Static** (reserved)
- RFC 1918 private ranges
- Assigned from subnet ranges

#### External IP Addresses
- **Ephemeral**: Temporary, released when resource stopped
- **Static**: Reserved, persist beyond resource lifecycle
- **Regional**: Used by regional resources (VMs, [[cloud-load-balancing|internal LBs]])
- **Global**: Used by global resources ([[cloud-load-balancing|Global Load Balancers]])

### MTU (Maximum Transmission Unit)
- Default: 1460 bytes
- Can increase to **8896 bytes** (Jumbo frames) for better performance
- Not supported: [[cloud-vpn|VPN]], peering with external networks

### Network Performance Tiers
**AWS Equivalent:** N/A (AWS uses Premium only)
- **Premium Tier**: Google's global network, **best performance**, single global IP
- **Standard Tier**: ISP networks, regional IPs, lower cost
- Can mix tiers within project
- Savings: ~50% on egress costs

### Pricing
- **VPC Network**: No charge
- **Static IP**: Charged when not attached to running resource
- **Egress traffic**: Charged (varies by destination)
- **Ingress traffic**: Free
- **Private Google Access**: Free
- **VPC Peering**: No additional charge (standard egress applies)

---

## ACE Level

### Essential gcloud Commands
```bash
# Create custom VPC
gcloud compute networks create VPC_NAME \
  --subnet-mode=custom \
  --bgp-routing-mode=regional

# Create subnet
gcloud compute networks subnets create SUBNET_NAME \
  --network=VPC_NAME \
  --region=REGION \
  --range=10.0.1.0/24

# List VPCs
gcloud compute networks list

# List subnets
gcloud compute networks subnets list

# Expand subnet range
gcloud compute networks subnets expand-ip-range SUBNET_NAME \
  --region=REGION \
  --prefix-length=20

# Create firewall rule (allow SSH)
gcloud compute firewall-rules create allow-ssh \
  --network=VPC_NAME \
  --allow=tcp:22 \
  --source-ranges=0.0.0.0/0

# Create firewall rule with tags
gcloud compute firewall-rules create allow-http \
  --network=VPC_NAME \
  --allow=tcp:80 \
  --target-tags=web-server

# List firewall rules
gcloud compute firewall-rules list

# Delete firewall rule
gcloud compute firewall-rules delete RULE_NAME

# Enable Private Google Access
gcloud compute networks subnets update SUBNET_NAME \
  --region=REGION \
  --enable-private-ip-google-access

# Reserve static external IP
gcloud compute addresses create ADDRESS_NAME --region=REGION

# List routes
gcloud compute routes list

# Create static route
gcloud compute routes create ROUTE_NAME \
  --network=VPC_NAME \
  --destination-range=10.0.2.0/24 \
  --next-hop-instance=INSTANCE_NAME \
  --next-hop-instance-zone=ZONE
```

### Key Concepts for ACE
- Creating custom VPC networks and subnets
- Understanding regional subnets vs AWS AZ-specific subnets
- Configuring firewall rules with tags and [[security-iam|service accounts]]
- Enabling Private Google Access for private VMs
- Managing static and ephemeral IP addresses
- Expanding subnet ranges without downtime
- Viewing and understanding VPC Flow Logs
- Difference between auto-mode and custom-mode VPCs

---

## PCA Level

### Architectural Patterns
#### Hub-and-Spoke Topology
- Central hub VPC connected to multiple spoke VPCs
- Use [[cloud-vpn|Cloud VPN]] or [[cloud-interconnect|Cloud Interconnect]] for on-prem
- Shared services ([[cloud-dns|DNS]], monitoring) in hub
- Requires VPC peering or [[cloud-vpn|VPN tunnels]] between hub and spokes
- **Non-transitive nature** of peering requires careful design

#### Shared VPC for Multi-Project Organizations
- Centralized networking in host project
- Multiple service projects consume shared VPC
- Single point of control for security and compliance
- Simplified IP address management
- Required permissions: `compute.xpnAdmin`, `compute.networkUser`

#### Multi-Region VPC Architecture
- Single global VPC with regional subnets
- Global routing mode for cross-region communication
- Regional resources in each region for low latency
- [[cloud-load-balancing|Global Load Balancing]] for traffic distribution
- Consider VPC flow logs for network visibility

### Network Segmentation Strategies
#### By Environment
- Separate VPCs for dev, staging, production
- VPC peering or [[cloud-vpn|VPN]] for cross-environment access
- Isolated security postures

#### By Application Tier
- Subnets for web, app, data tiers
- Firewall rules restrict inter-tier traffic
- Use network tags for flexible rule targeting

#### By Compliance Boundary
- VPC Service Controls for regulatory compliance
- Separate VPCs for different compliance zones (PCI, HIPAA)
- Private Google Access for regulated workloads

### High Availability Design
- **Regional subnets** span all zones automatically
- [[cloud-load-balancing|Cloud Load Balancing]] for traffic distribution
- [[cloud-vpn|HA VPN]] for 99.99% SLA connectivity
- Multiple Cloud Routers in each region for BGP redundancy
- Regional Persistent Disks for data replication

### Security Best Practices
- **Least Privilege Firewall Rules**: Deny by default, allow explicitly
- **Use [[security-iam|Service Accounts]] for Rules**: More secure than tags
- **Hierarchical Firewall Policies**: Enforce org-wide rules
- **Private Google Access**: Avoid external IPs when possible
- **VPC Service Controls**: Prevent data exfiltration
- **Flow Logs**: Enable for security monitoring
- **Private Service Connection**: Use private IPs for managed services
- **Shared VPC**: Centralize network security management

### Cost Optimization
- **Network Tier**: Use Standard tier for cost-sensitive workloads
- **Regional Egress**: Keep traffic within region when possible
- **VPC Peering**: Use instead of external IPs for inter-VPC communication
- **Private Google Access**: Avoid egress charges for Google API access
- **Committed Use Discounts**: Apply to VM network egress
- **Release Static IPs**: When not in use to avoid charges

### Migration Considerations
#### From AWS
- **VPC Scope**: GCP VPC is global, AWS VPC is regional
  - Design: Single global VPC vs multiple regional VPCs
- **Subnets**: GCP subnets are regional, AWS subnets are AZ-specific
  - Simplifies multi-AZ deployments in GCP
- **Security Groups**: Map to firewall rules with tags/[[security-iam|service accounts]]
- **Network ACLs**: Map to firewall rules (stateful in GCP)
- **VPC Endpoints**: Use Private Google Access and Private Service Connection
- **Transit Gateway**: Use VPC peering or Network Connectivity Center

#### BYOIP Strategy
- Validate IP ownership
- Create IP prefix in GCP
- Announce to Google's network
- Update [[cloud-dns|DNS records]] gradually

### IP Address Planning
- **Subnet sizing**: Plan for growth, can expand later
- **Secondary ranges**: Reserve for GKE pods/services
- **Avoid overlaps**: Critical for VPC peering and hybrid connectivity
- **RFC 1918 ranges**: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
- **Organization-wide IPAM**: Centralized IP address management

### Advanced Firewall Configurations
#### Egress Deny Rules
- Block outbound traffic to specific destinations
- Prevent data exfiltration
- Higher priority than default allow egress

#### Firewall Insights
- Identify overly permissive rules
- Find unused firewall rules
- Optimize for least privilege

#### Firewall Rules Logging
- Log allowed or denied connections
- Integrates with Cloud Logging
- Performance impact: ~0.1% throughput reduction

### Network Connectivity Center
**AWS Equivalent:** AWS Transit Gateway
- Centralized hub for connectivity management
- Connect VPCs, on-prem, other clouds
- Visualize network topology
- Simplifies complex hybrid architectures

### Private Service Connect
- Access managed services via **private endpoints**
- More flexible than Private Service Connection
- Supports Google APIs, third-party services
- No VPC peering required
- See [[private-google-access-vs-psc|Private Google Access vs Private Service Connect]] for comparison

### Well-Architected Considerations
- **Operational Excellence**: Hierarchical firewall policies, centralized management with Shared VPC
- **Reliability**: Regional subnets, multiple zones, [[cloud-vpn|HA VPN]], global routing
- **Security**: VPC Service Controls, Private Google Access, least privilege firewall rules, flow logs
- **Performance**: Premium network tier, low latency routing, MTU optimization
- **Cost**: Standard network tier, regional traffic, VPC peering, rightsized static IPs
- **Sustainability**: Optimize network paths, reduce unnecessary data transfer
