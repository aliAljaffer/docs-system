# 10. Resilience and Disaster Recovery

**Goal:** Plan [[disaster-recovery|disaster recovery]] that meets your recovery targets.

## Key terms

| Term | Meaning | Loss or downtime |
|---|---|---|
| Disaster | An event with a negative impact on [[business-continuity|business continuity]] or finances | - |
| RPO (recovery point objective) | How far back you can recover | Data loss is the time between the recovery point and the disaster. |
| [[rto|RTO]] (recovery time objective) | How long recovery takes | Downtime is the time between the disaster and recovery. |

Minimize both RPO and RTO. Lower values cost more.

## DR strategies

Ordered from lowest cost to highest:

| Strategy | How it works | RPO and RTO |
|---|---|---|
| Backup and restore | Back up data. Restore after a disaster. | High RPO and RTO. Easy and cheap. |
| Pilot light | A small version of the app always runs. Use it for critical core systems. | Lower RPO and RTO than backup and restore. Relatively cheap. |
| Warm standby | The full system runs at minimum size. Scale up after a disaster. | Low RPO and RTO |
| Multi-site (hot site) | Full production scale runs on premises and in AWS. Both sides are active. DNS points to both. | Very low RTO. Very expensive. |
| All AWS multi-Region | Same as multi-site, but both sites run on AWS | Same as multi-site |

## AWS Backup

- Manages and automates backups across AWS services from one place.
- Needs no custom scripts.
- Vault Lock enforces write-once-read-many (WORM) backups. When it is on, no one can delete the backups. Even the root user cannot.

## Database migration

### AWS Database Migration Service (DMS)

[[migration-database-migration-service|DMS]] migrates databases quickly and securely. The source database stays available during the migration.

- Supports homogeneous (same engine) and heterogeneous (different engine) migrations.
- Runs continuous data replication.
- Needs an EC2 instance to run the replication.
- The Schema Conversion Tool (SCT) converts a schema from one engine to another. You do not need SCT for same-engine migrations.

## Server migration

### Application Discovery Service

Application Discovery Service is a migration planning tool. It collects data from your data center.

- Agentless discovery collects VM inventory, configurations, and performance history.
- Agent-based discovery collects system configurations, performance, running processes, and network details.
- View results in Migration Hub.

### Application Migration Service

[[migration-application-migration-service|Application Migration Service]] performs lift-and-shift migrations. It converts physical, virtual, and cloud servers to run natively on AWS. It causes minimal downtime and lower cost.

For large data transfers, see [lesson 4](04-storage.md).

## Exam tips

- RPO is the amount of data you can lose. RTO is the amount of downtime you can accept.
- Pilot light keeps only the core running. Warm standby runs the full system at minimum size.
- Multi-site has the lowest RTO and the highest cost.
- Aurora Global Database promotes a secondary Region in under 1 minute.
- RDS Multi-AZ is for disaster recovery, not scaling.
- AWS Backup Vault Lock prevents anyone from deleting backups while it is on.
- DMS keeps the source database available during migration.
- Use [[networking-route53|Route 53]] failover routing to switch traffic at the DNS level.

[Next: Cost](11-cost.md)
