---
title: Identity-aware-proxy
category: GCP
description: 'GCP note: Identity-aware-proxy.'
tags:
- gcp
- security
---


# Identity-aware-proxy

`gcp` `security`

## Identity-Aware Proxy (IAP)
**AWS Equivalent:** AWS Cognito + ALB Authentication (partial equivalence)

**Context-aware access control for applications** - Authenticate users without VPN, enforce access policies based on identity and context
### Overview
- **Zero Trust access model** - No VPN required
- **Identity-based access** - Google accounts, workforce identity
- **Context-aware** - Device, location, IP address
- **Application-level authentication** - Works at L7 (HTTP/HTTPS)
- **Integration** - GKE, Cloud Run, Compute Engine, App Engine
- **BeyondCorp implementation** for cloud applications

### How It Works
```text
1. User accesses application URL (iap.example.com)
2. IAP intercepts request
3. Check if user is authenticated
4. If not -> Redirect to Google Sign-In
5. User authenticates
6. IAP checks access policy (IAM + Access Levels)
7. If authorized -> Forward request to application with identity headers
8. If denied -> 403 Forbidden
9. Application receives request with user identity
```

### Core Concepts
#### Identity
- **Google Account**: Gmail or Workspace users
- **Service Account**: For service-to-service authentication
- **Google Groups**: Grant access to entire groups
- **Cloud Identity**: Non-Gmail organizational accounts

#### Access Policy
- **IAM roles**: Who can access (`roles/iap.httpsResourceAccessor`)
- **Access Levels**: Context-aware conditions (IP, device, location)
- **VPC Service Controls**: Additional perimeter security

#### IAP-Secured Resource
- Web application behind load balancer
- App Engine application
- Cloud Run service
- GKE service via Ingress
- Compute Engine instances

### Supported Resources
#### App Engine
- **Easiest integration, built-in support**
- Enable IAP with one click
- No additional configuration needed

#### Cloud Run
- Requires ingress via HTTPS Load Balancer
- Backend service configuration
- IAP enabled on backend service

#### GKE
- External HTTPS Load Balancer + Ingress
- BackendConfig CRD for IAP settings
- Per-service or cluster-wide

#### Compute Engine
- Instance groups behind HTTPS Load Balancer
- Backend service with IAP enabled
- Applications must respect IAP headers

#### On-Premises (via Connector)
- IAP Connector for on-prem applications
- **Bring BeyondCorp to hybrid environments**
- No VPN tunnel needed

### IAM Roles for IAP
**Access Roles:**
- `roles/iap.httpsResourceAccessor`: Access HTTPS resources
- `roles/iap.tunnelResourceAccessor`: TCP tunneling (SSH, RDP)
- `roles/iap.webServiceUser`: Legacy, use httpsResourceAccessor instead

**Admin Roles:**
- `roles/iap.admin`: Full IAP admin (configure settings, IAM)
- `roles/iap.settingsAdmin`: Configure IAP settings only

**Best Practice:**
- Grant `httpsResourceAccessor` to users/groups
- Grant at resource level (not project-wide)
- Use Google Groups for easier management

### Enabling IAP
#### App Engine
```bash
# Enable IAP on App Engine app
gcloud app services update default --enable-iap

# Grant access to user
gcloud iap web add-iam-policy-binding \
  --resource-type=app-engine \
  --member='user:alice@example.com' \
  --role='roles/iap.httpsResourceAccessor'
```

#### Compute Engine (HTTPS Load Balancer)
```bash
# 1. Create HTTPS load balancer with backend service
# 2. Enable IAP on backend service
gcloud compute backend-services update BACKEND_SERVICE \
  --iap=enabled \
  --global

# 3. Configure OAuth consent screen (in Cloud Console)

# 4. Grant access
gcloud iap web add-iam-policy-binding \
  --resource-type=backend-services \
  --service=BACKEND_SERVICE \
  --member='group:eng@example.com' \
  --role='roles/iap.httpsResourceAccessor'
```

