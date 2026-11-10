# Backlink candidates for definition pages

Snapshot of `content/en` on 2026-11-10. Re-run the scan after a new sync because the definition
set grows with each vault import.

222 definitions, 45 post pages with at least one candidate,
303 plain-text mentions that name a definition the page does not link.
102 definitions still have zero inbound wikilinks.

Applied so far: 153 links across 50 pages, 74 wrong-target links retargeted in GCP pages, and an
import fix that restores wiki links written as relative paths in the vault. Post-to-definition links
in `content/en` rose from 231 to 408. Orphan definitions fell from 142 to 102. Links now live in
the vault and the portfolio/four-hats sources, so `sync.py` keeps them.

Matching rules: frontmatter, fenced code, inline code, existing links and link targets are ignored.
One link per definition per page, first plain mention only. `IAM`, `VPC` and `KMS` are routed to the
AWS page on AWS posts and to the GCP page on GCP posts. Line numbers are from the current files,
so edit a file from the bottom up.

Fit: `strong` means the mention is unambiguous. `loose` means the word has other meanings and the
link is optional. Pick 2 to 4 links per page. Do not link every row in a table.

Syntax: `[[slug|anchor]]`. A bare slug works only when the file stem is unique. Two stems are
duplicated (`deployment-strategies`, `docs-system`), so the blog must link to
`[[gcp/deployment-strategies|deployment strategies]]`.

## Start here

One page from each section, two links each. These give the most coverage for the least editing.

| Page | Link 1 | Link 2 |
|---|---|---|
| `notes/certifications/4-solutions-architect-associate-saa-c03.md` | `[[aws/storage-ebs\|EBS]]` L189 | `[[aws/networking-direct-connect\|Direct Connect]]` L533 |
| `notes/react/react.md` | `[[web/component\|component]]` L62 | `[[web/hook\|Hooks]]` L20 |
| `projects/image-captioning.md` | `[[aws/application-integration-step-functions\|Step Functions]]` L101 | `[[aws/compute-lambda\|Lambda]]` L64 |
| `four-hats/episodes/ep03-run-the-app.md` | `[[cloud/containers\|containers]]` L10 |  |
| `notes/gcp/4-managing-operations.md` | `[[cloud/logging\|logging]]` L46 | `[[cloud/region\|region]]` L92 |

## Top targets

| Definition | Pages | Mentions | Inbound now |
|---|---|---|---|
| `cloud/containers` | 23 | 70 | 4 |
| `web/component` | 6 | 48 | 1 |
| `cloud/region` | 10 | 19 | 1 |
| `cloud/logging` | 6 | 18 | 2 |
| `aws/compute-lambda` | 3 | 16 | 2 |
| `web/hook` | 3 | 11 | 1 |
| `aws/analytics-kinesis` | 1 | 7 | 0 |
| `aws/networking-direct-connect` | 1 | 7 | 0 |
| `aws/storage-ebs` | 1 | 7 | 0 |
| `cloud/scalability` | 5 | 7 | 0 |
| `cloud/cidr` | 1 | 6 | 5 |
| `aws/compute-fargate` | 1 | 6 | 1 |
| `aws/security-kms` | 1 | 6 | 1 |
| `web/props` | 2 | 6 | 0 |
| `aws/analytics-redshift` | 1 | 5 | 0 |
| `aws/management-and-governance-auto-scaling` | 1 | 5 | 1 |
| `cloud/governance-and-compliance` | 2 | 4 | 0 |
| `aws/containers-eks` | 1 | 4 | 0 |
| `aws/networking-api-gateway` | 2 | 4 | 1 |
| `aws/security-cognito` | 1 | 4 | 1 |

## Certification notes (mostly AWS)

### `notes/certifications/4-solutions-architect-associate-saa-c03.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 189 | `[[aws/storage-ebs\|EBS]]` | strong | Configurations for your launched instances detailing information like: AMI and Instance Type, EC2 User Data, E |
| 533 | `[[aws/networking-direct-connect\|Direct Connect]]` | strong | - Accessed on prem using VPN or Direct Connect |
| 640 | `[[aws/analytics-kinesis\|Kinesis]]` | strong | - Kinesis Data Firehose |
| 377 | `[[aws/security-kms\|AWS KMS]]` | strong | - Database Master & Replicas encryption using AWS KMS - Must be defined as launch time |
| 716 | `[[aws/compute-fargate\|Fargate]]` | strong | - Fargate - Serverless, no provisioning. Create **Task Definition** and AWS will run the task based on CPU / R |

