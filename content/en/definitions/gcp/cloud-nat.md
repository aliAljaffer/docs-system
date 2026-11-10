---
title: Cloud-nat
category: GCP
description: 1. VM sends packet to internet destination
tags:
- gcp
- networking
---

<!-- imported from ObsidianVault/studies/cloud-architecht/gcp/networking/cloud-nat.md. Edit the source, then run sync.py. -->

# Cloud-nat

`gcp` `networking`

## Cloud NAT
**AWS Equivalent:** NAT Gateway
**Managed Network Address Translation** service for outbound internet connectivity from **private instances**
### Key Differences from AWS NAT Gateway
| Feature         | GCP Cloud NAT                    | AWS NAT Gateway             |
| --------------- | -------------------------------- | --------------------------- |
| Scope           | **Regional service**             | Availability Zone specific  |
| IP allocation   | Manual or automatic              | Automatic (per NAT Gateway) |
| Redundancy      | **Built-in regional redundancy** | Need NAT GW per AZ          |
| Port allocation | **Configurable per VM**          | Fixed (64,512 ports total)  |
| Implementation  | **Software-defined**             | Hardware appliance          |
| Logging         | Detailed (per connection)        | Flow logs only              |
| Cost            | Based on VMs + data processed    | Per NAT Gateway-hour + data |

---
## Cloud NAT Overview
- **Regional** resource
- Provides outbound internet access for private VMs
- **No external IP required** for VMs
- **Highly available** within region (no single point of failure)
- **Software-defined**, not a physical instance
- Cannot be used for **inbound connections** (ingress)

### How It Works
```
Private VM (no external IP) → Cloud Router → Cloud NAT → Internet
```

1. VM sends packet to internet destination
2. Cloud NAT translates private IP to public NAT IP
3. Response traffic automatically translated back
4. Stateful connection tracking

---

## Cloud NAT Architecture

### Components
#### Cloud Router (Required)
- **Must exist in same region** as Cloud NAT
- Manages NAT configuration
- Advertises routes
- See [[cloud-vpn|Cloud VPN]] or [[cloud-interconnect|Cloud Interconnect]] for details

#### NAT Gateway
- Logical configuration on Cloud Router
- Defines:
  - Which subnets use NAT
  - NAT IP addresses
  - Port allocation
  - Logging settings

#### NAT IP Addresses
- **Automatic allocation**: Google assigns IPs
- **Manual allocation**: You specify reserved external IPs
- Can use **1 to 64 NAT IPs** per gateway
- More IPs = more concurrent connections

---

## Configuration Options

### Source Configuration
**Which VMs use Cloud NAT?**
- **All subnets in region**: All VMs in all subnets
- **Custom subnets**: Select specific subnets
  - **All IP ranges**: Primary + secondary ranges
  - **Primary IP ranges only**: Exclude secondary ranges (e.g., GKE pods)

### NAT IP Address Allocation
#### Automatic
- Google allocates external IPs
- Specify minimum number of IPs
- Automatically scales up based on usage
- **Recommended for most use cases**

#### Manual
- You reserve and assign specific external IPs
- More control over IP addresses
- Use cases: IP allowlisting, fixed IPs for compliance

### Port Allocation
**Ports per VM:**
- **Minimum ports per VM**: 64 to 65,536 (default 64)
- **Maximum ports per VM**: Can set upper limit
- Each NAT IP provides **64,512 usable ports**
- **Ports shared across all VMs** using that NAT IP

#### Port Allocation Methods
**Dynamic port allocation:**
- Ports assigned as needed
- Efficient for variable workloads
- Default: Min 64, max 65,536 per VM

**Static port allocation:**
- Fixed ports per VM
- Predictable, easier troubleshooting
- Less efficient (ports reserved even if unused)

### Connection Limits
- NAT IP ports: **64,512 ports per IP**
- **Calculation**: `Total connections = NAT IPs × 64,512`
- Example: 4 NAT IPs = 258,048 concurrent connections
- Connections timeout after **inactivity period**

---

## Timeout Configuration
**Connection idle timeouts:**
- **TCP Established**: 1200 seconds (20 min, default)
- **TCP Transitory**: 30 seconds (default)
- **UDP**: 30 seconds (default)
- **ICMP**: 30 seconds (default)

**Configurable:**
- Adjust based on application requirements
- Longer timeouts: More connections, more port usage
- Shorter timeouts: Faster port recycling

---

