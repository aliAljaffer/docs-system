---
title: Cloud-load-balancing
category: GCP
description: 'GCP note: Cloud-load-balancing.'
tags:
- gcp
- networking
---


# Cloud-load-balancing

`gcp` `networking`

## Cloud Load Balancing
**AWS Equivalent:** ELB, ALB, NLB
**Fully managed** load balancing service, **globally distributed**, **auto-scaling**

### Key Differences from AWS
| Feature | GCP Load Balancing | AWS ELB/ALB/NLB |
|---------|-------------------|-----------------|
| Scope | **Single global anycast IP** | Regional (need multiple IPs) |
| Management | Single service, multiple types | Separate services (ALB, NLB, CLB) |
| Backend groups | Cross-region backends | Regional only |
| SSL offloading | Built-in for HTTPS | ACM or IAM certs |
| Health checks | Configured per backend | Per target group |

### Load Balancer Types Overview
```
External Load Balancers (internet-facing)
├── Global
│   ├── HTTP(S) Load Balancer (Layer 7)
│   ├── SSL Proxy (Layer 4, SSL traffic)
│   └── TCP Proxy (Layer 4, TCP traffic)
└── Regional
    ├── Network Load Balancer (Layer 4, passthrough)
    └── External Application Load Balancer (Layer 7, regional)

Internal Load Balancers (private)
├── Internal HTTP(S) Load Balancer (Layer 7)
└── Internal TCP/UDP Load Balancer (Layer 4)
```

---

## HTTP(S) Load Balancing
**AWS Equivalent:** Application Load Balancer + CloudFront
**Layer 7** load balancer for HTTP/HTTPS traffic

### Global HTTP(S) Load Balancer
- **Single global anycast IP** serves traffic worldwide
- Automatic routing to nearest healthy backend
- Cross-region failover and load balancing
- Integrated with Cloud CDN
- SSL/TLS termination at the edge

#### Components
- **Forwarding rules**: Map IP + port to target proxy
- **Target proxy**: Routes requests to URL map
- **URL map**: Routes based on host and path
- **Backend services**: Manages backend instance groups
- **Backend groups**: Actual compute resources ([[gcp/compute-engine|Compute Engine]], [[gcp/gke|GKE]], [[gcp/cloud-run|Cloud Run]], [[gcp/cloud-functions|Cloud Functions]])
- **Health checks**: Monitor backend health

#### URL Maps and Content-Based Routing
- Host-based routing: `example.com` vs `api.example.com`
- Path-based routing: `/api/*` vs `/static/*`
- Header-based routing: Custom headers
- Query parameter routing: `?version=v2`
- **More sophisticated than AWS ALB**: Supports redirects, rewrites, header manipulation

#### Backend Service Configuration
- **Balancing mode**: UTILIZATION, RATE, or CONNECTION
- **Session affinity**:
  - Client IP
  - Generated cookie
  - Client IP + protocol
  - HTTP cookie
- **Connection draining**: Timeout for in-flight requests (0-3600s)
- **Timeout**: Backend response timeout (1-86400s)

#### SSL/TLS Configuration
- **SSL certificates**: Google-managed or self-managed
- **Google-managed certs**: **Automatic provisioning and renewal**
- **SSL policies**: Control TLS versions and cipher suites
- **HTTPS redirect**: Automatic HTTP to HTTPS redirect

### Regional External Application Load Balancer
- Similar to Global HTTP(S) but regional scope
- Lower latency for regional traffic
- Software-defined, not hardware-based
- Use case: Regional applications, compliance requirements

---

## Network Load Balancing
**AWS Equivalent:** Network Load Balancer
**Layer 4** load balancer for TCP/UDP traffic

### External Network Load Balancer
- **Passthrough**: Does not terminate connections
- **Preserves client source IP**
- Regional resource
- Ultra-low latency
- **Not proxied** (unlike AWS NLB which is proxied)
- Supports **connection tracking**

