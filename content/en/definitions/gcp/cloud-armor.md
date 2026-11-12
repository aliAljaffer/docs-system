---
title: cloud-armor
category: GCP
description: 'GCP note: Cloud-armor.'
tags:
- gcp
- networking
---


# cloud-armor

## Cloud Armor
**DDoS protection** and **Web Application Firewall (WAF)** for applications behind [[cloud-load-balancing|Cloud Load Balancing]]

**AWS Equivalent:** AWS WAF + AWS Shield

### Key Differences from AWS WAF & Shield
| Feature         | GCP Cloud Armor                    | AWS WAF + Shield                  |
| --------------- | ---------------------------------- | --------------------------------- |
| DDoS protection | **Built-in (Standard + Advanced)** | Shield Standard + Shield Advanced |
| WAF rules       | Included with Cloud Armor          | Separate WAF pricing              |
| Scope           | Global (via Load Balancer)         | Regional or global (CloudFront)   |
| Pricing         | Per policy + rules + requests      | Per WebACL + rules + requests     |
| Managed rules   | Google-managed + third-party       | AWS Managed Rules + Marketplace   |
| Rate limiting   | **Built-in**                       | Separate rule type                |
| Bot management  | Included (reCAPTCHA Enterprise)    | Separate Bot Control              |

---