## Logging
**AWS Equivalent:** VPC Flow Logs (less detailed)
- **Per-connection logging** (more detailed than AWS)
- Logs include:
  - Source/destination IPs and ports
  - NAT IP used
  - Bytes transferred
  - Timestamp
- Sent to [[gcp/cloud-logging|Cloud Logging]]
- **Filter options**:
  - **All**: Log all connections (high volume)
  - **Errors only**: Failed translations
  - **Translations only**: NAT events, not every packet
  - **None**: No logging

**Performance impact:**
- Logging adds minimal latency
- High connection volume = high log volume
- Use sampling or error-only for cost optimization
---
## Private Google Access
**Important:** Cloud NAT is **NOT required** for [[vpc|Private Google Access]]
- [[vpc|Private Google Access]]: VM → Google APIs (e.g., [[gcp/cloud-storage|Cloud Storage]])
- Cloud NAT: VM → Internet (e.g., software updates, external APIs)
- Can use both simultaneously

---

## High Availability
- **Built-in regional redundancy**
- No single point of failure
- **No VM instance** to manage or fail
- Distributed across zones automatically
- Unlike AWS (need NAT Gateway per AZ), GCP handles HA automatically

---

## Pricing
- **NAT gateway**: Per hour
  - ~$0.045 per hour (~$33/month)
- **Data processed**: Per GB
  - ~$0.045 per GB processed
- **NAT IP addresses**: Standard external IP pricing
  - In-use external IP: Free
  - Reserved but unused: Charged
- **No charge for Private Google Access** (separate feature)

---

## ACE Level

### Essential gcloud Commands
```bash
# Create Cloud Router (required first)
gcloud compute routers create ROUTER_NAME \
  --network=VPC_NAME \
  --region=REGION

# Create Cloud NAT (automatic IP allocation)
gcloud compute routers nats create NAT_CONFIG_NAME \
  --router=ROUTER_NAME \
  --region=REGION \
  --auto-allocate-nat-external-ips \
  --nat-all-subnet-ip-ranges

# Create Cloud NAT (manual IP allocation)
# First, reserve external IPs
gcloud compute addresses create NAT_IP_1 --region=REGION
gcloud compute addresses create NAT_IP_2 --region=REGION

# Then create NAT with manual IPs
gcloud compute routers nats create NAT_CONFIG_NAME \
  --router=ROUTER_NAME \
  --region=REGION \
  --nat-external-ip-pool=NAT_IP_1,NAT_IP_2 \
  --nat-all-subnet-ip-ranges

# Create Cloud NAT for specific subnets
gcloud compute routers nats create NAT_CONFIG_NAME \
  --router=ROUTER_NAME \
  --region=REGION \
  --auto-allocate-nat-external-ips \
  --nat-custom-subnet-ip-ranges=SUBNET_1,SUBNET_2

# List Cloud NAT configurations
gcloud compute routers nats list --router=ROUTER_NAME --region=REGION

# Describe Cloud NAT
gcloud compute routers nats describe NAT_CONFIG_NAME \
  --router=ROUTER_NAME \
  --region=REGION

# Update Cloud NAT (enable logging)
gcloud compute routers nats update NAT_CONFIG_NAME \
  --router=ROUTER_NAME \
  --region=REGION \
  --enable-logging

# Update Cloud NAT (port allocation)
gcloud compute routers nats update NAT_CONFIG_NAME \
  --router=ROUTER_NAME \
  --region=REGION \
  --min-ports-per-vm=128 \
  --max-ports-per-vm=512

# Delete Cloud NAT
gcloud compute routers nats delete NAT_CONFIG_NAME \
  --router=ROUTER_NAME \
  --region=REGION

# View Cloud NAT logs (in Cloud Logging)
gcloud logging read "resource.type=nat_gateway" --limit=50
```

### Key Concepts for ACE
- Understanding when Cloud NAT is needed (private VMs accessing internet)
- Creating Cloud Router as prerequisite
- Configuring Cloud NAT with automatic or manual IP allocation
- Selecting which subnets use Cloud NAT
- Understanding port allocation and connection limits
- Enabling logging for monitoring and troubleshooting
- Differentiating Cloud NAT from [[vpc|Private Google Access]]
- Monitoring NAT usage and connection counts

---

## PCA Level

### Architectural Patterns
#### Private GKE with Cloud NAT
- [[gcp/gke|GKE private cluster]] (no external IPs on nodes)
- Cloud NAT for:
  - Pulling images from Docker Hub, gcr.io
  - External API calls
  - Software updates
- **[[vpc|Private Google Access]]** for GCP services
- Secure, no direct internet exposure