#### Load Balancing Algorithms
- **5-tuple hash**: Source IP, source port, dest IP, dest port, protocol
- **3-tuple hash**: Source IP, dest IP, protocol
- **2-tuple hash**: Source IP, dest IP

#### Session Affinity
- CLIENT_IP (5-tuple)
- CLIENT_IP_PROTO (3-tuple)
- CLIENT_IP_PORT_PROTO (2-tuple)

#### Use Cases
- TCP/UDP traffic not using HTTP(S)
- Preserve client IP address
- Ultra-low latency requirements
- Non-HTTP protocols (SMTP, LDAP, DNS)

### Internal TCP/UDP Load Balancer
**AWS Equivalent:** Internal NLB
- **Private load balancing** within [[vpc|VPC]]
- Layer 4 load balancer
- Distributes traffic to backends in same region
- **No external IP required**
- Use cases: Database connections, microservices, internal APIs

#### Key Features
- **Lightweight**: Software-defined
- **High availability**: Active/active across zones
- **Preserves source IP**: With Direct Server Return
- **Health checking**: TCP, HTTP(S), HTTP/2, gRPC
- **No pre-warming required**: Scales automatically

---

## SSL Proxy Load Balancing
**AWS Equivalent:** NLB with TLS listener
**Layer 4** load balancer for **SSL/TLS traffic** (non-HTTP)

### Features
- **Global**: Single anycast IP
- **SSL termination**: Offloads SSL from backends
- **Intelligent routing**: To nearest healthy backend
- Supports TCP with SSL/TLS
- Use cases: SMTP over TLS, IMAP over SSL

### Configuration
- SSL certificates at load balancer
- Can use Google-managed certificates
- Backend communication: SSL or TCP
- SSL policies for security control

---

## TCP Proxy Load Balancing
**AWS Equivalent:** NLB
**Layer 4** load balancer for **TCP traffic** (non-SSL)

### Features
- **Global**: Single anycast IP
- Intelligent routing to backends
- IPv6 termination
- Does not preserve client IP (proxied)

### Use Cases
- TCP traffic that's not HTTP(S)
- Global TCP applications
- IPv6 client support with IPv4 backends

---

## Internal HTTP(S) Load Balancing
**AWS Equivalent:** Internal ALB
**Layer 7** load balancer for **private** HTTP(S) traffic

### Features
- Regional resource
- **Proxy-based**, software-defined
- Only private IP addresses
- URL-based routing like external HTTP(S) LB
- Integrated with [[vpc|VPC]] networks
- No external internet exposure

### Use Cases
- Microservices architecture
- Internal APIs
- Multi-tier applications
- Private HTTP(S) services

---

## Load Balancer Comparison Table
| Type | Layer | Scope | Preserves IP | Use Case |
|------|-------|-------|--------------|----------|
| HTTP(S) LB | 7 | Global | No | Web apps, APIs |
| Regional App LB | 7 | Regional | No | Regional web apps |
| Network LB | 4 | Regional | **Yes** | TCP/UDP, low latency |
| SSL Proxy | 4 | Global | No | SSL/TLS traffic |
| TCP Proxy | 4 | Global | No | TCP traffic |
| Internal HTTP(S) | 7 | Regional | No | Private web apps |
| Internal TCP/UDP | 4 | Regional | Yes (DSR) | Private TCP/UDP |

---

## Backend Types
### Instance Groups
**Managed Instance Groups (MIG)**
- Autoscaling based on CPU, load, custom metrics
- Auto-healing with health checks
- **Most common backend type**
- See [[gcp/compute-engine|Compute Engine MIGs]]

**Unmanaged Instance Groups**
- Heterogeneous instances
- Manual management

### Network Endpoint Groups (NEG)
#### Zonal NEG
- Specific IP:port endpoints
- More flexible than instance groups
- Use case: Containerized apps, custom backends

