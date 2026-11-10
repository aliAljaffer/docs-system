# Backlink candidates for definition pages

Snapshot of `content/en` on 2026-11-10. Re-run the scan after a new sync because the definition
set grows with each vault import.

222 definitions, 67 post pages with at least one candidate,
1,209 plain-text mentions that name a definition the page does not link.
142 definitions still have zero inbound wikilinks.

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
| `notes/certifications/4-solutions-architect-associate-saa-c03.md` | `[[aws/compute-ec2\|EC2]]` L64 | `[[aws/networking-vpc\|VPC]]` L434 |
| `notes/gcp/readme.md` | `[[gcp/vpc\|VPCs]]` L114 | `[[gcp/cloud-storage\|Cloud Storage]]` L76 |
| `notes/react/react.md` | `[[react/main-context-concepts\|Context API]]` L300 | `[[react/usereducer\|useReducer]]` L60 |
| `projects/body-power-gym.md` | `[[aws/containers-ecs\|ECS]]` L45 | `[[cloud/containers\|Containerization]]` L46 |
| `four-hats/episodes/ep07-plan-the-infrastructure.md` | `[[gcp/vpc\|VPC]]` L11 | `[[cloud/cidr\|CIDR]]` L19 |
| `blogs/homelab.md` | `[[cloud/disaster-recovery\|disaster recovery]]` L20 |  |

## Top targets

| Definition | Pages | Mentions | Inbound now |
|---|---|---|---|
| `cloud/containers` | 27 | 82 | 0 |
| `gcp/vpc` | 10 | 56 | 1 |
| `cloud/region` | 11 | 48 | 1 |
| `web/component` | 6 | 48 | 1 |
| `aws/compute-ec2` | 1 | 43 | 2 |
| `gcp/iam` | 9 | 38 | 0 |
| `gcp/gke` | 11 | 35 | 6 |
| `aws/storage-s3` | 4 | 33 | 2 |
| `aws/networking-vpc` | 1 | 32 | 3 |
| `aws/compute-lambda` | 4 | 27 | 2 |
| `cloud/serverless` | 5 | 23 | 2 |
| `aws/management-and-governance-cloudwatch` | 3 | 22 | 0 |
| `cloud/logging` | 8 | 21 | 1 |
| `aws/security-iam` | 3 | 20 | 4 |
| `gcp/bigquery` | 5 | 20 | 5 |
| `cloud/infrastructure-as-code` | 9 | 19 | 0 |
| `gcp/compute-engine` | 6 | 19 | 4 |
| `gcp/cloud-storage` | 4 | 18 | 4 |
| `gcp/vertex-ai` | 4 | 18 | 4 |
| `aws/containers-ecs` | 2 | 17 | 1 |

## Blogs

### `blogs/homelab.md`  (imported from `portfolio/src/data/homelab.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 20 | `[[cloud/disaster-recovery\|disaster recovery]]` | strong | The k3s cluster grew up. Talos Linux, full GitOps, real disaster recovery, and three stacked firmware bugs on  |

### `blogs/deployment-strategies.md`  (imported from `portfolio/src/data/deployment-strategies.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 12 | `[[gcp/deployment-strategies\|Deployment Strategies]]` | strong | # Application Zero-Downtime Deployment Strategies |

### `blogs/k8s-adventures.md`  (imported from `portfolio/src/data/k8s-adventures.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 37 | `[[gcp/gke\|GKE]]` | strong | In managed environments like AKS (Azure), GKE (Google), or EKS (AWS), I didn't really focus on the inner worki |
| 49 | `[[cloud/infrastructure-as-code\|Infrastructure as Code]]` | strong | I learned this saying, which is a design philosophy where you treat your systems that you build as **cattle**: |

### `blogs/certification-roadmap.md`  (imported from `portfolio/src/data/certification-roadmap.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 52 | `[[gcp/gke\|GKE]]` | strong | 4. **Certified Kubernetes Administrator (CKA)**: Just like Linux, Kubernetes is everywhere, especially in Saud |

## Certification notes (mostly AWS)

### `notes/certifications/4-solutions-architect-associate-saa-c03.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 64 | `[[aws/compute-ec2\|EC2]]` | strong | - EC2, EC2 Auto Scaling Groups, ECS |
| 434 | `[[aws/networking-vpc\|VPC]]` | strong | - **Private Hosted Zone**: Records that specify how to route traffic internally (on a VPC, for example) |
| 362 | `[[aws/storage-s3\|S3]]` | strong | - Restoring MySQL RDS database from S3 |
| 65 | `[[aws/management-and-governance-cloudwatch\|CloudWatch]]` | strong | - AWS Cert. Manager, CloudWatch |
| 333 | `[[cloud/serverless\|Serverless]]` | strong | ### Aurora Serverless |

