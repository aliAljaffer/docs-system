---
title: Deployment-strategies
category: GCP
description: 'GCP note: Deployment-strategies.'
tags:
- gcp
- devops
---


# Deployment-strategies

`gcp` `devops`

## Deployment Strategies
**Comprehensive guide** to **6 deployment strategies** for GCP services
**Critical for PCA exam** - case studies often test deployment approach selection

### Overview
Deployment strategy = **how you release new application versions** to production
Trade-offs: Downtime vs complexity vs cost vs risk

---

## 1. Recreate Deployment

### How It Works
1. Terminate all V1 instances
2. Deploy V2 instances
3. Start serving traffic

### Characteristics
- **Downtime**: **Yes** (brief period with zero instances)
- **Rollback speed**: Slow (need to redeploy V1)
- **Resource cost**: **Low** (no extra infrastructure)
- **Complexity**: Very simple
- **Traffic control**: All or nothing

### Use Cases
✓ Dev/test environments
✓ Non-critical applications
✓ Overnight maintenance windows
✗ Production systems (downtime unacceptable)

### GCP Services
- [[gcp/compute-engine|Managed Instance Groups]]: Delete group, create new
- Not recommended for production

---

## 2. Rolling Update (Rolling Deployment)

### How It Works
1. Gradually replace V1 instances with V2
2. One instance (or small batch) at a time
3. Wait for health check pass
4. Continue until all instances replaced

### Characteristics
- **Downtime**: **Zero**
- **Rollback speed**: Slow (must roll forward to previous version)
- **Resource cost**: **No extra infrastructure**
- **Complexity**: Low-medium
- **Traffic control**: Both versions serve traffic during rollout
- **Deployment time**: Slowest (one-by-one)

### Use Cases
✓ Cost-sensitive production deployments
✓ Stateless applications
✓ When backward compatibility guaranteed
✗ Breaking API changes
✗ Database schema changes without compatibility

### GCP Services
- **[[gcp/compute-engine|Managed Instance Groups]]**: Rolling update with `instance-group-manager update`
- **[[gcp/gke|GKE]]**: RollingUpdate strategy (default)
  ```yaml
  spec:
    strategy:
      type: RollingUpdate
      rollingUpdate:
        maxSurge: 1
        maxUnavailable: 0
  ```
- **[[app-engine|App Engine]]**: Gradual traffic migration

### Example
```bash
# MIG rolling update
gcloud compute instance-groups managed rolling-action start-update my-mig \
  --version=template=new-template \
  --max-surge=1 \
  --max-unavailable=0
```

---

## 3. Rolling Update with Additional Batch

### How It Works
1. Create **new instances** with V2 (in addition to V1)
2. Wait for new instances to be healthy
3. Gradually shift traffic from V1 to V2
4. Terminate V1 instances once V2 fully deployed

### Characteristics
- **Downtime**: **Zero**
- **Rollback speed**: Fast (V1 instances still running during transition)
- **Resource cost**: **Medium** (extra instances during deployment)
- **Complexity**: Medium
- **Traffic control**: Gradual shift from V1 to V2
- **Deployment time**: Faster than rolling (parallel deployment)

### Use Cases
✓ Production applications where rollback speed matters
✓ When you can afford temporary extra infrastructure
✓ Testing new version with real traffic before full commitment

### GCP Services
- **[[gcp/compute-engine|MIG]]**: Use `max-surge` parameter
  ```bash
  gcloud compute instance-groups managed rolling-action start-update my-mig \
    --version=template=new-template \
    --max-surge=3 \  # Extra instances during rollout
    --max-unavailable=0
  ```

---

## 4. Canary Deployment

### How It Works
1. Deploy V2 to **small subset** (10-20%) of instances
2. Route small % of traffic to V2
3. **Monitor metrics**: Error rate, latency, user feedback
4. If successful: Gradually increase V2 traffic
5. If problems: Quick rollback to 100% V1

