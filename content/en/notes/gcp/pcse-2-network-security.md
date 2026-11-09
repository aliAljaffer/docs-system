---
title: 2 - Network Security
category: GCP
description: 'Part of PCSE Home. Official exam guide sections 2.1 to 2.3: securing
  communications and establishing boundary protection.'
tags:
- gcp
- security
- pcse
---

<!-- imported from ObsidianVault/studies/PCSE/2 - Network Security.md. Edit the source, then run sync.py. -->

# 2 - Network Security

`gcp` `security` `pcse`

## 2 - Network Security (~22%)

Part of [[pcse-home|PCSE Home]]. Official exam guide sections 2.1 to 2.3: securing communications and establishing boundary protection.

### 2.1 Designing and configuring perimeter security

**Cloud NGFW (replaces classic "firewall rules only" thinking):**

Three configuration layers, in order of where they attach:

1. **Hierarchical firewall policies:** attach at org or folder level; inherited by child projects' VPCs; support rules with priorities; cannot be bypassed by projects.
2. **Global network firewall policies:** attach at VPC level; the modern replacement for classic per-VPC firewall rules; support threat inspection.
3. **Classic VPC firewall rules:** per network, still exist; implied deny egress / allow ingress defaults.

- **Tiers:** Cloud NGFW Essentials (rules, logging), Enterprise (adds Layer 7 filtering and TLS inspection with Security Profiles: Palo Alto Networks and CrowdStrike threat lists), Plus (adds advanced EDR-based features). Firewall endpoints are required for Enterprise/Plus inspection and are billed.
- **Secure tags:** identity-based firewall rules for VMs (tag the VM, write rules against the tag), pairs with NGFW policies.
- **L7 inspection:** only in global network firewall policies with security profile groups; requires TLS inspection (with trust config) for encrypted traffic.

**Load balancers as perimeter controls:** external LBs accept internet traffic, internal LBs accept RFC 1918 only (scope and exposure are independent); secure the entry with SSL policies (minimum TLS version and ciphers) and Google-managed certificates; Cloud Armor attaches to external global LB backends.

**Identity-Aware Proxy:** PCSE wants config: enable IAP on a backend service or for TCP forwarding; control with IAM roles (`roles/iap.httpsResourceAccessor`); combine with ACM access levels for context-aware access. IAP TCP forwarding gives secure RDP/SSH without public IPs or bastions.

**Cloud Armor: the WAF and edge security product.**
- Security policies attach to external HTTPS/TCP proxy load balancer backends (and Cloud CDN).
- Rule types: IP/CIDR allow-deny, expression-based (CEL), **preconfigured WAF rules** (ModSecurity CRS: SQLi, XSS, LFI, RFI, RCE, scanner detection), geo-based.
- **Rate limiting** (throttle/ban with enforce action), **Adaptive Protection** (ML-based L7 DDoS detection with suggested rules), **bot management** (reCAPTCHA integration), **edge security policies** (for CDN/cache), named IP lists (third-party threat intel).
- Enterprise tier adds DDoS response support and managed protection plans.

**Certificate Authority Service (CAS):** managed private CA. CA pools (DevOps vs Enterprise tiers), root/subordinate CAs, issue and revoke certs via API, cert templates. Use case: replace self-signed or manual PKI for mTLS or internal services.

**Secure Web Proxy:** managed egress web proxy (Network Security API) to control and inspect outbound HTTPS from VMs without a proxy VM; rules with URL lists, optional TLS inspection. Use case: "egress must only reach approved SaaS domains."

**Cloud DNS security:** DNSSEC on public zones (signing states: on, transfer, off), DNS forwarding/peering zones for hybrid, response policies for split-horizon, private zones with VPC association, and the critical pattern for private Google access: a **private DNS zone for `googleapis.com` (and `gcr.io`, `pkg.dev`) pointing at the restricted or private VIPs**.

**Monitoring and restricting APIs:**
- Inventory enabled services with Cloud Asset Inventory.
- Restrict: disable unused APIs, `gcp.resourceRestrictions` org policy (with VPC-SC perimeter) and `gcp.restrictNonCmekServices`, domain-restricted sharing `iam.allowedPolicyMemberDomains`, and use PGA/restricted VIP so only intended Google APIs are reachable.