#### Cloud Run
```bash
# 1. Create HTTPS Load Balancer with Cloud Run backend (NEG)
# 2. Enable IAP on backend service
gcloud compute backend-services update BACKEND_SERVICE \
  --iap=enabled \
  --global

# 3. Grant access
gcloud iap web add-iam-policy-binding \
  --resource-type=backend-services \
  --service=BACKEND_SERVICE \
  --member='user:bob@example.com' \
  --role='roles/iap.httpsResourceAccessor'
```

#### GKE
```yaml
# BackendConfig for IAP
apiVersion: cloud.google.com/v1
kind: BackendConfig
metadata:
  name: iap-backendconfig
spec:
  iap:
    enabled: true
    oauthclientCredentials:
      secretName: iap-oauth-secret

---
# Service using IAP
apiVersion: v1
kind: Service
metadata:
  name: my-service
  annotations:
    cloud.google.com/backend-config: '{"default": "iap-backendconfig"}'
spec:
  type: NodePort
  selector:
    app: my-app
  ports:
    - port: 8080
      targetPort: 8080

---
# Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /*
            pathType: ImplementationSpecific
            backend:
              service:
                name: my-service
                port:
                  number: 8080
```

### OAuth Consent Screen
**Required for IAP:**
- Application name
- Support email
- Scopes (openid, email, profile)
- Authorized domains
- Application logo (optional)

**User Consent:**
- Internal users (same org): No consent required
- External users: Consent screen shown on first access

### IAP Headers
**IAP adds headers to forwarded requests:**
- `X-Goog-IAP-JWT-Assertion`: Signed JWT token with user identity
- `X-Goog-Authenticated-User-Email`: User email
- `X-Goog-Authenticated-User-ID`: User ID

**Application should verify JWT:**
```python
# Python example - Verify IAP JWT
from google.auth.transport import requests
from google.oauth2 import id_token

def verify_iap_jwt(iap_jwt, expected_audience):
    try:
        decoded_jwt = id_token.verify_token(
            iap_jwt,
            requests.Request(),
            audience=expected_audience,
            certs_url='https://www.gstatic.com/iap/verify/public_key'
        )
        return decoded_jwt
    except Exception as e:
        print(f'JWT verification failed: {e}')
        return None

# In request handler
iap_jwt = request.headers.get('X-Goog-IAP-JWT-Assertion')
if iap_jwt:
    user_info = verify_iap_jwt(iap_jwt, expected_audience='/projects/PROJECT_NUMBER/apps/PROJECT_ID')
    user_email = user_info['email']
else:
    # Reject request (not from IAP)
    return 'Unauthorized', 401
```

### TCP Tunneling (SSH/RDP)
**Access VMs without external IPs:**
```bash
# Enable IAP for TCP forwarding
gcloud compute firewall-rules create allow-iap-proxy \
  --direction=INGRESS \
  --action=allow \
  --rules=tcp:22,tcp:3389 \
  --source-ranges=35.235.240.0/20

# SSH via IAP
gcloud compute ssh INSTANCE_NAME \
  --zone=ZONE \
  --tunnel-through-iap

# RDP via IAP (Windows)
gcloud compute start-iap-tunnel INSTANCE_NAME 3389 \
  --local-host-port=localhost:3389 \
  --zone=ZONE

# Then connect to localhost:3389 with RDP client

# Grant access
gcloud iap tcp add-iam-policy-binding \
  --member='user:alice@example.com' \
  --role='roles/iap.tunnelResourceAccessor' \
  --zone=ZONE \
  --instance=INSTANCE_NAME
```

### Access Levels (Context-Aware Access)
**Integrate with Access Context Manager:**
```bash
# Create access level
gcloud access-context-manager levels create corporate-network \
  --title="Corporate Network Only" \
  --basic-level-spec=level.yaml \
  --policy=POLICY_ID

# level.yaml
combiningFunction: AND
conditions:
  - ipSubnetworks:
      - "203.0.113.0/24"  # Corporate office
  - devicePolicy:
      requireScreenlock: true

# Apply to IAP
# (Configured in IAP settings, not via gcloud)
```

**Use Cases:**
- Require corporate network or VPN
- Require managed devices
- Time-based access
- Geographic restrictions