24 more definitions appear on this page: `cloud/cidr`, `aws/management-and-governance-auto-scaling`, `aws/analytics-redshift`, `aws/security-cognito`, `aws/storage-efs`, `aws/containers-eks`, `aws/networking-api-gateway`, `aws/analytics-athena`, `aws/application-integration-eventbridge`, `aws/management-and-governance-cloudformation`, `aws/containers-ecr`, `aws/ec2-user-data` and 12 more.

### `notes/certifications/7-certified-kubernetes-application-developer-ckad.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 20 | `[[cloud/containers\|Containers]]` | loose | Containers that run before the main container and have to succeed for the main container to run. **The InitCon |
| 43 | `[[cloud/scalability\|Scalability]]` | loose | ### Deployment Scalability |

## GCP notes

### `notes/gcp/4-managing-operations.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 46 | `[[cloud/logging\|logging]]` | loose | ### 4.2 Configuring logging, monitoring, and detection |
| 92 | `[[cloud/region\|region]]` | loose | - Packet Mirroring: copies headers plus payloads, consumes VM (not network) bandwidth; sources: subnets, tags, |

### `notes/gcp/readme.md`  (imported from `ObsidianVault/studies/cloud-architecht/gcp/README.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 273 | `[[cloud/disaster-recovery\|Disaster recovery]]` | strong | - Disaster recovery strategies |
| 309 | `[[cloud/total-cost-of-ownership\|TCO]]` | strong | 1. **Assess**: TCO calculation, workload prioritization (low complexity + high value first) |
| 363 | `[[cloud/operational-excellence-pillars\|Operational Excellence]]` | strong | 1. **Operational Excellence**: 4 golden signals (latency, traffic, errors, saturation), SLI/SLO/error budgets |
| 550 | `[[cloud/migration-strategies\|migration strategies]]` | strong | - Advanced topics: Multi-region deployments, hybrid architectures, migration strategies |
| 219 | `[[cloud/logging\|logging]]` | loose | - [[gcp/cloud-logging/Cloud Logging]] - Log analytics, centralized logging |

1 more definitions appear on this page: `cloud/containers`.