#### Multi-Tier Application
- Web tier: Public IPs + [[cloud-load-balancing|Load Balancer]]
- App tier: Private IPs + Cloud NAT (outbound only)
- Database tier: Private IPs, no NAT (internal only)
- Layered security with [[vpc|VPC firewall rules]]

#### Hybrid Cloud with Cloud NAT
- On-premises connected via [[cloud-vpn|Cloud VPN]] or [[cloud-interconnect|Cloud Interconnect]]
- Cloud resources with private IPs
- Cloud NAT for internet-bound traffic
- On-premises traffic via [[cloud-vpn|VPN]]/[[cloud-interconnect|Interconnect]] (no NAT)

#### Multi-Region NAT
- Cloud NAT in each region (regional resource)
- Region-specific NAT IPs
- VMs use NAT in their region
- Global routing for cross-region communication

### High Availability Design
- **Regional redundancy built-in** (no manual setup needed)
- Multiple NAT IPs for higher capacity
- Monitor connection usage to avoid port exhaustion
- Set appropriate timeouts based on application needs
- Unlike AWS: No need for NAT Gateway per AZ

### Security Best Practices
- **Least privilege**: Only NAT subnets that need internet access
- **[[vpc|Firewall rules]]**: Control egress traffic from VMs
- **[[vpc|Private Google Access]]**: Use instead of NAT for Google APIs
- **Logging**: Enable for security monitoring and forensics
- **IP allowlisting**: Use manual NAT IPs for external allowlisting
- **[[gcp/vpc-service-controls|VPC Service Controls]]**: Prevent data exfiltration
- **Monitoring**: Alert on unusual connection patterns

### Performance Optimization
- **Port allocation**:
  - High connection apps: Increase min ports per VM
  - Low connection apps: Use default (64) to conserve ports
- **NAT IP count**:
  - More IPs = more concurrent connections
  - Formula: `NAT IPs needed = (Total connections) / 64,512`
- **Timeout tuning**:
  - Short-lived connections: Lower timeouts (faster port recycling)
  - Long-lived connections: Higher timeouts (avoid premature drops)
- **Regional placement**: Co-locate resources to minimize latency

### Cost Optimization
- **Minimize NAT usage**:
  - Use [[vpc|Private Google Access]] for Google APIs (free)
  - Internal communication via private IPs (no NAT needed)
- **Logging**:
  - Use "Errors only" or "Translations only" to reduce log volume
  - Disable logging if not needed
- **NAT IP allocation**:
  - Automatic allocation: Scales down when not needed
  - Manual allocation: Ensure IPs are actually used (avoid reserved unused IPs)
- **Regional architecture**: Keep traffic within region to avoid NAT egress charges

### Migration Strategies
#### From AWS NAT Gateway
- **AWS**: Need NAT Gateway per AZ for HA
- **GCP**: Single Cloud NAT per region (built-in HA)
- **Migration**:
  - Create Cloud Router in region
  - Create Cloud NAT for subnets
  - Test outbound connectivity
  - Remove external IPs from VMs
- **Cost comparison**: GCP often cheaper (no per-AZ cost)

#### From NAT Instance (AWS) or VM-based NAT
- **Old**: VM running NAT software (iptables, NAT instance)
- **New**: Managed Cloud NAT
- **Benefits**: No VM to maintain, higher availability, better performance
- **Migration**: Enable Cloud NAT, test, decommission NAT VM

### Capacity Planning
#### Connection Calculation
- **Ports per NAT IP**: 64,512
- **Total capacity**: `NAT IPs × 64,512 = Max concurrent connections`
- **Example**: 4 NAT IPs = 258,048 connections

#### Sizing Guidelines
- **Low traffic** (web servers): 1-2 NAT IPs
- **Medium traffic** (app servers): 2-4 NAT IPs
- **High traffic** (data processing): 4-8 NAT IPs
- **Very high traffic** (large scale): 8+ NAT IPs (up to 64)

#### Monitoring Metrics
- **Allocated ports**: Current port usage
- **Port allocation failures**: Indicates port exhaustion
- **Dropped packets**: NAT capacity issues
- **Connection count**: Track vs limit

### Advanced Configurations
#### Subnet-Specific NAT
```bash
# NAT only for specific subnets
gcloud compute routers nats create nat-app-tier \
  --router=my-router \
  --region=us-central1 \
  --nat-custom-subnet-ip-ranges=app-subnet-1,app-subnet-2 \
  --auto-allocate-nat-external-ips
```
**Use case:** Web tier has external IPs, app tier uses NAT