### Session Controls
**Session length:**
- Default: 14 days
- Configurable: 1 hour to 30 days
- Force re-authentication for sensitive apps

**Forced re-authentication:**
- For critical operations
- After password change
- After security incident

### Programmatic Access
**Service-to-service with service accounts:**
```python
# Python - Access IAP-protected service
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import requests

# Service account credentials
credentials = service_account.IDTokenCredentials.from_service_account_file(
    '/path/to/service-account-key.json',
    target_audience='IAP_CLIENT_ID'
)

# Get ID token
credentials.refresh(Request())
id_token = credentials.token

# Make request with ID token
headers = {'Authorization': f'Bearer {id_token}'}
response = requests.get('https://iap-app.example.com/api', headers=headers)
```

### Bypass IAP (Not Recommended)
**If application has public endpoint:**
- Users can bypass IAP
- **Always use IAP as sole ingress**
- Block direct access to backend

**For App Engine:**
- `dispatch.yaml` to force IAP
- Firewall rules to block direct access

**For Compute Engine:**
- Internal load balancer only
- No external IPs on instances
- Firewall rules: Only allow from load balancer

### Monitoring & Logging
**Audit Logs:**
- IAP access granted/denied
- User authentication events
- Policy changes

```bash
# View IAP access logs
gcloud logging read "resource.type=gae_app \
  AND protoPayload.metadata.@type=\"type.googleapis.com/google.cloud.audit.IapAuditLog\""

# View denied access
gcloud logging read "resource.type=gae_app \
  AND protoPayload.metadata.denied=true"
```

**Metrics:**
- Requests per user
- Authentication failures
- Latency added by IAP (~10-50ms)

### Limitations
- HTTPS/TCP only (no UDP)
- Requires HTTPS Load Balancer for Compute Engine/GKE
- OAuth consent screen required
- **Not a replacement for application-level authorization**
- Adds latency (typically 10-50ms)
- Limited to Google identities (no SAML federation directly)

### IAP vs VPN
| Aspect | IAP | VPN |
|--------|-----|-----|
| Network access | Application-level | Network-level |
| Setup complexity | Low | Medium-High |
| User experience | Browser-based | Client software |
| Granularity | Per-resource | Network-wide |
| Context-aware | Yes | Limited |
| Zero Trust | Yes | No |
| Latency | Low (~10-50ms) | Variable |
| Cost | Free (IAP itself) | VPN gateway costs |

### IAP vs AWS ALB Authentication
| Feature | IAP | ALB Auth + Cognito |
|---------|-----|---------------------|
| Identity providers | Google, Workspace, Cloud Identity | Cognito, SAML, OIDC, Social |
| Context-aware | Yes (Access Levels) | No |
| TCP tunneling | Yes | No |
| On-prem support | Yes (IAP Connector) | No |
| Setup complexity | Low | Medium |
| Pricing | Free | Cognito pricing |
| Zero Trust | Built-in | Requires additional services |

### Pricing
- **IAP itself is free**
- Costs from: HTTPS Load Balancer, backend services
- TCP tunneling: Free (only data egress charges)

---

## ACE Level

