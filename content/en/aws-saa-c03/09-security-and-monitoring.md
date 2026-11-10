# 9. Security and Monitoring

**Goal:** Protect workloads, manage keys and secrets, and track activity.

## Encryption and secrets

### AWS KMS

[[security-kms|KMS]] manages encryption keys. You can audit key use in CloudTrail.

- Symmetric (AES-256): one key encrypts and decrypts.
- Asymmetric (RSA): a public key encrypts, and a private key decrypts.
- Key policies control access to keys.
- Multi-Region keys share one key ID across Regions. You can encrypt in one Region and decrypt in another. The note says they are usually not recommended. Use cases: global client-side encryption, global DynamoDB, and global Aurora.
- To move encrypted data to another Region, copy a snapshot to that Region.

### Systems Manager Parameter Store

[[management-and-governance-systems-manager|Systems Manager]] Parameter Store stores configuration and secrets. It tracks versions and integrates with CloudFormation.

### Secrets Manager

- Stores secrets.
- Forces rotation on a schedule (every X days).
- A custom [[compute-lambda|Lambda]] function can generate new secrets during rotation.
- Integrates with RDS.
- Encrypts secrets with KMS.
- Multi-Region secrets replicate to other Regions for availability and [[disaster-recovery|disaster recovery]].

### AWS Certificate Manager (ACM)

- Provisions and deploys TLS certificates for in-flight encryption.
- Works with CLB, ALB, NLB, [[networking-cloudfront|CloudFront]], and APIs.
- You cannot use ACM certificates with EC2.

### Cognito

[[security-cognito|Cognito]] gives users an identity for your app.

- User pools provide sign-in, MFA, and federation with providers such as Google and Facebook. They integrate with [[networking-api-gateway|API Gateway]] and ALB.
- Identity pools give users AWS credentials to reach AWS resources directly. They can use a user pool as the identity provider.

## Threat protection

### AWS WAF

[[security-waf|WAF]] is a Layer 7 (HTTP) firewall. Deploy it on ALB, API Gateway, CloudFront, AppSync, or Cognito user pools.

### AWS Shield

[[security-shield|Shield]] protects against DDoS attacks at Layers 3 and 4.

- Shield Standard is free. It protects against SYN floods and similar Layer 3 and 4 attacks.
- Shield Advanced provides DDoS mitigation for sophisticated attacks. It costs $3k per month. It protects against higher fees during an attack.
- Shield Advanced deploys WAF rules to mitigate Layer 7 attacks.

### Firewall Manager

[[management-and-governance-organizations|Organizations]] accounts can share one security policy through Firewall Manager.

- A policy covers WAF, Shield Advanced, security groups, Network Firewall, and the [[networking-route53|Route 53]] Resolver DNS firewall.
- Policies are Region-based.
- Rules apply to new resources in all accounts, including future accounts.

### AWS Network Firewall

Network Firewall protects an entire [[networking-vpc|VPC]]. It filters Layer 3 to Layer 7 traffic.

- Inspects VPC-to-VPC traffic, inbound and outbound internet traffic, and traffic from [[networking-direct-connect|Direct Connect]] and VPN.
- Uses a Gateway Load Balancer internally.
- Supports thousands of rules. Filters by IP and port, protocol, stateful domain list, and regex.
- Actions: allow, drop, or alert. Supports active flow inspection.
- Sends logs to [[storage-s3|S3]], CloudWatch, or Data Firehose.

### GuardDuty

[[security-guardduty|GuardDuty]] detects threats with machine learning and anomaly detection. It reads CloudTrail logs, VPC Flow Logs, and DNS logs. It integrates with EventBridge. It detects cryptocurrency attacks.

### Inspector

[[security-inspector|Inspector]] runs automated security assessments.

- EC2: uses the SSM agent. Checks network reachability and scans the OS for known vulnerabilities.
- Container images in [[containers-ecr|ECR]]: assesses images when they are pushed.
- Lambda functions: finds vulnerabilities in function code and dependencies.
- Reports to Security Hub. Sends findings to [[application-integration-eventbridge|EventBridge]].

### Macie

Macie protects data in S3 buckets. It alerts on sensitive data, such as PII, and notifies you through EventBridge.

## Monitoring and audit

| Service | Purpose |
|---|---|
| [[management-and-governance-cloudwatch|CloudWatch]] | Metrics, alarms, and logs for AWS services |
| [[management-and-governance-cloudtrail|CloudTrail]] | Records API calls and events for governance, compliance, and audit |
| [[management-and-governance-config|AWS Config]] | Records resource configuration and evaluates it against rules |

### CloudWatch

- Provides metrics for every AWS service. Metrics belong to namespaces.
- A dimension is an attribute of a metric, such as an instance ID. A metric has up to 30 dimensions.
- You can create custom metrics.
- Alarms can target EC2, [[management-and-governance-auto-scaling|Auto Scaling]], and SNS.
- Composite alarms combine several alarms.
- Metric streams send near real-time metrics to Data Firehose or third-party providers.
- Insights features: Container Insights, Lambda Insights, Contributor Insights (top contributors), and Application Insights.

### CloudTrail

- Enabled by default. Records API calls and operations.
- Event history covers 90 days. Move older logs to S3, then query them with [[analytics-athena|Athena]].
- Management events record operations on resources. You can separate read and write events.
- Data events are not logged by default.
- CloudTrail Insights builds a baseline of normal activity and flags unusual activity.
- If a resource is deleted, check CloudTrail.

### AWS Config

- Records resource configuration.
- Config rules are AWS-managed or custom. Custom rules run in Lambda. Example: check that each [[storage-ebs|EBS]] volume is type `gp2`.

## Exam tips

- Shield Standard is free. Shield Advanced suits sophisticated attacks.
- WAF works at Layer 7. Shield works at Layers 3 and 4.
- To investigate a deleted resource, check CloudTrail.
- CloudTrail keeps 90 days of history. Store logs in S3 for longer.
- Data events are not logged by default.
- ACM certificates do not work with EC2.
- Multi-Region KMS keys are usually not recommended.
- Secrets Manager rotates secrets. Parameter Store stores configuration.

[Next: Resilience and Disaster Recovery](10-resilience-and-dr.md)
