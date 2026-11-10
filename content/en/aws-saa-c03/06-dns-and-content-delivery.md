# 6. DNS and Content Delivery: Route 53, CloudFront, Global Accelerator

**Goal:** Route users to the right endpoint with DNS, edge caching, or a global entry point.

## Route 53

[[networking-route53|Route 53]] is a highly available, scalable, fully managed DNS service. It is authoritative, so you can update its records. Route 53 has a 100% [[sla|availability SLA]].

### Records

Each record has:

- A domain or subdomain name
- A record type
- A value
- A routing policy
- A TTL

| Type | Maps |
|---|---|
| A | Hostname to IPv4 address |
| AAAA | Hostname to IPv6 address |
| CNAME | Hostname to another hostname |
| NS | Name servers for a hosted zone |

Advanced record types (CAA, DS, MX, NAPTR, PTR, SOA, TXT, SPF, SRV) are not in the exam.

### Hosted zones

A hosted zone holds the records for a domain and its subdomains.

- Public hosted zone: routes internet traffic.
- Private hosted zone: routes traffic inside a [[networking-vpc|VPC]].
- Each hosted zone costs $0.50 per month.

### CNAME versus Alias

- CNAME maps a hostname to another hostname. It works only for non-root domains.
- Alias maps a hostname to an AWS resource. It works for root and non-root domains. It is free. It has native health checks. It is always type A or AAAA. You cannot set its TTL.
- Alias targets: load balancers, [[networking-cloudfront|CloudFront]] distributions, API Gateway, Elastic Beanstalk environments, S3 website endpoints, VPC interface endpoints, Global Accelerator, and another record in the same hosted zone.
- An Alias cannot point to an EC2 DNS name.

### Routing policies

| Policy | Use | Notes |
|---|---|---|
| Simple | One resource. Or several values, where the client picks one at random. | Cannot use health checks. An Alias points to one AWS resource only. |
| Weighted | Splits traffic by weight, such as load balancing between Regions or testing a new version | Weights do not need to total 100. Weight 0 stops traffic to that record. If all records have weight 0, traffic splits equally. Health checks allowed. |
| Failover | Primary and secondary ([[disaster-recovery|disaster recovery]]) resources | Requires a health check on the primary. Use the same record name, preferably. |
| Latency | The resource with the lowest latency to the client | Health checks allowed. |
| Geolocation | Routes by user location | Create a default record for locations with no match. |
| Multi-value answer | Up to 8 healthy records per response | Not a substitute for a load balancer. Health checks allowed. |
| Geoproximity | Routes by location of users and resources, with a bias | Uses Route 53 Traffic Flow. Non-AWS resources need latitude and longitude. |
| IP-based | Routes by client [[cidr|CIDR]] | Example: send users of one ISP to a specific endpoint. |

### Domain registrar and DNS

A registrar sells domain names. Many registrars also host DNS. To use Route 53 with a domain from another registrar:

1. Create a hosted zone in Route 53.
2. Update the NS records at the registrar to the Route 53 name servers.

## CloudFront

CloudFront is a CDN. It caches content at edge locations. It protects against DDoS attacks and integrates with [[security-shield|Shield]] and [[security-waf|WAF]].

Origins:

- [[storage-s3|S3]] bucket. Use Origin Access Control so that only CloudFront can read the bucket.
- Custom HTTP origin: ALB, EC2, an S3 static website, or any HTTP backend.

| Price class | Coverage |
|---|---|
| Price Class All | All regions. Best performance. |
| Price Class 200 | Most regions, without the most expensive ones |
| Price Class 100 | Only the cheapest regions |

## Global Accelerator

- Use it for an app in one Region that has users worldwide.
- It uses Anycast IP addresses. Clients connect to the nearest [[edge-location|edge location]]. A unicast IP is one server with one IP.
- Traffic goes from the edge location to the app over the AWS internal network.
- Works with Elastic IPs, EC2, ALB, and NLB, public or private.
- Provides static IP addresses, health checks, failover in under 1 minute, and DDoS protection.

| | CloudFront | Global Accelerator |
|---|---|---|
| How it helps | Caches content at the edge and serves it there | Routes connections through the edge to the app in its Region |

## Exam tips

- Use an Alias to point a root domain at an AWS resource. CNAME does not work at the root.
- Alias records are free.
- A failover policy needs a health check on the primary resource.
- A multi-value answer is not a load balancer.
- Route 53 routing works at the DNS level. It is not load balancer routing.
- A simple routing policy cannot use health checks.
- CloudFront caches content. Global Accelerator routes connections.

[Next: Databases](07-databases.md)
