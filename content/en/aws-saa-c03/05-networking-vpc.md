# 5. Networking: VPC, Routing, and Hybrid Links

**Goal:** Design a [[networking-vpc|VPC]] that controls traffic in and out, and connect it to on-premises networks.

## IP addressing

- Private IP ranges allowed in a VPC:
  - `10.0.0.0/8`: large networks
  - `172.16.0.0/12`
  - `192.168.0.0/16`: home networks
- A VPC CIDR must not overlap with your other networks.
- Avoid Elastic IPs. Use a DNS name, or a load balancer, in front of a public IP.

| Limit | Value |
|---|---|
| VPCs per region | 5 (soft limit) |
| [[cidr|CIDR]] blocks per VPC | 5 |
| Smallest CIDR | `/28` (16 addresses) |
| Largest CIDR | `/16` (65,536 addresses) |

## Subnets

A subnet is a range inside the VPC CIDR. AWS reserves 5 IP addresses in each subnet. Example for `10.0.0.0/24`:

| Address | Reserved for |
|---|---|
| 10.0.0.0 | Network address |
| 10.0.0.1 | VPC router |
| 10.0.0.2 | Amazon-provided DNS |
| 10.0.0.3 | Future use |
| 10.0.0.255 | Broadcast address |

## Internet access

| Component | Direction | Notes |
|---|---|---|
| Internet gateway | Two-way for public resources | One per VPC. Scales and is highly available. Needs a route such as `0.0.0.0/0` to the gateway. |
| NAT gateway | Private subnets to internet | AWS-managed. See the list below the table. |
| NAT instance (outdated) | Private subnets to internet | EC2 in a public subnet. Disable source/destination check. Not highly available. |
| Egress-only internet gateway | Outbound IPv6 only | Update route tables. |

NAT gateway facts:

- It is resilient within one AZ. Create one per AZ for [[fault-tolerance|fault tolerance]].
- It is billed per hour.
- It needs an internet gateway.
- Bandwidth runs from 5 to 100 Gbps.
- Instances in the same subnet cannot use it.

### Bastion hosts

A bastion host is an EC2 instance in a public subnet. Use it to reach private instances:

1. Allow SSH (port 22) to the bastion host from a restricted CIDR.
2. SSH into the bastion host.
3. Allow SSH to private instances only from the bastion security group or its private IP.
4. SSH from the bastion host to the private instances.

## Security groups and NACLs

| | Security group | Network ACL (NACL) |
|---|---|---|
| Level | Instance | Subnet |
| State | Stateful. Remembers inbound connections, so replies go out. | Stateless |

NACL rules:

- Each subnet has one NACL.
- Each rule has a number. The first rule that matches decides allow or deny.
- The last rule (`*`) denies.
- Add rules in steps of 100.
- The default NACL allows all inbound and outbound traffic.

Clients use ephemeral ports for replies. Ranges:

- Linux: 32768 to 60999
- IANA and Windows 10: 49152 to 65535

## VPC peering

- Peering connects two VPCs privately over the AWS network. Cross-Region and cross-account peering work.
- CIDRs must not overlap.
- Peering is not transitive. If A peers with B and B peers with C, A does not reach C.
- Update the route tables in both VPCs.
- You can reference security groups from a peered VPC.

## Transit Gateway

Transit Gateway is a transitive alternative to VPC peering. It connects VPCs, VPNs, and Direct Connect gateways.

- Works across Regions. You can peer transit gateways together.
- Route tables control which VPC reaches which.
- It is the only AWS service for IP multicast.
- Use cases: increase throughput, and share Direct Connect across accounts.

## VPC endpoints

Endpoints reach AWS services over a private connection that uses AWS PrivateLink. Traffic does not use the public internet.

| Type | How it works | Services | Cost |
|---|---|---|---|
| Interface | Elastic network interface with a private IP | Most AWS services | Per hour, plus per GB processed |
| Gateway | Target in a route table. No private IP. | [[storage-s3|S3]], DynamoDB | Free |

### VPC Flow Logs

- Flow logs capture IP traffic for a VPC, a subnet, or a network interface.
- They send data to S3, [[management-and-governance-cloudwatch|CloudWatch Logs]], or Data Firehose.
- They also capture traffic from ELB, RDS, and ElastiCache.

## Hybrid connectivity

### Site-to-Site VPN

- [[networking-vpn|Site-to-Site VPN]] creates an encrypted connection over the public internet between a VPC and an on-premises network.
- The virtual private gateway (VGW) is the AWS side. Attach it to the VPC.
- The customer gateway (CGW) is the device or software on your side.
- To ping over the VPN, allow ICMP inbound in the VPC security group.

### AWS Direct Connect

- [[networking-direct-connect|Direct Connect]] provides a dedicated private connection from your network to AWS.
- It is private, but not encrypted. For encryption, combine it with a VPN.
- One connection reaches public resources (such as S3) and private resources (such as EC2).
- It needs a virtual private gateway on the VPC.
- Dedicated connections: 1, 10, or 100 Gbps.
- Hosted connections: 50 Mbps, 500 Mbps, or 10 Gbps. Capacity can be added or removed. Some partners offer 1, 2, 5, or 10 Gbps.
- Lead time: longer than 1 month.
- A Direct Connect gateway links one connection to VPCs in several Regions in the same account.

### IPv6

- All IPv6 addresses in AWS are public.
- Use an egress-only internet gateway for outbound-only IPv6 access.

## Exam tips

- Security groups are stateful and work at the instance level. NACLs are stateless and work at the subnet level.
- NACL rules are checked by number. The first match wins.
- VPC peering is not transitive. Use Transit Gateway for transitive routing.
- Gateway endpoints for S3 and DynamoDB are free.
- Use one NAT gateway per AZ for fault tolerance.
- Direct Connect is not encrypted. Add a VPN for encryption.
- Direct Connect lead times are longer than 1 month.
- Avoid Elastic IPs. Use DNS names.

[Next: DNS and Content Delivery](06-dns-and-content-delivery.md)
