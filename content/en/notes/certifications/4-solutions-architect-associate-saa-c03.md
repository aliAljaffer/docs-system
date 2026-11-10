---
title: ✅ 4. Solutions Architect - Associate SAA-C03
category: Certifications
description: Min / Max Sizes, Initial Capacity, and Scaling Policies.
tags:
- certification
---

<!-- imported from ObsidianVault/studies/cloud-architecht/✅ 4. Solutions Architect - Associate SAA-C03.md. Edit the source, then run sync.py. -->

# ✅ 4. Solutions Architect - Associate SAA-C03

`certification`

## AWS Overview
[[region|AWS Region]] choice:
1. Compliance with data governance and legal requirements: data never leaves region without explicit permission
2. Proximity to customers
3. Available services within a region
4. Pricing
- [[availability-zones|availability zones]]
- [[edge-location|edge location]]: 400+ Edge Locations
- Region Table: Allows you to see services available for each region
----
 
## [[security-iam|IAM]]
### Summary
- As best practice, employ [[principle-of-least-privilege|principle of least privilege]].
-  are JSON documents detailing what can and can't be done, by who and on what service. A policy contains: Version Number, Policy ID, Statement(s). Statement(s) are composed of:
	- **Statement** ID
	- **Action**: List of actions that the policy governs
	- **Effect**: Whether to allow or deny the listed actions
	- **Principal**: The user the policy applies to
	- **Resources**: Which AWS resources to the policy applies to
	- **Condition** (optional) one or more conditions to satisfy for policy to be applicable, otherwise ignore the policy
-  can be set to adhere to cybersecurity rules to enforce strong passwords by users.
- An addition layer of security can be added by enforcing [[multi-factor-authentication|multi factor authentication]] devices. These devices come in different formats:
	- Virtual (Google Authenticator)
	- Universal 2nd Factory (Physical, U2F): YubiKey
	- SurePassID's Key Fob for AWS GovCloud.
-  provide a way for AWS resources to have access to other AWS resources. 
	- Examples include [[compute-lambda|Lambda]] needing a [[storage-s3|S3]] Role to be able to upload a file programmatically.
- Access to AWS can be done in three ways:
	- AWS CLI - access keys and secret keys
	- AWS Management Console - password + MFA
	- AWS SDK - access keys and secret keys
- Reports can be acquired account-level using Credentials Report, showing status of each user in the account and activity. And user-level with Access Advisor, to see which services the accounts are using.
- 

---
## [[compute-ec2|EC2]]
### Summary
- s
- 
---
## Elastic Load Balancer
### Why use?
![](/assets/vault/pasted-image-20250601200440.webp)
### Features
- ELB is a **managed** load balancer
	- AWS guarantees that it will be working
- it costs less to setup your own LB but it will be more effort on your end
- It is integrated with many AWS services
	- EC2, EC2 Auto Scaling Groups, ECS
	- AWS Cert. Manager, [[aws/management-and-governance-cloudwatch|CloudWatch]]
	- Route 53, WAF, Global Accelerator
### Health Checks
- ELB checks if an instance is properly working, in order to send traffic to it.
- CRUCIAL for ELB.
- `/health` route
### Types
#### Classic Load Balancer (v1) - 2009
- `HTTP, HTTPS, TCP, SSL`
#### Application Load Balancer (v2) - 2016
- `HTTP/2, HTTPS, WebSocket`
- Layer 7 - Application
- **Routing tables to different target groups:**
	- Routing based on  path in URL
	- Routing based on hostname (one.example.com and two.example.com)
	- Routing based on query string, Headers
- **Great fit for MICRO services and container-based applications (Docker, [[containers-ecs|ecs]])**
- Has port mapping feature to redirect to a dynamic port in ECS
- In comparison, we'd need multiple Classic Load Balancer per application.
##### Target Groups
ALB can route to multiple target groups. Health checks are at the target group level.
- EC2 instances - `HTTP`
- ECS tasks - `HTTP`
- Lambda Functions - `HTTP` req. translated into a `JSON` event
- IP addresses - **must be private**
##### Good to Know
- You get a fixed Hostname to access the load balanced target group
- The application servers don't see the IP of the client directly
	- the true IP of the client is inserted in the header X-Forwarded-For
	- `X-Forwarded-Port` and `X-Forwarded-Proto`
#### Network Load Balancer (v2) - 2017
- `TCP, TLS, UDP`
- Layer 4
- Ultra-low latency
- Ultra-high performance, handles millions of request per second
- One static IP per AZ, and supports assigning Elastic IP.
- NLB = Extreme performance, TCP, UDP
##### Target Groups
- EC2 instances
- IP Addresses - **Private**
- Application Load Balancer (NLB $\rightarrow$ ALB)
- Health Checks support `HTTP, HTTPS, TCP`
#### Gateway Load Balancer
- Layer 3 - Network - **IP Protocol.**
- Deploy, scale, and manage a fleet of 3rd party *network virtual appliances* in AWS.
- Network Virtual Appliances: Firewalls, Intrusion Detection and Prevention Systems, Deep Packet Inspection Systems, Payload Manipulation, etc.
- To analyze network traffic
- If you want to have all traffic go through a Firewall, use GLB
- Combines the following functions:
	- Transparent Network Gateway - single entry/exit for all traffic
	- Load Balancer - distributes traffic to virtual appliances
- **Uses GENEVE protocol (port 6081)**
![](/assets/vault/pasted-image-20250603162616.webp)
##### Target Groups
- EC2 instances
- IP Addresses - **Private**
### Security Groups for ELB
- Users can reach the Load Balancer from ANYWHERE HTTP/HTTPS
	- `HTTP/S 80/443 0.0.0.0/0`
- EC2 Instances only allow traffic coming from the load balancer itself
	- allows `HTTP` traffic on `port 80`, with source of `SG-Load Balancer`
![](/assets/vault/pasted-image-20250602224711.webp)
### Sticky Sessions
- It is possible to implement stickiness so that the same client is always redirected to the same instance behind a load balancer.
- Works for CLB, ALB, NLB
- Cookie is used for stickiness and has an expiration date you control.
- Use case: Make sure the user doesn't lose his session data.
- Drawback: Enabling stickiness may imbalance to the load over the EC2 instances
#### Enabling Stickiness
Target Group -> Actions -> Edit Attributes ->  \[Target Selection Configuration\] Stickiness
#### Stickiness Cookie Types
- ****Application-based Cookies****:
	- Custom cookie:
		- Generated by the target
		- Can include any custom attr.
		- Cookie name must be specific indiv.lly for each target group.
		- Don't use **AWSALB**, **AWSALBAPP**, or **AWSALBTG** (reserved)
	- Application cookie:
		- Generated by the load balancer
		- Cookie name is **AWSALBAPP**
- ****Duration-based cookie****:
	- Generated by the load balancer
	- Cookie name is **AWSALB** for ALB and **AWSELB** for CLB 
### Cross-Zone Load Balancing
![](/assets/vault/pasted-image-20250603170700.webp)
- ALB
	- Enabled by default (can be disabled at the Target Group level)
	- No charges for inter-AZ data
- NLB & GLB
	- Disabled by default
	- You pay charges for inter-AZ data if enabled
- CLB
	- No charges for inter-AZ data
### Server Name Indication - SNI
- SNI solves the problem of **loading multiple SSL certs onto one web server**, to serve multiple websites
- Only works for ALB, NLB, [[networking-cloudfront|CloudFront]]
#### Support for SSL Certs
- CLB
	- Support only one SSL cert
	- m-to-m CLB -> SSL
- ALB
	- Supports multiple listeners with multiple SSL certs
	- Uses SNI
- NLB
	- Supports multiple listeners with multiple SSL certs
	- Uses SNI
### Connection Draining
- Naming:
	- Connection Draining for CLB
	- Deregistration Delay for ALB & NLB
- Time to complete "in-flight requests" while the instance is de-registering or unhealthy
- Stops sending new requests to the EC2 instance which is de-registering.
- From 1 to 3600 seconds (default: 300)
- Can be disabled with value 0.
---
## Auto Scaling Group
![](/assets/vault/pasted-image-20250603175318.webp)
- How-to:
	- Set minimum capacity of EC2s
	- Set desired capacity
	- Set maximum capacity
- Can be used with Elastic Load Balancer
- ELB + ASG is a common combination
### Launch Templates
Configurations for your launched instances detailing information like: AMI and Instance Type, EC2 User Data, EBS Volumes, Security Groups, Load Balancer information, Networking information, etc.