#### Internet NEG
- **External** endpoints (outside GCP)
- Use case: Multi-cloud, hybrid architectures

#### Serverless NEG
- [[gcp/cloud-run|Cloud Run]], [[gcp/cloud-functions|Cloud Functions]], [[gcp/app-engine|App Engine]]
- **Fully managed** backends

#### Hybrid Connectivity NEG
- On-premises endpoints via [[cloud-vpn|VPN]]/[[cloud-interconnect|Interconnect]]

---

## Health Checks
**AWS Equivalent:** Target Group Health Checks
- Monitor backend availability
- Types: HTTP, HTTPS, HTTP/2, TCP, SSL, gRPC
- **Check interval**: 1-300 seconds (default 5s)
- **Timeout**: 1-300 seconds (default 5s)
- **Healthy threshold**: Consecutive successes (default 2)
- **Unhealthy threshold**: Consecutive failures (default 2)

### Health Check Firewall
- Allow health check IP ranges:
  - `35.191.0.0/16`
  - `130.211.0.0/22`
- Create firewall rule to allow these ranges

---

## Advanced Features

### Cloud Armor Integration
**AWS Equivalent:** AWS WAF + Shield
- DDoS protection
- Web Application Firewall (WAF)
- Rate limiting
- See [[cloud-armor|Cloud Armor]] for details

### Cloud CDN Integration
**AWS Equivalent:** CloudFront
- Cache static content at edge locations
- Reduce latency and backend load
- See Cloud CDN for details

### Identity-Aware Proxy (IAP)
- Application-level access control
- **No [[cloud-vpn|VPN]] required**
- Context-aware access based on user identity
- Integrated with load balancer

### Traffic Management
#### Weighted Traffic Splitting
- Gradual rollouts (canary deployments)
- A/B testing
- Blue/green deployments
- Percentage-based traffic distribution

#### Traffic Steering
- Route traffic based on request properties
- Header-based routing
- Cookie-based routing

### SSL Policies
- Control TLS versions (1.0, 1.1, 1.2, 1.3)
- Cipher suite selection
- ==Modern__, Compatible, Restricted, Custom profiles
- Apply to HTTPS, SSL Proxy, TCP Proxy load balancers

### Custom Headers
- Add/remove/modify HTTP headers
- Use cases: Backend routing, security, debugging
- `X-Forwarded-For`, `X-Forwarded-Proto` automatically added

### Connection Draining
**AWS Equivalent:** Connection Draining / Deregistration Delay
- Gracefully remove backends
- Complete in-flight requests
- Timeout: 0-3600 seconds

### Outlier Detection
- Automatically remove unhealthy backends
- Based on success rate, latency
- Faster than health checks
- Temporarily eject failing backends

---

## Capacity Planning
- **Pre-warming**: Contact Google for large traffic spikes
  - Generally not needed (auto-scales)
  - Recommended for: >1 million requests/second
- **Rate limits**: Configurable per backend
- **Connection limits**: Automatic scaling

---

## Pricing
- **Forwarding rules**: Per hour
- **Data processing**: Per GB processed
- **Global LB**: Slightly higher than regional
- **No charge**: For bandwidth between LB and backends in same region
- **Egress**: Standard egress pricing applies

---

## ACE Level

