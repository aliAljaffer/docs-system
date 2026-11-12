# 2. Network security

**Goal:** Control traffic with firewalls, load balancers, Cloud Armor, and private connectivity.

## Firewall layers

Google Cloud has three firewall layers. Each layer attaches at a different level.

| Layer | Attaches to | Notes |
|---|---|---|
| Hierarchical firewall policies | Organization or folder | Child projects inherit them. Projects cannot bypass them. |
| Global network firewall policies | [[vpc|VPC]] network | Replace per-VPC rules. Support threat inspection. |
| Classic VPC firewall rules | VPC network | Still exist. Implied rules at priority 65535: allow egress, deny ingress. |

[[cloud-ngfw]] tiers:

| Tier | Includes |
|---|---|
| Essentials | Rules and logging |
| Enterprise | Adds Layer 7 filtering and TLS inspection with security profiles. Profiles include Palo Alto Networks and CrowdStrike threat lists. |
| Plus | Adds advanced EDR-based features |

Firewall endpoints are required for Enterprise and Plus inspection. They are billed.

Layer 7 inspection works only in global network firewall policies with security profile groups. Encrypted traffic needs TLS inspection with a trust config.

### Rule behavior

- Firewall rules attach to a VPC, not to one subnet or VM.
- Targets are all instances, network tags, or service accounts. A rule uses tags or service accounts, not both.
- Service account targets are safer. Attaching a service account needs an [[iam|IAM]] permission. Network tags need none.
- Ingress rules cannot use destination ranges. Egress rules cannot use source ranges. An omitted source or destination means 0.0.0.0/0.
- `--source-ranges` and `--source-tags` together form a union. A tagged VM matches even outside the ranges.
- Priority runs from 0 to 65535. Lower numbers win. The default is 1000.
- Deny overrides allow only at equal priority. Otherwise, the lower number wins, whatever the action.
- You cannot change a rule's direction or action. Create the new rule, then delete the old one.
- Firewall Rules Logging is set per rule. It never applies to implied rules. Logs go to [[cloud-logging]], [[pub-sub]], or [[bigquery]].
- Secure tags create identity-based rules. Tag a VM, then write rules against the tag.

## Load balancers and edge controls

- External load balancers accept internet traffic. Internal load balancers accept RFC 1918 traffic only. Exposure and scope are separate settings.
- Set SSL policies to control the minimum TLS version and ciphers.
- Use Google-managed certificates where possible.
- [[cloud-armor]] attaches to external global load balancer backends.

## Cloud Armor

Cloud Armor is the WAF and DDoS product at the edge.

- Security policies attach to external HTTPS and TCP proxy load balancer backends and to Cloud CDN.
- Rule types: IP and CIDR allow or deny, CEL expressions, preconfigured WAF rules, and geo-based rules.
- Preconfigured WAF rules use ModSecurity CRS. They detect SQLi, XSS, LFI, RFI, RCE, and scanners.
- Preconfigured WAF sensitivity runs from 0 to 4. Level N enables signatures up to N. A lower level gives higher confidence and fewer false positives.
- Rate limiting throttles or bans clients. Use the enforce action.
- Adaptive Protection detects L7 DDoS with machine learning and suggests rules. Full alerts need Cloud Armor Enterprise (formerly Managed Protection Plus).
- Bot management integrates with reCAPTCHA.
- Edge security policies protect CDN content. Named IP lists hold third-party [[threat-intelligence|threat intelligence]].
- Rule priority runs from 0 to 2147483647. The default rule sits at 2147483647. Actions include `deny-404` and `deny-502`.
- Backends can be serverless NEGs, internet NEGs, or [[cloud-storage|Cloud Storage]] buckets.

## Identity-Aware Proxy (IAP)

- Enable [[identity-aware-proxy|IAP]] on a backend service or for TCP forwarding.
- Control access with the `roles/iap.httpsResourceAccessor` role.
- Add access levels for context-aware access.
- TCP forwarding gives SSH and RDP access without public IPs or bastion hosts.

## Private connectivity

| Need | Answer |
|---|---|
| VMs without public IPs reach Google APIs | Private Google Access on the subnet |
| On-premises hosts reach Google APIs over VPN or Interconnect | Private Google Access for on-premises hosts, a route for the VIPs, and a DNS zone for `googleapis.com` |
| Allow only Google APIs that support [[vpc-service-controls|VPC Service Controls]] | `restricted.googleapis.com` VIP (199.36.153.4/30) with DNS |
| Private access to one managed service | Private Service Connect (PSC) endpoint |
| Outbound internet from private VMs | [[cloud-nat]] |
| On-premises to VPC | HA VPN or [[cloud-interconnect]] |
| VPC to VPC | Peering or Shared VPC |

