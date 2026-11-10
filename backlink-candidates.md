# Backlink candidates for definition pages

Snapshot of `content/en` on 2026-11-10. Re-run the scan after a new sync because the definition
set grows with each vault import.

Applied in the first pass: 123 links across 45 pages, plus 11 retargeted links that pointed at the
AWS IAM and VPC pages from GCP pages. Net post-to-definition links rose from 231 to 283 in
`content/en`, and orphans fell from 142 to 121.

What is left: 222 definitions, 47 post pages with at least one candidate,
535 plain-text mentions that name a definition the page does not link.
121 definitions still have zero inbound wikilinks.

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
| `notes/gcp/readme.md` | `[[gcp/cloud-run\|Cloud Run]]` L70 | `[[gcp/cloud-sql\|Cloud SQL]]` L82 |
| `notes/certifications/4-solutions-architect-associate-saa-c03.md` | `[[cloud/disaster-recovery\|Disaster Recovery]]` L240 | `[[aws/application-integration-sqs\|SQS]]` L597 |
| `notes/react/react.md` | `[[web/component\|component]]` L62 | `[[web/hook\|Hooks]]` L20 |
| `projects/body-power-gym.md` | `[[aws/compute-fargate\|Fargate]]` L45 | `[[cloud/infrastructure-as-code\|Infrastructure as Code]]` L51 |
| `four-hats/episodes/ep03-run-the-app.md` | `[[cloud/containers\|containers]]` L10 |  |

## Top targets

| Definition | Pages | Mentions | Inbound now |
|---|---|---|---|
| `cloud/containers` | 23 | 70 | 4 |
| `web/component` | 6 | 48 | 1 |
| `cloud/logging` | 8 | 21 | 1 |
| `cloud/region` | 10 | 19 | 1 |
| `aws/compute-lambda` | 3 | 16 | 2 |
| `web/hook` | 3 | 11 | 1 |
| `cloud/disaster-recovery` | 2 | 10 | 2 |
| `gcp/cloud-run` | 2 | 10 | 4 |
| `aws/application-integration-sns` | 1 | 9 | 1 |
| `aws/application-integration-sqs` | 1 | 9 | 1 |
| `aws/machine-learning-glue` | 1 | 9 | 0 |
| `aws/compute-fargate` | 2 | 8 | 0 |
| `aws/management-and-governance-cloudtrail` | 1 | 8 | 1 |
| `cloud/scalability` | 6 | 8 | 0 |
| `aws/analytics-kinesis` | 1 | 7 | 0 |
| `aws/management-and-governance-auto-scaling` | 2 | 7 | 0 |
| `aws/networking-direct-connect` | 1 | 7 | 0 |
| `aws/storage-ebs` | 1 | 7 | 0 |
| `gcp/compute-engine` | 2 | 7 | 6 |
| `gcp/cloud-functions` | 2 | 7 | 0 |

## Certification notes (mostly AWS)

### `notes/certifications/4-solutions-architect-associate-saa-c03.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 240 | `[[cloud/disaster-recovery\|Disaster Recovery]]` | strong | - Multi-AZ setup for Disaster Recovery |
| 597 | `[[aws/application-integration-sqs\|SQS]]` | strong | ## SQS |
| 627 | `[[aws/application-integration-sns\|SNS]]` | strong | ## SNS |
| 925 | `[[aws/machine-learning-glue\|Glue]]` | strong | - Use Glue to convery your data to Parquet |
| 1121 | `[[aws/management-and-governance-cloudtrail\|CloudTrail]]` | strong | ### CloudTrail |

29 more definitions appear on this page: `aws/storage-ebs`, `aws/networking-direct-connect`, `aws/analytics-kinesis`, `aws/security-kms`, `aws/compute-fargate`, `cloud/cidr`, `aws/management-and-governance-auto-scaling`, `aws/analytics-redshift`, `aws/security-cognito`, `aws/storage-efs`, `aws/containers-eks`, `aws/networking-api-gateway` and 17 more.