## Cloud Armor Overview
- **Layer 7** security (HTTP/HTTPS)
- Protects applications behind:
  - [[cloud-load-balancing#global http(s) load balancer|Global HTTP(S) Load Balancer]]
  - [[cloud-load-balancing#regional external application load balancer|Regional External Application Load Balancer]]
- Defends against:
  - **DDoS attacks** (Layer 3, 4, 7)
  - **OWASP Top 10** vulnerabilities
  - **Application-layer attacks**
  - **Bot traffic**
- **No separate charge for DDoS protection** (included)

---

## Cloud Armor Tiers

### Cloud Armor Standard
**Included with all projects:**
- **Network DDoS protection** (Layer 3/4)
- Always-on detection and mitigation
- Protection against volumetric attacks
- **No configuration required**
- **No additional cost**

### Cloud Armor (Paid)
**Application-level protection:**
- **WAF rules** (allow/deny based on conditions)
- **Rate limiting** (requests per client IP)
- **Preconfigured rules** (SQLi, XSS, LFI, RCE, etc.)
- Custom rules (IP, geolocation, headers, etc.)
- **Adaptive protection** (ML-based anomaly detection)
- Logging and monitoring
- **Cost**: Per security policy + rules + requests

---

## Security Policies
**Security policy** = Collection of rules applied to backend service
- Attached to **backend services** of HTTP(S) Load Balancers
- **Priority-based** rules (0-2147483647, lower = higher priority)
- **Default rule**: Priority 2147483647 (allow or deny)

### Rule Components
- **Priority**: Determines evaluation order
- **Match condition**: When to apply rule
  - IP address/range
  - Geographic region
  - Request headers
  - Request path/query
  - Expression language (CEL)
- **Action**: What to do

| Action | Effect |
|---|---|
| Allow | Permit traffic |
| Deny | Block with HTTP 403/404/429/502 |
| Rate-based ban | Block after threshold |
| Redirect | Send to different URL |
| Throttle | Rate limit |

---

## Preconfigured WAF Rules
**AWS Equivalent:** AWS Managed Rules
**Google-managed rule sets** for common vulnerabilities

### Available Rule Sets
| Rule set | Protects against |
|---|---|
| SQLi | SQL injection |
| XSS | Cross-site scripting |
| LFI | Local file inclusion |
| RFI | Remote file inclusion |
| RCE | Remote code execution |
| Scanner detection | Security scanners (blocked) |
| Protocol attack | Malformed requests |
| Session fixation | Session hijacking |
| Java attack | Attacks on Java applications |
| PHP attack | PHP-specific vulnerabilities |
| Node.js attack | Node.js vulnerabilities |

### Sensitivity Levels
Each rule can be configured with sensitivity:
| Level | Effect |
|---|---|
| 0 | Off (disabled) |
| 1 | High threshold (low false positives, may miss attacks) |
| 2 | Medium threshold, **recommended** |
| 3 | Low threshold (more false positives, better detection) |
| 4 | Very low threshold (highest sensitivity) |

---

## Custom Rules

### IP-Based Rules
```yaml
# Allow specific IP
action: allow
match:
  srcIpRanges: ["203.0.113.0/24"]

# Deny specific IP
action: deny(403)
match:
  srcIpRanges: ["198.51.100.0/24"]
```

### Geographic Rules
```yaml
# Block traffic from specific countries
action: deny(403)
match:
  expr:
    expression: "origin.region_code ** 'CN' || origin.region_code ** 'RU'"
```

### Header-Based Rules
```yaml
# Block if specific header present
action: deny(403)
match:
  expr:
    expression: "has(request.headers['x-bad-bot'])"
```

### Advanced Expression Language (CEL)
**Common Expression Language** for complex rules:
```yaml
# Block non-HTTPS
expression: "request.scheme != 'https'"

# Allow only specific user agents
expression: "!request.headers['user-agent'][0].contains('MyApp')"

# Block requests with SQL keywords in query
expression: "request.query.contains('SELECT') || request.query.contains('DROP')"
```

---

## Rate Limiting
**AWS Equivalent:** Rate-based rules (separate in AWS WAF)
**Limit requests per client IP**

### Configuration
- **Threshold**: Requests per minute/second
- **Action**: Deny, throttle, or ban
- **Ban duration**: How long to block after threshold exceeded
- **Key**: Client IP (default) or custom key (headers, etc.)

### Example
```yaml
action: rate_based_ban
rateLimitOptions:
  conformAction: allow
  exceedAction: deny(429)
  enforceOnKey: IP
  rateLimitThreshold:
    count: 100
    intervalSec: 60
  banDurationSec: 600
```
**Result:** Block IP for 10 minutes after >100 requests in 60 seconds

### Use Cases
- **API rate limiting**: Protect backend APIs
- **Brute force protection**: Login pages
- **DDoS mitigation**: Block rapid requests
- **Cost control**: Limit expensive operations

---

## Adaptive Protection
**AWS Equivalent:** Shield Advanced (similar concept)
**ML-based DDoS protection**

### Features
- Learns normal traffic patterns
- Detects anomalies automatically
- Suggests security policy rules
- Alerts on attacks
- **Requires Cloud Armor subscription**

### How It Works
1. Analyzes baseline traffic (learning period)
2. Detects deviations (potential attacks)
3. **Suggests rules** (doesn't auto-block)
4. You approve and deploy rules

### Use Cases
- Unknown attack patterns
- Zero-day vulnerabilities
- Sophisticated DDoS attacks
- Supplement to preconfigured rules

---

## Bot Management
**AWS Equivalent:** AWS WAF Bot Control (separate)
Integrated with **reCAPTCHA Enterprise**

### reCAPTCHA Integration
- Challenge suspicious traffic
- Score-based (0.0-1.0): 1.0 = human, 0.0 = bot
- Action based on score threshold
- Invisible reCAPTCHA or checkbox

### Bot Detection Actions
| Action | Applies to |
|---|---|
| Allow | Trusted bots (Googlebot, etc.) |
| Challenge | Suspicious traffic (reCAPTCHA) |
| Deny | Known malicious bots |
| Redirect | CAPTCHA page |

---

## Edge Security Policy (Preview)
**AWS Equivalent:** CloudFront Functions + WAF
Apply security policies **at edge locations**

- Faster than backend service policies
- Lower latency for blocked requests
- Use cases: Geoblocking, simple IP blocks
- **Not all Cloud Armor features available**

---

## Logging and Monitoring

### Request Logging
- Enabled per security policy
- Logs to [[gcp/cloud-logging|Cloud Logging]]
- Contains:
  - Matched rule
  - Action taken
  - Client IP, location
  - Request details
  - Rate limit info

### Sampling
- Log all requests (expensive)
- Sample rate (e.g., 0.1 = 10% of requests)
- **All blocked requests always logged**

### Metrics
[[gcp/cloud-monitoring|Cloud Monitoring]] metrics:
- **Request count**: Total requests
- **Allowed/denied requests**: Per action
- **Rate limit exceeded**: Throttle events
- **Preconfigured rule hits**: WAF detections
- **Adaptive protection alerts**: ML detections

---

## Advanced Features

### Named IP Lists
**Reusable IP lists** for multiple rules:
```bash
# Create IP list
gcloud compute security-policies list-preconfigured-expression-sets list

# Reference in rule
match:
  expr:
    expression: "inIpRange(origin.ip, '192.0.2.0/24')"
```

### Preview Mode
- Test rules without blocking traffic
- **Log-only mode** to validate rules
- Prevents false positives
- Recommended before enforcing new rules

### Custom Error Pages
- Replace default 403/404 error pages
- Brand-consistent error messages
- Informative to users
- Can include support info

### JSON-Based Configuration
- Define policies as JSON
- Infrastructure as Code (IaC)
- Version control
- Automation with Terraform, Cloud Deployment Manager

---

## Pricing
- **Security policy**: $5 per month per policy
- **Security rules**: $1 per month per rule (beyond 5 rules)
- **Requests**: $0.75 per million requests (Standard tier locations)
- **Advanced features**: Additional cost
  - Adaptive Protection: Additional fee
  - Managed Protection Plus: Premium tier
- **reCAPTCHA Enterprise**: Separate pricing per assessment

---

## ACE Level

### Essential gcloud Commands
```bash
# Create security policy
gcloud compute security-policies create POLICY_NAME \
  --description="My security policy"

# Add rule to allow specific IP
gcloud compute security-policies rules create 1000 \
  --security-policy=POLICY_NAME \
  --action=allow \
  --src-ip-ranges="203.0.113.0/24"

# Add rule to deny specific region
gcloud compute security-policies rules create 2000 \
  --security-policy=POLICY_NAME \
  --action=deny-403 \
  --expression="origin.region_code == 'CN'"

# Add preconfigured WAF rule (SQLi protection)
gcloud compute security-policies rules create 3000 \
  --security-policy=POLICY_NAME \
  --action=deny-403 \
  --expression="evaluatePreconfiguredExpr('sqli-stable')"

# Add rate limiting rule
gcloud compute security-policies rules create 4000 \
  --security-policy=POLICY_NAME \
  --action=rate-based-ban \
  --rate-limit-threshold-count=100 \
  --rate-limit-threshold-interval-sec=60 \
  --ban-duration-sec=600 \
  --conform-action=allow \
  --exceed-action=deny-429 \
  --enforce-on-key=IP

# Update default rule
gcloud compute security-policies rules update 2147483647 \
  --security-policy=POLICY_NAME \
  --action=deny-403

# List security policies
gcloud compute security-policies list

# Describe security policy
gcloud compute security-policies describe POLICY_NAME

# Attach policy to backend service
gcloud compute backend-services update BACKEND_SERVICE_NAME \
  --security-policy=POLICY_NAME \
  --global

# Detach policy from backend service
gcloud compute backend-services update BACKEND_SERVICE_NAME \
  --security-policy="" \
  --global

# Enable logging
gcloud compute security-policies update POLICY_NAME \
  --log-level=VERBOSE

# Delete security policy
gcloud compute security-policies delete POLICY_NAME
```

### Key Concepts for ACE
- Creating security policies with rules
- Understanding rule priorities and evaluation order
- Using preconfigured WAF rules for common vulnerabilities
- Implementing rate limiting to prevent abuse
- Using IP-based and geographic rules
- Attaching security policies to backend services
- Monitoring security policy metrics and logs
- Testing rules in preview mode before enforcement

---

## PCA Level

### Architectural Patterns
#### Multi-Tier Security
- **Edge**: Geographic blocking, IP allowlist
- **WAF**: Preconfigured rules (SQLi, XSS)
- **Rate limiting**: Per-endpoint limits
- **Adaptive protection**: ML-based anomaly detection
- **Application**: Input validation, authentication

#### Defense in Depth
```text
Internet
  ↓
Cloud Armor (DDoS + WAF)
  ↓
Global Load Balancer
  ↓
VPC Firewall Rules
  ↓
GKE Network Policies
  ↓
Application (Authentication, Authorization)
```

#### API Protection
- Rate limiting per API endpoint
- API key validation (header-based rules)
- Geographic restrictions
- Bot management (block automated scraping)
- Custom error messages for API clients

#### Multi-Backend Policies
- Different policies per backend service
- Example:

| Backend | Policy |
|---|---|
| Public API | Strict rate limiting, WAF |
| Admin panel | IP allowlist, MFA |
| Static content | Minimal rules (CDN caching) |

### High Availability Design
- Cloud Armor operates at **Google's edge**
- No single point of failure
- **Global distribution**
- Integrated with load balancer (also HA)
- Automatic failover (no manual intervention)

### Security Best Practices
- **Enable all preconfigured rules**: Start with sensitivity 2
- **Preview mode first**: Test rules before enforcement
- **Rate limiting**: Implement for all public endpoints
- **Geographic blocking**: Block high-risk regions if applicable
- **Adaptive protection**: Enable for critical applications
- **Logging**: Full logging for security analysis
- **Regular review**: Update rules based on attack patterns
- **Least privilege**: Only allow necessary traffic
- **Custom error pages**: Don't leak system information

### Performance Optimization
- **Rule order**: Most common rules first (lower priority number)
- **Simple rules**: Faster evaluation than complex CEL expressions
- **Caching**: Use Cloud CDN to reduce backend load
- **Edge policies**: Block at edge for lower latency
- **Sampling logs**: Reduce log volume (log all blocks, sample allows)

### Cost Optimization
- **Consolidate policies**: Reuse policies across backend services
- **Optimize rule count**: Combine rules where possible (<5 rules free)
- **Log sampling**: Sample allowed traffic, log all denied
- **Geographic blocking**: Block unnecessary regions to reduce request volume
- **CDN integration**: Cache static content to reduce backend requests

### Migration Strategies
#### From AWS WAF + Shield
| Area | AWS WAF or Shield | Cloud Armor |
|---|---|---|
| WAF rules | AWS managed rules | Preconfigured rules |
| IP sets | AWS IP sets | IP range rules |
| Rate limiting | AWS rate rules | Rate limiting |
| Geographic | AWS geo-match | region_code |
| Custom rules | AWS conditions | CEL expressions |
| Logging | AWS Kinesis | Cloud Logging |

#### Testing Approach
1. **Inventory**: List all AWS WAF rules and Shield protections
2. **Create parallel**: Set up Cloud Armor policies in GCP
3. **Preview mode**: Test without blocking
4. **Validate**: Compare logs and metrics
5. **Gradual cutover**: Migrate traffic via DNS or load balancer
6. **Monitor**: Watch for false positives/negatives
7. **Optimize**: Tune rules based on production traffic

### Advanced Rule Configurations
#### Multi-Condition Rules
```yaml
# Block traffic from specific region to specific path
expression: |
  origin.region_code == 'CN' &&
  request.path.matches('/admin/.*')
```

#### Header Validation
```yaml
# Require specific header
expression: |
  !has(request.headers['x-api-key']) ||
  request.headers['x-api-key'][0] != 'secret-key'
action: deny-403
```

#### Path-Based Rate Limiting
```yaml
# Different rate limits per endpoint
# Rule 1: /api/login - 5 req/min
expression: request.path == '/api/login'
rateLimitThreshold:
  count: 5
  intervalSec: 60

# Rule 2: /api/search - 100 req/min
expression: request.path == '/api/search'
rateLimitThreshold:
  count: 100
  intervalSec: 60
```

#### Bot Detection with reCAPTCHA
```yaml
# Challenge low-score traffic
expression: token.recaptcha_action.score < 0.5
action: deny-403  # Or redirect to CAPTCHA
```

### Compliance Considerations
- **PCI DSS**: WAF requirement satisfied by Cloud Armor
- **OWASP Top 10**: Preconfigured rules cover many vulnerabilities
- **Logging**: Retain logs for audit and compliance
- **Data residency**: Requests processed at edge (consider for regulations)
- **Encryption**: All traffic HTTPS (enforced by load balancer)

### Observability
#### Cloud Monitoring Dashboards
- Request rate (allowed vs denied)
- Top blocked IPs
- Top triggered rules
- Geographic distribution of requests
- Rate limit violations

#### Cloud Logging Queries
```bash
# View blocked requests
gcloud logging read "resource.type=http_load_balancer AND \
  jsonPayload.enforcedSecurityPolicy.outcome=DENY" \
  --limit=100

# View rate limit violations
gcloud logging read "resource.type=http_load_balancer AND \
  jsonPayload.enforcedSecurityPolicy.configuredAction=RATE_BASED_BAN" \
  --limit=50

# Analyze attack patterns
gcloud logging read "jsonPayload.enforcedSecurityPolicy.preconfiguredExprIds:*" \
  --format="table(jsonPayload.enforcedSecurityPolicy.preconfiguredExprIds, \
  httpRequest.remoteIp)"
```

#### Alerting
- **High deny rate**: Potential attack or misconfiguration
- **Rate limit exceeded**: Specific IPs triggering limits
- **Adaptive protection alert**: ML-detected anomaly
- **New attack pattern**: Preconfigured rule hits spike

### Troubleshooting
| Issue | Symptom | Diagnosis | Fix |
|---|---|---|---|
| False positives | Legitimate traffic blocked | Review logs for matched rule | Lower preconfigured rule sensitivity. Add allow rule with higher priority. Adjust rate limit thresholds. Use preview mode to test |
| False negatives | Attacks not blocked | Review attack traffic patterns | Increase preconfigured rule sensitivity. Add custom rules for specific attacks. Enable adaptive protection. Tune rate limits |
| Performance issues | High latency from complex CEL expressions | - | Simplify rules, use preconfigured rules |

### Integration with GCP Services
- **[[cloud-load-balancing|Cloud Load Balancing]]**: Required (backend service attachment)
- **Cloud CDN**: Cache to reduce backend load
- **[[gcp/cloud-monitoring|Cloud Monitoring]]**: Metrics and dashboards
- **[[gcp/cloud-logging|Cloud Logging]]**: Security logs
- **reCAPTCHA Enterprise**: Bot detection
- **[[gcp/binary-authorization|Binary Authorization]]**: Container image verification
- **[[gcp/vpc-service-controls|VPC Service Controls]]**: Perimeter security

### Advanced DDoS Protection
#### Volumetric Attacks (Layer 3/4)
- Handled by Cloud Armor Standard (automatic)
- Google's network absorbs traffic
- No configuration needed

#### Application-Layer Attacks (Layer 7)
- HTTP floods, slowloris
- Mitigate with rate limiting
- Adaptive protection for unknown patterns
- Custom rules for specific attack signatures

#### Combined Defense
- **Layer 3/4**: Automatic (Cloud Armor Standard)
- **Layer 7**: WAF rules + rate limiting
- **Adaptive**: ML-based detection
- **CDN**: Absorb static content requests

### Well-Architected Considerations
- **Operational Excellence**: Managed service, automated DDoS protection, adaptive learning
- **Reliability**: Global edge, no SPOF, automatic failover, 99.99%+ availability
- **Security**: WAF, DDoS protection, rate limiting, bot management, compliance-ready
- **Performance**: Edge processing, minimal latency, rule optimization
- **Cost**: Included DDoS protection, pay-per-use WAF, optimize rule count
- **Sustainability**: Efficient edge processing, reduced backend load with CDN integration