See [[private-google-access-vs-psc]] for the full comparison.

- Private Google Access is a per-subnet setting. It needs `compute.subnetworks.setPrivateIpGoogleAccess`.
- Private Google Access traffic uses public VIPs. PSC traffic uses internal IPs.
- API bundles: `all-apis` maps to `private.googleapis.com`. `vpc-sc` maps to `restricted.googleapis.com`.
- For `googleapis.com`, `gcr.io`, and `pkg.dev`, create a private DNS zone that points at the restricted or private VIPs.
- PSC endpoints get an internal IP in your subnet. They need the Service Directory and [[cloud-dns|Cloud DNS]] APIs, and the `servicedirectory.editor` and `dns.admin` roles.

### Cloud NAT

- Cloud NAT is regional. It does SNAT only. It allows no inbound connections.
- Use manual or automatic NAT IP addresses.
- Each NAT IP gives 64,512 TCP and 64,512 UDP ports.
- Subnet scope options: all subnet IP ranges, primary ranges, or custom ranges.

### HA VPN and Cloud Interconnect

| Feature | HA VPN | Dedicated Interconnect |
|---|---|---|
| Encryption | IPsec | Not encrypted by default. Add IPsec or MACsec. |
| Capacity | 3 Gbps per tunnel | 10 or 100 Gbps |
| Requirements | One gateway with two interfaces and two reserved public IPs. At least two tunnels from the same region. BGP. | A colocation facility. LACP, eBGP-4, and 802.1Q. |
| SLA | 99.99% | - |

- Use [[cloud-interconnect]] for more than 3 Gbps or lower latency.
- Each VLAN attachment pairs with a Cloud Router BGP session.

### Cloud DNS security

- DNSSEC signing states: on, transfer, off.
- Response policies provide split-horizon DNS.
- Forwarding zone targets must be public IPs. RFC 1918 targets work only over VPN or Interconnect.
- DNS peering is one way. The producer needs `dns.networks.targetWithPeeringZone`.

## VPC design

| Factor | VPC peering | Shared VPC |
|---|---|---|
| Scope | Network to network | Service projects attach to a host project |
| IAM separation | None | Host admins control the network. Service project admins control their resources. |
| Transitive routing | No | Not covered in the notes |
| Subnet control | Not applicable | Org policy `compute.restrictSharedVpcSubnetworks` |

- Shared VPC needs an organization. Setup needs `compute.xpnAdmin` and `resourcemanager.projectIamAdmin` at the organization or folder, and `compute.networkUser` per subnet.
- The Compute API must be enabled in the host and service projects. The service project pays for its compute.
- VMs in different service projects reach each other by internal routing. Use firewall rules to restrict that traffic.
- Peering limits: no overlapping [[cidr]] ranges. Firewall rules cannot use tags or service accounts from the peer network, so use IP ranges. Internal Compute Engine DNS does not resolve across peering. Peering is not transitive.

## VPC Service Controls

- Create an access policy at the organization level. Then create perimeters around projects.
- Inside a perimeter, services refuse requests from outside. An access level or ingress rule can allow them.
- Enforced denials return HTTP 403 and name the perimeter.
- Dry run mode logs would-be violations. Deploy in dry run first.
- Ingress rules match identity, access level, service, and resource.
- Egress rules control which data can leave, to external projects or identities.
- Bridges allow specified service interactions between two perimeters.
- Perimeters take projects only (`projects/<number>`). A project belongs to one perimeter.
- Access levels gate ingress only. Basic attributes: `ipSubnetworks` (no RFC 1918), `regions`, `members`, and `devicePolicy`. A custom level is one CEL expression over `origin`, `request.auth`, `levels`, and `device`.
- Limits: some services are not supported. Each project lists its services. Third-party client libraries need DNS and routing to the restricted VIPs.
- Prerequisites: enable the Access Context Manager API. Grant `roles/accesscontextmanager.policyAdmin`.

Exam pattern: "Block data exfiltration from BigQuery to an outside project." Answer: a VPC Service Controls perimeter with `gcp.resourceRestrictions`, not IAM.

!!! tip "Exam tips"
    - Know the three firewall layers. L7 and TLS inspection live in global network firewall policies.
    - Deny beats allow only at equal priority. Otherwise, the lower priority number wins.
    - Service account targets beat network tags for security.
    - Know the private access matrix: Private Google Access, restricted VIP, PSC, and Cloud NAT.
    - Use VPC Service Controls for service-level exfiltration. Use IAM for identity-level access.
    - Test VPC Service Controls in dry run before you enforce it.
    - Interconnect is not encrypted by default. HA VPN uses IPsec.

Labs: [[networking-labs]] (Network Security, Cloud Armor, Routing and Addressing), [[security-labs]].

[Next: Data protection](03-data-protection.md)