### `notes/certifications/7-certified-kubernetes-application-developer-ckad.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 20 | `[[cloud/containers\|Containers]]` | loose | Containers that run before the main container and have to succeed for the main container to run. **The InitCon |
| 43 | `[[cloud/scalability\|Scalability]]` | loose | ### Deployment Scalability |

## GCP notes

### `notes/gcp/readme.md`  (imported from `ObsidianVault/studies/cloud-architecht/gcp/README.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 70 | `[[gcp/cloud-run\|Cloud Run]]` | strong | - Cloud Run - Services vs Jobs |
| 82 | `[[gcp/cloud-sql\|Cloud SQL]]` | strong | - Cloud SQL - MySQL, PostgreSQL, SQL Server |
| 62 | `[[gcp/cloud-monitoring\|Cloud Monitoring]]` | strong | - Cloud Monitoring - Ops Agent |
| 68 | `[[gcp/compute-engine\|Compute Engine]]` | strong | - Compute Engine - Machine types, preemptible VMs |
| 77 | `[[gcp/persistent-disk\|Persistent Disk]]` | strong | - Persistent Disk - Zonal vs Regional |

46 more definitions appear on this page: `gcp/firestore`, `gcp/gemini`, `cloud/cost-optimization-pillar`, `gcp/cloud-functions`, `gcp/cloud-spanner`, `gcp/bigtable`, `gcp/deployment-strategies`, `gcp/filestore`, `gcp/private-google-access-vs-psc`, `gcp/cloud-load-balancing`, `gcp/alloydb`, `gcp/cloud-kms` and 34 more.

