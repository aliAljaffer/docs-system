---
title: cloud-vpn
category: GCP
description: 'GCP note: Cloud-vpn.'
tags:
- gcp
- networking
---


# cloud-vpn

`gcp` `networking`

## Cloud VPN
**IPsec virtual private network (VPN)** connection between Google Cloud [[vpc|VPC]] and on-premises or other cloud networks

**AWS Equivalent:** AWS Site-to-Site VPN

### Key Differences from AWS VPN
| Feature | GCP Cloud VPN | AWS Site-to-Site VPN |
|---------|---------------|----------------------|
| HA SLA | **99.99%** with HA VPN | 99.95% (two tunnels) |
| BGP required | **Required for HA VPN** | Optional |
| Redundancy | 2 tunnels minimum (HA) | 2 tunnels recommended |
| Throughput | 3 Gbps per tunnel | 1.25 Gbps per connection |
| Routing | Static or dynamic (BGP) | Static or dynamic (BGP) |
| Cost | Per tunnel-hour | Per connection-hour |

### Cloud VPN Types
| Aspect | HA VPN (**Recommended**) | Classic VPN (**Legacy**) |
|--------|--------------------------|--------------------------|
| SLA | **99.99%** when configured with two tunnels | **99.9%** with two tunnels |
| Routing | **Requires BGP** (dynamic routing) | Static or dynamic routing |
| External IPs | Two external IP addresses on GCP side | Single external IP address |
| Tunnels | **Supports multiple tunnels per gateway** | - |
| Resource | Regional resource with automatic redundancy | - |
| Status | Introduced in 2019, replaces Classic VPN | **Not recommended for new deployments**. Will be deprecated eventually |

---

## HA VPN

### HA VPN Gateway
- Regional resource with **two interfaces**
- Each interface has its own external IP
- **Active/active** configuration
- Supports up to 8 tunnels per gateway
- IPv4 only (IPv6 not supported)

### HA VPN Topologies
#### To On-Premises (Recommended)
| On-prem setup | GCP interfaces | Tunnels | SLA | Notes |
|---------------|----------------|---------|-----|-------|
| **Two on-prem VPN devices** | 2 GCP interfaces → 2 on-prem devices | 4 total (2 per device) | **99.99%** | Full redundancy |
| **Single on-prem VPN device with 2 interfaces** | 2 GCP interfaces → 2 interfaces on 1 device | 4 total | 99.99% | Device is single point of failure |
| **Single on-prem VPN device with 1 interface** | 1 GCP interface → 1 on-prem interface | 2 | **99.9%** | Minimal redundancy |

