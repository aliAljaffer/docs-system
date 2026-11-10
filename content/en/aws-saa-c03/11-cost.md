# 11. Cost

**Goal:** Know the price facts for the services in this course.

## Price facts

| Service | Price fact |
|---|---|
| [[networking-route53|Route 53]] hosted zone | $0.50 per month for each hosted zone |
| Route 53 Alias record | Free |
| NAT gateway | Billed per hour. Each AZ needs its own gateway for [[fault-tolerance|fault tolerance]]. |
| [[networking-vpc|VPC]] interface endpoint | Per hour, plus per GB processed |
| VPC gateway endpoint ([[storage-s3|S3]], DynamoDB) | Free |
| [[security-shield|Shield]] Advanced | $3k per month |
| [[management-and-governance-config|AWS Config]] | $0.003 per config item per region. $0.001 per rule evaluation per region. |
| [[analytics-athena|Athena]] | $5 per TB scanned |
| [[autoscaling-groups-and-load-balancers|Network Load Balancer]] and Gateway Load Balancer | Inter-AZ data is charged when cross-zone balancing is enabled |
| ALB and CLB | No charge for inter-AZ data |
| Aurora | Costs 20% more than RDS |
| Stopped RDS database | Storage is still billed |
| RDS replica traffic | Free within a Region. Cross-Region traffic costs money. |
| DynamoDB provisioned | Pay for RCUs and WCUs |
| DynamoDB on-demand | Pay per use. The note calls it expensive. |
| Aurora [[serverless|Serverless]] | Pay per second |
| [[analytics-kinesis|Kinesis]] Data Streams provisioned | Pay per shard per hour |
| Data Firehose | Pay as you go |
| Spot instances | Available for EKS node groups and EMR task nodes |

## Cost levers from this course

- Athena: use columnar formats and compression, so queries scan less data.
- RDS: for a long stop, take a snapshot and restore later. Stopped storage still costs money.
- Athena and [[management-and-governance-cloudtrail|CloudTrail]]: move old logs to S3 and query them only when needed.
- [[networking-direct-connect|Direct Connect]]: one of its use cases is lower cost.
- Shield Standard is free. Use Shield Advanced only for sophisticated attacks.

## Exam tips

- A stopped RDS database still pays for storage.
- Aurora Serverless suits intermittent workloads.
- Athena cost depends on the data scanned.
- Use a gateway endpoint for S3 or DynamoDB. It is free. Interface endpoints charge per hour and per GB.
- Each NAT gateway bills per hour.
- Route 53 Alias records are free. Each hosted zone costs $0.50 per month.

[Next: Exam Strategy](12-exam-strategy.md)
