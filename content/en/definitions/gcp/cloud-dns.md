---
title: Cloud-dns
category: GCP
description: 'GCP note: Cloud-dns.'
tags:
- gcp
- networking
---


# Cloud-dns

`gcp` `networking`

## Cloud DNS
**AWS Equivalent:** [[networking-route53|Route 53]]
**Managed authoritative DNS** service running on Google's global infrastructure

### Key Differences from AWS Route 53
| Feature | GCP Cloud DNS | AWS Route 53 |
|---------|---------------|--------------|
| Queries/sec | **100% SLA** | 100% SLA |
| Anycast network | Google's global network | AWS global network |
| DNSSEC | Supported | Supported |
| Private zones | Yes | Yes (Private Hosted Zones) |
| Routing policies | **Not available** | 7 types (weighted, latency, etc.) |
| Health checks | Via load balancing only | Native support |
| Pricing | Per zone + queries | Per hosted zone + queries |

---

## DNS Zone Types

### Public Zones
- **Authoritative DNS** for internet-facing domains
- **Publicly visible** on the internet
- Answers queries from any client
- Uses Google's anycast network
- **100 billion queries/day capacity**

### Private Zones
- **Internal DNS** for [[vpc|VPC]] resources
- **Only accessible from specified VPCs**
- Not visible on public internet
- Uses split-horizon DNS
- Queries stay within Google's network

### Forwarding Zones
- Forward DNS queries to another DNS server
- Use cases:
  - On-premises DNS integration
  - Hybrid cloud scenarios
  - Conditional forwarding
- Alternative nameservers (on-prem, other cloud)

### Peering Zones
- **Query private zones in another [[vpc|VPC]]**
- Cross-VPC or cross-project DNS resolution
- Requires [[vpc|VPC]] to be peered or connected
- Use cases: Shared services, multi-project architectures

---

## DNS Records
Supported record types:
- **A**: IPv4 address
- **AAAA**: IPv6 address
- **CNAME**: Canonical name (alias)
- **MX**: Mail exchange
- **TXT**: Text records (SPF, DKIM, verification)
- **NS**: Name server
- **SOA**: Start of authority (auto-managed)
- **SRV**: Service locator
- **PTR**: Reverse DNS lookup
- **CAA**: Certificate authority authorization
- **NAPTR**: Naming authority pointer
- **SPF**: Sender policy framework (deprecated, use TXT)

---

## DNSSEC
**DNS Security Extensions**
- **Cryptographically signs** DNS records
- Protects against cache poisoning and spoofing
- Supported for both public and private zones
- Managed key rotation
- **Enable at zone creation or later**

### DNSSEC Configuration
- **Automatic key management**: Google handles key rotation
- **DS records**: Add to parent zone (registrar)
- **Chain of trust**: From root to your zone
- **Validation**: Resolvers verify signatures

---

## DNS Features

### Split-Horizon DNS
- Same domain name resolves differently:
  - **Internal resolution** for VPC resources
  - **External resolution** for internet clients
- Use case: `example.com` resolves to:
  - Private IP from VPC
  - Public IP from internet

### DNS Policies
- Control DNS resolution behavior for VPCs
- **Inbound forwarding**: Allow on-premises to query Cloud DNS
- **Outbound forwarding**: VPC queries forwarded to alternative servers
- **Alternative name servers**: Custom DNS servers for specific domains

### Inbound Server Policy
- **VMs in VPC can answer DNS queries from on-premises**
- Requires [[cloud-vpn|Cloud VPN]] or [[cloud-interconnect|Cloud Interconnect]]
- Configure on-prem to forward queries to VPC IP ranges
- Use case: On-prem queries for GCP resource names

### Outbound Server Policy
- Forward queries for specific domains to alternative servers
- Use case: On-prem Active Directory DNS
- Example: `*.corp.example.com` → on-premises DNS servers

### DNS Peering
- Consumer VPC queries producer VPC's private zones
- Requires network connectivity (peering, VPN, Interconnect)
- Producer authorizes consumer VPC
- Use case: Shared services DNS

---

## Cloud DNS Routing (Limited)
Unlike AWS Route 53, Cloud DNS does **not support** advanced routing policies:
- ❌ No weighted routing
- ❌ No latency-based routing
- ❌ No geolocation routing
- ❌ No geoproximity routing