46 more definitions appear on this page: `aws/autoscaling-groups-and-load-balancers`, `aws/security-iam`, `aws/containers-ecs`, `cloud/disaster-recovery`, `aws/application-integration-sqs`, `aws/application-integration-sns`, `aws/machine-learning-glue`, `aws/management-and-governance-cloudtrail`, `aws/storage-ebs`, `aws/networking-direct-connect`, `aws/analytics-kinesis`, `aws/networking-route53` and 34 more.

### `notes/certifications/6-solutions-architect-professional-sap-c02.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 17 | `[[aws/security-iam\|IAM]]` | strong | ## IAM Policies |
| 23 | `[[aws/storage-s3\|S3]]` | strong | - S3 Buckets |
| 25 | `[[aws/security-kms\|KMS]]` | strong | - KMS Keys |
| 27 | `[[aws/application-integration-sqs\|SQS]]` | strong | - SQS Queues |
| 33 | `[[aws/management-and-governance-cloudtrail\|CloudTrail]]` | strong | Fine-grained IAM policies based on access activity for the past 90 days. Reviews CloudTrail Logs for a service |

### `notes/certifications/7-certified-kubernetes-application-developer-ckad.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 69 | `[[aws/management-and-governance-cloudwatch\|CloudWatch]]` | strong | - Useful when an agent is needed, like AWS CloudWatch Agent. |
| 20 | `[[cloud/containers\|Containers]]` | loose | Containers that run before the main container and have to succeed for the main container to run. **The InitCon |
| 43 | `[[cloud/scalability\|Scalability]]` | loose | ### Deployment Scalability |

### `notes/certifications/10-professional-cloud-architect-pca.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 17 | `[[gcp/iam\|IAM]]` | strong | - AWS IAM Roles = GCP Service Accounts |
| 20 | `[[gcp/vpc\|VPCs]]` | strong | - VPCs are global! And subnets can live in multiple Zones! |
| 31 | `[[rest\|REST API]]` | strong | REST API -> HTTP |

## GCP notes

### `notes/gcp/readme.md`  (imported from `ObsidianVault/studies/cloud-architecht/gcp/README.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 114 | `[[gcp/vpc\|VPCs]]` | strong | - Creating VPCs, subnets, firewall rules |
| 76 | `[[gcp/cloud-storage\|Cloud Storage]]` | strong | - Cloud Storage - Storage classes |
| 83 | `[[gcp/bigquery\|BigQuery]]` | strong | - BigQuery - Data warehouse |
| 95 | `[[gcp/vertex-ai\|Vertex AI]]` | strong | - Vertex AI - Unified ML platform, AutoML |
| 69 | `[[gcp/gke\|GKE]]` | strong | - GKE - Autopilot vs Standard, node pools |

51 more definitions appear on this page: `gcp/cloud-run`, `gcp/cloud-sql`, `gcp/cloud-monitoring`, `gcp/compute-engine`, `gcp/persistent-disk`, `gcp/firestore`, `gcp/gemini`, `cloud/cost-optimization-pillar`, `gcp/cloud-functions`, `gcp/cloud-spanner`, `gcp/bigtable`, `gcp/deployment-strategies` and 39 more.

