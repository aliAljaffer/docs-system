---
title: Network devices
category: Networking
description: Detection - Alarm or alert
tags:
- networking
- devices
---


# Network devices

`networking` `devices`

This page lists common network and security devices, and the Open Systems Interconnection (OSI) layer each one works at.

[[osi-model|OSI Model]]
## Network devices by layer

| Layer | Device | What it does |
|---|---|---|
| 1 | Analog modem | - |
| 1 | Hub | Does not care where the signal comes from or where it's going, just repeats the signal to the ports |
| 2 | Switch | Few ports, or many, can be simple/complex, only communicates with local network devices. Smarter than a hub. Uses an ASIC chip |
| 2 | Wireless access point (WAP) | Connects wireless to wired, a bridge. Most common: bridges 802.11 wireless to 802.3 ethernet |
| 3 | Multilayer switch (MLS) | Can communicate and pass data to non-local network devices. Expensive |
| 3 | Router | Most common network device. Uses software as opposed to ASIC chip. Can communicate with local and non-local devices. Most cases will have a **router** with less ports than a **switch**. Routes traffic between IP subnets |
## Security devices
### Firewall 
Can be software based, or it's own device. 
Operates on layers 2,3,4, 7 [[osi-model|OSI Model]]
It blocks packets from entering or leaving the network:
1. Via stateless inspection: inspects all packets against a set of rules.
2. Via stateful inspection: Only examines the state of the connection between networks. I.e. when a. connection is made from an internal network to an external one, the firewall will not examine any packets returning from the external connection. As a general rule, external connections are not allowed to be initiated with the internal network.
It is the first line of defense in protecting the internal network from outside threats.
### Intrusion detection system (IDS) vs intrusion prevention system (IPS)

| Attribute | IDS | IPS |
|---|---|---|
| Role | Passive system, monitors when a network breach or attack is occurring | Active system, designed to stop an attack by deploying an action or set of actions |
| Action on attack | Detection: alarm or alert | Prevention: stops the attack |
| Traffic path | Receives a copy of all traffic | All traffic must flow through the IPS, by being between the router (with a firewall) and the destination network segment |
| Evaluation | Signature based, anomaly based, policy based | - |
### Virtual Private Network (VPN) concentrator
Layers: 2,3,7.
...is used by remote hosts to access a private network through an encrypted tunnel through a public network. Once connected, remote hosts are seen as on-premise hosts.

#### Types:

| Type | Connects | Client software |
|---|---|---|
| Site-to-Site VPN | Allows a remote site's network to connect to the main site's network and be seen as a local network segment | - |
| Host-to-site VPN | Remote access VPN allows select remote users to connect to the local network | Remote system uses VPN client software to make the connection |
| Host-to-Host VPN | Allows a secure connection between two systems | Not needed |
#### Protocols

| Protocol | Layer | Use |
|---|---|---|
| Internet Protocol Security (IPsec) | 3 | A protocol suite. Can be used with Authentication Header (AH) protocol. Can be used with Encapsulating Security Payload (ESP): transport mode or tunnel mode. **ISAKMP** |
| Generic Routing Encapsulation (GRE) | - | Tunneling protocol that is capable of encapsulating a wide variety of network layer protocols |
| Point-to-Point Tunneling Protocol (PPTP) | - | Dial up VPN connections |
| Transport Layer Security (TLS) | >= 5 | Cryptographic protocol used to create a secure encrypted connection between two end devices or applications. Commonly used to create a secure encrypted internet session |
| Secure Socket Layer (SSL) | - | Older protocol similar to TLS, commonly used in internet transactions |
## Optimization and performance devices
### Load balancer
content switch/filter.
A network appliance that is used to load balance between multiple hosts that contain the same data - spreading out the workload for greater efficiency.
- Configurable load
- TCP offload
- SSL offload
- Caching
- Prioritization
- Content-switching
	- Balance based on webpage requested (each webpage to specific server)
### Proxy server
- Requests resources on behalf of client machines to protect their identity. 
- Sits between the users and the external network.
- Useful for caching info, access control, URL filtering, content scanning
## Storage 
### NAS vs SAN

| Attribute | Network Attached Storage (NAS) | Storage Area Network (SAN) |
|---|---|---|
| Access | Connect to a shared storage device across network | Looks and feels like a local storage device |
| Access level | File-level. File must be pulled to machine | Block level |
| Efficiency | - | Very efficient reading and writing |
| Bandwidth | - | Requires a lot of bandwidth |
## Network devices
## Access Points
- Not a wireless router!
- A bridge extending a wired network into wireless
### **Wireless LAN controller**
- Centralized management of multiple access points
- Deploy new access points
- Performance and security monitoring
- Configure and deploy changes to all sites
- Report on AP use
- Usually proprietary (belonging to the same manufacturer as APs)
### Networking Functions
- Access to important data
- Remote access
- Traffic management
- Protocol support
### Content Delivery Network (CDN)
- Speeds up the process of data delivery
- Geographically distributed caching servers
### [[networking-vpn|Virtual Private Network]]
- use Concentrator or head-end to manage VPN connections
	- Encryption/decryption access device
	- Often integrated into a firewall