**Workaround**: Use [[cloud-load-balancing|Cloud Load Balancing]] for traffic management:
- [[cloud-load-balancing|Global Load Balancer]] handles geo-routing
- Point DNS A record to Load Balancer IP
- Load Balancer distributes to backends

---

## DNS Server Addresses

### Internal DNS
- **Metadata server**: `169.254.169.254` (default)
- **Google's public DNS**: `8.8.8.8`, `8.8.4.4` (can configure)
- Automatically resolves:
  - VPC private zones
  - Public internet domains

### VPC Internal DNS Names
- **Zonal DNS**: `INSTANCE_NAME.ZONE.c.PROJECT_ID.internal`
  - Example: `my-vm.us-central1-a.c.my-project.internal`
- **Global DNS**: `INSTANCE_NAME.c.PROJECT_ID.internal`
  - Example: `my-vm.c.my-project.internal`
- **Custom DNS**: Use private zones for custom names

---

## DNS Query Limits
- **Queries per second**: Unlimited (100 billion/day)
- **Zones per project**: 10,000 (can be increased)
- **Record sets per zone**: 10,000 per zone (public), 100,000 (private)
- **Records per record set**: 100 resource records

---

## Pricing
- **Public zone**: $0.20 per zone per month (first 25 zones)
- **Private zone**: $0.10 per zone per month
- **Queries**:
  - 0-1 billion queries/month: $0.40 per million
  - 1+ billion queries/month: $0.20 per million
- **Inbound forwarding**: $0.10 per million queries

---

## ACE Level

### Essential gcloud Commands
```bash
# Create public DNS zone
gcloud dns managed-zones create ZONE_NAME \
  --dns-name="example.com." \
  --description="Example public zone"

# Create private DNS zone
gcloud dns managed-zones create ZONE_NAME \
  --dns-name="example.internal." \
  --description="Example private zone" \
  --visibility=private \
  --networks=VPC_NAME

# List DNS zones
gcloud dns managed-zones list

# Describe DNS zone
gcloud dns managed-zones describe ZONE_NAME

# Add A record
gcloud dns record-sets create www.example.com. \
  --zone=ZONE_NAME \
  --type=A \
  --ttl=300 \
  --rrdatas="1.2.3.4"

# Add CNAME record
gcloud dns record-sets create blog.example.com. \
  --zone=ZONE_NAME \
  --type=CNAME \
  --ttl=300 \
  --rrdatas="www.example.com."

# List DNS records
gcloud dns record-sets list --zone=ZONE_NAME

# Update record
gcloud dns record-sets update www.example.com. \
  --zone=ZONE_NAME \
  --type=A \
  --ttl=300 \
  --rrdatas="5.6.7.8"

# Delete record
gcloud dns record-sets delete www.example.com. \
  --zone=ZONE_NAME \
  --type=A

# Enable DNSSEC
gcloud dns managed-zones update ZONE_NAME \
  --dnssec-state=on

# Get nameservers
gcloud dns managed-zones describe ZONE_NAME \
  --format="get(nameServers)"

# Create forwarding zone
gcloud dns managed-zones create ZONE_NAME \
  --dns-name="corp.example.com." \
  --description="Forward to on-prem" \
  --visibility=private \
  --networks=VPC_NAME \
  --forwarding-targets=10.0.0.1,10.0.0.2

# Create peering zone
gcloud dns managed-zones create ZONE_NAME \
  --dns-name="shared.example.com." \
  --description="Peer to another VPC" \
  --visibility=private \
  --networks=VPC_NAME \
  --target-network=TARGET_VPC_URL
```

### Key Concepts for ACE
- Creating public and private DNS zones
- Adding and managing DNS records (A, AAAA, CNAME, MX, TXT)
- Understanding TTL and DNS propagation
- Configuring DNSSEC for security
- Using private zones for internal [[vpc|VPC]] resolution
- Forwarding zones for hybrid cloud DNS
- Peering zones for cross-VPC DNS
- Viewing and updating nameservers

---

## PCA Level

### Architectural Patterns
#### Hybrid Cloud DNS Architecture
- **Private zones** in [[vpc|VPC]] for GCP resources
- **Forwarding zones** for on-premises domains
- **Inbound server policy** for on-prem to query GCP
- **Outbound server policy** for GCP to query on-prem
- Requires [[cloud-vpn|Cloud VPN]] or [[cloud-interconnect|Cloud Interconnect]]