### Characteristics
- **Downtime**: **Zero**
- **Rollback speed**: **Very fast** (just shift traffic back)
- **Resource cost**: Medium (extra canary instances)
- **Complexity**: Medium-high
- **Risk**: **Minimal user impact** (small subset exposed)
- **Deployment time**: Gradual (hours to days)

### Use Cases
✓ **Critical production systems** (minimizes blast radius)
✓ Testing new features with real users
✓ When you need confidence before full rollout
✓ A/B testing new features

### GCP Services
#### App Engine
```bash
# Deploy V2 without promoting
gcloud app deploy --no-promote --version=v2

# Gradually shift traffic
gcloud app services set-traffic default --splits=v1=90,v2=10
# Monitor...
gcloud app services set-traffic default --splits=v1=50,v2=50
# Monitor...
gcloud app services set-traffic default --splits=v2=100
```

#### Cloud Run
```bash
# Deploy new revision
gcloud run deploy my-service --image=IMAGE --tag=v2 --no-traffic

# Split traffic
gcloud run services update-traffic my-service --to-revisions=v1=90,v2=10
```

#### GKE with Istio
```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: my-service
spec:
  http:
  - match:
    route:
    - destination:
        host: my-service
        subset: v1
      weight: 90
    - destination:
        host: my-service
        subset: v2
      weight: 10
```

#### MIG
```bash
# Create canary instance group
gcloud compute instance-groups managed create my-mig-canary --template=v2-template

# Use Cloud Load Balancing to split traffic
gcloud compute backend-services add-backend my-backend \
  --instance-group=my-mig-canary \
  --balancing-mode=RATE \
  --max-rate-per-instance=10  # 10% of traffic
```

---

## 5. Blue/Green Deployment

### How It Works
1. Deploy V2 to **completely separate environment** (Green)
2. V1 (Blue) continues serving 100% traffic
3. Test Green environment thoroughly
4. **Instant traffic switch** from Blue to Green
5. Keep Blue running for quick rollback
6. After validation period: Decommission Blue

### Characteristics
- **Downtime**: **Zero**
- **Rollback speed**: **Instant** (switch back to Blue)
- **Resource cost**: **High** (double infrastructure during transition)
- **Complexity**: Medium
- **Traffic control**: Instant 100% switch
- **Testing**: Full pre-production testing in Green

### Use Cases
✓ Mission-critical applications
✓ When instant rollback required
✓ Database migrations (with backward compatibility)
✓ Major version upgrades
✗ Cost-sensitive applications (expensive)

### GCP Services
#### Cloud Load Balancing + MIGs
```bash
# Blue environment (currently serving)
my-mig-blue (100% traffic)

# Green environment (new version)
my-mig-green (0% traffic initially)

# Test Green...

# Switch traffic instantly
gcloud compute backend-services update my-backend \
  --remove-backend=my-mig-blue \
  --add-backend=my-mig-green

# Rollback if needed (instant)
gcloud compute backend-services update my-backend \
  --remove-backend=my-mig-green \
  --add-backend=my-mig-blue
```

#### Cloud DNS (for multi-region blue/green)
```bash
# Update DNS to point to Green region
gcloud dns record-sets transaction start --zone=my-zone
gcloud dns record-sets transaction remove --zone=my-zone \
  --name=myapp.example.com --type=A --ttl=300 "BLUE_IP"
gcloud dns record-sets transaction add --zone=my-zone \
  --name=myapp.example.com --type=A --ttl=300 "GREEN_IP"
gcloud dns record-sets transaction execute --zone=my-zone
```

#### App Engine / Cloud Run
- Similar to canary but switch traffic instantly (0% → 100%)

---

## 6. Shadow Deployment (Dark Launch)

### How It Works
1. Deploy V2 in production
2. **Mirror production traffic** to V2
3. V1 serves actual responses to users
4. V2 processes requests but responses discarded
5. Compare V2 behavior to V1
6. Fix issues without user impact
7. Once confident: Promote V2 to serve traffic