### Essential gcloud Commands
```bash
# Enable IAP API
gcloud services enable iap.googleapis.com

# Enable IAP on App Engine
gcloud app services update SERVICE_NAME --enable-iap

# Disable IAP on App Engine
gcloud app services update SERVICE_NAME --no-enable-iap

# Enable IAP on backend service (Compute Engine/GKE)
gcloud compute backend-services update BACKEND_SERVICE \
  --iap=enabled \
  --global

# Grant IAP access (HTTPS)
gcloud iap web add-iam-policy-binding \
  --resource-type=app-engine \
  --member='user:alice@example.com' \
  --role='roles/iap.httpsResourceAccessor'

# Grant IAP access (backend service)
gcloud iap web add-iam-policy-binding \
  --resource-type=backend-services \
  --service=BACKEND_SERVICE \
  --member='group:eng@example.com' \
  --role='roles/iap.httpsResourceAccessor'

# Grant TCP tunnel access
gcloud iap tcp add-iam-policy-binding \
  --member='user:bob@example.com' \
  --role='roles/iap.tunnelResourceAccessor' \
  --zone=ZONE \
  --instance=INSTANCE_NAME

# Remove IAP access
gcloud iap web remove-iam-policy-binding \
  --resource-type=app-engine \
  --member='user:alice@example.com' \
  --role='roles/iap.httpsResourceAccessor'

# View IAP settings
gcloud iap settings get

# SSH via IAP tunnel
gcloud compute ssh INSTANCE_NAME \
  --zone=ZONE \
  --tunnel-through-iap

# SCP via IAP tunnel
gcloud compute scp LOCAL_FILE INSTANCE_NAME:REMOTE_PATH \
  --zone=ZONE \
  --tunnel-through-iap

# Create IAP tunnel for custom port
gcloud compute start-iap-tunnel INSTANCE_NAME 8080 \
  --local-host-port=localhost:8080 \
  --zone=ZONE

# List IAP policy
gcloud iap web get-iam-policy \
  --resource-type=app-engine
```

### Key Concepts for ACE
- Understanding IAP as Zero Trust access control
- Enabling IAP on App Engine applications
- Enabling IAP on backend services (Compute Engine, GKE)
- Granting IAP access with IAM roles
- Using IAP for SSH/RDP access without external IPs
- Understanding OAuth consent screen setup
- Viewing IAP audit logs
- Understanding IAP headers in application code
- Basic troubleshooting (403 errors, access denied)
- Understanding when to use IAP vs VPN

---

## PCA Level

### Architectural Patterns
#### Zero Trust Enterprise Access
```text
Architecture:
1. All applications behind IAP (no VPN)
2. Access Levels: Corporate network OR VPN OR managed device
3. MFA required for all users
4. Context-aware policies (IP, device, location)
5. Continuous verification (session controls)

Benefits:
- No broad network access
- Per-application access control
- Context-aware decisions
- Simplified user experience
- BeyondCorp implementation
```

#### Hybrid Cloud Architecture
```text
Components:
- GCP: Applications with IAP
- On-Premises: Applications with IAP Connector
- Single identity (Cloud Identity/Workspace)
- Unified access policies
- No site-to-site VPN needed

Access Flow:
User -> IAP -> GCP Load Balancer -> GCP App
User -> IAP -> IAP Connector -> On-Prem App
Same authentication, same policies
```

#### Multi-Tier Application Security
```text
Tiers:
1. Public tier: Cloud Armor (DDoS, WAF)
2. Identity tier: IAP (authentication)
3. Application tier: App-level authorization
4. Data tier: Encryption (KMS, VPC SC)

Defense in Depth:
- Cloud Armor: Block malicious IPs
- IAP: Authenticate users
- Application: Authorize actions (RBAC)
- VPC SC: Prevent data exfiltration
```

### Advanced IAP Configuration
#### Custom Access Levels
```yaml
# access-level-advanced.yaml
title: "Production Access"
basic:
  combiningFunction: AND
  conditions:
    # Require corporate network
    - ipSubnetworks:
        - "203.0.113.0/24"

    # Require managed device
    - devicePolicy:
        requireScreenlock: true
        requireCorpOwned: true
        osConstraints:
          - osType: DESKTOP_CHROME_OS
          - osType: DESKTOP_MAC
            minimumVersion: "13.0.0"

    # Business hours only for contractors
    - members:
        - "group:contractors@example.com"
      regions:
        - "US"
      # Custom condition (business hours)
```

**Apply to IAP:**
1. Create access level in Access Context Manager
2. Configure in IAP settings (Cloud Console)
3. Access level enforced in addition to IAM

#### Per-Resource Policies
```bash
# Different policies for different apps
# Production app: Strict access
gcloud iap web add-iam-policy-binding \
  --resource-type=backend-services \
  --service=prod-backend \
  --member='group:prod-team@example.com' \
  --role='roles/iap.httpsResourceAccessor'

# Development app: More permissive
gcloud iap web add-iam-policy-binding \
  --resource-type=backend-services \
  --service=dev-backend \
  --member='group:all-engineers@example.com' \
  --role='roles/iap.httpsResourceAccessor'
```