### Essential gcloud Commands
```bash
# Create HTTP(S) Load Balancer (multi-step process)

# 1. Create instance group (or use existing MIG)
gcloud compute instance-groups unmanaged create IG_NAME --zone=ZONE

# 2. Create health check
gcloud compute health-checks create http HEALTH_CHECK_NAME \
  --port=80 \
  --request-path=/

# 3. Create backend service
gcloud compute backend-services create BACKEND_SERVICE_NAME \
  --protocol=HTTP \
  --health-checks=HEALTH_CHECK_NAME \
  --global

# 4. Add backend to backend service
gcloud compute backend-services add-backend BACKEND_SERVICE_NAME \
  --instance-group=IG_NAME \
  --instance-group-zone=ZONE \
  --global

# 5. Create URL map
gcloud compute url-maps create URL_MAP_NAME \
  --default-service=BACKEND_SERVICE_NAME

# 6. Create target HTTP proxy
gcloud compute target-http-proxies create TARGET_PROXY_NAME \
  --url-map=URL_MAP_NAME

# 7. Create forwarding rule (global IP)
gcloud compute forwarding-rules create FORWARDING_RULE_NAME \
  --global \
  --target-http-proxy=TARGET_PROXY_NAME \
  --ports=80

# List load balancers
gcloud compute forwarding-rules list
gcloud compute backend-services list

# Create Network Load Balancer
gcloud compute forwarding-rules create NLB_NAME \
  --region=REGION \
  --ports=80 \
  --backend-service=BACKEND_SERVICE_NAME

# Create Internal Load Balancer
gcloud compute forwarding-rules create ILB_NAME \
  --region=REGION \
  --load-balancing-scheme=INTERNAL \
  --network=VPC_NAME \
  --subnet=SUBNET_NAME \
  --ports=80 \
  --backend-service=BACKEND_SERVICE_NAME

# View forwarding rule details
gcloud compute forwarding-rules describe RULE_NAME --global

# Update backend service
gcloud compute backend-services update BACKEND_SERVICE_NAME \
  --timeout=60s \
  --global
```

### Key Concepts for ACE
- Understanding different load balancer types and when to use each
- Creating HTTP(S) load balancers with backend services
- Configuring health checks for backends
- Setting up URL maps for content-based routing
- Managing SSL certificates (Google-managed vs self-managed)
- Difference between global and regional load balancers
- Creating internal load balancers for private traffic
- Viewing load balancer metrics in [[gcp/cloud-monitoring|Cloud Monitoring]]

---

## PCA Level

### Architectural Patterns
#### Global Multi-Region Architecture
- Global HTTP(S) Load Balancer with backends in multiple regions
- Automatic failover to healthy region
- Lowest latency routing
- Cloud CDN for static content caching
- [[cloud-armor|Cloud Armor]] for security

#### Microservices Architecture
- Internal HTTP(S) Load Balancer for service-to-service communication
- Multiple backend services for different microservices
- URL-based routing to different services
- [[gcp/gke|GKE]] with container-native load balancing

#### Hybrid Cloud Architecture
- TCP/UDP Load Balancer with Hybrid Connectivity NEG
- On-premises backends via [[cloud-vpn|Cloud VPN]] or [[cloud-interconnect|Cloud Interconnect]]
- Gradual migration with traffic splitting
- Internet NEG for multi-cloud backends

#### Multi-Tier Application
- External HTTP(S) Load Balancer for web tier
- Internal HTTP(S) Load Balancer for app tier
- Internal TCP/UDP Load Balancer for database tier
- Layered security with [[vpc|VPC]] firewall rules

### High Availability Design
- **Regional redundancy**: Backends in multiple zones
- **Cross-region failover**: Global LB with multi-region backends
- **Health checks**: Aggressive monitoring (5s interval)
- **Outlier detection**: Fast failure detection
- **Connection draining**: Graceful backend removal
- **Managed instance groups**: Auto-healing backends

### Security Best Practices
- **[[cloud-armor|Cloud Armor]]**: DDoS protection, WAF rules, rate limiting
- **SSL/TLS**: Use modern SSL policies (TLS 1.2+)
- **Google-managed certificates**: Automatic renewal
- **IAP**: Application-level access control
- **Private load balancers**: For internal services
- **Firewall rules**: Restrict to LB health check ranges
- **[[gcp/vpc-service-controls|VPC Service Controls]]**: Perimeter security

### Performance Optimization
- **Cloud CDN**: Cache static content
- **HTTP/2**: Enable for performance
- **Session affinity**: For stateful applications
- **Connection pooling**: Backend reuse
- **Outlier detection**: Remove slow backends
- **Balancing mode**: UTILIZATION for auto-scaling backends
- **Cross-region backends**: Reduce latency globally

