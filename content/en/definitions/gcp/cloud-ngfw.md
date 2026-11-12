---
title: cloud-ngfw
category: GCP
description: 'GCP note: Cloud-ngfw.'
tags:
- gcp
- networking
---


# cloud-ngfw

## Cloud NGFW (Next-Generation Firewall) Enterprise
**Advanced Layer 3-7 stateful firewall** with **intrusion detection/prevention (IDS/IPS)** for VPC networks

**AWS Equivalent:** AWS Network Firewall

### Key Differences from AWS Network Firewall
| Feature | GCP Cloud NGFW Enterprise | AWS Network Firewall |
|---------|---------------------------|----------------------|
| Provider | Powered by **Palo Alto Networks** | AWS-managed |
| Deployment | Managed by Google | Customer-managed endpoints |
| IDS/IPS | **Built-in (advanced threat protection)** | Requires Suricata rules |
| SSL/TLS Inspection | Yes (decrypt and inspect) | Yes |
| URL Filtering | Yes | Domain filtering only |
| Threat Intelligence | Google Threat Intelligence + Palo Alto | AWS threat feeds |
| Scope | VPC network level | VPC subnet level |
| Pricing | Per endpoint + GB processed | Per endpoint + GB processed |

---

## Cloud NGFW vs Other GCP Firewall Services

**Three firewall services in GCP - know the differences:**

| Feature | VPC Firewall Rules | Cloud Armor | Cloud NGFW Enterprise |
|---------|-------------------|-------------|----------------------|
| **OSI Layer** | **Layer 3-4** | **Layer 7** | **Layer 3-7** |
| **Type** | Stateful (connection tracking) | Application firewall | Stateful + IDS/IPS |
| **Scope** | VPC network | Load balancer backend | VPC network |
| **Use Case** | Basic network filtering | Web app protection (WAF) | Advanced threat protection |
| **DDoS Protection** | No | **Yes (built-in)** | Limited |
| **Intrusion Detection** | No | Limited (WAF rules) | **Yes (full IDS/IPS)** |
| **SSL Inspection** | No | No (at LB level) | **Yes** |
| **Threat Intelligence** | No | Limited | **Yes (Google + Palo Alto)** |
| **Cost** | **Free** | Per policy + requests | Per endpoint + GB |
| **Management** | Simple allow/deny rules | Security policies | Advanced rulesets |