### GKE Integration Patterns
#### Multi-Service IAP
```yaml
# Different IAP configs for different services
apiVersion: cloud.google.com/v1
kind: BackendConfig
metadata:
  name: admin-iap
spec:
  iap:
    enabled: true
    oauthclientCredentials:
      secretName: admin-iap-secret

---
apiVersion: cloud.google.com/v1
kind: BackendConfig
metadata:
  name: app-iap
spec:
  iap:
    enabled: true
    oauthclientCredentials:
      secretName: app-iap-secret

---
# Admin service (restricted access)
apiVersion: v1
kind: Service
metadata:
  name: admin-service
  annotations:
    cloud.google.com/backend-config: '{"default": "admin-iap"}'
spec:
  type: NodePort
  selector:
    app: admin
  ports:
    - port: 8080

---
# Application service (wider access)
apiVersion: v1
kind: Service
metadata:
  name: app-service
  annotations:
    cloud.google.com/backend-config: '{"default": "app-iap"}'
spec:
  type: NodePort
  selector:
    app: frontend
  ports:
    - port: 8080
```

### Application Integration
#### JWT Verification in Application
```python
# Python Flask app with IAP JWT verification
from flask import Flask, request, abort
from google.auth.transport import requests
from google.oauth2 import id_token

app = Flask(__name__)

IAP_AUDIENCE = '/projects/PROJECT_NUMBER/apps/PROJECT_ID'

def verify_iap_request():
    """Verify IAP JWT and return user info"""
    iap_jwt = request.headers.get('X-Goog-IAP-JWT-Assertion')

    if not iap_jwt:
        # Request not from IAP
        abort(401, 'Unauthorized - No IAP token')

    try:
        decoded_jwt = id_token.verify_token(
            iap_jwt,
            requests.Request(),
            audience=IAP_AUDIENCE,
            certs_url='https://www.gstatic.com/iap/verify/public_key'
        )

        return {
            'email': decoded_jwt['email'],
            'user_id': decoded_jwt['sub'],
            'is_admin': 'admin@example.com' in decoded_jwt['email']
        }

    except Exception as e:
        abort(401, f'Unauthorized - Invalid token: {e}')

@app.route('/api/data')
def get_data():
    user = verify_iap_request()

    # Application-level authorization
    if not user['is_admin']:
        abort(403, 'Forbidden - Admin only')

    return {'data': 'sensitive information', 'user': user['email']}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

#### Node.js Integration
```javascript
// Node.js Express app with IAP
const express = require('express');
const { OAuth2Client } = require('google-auth-library');

const app = express();
const client = new OAuth2Client();

const IAP_AUDIENCE = '/projects/PROJECT_NUMBER/apps/PROJECT_ID';

async function verifyIapRequest(req, res, next) {
  const iapJwt = req.header('X-Goog-IAP-JWT-Assertion');

  if (!iapJwt) {
    return res.status(401).send('Unauthorized - No IAP token');
  }

  try {
    const ticket = await client.verifyIdToken({
      idToken: iapJwt,
      audience: IAP_AUDIENCE
    });

    const payload = ticket.getPayload();
    req.user = {
      email: payload.email,
      userId: payload.sub
    };

    next();
  } catch (e) {
    return res.status(401).send('Unauthorized - Invalid token');
  }
}

app.get('/api/data', verifyIapRequest, (req, res) => {
  res.json({
    data: 'sensitive information',
    user: req.user.email
  });
});

app.listen(8080, () => console.log('Server running on port 8080'));
```

### TCP Tunneling for Databases
```bash
# Access Cloud SQL via IAP tunnel
gcloud compute start-iap-tunnel sql-proxy-vm 3306 \
  --local-host-port=localhost:3306 \
  --zone=us-central1-a

# Connect to MySQL
mysql -h 127.0.0.1 -P 3306 -u root -p

# Access private GKE cluster
gcloud compute start-iap-tunnel bastion-host 8001 \
  --local-host-port=localhost:8001 \
  --zone=us-central1-a

