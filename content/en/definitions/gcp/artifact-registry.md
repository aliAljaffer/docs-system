---
title: artifact-registry
category: GCP
description: 'GCP note: Artifact-registry.'
tags:
- gcp
- devops
---


# artifact-registry

`gcp` `devops`

## Artifact Registry
**Managed artifact repository** for containers and packages

**AWS Equivalent:** Amazon ECR + CodeArtifact

### Overview
- Store Docker images, language packages (Maven, npm, Python)
- **Successor to Container Registry**
- Regional and multi-regional repositories
- Integrated vulnerability scanning
- Fine-grained IAM

### Supported Formats
| Format | Stores |
|---|---|
| Docker | Container images |
| Maven | Java packages |
| npm | Node.js packages |
| Python | PyPI packages |
| Apt | Debian packages |
| Yum | RPM packages |
| Go | Go modules |
| KFP | Kubeflow Pipelines components |

### Repository Types
| Type | Description |
|---|---|
| Standard | Regional storage |
| Multi-regional | Replicated across regions |
| Remote | Proxy for external registries (Docker Hub, Maven Central) |
| Virtual | Aggregates multiple repositories |

### Image Management
- Tag mutable/immutable
- Delete images and tags
- Vulnerability scanning
- SBOM (Software Bill of Materials) generation

### Vulnerability Scanning
- **Automatic scanning** on push
- CVE detection
- Severity levels: Critical, High, Medium, Low
- Integration with [[binary-authorization|Binary Authorization]]

### IAM Roles
| Role | Grants |
|---|---|
| `roles/artifactregistry.reader` | Pull images |
| `roles/artifactregistry.writer` | Push images |
| `roles/artifactregistry.admin` | Full access |

### Pricing
- **Storage**: $0.10 per GB/month
- **Network egress**: Standard GCP rates
- **Scanning**: Free

---

## ACE Level

### Essential Commands
```bash
# Create repository
gcloud artifacts repositories create my-repo \
  --repository-format=docker \
  --location=us-central1

# Configure Docker
gcloud auth configure-docker us-central1-docker.pkg.dev

# Tag image
docker tag myapp:latest us-central1-docker.pkg.dev/PROJECT/my-repo/myapp:latest

# Push image
docker push us-central1-docker.pkg.dev/PROJECT/my-repo/myapp:latest

# Pull image
docker pull us-central1-docker.pkg.dev/PROJECT/my-repo/myapp:latest

# List images
gcloud artifacts docker images list us-central1-docker.pkg.dev/PROJECT/my-repo
```

### Key Concepts for ACE
- Creating Docker repositories
- Pushing and pulling images
- Configuring Docker authentication
- Understanding regional vs multi-regional
- Viewing vulnerability scan results

---

## PCA Level

### Multi-Region Strategy
- Use for high availability
- Closer to global users
- Higher cost than regional

### Security
- **Vulnerability scanning**: Block vulnerable images
- **Binary Authorization**: Deploy only signed images
- **IAM**: Fine-grained access control
- **CMEK**: Customer-managed encryption

### Cost Optimization
- Delete unused images
- Use lifecycle policies
- Regional for single-region workloads

### Well-Architected
- **Reliability**: Multi-region, scanning
- **Security**: Scanning, IAM, CMEK
- **Cost**: Lifecycle policies, regional storage