Min / Max Sizes, Initial Capacity, and Scaling Policies.
### ASG and CloudWatch
- It is possible to scale an ASG based on CloudWatch alarm
- An alarm monitors a metric, such as Average CPU.
- **Metrics such as Average CPU are computed for the overall ASG instances!**
- Based on the alarm:
	- Scale-out policies to increase number EC2
	- Scale-in policies to decrease number EC2
### Scaling Policies
#### Dynamic Scaling
- **Target Tracking Scaling**
	- Simple to set-up
	- Example: I want the average ASG CPU to stay at around 40%.
- **Simple / Step Scaling**
	- When a CloudWatch alarm is triggered (ex. CPU > 70%), then add 2 EC2 units.
	- When a CloudWatch alarm is triggered (ex. CPU < 30%), then remove 1 EC2 unit.
#### Scheduled Scaling
- Anticipate a scaling based on known usage patterns
- Example: Increase min. capacity to 10 at 5pm on Fridays.
#### Predictive Scaling
- Continuously forecast load and schedule scaling ahead.
- Good for repeating patterns
- Uses **Machine Learning**
### Good Metrics to Scale On
- **CPUUtilization**: Avg. CPU Util. across instances
- **RequestCountPerTarget**: To make sure the number of requests per EC2 is stable.
- Average Network In / Out if the application is network-bound
- Any custom metric you can push using **CloudWatch**.
### Scaling Cooldown
- After a scaling happens, you're in cooldown
- default: 300 seconds.
---
## Amazon RDS
- RDS = Relational Database Service
- A **managed** database service using SQL
- Allows you to create AWS-managed databases in the cloud using popular #engines:
	- Postgres
	- MySQL
	- MariaDB
	- Oracle
	- Microsoft SQL Server
	- IBM DB2
	- Aurora
### Why RDS?
- It is a managed service
	- Automated provisioning, OS patching
	- Continuous backups and restores
	- Monitoring dashboards
	- Read Replicas for improved performance
	- Multi-AZ setup for Disaster Recovery
	- Maintenance windows for upgrades
	- Scaling, both vertical and horizontal
	- Storage back by EBS
- **You cannot SSH into instances**
### RDS Storage Auto Scaling
Helps increase storage in an RDS instance if low-storage is detected, all automatically. You set a **Maximum Storage Threshold**, and the storage is automatically increased if:
- Free storage is less than 10% of allocated storage
- Low-storage lasts at least 5 minutes
- 6 hours have passed since the last modification
Useful for applications with **unpredictable workloads**, supports all RDS database engines
### RDS Read Replicas
READ REPLICAS ARE ONLY FOR ***READ*** (`SELECT ...`) OPERATIONS! NO `INSERT`, `UPDATE`, `DELETE` Can create up to 15 Read Replicas:
- Within AZ
- Cross AZ
- Cross Region
Replication is **ASYNC**, reads are "eventually consistent". To use Read Replicas, the main applications must update the conn_string to leverage read replicas.
#### Use Cases
You have a prod. database and another team wants to run analytics on the database. You create a replica so they can run analytics on it, as to not affect the performance of the prod. database.
#### Network Cost
**Free for same region traffic, costs $ for Cross-Region.**
![](/assets/vault/pasted-image-20250605185137.webp)
### RDS Multi AZ for Disaster Recovery
for Disaster Recovery. **Synchronous** replication. Meaning, any operation that applies to the main DB, must also be applied to the standby instance. You get one DNS name. #availability
No need for manual intervention in apps. **Not used for scaling**.
**Read Replicas can be setup as Multi AZ for Disaster Recovery.**
### RDS From Single-AZ to Multi-AZ
- Zero downtime operation
- Just click on `modify` for the database.
Behind the scenes:
1. Snapshot is taken from Main DB.
2. A DB is restored from the snapshot.
3. Main DB and Restored DB are synchronized.
### RDS Custom
- Managed Oracle and Microsoft SQL Server **with OS and database customization**
- With Custom, we have access to the underlying database and OS so you can configure settings, install patches, access EC2 with SSH
- De-activate Automation Mode to perform your customization.

### RDS Backups
- Automated backups
	- Daily full
	- Transaction logs every 5 mins
	- 1 - 35 days of retention, or **can be disabled with 0.**
	- **Earliest backup you have is one from 5 minutes ago!**
- Manual DB Snapshots
	- triggered by the user
	- Retention for as long as you want
- **Trick: In a stopped RDS database, you will still pay for storage. If you plan on stopping it for a long time, you should snapshot it and restore when needed**
### RDS Restore

### Amazon RDS Proxy
- Fully managed database proxy for RDS
- Allows apps to pool and share DB connections established with the database.
- Improving database efficiency by reducing the stress on database resources and minimize open connections
- [[serverless|Serverless]], autoscaling, highly available (multi-AZ)
- Reduced RDS & Aurora failover time by up to 66%
- Supports RDS (MySQL, PostgreSQL, MariaDB, MS SQL Server) and Aurora (MySQL, PostgreSQL)
- No code changes required for most apps
- **Enforce IAM Authentication for DB, and securely store credentials in AWS Secrets Manager**
- RDS Proxy is never publicly accessible (Must be accessed from [[vpc]])

---
## Amazon Aurora
Supports Postgres and MySQL. Aurora is cloud-optimized with 5x performance over MySQL on RD, and 3x performance of Postgres on RDS.
Storage grows auto. in increments of 10GB, up to 128TB. Aurora can have up to 15 replicas and the replication process is faster than MySQL (sub 10 m.s. replica lag).. Failover is instantaneous. High #availability **Aurora costs 20% more than  but is more efficient.**
### High Availability and Read Scaling
- 6 copies of your data across 3 AZs
	- 4 copies out of 6 needed for **WRITES**
	- 3 for **READS**
	- Self-healing with P2P replication
	- **Storage is striped across 100s of volumes**
- One Aurora instance takes **WRITES** (master)
- Failover in less than 30 seconds
- Master + up to 15 Aurora Read Replicas serve reads
- Support for Cross Region Replication
### Aurora DB Cluster
Writer Endpoint pointing to the master. 
Reader Endpoint = Connection load balancing
### Features of Aurora
- Automatic fail-over
- Backups and Recovery
- Isolation and security
- Industry compliance
- Push-button scaling
- Automated Patching with Zero Downtime
- Advanced Monitoring
- Routine Maintenance
- Backtrack: Restore data at any point of time **without using backups** 
### Aurora Auto Scaling
![](/assets/vault/pasted-image-20250605211516.webp)
### Aurora Custom Endpoint
Setup a custom endpoint that points to specific Aurora instance(s) to use for external tasks such as analytics. Usually the instances are more powerful.
Generally, if a custom endpoint is set, the Reader Endpoint is not used.
### Aurora Serverless
- Automated database instantiation and auto-scaling based on usage.
- Good for infrequent, intermittent or unpredictable workloads
- No capacity planning needing
- Pay per second, can be more cost-effective
### Global Aurora
- Aurora Cross Region Read Replicas
	- Useful for disaster recovery
	- Simple to put in place
