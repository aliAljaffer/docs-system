# 4. Storage: File Systems, Hybrid, and Transfer

**Goal:** Choose a file system, a hybrid storage option, or a data transfer service.

This lesson covers file systems, hybrid storage, and data transfer. For the basics of [[storage-s3|S3]], [[storage-ebs|EBS]], and [[storage-efs|EFS]], see their definition pages.

## Amazon FSx

FSx provides fully managed file systems for high-performance workloads.

| Option | Protocol or fit | Use cases from this course |
|---|---|---|
| FSx for Windows File Server | SMB, NTFS, Active Directory, ACLs, user quotas, Microsoft DFS Namespaces | Windows workloads. Mounts on Linux EC2 too. Can run Multi-AZ. Backed up daily to S3. |
| FSx for Lustre | Parallel, distributed file system | Machine learning, HPC, video processing, financial modeling, electronic design automation |
| FSx for NetApp ONTAP | NFS, SMB, iSCSI | Move ONTAP or NAS workloads to AWS. Snapshots, replication, compression, deduplication. |
| FSx for OpenZFS | NFS | Move ZFS workloads to AWS. Up to 1 million IOPS. |

- FSx for Windows File Server scales to tens of GB/s and millions of IOPS.
- FSx for Lustre scales to hundreds of GB/s. It reads S3 data as a file system and writes results back to S3.
- Clients reach FSx for Windows File Server and FSx for Lustre on premises through a [[networking-vpn|VPN]] or [[networking-direct-connect|Direct Connect]].

### Deployment options

| Option | Replication | Use |
|---|---|---|
| Scratch | Not replicated. High burst (6x faster). | Short-term processing. Optimizes cost. |
| Persistent | Replicated within the same AZ. Failed files are replaced within minutes. | Long-term processing and sensitive data |

## AWS Storage Gateway

[[storage-storage-gateway|Storage Gateway]] connects on-premises data with AWS storage. A hardware appliance option also exists.

| Gateway | Interface | Notes |
|---|---|---|
| File | SMB | Caches the most recently used files. Uses Active Directory for user authentication. |
| Volume | iSCSI block storage | Backed by EBS snapshots. Cached or stored volumes. |
| Tape | Virtual tape library | Backed by S3 and Glacier. |

## AWS Snow Family

- [[migration-aws-snow-family|Snowball]] is a secure, portable device. It moves petabytes of data into and out of AWS.
- Snowball also supports edge computing. It runs EC2 instances or [[compute-lambda|Lambda]] where the data is created.
- Snowcone has the DataSync agent preinstalled. Use it when the network cannot handle a DataSync transfer.

## AWS Transfer Family

- Transfer Family provides FTP, FTPS, and SFTP.
- It is managed, scalable, and highly available.
- It authenticates users with LDAP, Active Directory, [[security-cognito|Cognito]], or Okta.
- Use case: file sharing.

## AWS DataSync

DataSync moves large amounts of data.

- On premises or other clouds to AWS. Requires an agent.
- AWS to AWS, between different storage services.
- Targets: S3 (any storage class), EFS, and FSx.
- Schedule tasks hourly, daily, or weekly.
- Preserves file permissions and metadata.
- One agent task can use 10 Gbps.

## Exam tips

- Choose FSx scratch for temporary, high-burst work. Choose FSx persistent for long-term work and sensitive data.
- FSx for Windows File Server uses SMB and Active Directory. FSx for Lustre suits ML and HPC.
- Use DataSync for large online transfers. Use a Snow device when the network cannot handle the transfer.
- Volume Gateway is backed by EBS snapshots. Tape Gateway is backed by S3 and Glacier.
- File Gateway caches recently used files locally.

[Next: Networking and VPC](05-networking-vpc.md)