### `notes/gcp/2-network-security.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 66 | `[[gcp/cloud-run\|Cloud Run]]` | strong | - Cloud Armor also supports [[serverless/serverless]] NEGs ([[app-engine/App Engine]], Cloud Run, Functions),  |
| 77 | `[[gcp/compute-engine\|Compute Engine]]` | strong | - **Peering restrictions (2025 exam reports):** no overlapping [[cidr/CIDR]] ranges between peers; firewall ru |
| 78 | `[[gcp/gke\|GKE]]` | strong | - **N-tier isolation:** tiered subnets + NGFW policies per tier + secure tags; private GKE clusters for the da |
| 32 | `[[cloud/logging\|logging]]` | loose | - **Tiers:** Cloud NGFW Essentials (rules, logging), Enterprise (adds Layer 7 filtering and TLS inspection wit |
| 114 | `[[cloud/region\|region]]` | loose | - HA VPN: one gateway with two interfaces (two reserved public IPs), at least two tunnels originating in the s |

### `notes/gcp/3-data-protection.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 37 | `[[cloud/logging\|logging]]` | loose | - **[[secret-manager/Secret Manager]]:** versions (enable/disable/destroy), replication policy (auto or user-m |
| 37 | `[[cloud/region\|regions]]` | loose | - **[[secret-manager/Secret Manager]]:** versions (enable/disable/destroy), replication policy (auto or user-m |
| 71 | `[[gcp/cloud-vpn\|HA VPN]]` | loose | - Hybrid: HA VPN encrypts with IPsec by default; Dedicated Interconnect can be encrypted with MACsec (also IPs |
| 109 | `[[cloud/governance-and-compliance\|Governance]]` | loose | - Governance: SAIF (Secure AI Framework) is Google's blueprint for AI security. SCC gives AI asset discovery ( |

### `notes/gcp/1-configuring-access.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 102 | `[[cloud/region\|regions]]` | loose | - Workspace-specific controls to know by name: Drive external sharing settings and Trust rules, context-aware  |

### `notes/gcp/5-compliance.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 23 | `[[cloud/region\|regions]]` | loose | - **Assured Workloads:** creates a folder with enforced compliance regime (FedRAMP Moderate/High, IL2/4/5, CJI |

### `notes/gcp/pcse-home.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 62 | `[[cloud/logging\|Logging]]` | loose | / 4. Operations / RPO/RTO and backups; Web Security Scanner; Security Command Center; Cloud Logging and sinks; |

### `notes/gcp/cheat-sheets.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 59 | `[[cloud/containers\|containers]]` | loose | 6. Lateral movement in containers -> Container Threat Detection. |

### `notes/gcp/final-week-checklist.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 36 | `[[gcp/cloud-vpn\|HA VPN]]` | loose | - [ ] Know encryption in transit: SSL policies, IPsec on HA VPN, MACsec on Dedicated Interconnect. |

## Other notes

### `notes/react/react.md`  (imported from `ObsidianVault/webdev/react/react.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 62 | `[[web/component\|component]]` | loose | - Get the `dispatch` function using the `useDispatch()` hook inside a subscribed component of the `store` |
| 20 | `[[web/hook\|Hooks]]` | loose | ## Hooks |
| 475 | `[[web/props\|props]]` | loose | ## Render props |
| 271 | `[[react/provider\|provider]]` | loose | 8. In `index.js` import the `store` we just made and supply it to the entire app with the provider |

### `notes/react/react-router-forms.md`  (imported from `ObsidianVault/webdev/react/react-router/forms.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 43 | `[[web/hook\|hook]]` | loose | - Use `redirect()` instead of [[react-router-usenavigate/useNavigate]] when not in a hook or component. |
| 43 | `[[web/component\|component]]` | loose | - Use `redirect()` instead of [[react-router-usenavigate/useNavigate]] when not in a hook or component. |

### `notes/devops/week3-day4.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 17 | `[[cloud/scalability\|scalability]]` | loose | - Stress test to show scalability |
| 26 | `[[cloud/containers\|containers]]` | loose | - Hardened containers: multi-stage builds, non root user, [[principle-of-least-privilege/POLP]] |

### `notes/react/react-router-loaders.md`  (imported from `ObsidianVault/webdev/react/react-router/loaders.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 16 | `[[web/component\|component]]` | loose | - Loaders load data before component renders |

### `notes/devops/week6-project.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 17 | `[[cloud/scalability\|scalability]]` | loose | You’re the core tech team at a company that migrated a legacy app from a single on-prem VM to Azure because th |

### `notes/react/main-concepts.md`  (imported from `ObsidianVault/webdev/react/main-concepts.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 28 | `[[web/props\|Props]]` | loose | - Props change |

### `notes/react/react-router-error-handling.md`  (imported from `ObsidianVault/webdev/react/react-router/error-handling.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 18 | `[[web/component\|component]]` | loose | Provide the parent route or any routes that may cause errors by loading with a `errorElement` component to sho |

### `notes/react/react-router-setting-routes.md`  (imported from `ObsidianVault/webdev/react/react-router/setting-routes.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 32 | `[[web/component\|component]]` | loose | - For an AppLayout component, make it the parent of paths that it lays out and make it not have a path |

### `notes/react/react-router-usenavigate.md`  (imported from `ObsidianVault/webdev/react/react-router/useNavigate.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 15 | `[[web/hook\|hook]]` | loose | Navigator hook that returns a function to change the URL. |

## Project pages

### `projects/image-captioning.md`  (imported from `portfolio/src/data/image-captioning.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 101 | `[[aws/application-integration-step-functions\|Step Functions]]` | strong | - **Asynchronous Execution**: For Lambdas, I was envisioning a workflow for the image like this: `upload-to-s3 |
| 64 | `[[aws/compute-lambda\|Lambda]]` | loose | Next, I created two Lambda functions. One function receives an image file `image/*` from the frontend, and upl |
| 49 | `[[aws/free-services\|free tier]]` | loose | The main concern to me was the cost of building this project. However, knowing that most of the services I dec |

### `projects/body-power-gym.md`  (imported from `portfolio/src/data/body-power-gym.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 67 | `[[aws/storage-s3\|S3]]` | strong | I went with Strapi because it seemed easy to work with, just looking at the documentation. (And it was.) It al |
| 113 | `[[aws/networking-api-gateway\|API Gateway]]` | strong | Webhooks are wonderful. They are basically a way for service A to notify service B that an event occurred. In  |
| 45 | `[[aws/compute-lambda\|Lambda]]` | loose | - **AWS Services**: VPC, [[aws/containers-ecs/ECS]] [[aws/compute-fargate/Fargate]], ALB, [[aws/containers-ecr |
| 75 | `[[cloud/scalability\|scalability]]` | loose | I also thought, why not containerize? Containerization would tremendously help with scalability of the website |

### `projects/aws-budget-discord-notifs.md`  (imported from `portfolio/src/data/aws-budget-discord-notifs.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 43 | `[[aws/compute-lambda\|Lambda]]` | loose | - `AWS_ACCESS_KEY`: AWS Access Key with access to Lambda, [[aws/application-integration-sns/SNS]], Budgets, an |
| 49 | `[[cloud/region\|region]]` | loose | - `AWS_REGION`: Primary region to deploy to |

### `projects/azure-3t-app.md`  (imported from `portfolio/src/data/azure-3t-app.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 28 | `[[cloud/cloud-computing\|Cloud Computing]]` | strong | The frontend and backend code was provided by Mr. Saurabh Dhingra ([github/saurabhd2106](https://github.com/sa |
| 18 | `[[cloud/containers\|containers]]` | loose | Azure Three-Tier web app deployed using Terraform and containers |

### `projects/e2e-automated-deployment-azure.md`  (imported from `portfolio/src/data/e2e-automated-deployment-azure.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 130 | `[[cloud/scalability\|Scalability]]` | loose | - **Scalability**: Easy to add new resources without affecting existing ones |
| 182 | `[[cloud/region\|regions]]` | loose | - Reproducible environments across regions or subscriptions |
| 197 | `[[cloud/logging\|logging]]` | loose | **Application Gateway 403 Errors**: After provisioning the Application Gateway, we encountered persistent 403  |

### `projects/tuwaiq-tracker.md`  (imported from `portfolio/src/data/tuwaiq-tracker.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 106 | `[[web/component\|components]]` | loose | The final product did adapt the main components, so I was happy with the design overall. Next, I started build |

### `projects/catus-locatus.md`  (imported from `portfolio/src/data/catus-locatus.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 32 | `[[cloud/cloud-computing\|Cloud Computing]]` | strong | I was sponsored by [Saudi Digital Academy (SDA)](https://sda.edu.sa/) to attend a 3-month [DevOps & Cloud Comp |
| 58 | `[[aws/free-services\|free tier]]` | loose | I began on creating a backend, because in my original project I was using `supabase`, which is a platform that |

### `projects/grooszy/API.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 588 | `[[cloud/tagging\|tagging]]` | loose | normalized merchant name, plus manual merchant tagging. Per month: outflow total, |

## Course and site pages

### `four-hats/episodes/ep03-run-the-app.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 10 | `[[cloud/containers\|containers]]` | loose | / You build / Three containers on one Docker network, with the app reachable at `http://localhost:8080` / |

### `four-hats/episodes/ep05-containers.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 1 | `[[cloud/containers\|Containers]]` | loose | # SWE-05: Containers |

### `four-hats/episodes/ep07-plan-the-infrastructure.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 11 | `[[cloud/region\|region]]` | loose | / Done when / The plan names the service model, region, zone, VM size, [[gcp/vpc/VPC]] and subnet, open ports, |
| 138 | `[[cloud/containers\|containers]]` | loose | 6. The three containers. |

### `four-hats/episodes/ep11-hello-kubernetes.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 37 | `[[cloud/containers\|containers]]` | loose | A cluster is a set of machines that run containers. The control plane decides, and the nodes run the Pods. A P |

### `four-hats/cleanup-guide.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 9 | `[[cloud/containers\|containers]]` | loose | 1. Stop both Compose projects. Delete their containers, networks, volumes, and images: |

### `four-hats/episodes/ep01-set-up-your-laptop.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 36 | `[[cloud/containers\|containers]]` | loose | / Docker Desktop / Runs containers for the app, the database, and the course tools. / All / |

### `four-hats/episodes/ep14-state.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 76 | `[[cloud/containers\|containers]]` | loose | The StatefulSet in this act runs two containers in one Pod: `postgres` and `postgres-exporter`. That is why th |

### `four-hats/costs-and-free-options.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 9 | `[[cloud/containers\|Containers]]` | loose | / Docker Desktop / Containers / Free for personal use and education / |
| 23 | `[[cloud/region\|regions]]` | loose | - Google Cloud also has an Always Free tier. It includes one `e2-micro` VM in some US regions. |

### `four-hats/episodes/ep10-now-in-the-cloud.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 40 | `[[cloud/containers\|containers]]` | loose | Terraform and the `gcloud` command run in containers. Sign in and enable the Compute Engine API: |
| 75 | `[[cloud/region\|region]]` | loose | - `variables.tf`: project ID, region, zone, machine type, SSH public key, and your IP in [[cloud/cidr/CIDR]] f |

### `four-hats/episodes/ep12-services-and-troubleshooting.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 83 | `[[cloud/containers\|Containers]]` | loose | / Kubernetes (Pods, Deployments, Services) / 11, 12 / Containers & Orchestration / Deployed a three-tier app t |

### `four-hats/episodes/ep13-configuration.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 28 | `[[cloud/containers\|containers]]` | loose | Wiring decides how a setting reaches a container. `envFrom` loads every key from a ConfigMap as an environment |

### `four-hats/episodes/ep15-scale.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 130 | `[[cloud/containers\|Containers]]` | loose | / Autoscaling (HPA), resource management / 15 / Containers and Orchestration / Set requests, limits, and probe |

### `four-hats/setup.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 9 | `[[cloud/containers\|containers]]` | loose | / Docker Desktop / Runs containers and the course tools / |

### `four-hats/episodes/ep00-four-careers-one-project.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 115 | `[[cloud/containers\|Containers]]` | loose | / Docker Desktop and Minikube / Containers and a local Kubernetes cluster / Free / |

### `four-hats/episodes/ep02-git-and-github.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 160 | `[[cloud/containers\|containers]]` | loose | Episode 3 runs the app. You start the database, the backend, and the frontend in three containers on one priva |

### `four-hats/episodes/ep08-your-first-vm.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 44 | `[[cloud/containers\|containers]]` | loose | Both are useful. This act uses a VM because the course needs a real server with its own SSH service, users, an |

### `four-hats/episodes/ep26-build-your-cv.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 46 | `[[cloud/containers\|Containers]]` | loose | - Containers & Orchestration |

## Orphan definitions

Zero inbound wikilinks: 102 of 222.

### Orphans that already appear in a post

- `aws/analytics-athena` `aws/analytics-kinesis` `aws/analytics-redshift` `aws/application-integration-step-functions` `aws/compute-beanstalk` `aws/containers-eks`
- `aws/ec2-user-data` `aws/financial-management-budgets` `aws/free-services` `aws/management-and-governance-config` `aws/management-and-governance-systems-manager` `aws/networking-direct-connect`
- `aws/networking-vpn` `aws/security-guardduty` `aws/storage-ebs` `cloud/governance-and-compliance` `cloud/migration-strategies` `cloud/scalability`
- `cloud/tagging` `react/provider` `web/props`

### Orphans with no mention anywhere

- `aws/allocation-tags` `aws/application-integration-appflow` `aws/aws-compute` `aws/aws-networking` `aws/aws-services` `aws/aws-storage`
- `aws/business-applications-connect` `aws/business-applications-ses` `aws/compute-ec2-ccp` `aws/compute-lightsail` `aws/compute-outposts` `aws/customer-enablement-activate`
- `aws/customer-enablement-aws-vm-import-export` `aws/customer-enablement-repost` `aws/customer-enablement-support-plans` `aws/database-aws-database` `aws/dev-tools-overview` `aws/financial-management-billing-and-cost-management`
- `aws/financial-management-cost-and-usage-reports` `aws/financial-management-cost-explorer` `aws/financial-management-marketplace` `aws/financial-management-pricing-calculator` `aws/front-end-amplify` `aws/front-end-appsync`
- `aws/front-end-device-farm` `aws/iot-overview` `aws/machine-learning-augmented-ai` `aws/machine-learning-bedrock` `aws/machine-learning-codeguru` `aws/machine-learning-deepcomposer`
- `aws/machine-learning-forecast` `aws/machine-learning-kendra` `aws/machine-learning-lex` `aws/machine-learning-panorama` `aws/machine-learning-polly` `aws/machine-learning-q`
- `aws/machine-learning-rekognition` `aws/machine-learning-textract` `aws/machine-learning-transcribe` `aws/machine-learning-translate` `aws/management-and-governance-license-manager` `aws/management-and-governance-organizations`
- `aws/media-services-overview` `aws/migration-application-migration-service` `aws/migration-aws-snow-family` `aws/migration-database-migration-service` `aws/security-artifact` `aws/security-inspector`
- `aws/security-security-token-service` `aws/storage-storage-gateway` `cloud/application-integration` `cloud/c-suite` `cloud/cloud-adoption-framework` `cloud/cloud-hosting`
- `cloud/consolidated-billing` `cloud/csp` `cloud/dedicated-server` `cloud/elasticity` `cloud/fault-tolerance` `cloud/high-durability`
- `cloud/partner-network` `cloud/restful-apis` `cloud/shared-hosting` `cloud/tenets-of-aws` `cloud/totp` `cloud/traditional-ai`
- `cloud/vms-and-containers` `cloud/vps` `gcp/ai-ml-labs` `gcp/compute-labs` `gcp/data-analytics-labs` `gcp/databases-labs`
- `gcp/devops-labs` `gcp/eventarc` `gcp/management-labs` `gcp/ops-labs` `gcp/storage-labs` `networking/main`
- `networking/osi-model` `react/react-lazy` `web/pure-functions`

The AWS service pages are all orphans today. The fastest win is one link per service from
`notes/certifications/4-solutions-architect-associate-saa-c03.md` and `projects/image-captioning.md`.

## Wrong targets found while scanning

| Where | Problem |
|---|---|
| `notes/gcp/readme.md` line 53 | `[[security-iam\|IAM]]` points at the AWS IAM page in a GCP note. Use `[[iam\|IAM]]`. |
| `notes/gcp/readme.md` line 90 | `[[networking-vpc\|VPC]]` points at the AWS VPC page. Use `[[vpc\|VPC]]`. |
| `notes/certifications/10-professional-cloud-architect-pca.md` line 17 | The line compares AWS IAM with GCP Service Accounts. If you link IAM there, use `security-iam`, not `iam`. |

## Do not link these

| Match | Why |
|---|---|
| `Provider` in `projects/grooszy/*`, `fai/*`, `openziti-operator/*` | Identity provider, not React context |
| `Provider` in `notes/certifications/5-terraform-associate-003.md` | Terraform provider |
| `components` in `blogs/alb-in-ack.md` | Alibaba console menu |
| `components` in `blogs/logic-for-documentation.md`, `notes/web/typescript.md`, `notes/web/tailwindcss.md` | Prose, not UI components |
| `VPC` / `IAM` in the AWS certification notes | Already routed to the AWS pages. Do not add the GCP page too |
| `containers` in `projects/catus-locatus.md` line 113 | Azure blob containers |
| `Error reporting` in `notes/devops/week5-day1.md` | Prose, not GCP Error Reporting |
| `Lambda` in `notes/interviews/study-guide-for-technical-interview.md` line 29 | Java lambda expressions |
| `logging` in `blogs/k8s-adventures-pt2.md` | Kubernetes audit log levels |
| `region` in prose | Geography, not a cloud region |

## Apply

1. Authored page under `content/en/`: edit it, then run `build.py`.
2. Page with an `<!-- imported from ... -->` marker: edit the source, then run `sync.py` and `build.py`.
3. `build.py` fails on an unresolved target, so a typo in a slug stops the build.
4. Links convert to relative URLs and feed `assets/backlinks.json`, so every link is a real backlink.

