---
title: Cloud-build
category: GCP
description: 'GCP note: Cloud-build.'
tags:
- gcp
- devops
---


# Cloud-build

`gcp` `devops`

## Cloud Build
**Fully managed CI/CD** platform

**AWS Equivalent:** AWS CodeBuild + CodePipeline

### Overview
- Build, test, and deploy on Google Cloud
- **Serverless**, no build servers to manage
- Native Docker support
- Integrates with GitHub, Bitbucket, Cloud Source Repositories
- Build triggers on git events

### Build Configuration
#### cloudbuild.yaml
```yaml
steps:
- name: 'gcr.io/cloud-builders/docker'
  args: ['build', '-t', 'gcr.io/$PROJECT_ID/myapp', '.']
- name: 'gcr.io/cloud-builders/docker'
  args: ['push', 'gcr.io/$PROJECT_ID/myapp']
- name: 'gcr.io/cloud-builders/gcloud'
  args: ['run', 'deploy', 'myapp', '--image', 'gcr.io/$PROJECT_ID/myapp', '--region', 'us-central1']
```

### Build Steps
- Each step runs in a Docker container
- **Steps execute sequentially** by default
- Can specify custom builder images
- Share artifacts via `/workspace` directory

### Build Triggers
| Source | Events |
|---|---|
| GitHub | Push, pull request, tag |
| Bitbucket | Push, pull request |
| Cloud Source Repositories | Push, tag |

- **Automatic builds on code changes**
- Branch/tag filters

### Substitution Variables
| Variable | Value |
|---|---|
| `$PROJECT_ID` | Project ID |
| `$BUILD_ID` | Build ID |
| `$COMMIT_SHA` | Git commit SHA |
| `$BRANCH_NAME` | Git branch |
| `$_VAR_NAME` | Custom variable |

### Artifact Storage
- Build artifacts to [[gcp/cloud-storage|Cloud Storage]]
- Container images to [[artifact-registry|Artifact Registry]]/Container Registry
- Build logs to Cloud Logging

### Private Pools
- **Dedicated worker VMs** in your VPC
- Access private resources (Cloud SQL, internal IPs)
- Custom machine types
- Higher security

### Build Timeout & Pricing
| Setting | Value |
|---|---|
| Default timeout | 10 minutes |
| Max timeout | 24 hours |
| Free tier | 120 build-minutes/day |
| Pricing | $0.003 per build-minute (after free tier) |

---

## ACE Level

### Essential Commands
```bash
# Submit build manually
gcloud builds submit --config=cloudbuild.yaml .

# Submit with substitutions
gcloud builds submit --substitutions=_ENV=prod .

# Create trigger
gcloud builds triggers create github \
  --repo-name=my-repo \
  --repo-owner=my-org \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml

# List builds
gcloud builds list

# View build logs
gcloud builds log BUILD_ID

# List triggers
gcloud builds triggers list
```

### Key Concepts for ACE
- Creating cloudbuild.yaml files
- Submitting builds manually
- Creating build triggers for GitHub repos
- Understanding build steps and builders
- Viewing build logs
- Using substitution variables

---

## PCA Level

### CI/CD Pipeline
```text
Git Push → Cloud Build Trigger → Build & Test → Push to Artifact Registry
                                               → Deploy to Cloud Run
                                               → Notify via Pub/Sub
```

### Multi-Stage Builds
```yaml
# Build stage
- name: 'maven'
  args: ['mvn', 'clean', 'package']

# Test stage
- name: 'maven'
  args: ['mvn', 'test']

# Docker build
- name: 'gcr.io/cloud-builders/docker'
  args: ['build', '-t', '$_IMAGE_NAME', '.']

# Deploy stage
- name: 'gcr.io/cloud-builders/gcloud'
  args: ['run', 'deploy', ...]
```

### Security Best Practices
- **Service account**: Least privilege for builds
- **Private pools**: For sensitive builds
- **Secrets**: [[secret-manager|Secret Manager]] integration
- **VPC**: Private pools in VPC
- **IAM**: Control who can trigger builds

### Integration Patterns
- **Cloud Build** → Cloud Deploy → Multi-env deployment
- **Cloud Build** + **Binary Authorization** → Verified deployments
- **Cloud Build** + **Pub/Sub** → Event-driven workflows

### Cost Optimization
- Use free tier (120 min/day)
- Optimize build steps
- Cache dependencies
- Parallel steps where possible

### Well-Architected Considerations
- **Operational Excellence**: Automated builds, infrastructure as code
- **Reliability**: Automated testing, reproducible builds
- **Security**: Private pools, service accounts, secret management
- **Performance**: Parallel builds, caching, optimized images
- **Cost**: Free tier, efficient builds