#### To Another GCP VPC (VPC-to-VPC)
- HA VPN gateway in each [[vpc|VPC]]
- 2 tunnels between gateways
- Use cases: Multi-project, multi-organization connectivity
- **Consider [[vpc#vpc peering|VPC Peering]] instead** (better performance, no cost)

#### To AWS (GCP-to-AWS)
- HA VPN in GCP
- AWS Virtual Private Gateway or Transit Gateway
- 4 tunnels for full redundancy
- BGP required on both sides

### Cloud Router (Required for HA VPN)
**AWS Equivalent:** Virtual Private Gateway (for BGP)
- Managed BGP service
- **Dynamically exchanges routes** between VPC and on-premises
- Regional resource
- Supports custom BGP advertisements
- ASN: 64512-65534 (private), 4200000000-4294967294 (4-byte)
- **Required for HA VPN**

#### BGP Configuration
- **ASN**: Autonomous System Number for your network
- **BGP sessions**: One per tunnel
- **Route priorities**: MED (Multi-Exit Discriminator) for preferring routes
- **Graceful restart**: Maintains routes during BGP session reset

### Tunnel Configuration
| Setting | Value |
|---------|-------|
| **IKE version** | IKEv2 (recommended) or IKEv1 |
| **Shared secret** | Pre-shared key for authentication |
| **Encryption** | AES-128, AES-256, 3DES |
| **Integrity** | SHA-1, SHA-256, SHA-384, SHA-512 |
| **Perfect Forward Secrecy** | DH groups 2, 5, 14-24 |
| **MTU** | 1460 bytes (default), max 1460 |

### VPN Throughput
- **3 Gbps per tunnel**
- **15 Gbps per gateway** (with 8 tunnels)
- Multiple tunnels for higher throughput
- Use [[cloud-interconnect|Cloud Interconnect]] for >15 Gbps

---

## Classic VPN

### Classic VPN Gateway
- Regional resource with **single external IP**
- Supports static or dynamic routing
- Target VPN Gateway resource
- **Not recommended for new deployments**

### Routing Modes (Classic VPN)
| Aspect | Static routing | Dynamic routing |
|--------|----------------|-----------------|
| Cloud Router | No Cloud Router required | Requires Cloud Router |
| Route exchange | Manually configure routes on both sides. Cannot automatically learn new routes | BGP-based route exchange. Automatically propagates route changes |
| Fit | Simple but not scalable | **Preferred over static routing** |

---

## Configuration Steps (HA VPN)

### GCP Side
1. **Create HA VPN Gateway** in target VPC and region
2. **Create Cloud Router** in same region (if not exists)
3. **Create VPN Tunnels** (2 or 4 depending on topology)
   - Configure peer IP addresses
   - Set IKE version and shared secret
4. **Create BGP sessions** on Cloud Router
   - One BGP session per tunnel
   - Configure ASNs and IP ranges

### On-Premises Side
1. **Configure VPN device** with GCP tunnel details
2. **Set up BGP** with Cloud Router ASN
3. **Configure firewall** to allow VPN traffic (UDP 500, 4500)
4. **Test connectivity** and monitor tunnel status

---

## Routing Configuration

### Dynamic Routing Mode
Configured at [[vpc|VPC]] level, affects Cloud Router behavior:
- **Regional**: Routes learned in one region stay in that region
- **Global**: Routes learned in one region **propagate to all regions**
  - Required for multi-region VPN connectivity
  - Slightly higher cost

### Route Priorities
- **Base priority**: 100 (default for BGP routes)
- Lower number = higher priority
- Use for active/passive failover
- Adjust via Cloud Router custom advertisements

### Custom Route Advertisements
- Advertise specific IP ranges to on-premises
- Suppress default VPC routes
- Useful for fine-grained traffic control

---

## Monitoring and Troubleshooting

### Tunnel Status
| Status | Meaning |
|--------|---------|
| **Established** | Tunnel is up and running |
| **Waiting for full config** | Configuration incomplete |
| **Network error** | Connectivity issues |
| **Authorization error** | Shared secret mismatch |

### Metrics (Cloud Monitoring)
- **Tunnel established**: Boolean (up/down)
- **Sent/received bytes**: Throughput
- **Sent/received packets**: Packet count
- **Dropped packets**: Indicates issues

### Logs
- [[gcp/cloud-logging|Cloud Logging]] for VPN events
- BGP session events
- Tunnel state changes

### Common Issues
| Issue | Fix |
|-------|-----|
| **Shared secret mismatch** | Check both sides |
| **MTU issues** | Set MTU to 1460 or lower |
| **Firewall blocking** | Allow UDP 500, 4500, ESP (IP protocol 50) |
| **Routing issues** | Verify Cloud Router BGP configuration |
| **ASN conflicts** | Ensure unique ASNs |

---

## Security

### Encryption
- **All traffic encrypted** with IPsec
- Strong cipher suites supported
- IKEv2 recommended for better security

### Authentication
- Pre-shared key (PSK)
- **Rotate keys regularly** for security

### Firewall Rules
- Create [[vpc#firewall rules|VPC firewall rules]] for VPN traffic
- Allow traffic from on-premises IP ranges
- Use tags for granular control

---

## Pricing
- **HA VPN**: Per tunnel-hour + egress traffic
  - Tunnel: ~$0.05/hour per tunnel
  - Egress: Standard internet egress rates
- **Classic VPN**: Similar pricing
- **Cloud Router**: No additional charge (included)
- **No charge**: For traffic between VPN and VPC resources

---

## ACE Level

### Essential gcloud Commands
```bash
# Create HA VPN gateway
gcloud compute vpn-gateways create HA_VPN_GW_NAME \
  --network=VPC_NAME \
  --region=REGION

# Create Cloud Router (if not exists)
gcloud compute routers create ROUTER_NAME \
  --region=REGION \
  --network=VPC_NAME \
  --asn=65001

# Create VPN tunnel
gcloud compute vpn-tunnels create TUNNEL_NAME \
  --peer-gcp-gateway=PEER_VPN_GW_NAME \
  --region=REGION \
  --ike-version=2 \
  --shared-secret=SHARED_SECRET \
  --router=ROUTER_NAME \
  --vpn-gateway=HA_VPN_GW_NAME \
  --interface=0

# Create BGP session
gcloud compute routers add-interface ROUTER_NAME \
  --interface-name=INTERFACE_NAME \
  --vpn-tunnel=TUNNEL_NAME \
  --region=REGION

gcloud compute routers add-bgp-peer ROUTER_NAME \
  --peer-name=BGP_PEER_NAME \
  --peer-asn=PEER_ASN \
  --interface=INTERFACE_NAME \
  --region=REGION

# List VPN gateways
gcloud compute vpn-gateways list

# List VPN tunnels
gcloud compute vpn-tunnels list

# Describe VPN tunnel
gcloud compute vpn-tunnels describe TUNNEL_NAME --region=REGION

# View Cloud Router status
gcloud compute routers get-status ROUTER_NAME --region=REGION

# Delete VPN tunnel
gcloud compute vpn-tunnels delete TUNNEL_NAME --region=REGION
```

### Key Concepts for ACE
- Understanding difference between HA VPN and Classic VPN
- Creating HA VPN gateways with two interfaces
- Configuring Cloud Router for BGP
- Setting up VPN tunnels with proper encryption
- Monitoring tunnel status and troubleshooting
- Understanding regional vs global routing modes
- Calculating required number of tunnels for SLA
- Basic BGP concepts (ASN, peering)

---

## PCA Level

### Architectural Patterns
#### Hybrid Cloud Connectivity
- HA VPN for secure connection to on-premises
- Multiple tunnels for redundancy and throughput
- BGP for automatic failover
- [[cloud-interconnect|Cloud Interconnect]] for higher bandwidth needs
- Split traffic: VPN for control plane, Interconnect for data plane

#### Multi-Cloud Connectivity
- HA VPN between GCP and AWS/Azure
- BGP for dynamic routing
- Multiple tunnels for redundancy
- Consider network throughput requirements
- Latency-sensitive workloads may need Interconnect

#### Disaster Recovery
- VPN for DR site connectivity
- Active/passive configuration
- Route priorities for failover
- Regular DR testing via tunnel switching

#### Multi-Region Hub-and-Spoke
- Central hub VPC with HA VPN to on-premises
- Spoke VPCs connected via [[vpc#vpc peering|VPC Peering]]
- Global routing mode for cross-region communication
- Centralized egress to on-premises

### High Availability Design
- **99.99% SLA**:
  - 2 on-prem VPN devices
  - 4 tunnels minimum
  - BGP for automatic failover
- **Multi-region redundancy**:
  - VPN gateways in multiple regions
  - Global routing mode
  - Cloud Router in each region
- **Monitoring**:
  - Alert on tunnel down
  - BGP session monitoring
  - Throughput and latency tracking

### Performance Optimization
- **Throughput**:
  - 3 Gbps per tunnel
  - Use 4+ tunnels for 12+ Gbps
  - Consider [[cloud-interconnect|Cloud Interconnect]] for >15 Gbps
- **Latency**:
  - VPN adds ~10-30ms latency
  - Choose region closest to on-premises
  - Use Premium network tier
- **MTU**:
  - Set to 1460 to avoid fragmentation
  - Test with ping: `ping -M do -s 1432 IP_ADDRESS`

### Security Best Practices
- **Strong encryption**: AES-256, IKEv2
- **Key rotation**: Rotate shared secrets regularly
- **Firewall rules**: Restrict to specific IP ranges
- **Private IP addressing**: Use RFC 1918 ranges
- **VPN monitoring**: Alert on tunnel status changes
- **Least privilege**: Restrict Cloud Router permissions

### Cost Optimization
- **VPN vs Interconnect**:
  - VPN: Lower cost, suitable for <10 Gbps
  - Interconnect: Higher cost, better for >10 Gbps sustained
- **Tunnel consolidation**: Use fewer tunnels if throughput allows
- **Regional placement**: Co-locate resources to minimize egress
- **Committed Use Discounts**: Not applicable to VPN, but to VPC resources

### BGP Design Considerations
- **ASN selection**: Use private ASNs (64512-65534)
- **Route filtering**: Advertise only necessary routes
- **Route priorities**: Use MED for active/passive
- **Graceful restart**: Enable for minimal downtime during restarts
- **BFD (Bidirectional Forwarding Detection)**: Faster failure detection
  - Detect failures in seconds vs minutes
  - Recommended for HA configurations

### Migration Strategies
#### From AWS Site-to-Site VPN
- Similar architecture, easier setup in GCP
- AWS: 2 tunnels per connection (1.25 Gbps each)
- GCP: Multiple tunnels per gateway (3 Gbps each)
- BGP configuration similar on both platforms
- Test connectivity before cutover

#### From Direct Connect to Cloud VPN
- Temporary VPN for migration
- Gradual traffic shift
- Keep Direct Connect as backup during migration
- Final cutover to Cloud Interconnect

### Capacity Planning
- **Tunnel count**: Based on throughput needs

| Throughput | Tunnels |
|------------|---------|
| 1-3 Gbps | 2 tunnels (HA) |
| 3-6 Gbps | 4 tunnels |
| 6-15 Gbps | 8 tunnels (max per gateway) |
| >15 Gbps | Multiple gateways or use Interconnect |

- **Egress bandwidth**: Monitor and forecast
- **BGP routes**: Max 100-200 routes per Cloud Router (soft limit)

### Compliance Considerations
- **Encryption**: Meets FIPS 140-2 requirements
- **Data sovereignty**: Choose region based on regulations
- **Audit logging**: Enable for compliance tracking
- **Private connectivity**: No internet exposure for VPN traffic

### Observability
- **[[gcp/cloud-monitoring|Cloud Monitoring]]**:
  - Tunnel status (up/down)
  - Throughput (bytes sent/received)
  - Packet drops
- **[[gcp/cloud-logging|Cloud Logging]]**:
  - Tunnel establishment events
  - BGP session changes
  - Configuration changes
- **Alerting**:
  - Tunnel down
  - High packet loss
  - BGP session flapping

### Advanced Configurations
#### Route-Based vs Policy-Based VPN
- GCP uses **route-based VPN**
- On-prem devices may use policy-based
- May require NAT-T for policy-based compatibility

#### ECMP (Equal-Cost Multi-Path)
- Multiple tunnels with same cost
- Load balancing across tunnels
- Better throughput utilization
- Enabled by default with BGP

#### VPN Tunnel Redundancy Patterns
| Pattern | Routing |
|---------|---------|
| **Active/Active** | Equal cost routes, ECMP load balancing |
| **Active/Passive** | Different route priorities, failover only |
| **Active/Active with Unequal Cost** | Weighted load balancing via MED |

### VPN vs VPC Peering vs Cloud Interconnect
| Feature | Cloud VPN | VPC Peering | Cloud Interconnect |
|---------|-----------|-------------|-------------------|
| Connectivity | Encrypted tunnel | Direct VPC connection | Dedicated circuit |
| Throughput | 3 Gbps/tunnel, 15 Gbps/gateway | 100+ Gbps | 10-200 Gbps |
| Latency | +10-30ms | Native VPC latency | Lowest latency |
| Cost | Moderate (tunnel + egress) | Low (egress only) | High (port + egress) |
| Use case | Hybrid, multi-cloud | VPC-to-VPC within GCP | High bandwidth hybrid |

### Well-Architected Considerations
- **Operational Excellence**: Managed service, automatic failover with BGP, monitoring
- **Reliability**: 99.99% SLA with HA VPN, multiple tunnels, regional redundancy
- **Security**: IPsec encryption, strong ciphers, firewall rules, key rotation
- **Performance**: 3 Gbps per tunnel, ECMP load balancing, low latency routing
- **Cost**: Pay per tunnel-hour, optimize tunnel count, consider Interconnect for high bandwidth
- **Sustainability**: Efficient routing, minimize unnecessary traffic, use regional resources
