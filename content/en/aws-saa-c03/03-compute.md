# 3. Compute: Load Balancing, Scaling, Containers

**Goal:** Choose a compute option, distribute traffic to it, and scale it.

## Elastic Load Balancing

[[autoscaling-groups-and-load-balancers|Elastic Load Balancing]] (ELB) is a managed load balancer. AWS keeps it running. It integrates with EC2, Auto Scaling groups, ECS, Certificate Manager, [[management-and-governance-cloudwatch|CloudWatch]], Route 53, WAF, and Global Accelerator.

ELB runs health checks. It sends traffic only to healthy targets.

### Load balancer types

| Type | Version | Protocols | Notes |
|---|---|---|---|
| Classic (CLB) | v1, 2009 | HTTP, HTTPS, TCP, SSL | Supports one SSL certificate |
| Application (ALB) | v2, 2016 | HTTP/2, HTTPS, WebSocket | Layer 7. Routes by path, hostname, query string, or headers |
| Network (NLB) | v2, 2017 | TCP, TLS, UDP | Layer 4. Ultra-low latency. One static IP per AZ. Supports Elastic IP |
| Gateway (GLB) | - | IP protocol (GENEVE, port 6081) | Layer 3. Deploys third-party network virtual appliances |

- ALB suits microservices and containers. Its port mapping sends traffic to dynamic ports in ECS. With CLB, you need one load balancer per application.
- GLB sends all traffic through a firewall or inspection appliance. It combines a transparent gateway and a load balancer.

### Target groups

ALB and NLB send traffic to target groups:

| Target type | Notes |
|---|---|
| EC2 instances | - |
| ECS tasks | - |
| Lambda functions | The request becomes a JSON event. |
| IP addresses | They must be private. |

- Health checks for ALB run at the target group level.
- NLB health checks support HTTP, HTTPS, and TCP.

### Client IP and headers

The application servers behind an ALB do not see the client IP directly. ALB adds these headers:

- `X-Forwarded-For`: the client IP
- `X-Forwarded-Port`
- `X-Forwarded-Proto`

### Security groups for load balancers

- The load balancer security group allows HTTP (80) and HTTPS (443) from `0.0.0.0/0`.
- The EC2 security group allows HTTP on port 80 only from the load balancer security group.

### Sticky sessions

- Sticky sessions send a client to the same instance with a cookie. They work with CLB, ALB, and NLB.
- You set the cookie expiry.
- Stickiness can cause an uneven load across instances.

| Cookie type | Created by | Cookie name |
|---|---|---|
| Application-based, custom | Target | Your name. Unique per target group. Do not use AWSALB, AWSALBAPP, or AWSALBTG. |
| Application-based, application cookie | Load balancer | AWSALBAPP |
| Duration-based | Load balancer | AWSALB (ALB) or AWSELB (CLB) |

To enable stickiness:

1. Open the target group.
2. Select Actions.
3. Select Edit attributes.
4. Go to Target selection configuration.

### Cross-zone load balancing

| Load balancer | Cross-zone default | Inter-AZ data charge |
|---|---|---|
| ALB | Enabled. You can disable it per target group. | No charge |
| NLB | Disabled | Charged if you enable it |
| GLB | Disabled | Charged if you enable it |
| CLB | - | No charge |

### Server Name Indication (SNI)

SNI lets one server host several TLS certificates for several sites. It works with ALB, NLB, and [[networking-cloudfront|CloudFront]]. CLB supports only one SSL certificate.

### Connection draining

- Connection draining (CLB) and deregistration delay (ALB and NLB) both allow in-flight requests to finish.
- New requests stop going to an instance that is deregistering or unhealthy.
- Range: 1 to 3600 seconds. Default: 300. Set 0 to disable.

## Auto Scaling groups

An [[management-and-governance-auto-scaling|Auto Scaling group]] (ASG) adds or removes EC2 instances. Set three values:

1. Minimum capacity
2. Desired capacity
3. Maximum capacity

A launch template defines each instance. It holds the AMI, instance type, EC2 user data, [[storage-ebs|EBS]] volumes, security groups, load balancer details, and network details.

### Scaling policies

| Policy | How it works |
|---|---|
| Target tracking | Keeps a metric near a target. Example: average CPU at 40%. |
| Simple or step | A CloudWatch alarm adds or removes units. Example: CPU above 70% adds 2 instances. |
| Scheduled | Scales at known times. Example: minimum capacity 10 at 5 PM on Fridays. |
| Predictive | Forecasts load with machine learning and schedules scaling ahead. Good for repeating patterns. |

### Metrics and cooldown

- Good metrics to scale on: `CPUUtilization`, `RequestCountPerTarget`, network in and out, and any custom CloudWatch metric.
- Metrics such as average CPU are computed across the whole ASG.
- After a scaling action, the group waits in cooldown. The default is 300 seconds.

## Containers

| Service | Launch types | Use case from this course |
|---|---|---|
| [[containers-ecs|ECS]] | EC2, Fargate | Run containers. Fargate is [[serverless|serverless]]. You create a task definition, and AWS runs it by CPU and memory. |
| [[containers-eks|EKS]] | EC2 nodes, Fargate | Use Kubernetes when you already run it on premises or in another cloud. Kubernetes is cloud-agnostic. |
| App Runner | Fully managed | Web apps, APIs, and microservices. Deploy from a container image or source code. |

- ECS can mount [[storage-efs|EFS]] for data persistence. This works with EC2 and Fargate.
- ECS scales on average CPU, average memory, or ALB `RequestCountPerTarget`.
- For EC2 launch types, use an ECS capacity provider paired with an ASG. AWS recommends it.
- EKS node types:
  - Managed node groups: AWS creates and manages EC2 instances, in an ASG. On-demand or Spot.
  - Self-managed nodes: you run EC2 instances in an ASG. You can use prebuilt AMIs.
  - AWS [[compute-fargate|Fargate]]
- EKS storage uses a StorageClass with CSI drivers. Options include EBS, EFS, FSx for Lustre, and FSx for NetApp ONTAP. EFS is the only option that works with Fargate.
- App Runner is accessed by URL. It provides autoscaling, [[high-availability|high availability]], load balancing, and encryption. It supports VPC access.
- App2Container is a CLI tool. It moves Java and .NET apps into containers. It generates [[management-and-governance-cloudformation|CloudFormation]] templates and registers images in ECR.

## Edge compute

[[compute-lambda|Lambda]]@Edge runs code that you attach to CloudFront distributions. The code runs close to users. You pay per use.

## Exam tips

- Pair ELB with an ASG. This is the common combination.
- Use ALB for path, host, and header routing, and for containers. Use NLB for TCP or UDP at very high performance.
- The default ASG cooldown is 300 seconds.
- Predictive scaling uses machine learning for repeating patterns.
- Fargate removes server management.
- For EKS on Fargate, use EFS.
- Average CPU metrics are computed for the whole ASG, not per instance.

[Next: Storage](04-storage.md)