### Quality of Service (QoS)
- Traffic shaping, packet shaping (Prioritization)
- Control by bandwidth usage or data rates
- Routers, switches, firewalls to manage QoS
### Time to Live (TTL)
- How long data is available?
- Can be used to prevent routing loops
### Internet Protocol (IP)
- Loops could cause a packet to live forever
- Each pass through a router is a hop
- Default TTL for Mac/Linux is 64 hops, and 128 hops for Windows
- On average, you need 12-16 hops.
### Domain Name System (DNS)
- Translates hostnames to IP addresses
## Building the Cloud
### Virtual Networks
- Network function virtualization
	- Replace physical network devices with virtual versions
### [[vpc|Virtual Private Cloud]]

| Component | Purpose |
|---|---|
| Transit Gateway | A cloud router that connects multiple VPCs |
| Internet gateway | Allows access over the internet to your application VPC |
| VPC NAT Gateway | Allows outbound communication to the internet, but not necessarily inbound |
| VPC Endpoint | Sets up a direct connection between cloud provider networks |
### Security lists / Access Control Lists
- Adds inbound/outbound rules that apply to all VPCs
### Network security group / Security Group
- Adds more granularity to ACLs
- Rules are specific to devices and network connections
### Cloud service models

| Model | What it is | Who manages | Example |
|---|---|---|---|
| Software as a Service (SaaS) | On-demand software. No local installation. Complete application offering | Central management of data and applications | Google Mail, Office365 |
| Infrastructure as a Service (IaaS) | You want to code your application, but need hardware and resources. Your data is on the cloud | You're still responsible for the management and security | - |
| Platform as a Service (PaaS) | No servers, no software, no maintenance team | Someone else handles the platform, you handle the development. You don't have direct control of the data, people, or infrastructure. Trained security professionals are watching your stuff | SalesForce |

![](/assets/vault/pasted-image-20250521165813.webp)
## Introduction to IP
![](/assets/vault/screenshot-2025-05-21-at-5.52.37-pm.webp)
### TCP vs UDP
Transported inside of **IP**
OSI Layer 4 (Transport)
Multiplexing, the ability to use many different apps at the same time

| Protocol/Feature | TCP                                                                         | UDP                                                          |
| ---------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------ |
| Delivery         | Reliable, recovery from errors, device confirms data delivery, but **SLOW** | Unreliable, no error recovery no reordering of data**FAST**! |
| Connection       | Opens and closes connection                                                 | Connectionless, no formal open or close connections          |
| Flow Control     | The receiver can manage how much data is sent                               | No flow control, sender determines the amount of data sent   |
### List of Ports
#### IPv4 Sockets
- Server IP address, protocol, server application port number
- Client IP address, protocol, client port number
#### Non-ephemeral ports - permanent port numbers
- 0 - 1,023
- usually on a server or a service
#### Ephemeral ports - temporary
- 1024 - 65,535
#### TCP and UDP
- 0 - 65,535
- The two are not the same! TCP 80 $\neq$ UDP 80
**Port numbers are for communication, not security!**
## Common Ports

| Protocol | Port | Notes |
|---|---|---|
| File Transfer Protocol (FTP) | tcp/20 (data transfer), tcp/21 (control) | Transfer files between systems. Auth: User/Pass |
| Secure Shell (SSH) | tcp/22 | Secure remote connection |
| Secure FTP (SFTP) | tcp/22 | Encrypted file transfer |
| Telnet | tcp/23 | Non-encrypted remote connection via console |
| Simple Mail Transfer Protocol (SMTP) | tcp/25 (PLAINTEXT EW), tcp/587 (SMTP using TLS encryption) | Server to server email transfer. For email receiving: IMAP, POP3 |
| Domain Name System (DNS) | udp/53, tcp/53 for large transfers | - |
| Dynamic Host Config. Protocol (DHCP) | udp/67, udp/68 | Automated config. of IP address, subnet mask. Dynamic / pooled: each system is given a lease time. DHCP reservation. Requires DHCP server |
| Trivial File Transfer Protocol (TFTP) | udp/69 | Very simple file transfer. No auth. Useful when starting a system |
| HTTP and HTTPS | tcp/80 (HTTP, PLAINTEXT), tcp/443 (HTTPS, SSL/TLS encrypted) | HyperText Transfer Protocol |
| Network Time Protocol (NTP) | udp/123 | Switches, routers, firewalls, servers, etc sync their time. Automatic updates |
| Simple Network Management Protocol (SNMP) | udp/161, SNMP trap udp/162 | Gather statistics from network devices. Traps carry alerts and notifs from other network devices |
| Lightweight Directory Access Protocol (LDAP) | tcp/389, LDAPS (LDAP + SSL) tcp/636 | Store and retrieve information in a network directory |
| Server Message Block (SMB) | tcp/445 (plaintext) | File sharing, printer sharing. Also called Common Internet File System CIFS. Built-into Windows |
| Syslog | udp/514 | Standard for message logging. Usually used with SIEM |
| Databases (SQL) | tcp/1433 | Microsoft SQL Server MS-SQL |
| Remote Desktop Protocol (RDP) | tcp/3389 | Share a desktop from a remote location |
| Session Initiation Protocol (SIP) | tcp/5060, tcp/5061 | Voice-Over-IP (VOIP) |

### SNMP versions

| Version | Security | Features |
|---|---|---|
| v1 | Plaintext | The original. Structured tables |
| v2 | Plaintext | Data type enhancements, bulk transfers |
| v3 | SECURE | Message integrity, authentication |
## Other Useful Protocols
### Internet Control Message Protocol
Text messaging for network devices to communicate 
### Generic Routing Encapsulation
- The "Tunnel" between two endpoints