**Example:**
```text
On-Premises DNS (corp.local)
     ↕ (forwarding)
Cloud VPN/Interconnect
     ↕
Cloud DNS Forwarding Zone (corp.local → on-prem DNS)
Cloud DNS Private Zone (gcp.corp.local)
     ↕
VPC Resources
```

#### Multi-Project DNS Architecture
- **[[vpc|Shared VPC]]**: Host project manages DNS zones
- **DNS Peering**: Service projects peer to host DNS zones
- Centralized DNS management
- Consistent naming across projects

#### Multi-Cloud DNS
- Cloud DNS for GCP resources
- AWS Route 53 for AWS resources
- Conditional forwarding between clouds
- Or: Single cloud for DNS, forward from other clouds

#### Global Application with DNS
- Cloud DNS public zone for domain
- A record → [[cloud-load-balancing|Global Load Balancer]] IP
- Load Balancer handles geo-routing
- Multiple backend regions for low latency

### High Availability Design
- **Cloud DNS SLA**: **100% availability**
- **Anycast network**: Google's global infrastructure
- **Multiple nameservers**: 4+ NS records automatically
- **Redundant forwarding targets**: Multiple IPs for forwarding zones
- **Zone redundancy**: Cloud DNS automatically redundant

### Security Best Practices
- **DNSSEC**: **Enable for all public zones**
  - Protects against DNS spoofing
  - Automatic key rotation
  - Validate with DNS checker tools
- **Private zones**: Use for internal resources
  - Never expose internal IPs publicly
  - Restrict to specific [[vpc|VPCs]]
- **[[gcp/vpc-service-controls|VPC Service Controls]]**: Protect DNS zones
- **[[gcp/iam|IAM]]**: Least privilege for DNS management
  - `roles/dns.admin`: Full DNS management
  - `roles/dns.reader`: Read-only access
- **Audit logging**: Track DNS zone changes

### Performance Optimization
- **TTL tuning**:
  - Lower TTL (60-300s) for frequently changing records
  - Higher TTL (3600s+) for static records
  - Balance between cache efficiency and update speed
- **Anycast network**: **Automatic low-latency routing**
- **Private zones**: Faster resolution within VPC (no internet)
- **Record limits**: Stay within limits for best performance
  - <10,000 record sets per zone recommended

### Cost Optimization
- **Consolidate zones**: Fewer zones = lower cost
- **Public vs private zones**: Private zones are cheaper ($0.10 vs $0.20)
- **Query optimization**: Cache DNS responses at application level
- **High query volumes**: Lower per-query cost at >1 billion queries/month
- **Delete unused zones**: Avoid charges for inactive zones

### Migration Strategies
#### From AWS Route 53
- **Export Route 53 records**: Use AWS CLI
- **Create Cloud DNS zones**: Map hosted zones
- **Import records**: Use `gcloud` or Console import
- **Update NS records**: At domain registrar
- **Monitor TTL expiration**: Wait for old records to expire
- **Validate resolution**: Test from multiple locations

#### From On-Premises DNS
- **Inventory DNS zones and records**
- **Create Cloud DNS zones** (public/private)
- **Migrate records incrementally** per domain
- **Hybrid period**: Use forwarding zones
- **Update resolvers**: Point to Cloud DNS
- **Decommission on-prem DNS** gradually

#### Hybrid Migration Pattern
- **Phase 1**: Forwarding zone in Cloud DNS → on-prem
- **Phase 2**: Migrate records to Cloud DNS private zone
- **Phase 3**: Inbound policy for on-prem to query Cloud DNS
- **Phase 4**: Update on-prem resolvers to use Cloud DNS
- **Phase 5**: Decommission on-prem DNS

### Advanced DNS Configurations
#### Split-Horizon DNS Setup
**Public zone:**
- `example.com` → `A` record → `35.190.1.100` (public IP)

**Private zone:**
- `example.com` → `A` record → `10.0.1.10` (private IP)
- Only accessible from VPC

**Result:**
- Internet clients resolve to public IP
- VPC resources resolve to private IP

#### Multi-VPC DNS Peering
**Producer VPC (Shared Services):**
- Private zone: `shared.example.internal`
- Records for shared services (databases, APIs)

**Consumer VPC (Applications):**
- Peering zone: `shared.example.internal` → Producer VPC
- Can resolve `db.shared.example.internal` → Producer's private IP