### Cost Optimization
- **Regional LB**: Use when traffic is regional
- **Serverless NEG**: No idle backend costs for [[gcp/cloud-run|Cloud Run]], [[gcp/cloud-functions|Cloud Functions]]
- **Autoscaling backends**: Scale down during low traffic
- **Cloud CDN**: Reduce backend load and egress costs
- **Internal LB**: No egress charges for [[vpc|VPC]] traffic
- **[[gcp/compute-engine|Committed Use Discounts]]**: For predictable backend resources

### Traffic Management Strategies
#### Canary Deployments
- Weighted traffic splitting (95% old, 5% new)
- Monitor error rates, latency
- Gradual rollout (5% → 25% → 50% → 100%)
- Automatic rollback on errors

#### Blue/Green Deployments
- Two backend services (blue, green)
- Instant traffic switch via URL map update
- Zero-downtime deployments
- Easy rollback

#### A/B Testing
- Route based on cookies or headers
- Test different versions for different users
- Analyze metrics per backend

### Migration Strategies
#### From AWS ALB/NLB
- **ALB to HTTP(S) LB**: Similar features, simpler global setup
- **NLB to Network LB**: Note IP preservation differences
- **ELB Classic**: Migrate to HTTP(S) or Network LB
- **Cross-region**: Single global IP vs multiple regional IPs

#### Hybrid Migration
- Use Hybrid Connectivity NEG
- Gradually shift traffic from on-prem to GCP
- Traffic splitting for controlled migration
- Monitor latency and errors during migration

### Observability
- **[[gcp/cloud-monitoring|Cloud Monitoring]]**:
  - Request count, latency, error rate
  - Backend utilization, health
  - Per-backend metrics
- **[[gcp/cloud-logging|Cloud Logging]]**:
  - HTTP request logs
  - SSL certificate expiration
  - Backend health changes
- **[[gcp/cloud-trace|Cloud Trace]]**: Request latency breakdown

### Container-Native Load Balancing
- [[gcp/gke|GKE]] pods as direct backends (not node proxying)
- **Lower latency** (no extra hop)
- Better load distribution
- Requires [[gcp/gke|VPC-native cluster]]
- Uses NEG automatically

### Advanced URL Map Configurations
- **Host rules**: Route by hostname
- **Path matchers**: Route by URL path
- **Route rules**: Header, query param routing
- **URL redirects**: HTTP to HTTPS, domain redirects
- **URL rewrites**: Modify request path before backend
- **Header manipulation**: Add/remove headers
- **Fault injection**: Testing resilience

### SSL Certificate Management
- **Google-managed**: **Automatic issuance and renewal**
  - Requires domain ownership verification
  - DNS or HTTP challenge
  - Supports wildcard domains
- **Self-managed**: Upload your own certs
  - Full control over cert lifecycle
  - Use for complex CA requirements
- **Certificate Map**: Multiple certs per load balancer

### Capacity Planning
- **Backends**: Plan for 50% headroom for zone failures
- **Health checks**: Balance frequency vs backend load
- **Connection limits**: Monitor backend connection capacity
- **Rate limits**: Protect backends from overload
- **Pre-warming**: Only for >1M QPS launches

### Well-Architected Considerations
- **Operational Excellence**: Managed service, automatic scaling, Google-managed certs
- **Reliability**: Multi-region backends, health checks, auto-healing, connection draining
- **Security**: [[cloud-armor|Cloud Armor]], SSL/TLS, IAP, modern SSL policies, private LBs
- **Performance**: Global anycast, Cloud CDN, outlier detection, HTTP/2, low latency
- **Cost**: Autoscaling backends, regional LBs, serverless NEGs, CDN caching
- **Sustainability**: Efficient routing, auto-scaling reduces idle capacity
