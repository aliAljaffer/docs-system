# 12. Exam Strategy

**Goal:** Answer scenario questions by ruling out wrong options first.

## Method

1. Find the requirement in the question. Common ones: RPO, RTO, cost, latency, message order, replay, global reach, or [[disaster-recovery|disaster recovery]].
2. Remove options that break a fact in the traps table below.
3. Choose the managed service that meets the requirement.
4. If two options remain, compare them in the lesson tables.

## Common traps

| Wrong idea | Correct fact |
|---|---|
| Read replicas accept writes | Read replicas serve `SELECT` only. |
| Multi-AZ scales reads | Multi-AZ is for disaster recovery. Use read replicas to scale reads. |
| ElastiCache works without code changes | ElastiCache needs heavy application code changes. |
| Use an Elastic IP for a web server | Avoid Elastic IPs. Use a DNS name. |
| Security groups are stateless | Security groups are stateful. NACLs are stateless. |
| [[networking-vpc|VPC]] peering is transitive | Peering is not transitive. Use Transit Gateway. |
| A CNAME works at the root domain | CNAME works only for non-root domains. Use an Alias. |
| Data Firehose feeds Managed Service for Apache Flink | Flink reads Data Streams, not Data Firehose. |
| SQS Standard keeps order | Use FIFO for order. |
| Lazy loading is always fresh | Lazy loading can serve stale data. Write-through does not. |
| [[networking-direct-connect|Direct Connect]] is encrypted | Direct Connect is private, not encrypted. Add a VPN. |
| ACM certificates work on EC2 | You cannot use ACM certificates with EC2. |
| DynamoDB items can be larger than 400 KB | The maximum item size is 400 KB. |
| Multi-site DR is cheap | Multi-site has very low RTO and is very expensive. |
| Global Accelerator caches content | [[networking-cloudfront|CloudFront]] caches content. Global Accelerator routes connections. |
| A simple routing policy uses health checks | A simple routing policy cannot use health checks. |
| CloudWatch records API calls | [[management-and-governance-cloudtrail|CloudTrail]] records API calls. |
| ASG CPU metrics are per instance | Average CPU metrics are computed across the whole ASG. |
| QLDB is decentralized | QLDB has a central authority. Managed Blockchain is decentralized. |

## Exam tips

- Read the full scenario before you choose an option.
- Watch for key words: order, replay, global, latency, disaster recovery, [[serverless|serverless]], and cost.
- Check the RPO and RTO first when a question describes a disaster.
- Use the traps table to remove wrong options quickly.

[Back to the course index](index.md)