### Variant: **Record and Replay**
- Record production traffic
- Replay against V2 in isolated environment
- Analyze differences

### Characteristics
- **Downtime**: **Zero**
- **User impact**: **Zero** (users never see V2 responses)
- **Resource cost**: **High** (double compute)
- **Complexity**: **Very high**
- **Safety**: Maximum (no user impact from V2 issues)

### Use Cases
✓ Testing major refactoring
✓ Performance testing with real traffic patterns
✓ Validating new algorithms
✓ Testing third-party integrations (requires stubbing)

### Challenges
- **Side effects**: Must prevent V2 from:
  - Writing to databases
  - Calling external APIs (payments, emails)
  - Creating real resources
- Requires sophisticated traffic mirroring
- Complex to implement correctly

### GCP Services
#### GKE with Istio
```yaml
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: my-service
spec:
  http:
  - mirror:
      host: my-service-v2  # Shadow traffic to V2
      subset: v2
    route:
    - destination:
        host: my-service  # V1 serves actual traffic
        subset: v1
```

#### Load Balancing + Traffic Mirroring (Advanced)
- Use custom middleware to duplicate requests
- Send duplicates to V2
- Discard V2 responses

---

## Deployment Strategy Comparison

| Strategy | Downtime | Resource Cost | Rollback Speed | Complexity | Risk | Best For |
|----------|----------|---------------|----------------|------------|------|----------|
| **Recreate** | Yes | Low | Slow | Very Low | High | Dev/test |
| **Rolling** | No | Low | Slow | Low | Medium | Cost-sensitive |
| **Rolling + Batch** | No | Medium | Fast | Medium | Medium | Production |
| **Canary** | No | Medium | Very Fast | Medium-High | **Low** | **Critical apps** |
| **Blue/Green** | No | **High** | **Instant** | Medium | Low | Mission-critical |
| **Shadow** | No | High | N/A | **Very High** | **Minimal** | Testing |

---

## A/B Testing vs Canary

### Canary Deployment
- **Goal**: Test new version for stability, performance, errors
- **Metrics**: Error rate, latency, resource usage
- **Duration**: Short (hours to days)
- **Decision**: Rollout or rollback based on technical metrics

### A/B Testing
- **Goal**: Test new feature for user engagement, conversion
- **Metrics**: User behavior, business KPIs, click-through rate
- **Duration**: Longer (days to weeks)
- **Decision**: Keep feature or remove based on business metrics
- **Implementation**: Same as canary (traffic splitting)

---

## Decision Tree

```
Do you need zero downtime?
├─ No → Recreate (simplest)
└─ Yes
   ├─ Can you afford double infrastructure?
   │  ├─ Yes
   │  │  ├─ Need instant rollback? → Blue/Green
   │  │  └─ Testing only? → Shadow
   │  └─ No
   │     ├─ Need gradual rollout with monitoring? → Canary
   │     └─ Simple production deployment? → Rolling
   └─ Need to test with small user subset? → Canary or A/B
```

---

## Well-Architected Alignment

- **Operational Excellence**: Canary (gradual, monitored rollouts)
- **Reliability**: Blue/Green (instant rollback), Canary (minimal blast radius)
- **Security**: Shadow (test without user exposure)
- **Performance**: Rolling + Batch (faster than rolling)
- **Cost**: Rolling (no extra infrastructure)
- **Sustainability**: Rolling (minimal waste)

---

## PCA Exam Tips

**Exam will test:**
1. Selecting appropriate strategy for scenario
2. Understanding trade-offs
3. GCP service capabilities for each strategy
4. Rollback procedures
5. Cost implications

**Common scenarios:**
- "Minimize user impact during deployment" → **Canary**
- "Instant rollback required" → **Blue/Green**
- "Minimal cost, stateless app" → **Rolling**
- "Test major refactoring without risk" → **Shadow**
- "Breaking database changes" → **Blue/Green** (with dual-write period)