**Private vs public IP addressing:** know which products require external IPs (external HTTP(S) LB, Cloud NAT gateway itself), and that VMs without public IPs can still reach Google APIs via PGA and the internet via Cloud NAT.

**Additional facts:**
- Firewall rules attach to a VPC only, never a single subnet or VM; targets are all instances, network tags, or SAs; tags and SAs are mutually exclusive in one rule.
- SA targets are safer than tags: attaching a SA needs an IAM permission, network tags have none.
- Ingress rules cannot use destination ranges; egress rules cannot use source ranges; an omitted source or destination means 0.0.0.0/0.
- `--source-ranges` plus `--source-tags` is a union: tagged VMs match even outside the ranges.
- Priority 0-65535, lower wins, default 1000; **deny overrides allow only at equal priority, otherwise the lower number wins regardless of action**; you cannot change an existing rule's direction or action, create the new rule then delete the old.
- Firewall Rules Logging is per rule (never on the two implied rules) and exports to Cloud Logging, Pub/Sub, or BigQuery.
- Network firewall policies group rules under IAM control: hierarchical (org/folder), global (VPC), regional (VPC).
- Cloud Armor also supports serverless NEGs (App Engine, Cloud Run, Functions), Internet NEGs (hybrid/multicloud), and GCS bucket backends; advanced network DDoS protection covers regional external TCP/UDP LBs, protocol forwarding, and public-IP VMs.
- Preconfigured WAF sensitivity 0-4: level N enables signatures up to N; lower level = higher confidence, fewer false positives.
- Cloud Armor rule priority 0 to 2147483647, the default rule sits at 2147483647; actions include `deny-404` and `deny-502`.
- Adaptive Protection full alerts require Managed Protection Plus, now named Cloud Armor Enterprise.
- CAS tiers: devops (high-volume, short-lived certs) vs enterprise (long-lived); the key pair is generated locally and never sent to Google.
- Cloud DNS: IAM at project and zone level; forwarding zone targets must be public IPs unless RFC 1918 over VPN/Interconnect; DNS peering is unidirectional and needs `dns.networks.targetWithPeeringZone` on the producer.

### 2.2 Configuring boundary segmentation

- **VPC security properties:** global vs regional resources, subnets regional, firewall implied rules, effective firewall evaluation: priority 0-65535, lower number wins (default 1000); deny overrides allow only at equal priority.
- **VPC peering vs Shared VPC (config-level now):** peering = network-to-network, no IAM separation, transitivity absent; Shared VPC = project-level attachment to host project, service project admins, IAM control at host, org policy `compute.restrictSharedVpcSubnetworks` to limit which subnets service projects can use.
- **Peering restrictions (2025 exam reports):** no overlapping [[cidr|CIDR]] ranges between peers; firewall rules cannot use tags or SAs from the peer network (use IP ranges); internal Compute Engine DNS does not resolve across peering (use IPs); no transitive peering.
- **N-tier isolation:** tiered subnets + NGFW policies per tier + secure tags; private GKE clusters for the data tier; PSC for southbound private access to services.
- **VPC Service Controls (config detail is heavily tested):**
	- Create an access policy (ACM) at org level, then perimeters around projects; services inside the perimeter refuse requests from outside unless the caller is within an access level or an ingress rule matches.
	- **Dry run mode:** log would-be violations before enforcement. Always deploy with dry run first.
	- **Ingress rules:** identity + access level + service + resource. **Egress rules:** what data can leave (to external projects/identities). **Bridges:** allow specified service interactions between two perimeters.
	- Known limitations: no support for some services, per-project services list required, and third-party client libraries need DNS + routing to restricted VIPs.
- Exam pattern: "data exfiltration from BigQuery to an outside project must be blocked" -> VPC-SC perimeter + `gcp.resourceRestrictions`, not IAM.