#### Conditional Forwarding
**Scenario:** Resolve corporate domains to on-prem DNS
```bash
# Forwarding zone for corp.example.com
gcloud dns managed-zones create corp-forward \
  --dns-name="corp.example.com." \
  --visibility=private \
  --networks=vpc-name \
  --forwarding-targets=10.10.1.10,10.10.1.11
```
**Result:** Queries for `*.corp.example.com` forwarded to `10.10.1.10`, `10.10.1.11`

### DNS Policies
#### Inbound Server Policy
**Use case:** On-premises queries Cloud DNS
```bash
# Enable inbound forwarding
gcloud dns policies create inbound-policy \
  --enable-inbound-forwarding \
  --networks=vpc-name
```
**On-prem configuration:**
- Forward `gcp.example.internal` to VPC IP ranges (e.g., `10.0.0.2`)

#### Outbound Server Policy
**Use case:** VPC queries on-premises DNS
```bash
# Alternative name servers for specific domains
gcloud dns policies create outbound-policy \
  --networks=vpc-name \
  --alternative-name-servers=10.10.1.10,10.10.1.11 \
  --private-alternative-name-servers=corp.example.com.
```

### Observability
- **[[gcp/cloud-monitoring|Cloud Monitoring]]**:
  - Query count per zone
  - Query response time
  - DNSSEC validation failures
- **[[gcp/cloud-logging|Cloud Logging]]**:
  - DNS query logs (must enable)
  - Zone configuration changes
  - DNSSEC key rotation events
- **DNS Query Logging**:
  - **Not enabled by default** (performance impact)
  - Enable for troubleshooting or compliance
  - Sent to [[gcp/cloud-logging|Cloud Logging]]

### Troubleshooting
#### DNS Resolution Issues
- **Verify zone visibility**: Public vs private
- **Check VPC network**: Private zones attached to correct VPC
- **Validate record syntax**: Proper FQDN format (trailing dot)
- **TTL consideration**: Wait for TTL expiration after changes
- **DNSSEC validation**: Check for DNSSEC errors

#### Tools
```bash
# Query Cloud DNS directly
dig @8.8.8.8 example.com

# Query private zone from VM
dig @169.254.169.254 internal.example.com

# Check DNSSEC
dig example.com +dnssec

# Trace DNS resolution
dig example.com +trace
```

### Integration with Other GCP Services
- **[[cloud-load-balancing|Cloud Load Balancing]]**: DNS → LB IP for global routing
- **[[gcp/compute-engine|Compute Engine]]**: Automatic internal DNS names
- **[[gcp/gke|GKE]]**: CoreDNS with Cloud DNS integration
- **[[gcp/cloud-run|Cloud Run]]**: Custom domains with Cloud DNS
- **[[gcp/app-engine|App Engine]]**: Custom domains mapped via DNS

### Compliance Considerations
- **DNSSEC**: Required for many compliance frameworks
- **Audit logging**: Track all DNS changes
- **Private zones**: Keep internal names private
- **Data residency**: DNS data stored globally (consider for compliance)
- **VPC Service Controls**: Protect DNS zones from data exfiltration

### Capacity Planning
- **Zones**: Plan for organizational structure
- **Record sets**: <10,000 per zone for best performance
- **Query volume**: Monitor and forecast
- **Forwarding targets**: Multiple for redundancy
- **TTL strategy**: Balance caching vs flexibility

### DNSSEC Key Management
- **Automatic rotation**: Google manages key lifecycle
- **Key types**:
  - Zone Signing Key (ZSK): Signs records, rotates every 30 days
  - Key Signing Key (KSK): Signs ZSK, rotates every 60 days
- **DS record**: Must update at registrar after KSK rotation
- **Monitoring**: Alert on DNSSEC validation failures

### Well-Architected Considerations
- **Operational Excellence**: Managed service, automatic DNSSEC rotation, minimal maintenance
- **Reliability**: 100% SLA, global anycast, automatic redundancy, multi-NS records
- **Security**: DNSSEC, private zones, IAM controls, VPC Service Controls, audit logging
- **Performance**: Global anycast, low latency, TTL optimization, private zone speed
- **Cost**: Consolidate zones, optimize queries, use private zones where applicable
- **Sustainability**: Efficient global infrastructure, minimal operational overhead