### `notes/gcp/2-network-security.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 28 | `[[gcp/vpc\|VPCs]]` | strong | 1. **Hierarchical firewall policies:** attach at org or folder level; inherited by child projects' VPCs; suppo |
| 38 | `[[gcp/iam\|IAM]]` | strong | **[[identity-aware-proxy/Identity-Aware Proxy]]:** PCSE wants config: enable IAP on a backend service or for T |
| 66 | `[[gcp/cloud-armor\|Cloud Armor]]` | strong | - Cloud Armor also supports serverless NEGs (App Engine, Cloud Run, Functions), Internet NEGs (hybrid/multiclo |
| 50 | `[[gcp/private-google-access-vs-psc\|private Google access]]` | strong | **[[cloud-dns/Cloud DNS]] security:** DNSSEC on public zones (signing states: on, transfer, off), DNS forwardi |
| 56 | `[[gcp/cloud-nat\|Cloud NAT]]` | strong | **Private vs public IP addressing:** know which products require external IPs (external HTTP(S) LB, Cloud NAT  |

16 more definitions appear on this page: `gcp/cloud-dns`, `gcp/vpc-service-controls`, `cloud/sla`, `gcp/cloud-ngfw`, `gcp/identity-aware-proxy`, `gcp/bigquery`, `gcp/cloud-logging`, `gcp/pub-sub`, `cloud/serverless`, `gcp/app-engine`, `gcp/cloud-run`, `gcp/compute-engine` and 4 more.

### `notes/gcp/3-data-protection.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 34 | `[[gcp/iam\|IAM]]` | strong | - **[[bigquery/BigQuery]]:** IAM at dataset/table level, **policy tags** + column-level security (Data Catalog |
| 107 | `[[gcp/vertex-ai\|Vertex AI]]` | strong | - Models: vulnerability scanning and signed images in [[artifact-registry/Artifact Registry]], [[binary-author |
| 51 | `[[gcp/vpc-service-controls\|VPC-SC]]` | strong | - Secret Manager: versions are immutable (rotation = new version); user-managed replication via `--locations`; |
| 63 | `[[gcp/vpc\|VPC]]` | strong | / Cloud EKM / You (external key manager: Fortanix, Thales, etc.) / Keys must live outside Google; via VPC endp |
| 118 | `[[gcp/gemini\|Gemini]]` | strong | **3. Security controls for Gemini Enterprise Agent Platform:** |

15 more definitions appear on this page: `gcp/bigquery`, `gcp/secret-manager`, `gcp/cloud-kms`, `gcp/gke`, `gcp/cloud-storage`, `gcp/security-command-center`, `gcp/compute-engine`, `gcp/dataflow`, `gcp/dataproc`, `cloud/principle-of-least-privilege`, `gcp/private-google-access-vs-psc`, `cloud/logging` and 3 more.

### `notes/gcp/4-managing-operations.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 58 | `[[gcp/pub-sub\|Pub/Sub]]` | strong | **Incident response flow:** detect (Event Threat Detection, audit logs, SCC findings), notify (SCC notificatio |
| 30 | `[[gcp/security-command-center\|SCC]]` | strong | - **VM patch management:** **VM Manager** (OS Config agent): patch jobs (one-off) and patch policies (recurrin |
| 56 | `[[gcp/bigquery\|BigQuery]]` | strong | / Log Analytics / SQL queries over log buckets / Enable on a log bucket; query in Cloud Logging UI (BigQuery e |
| 43 | `[[gcp/iam\|IAM]]` | strong | - Artifact Registry: regional repositories per project, repo-level IAM, put repositories inside a VPC-SC perim |
| 56 | `[[gcp/cloud-logging\|Cloud Logging]]` | strong | / Log Analytics / SQL queries over log buckets / Enable on a log bucket; query in Cloud Logging UI (BigQuery e |

12 more definitions appear on this page: `gcp/binary-authorization`, `gcp/cloud-storage`, `gcp/vpc`, `gcp/cloud-build`, `gcp/gke`, `gcp/artifact-registry`, `gcp/cloud-functions`, `gcp/cloud-kms`, `gcp/vpc-service-controls`, `gcp/dataflow`, `cloud/logging`, `cloud/region`.

### `notes/gcp/pcse-home.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 59 | `[[gcp/cloud-storage\|Cloud Storage]]` | strong | / 1. Configuring access / Cloud Identity and Admin console; users, groups, 2-Step Verification; GCDS and SAML  |
| 59 | `[[gcp/iam\|IAM]]` | strong | / 1. Configuring access / Cloud Identity and Admin console; users, groups, 2-Step Verification; GCDS and SAML  |
| 60 | `[[gcp/vpc\|VPC]]` | strong | / 2. Network security / VPCs, subnets, firewalls, IP addressing; Shared VPC and peering; Interconnect options; |
| 60 | `[[gcp/cloud-armor\|Cloud Armor]]` | strong | / 2. Network security / VPCs, subnets, firewalls, IP addressing; Shared VPC and peering; Interconnect options; |
| 60 | `[[gcp/identity-aware-proxy\|IAP]]` | strong | / 2. Network security / VPCs, subnets, firewalls, IP addressing; Shared VPC and peering; Interconnect options; |

15 more definitions appear on this page: `gcp/private-google-access-vs-psc`, `gcp/secret-manager`, `gcp/binary-authorization`, `gcp/security-command-center`, `gcp/cloud-dns`, `gcp/cloud-nat`, `gcp/cloud-ngfw`, `gcp/vpc-service-controls`, `gcp/bigquery`, `gcp/cloud-sql`, `gcp/cloud-logging`, `gcp/gemini` and 3 more.

### `notes/gcp/1-configuring-access.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 46 | `[[gcp/iam\|IAM]]` | strong | - Super Admin (Cloud Identity/Workspace) and Organization Administrator (IAM) are deliberately separate roles: |
| 54 | `[[gcp/gke\|GKE]]` | strong | / Workload on [[gke/GKE]] needs Google API access / Workload Identity Federation for GKE (Kubernetes SA bindin |
| 129 | `[[gcp/vpc-service-controls\|VPC-SC]]` | strong | - ACM's access policy is the org-scoped container; ACM only describes rules, enforcement happens in VPC-SC, IA |
| 61 | `[[gcp/app-engine\|App Engine]]` | strong | - **Default service accounts** (Compute Engine default SA, App Engine default SA): have Editor on the project. |
| 61 | `[[gcp/compute-engine\|Compute Engine]]` | strong | - **Default service accounts** (Compute Engine default SA, App Engine default SA): have Editor on the project. |

5 more definitions appear on this page: `gcp/security-command-center`, `gcp/secret-manager`, `cloud/principle-of-least-privilege`, `gcp/identity-aware-proxy`, `cloud/region`.

### `notes/gcp/cheat-sheets.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 42 | `[[gcp/vpc\|VPC]]` | strong | 5. VPC-to-VPC within org with central control -> Shared VPC. |
| 60 | `[[gcp/security-command-center\|SCC]]` | strong | 7. Malware or ransomware running on VMs -> VM Threat Detection (SCC). See [[attack-detection/Attack detection] |
| 23 | `[[gcp/gke\|GKE]]` | strong | 1. [[gke/GKE]] workload -> Workload Identity Federation for GKE. |
| 47 | `[[gcp/iam\|IAM]]` | strong | 1. IAM wrong principal -> org policy domain-restricted sharing. |
| 66 | `[[gcp/vpc-service-controls\|VPC Service Controls]]` | strong | 4. Data exfiltration from AI data projects -> VPC Service Controls. |

1 more definitions appear on this page: `cloud/containers`.

### `notes/gcp/final-week-checklist.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 28 | `[[gcp/vpc-service-controls\|VPC-SC]]` | strong | - [ ] Can configure VPC-SC in dry run, write an ingress and egress rule, and explain bridges. |
| 26 | `[[gcp/iam\|IAM]]` | strong | - [ ] Can trace an access decision through allow binding, deny policy, IAM condition, and [[vpc-service-contro |
| 29 | `[[gcp/private-google-access-vs-psc\|private Google access]]` | strong | - [ ] Know the PGA/restricted VIP/PSC/[[cloud-nat/NAT]] matrix and the DNS zone pattern for private Google acc |
| 33 | `[[gcp/security-command-center\|SCC]]` | strong | - [ ] Know SCC tiers, the built-in detectors, and continuous export targets. See [[security-command-center/Sec |
| 37 | `[[gcp/gemini\|Gemini]]` | strong | - [ ] Can name the three AI layers (data, model, interaction) and the control for each, the IaaS vs PaaS train |

2 more definitions appear on this page: `gcp/vertex-ai`, `gcp/cloud-vpn`.

### `notes/gcp/5-compliance.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 22 | `[[gcp/iam\|IAM]]` | strong | - **Shared responsibility model (in depth):** map a control question ("who patches the OS on [[compute-engine/ |
| 32 | `[[gcp/vpc\|VPC]]` | strong | - Segmentation -> [[vpc-service-controls/VPC-SC]], Shared VPC, NGFW policies, ACM. |
| 41 | `[[gcp/pub-sub\|Pub/Sub]]` | strong | - Access Approval: requests arrive by email or Pub/Sub; approve via console or API; requests are signed, Googl |
| 23 | `[[cloud/region\|regions]]` | loose | - **Assured Workloads:** creates a folder with enforced compliance regime (FedRAMP Moderate/High, IL2/4/5, CJI |

### `notes/gcp/certificate-topics.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 19 | `[[cloud/cloud-computing\|Cloud Computing]]` | strong | ## Pillars of Cloud Computing |

### `notes/gcp/skills-needed.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 18 | `[[cloud/containers\|Containerization]]` | strong | Containerization |

## Other notes

### `notes/react/react.md`  (imported from `ObsidianVault/webdev/react/react.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 300 | `[[react/main-context-concepts\|Context API]]` | strong | ## Redux vs Context API |
| 60 | `[[react/usereducer\|useReducer]]` | strong | - First, know [useReducer()](#usereducer) |
| 737 | `[[react/suspense\|Suspense]]` | strong | ## Suspense |
| 343 | `[[react/prop-drilling\|prop drilling]]` | strong | / When you need to solve a simple prop drilling problem                                              / When yo |
| 796 | `[[cloud/serverless\|serverless]]` | strong | When deployed to vercel: each dynamic route becomes a serverless function. |

4 more definitions appear on this page: `web/component`, `web/hook`, `web/props`, `react/provider`.

### `notes/interviews/study-guide-for-technical-interview.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 99 | `[[security/cryptography\|Cryptography]]` | strong | ## **Cryptography & Data Security** |
| 117 | `[[networking/osi-model\|OSI Model]]` | strong | - OSI Model and TCP/IP Stack |
| 66 | `[[web/memoization\|Memoization]]` | strong | - Dynamic programming (Memoization, Tabulation) |
| 72 | `[[cloud/infrastructure-as-code\|Infrastructure as Code]]` | strong | - Infrastructure as Code (Terraform, Ansible) |
| 125 | `[[cloud/multi-factor-authentication\|MFA]]` | strong | - Authentication mechanisms (MFA, OAuth, SAML) |

1 more definitions appear on this page: `cloud/logging`.

### `notes/devops/week3-day4.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 26 | `[[cloud/principle-of-least-privilege\|POLP]]` | strong | - Hardened containers: multi-stage builds, non root user, POLP |
| 17 | `[[cloud/scalability\|scalability]]` | loose | - Stress test to show scalability |
| 26 | `[[cloud/containers\|containers]]` | loose | - Hardened containers: multi-stage builds, non root user, POLP |

### `notes/react/react-router-forms.md`  (imported from `ObsidianVault/webdev/react/react-router/forms.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 43 | `[[web/hook\|hook]]` | loose | - Use `redirect()` instead of [[react-router-usenavigate/useNavigate]] when not in a hook or component. |
| 43 | `[[web/component\|component]]` | loose | - Use `redirect()` instead of [[react-router-usenavigate/useNavigate]] when not in a hook or component. |

### `notes/devops/week6-project.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 35 | `[[rest\|REST API]]` | strong | - **Backend:** Maven-Java REST API. |
| 17 | `[[cloud/scalability\|scalability]]` | loose | You’re the core tech team at a company that migrated a legacy app from a single on-prem VM to Azure because th |

### `notes/react/react-router-loaders.md`  (imported from `ObsidianVault/webdev/react/react-router/loaders.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 16 | `[[web/component\|component]]` | loose | - Loaders load data before component renders |

### `notes/interviews/interview-prep.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 137 | `[[networking/osi-model\|OSI layers]]` | strong | OSI layers: |
| 198 | `[[cloud/scalability\|scalability]]` | loose | > Some advantages of using OOPs in Java include code reusability, modularity, flexibility, scalability, and ea |

### `notes/devops/week1-day1.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 24 | `[[cloud/infrastructure-as-code\|Infrastructure as Code]]` | strong | ### IaC - Infrastructure as Code |

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

### `notes/security/attack-prevention-strategies.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 24 | `[[cloud/principle-of-least-privilege\|least privilege]]` | strong | ### Follow the principle of least privilege |

## Project pages

### `projects/body-power-gym.md`  (imported from `portfolio/src/data/body-power-gym.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 45 | `[[aws/containers-ecs\|ECS]]` | strong | - **AWS Services**: VPC, ECS Fargate, ALB, ECR, CodeBuild, EventBridge, CloudWatch, Lambda, Certificate Manage |
| 46 | `[[cloud/containers\|Containerization]]` | strong | - **Containerization**: Docker, multi-stage builds, container orchestration, image optimization |
| 45 | `[[aws/application-integration-eventbridge\|EventBridge]]` | strong | - **AWS Services**: VPC, ECS Fargate, ALB, ECR, CodeBuild, EventBridge, CloudWatch, Lambda, Certificate Manage |
| 45 | `[[aws/containers-ecr\|ECR]]` | strong | - **AWS Services**: VPC, ECS Fargate, ALB, ECR, CodeBuild, EventBridge, CloudWatch, Lambda, Certificate Manage |
| 45 | `[[aws/management-and-governance-cloudwatch\|CloudWatch]]` | strong | - **AWS Services**: VPC, ECS Fargate, ALB, ECR, CodeBuild, EventBridge, CloudWatch, Lambda, Certificate Manage |

9 more definitions appear on this page: `aws/compute-fargate`, `cloud/infrastructure-as-code`, `aws/management-and-governance-auto-scaling`, `aws/management-and-governance-cloudformation`, `cloud/logging`, `aws/storage-s3`, `aws/networking-api-gateway`, `aws/compute-lambda`, `cloud/scalability`.

### `projects/image-captioning.md`  (imported from `portfolio/src/data/image-captioning.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 66 | `[[aws/networking-api-gateway\|API Gateway]]` | strong | To handle uploads, I setup an API Gateway with a `/upload` **POST** route. This is what triggers the first Lam |
| 19 | `[[cloud/serverless\|serverless]]` | strong | A serverless image captioning app using AWS services and a HuggingFace model on SageMaker. |
| 19 | `[[aws/machine-learning-sagemaker\|SageMaker]]` | strong | A serverless image captioning app using AWS services and a HuggingFace model on SageMaker. |
| 29 | `[[aws/security-cognito\|Cognito]]` | strong | Serverless Alt-Text Generation for better accessibility on the web using AI, built mostly on Amazon Web Servic |
| 55 | `[[aws/storage-s3\|S3]]` | strong | Once that was done, I setup two S3 buckets: `textify-website` for hosting the website files, and `textify-img` |

4 more definitions appear on this page: `aws/networking-cloudfront`, `aws/application-integration-step-functions`, `aws/compute-lambda`, `aws/free-services`.

### `projects/catus-locatus.md`  (imported from `portfolio/src/data/catus-locatus.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 60 | `[[cloud/containers\|Containerization]]` | strong | ### Containerization |
| 85 | `[[aws/networking-route53\|Route 53]]` | strong | Our main Infrastructure-as-Code tool. Since the domain we were using (this same one you're on!) is on AWS Rout |
| 121 | `[[cloud/principle-of-least-privilege\|Least Privilege]]` | strong | Again, nothing too fancy. We'll use the domain's Hosted Zone, and to manage the DNS records on it I created an |
| 32 | `[[cloud/cloud-computing\|Cloud Computing]]` | strong | I was sponsored by [Saudi Digital Academy (SDA)](https://sda.edu.sa/) to attend a 3-month [DevOps & Cloud Comp |
| 58 | `[[aws/free-services\|free tier]]` | loose | I began on creating a backend, because in my original project I was using `supabase`, which is a platform that |

### `projects/e2e-automated-deployment-azure.md`  (imported from `portfolio/src/data/e2e-automated-deployment-azure.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 59 | `[[cloud/containers\|containers]]` | strong | For the application, we'll host it as a containerized Azure Web App. It provides a simple platform to deploy a |
| 105 | `[[cloud/infrastructure-as-code\|Infrastructure as Code]]` | strong | ### Infrastructure as Code - Terraform Modules |
| 130 | `[[cloud/scalability\|Scalability]]` | loose | - **Scalability**: Easy to add new resources without affecting existing ones |
| 182 | `[[cloud/region\|regions]]` | loose | - Reproducible environments across regions or subscriptions |
| 197 | `[[cloud/logging\|logging]]` | loose | **Application Gateway 403 Errors**: After provisioning the Application Gateway, we encountered persistent 403  |

### `projects/aws-budget-discord-notifs.md`  (imported from `portfolio/src/data/aws-budget-discord-notifs.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 43 | `[[aws/application-integration-sns\|SNS]]` | strong | - `AWS_ACCESS_KEY`: AWS Access Key with access to Lambda, SNS, Budgets, and IAM. See: [https://docs.aws.amazon |
| 43 | `[[aws/security-iam\|IAM]]` | strong | - `AWS_ACCESS_KEY`: AWS Access Key with access to Lambda, SNS, Budgets, and IAM. See: [https://docs.aws.amazon |
| 43 | `[[aws/compute-lambda\|Lambda]]` | loose | - `AWS_ACCESS_KEY`: AWS Access Key with access to Lambda, SNS, Budgets, and IAM. See: [https://docs.aws.amazon |
| 49 | `[[cloud/region\|region]]` | loose | - `AWS_REGION`: Primary region to deploy to |

### `projects/azure-3t-app.md`  (imported from `portfolio/src/data/azure-3t-app.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 28 | `[[cloud/cloud-computing\|Cloud Computing]]` | strong | The frontend and backend code was provided by Mr. Saurabh Dhingra ([github/saurabhd2106](https://github.com/sa |
| 62 | `[[cloud/principle-of-least-privilege\|least privilege]]` | strong | - Principle of least privilege is applied to Network Security Groups, offering a high level of security. |
| 18 | `[[cloud/containers\|containers]]` | loose | Azure Three-Tier web app deployed using Terraform and containers |

### `projects/tuwaiq-tracker.md`  (imported from `portfolio/src/data/tuwaiq-tracker.md`)

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 106 | `[[web/component\|components]]` | loose | The final product did adapt the main components, so I was happy with the design overall. Next, I started build |

### `projects/openziti-operator/operations.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 3 | `[[cloud/high-availability\|High availability]]` | strong | ## High availability |
| 13 | `[[status-code\|HTTP status]]` | strong | / `ziti_operator_api_requests_total{method,kind,code}` / Calls to the Ziti API. `code` is the HTTP status, or  |

### `projects/grooszy/API.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 588 | `[[cloud/tagging\|tagging]]` | loose | normalized merchant name, plus manual merchant tagging. Per month: outflow total, |

## Course and site pages

### `four-hats/episodes/ep07-plan-the-infrastructure.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 11 | `[[gcp/vpc\|VPC]]` | strong | / Done when / The plan names the service model, region, zone, VM size, VPC and subnet, open ports, and monthly |
| 19 | `[[cloud/cidr\|CIDR]]` | strong | - Read CIDR notation and plan one VPC with one subnet. |
| 55 | `[[gcp/compute-engine\|Compute Engine]]` | strong | / IaaS / Operating system, runtime, app / Hardware, network / A Compute Engine VM. This act. / |
| 76 | `[[cloud/principle-of-least-privilege\|least privilege]]` | strong | ## Ports and least privilege |
| 11 | `[[cloud/region\|region]]` | loose | / Done when / The plan names the service model, region, zone, VM size, VPC and subnet, open ports, and monthly |

1 more definitions appear on this page: `cloud/containers`.

### `four-hats/episodes/ep10-now-in-the-cloud.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 10 | `[[gcp/compute-engine\|Compute Engine]]` | strong | / You build / A network, firewall rules, and a Compute Engine VM on Google Cloud with Terraform, then the task |
| 53 | `[[cloud/infrastructure-as-code\|Infrastructure as code]]` | strong | Infrastructure as code means desired state in files. Tools reconcile reality with what you wrote. |
| 75 | `[[cloud/cidr\|CIDR]]` | strong | - `variables.tf`: project ID, region, zone, machine type, SSH public key, and your IP in CIDR form. |
| 142 | `[[gcp/cloud-load-balancing\|Cloud Load Balancing]]` | strong | / Load balancer / Sits in front of many servers. It spreads traffic across them, so no server is overwhelmed.  |
| 40 | `[[cloud/containers\|containers]]` | loose | Terraform and the `gcloud` command run in containers. Sign in and enable the Compute Engine API: |

1 more definitions appear on this page: `cloud/region`.

### `four-hats/episodes/ep05-containers.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 98 | `[[cloud/principle-of-least-privilege\|least privilege]]` | strong | This is least privilege at the process level. It does not replace a network policy or a read-only filesystem,  |
| 1 | `[[cloud/containers\|Containers]]` | loose | # SWE-05: Containers |

### `four-hats/episodes/ep03-run-the-app.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 10 | `[[cloud/containers\|containers]]` | loose | / You build / Three containers on one Docker network, with the app reachable at `http://localhost:8080` / |

### `four-hats/episodes/ep19-alerting.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 5 | `[[gcp/gke\|GKE]]` | strong | Dashboards need someone to look at them. Alerts come to you. This episode makes the app send a message to Disc |
| 157 | `[[gcp/persistent-disk\|Persistent Disk]]` | strong | Delete the cluster right after the demo, not at the end of the session. The cluster can leave Persistent Disk  |

### `four-hats/cleanup-guide.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 35 | `[[gcp/gke\|GKE]]` | strong | 5. Delete the GKE demo cluster: |
| 9 | `[[cloud/containers\|containers]]` | loose | 1. Stop both Compose projects. Delete their containers, networks, volumes, and images: |

### `four-hats/episodes/ep04-add-a-feature-with-a-test.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 19 | `[[status-code\|status codes]]` | strong | - Explain HTTP status codes and REST semantics: methods name the action, resources name the thing. |

### `four-hats/episodes/ep11-hello-kubernetes.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 37 | `[[cloud/containers\|containers]]` | loose | A cluster is a set of machines that run containers. The control plane decides, and the nodes run the Pods. A P |

### `four-hats/costs-and-free-options.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 17 | `[[gcp/gke\|GKE]]` | strong | Episode 10 repeats the Act 2 VM work on Google Cloud. Episode 19 closes with a demo of the same Kubernetes man |
| 9 | `[[cloud/containers\|Containers]]` | loose | / Docker Desktop / Containers / Free for personal use and education / |
| 23 | `[[cloud/region\|regions]]` | loose | - Google Cloud also has an Always Free tier. It includes one `e2-micro` VM in some US regions. |

### `four-hats/episodes/ep23-scan-and-verify.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 33 | `[[cloud/infrastructure-as-code\|IaC]]` | strong | / SCA, IaC, and secrets, Trivy / Container images, Dockerfiles, Kubernetes YAML, Terraform, and credentials co |

### `four-hats/episodes/ep26-build-your-cv.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 47 | `[[cloud/infrastructure-as-code\|Infrastructure as Code]]` | strong | - Infrastructure as Code |
| 46 | `[[cloud/containers\|Containers]]` | loose | - Containers & Orchestration |

### `four-hats/episodes/ep00-four-careers-one-project.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 47 | `[[rest\|REST API]]` | strong | / Backend / Python Flask REST API / Validate requests, run SQL, return JSON / |
| 82 | `[[cloud/cidr\|CIDR]]` | strong | You plan the machine: CPU, memory, storage, firewall, CIDR, DNS, and cost. Then you build the same machine twi |
| 115 | `[[cloud/containers\|Containers]]` | loose | / Docker Desktop and Minikube / Containers and a local Kubernetes cluster / Free / |

### `four-hats/episodes/ep01-set-up-your-laptop.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 36 | `[[cloud/containers\|containers]]` | loose | / Docker Desktop / Runs containers for the app, the database, and the course tools. / All / |

### `four-hats/episodes/ep06-continuous-integration.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 18 | `[[cloud/principle-of-least-privilege\|least privilege]]` | strong | - Apply least privilege with `contents: read`. |

### `four-hats/episodes/ep12-services-and-troubleshooting.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 59 | `[[gcp/cloud-load-balancing\|cloud load balancing]]` | strong | A Service of type LoadBalancer needs a cloud. Minikube uses NodePort plus `minikube service` for local access. |
| 83 | `[[cloud/containers\|Containers]]` | loose | / Kubernetes (Pods, Deployments, Services) / 11, 12 / Containers & Orchestration / Deployed a three-tier app t |

### `four-hats/episodes/ep14-state.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 76 | `[[cloud/containers\|containers]]` | loose | The StatefulSet in this act runs two containers in one Pod: `postgres` and `postgres-exporter`. That is why th |

### `four-hats/episodes/ep20-think-like-an-attacker.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 17 | `[[status-code\|status code]]` | strong | - Read an API by hand with `curl` and name each endpoint, parameter, and status code. |

### `four-hats/episodes/ep13-configuration.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 28 | `[[cloud/containers\|containers]]` | loose | Wiring decides how a setting reaches a container. `envFrom` loads every key from a ConfigMap as an environment |

### `four-hats/episodes/ep15-scale.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 130 | `[[cloud/containers\|Containers]]` | loose | / Autoscaling (HPA), resource management / 15 / Containers and Orchestration / Set requests, limits, and probe |

### `four-hats/episodes/ep21-exploit-the-sql-injection.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 47 | `[[status-code\|status code]]` | strong | A normal search always returns `200`. It returns an empty list when no title matches. It returns your own task |

### `four-hats/episodes/ep22-fix-and-harden.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 54 | `[[cloud/principle-of-least-privilege\|least privilege]]` | strong | Default-deny first, then add only the paths the app needs. One policy blocks all ingress and all egress in `ap |

### `four-hats/setup.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 9 | `[[cloud/containers\|containers]]` | loose | / Docker Desktop / Runs containers and the course tools / |

### `four-hats/episodes/ep02-git-and-github.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 160 | `[[cloud/containers\|containers]]` | loose | Episode 3 runs the app. You start the database, the backend, and the frontend in three containers on one priva |

### `four-hats/episodes/ep08-your-first-vm.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 44 | `[[cloud/containers\|containers]]` | loose | Both are useful. This act uses a VM because the course needs a real server with its own SSH service, users, an |

### `four-hats/episodes/ep09-configuration-as-code.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 156 | `[[gcp/vpc\|VPC]]` | strong | / Firewalls (UFW, VPC rules) / 9, 10 / Cloud and Infrastructure / Closed all ports except SSH and HTTP with UF |

### `four-hats/episodes/ep24-broken-access-control.md`

| Line | Link | Fit | Anchor in text |
|---|---|---|---|
| 67 | `[[status-code\|status code]]` | strong | Add the test imports, a token helper that signs a token for a user ID, and an auth header helper. Then add a t |

## Orphan definitions

Zero inbound wikilinks: 142 of 222.

### Orphans that already appear in a post

- `aws/analytics-athena` `aws/analytics-kinesis` `aws/analytics-redshift` `aws/application-integration-eventbridge` `aws/application-integration-sns` `aws/application-integration-sqs`
- `aws/application-integration-step-functions` `aws/compute-beanstalk` `aws/compute-fargate` `aws/containers-ecr` `aws/containers-eks` `aws/ec2-user-data`
- `aws/financial-management-budgets` `aws/free-services` `aws/machine-learning-glue` `aws/management-and-governance-auto-scaling` `aws/management-and-governance-cloudformation` `aws/management-and-governance-cloudtrail`
- `aws/management-and-governance-cloudwatch` `aws/management-and-governance-config` `aws/management-and-governance-systems-manager` `aws/networking-api-gateway` `aws/networking-direct-connect` `aws/networking-vpn`
- `aws/security-cognito` `aws/security-guardduty` `aws/security-kms` `aws/storage-ebs` `cloud/cloud-computing` `cloud/containers`
- `cloud/generative-ai` `cloud/governance-and-compliance` `cloud/infrastructure-as-code` `cloud/migration-strategies` `cloud/scalability` `cloud/tagging`
- `gcp/alloydb` `gcp/app-engine` `gcp/bigtable` `gcp/cloud-composer` `gcp/cloud-functions` `gcp/cloud-profiler`
- `gcp/cloud-spanner` `gcp/cloud-trace` `gcp/dataflow` `gcp/dataproc` `gcp/deployment-strategies` `gcp/error-reporting`
- `gcp/filestore` `gcp/firestore` `gcp/iam` `gcp/memorystore` `gcp/persistent-disk` `networking/osi-model`
- `react/main-context-concepts` `react/prop-drilling` `react/provider` `react/suspense` `status-code` `web/props`

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

78 of the 95 AWS pages are orphans. The fastest win is one link per service from
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