**Decision Matrix:**
- **[[vpc#firewall rules|VPC Firewall Rules]]**: Basic IP/port filtering (free, simple)
- **[[cloud-armor|Cloud Armor]]**: Web application protection (WAF, DDoS)
- **Cloud NGFW**: Advanced network security (IDS/IPS, SSL inspection, threat intel)

---

## Cloud NGFW Overview

### What It Is
- **Managed next-generation firewall** service
- Powered by **Palo Alto Networks technology**
- Deployed as **firewall endpoints** in your VPC
- **Stateful inspection**: Tracks connection state
- **Deep packet inspection (DPI)**: Inspects packet contents
- **Threat prevention**: IDS/IPS with signature-based + anomaly detection
- Fully managed by Google (no appliance management)

### Key Capabilities
| Capability | What it does |
|------------|--------------|
| **Layer 3-7 Filtering** | IP, port, protocol, application |
| **Intrusion Detection & Prevention (IDS/IPS)** | Block known threats |
| **SSL/TLS Decryption** | Inspect encrypted traffic |
| **URL Filtering** | Allow/deny based on URL categories |
| **Geo-based Filtering** | Block traffic from specific countries (network layer) |
| **Application Awareness** | Identify and control applications (not just ports) |
| **Threat Intelligence** | Google Cloud Threat Intelligence + Palo Alto feeds |
| **Logging & Monitoring** | Detailed connection and threat logs |

---

## Architecture

### Deployment Model
```text
┌─────────────────────────────────────────┐
│          VPC Network                    │
│                                         │
│  ┌──────────┐    Cloud NGFW    ┌──────┐│
│  │ Subnet A │────Endpoint───────│VM 1  ││
│  └──────────┘       │           └──────┘│
│                     │                   │
│  ┌──────────┐       │           ┌──────┐│
│  │ Subnet B │───────┼───────────│VM 2  ││
│  └──────────┘       │           └──────┘│
│                     │                   │
│                     ▼                   │
│            Threat Intelligence          │
│            (Google + Palo Alto)         │
└─────────────────────────────────────────┘
```

### Components
| Component | Role |
|-----------|------|
| Firewall Endpoint | Logical deployment point in VPC |
| Security Profile Group | Collection of security profiles: Threat Prevention (IDS/IPS), URL Filtering, SSL Decryption, File Blocking |
| Firewall Policy | Rules for traffic inspection and action |
| Threat Intelligence | Cloud-based threat feeds |

---

## Security Profiles

### 1. Threat Prevention (IDS/IPS)
**Purpose**: Detect and block known attacks

**Capabilities:**
- **Signature-based detection**: Known vulnerabilities (CVEs)
- **Anomaly-based detection**: Unusual traffic patterns
- **Protocol anomaly detection**: Malformed packets
- **Actions**:

| Action | Effect |
|--------|--------|
| **Alert** | Log only (IDS mode) |
| **Drop** | Block and log (IPS mode) |
| **Reset** | Terminate connection |

**Threat Categories:**
- Spyware
- Vulnerability exploits
- Viruses
- Command & Control (C2) traffic
- DNS tunneling
- SQL injection
- Cross-site scripting (XSS)

**Update Frequency**: **Automatic signature updates** (Google-managed)

### 2. URL Filtering
**Purpose**: Control web access by URL category

**Categories** (60+ built-in):
- Malware/Phishing sites
- Adult content
- Gambling
- Social media
- File sharing
- Streaming media
- Custom categories (user-defined URLs)

**Actions:**
- Allow
- Block
- Alert (log only)
- Continue (with warning)

### 3. SSL/TLS Decryption
**Purpose**: Inspect encrypted traffic

**Modes:**
- **Decryption**: Decrypt, inspect, re-encrypt
- **No decryption**: Pass through (for trusted apps)

**Use Cases:**
- Detect malware in HTTPS traffic
- Prevent data exfiltration via encrypted channels
- Inspect encrypted C2 traffic

**Considerations:**
- Requires certificate management
- Performance impact (CPU overhead)
- Privacy concerns (inspect internal traffic)

### 4. File Blocking
**Purpose**: Block file transfers by type

**File Types:**
- Executables (.exe, .dll)
- Scripts (.ps1, .bat, .sh)
- Archives (.zip, .rar)
- Office documents (.doc, .xls)
- Custom MIME types

**Directions:**
- Upload (client → server)
- Download (server → client)
- Both

---

## Firewall Policies

### Policy Structure
Similar to VPC firewall rules but with advanced capabilities:

```yaml
# Example: Block malicious traffic, inspect HTTPS
priority: 1000
match:
  srcIpRanges: ["10.0.0.0/8"]
  destIpRanges: ["0.0.0.0/0"]
  layer4Configs:
    - ipProtocol: "tcp"
      ports: ["443"]
action: "allow"  # Allow but inspect
enableLogging: true
securityProfileGroup: "strict-inspection"
```

### Rule Components
- **Priority**: Lower number = higher priority (like VPC firewall rules)
- **Match criteria**:
  - Source/destination IP
  - Layer 4 config (protocol, ports)
  - Direction (ingress/egress)
- **Action**:
  - **allow**: Permit traffic
  - **deny**: Block traffic
  - **apply_security_profile_group**: Inspect with NGFW
- **Security profile group**: Which profiles to apply (threat, URL, SSL)

### Advanced Match Criteria
- **Application**: Match specific applications (not just ports)
  - Example: Block BitTorrent even on non-standard ports
- **Geo-location**: Source/destination country
- **User/Group**: Integrate with identity (advanced)

---

## Deployment Patterns

### Pattern 1: Hub-and-Spoke Security
```text
┌────────────────────────────────────────┐
│       Hub VPC (Security)               │
│   ┌──────────────────────┐             │
│   │  Cloud NGFW Endpoint │             │
│   └──────────┬───────────┘             │
│              │                         │
└──────────────┼─────────────────────────┘
               │ VPC Peering
       ┌───────┴────────┐
       │                │
┌──────▼─────┐    ┌────▼──────┐
│ Spoke VPC 1│    │Spoke VPC 2│
│ (Workloads)│    │(Workloads)│
└────────────┘    └───────────┘
```
**Use case**: Centralized security inspection for multiple VPCs

### Pattern 2: Inline Inspection
```text
Internet
   ↓
Cloud NAT / Cloud VPN
   ↓
Cloud NGFW Endpoint
   ↓
VPC Subnets (workloads)
```
**Use case**: Inspect all north-south traffic (internet-bound)

### Pattern 3: East-West Inspection
```text
VPC Subnet A  →  Cloud NGFW  →  VPC Subnet B
(untrusted)         ↓            (trusted)
                  IDS/IPS
```
**Use case**: Inspect traffic between internal subnets (lateral movement detection)

---

## Use Cases

### 1. Zero-Trust Network Security
**Scenario**: Implement microsegmentation with advanced threat detection
- Inspect all east-west traffic between workloads
- Apply least-privilege network access
- Detect lateral movement attempts
- Log all connections for audit

### 2. Secure Internet Access
**Scenario**: Employees/VMs accessing internet
- URL filtering (block malicious/inappropriate sites)
- Threat prevention (block exploits, malware)
- SSL inspection (detect encrypted threats)
- Data loss prevention (block sensitive file uploads)

### 3. Hybrid Cloud Security
**Scenario**: Secure connectivity between on-premises and GCP
- Inspect Cloud VPN / Cloud Interconnect traffic
- Apply same security policies as on-premises firewall
- Centralized logging and management
- Consistent security posture

### 4. Compliance Requirements
**Scenario**: PCI DSS, HIPAA, regulatory compliance
- IDS/IPS requirement (PCI DSS 11.4)
- Network segmentation (cardholder data environment)
- Detailed logging and auditing
- Threat intelligence integration

### 5. Advanced Persistent Threat (APT) Detection
**Scenario**: Protect against sophisticated attacks
- Signature-based detection (known exploits)
- Anomaly-based detection (zero-day threats)
- C2 traffic detection (beaconing, data exfil)
- SSL inspection (encrypted C2 channels)

---

## Comparison: Cloud NGFW vs VPC Firewall Rules

### When to Use VPC Firewall Rules
✓ Simple allow/deny based on IP/port
✓ Cost-sensitive (free)
✓ Low-latency requirements (minimal overhead)
✓ Basic network segmentation
✓ Allow Google Cloud APIs traffic

**Example**: "Allow TCP port 443 from 10.0.0.0/8 to my web servers"

### When to Use Cloud NGFW Enterprise
✓ Need intrusion detection/prevention (IDS/IPS)
✓ Require SSL/TLS inspection
✓ URL filtering and content inspection
✓ Compliance requirements (PCI DSS IDS/IPS)
✓ Advanced threat protection (APT, zero-day)
✓ Application-aware filtering (not just port-based)
✓ Geo-based filtering at network layer

**Example**: "Block all traffic from China, inspect HTTPS for malware, prevent SQL injection attacks"

### Can Use Both Together
- **VPC Firewall Rules**: Coarse-grained allow/deny (first line)
- **Cloud NGFW**: Deep inspection for allowed traffic (second line)

**Example**:
1. VPC Firewall: Allow HTTPS from internet to web tier
2. Cloud NGFW: Inspect HTTPS traffic for threats, block malicious URLs

---

## ACE Level

### Essential Concepts
Cloud NGFW is **PCA-level** content, less common on ACE exam. ACE focuses on:
- [[vpc#firewall rules|VPC Firewall Rules]] (basic allow/deny)
- [[cloud-armor|Cloud Armor]] (WAF for web apps)

**ACE awareness**: Understand that Cloud NGFW exists for advanced network security, but detailed implementation is PCA-level.

**Key differences to know for ACE**:
- [[vpc#firewall rules|VPC Firewall Rules]] = Basic Layer 3-4
- [[cloud-armor|Cloud Armor]] = Layer 7 WAF (web apps only)
- Cloud NGFW = Advanced Layer 3-7 with IDS/IPS (enterprise)

---

## PCA Level

### Architecture Design Decisions

#### Decision 1: Cloud NGFW vs Cloud Armor
**Question**: "Protect web application from SQL injection and DDoS attacks"

**Answer**: **[[cloud-armor|Cloud Armor]]**
- **Why**: Web application protection (WAF), DDoS included, lower cost
- **Why not Cloud NGFW**: Designed for network-level threats, not web app attacks, higher cost

#### Decision 2: Cloud NGFW vs VPC Firewall Rules
**Question**: "Inspect traffic for known malware signatures and block C2 traffic"

**Answer**: **Cloud NGFW Enterprise**
- **Why**: Requires IDS/IPS, signature-based detection, threat intelligence
- **Why not VPC Firewall**: No deep packet inspection, no threat detection

#### Decision 3: Layered Security
**Question**: "Design defense-in-depth for multi-tier application"

**Answer**: **Use all three together**
```text
Internet
  ↓
Cloud Armor (Layer 7 WAF, DDoS)
  ↓
Load Balancer
  ↓
Cloud NGFW (IDS/IPS, SSL inspection)
  ↓
VPC Firewall Rules (basic allow/deny)
  ↓
Application Tier
```

### High Availability Design
- **Multi-zone deployment**: NGFW endpoints in multiple zones
- **Automatic failover**: Managed by Google (no manual intervention)
- **Scalability**: Auto-scales based on traffic volume
- **No single point of failure**: Redundant endpoints

### Performance Optimization
- **Bypass trusted traffic**: Don't inspect known-safe traffic (Google APIs, internal)
- **Selective SSL decryption**: Decrypt only suspicious traffic (reduce CPU overhead)
- **Profile tuning**: Disable unnecessary profiles (e.g., URL filtering for server-to-server)
- **Rule optimization**: Most permissive rules first (reduce rule evaluation time)

### Cost Optimization
- **Use VPC Firewall Rules first**: Handle simple allow/deny with free rules
- **Cloud NGFW for critical paths only**: Apply to high-risk traffic flows
- **Profile selection**: Only enable needed profiles (threat prevention, not URL filtering for servers)
- **Data transfer**: Minimize inter-zone traffic (Cloud NGFW charges per GB)
- **Right-size endpoints**: Monitor utilization, adjust capacity

**Pricing Model**:
- **Firewall endpoint**: ~$0.0625/hour (~$45/month) per endpoint
- **Data processing**: $0.015 per GB processed
- **Example**: 1 endpoint processing 10 TB/month = $45 + $150 = $195/month

### Security Best Practices
1. **Defense in Depth**: Layer Cloud NGFW with VPC Firewall Rules and Cloud Armor
2. **Least Privilege**: Default deny, explicit allow with NGFW inspection
3. **SSL Inspection**: Enable for untrusted traffic (internet-bound, external APIs)
4. **Threat Intelligence**: Always enabled (automatic updates)
5. **Logging**: Enable comprehensive logging for forensics and compliance
6. **Profile Management**: Use strict profiles for internet-facing, relaxed for internal
7. **Regular Updates**: Security profiles auto-update (verify policy coverage)
8. **Geo-blocking**: Block high-risk countries for internet traffic
9. **Application Control**: Use application-aware rules (not just port-based)
10. **Incident Response**: Integrate logs with [[gcp/cloud-logging|Cloud Logging]] and SIEM

### Migration Strategies

#### From AWS Network Firewall
**Mapping**:

| AWS Network Firewall | Cloud NGFW |
|----------------------|------------|
| Stateful rules | Firewall policies |
| Suricata rules | Threat prevention profiles |
| Domain filtering | URL filtering |
| TLS inspection | SSL decryption |

**Process**:
1. Inventory existing AWS Network Firewall rules
2. Create equivalent Cloud NGFW policies
3. Deploy Cloud NGFW endpoints in VPC
4. Test in log-only mode (alert without blocking)
5. Gradually enable enforcement
6. Monitor for false positives
7. Optimize profiles and rules

#### From On-Premises Palo Alto Networks
**Advantage**: Cloud NGFW uses Palo Alto technology
- Export existing security policies
- Import into Cloud NGFW (compatible format)
- Leverage familiar management paradigm
- Consistent security posture (on-prem + cloud)

### Compliance Considerations

| Framework | Requirement | Cloud NGFW control |
|-----------|-------------|--------------------|
| PCI DSS | **Requirement 11.4**: IDS/IPS for cardholder data environment | Cloud NGFW threat prevention profiles |
| PCI DSS | **Requirement 1.3**: Network segmentation | Cloud NGFW + VPC Firewall Rules |
| HIPAA | Audit logging of all network access | Cloud NGFW comprehensive logging to Cloud Logging |
| HIPAA | Encryption in transit | Enforce TLS (Cloud NGFW policy) |
| HIPAA | Intrusion detection | Cloud NGFW IDS mode (alert on threats) |
| GDPR | Data residency (EU) | Consideration: Cloud NGFW endpoints in EU regions |
| GDPR | Data exfiltration prevention | Cloud NGFW SSL inspection + file blocking |

### Integration with GCP Services
- **[[vpc|VPC]]**: Deployed as VPC firewall endpoints
- **[[cloud-interconnect|Cloud Interconnect]] / [[cloud-vpn|Cloud VPN]]**: Inspect hybrid traffic
- **[[gcp/cloud-logging|Cloud Logging]]**: Centralized logging
- **[[gcp/cloud-monitoring|Cloud Monitoring]]**: Metrics and alerting
- **[[gcp/vpc-service-controls|VPC Service Controls]]**: Perimeter security (complementary)
- **Security Command Center**: Threat findings aggregation
- **Chronicle (Google Cloud SIEM)**: Security analytics and investigation

### Monitoring and Observability

#### Key Metrics (Cloud Monitoring)
| Metric | Meaning |
|--------|---------|
| Connections inspected | Total traffic processed |
| Threats detected | IDS/IPS hits |
| Threats blocked | IPS actions (drop/reset) |
| SSL sessions decrypted | TLS inspection volume |
| URLs blocked | URL filtering hits |
| Endpoint health | Availability of NGFW endpoints |

#### Logging (Cloud Logging)
```bash
# View threat detections
gcloud logging read "resource.type=gce_firewall_endpoint AND \
  jsonPayload.threatName!=null" \
  --limit=100 \
  --format=json

# View blocked connections
gcloud logging read "resource.type=gce_firewall_endpoint AND \
  jsonPayload.action=DROP" \
  --limit=50

# Analyze threat trends
gcloud logging read "resource.type=gce_firewall_endpoint" \
  --format="table(jsonPayload.threatName, jsonPayload.threatSeverity, \
  jsonPayload.srcIp, timestamp)"
```

#### Alerting Policies
- **Critical threat detected**: Severity = Critical
- **High threat volume**: >100 threats/min (potential attack)
- **Endpoint unhealthy**: Availability < 100%
- **Unusual outbound connections**: Potential C2 traffic

### Troubleshooting

#### Issue: Legitimate Traffic Blocked
**Symptom**: Application failing, Cloud NGFW logs show "drop"

**Diagnosis**:
1. Review Cloud Logging for threat name/signature
2. Determine if false positive (legitimate traffic)
3. Check SSL inspection (certificate trust issues)

**Resolution**:
- **False positive**: Add exception to security profile
- **Overly strict policy**: Adjust threat prevention sensitivity
- **SSL issue**: Add trusted certificate or disable decryption for specific destination

#### Issue: High Latency
**Symptom**: Increased network latency after deploying Cloud NGFW

**Diagnosis**:
- Check SSL decryption (CPU overhead)
- Verify endpoint capacity (under-provisioned)
- Review rule complexity (too many rules)

**Resolution**:
- **Selective decryption**: Decrypt only suspicious traffic
- **Scale endpoints**: Add more endpoints or increase capacity
- **Optimize rules**: Consolidate rules, use application-aware rules

#### Issue: Threats Not Detected
**Symptom**: Known malware not blocked

**Diagnosis**:
- Verify security profile enabled
- Check action (alert vs drop)
- Confirm signature coverage (malware type)

**Resolution**:
- **Enable IPS**: Change from alert (IDS) to drop (IPS)
- **Update profiles**: Verify automatic updates enabled
- **Custom signatures**: Add custom threat signatures if needed

### Advanced Configurations

#### Decryption Exclusions
```yaml
# Don't decrypt traffic to trusted domains
sslDecryptionPolicy:
  excludeRules:
    - domains: ["*.google.com", "*.googleapis.com"]
      action: "no-decrypt"
```

#### Geo-Based Policies
```yaml
# Block all traffic from high-risk countries
firewallPolicy:
  rules:
    - priority: 100
      match:
        srcRegionCodes: ["CN", "RU", "KP"]
      action: "deny"
      enableLogging: true
```

#### Application-Aware Rules
```yaml
# Block peer-to-peer applications
firewallPolicy:
  rules:
    - priority: 200
      match:
        applications: ["bittorrent", "kazaa"]
      action: "deny"
      enableLogging: true
```

---

## Well-Architected Considerations

- **Operational Excellence**: Fully managed (no appliance management), automatic threat signature updates, centralized logging
- **Reliability**: Multi-zone deployment, automatic failover, Google-managed infrastructure, 99.99% SLA (regional)
- **Security**: IDS/IPS, SSL/TLS inspection, threat intelligence, URL filtering, application control, comprehensive logging
- **Performance**: Auto-scaling, selective SSL decryption, rule optimization, bypass for trusted traffic
- **Cost**: Pay-per-use (endpoint + GB), optimize with VPC Firewall Rules for simple allow/deny, selective profile usage
- **Sustainability**: Managed service (efficient infrastructure), auto-scaling reduces idle resources

---

## PCA Exam Tips

**Exam will test:**
1. **Service selection**: Cloud NGFW vs Cloud Armor vs VPC Firewall Rules
2. **Use case identification**: When IDS/IPS is required (compliance, threat protection)
3. **Layered security**: Defense-in-depth patterns
4. **Performance vs security trade-offs**: SSL inspection overhead
5. **Cost optimization**: When to use free VPC Firewall Rules vs paid Cloud NGFW

**Common scenarios:**

| Scenario | Answer |
|----------|--------|
| "Requirement: IDS/IPS for PCI DSS compliance" | **Cloud NGFW Enterprise** |
| "Block SQL injection attacks on web application" | **[[cloud-armor|Cloud Armor]]** (WAF) |
| "Allow only TCP 443 from internet to web tier" | **VPC Firewall Rules** (simple, free) |
| "Inspect encrypted traffic for malware" | **Cloud NGFW** (SSL decryption) |
| "Detect and block command & control (C2) traffic" | **Cloud NGFW** (threat intelligence) |
| "DDoS protection for HTTP(S) application" | **[[cloud-armor|Cloud Armor]]** (built-in DDoS) |
| "Block traffic from specific countries to VPC" | **Cloud NGFW** (geo-filtering) or **VPC Firewall Rules** (if IP-based) |

**Key exam distinction**:

| Service | Layer | Attached to | Focus |
|---------|-------|-------------|-------|
| **Cloud Armor** | **Layer 7** (HTTP/HTTPS only) | **Load balancer** | WAF + DDoS |
| **Cloud NGFW** | **Layer 3-7** | **VPC network** | IDS/IPS + threat intel |
| **VPC Firewall Rules** | **Layer 3-4** | **VPC network** | Basic allow/deny |

---

## Related Services

- **[[vpc|VPC]]**: Cloud NGFW deployed as VPC firewall endpoints
- **[[cloud-armor|Cloud Armor]]**: Layer 7 WAF (complementary to Cloud NGFW)
- **[[gcp/vpc-service-controls|VPC Service Controls]]**: Perimeter-based data exfiltration prevention
- **[[gcp/security-command-center|Security Command Center]]**: Centralized security findings
- **[[gcp/cloud-logging|Cloud Logging]]**: NGFW logs and threat detections
- **[[cloud-interconnect|Cloud Interconnect]] / [[cloud-vpn|Cloud VPN]]**: Hybrid connectivity (NGFW inspects traffic)
- **[[gcp/binary-authorization|Binary Authorization]]**: Container image verification
- **[[gcp/identity-aware-proxy|Identity-Aware Proxy]]**: Application-level access control