#### Primary Range Only NAT
```bash
# Exclude secondary ranges (GKE pods)
gcloud compute routers nats create nat-primary-only \
  --router=my-router \
  --region=us-central1 \
  --nat-primary-subnet-ip-ranges=SUBNET_NAME \
  --auto-allocate-nat-external-ips
```
**Use case:** GKE nodes use NAT, pods use separate routing

#### Manual NAT IPs for Allowlisting
```bash
# Reserve specific IPs
gcloud compute addresses create nat-ip-1 --region=us-central1
gcloud compute addresses create nat-ip-2 --region=us-central1

# Create NAT with manual IPs
gcloud compute routers nats create nat-manual \
  --router=my-router \
  --region=us-central1 \
  --nat-external-ip-pool=nat-ip-1,nat-ip-2 \
  --nat-all-subnet-ip-ranges
```
**Use case:** External API requires IP allowlisting

### Observability
#### Cloud Monitoring Metrics
- `nat/allocated_ports`: Ports currently allocated
- `nat/port_usage`: Port usage ratio
- `nat/dropped_received_packets_count`: Packets dropped
- `nat/sent_bytes_count`: Data egress volume
- `nat/new_connections_count`: Connection rate

#### Cloud Logging
```bash
# View NAT logs
gcloud logging read "resource.type=nat_gateway AND \
  resource.labels.region=us-central1" \
  --limit=100 \
  --format=json

# Filter by specific VM
gcloud logging read "resource.type=nat_gateway AND \
  jsonPayload.connection.src_ip=\"10.0.1.5\"" \
  --limit=50
```

#### Alerting
- **Port exhaustion**: `allocated_ports` / `total_ports` > 80%
- **Dropped packets**: `dropped_received_packets_count` > threshold
- **Connection failures**: Log-based alert on translation errors

### Troubleshooting
#### Connection Failures
- **Port exhaustion**: Increase NAT IPs or reduce timeouts
- **Firewall rules**: Check egress firewall rules allow traffic
- **Routing**: Verify default route to internet gateway exists
- **Subnet configuration**: Confirm subnet is included in NAT config

#### Performance Issues
- **High latency**: Check Cloud Monitoring for NAT metrics
- **Packet drops**: Increase NAT IP count
- **Timeouts**: Adjust idle timeout settings

#### Debugging Commands
```bash
# Check NAT configuration
gcloud compute routers nats describe NAT_NAME \
  --router=ROUTER_NAME \
  --region=REGION

# View NAT IPs in use
gcloud compute addresses list --filter="region:REGION"

# Test outbound connectivity from VM
# (SSH to VM first)
curl -I http://www.google.com
curl ifconfig.me  # Returns NAT IP
```

### Compliance Considerations
- **IP tracking**: Use manual NAT IPs for audit requirements
- **Logging**: Enable for compliance and forensics
- **Data sovereignty**: NAT traffic routed via Google's network
- **Egress controls**: Monitor and restrict outbound destinations

### Integration with GCP Services
- **[[gcp/gke|GKE]]**: Private clusters with Cloud NAT for outbound
- **[[gcp/compute-engine|Compute Engine]]**: Private VMs with internet access
- **[[gcp/cloud-run|Cloud Run]]**: Use [[gcp/cloud-run|VPC Connector]] + Cloud NAT for outbound
- **[[gcp/cloud-functions|Cloud Functions]]**: [[gcp/cloud-functions|VPC Connector]] + Cloud NAT
- **[[gcp/app-engine|App Engine]]**: Serverless VPC Access + Cloud NAT

### Cloud NAT vs Private Google Access vs VPN
| Feature | Cloud NAT | Private Google Access | VPN/Interconnect |
|---------|-----------|----------------------|------------------|
| Purpose | Internet access | Google APIs access | On-prem connectivity |
| IP translation | Yes | No | No |
| Target | Public internet | Google services | Private networks |
| Requires external IP | For NAT, not VMs | No | No |
| Cost | Gateway + data | Free | Tunnel/port + data |

### Well-Architected Considerations
- **Operational Excellence**: Managed service, no VMs to maintain, automatic scaling
- **Reliability**: Regional redundancy, no single point of failure, 99.95%+ availability
- **Security**: Private VMs, egress control, logging, no direct internet exposure for VMs
- **Performance**: Software-defined, low latency, configurable port allocation, timeout tuning
- **Cost**: Pay for usage, optimize with Private Google Access, efficient IP allocation
- **Sustainability**: Efficient resource usage, software-defined (no dedicated hardware)