# Configure kubectl to use tunnel
kubectl --server=http://localhost:8001 get pods
```

### Monitoring & Alerting
```bash
# Create log-based metric for failed access
gcloud logging metrics create iap-access-denied \
  --description="IAP access denied attempts" \
  --log-filter='resource.type="gae_app"
    AND protoPayload.metadata.@type="type.googleapis.com/google.cloud.audit.IapAuditLog"
    AND protoPayload.metadata.denied=true'

# Alert on unusual access patterns
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="IAP Access Denied Spike" \
  --condition-threshold-value=10 \
  --condition-threshold-duration=300s \
  --condition-filter='metric.type="logging.googleapis.com/user/iap-access-denied"'

# Dashboard metrics
# - Total requests per user
# - Failed authentication attempts
# - Latency added by IAP
# - Access by time of day/location
```

### Compliance & Audit
**SOC 2 CC6.6 (Logical Access):**
```text
Evidence:
1. IAP configuration (all apps protected)
2. IAM policies (who has access)
3. Access logs (who accessed what, when)
4. Session controls (re-authentication requirements)
5. Context-aware access levels

Audit queries:
- List all IAP-protected resources
- Export access logs to BigQuery
- Report on access by user/group
- Failed access attempts
```

**HIPAA Access Controls:**
```text
Requirements:
- Unique user identification
- Automatic logoff (session timeout)
- Encryption in transit
- Audit controls

IAP Implementation:
- Unique: Google identity per user
- Logoff: Session timeout (configurable)
- Encryption: HTTPS required
- Audit: Cloud Logging (all access)
```

### Break-Glass Procedure
```bash
# Emergency access without IAP (DO NOT USE IN PRODUCTION)
# Option 1: Temporarily disable IAP
gcloud compute backend-services update BACKEND_SERVICE \
  --iap=disabled \
  --global

# Option 2: Grant emergency access
gcloud iap web add-iam-policy-binding \
  --resource-type=backend-services \
  --service=BACKEND_SERVICE \
  --member='user:oncall@example.com' \
  --role='roles/iap.httpsResourceAccessor'

# Re-enable IAP after emergency
gcloud compute backend-services update BACKEND_SERVICE \
  --iap=enabled \
  --global
```

**Better Approach:**
- Pre-defined break-glass accounts
- MFA required for break-glass
- Automatic alerts on break-glass use
- Automatic expiration (IAM conditions)

### Cost Optimization
- IAP itself is free
- Costs from HTTPS Load Balancer: $18-25/month per LB
- Optimize: Share load balancer across multiple services
- TCP tunneling: Free (only egress charges)

### Multi-Organization Strategy
**For holding companies:**
```text
Challenge: Users need access to apps in multiple orgs

Solution:
1. Cloud Identity federation (single identity)
2. IAP in each org
3. Cross-org groups for access
4. Unified audit logging (export to central BigQuery)

Example:
user@company.com can access:
- IAP app in org A (via group in org A)
- IAP app in org B (via group in org B)
Same identity, separate policies
```

### Migration from VPN
**Planning:**
1. Inventory all VPN users and applications
2. Categorize applications (web, SSH, database)
3. Plan IAP rollout (web apps first)
4. Create access groups and policies
5. Pilot with non-critical apps
6. Train users (no VPN client needed)
7. Rollout to production
8. Decommission VPN

**Parallel Run:**
- Both VPN and IAP active
- Gradual user migration
- Monitor access patterns
- Identify and fix issues
- Full cutover after validation

### Well-Architected Considerations
- **Operational Excellence**: Infrastructure as code for IAP config, automated policy enforcement, clear runbooks for break-glass
- **Reliability**: Session timeout configuration, graceful degradation if IAP unavailable (rare), health checks for backend services
- **Security**: Zero Trust model, context-aware access, JWT verification in apps, MFA enforcement, audit logging, least privilege IAM
- **Performance**: Minimal latency (10-50ms), HTTP/2 support, global load balancing for low latency
- **Cost**: Free IAP service, optimize load balancer usage, share LBs across services where possible