- Aurora Global Database (recommended
	- 1 Primary region (R + W)
	- Up to 5 secondary (R) regions, replication lag $\lt\ 1$ second
	- Up to 16 Read Replicas per secondary region
	- Promoting another region for disaster recovery has an [[rto|RTO]] of $\lt$ 1 minute
	- **Typical cross-region replication takes less than 1 second.**
### Aurora Machine Learning
- Enables you to add ML-based predictions to your app via SQL
- Supports [[machine-learning-sagemaker|sagemaker]] and [[machine-learning-comprehend|comprehend]]
- No need to have ML experiences
- Use case: Fraud detection, ads targeting, sentiment analysis, product recommendations.
### Aurora Backups
- Automated backups
	- 1 - 35 days of retention, cannot be disabled.
	- point-in-time recovery in that timeframe
- Manual DB Snapshots
	- triggered by the user
	- Retention for as long as you want
### Aurora Restore Options
- Restoring a RDS / Aurora backup or snapshot creates a new database
- Restoring MySQL RDS database from S3
	- Create backup of on-prem DB
	- Store in Amazon S3
	- Restore into new RDS instance
- Restoring MySQL Aurora cluster from S3
	- Create a backup using Percona XtraBackup
	- Store the backup in S3
	- Restore onto new Aurora cluster running MySQL
### Aurora Database Cloning
- Create a new Aurora DB Cluster from an existing one
- Faster than snapshot and restore
- Uses copy-on-write protocol
- Fast, cost-effective, useful to create a **staging** database for tests
### RDS & Aurora Security
- **At-rest encryption**
	- Database Master & Replicas encryption using AWS KMS - Must be defined as launch time
	- Master must be encrypted for replicas to be encrypted
	- To encrypt unencrypted, snapshot -> restore as encrypted (Like EBS volumes)
- **In-flight encryption**: TLS-ready by default, use the AWS TLS root certificates client-side
- **IAM Authentication**: IAM roles to connect to your database instead of username and password. With Tokens.
- **Security Groups**: Control Network access to your RDS / Aurora
- No SSH available except 
- Audit Logs can be enabled and set to CloudWatch Logs for longer retention
## Amazon ElastiCache

Caches: In-memory databases with really high performance, low latency.
**Using ElastiCache requires heavy application code changes**
- Helps relive load in RDS
### Redis Vs. Memcached
Redis:
- Multi-AZ with Auto-Failover
- Read Replicas to scale reads and have [[high-availability|high availability]]
- Data Durability using AOF persistence
- Backup and restore features
- **Supports Sets and Sorted Sets**
Memecached:
- Multi-node for partitioning of data (**sharding**)
- No [[high-availability|high availability]]
- Non-persistent
- Backup and restore ([[serverless]])
- Multi-Threaded architecture
- For clusters running the Memcached engine, ElastiCache supports Auto Discovery - the ability for client programs to automatically identify all of the nodes in a cache cluster, and to initiate and maintain connections to all of these nodes. With Auto Discovery, your application does not need to manually connect to individual cache nodes; instead, your application connects to one Memcached node and retrieves the list of nodes. From that list, your application is aware of the rest of the nodes in the cluster and can connect to any of them. You do not need to hardcode the individual cache node endpoints in your application. **Cache node failures are automatically detected; failed nodes are automatically replaced.**
### Cache Security
- IAM Authentication is enabled only for **Redis.**
- IAM policies are only used for AWS API-level security.
- Redis AUTH enables password/token when creating a Redis cluster, which provides an extra level of security on top of . It uses SSL in-flight encryption.
- Memcached uses SASL based-authentication (advanced!)
### Loading Patterns
- **Lazy Loading**: **ALL READ DATA** is cached, and **can become stale**.
- **Write Through**: Adds/Updates data in the cache **WHEN WRITTEN** to a DB. **(No stale data!)**
- **Session Store**: Store temporary session data in cache using Time-To-Live (TTL) features.
### Use Case for Redis
Thanks to [Redis' Sorted Sets](https://redis.io/glossary/redis-sorted-sets/), one of the use cases can be on gaming leaderboards. Sorted Sets guarantees uniqueness and element ordering, and each time a new element is added, it's ranked in real-time and added in the correct rank/position.
## Route 53
A highly available, scalable, fully managed, and Authoritative (can be updated) DNS.
The only AWS service with 100% availability [[sla|SLA]].
### Records
- Define how traffic is routed for a domain (not to be confused with load balancer routing)
- Each record contains:
	- Domain/subdomain name
	- Record Type
	- Value
	- Routing policy
	- TTL
- Record types supported by Route 53: **A / AAAA / CNAME / NS**, and advanced types not included in exam: **CAA / DS / MX / NAPTR / PTR / SOA / TXT / SPF / SRV**
A = Maps a hostname to IPv4
AAAA = Maps to a IPv6
CNAME = hostname to hostname, target is a domain name with A or AAAA record.
NS = Name servers for the hosted zone
### Hosted Zones
A hosted zone is a container of records that define how to route traffic to a domain and its subdomains
- **Public Hosted Zone**: Records that specify how to route traffic on the internet
- **Private Hosted Zone**: Records that specify how to route traffic internally (on a [[aws/networking-vpc|VPC]], for example)
Each hosted zone costs $0.50 per month.
![](/assets/vault/pasted-image-20250608172727.webp)
### CNAME vs Alias
**CNAME** = hostname to other hostname, ****only for NON ROOT DOMAINS****
**ALIAS** = hostname to AWS resource, **works for both ROOT and NON ROOT domains**, **free** of charge, and native **health check**. Always of type A / AAAA. Can't set TTL. Targets: ELBs, CloudFront Distributions, API Gateway, Elastic Beanstalk envs, S3 Websites, VPC Interface Endpoints, Global Accelerator, Route 553 record in the same hosted zone. 
**Can't set ALIAS for EC2 DNS name.**
### Routing Policy
#### Simple
Route traffic to a single AWS resource. Can specify random values in the same record, and if multiple values are returned, a random one is chosen by the client. For Aliases, only one AWS resource can be selected. **Can't be associated with health checks.**
#### Weighted
Control the percentage of the requests that go to each specific resource. Assign each record a relative weight. Don't need to sum to 100. DNS records must have the same name and type. Can associate with health checks. 
0 weight on 1 record = no traffic to that record. 0 weight on all records = equal distributions of records.
Use case:
- Load balancing between regions
- Testing new versions.
#### Failover
Setup a primary EC2 instance and a secondary disaster-recovery one. A mandatory health check is associated with the primary instance. In case of a failed health check, we switch the routing to the secondary instance.
Same record names, preferably.
#### Latency-based
Redirect to the resource that has the least latency to the client. Useful when app is latency-sensitive. Latency is based on traffic between users and AWS Regions. Can associate with health checks. 
#### Geolocation
Different from latency based. This is based on user location. Should create a default record in case of no location match.
#### Multi-Value Answer
Route traffic to multiple resources. Can be associated with Health Checks. NOT a substitute for . Up to 8 healthy records are returned for each Multi-Value query.
#### Geoproximity (Using Route 53 Traffic Flow)
Route traffic based on geolocation of users and resources. Shift traffic based on **bias**
Resources:
- AWS resources (specify AWS region)
- Non-AWS resources (specify Lat and Lng)
#### IP-based Routing
Routing using CIDRs
example: route users from a particular ISP to a specific endpoint.
### Domain Registrar vs DNS Service
- Buy a domain from a Registrar
- Usually Registrars provide a DNS service
 But its still possible to use a 3rd party domain with AWS DNS service by specifying custom name servers:
1. Create a  in Route 53
2. Update NS Records on 3rd party website to use Route 53 Name Servers
---
## Three-tier architecture
1. Database Layer
2. Public Layer
3. Private Layer

---
## Speeding up application launch
![](/assets/vault/pasted-image-20250615171242.webp)

---
## CloudFront
- CDN
- Caches content at edge
- 216 edge locations globally
- DDOS protection, integration with [[security-shield|shield]] and [[security-waf|waf]]
### Origins
- S3 buckets, use Origin Access Control to guarantee only CF has access to bucket
- Custom Origin (HTTP) - ALB, [[compute-ec2|ec2]], [[storage-s3|s3]] website with static S3 hosting, any http backend 
### Price Classes
1. Price Class All: All regions, best performance
2. Price class 200: Most regions, minus expensive ones
3. Price class 100: Just the cheapest regions.
## Global Accelerator
- Use case: Single-region deployed app that has global user base.
- Latency-minimization.
- Unicast IP: One server-one IP
- Anycast IP: Many servers-one IP, routes to nearest to requesting client
	- Used by Global Accelerator
- Leverages the AWS internal network to route to your application
	- Client to Edge Location to ALB to the app.
- Works with: Elastic IP, EC2, ALB, NLB, public or private.
- Amazing performance:
	- Routes to lowest latency
	- Static IP
	- Internal AWS
	- Health Checks
	- Failover in < 1min.
	- Only 2 external IPs, secure
	- DDoS Protection
![](/assets/vault/pasted-image-20250705141852.webp)
CF = Cache content, serve from edge
GA = Route connections to the app using edge locations, serve from app region
## Snowball
- Highly-secure and portable data collection and processing device that operates with edge and migrates data in/out of AWS, helps with **Petabytes** of data.
![](/assets/vault/pasted-image-20250705144120.webp)
Use cases: Data migration or Edge Computing where you need to process data while it's being created. **Can run EC2 instances or lambda at the edge.**
![](/assets/vault/pasted-image-20250705144512.webp)
### Amazon FSx
- Launch 3rd party high-performance file systems on AWS, fully managed.
### Deployment Options
- **Scratch file system:** Temporary storage, data is not replicated, HIGH BURST (6x faster), Usage: short-term processing, optimize costs.
- **Persistent FS**: Long-term, same-AZ replication, replace failed files within minutes, Usage: long-term processing, sensitive data
### FSx for Windows File Server
Supports SMB & NTFS, Active Directory, ACLs, user quota. **Can be mounted on Linux EC2 instances.** Supports Microsoft DFS Namespaces.
Scales up to 10s of GB/s, Millions of IOS, 100s PB of data.
- SSD - Latency intesnive
- HDD
- Can be multi-az
- backedup daily to S3
- Accessed on prem using VPN or Direct Connect
### FSx for Lustre
Large-scale computing using parallel distributed file systems.
Lustre = Linux Cluster
- **ML, HPCs**
- Video processing, financial modeling, electronic design automation
- Scales up to 100s of GB/s, Millions of IOS, sub-ms latency.
- SSD: Low latency
- HDD: Throughput intensive
- S3 integration, reading S3 as FS and write back to S3
- Accessed on prem using VPN or Direct Connect

### FSx for NetApp ONTAP
- FS with NFS SMB iSCSI
- Move workloads running on ONTAP or NAS to AWS
- High compatibility
- Storage shrinks or grows automatically
- Snapshots, replication, lowcost, compression, data de-duplication
- Point-in-time insta cloning
### FSx for OpenZFS
- NFS
- Move ZFS -> AWS
- Snapshots, compression, low cost
- Up to 1mil IOPS with < 0.5 latency
## Hybrid Cloud for Storage
AWS Storage Gateway bridges S3 with on prem data
![](/assets/vault/pasted-image-20250705151909.webp)
### S3 File Gateway
![](/assets/vault/pasted-image-20250705152012.webp)
- File gateway caches most recently used files
- SMB has integration with Active Directory for user auth.
### Volume Gateway
- Block storage using iSCSI
- Backed by EBS snapshots
- Cached volumes
- Stored volumes
### Tape Gateway
- Physical tapes
- Virtual Tape Library backed by S3 and ****Glacier****
![](/assets/vault/pasted-image-20250705152452.webp)
### Storage Gateway Hardware Appliance
![](/assets/vault/pasted-image-20250705152558.webp)
### Summary
![](/assets/vault/pasted-image-20250705152755.webp)
## AWS Transfer Family
- Using FTP, FTPS, and SFTP
- Managed infra, scalable, HA
- LDAP, AD, Cognito, OKTA
- Usage: sharing files, CRM, etc.
![](/assets/vault/pasted-image-20250705153024.webp)
## AWS DataSync
- Move **large amounts of data** to/from
	- On-prem / other clouds to AWS (needs agent)
	- AWS to AWS (diff. storage services)
- Can sync to:
	- S3 (Any classes)
	- EFS
	- FSx
- Replication tasks can be scheduled hourly/daily/weekly
- ****File permissions and metadata are preserved****
- One agent task can use 10 Gbps
- In case of **DataSync** need but network isn't suitable for it, ****AWS Snowcone has datasync agent preinstalled**** 
![](/assets/vault/pasted-image-20250705153321.webp)

## SQS

Producers send messages to Queue, Consumers poll messages from the queue.
Use case: decouple between application tiers
### Standard Queue
- Unlimited throughput
- Retention: 4 days, max: 14 days
- Low latency <10ms
- Limited to 256KB per message.
- Can have duplicate messages
- Can have out of order messages
- **At-least-once delivery**
### Security
- In-flight encryption HTTPS API
- At-rest encryption using KMS Keys
### Message Visibility Timeout
After a message is polled, it's invisible to other consumers. The timeout is the `cooldown` where after, the message is visible again to be consumed. Consumer could call the `ChangeMessageVisibility` API to get more time.
### Long Polling
When a consumer requests messages from the queue, it can optional wait for messages to arrive if there are non in the queue.
![](/assets/vault/pasted-image-20250705210019.webp)
### FIFO Queue
Ordered queue, no out-of-order consumption
- Limited throughput 300msg/s
- Exactly-once send capability
- Messages are processed in order by the consumer
- Ordering by message group ID - mandatory param
### SQS with ASG
![](/assets/vault/pasted-image-20250705210253.webp)
### Using SQS as a buffer to database writes
![](/assets/vault/pasted-image-20250705210441.webp)
## SNS
Pub/Sub model of notification.
- SNS "Topic" has multiple subscribers.
- A publisher sends the message to the topic.
- Interested parties subscribe to the topic.
- 12.5mil sub/topic
- 100k topics limit
### Subscribers
- HTTP enpoint
- Email
- SMS & Mobile
- SQS
- Lambda
- Kinesis Data Firehose
### Publishers
- CloudWatch Alarms
- AWS Budgets
- Lambda
- ASG
  - S3
- DynamoDB
- CloudFormation
- DMS
- RDS
- etc...
![](/assets/vault/pasted-image-20250705212737.webp)
### Security
- In-flight encryption HTTPS API
- At-rest encryption using KMS Keys
Access controls: IAM Policies
## SNS + SQS: Fan Out
![](/assets/vault/pasted-image-20250705213002.webp)
Cross-Region delivery
### SNS FIFO Topic
......
SNS FIFO + SQS FIFO Fanout
### Message Filtering
JSON policy
## Kinesis Data Streams

- Collect and store streaming data in real-time.
- Retention up to 1year
- Ability to replay data by consumers
- Cant delete until expires
- up to 1 MB
- same partition ID guarantees order
![](/assets/vault/pasted-image-20250705213738.webp)
### Capacity Modes
- Provisioned:
	- Choose number of shards
	- Each shard gets 1MB/s in and 2MB/s out
	- Scale manually the number of shards
	- Pay per shard per hour
- On-demand:
	- No need to provision
	- Autoscaling
	- Default capacity 4MB/s in
## Data Firehose

Data sending to other destination.
- Fully managed
- Autoscaling, serverless, PAYG
- **Near real-time**
- Supports CSV, JSON, binary, text, ...
- Custom conversion can be done on lambda
- Producers:
	- Client
	- SDK
	- Kinesis agent
	- application
	- IoT
	- CloudWatch
	- Data Streams
- Destinations:
	- See image
![](/assets/vault/pasted-image-20250705214256.webp)
### Comparison
![](/assets/vault/pasted-image-20250705214508.webp)
### SQS SNS Kinesis
![](/assets/vault/pasted-image-20250705214628.webp)
## Amazon MQ
- Managed message broker service for RabbitMQ and ACTIVEMQ
- Doesn't scale like SQS and SNS
- has both Q and topic feature like SQS and SNS
## Container vs VM
![](/assets/vault/pasted-image-20250706123509.webp)
## Elastic Container Service
Launch types:
- EC2 - Provisioned EC2 instances and the containers are in them
- Fargate - Serverless, no provisioning. Create **Task Definition** and AWS will run the task based on CPU / RAM.
![](/assets/vault/pasted-image-20250706124003.webp)
### Data Volumes
for data persistence.
- Mount EFS onto ECS tasks. 
- Works with both EC2 and Fargate launch type
- Fargate + EFS = Serverless
### ECS Service Auto Scaling
Metrics to scale on:
- Avg. CPU Util.
- Avg. Mem. Util.
- ALB RequestCountPerTarget
### Autoscaling for EC2 Launch Types
- ASG
- ECS Cluster Capacity Provider (Recommended)
	- Capacity Provider paired with ASG
	- Add EC2 Instances when you're missing capacity (CPU, RAM)
### SA for ECS
![](/assets/vault/pasted-image-20250706124752.webp)
![](/assets/vault/pasted-image-20250706124834.webp)
![](/assets/vault/pasted-image-20250706124938.webp)
## Elastic Kubernetes Service
Launch types:
- EC2 - Provisioned EC2 instances and the containers are in them
- Fargate - Serverless, no provisioning. Create **Task Definition** and AWS will run the task based on CPU / RAM.
Use case: if company is already using KBNTS on prem or in other cloud
**Kubernetes is cloud-agnostic.**
Node types:
- Managed Node Groups:
	- Creates and manages EC2 instances for you
	- On-demand and spot instances
	- nodes are part of ASG
- Self-Managed
	- EKS Cluster + ASG
	- Can use prebuilt AMIs
	- On-demand and spot instances
- AWS Fargate
### Data Volumes
for data persistence.
Need to specify **StorageClass** manifest in EKS Cluster
Leverages **Container Storage Interface CSI** compliant driver
- EBS
- EFS (only class that works with fargate)
- FSx for Lustre
- FSx for NetApp
## AWS App Runner
- Fully managed service that makes it easy to deploy web apps
- No infra experience needed
- Start with container or source code (can connect to github)
- Accessed by URL
- Autoscaling, HA, LB, encryption
- VPC access support
Use case: web apps, apis, microservices, rapid prod development.
## AWS App2Container
- CLI tool for migrating **Java** and **.NET** into docker containers
- Lift-and-shift your apps 
- Generate CF Temlates
- Register containers to ECR
- Deploy to ECS, EKS, App Runner
- Supports CI/CD pipelines
## Lambda@Edge
- Edge Functions: Code you write and attach to CloudFront distributions
- Runs close yo your users
- PAYG, serverless
![](/assets/vault/pasted-image-20250706143304.webp)
![](/assets/vault/pasted-image-20250706143119.webp)
### CloudFront Functions
![](/assets/vault/pasted-image-20250706143230.webp)
### Comparison
![](/assets/vault/pasted-image-20250706143327.webp)
### Use Cases
![](/assets/vault/pasted-image-20250706143456.webp)
## DynamoDB

- NoSQL, fully managed, HA with multi-AZ
- Scales, millions of requests/sec
- Fast, single-digit ms
- Integrated with IAM for security
- low cost and autoscaling
- no maintenance, always available
- Standard & Infrequent Access
- Max size of a row = 400KB
![](/assets/vault/pasted-image-20250706144322.webp)
![](/assets/vault/pasted-image-20250706144352.webp)
### Read/Write Capacity
- Control how you manage table capacity
- Provisioned Mode (Default)
	- Plan capacity, specify r/w per sec
	- pay for RCU & WCU
	- can add autoscaling
- On-Demand mode
	- R/W autoscales based on workload
	- PAYG, expensive
	- #unpredictable, #steep_sudden_spike_workloads
	- No planning
### DynamoDB Accelerator (DAX)
- In-memory cache, managed
- **Help solve read congestion by caching**
- #Microseconds latency for cached data
### DynamoDB Streams
![](/assets/vault/pasted-image-20250706145237.webp)
### Stream Processing
![](/assets/vault/pasted-image-20250706145154.webp)
### Global Tables
Make a dynamoDB table accessible with low latency in multiple-regions
**Must enable DynamoDB streams first**
### TTL

![](/assets/vault/pasted-image-20250706145423.webp)
### Backups
![](/assets/vault/pasted-image-20250706145525.webp)
### S3 Integration
- Export to S3 (enable PITR)
- Import CSV, DynamoDB Json, or ION format
### Row-Level Security in DynamoDB with Cognito
![](/assets/vault/pasted-image-20250706151004.webp)
## API Gateway
![](/assets/vault/pasted-image-20250706150028.webp)
### Integrations
![](/assets/vault/pasted-image-20250706150125.webp)
### Endpoint Types
![](/assets/vault/pasted-image-20250706150246.webp)
### Security
![](/assets/vault/pasted-image-20250706150338.webp)
## Step Functions
Visual workflow builder
Features: Sequence, parallel, conditions, timeouts, etc
Can integrate with EC2, ECS, On-prem, API, ...
![](/assets/vault/pasted-image-20250706150530.webp)
## Cognito

Give users an identity to interact with our web app
### User Pools
- Sign-in 
- Integrate with API + ALB
- MFA
- Federated identities with Google, Facebook, etc
### Identity Pools
- Provide AWS credentials so they can access AWS resources directly
- integrate with user pools as ID provider
![](/assets/vault/pasted-image-20250706150901.webp)

## Databases
![](/assets/vault/pasted-image-20250706160718.webp)
### RDS Summary

![](/assets/vault/pasted-image-20250706161152.webp)
### Aurora Summary

![](/assets/vault/pasted-image-20250706161131.webp)
### ElastiCache Summary

![](/assets/vault/pasted-image-20250706161323.webp)
### DynamoDB Summary

![](/assets/vault/pasted-image-20250706161400.webp)
### S3 Summary

![](/assets/vault/pasted-image-20250706161505.webp)
### DocumentDB

- Aurora version of MongoDB
- Similar deployment concepts as 
### Neptune
- Graph database, like a social network.
- 3 AZ replications, -> 15 read replicas
- Billions of relations stored with ms latency queries
- Great for knowledge graphs like Wikipedia
#### Neptune Streams
- Real-time ordered sequence of every change to your graph data
- No duplicates, strict ordering
- Changes are available immediately after writing
- Available through HTTP REST API
### Keyspaces for Apache Cassandra

- Cassandra is O.S. NoSQL db.
- Replicated 3x across multi AZ
- Capacity mode:
	- Provisioned
	- On-demand
![](/assets/vault/pasted-image-20250706162003.webp)
### QLDB

Quantum Ledger Database
- A ledger is a book recording **financial transactions**
- Fully managed, serverless, HA, Replication across 3 AZ.
- Review history of changes
- Immutable: No entry can be removed or modified
- **HAS **CENTRAL** AUTHORITY CONTROLLER**
### Managed Blockchain
Decentralized
### Timestream
- managed, fast, scalable, serverless
- Time series database
- autoscale
- 100s times faster & 1/10th the cost of relational
- Built-in analytics
- encrypted
- IoT apps, operational, real-time appliances, ML with SageMaker, Grafana
### Athena

- Serverless query service to analyze data stored in S3 using SQL
- Connects to Quicksight
- $5 per TB scanned
- Use Case: Log analysis, BI, CLoudTrails
#### Performance Improvement
 Use Columnar data for cost-saving by scanning less
- Apache Parquet or ORC
- High Performance
- Use Glue to convery your data to Parquet
- Compress data
![](/assets/vault/pasted-image-20250706184249.webp)
#### Federated Query
- Allows to run SQL queries ANYWHERE
- Using Data Source Connectors that run on Lambda to run Federated Queries 
![](/assets/vault/pasted-image-20250706184558.webp)
### Redshift
PostgreSQL based DB but it's not used for OLTP. It's OLAP (Online analytical processing).
- 10x better performance than other data warehouses
- Columnar storage of data
- Provisioned cluster and Serverless cluster
- Has a SQL interface
- Integration with Quicksight and Tableau
- vs : Faster queries, joins, aggregation thanks to indices.
![](/assets/vault/pasted-image-20250706185539.webp)
#### Snapshots & DR
- Redshift has Multi-AZ for SOME clusters
- Auto or manual snapshot, restored into cluster
- Can copy snapshots to another region
![](/assets/vault/pasted-image-20250706185912.webp)
In EC2 case, better to write data in batches. LARGE INSERT!
#### Redshift Spectrum
- Query data that is already in S3 without loading
- Must have a Redshift cluster available
- Query is then submitted to thousands of Redshift Spectrum nodes
### OpenSearch
![](/assets/vault/pasted-image-20250706190224.webp)
- DynamoDB search
- CloudWatch Logs
### EMR
Hadoop Clusters for Big Data
EMR = **Elastic MapReduce**
100s of EC2 instances
Autoscale, can use Spot instances
Use case: big data, ML, web indexing
#### Node Types
- Master Node: Manages the cluster
- Core Node: Run tasks and store data
- Task Note: Just run tasks, usually Spot
### Quicksight

- Commonly Quicksight + Athena/Redshift
- Serverless ML-powered, creating dashboards
- Business Analytics, visualizations, ad-hoc
- In-memory computation using SPICE engine if data is imported into QuickSight
- Enterprise edition: Column-level security
- Integration, data sources: 
	- 
	- SaaS: Salesforce, Jira
	- Imports: XLSX, CSV, JSON
	- On prem: teradata
![](/assets/vault/pasted-image-20250706191005.webp)
### Glue
- Extract, transform, load (ETL) service
- Prepares data for analytics
- Serverless
![](/assets/vault/pasted-image-20250706191051.webp)
![](/assets/vault/pasted-image-20250706191200.webp)
#### Glue Data Catalog
Catalog of datasets.
![](/assets/vault/pasted-image-20250706191313.webp)
#### Glue Features
- **Glue Job Bookmarks**: Prevent reprocessing old data
- **Glue Elastic Views**: Combine and repl. data across multiple data stores using SQL.
- **Glue DataBrew**: Clean and normalize data for ML or analytics
- **Glue Studio**: GUI to run and monitor jobs
- **Glue Streaming ETL** (built on Apache Spark): Compatible with , Kafka, MSK
### Lake Formation
Data lake = central place to store data for analytics
- Fully managed service to setup a data lake in days
- automates complex steps
- Combine structured and unstructured
- Out of the box blueprints
- ****Fine-grained Access Control for apps (RLS and CLS)****
- Built on top of 
- **Use case**: Centralized permissions
![](/assets/vault/pasted-image-20250706192042.webp)
### Amazon Managed Service for Apache Flink

![](/assets/vault/pasted-image-20250707125919.webp)
Data Streams, NOT Firehose
### Amazon Managed Streaming for Apache Kafka
- Alternative to 
- Fully managed Apache Kafka
- Create, update, delete clusters
- deploy in vpc, multi AZ
- auto recovery from failure
- Data is stored on EBS for ****as long as you want****
- **MSK Serverless:** Run Apache Kafka without managing capacity
![](/assets/vault/pasted-image-20250707130218.webp)
#### MSK vs Kinesis Data Streams
![](/assets/vault/pasted-image-20250707130510.webp)
#### Consumers
- 
- 
- [[compute-lambda|lambda]]
- Apps running on EC2, ECS, EKS
## Machine Learning
### Rekognition
- Find objects, ppl, etc in images using ML
- Facial analysis and facial search to do user verification
- Create a db of "familiar faces".
- Use cases:
	- Labeling
	- Content Moderation: Detect content that is inappropriate, unwanted or offensive
	- Text Detection
	- Face Detection
	- Face Search
	- **Pathing (For sport game analysis)**
### Transcribe
Speech to text
**Can remove PII using Redaction** and access to Auto-Language Identification.
### Polly
Text to Speech
Opposite of 
#### Lexicon & SSML
- Customize the pronunciation of words using lexicons.
	- Acronyms: AWS -> Amazon Web Services
	- Stylized: Al1 Alj4ff3r -> Ali Aljaffer
- Speech Synthesis Markup Language
	- Emphasize words
	- breathing sounds, whispers
	- using Newscaster speech style
### Translate
You can guess what it does
### Lex
Same tech powering Alexa
- Automatic SPeech Recognition to convert speech to text
- Understands intent of text
- Helps build chatbots
### Connect
- Receive calls, create contact flow virtual contact center
- Can integrate with CRM or AWS
- No upfront payment, 80% cheaper than trad solutions
![](/assets/vault/pasted-image-20250707154655.webp)
### Comprehend
- NLP managed serverless service that finds insight and relationships in text
- #sentiment_analysis
- Use case: review analysis (+ve of -ve)
#### Comprehend Medical
Uses NLP to return useful info from clinical text. Can detect Protected Health Information (PHI). Store in S3.
### SageMaker
- Fully managed service for devs and data scientists to build ML models
### Kendra
****Document search service**** to extract answers from within a document. Can fine-tune search results.
### Personalize
- **Recommendation**, real-time
- Build apps that recommend to customers items that are similar.
![](/assets/vault/pasted-image-20250707155247.webp)
### Textract
Extracts text from scanned documents. NAFATH.
### Summary
![](/assets/vault/pasted-image-20250707155501.webp)
## Logging, Monitoring
### CloudWatch
- Provides metrics for every AWS service
- Metric is a variable to monitor.
- Metrics belong to namespaces
- Dimension is an attribute of a metric (instance ID, env, etc)
	- 30 Dimensions per metric
- Metrics have timestamps
- Can create custom metrics
#### Metric Streams
- Stream near-real-time metrics to Kinesis Data Firehose or 3rd party providers.
![](/assets/vault/pasted-image-20250707172212.webp)
### Alarms
![](/assets/vault/pasted-image-20250707175346.webp)
#### Alarm Targets
- EC2
- EC2 Autoscaling
- SNS
#### Composite Alarms
Create an alarm of alarms
### EC2 Instance Recovery with CloudWatch Alarms
![](/assets/vault/pasted-image-20250707174710.webp)
### CloudWatch Container Insights
![](/assets/vault/pasted-image-20250707180554.webp)
### CloudWatch Lambda Insights
![](/assets/vault/pasted-image-20250707180640.webp)
### CloudWatch Contributor Insights
**Top K contributors to ....**
![](/assets/vault/pasted-image-20250707180757.webp)
#### CloudWatch Application Insights
![](/assets/vault/pasted-image-20250707180920.webp)
### EventBridge
- **Schedule**: Cron Jobs
- Event **Pattern**: Event rules that can react to a service doing something
#### EventBridge Rules
- Sends JSON of the source event to the destination
![](/assets/vault/pasted-image-20250707180156.webp)
Replay events to see if the bug has been truly fixed
#### Schema Registry
![](/assets/vault/pasted-image-20250707180319.webp)
#### Cross-Account Bussing
![](/assets/vault/pasted-image-20250707180415.webp)
### CloudTrail
- Governance, compliance, and audit
- ENABLED
- Get history of events or API calls
- **If a resource is deleted in AWS, investigate CloudTrail**
- **90-Day retention**, move to S3 then use Athena to analyze.
#### CloudTrail Events
- **Management Events**: Operations performed on resources. Can separate read from write events.
- **Data Events**: Not logged by default.
- **CloudTrail Insights Event**: See below
#### CloudTrail Insights
- Enable to detect unusual activity.
- Analyzes what's "normal" to create a baseline to know what anomalies are.
![](/assets/vault/pasted-image-20250707181523.webp)
#### Intercept API Call
![](/assets/vault/pasted-image-20250707181701.webp)
### AWS Config
![](/assets/vault/pasted-image-20250707181836.webp)
#### Config Rules
- AWS-managed config rules
- Can make custom config rules (must be defined in Lambda)
	- ex: Evaluate if each EBS disk is type `gp2`
- Pricing: 0.003 USD per config item per region, 0.001 USD per config rule evaluation per region
![](/assets/vault/pasted-image-20250707182232.webp)
### CloudWatch vs CloudTrail vs Config
![](/assets/vault/pasted-image-20250707182347.webp)
#### Example
![](/assets/vault/pasted-image-20250707182443.webp)
## Identity and Access Management
### Organizations
![](/assets/vault/pasted-image-20250707185713.webp)
### Advantages
![](/assets/vault/pasted-image-20250707192230.webp)
### IAM Conditions
`aws:SourceIp` - Restricts the client IP from which the API calls are being made.
`aws:RequestedRegion` - Deny access to service T O  specific regions 
![](/assets/vault/pasted-image-20250707193810.webp)
`aws:PrincipalOrgID` - restrict/allow action by org ID
### IAM Roles vs. Resource-Based Policies
![](/assets/vault/pasted-image-20250707194043.webp)
![](/assets/vault/pasted-image-20250707202626.webp)
### IAM Permission Boundaries
Define the MAX permissions an IAM entity can get. Supports only users and roles, no groups.
Can be used with Organization SCPs.
![](/assets/vault/pasted-image-20250707203056.webp)
### IAM Policy
![](/assets/vault/pasted-image-20250707203712.webp)
1. No, `sqs:*` denies all.
2. No, there's an explicit deny on all `sqs` actions.
3. No, there's no explicit allow for `ec2:DescribeInstances`
### IAM Identity Center
- AWS SSO successor
- One login for all:
	- AWS accounts in 
	- Business cloud apps
	- SAML2.0-enabled apps
	- EC2 Windows Instances
- Identity Providers:
	- Built-it identity store
	- 3rd party: Active Directory, Okta, etc
#### Multi-Account Permissions
- Manage access across accounts
-  - collection of IAM policies
#### Application Assignments
- SSO access SAML2.0
- Provide required URLS
#### Attribute Based Access Control
- Fine-grained perms based on users attributes in the identity store
- Use case: define permissions once, modify AWS access by changing the attributes
#### Permission sets
![](/assets/vault/pasted-image-20250707204301.webp)
### Microsoft Active Directory
![](/assets/vault/pasted-image-20250707205810.webp)
### AWS Directory Services
![](/assets/vault/pasted-image-20250707210116.webp)
![](/assets/vault/pasted-image-20250707210237.webp)
### Control Tower
![](/assets/vault/pasted-image-20250707210344.webp)
#### Guardrails
- Ongoing governance for your Control Tower environment
- **Preventive Guardrail** using SCPs (Restrict regions across all accounts)
- **Detective Guardrail** using  (Identify untagged resources)
---
## Security
### Key Management Service KMS
- Able to audit key usage through CloudTrail
#### Encryption types
- Symmetric AES-256: same key for enc and dec.
- Asymmetric RSA: Pub to encrypt, Priv to decrypt
#### Cross-Region Keying
- Must take a snapshot copy to move to another region.
#### Key Policy
- Control access to KMS keys
![](/assets/vault/pasted-image-20250708113126.webp)
#### Multi-Region Key
- Main region, and then key replicates to other regions. Key-ID stays the same, and auto-rotation.
- Encrypt in one region, decrypt in other regions
- NOT recommended usually
- Use cases: global client-side encryption, encryption on Global DynamoDB, Global Aurora
- E.g. encryption the SSN column in user data allows the database to be hosted in other regions without fear of external PII access
#### AMI Sharing
![](/assets/vault/pasted-image-20250708210316.webp)
### Systems Manager Parameter Store
- Version tracking
- Storage for configs and secrets
- Integration with CloudFormation
![](/assets/vault/pasted-image-20250708210542.webp)
![](/assets/vault/pasted-image-20250708213545.webp)
### Secrets Manager
- Storing secrets
- Can force rotation of secrets every X days
- Automate generation of secrets on rotation using a custom Lambda
- Integrated with 
- Can be encrypted in KMS
- **RDS Integration**, **secrets**
- **Multi-Region secrets**: Replication to other regions. For availability and **DR**
### Certificate Manager ACM
- Provision and deploy TLS certificates
- Provide in-flight encryption
- CLB, ALB, NLB
- CF Distributions
- APIs
- Cannot use ACM with EC2
#### Request procedure for certs
![](/assets/vault/pasted-image-20250708221444.webp)
#### API Integration
![](/assets/vault/pasted-image-20250708221859.webp)
### Web Application Firewall WAF
- #Layer7 (HTTP)
- Deploy on:
	- ALB
	- API Gateway
	- CF
	- AppSync
	- Cognito User Pool
![](/assets/vault/pasted-image-20250708222113.webp)
![](/assets/vault/pasted-image-20250708222202.webp)
### Shield

- Protection from DDoS
- Shield Standard: Free, provides protection from attacks like SYN floods and other layer3/4 attacks
- Shield advanced: DDoS mitigation ($3k/m) protect against sophisticated attacks. Protect against higher fees during attack
- Deploys  rules to mitigate layer 7 attacks.
### Firewall Manager
- Manage rules in all accounts in the 
- Security policy: common set of rules. Applies to:
	- WAF (ALB, API, CF)
	- Shield Advanced
	- SGs for EC2
	- Network Firewall (VPC-level Firewall)
	-  resolver DNS firewall
	- Policies are region-based
- Rules are applied to new resources across all and future accounts
![](/assets/vault/pasted-image-20250708223018.webp)
### Best practices for DDoS
See **26. Security, Video 18.**
### GuardDuty
- ML-powered threat discovery to protect your account using Anomaly Detection
- Looks at CloudTrail logs, VPC Flow logs, DNS logs, etc.
- Can integrate with , where you can pretty much perform any action after an event triggers.
- Can protect CryptoCurrency attacks
![](/assets/vault/pasted-image-20250708224531.webp)
### Inspector
- Automated security assessments
- For EC2:
	- SSM agent
	- Analyze unintended network accessibility
	- **Analyze running OS against know vulns.**
- For Container Images in ECR
	- Assesses images as they are pushed
- For Lambda functions:
	- Identifies software vulns in function code and deps
	- Assessment of functions as they deploy
- Reporting & integration with AWS Security Hub
- Send findings to EventBridge
#### What Inspector does
![](/assets/vault/pasted-image-20250708225404.webp)
### Macie
- Fully managed data security and privacy in S3 buckets
- Alerts to sensitive data like PII and notifies you through 
---
## Networking
### Networking Concepts
#### Private vs. Public IP (IPv4)
- IPv4 = 3.7 billion addresses
#### Elastic IP
A static public IPv4. Avoid using Elastic IP. Instead, use a random public IP and register a DNS name to it ([[networking-route53|route53]]) or a [[autoscaling-groups-and-load-balancers|load balancer]]
#### SSL/TLS
- SSL Cert. allows traffic between clients and load balancer to be encrypted in transit
- SSL = Secure Sockets Layer
- TLS = Transport Layer Security
- TLS Certificates are mainly used, and have an expiration date and must be renewed.
![](/assets/vault/pasted-image-20250603171443.webp)
### VPC
#### Private CIDRs
private **allowed** CIDRS
- `10.0.0.0/8` Big Networks
- `172.16.0.0./12` AWS default VPC range
- `192.168.0.0/16` home networks
#### Limits
- 5 VPC per region, soft limit
- Max CIDR per VPC is 5
	- Min size is `/28` (2^4 = 16 addresses)
	- Max size is `/16` (65,536 addresses)
- Because VPC is private, only private cidrs are allowed 
- Your VPC CIDR should NOT overlap with your other networks.
#### Subnet
- Subrange in the VPC CIDR
- **AWS Reserves 5 IP addresses (First 4 and Last 1) in each subnet**
- The 5 addresses are not available for use
- e.g. for `10.0.0.0/24`
	- `10.0.0.0` - Network address
	- `10.0.0.1` - Reserved for VPC router
	- `10.0.0.2` - Reserved for mapping to Amazon-provided DNS
	- `10.0.0.3` - Reserved for future use
	- `10.0.0.255` Network Broadcast Address
![](/assets/vault/pasted-image-20250709125810.webp)
#### Internet Gateway
- Allows resources in VPC to connect to the internet
- Two-way connection
- Scales horizontally, HA
- One-to-one VPC-IGW
- **Route Table is needed!**
- `/0 -> igw`
#### Bastion Hosts
- An EC2 instance in a public subnet that has internet connectivity and access to private EC2 instances in private subnets.
- This allows you to reach the private instances through the Bastion host:
	- Bastion host security group has port 22 open for RESTRICTED CIDR, like the public corporation CIDR
	- SSH into bastion host
	- private EC2 instances must allow SSH from Bastion-SG or the private IP of Bastion host
	- SSH from within bastion host into private EC2 instances
#### NAT Instances (outdated)
NAT = Network Address Translation, re-writes packets
Allows EC2 instances in private subnets to connect to the internet.
Must be launched in Public Subnet!
Must disable **Source/Dest Check**
Route table required, like 
Not HA or resilient
![](/assets/vault/pasted-image-20250709133901.webp)
#### NAT Gateway
- AWS-managed NAT instances, HA, scalable
- Resilient within a single AZ
- Must create multiple NAT gateways in multiple AZs for fault-tolerance
- Pay per hour
- Can't be used by EC2 instances in the same subnet
- IGW required
- 5Gbps to 100Gbps bandwidth
#### Gateway vs Instance
![](/assets/vault/pasted-image-20250709143027.webp)
#### VPC Traffic Mirroring
![](/assets/vault/pasted-image-20250709164631.webp)
Use cases: Content inspection, troubleshooting, threat monitoring, ..
#### Security Groups & NACL
- SG = Instance-level, stateful = outbound is allowed, it remembers that an inbound connection got in
- NACL = Subnet-level, stateless
![](/assets/vault/pasted-image-20250709143721.webp)
##### NACL
- Like a firewall which control traffic from and to subnets
- One NACL per subnet
- You define the NACL rules with numbers for precedence, first rule to match will drive the decision to allow or deny
- last rule (\*) is a deny
- AWS recommends adding rules by increment of 100
##### Default NACL
Allows everything outbound and inbound by default.
##### Ephemeral Ports
- Clients connect to a defined port, and expect a response on an **ephemeral port** that is random and temporary for the connection life
- `IANA & MS Windows 10` -> Ports `49152 - 65535`
- `Linux` -> Ports `32768 - 60999`
![](/assets/vault/16.-nacl-&-security-groups-0001.webp)
#### SG vs NACL
![](/assets/vault/pasted-image-20250709144518.webp)
#### VPC Peering
- **Privately** connect two VPCs using AWS network
- Cross-Region and Cross-Account possible
- Make them behave as if they were the same network
- Must not overlap
- All VPCs must have peering enabled!
- Not transitive: **A -> B** and **B -> C** does not necessarily imply **A -> C**
- **Must update the route tables in each subnet** 
	- VPC A: send traffic going to vpcB.CIDR to peering connection
	- VPC B: send traffic going to vpcA.CIDR to peering connection
- You can reference SGs from other VPCs
#### VPC Endpoints
- Uses a PRIVATE connection to access AWS services without touching the public internet.
- Powered by AWS PrivateLink.
- Redundant and scale horizontally.
##### Interface Endpoints
- Provision an ENI (Elastic Network Interface) as entry point (so a Private IP)
- Supports most AWS services
- $ per hour + $ per GB of data processed
##### Gateway Endpoint
- Provisions a gateway and must be used as a target in a route table
- **No private IP**
- Supports S3 and DynamoDB
- FREE
##### Gateway or Interface for S3?
![](/assets/vault/pasted-image-20250709151544.webp)
#### VPC Flow Logs
- Capture IP traffic information going into your interfaces:
	- VPC Flow Logs
	- Subnet Flow Logs
	- ENI Flow Logs
- Helps with network monitoring
- Log data can go to S3, CloudWatch, Kinesis Data Firehose.
- Captures network info from AWS managed services too: ELB, RDS, ElastiCache, etc..
![](/assets/vault/pasted-image-20250709152851.webp)
##### What you can do with Flow Logs
![](/assets/vault/pasted-image-20250709153154.webp)
#### Site-to-Site VPN
- Encrypted connection over the PUBLIC internet connecting a VPC to an on-prem data center CGW.
- **Virtual Private Gateway VGW**
	- VPN Concentrator (?) **on the AWS side **of the VPN connection
	- VGW is created and attached to the VPC from which you want to create a S2S VPN connection.
	- Possibility to customize the Autonomous System Number (?)
- **Customer Gateway CGW**
	- Software or physical device on the customer side of the VPN connection
![](/assets/vault/pasted-image-20250709154742.webp)
**Route Propagation**
- Enable ICMP inbound connections in the VPC SG to be able to PING
##### VPN CloudHub
![](/assets/vault/pasted-image-20250709154941.webp)
### Direct Connect (DX)
- Provides dedicated private connection from a remote network to your VPC
- Dedicated connection must be setup between your data center and AWS Direct Connect locations
- Need VPG on VPC
- Private but not encrypted!
	- For encryption, use Direct Connect + VPN. See Diagram
- Access public resources like S3 and private resources like EC2 **on the same connection**
- Use cases: Increase bandwidth, lower cost, working with large data sets, more consistent network experience, and HYBRID ENVIRONMENTS
- IPv4 and IPv6 supported.
![](/assets/vault/pasted-image-20250709155515.webp)
#### Direct Connect Gateway
- Used to setup  to one or more VPC in different regions (same account)
![](/assets/vault/pasted-image-20250709155606.webp)
#### Connection Types
- Dedicated Connections: 1/10/100 Gbps capacity
	- Ethernet port for the customer
- Hosted Connections: 50/500Mbps/10Gbps
	- Capacity can be added or removed
	- 1/2/5/10Gbps available at select Direct Connect Partners
- ****Lead times: LONGER THAN 1 MONTH.****
#### Resiliency
- High Resiliency for Critical Workloads
- Maximum Resiliency for Critical Workloads.
#### S2S Connection as Backup
![](/assets/vault/pasted-image-20250709160609.webp)
#### Transit Gateway
Transitive Peering as an alternative to 
![](/assets/vault/pasted-image-20250709163920.webp)
- Can work corss-region
- You can peer transit gateways together
- Use route tables to limit which vpc can talk to another
- Works with DX Gateway, VPN connections
- Only AWS **IP Multicast** service
##### Use case: Increase throughput
![](/assets/vault/pasted-image-20250709164227.webp)
![](/assets/vault/pasted-image-20250709164316.webp)
##### Use case: Share  between multiple accounts.
![](/assets/vault/pasted-image-20250709164404.webp)
### IPv6
IPv4 only provides 4.3 billion addresses. IPv6 provides $3.4\cdot 10^{38}$ addresses. All IPv6 addresses in AWS are public.
#### Egress-only Internet Gateway
- Used for IPv6 Only!
- NAT Gateway but for IPv6
- Allows instances in your VPC **outbound** connections over IPv6.
- You must update the route tables
![](/assets/vault/pasted-image-20250709165925.webp)
### Networking Costs
![](/assets/vault/pasted-image-20250709170408.webp)
![](/assets/vault/pasted-image-20250709170649.webp)
![](/assets/vault/pasted-image-20250709170831.webp)
![](/assets/vault/pasted-image-20250709171045.webp) 
### Network Protections
- NACLs
- VPC SGs
- WAF
- Shield
- Firewall Manager
#### AWS Network Firewall
Protects the entire VPC with a firewall. Protects from Layer 3 to Layer 7 protection.
- Any direction you can inspect:
	-  to 
	- Outbound to internet
	- Inbound to internet
	- To/from  & 
- Internally, Network Firewall uses 
- Rules can be centrally managed cross-account by  to apply to many s
- Supports 1000s of rules and filtering for:
	- IP & port filtering
	- Protocol
	- Stateful domain list
	- regex patterns
- Traffic filtering: Allow, drop, alert
- Active flow inspection
- Send logs to S3, , 
## Disaster Recovery
- **Disaster**: Any event that has a negative impact on a company's business continuity or finances.
- Disaster Recovery is about preparing for and recovering from a disaster.
![](/assets/vault/pasted-image-20250709185549.webp)
RPO: How back in time can you go back to recover. Time in-between RPO and disaster is data loss. (Pre-disaster time)
RTO: The time you actually recover from a disaster. Time in-between disaster and RTO is downtime. (Post-disaster time)
**You want to minimize both.** But it's costly.
### Disaster Recovery Strategies
![](/assets/vault/pasted-image-20250709185809.webp)
#### Backup and Restore
Easy, cheap, high RPO and RTO.
#### Pilot Light
- A small version of the app is always running, useful for critical core apps.
- Faster than  as critical core is already running
- Lower RPO, Lower RTO, cheap-ish.
![](/assets/vault/pasted-image-20250709191659.webp)
#### Warm Standby
- Full system is up and running but at minimum size
- Upon disaster we can scale to production load.
- Low RPO, RTO.
#### Multi-Site / Hot Site
- Very low RTO, very expensive
- Full prod scale running on-prem and AWS
- Both active, DNS points to both active/active
#### All AWS Multi-Region
- Same as  but both apps are on AWS
### DR Tips
![](/assets/vault/pasted-image-20250709194236.webp)
### DMS
- Quickly and securely migrate databases to AWS
- Source db remains available
- Supports:
	- Homogeneous migrations
	- Heterogeneous migrations
- Continuos Data Replication
- Must create an EC2 instance to perform the replications
![](/assets/vault/pasted-image-20250709194504.webp)
#### Schema Conversion Tool SCT
- Convert schema from one engine to another
	- e.g. SQLite to MySQL
- No need for SCT for same-engine migrations
#### Continuos Replication
![](/assets/vault/pasted-image-20250709194746.webp)
#### Multi-AZ Deployment
![](/assets/vault/pasted-image-20250709194811.webp)
#### RDS & Aurora MySQL Migrations
![](/assets/vault/pasted-image-20250709195022.webp)
#### RDS & Aurora PostgreSQL Migrations
![](/assets/vault/pasted-image-20250709195121.webp)
### On-premise strategy with AWS
![](/assets/vault/pasted-image-20250709195411.webp)
### AWS Backup
- Fully managed central backup management and automation across AWS services
- No need for custom scripts
![](/assets/vault/pasted-image-20250709201025.webp)
![](/assets/vault/pasted-image-20250709201039.webp)
#### Vault Lock
Enforce Write-Once-Read-Many state for all the backups that prevent the backups from being deleted. Even root user can't delete backups when enabled.
### Application Discovery Service
- Migration planning tool that gathers information from data center
- Server util data, dependency mapping
- Using Agentless Discovery: VM inventory, configs, performance history
- Agent-Based Discovery: System configs, system performance, running processes, details of network
- Results can be viewed in Migration Hub
### Application Migration Service
- Lift-and-shift migration
- Converts your physical, virtual, cloud-based servers to natively run on AWS
- Minimal downtime, less costs
### Transferring large amounts of data into AWS
![](/assets/vault/pasted-image-20250709203130.webp)
### VMWare Cloud on AWS
![](/assets/vault/pasted-image-20250709203327.webp)