### `notes/gcp/4-managing-operations.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 36 | `[[gcp/cloud-storage\|Cloud Storage]]` | strong | - Gotcha: a [[vpc-service-controls/VPC-SC]] perimeter restricting Cloud Storage breaks `gcloud builds submit`  |
| 52 | `[[gcp/vpc\|VPC]]` | strong | / VPC Flow Logs / L3/L4 flows (5-tuple, bytes/packets) / Enable per subnet (all-or-nothing); aggregation inter |
| 58 | `[[gcp/cloud-functions\|Cloud Functions]]` | strong | **Incident response flow:** detect (Event Threat Detection, audit logs, SCC findings), notify (SCC notificatio |
| 97 | `[[gcp/dataflow\|Dataflow]]` | strong | - Splunk: export JSON to Pub/Sub (Dataflow onward); GCS exports: lifecycle to Nearline/Coldline then delete. |
| 46 | `[[cloud/logging\|logging]]` | loose | ### 4.2 Configuring logging, monitoring, and detection |

1 more definitions appear on this page: `cloud/region`.

### `notes/gcp/2-network-security.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 104 | `[[cloud/sla\|SLA]]` | strong | / On-prem to VPC / HA VPN (one gateway, two interfaces, 2+ tunnels, 99.99% SLA) or [[cloud-interconnect/Cloud  |
| 64 | `[[gcp/cloud-logging\|Cloud Logging]]` | strong | - Firewall Rules Logging is per rule (never on the two implied rules) and exports to Cloud Logging, Pub/Sub, o |
| 64 | `[[gcp/pub-sub\|Pub/Sub]]` | strong | - Firewall Rules Logging is per rule (never on the two implied rules) and exports to Cloud Logging, Pub/Sub, o |
| 66 | `[[cloud/serverless\|serverless]]` | strong | - Cloud Armor also supports serverless NEGs (App Engine, Cloud Run, Functions), Internet NEGs (hybrid/multiclo |
| 66 | `[[gcp/app-engine\|App Engine]]` | strong | - Cloud Armor also supports serverless NEGs (App Engine, Cloud Run, Functions), Internet NEGs (hybrid/multiclo |

5 more definitions appear on this page: `gcp/cloud-run`, `gcp/compute-engine`, `gcp/gke`, `cloud/logging`, `cloud/region`.

### `notes/gcp/3-data-protection.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 97 | `[[gcp/dataflow\|Dataflow]]` | strong | - Confidential family: Confidential VM, GKE Nodes, Dataflow, Dataproc, Space; SEV VMs on N2D support live migr |
| 97 | `[[gcp/dataproc\|Dataproc]]` | strong | - Confidential family: Confidential VM, GKE Nodes, Dataflow, Dataproc, Space; SEV VMs on N2D support live migr |
| 106 | `[[cloud/principle-of-least-privilege\|least privilege]]` | strong | - Data: Sensitive Data Protection discovery and redaction on training data, CMEK on data and model artifacts,  |
| 128 | `[[gcp/private-google-access-vs-psc\|Private Service Connect]]` | strong | - Private Service Connect endpoints for Vertex AI give private access from your VPC, including multicloud acce |
| 37 | `[[cloud/logging\|logging]]` | loose | - **[[secret-manager/Secret Manager]]:** versions (enable/disable/destroy), replication policy (auto or user-m |

3 more definitions appear on this page: `cloud/region`, `gcp/cloud-vpn`, `cloud/governance-and-compliance`.

### `notes/gcp/1-configuring-access.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 102 | `[[cloud/region\|regions]]` | loose | - Workspace-specific controls to know by name: Drive external sharing settings and Trust rules, context-aware  |

### `notes/gcp/5-compliance.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 23 | `[[cloud/region\|regions]]` | loose | - **Assured Workloads:** creates a folder with enforced compliance regime (FedRAMP Moderate/High, IL2/4/5, CJI |

### `notes/gcp/final-week-checklist.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 38 | `[[gcp/vertex-ai\|Vertex AI]]` | strong | - [ ] Know the Vertex AI specifics: dedicated VPC-SC perimeters, public endpoint gated by an access level, PSC |
| 36 | `[[gcp/cloud-vpn\|HA VPN]]` | loose | - [ ] Know encryption in transit: SSL policies, IPsec on HA VPN, MACsec on Dedicated Interconnect. |

### `notes/gcp/pcse-home.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 62 | `[[cloud/logging\|Logging]]` | loose | / 4. Operations / RPO/RTO and backups; Web Security Scanner; Security Command Center; Cloud Logging and sinks; |

### `notes/gcp/cheat-sheets.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 59 | `[[cloud/containers\|containers]]` | loose | 6. Lateral movement in containers -> Container Threat Detection. |

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
| 26 | `[[cloud/containers\|containers]]` | loose | - Hardened containers: multi-stage builds, non root user, [[cloud/principle-of-least-privilege/POLP]] |

### `notes/react/react-router-loaders.md`  (imported from `ObsidianVault/webdev/react/react-router/loaders.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 16 | `[[web/component\|component]]` | loose | - Loaders load data before component renders |

### `notes/devops/week6-project.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 17 | `[[cloud/scalability\|scalability]]` | loose | You’re the core tech team at a company that migrated a legacy app from a single on-prem VM to Azure because th |

### `notes/interviews/interview-prep.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 198 | `[[cloud/scalability\|scalability]]` | loose | > Some advantages of using OOPs in Java include code reusability, modularity, flexibility, scalability, and ea |

### `notes/interviews/study-guide-for-technical-interview.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 73 | `[[cloud/logging\|Logging]]` | loose | - Monitoring and Logging (Prometheus, Grafana, ELK stack) |

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

### `projects/body-power-gym.md`  (imported from `portfolio/src/data/body-power-gym.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 45 | `[[aws/compute-fargate\|Fargate]]` | strong | - **AWS Services**: VPC, [[aws/containers-ecs/ECS]] Fargate, ALB, [[aws/containers-ecr/ECR]], CodeBuild, [[aws |
| 51 | `[[cloud/infrastructure-as-code\|Infrastructure as Code]]` | strong | - **DevOps**: Infrastructure as Code (soon!), configuration management, deployment automation, rollback strate |
| 77 | `[[aws/management-and-governance-auto-scaling\|Auto Scaling]]` | strong | Unlike the backend instance, the frontend container would be the one always running, and getting **Auto Scalin |
| 45 | `[[aws/management-and-governance-cloudformation\|CloudFormation]]` | strong | - **AWS Services**: VPC, [[aws/containers-ecs/ECS]] Fargate, ALB, [[aws/containers-ecr/ECR]], CodeBuild, [[aws |
| 49 | `[[cloud/logging\|log aggregation]]` | strong | - **Monitoring**: CloudWatch metrics, EventBridge rules, alerting systems, log aggregation |

4 more definitions appear on this page: `aws/storage-s3`, `aws/networking-api-gateway`, `aws/compute-lambda`, `cloud/scalability`.

### `projects/image-captioning.md`  (imported from `portfolio/src/data/image-captioning.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 60 | `[[aws/networking-cloudfront\|CloudFront]]` | strong | 4. `invalidate_cache`: Invalidates the CloudFront CDN cache so that the newly-built version is served to the u |
| 101 | `[[aws/application-integration-step-functions\|Step Functions]]` | strong | - **Asynchronous Execution**: For Lambdas, I was envisioning a workflow for the image like this: `upload-to-s3 |
| 64 | `[[aws/compute-lambda\|Lambda]]` | loose | Next, I created two Lambda functions. One function receives an image file `image/*` from the frontend, and upl |
| 49 | `[[aws/free-services\|free tier]]` | loose | The main concern to me was the cost of building this project. However, knowing that most of the services I dec |

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

Zero inbound wikilinks: 121 of 222.

### Orphans that already appear in a post

- `aws/analytics-athena` `aws/analytics-kinesis` `aws/analytics-redshift` `aws/application-integration-step-functions` `aws/compute-beanstalk` `aws/compute-fargate`
- `aws/containers-eks` `aws/ec2-user-data` `aws/financial-management-budgets` `aws/free-services` `aws/machine-learning-glue` `aws/management-and-governance-auto-scaling`
- `aws/management-and-governance-cloudformation` `aws/management-and-governance-config` `aws/management-and-governance-systems-manager` `aws/networking-direct-connect` `aws/networking-vpn` `aws/security-guardduty`
- `aws/storage-ebs` `cloud/generative-ai` `cloud/governance-and-compliance` `cloud/migration-strategies` `cloud/scalability` `cloud/tagging`
- `gcp/alloydb` `gcp/bigtable` `gcp/cloud-composer` `gcp/cloud-functions` `gcp/cloud-profiler` `gcp/cloud-spanner`
- `gcp/cloud-trace` `gcp/dataflow` `gcp/dataproc` `gcp/error-reporting` `gcp/filestore` `gcp/firestore`
- `gcp/memorystore` `react/provider` `web/props`

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
- `gcp/devops-labs` `gcp/eventarc` `gcp/management-labs` `gcp/migration-framework` `gcp/ops-labs` `gcp/storage-labs`
- `gcp/workflows` `networking/main` `react/react-lazy` `web/pure-functions`

The AWS service pages are all orphans today. The fastest win is one link per service from
`notes/certifications/4-solutions-architect-associate-saa-c03.md` and `projects/image-captioning.md`.

## Wrong targets fixed

| Where | Problem |
|---|---|
| `notes/gcp/readme.md` (6 links) | `[[security-iam\|IAM]]` and `[[networking-vpc\|VPC]]` pointed at the AWS pages from a GCP note. Retargeted to `iam` and `vpc`. |
| `definitions/gcp/*.md` (4 links in `gke.md`) | Same retarget inside the GKE definition page. |
| `notes/certifications/10-professional-cloud-architect-pca.md` line 17 | The line compares AWS IAM with GCP Service Accounts. It now links to `aws/security-iam`. |

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