**Additional facts:**
- Custom VPCs ship without the default SSH/RDP allow rules that the default network has.
- Shared VPC needs an organization; setup roles `compute.xpnAdmin` + `resourcemanager.projectIamAdmin` (org/folder) and `compute.networkUser` per subnet; Compute API on both host and service projects; the service project pays for its compute.
- VMs in different service projects of one Shared VPC reach each other by internal routing; restrict that traffic with firewall rules.
- **Perimeters take projects only (`projects/<number>`); a project is in exactly one perimeter**; enforced denials return HTTP 403 naming the perimeter.
- Access levels gate ingress only; basic attributes: `ipSubnetworks` (RFC 1918 not allowed), `regions`, `members`, `devicePolicy`; combine function AND (default) or OR; custom level = one CEL expression over `origin`, `request.auth`, `levels`, `device`.
- VPC accessible services: `--enable-vpc-accessible-services` + `--vpc-allowed-services`; default all, `RESTRICTED-SERVICES` = all restricted services; enforcement happens only on the restricted-services list.
- Prerequisites: Access Context Manager API enabled; `roles/accesscontextmanager.policyAdmin`.

### 2.3 Establishing private connectivity

| Need | Answer |
|---|---|
| VMs with no public IP reach Google APIs | Private Google Access (enable on subnet) |
| On-prem hosts reach Google APIs over VPN/Interconnect | PGA for on-prem hosts + custom route for VIPs + DNS zone for `googleapis.com` |
| Only allow Google APIs, block general Google cloud-internal traffic | restricted.googleapis.com VIP (199.36.153.4/30) with DNS forwarding |
| Reach specific managed services privately from a VPC | Private Service Connect (PSC) endpoints (producer/consumer), or published services |
| Outbound internet for private VMs | Cloud NAT |
| On-prem to VPC | HA VPN (one gateway, two interfaces, 2+ tunnels, 99.99% SLA) or Cloud Interconnect (Dedicated/Partner) |
| VPC to VPC (same org or different) | peering or Shared VPC |

See PGA vs PSC for the full comparison.

**Details worth knowing:**
- PGA is a subnet-level setting; applies to instances with private IPs; requires no external IP on the VM.
- Restricted VIP: only Google APIs that support VPC-SC are reachable; pair with a private DNS zone for `googleapis.com` and routes over VPN/Interconnect (for on-prem) or a static route (for in-VPC).
- PSC endpoints get an internal IP in your subnet; PSC published services let other orgs consume privately; PSC supports Google APIs and third-party services.
- Cloud NAT: regional, with manual or auto-allocated IPs, port ranges; NAT does not allow inbound connections.
- HA VPN: one gateway with two interfaces (two reserved public IPs), at least two tunnels originating in the same region, BGP for the 99.99% SLA; Cloud VPN tunnels are IPsec, max 3 Gbps each; Interconnect for >3 Gbps or lower latency needs; both support PGA-for-on-prem via routing the VIP ranges over BGP.

**Additional facts:**
- An HA VPN gateway reserves two external IPs (one per interface); redundancy types: one, two, or four IPs.
- **Interconnect is not encrypted by default (add IPsec or MACsec)**; Dedicated = 10 or 100 Gbps at a colo facility and requires LACP, eBGP-4, and 802.1Q; each VLAN attachment pairs with a Cloud Router BGP session.
- Partner Interconnect: provider-supplied; pairing key; Cloud Router in the provider's region.
- API bundles: `all-apis` = private.googleapis.com; `vpc-sc` = restricted.googleapis.com.
- PGA is a per-subnet toggle (needs `compute.subnetworks.setPrivateIpGoogleAccess`); **PGA traffic still uses public VIPs, PSC uses internal IPs**.
- PSC endpoint = reserved internal IP + forwarding rule; needs the Service Directory and Cloud DNS APIs, roles `servicedirectory.editor` and `dns.admin`.
- Cloud NAT: SNAT only; subnet scope flags (`--nat-all-subnet-ip-ranges`, primary, or custom); each NAT IP gives 64,512 TCP + 64,512 UDP ports; static vs dynamic port allocation; idle timeout flags.

**Labs:** Networking Labs (Network Security, Cloud Armor, Routing and Addressing), Security Labs.
