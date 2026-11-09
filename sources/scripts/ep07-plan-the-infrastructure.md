# Episode 7: Plan the Infrastructure

**Length:** 27 to 32 minutes

**Focus:** Cloud Architect

**Learning goals:**
- Explain what a Cloud Engineer does
- Explain what the cloud is, and tell IaaS, PaaS, and SaaS apart
- Name a region, a zone, and an instance
- Size a VM from measured data
- Decide which ports to open and to whom
- Read CIDR notation (`/8`, `/16`, `/24`, `/32`) and plan a network with one subnet
- Name the three private address ranges (RFC1918)
- Look up a DNS name with `nslookup`
- Draw an architecture diagram
- Estimate a monthly cost with the GCP pricing calculator

**Prerequisites:**
- Episode 5 complete: `docker compose up` works
- A browser

## 00:00 Hook

**Say:**
- Your app runs on your laptop. Users cannot reach your laptop.
- Someone must decide where it runs, how big the server is, and who can connect.
- That person is the Cloud Engineer.
- Today you plan. You build nothing.

**Show:** Title screen. Laptop on the left, a cloud icon on the right.

## 01:30 Act 2 Briefing

**Say:**
- Welcome to Act 2. You are the new Cloud Engineer.
- Previously, the software team added a delete feature with a test, packaged the app in containers, and added CI. The app starts with `docker compose up`.
- Your task: the app runs only on developer laptops. Nobody else can reach it.
- Your goal: run it on a server that users can reach. Build the server from code. Keep the cost known and the open ports few.
- Done when: cloud-init and Ansible build a VM that runs the app, Terraform builds the same on Google Cloud, and you destroy it afterwards.
- Start here if you want only this role. Copy `act-1-software-engineer/` from the solved repository. You need Docker Desktop and Multipass.

**Show:** A briefing card with four lines: Role, Task, Goal, Done when.

## 03:30 What a Cloud Engineer Does

**Say:**
- You plan servers, networks, and firewalls.
- You write the setup as code.
- You watch the cost.
- You keep the system reachable and patched.
- Job titles: Cloud Engineer, Infrastructure Engineer, Systems Engineer, SRE.

**Show:** The list from `docs/act2-cloud-engineer.md`.

## 05:00 What the Cloud Is

**Say:**
- The cloud is renting someone else's computers over the internet, on demand. You pay for what you use.
- The provider owns data centres full of computers. You rent slices of them through a website called the console.
- Buying a server costs a lot up front and takes days. Renting costs cents per hour and takes about a minute.
- A region is a geographic area with data centres. You pick one near your users.
- A zone is an isolated data centre inside a region.
- An instance is one running VM. An image is the template it starts from.

**Show:** Two-column table: buying your own server, renting from the cloud.

**Say:**
- One question sorts every cloud service: how much do you manage, and how much does the provider manage?

**Show:** Table:

| Model | You manage | Provider manages | Example |
|---|---|---|---|
| IaaS (Infrastructure as a Service) | Operating system, runtime, app | Hardware, network | A Compute Engine VM. This is Act 2. |
| PaaS (Platform as a Service) | Your app and data | Everything else | A managed database |
| SaaS (Software as a Service) | Nothing, you log in and use it | All of it | Gmail, GitHub |

**Say:**
- We start at IaaS. You get the most control and the most work.
- Exercise: sort four items. A bare Ubuntu VM. Gmail. A managed database with no operating system to patch. A Compute Engine instance. Pause.
- Answer: IaaS, SaaS, PaaS, IaaS. Two items share an answer. People expect a VM and a Compute Engine instance to differ. They do not.

## 09:00 Measure the App

**Say:**
- Do not guess the size of a server. Measure.
- Start the stack from Act 1.

**Show:**

```shell
docker compose up -d --build
docker stats --no-stream
```

**Expect:** About 8 MB for the frontend, 50 MB for the backend, 30 MB for the database. About 100 MB in total.

**Say:**
- The idle stack is small. A build needs more memory than a running app.
- We plan for 2 vCPUs and 2 GB.

**Show:**

```shell
docker compose down -v
```

## 12:00 Ports and Firewall

**Say:**
- Every open port is a way in. Open as few as you can.
- A firewall rule says who may connect to which port.

**Show:** Table:

| Port | Used by | Open to |
|---|---|---|
| 22 | SSH | Your IP address only (`/32`) |
| 8080 | Web frontend | Everyone (`0.0.0.0/0`) |
| 8000 and 5432 | Backend and database | Nobody |

**Say:**
- A port is a numbered door on the server. One machine runs many services, one per port.
- Well-known ports: 22 is SSH, 80 is HTTP, 443 is HTTPS. We use 8080 for the web page.
- A firewall rule has three parts: port, protocol (TCP), and source.
- A port with a rule is not open to everyone. The source decides who. A rule with source `10.0.0.0/16` blocks a request from the internet.
- The backend and database talk inside the Docker network. They need no public port.
- This idea is least privilege.

## 14:30 CIDR and Subnets

**Say:**
- A firewall rule needs an address range. CIDR notation writes that range.
- An IPv4 address has 32 bits. The number after the slash says how many bits are fixed. The remaining bits are free for hosts.
- The number of addresses in a range is 2 to the power of (32 minus the number after the slash).

**Show:** Table:

| CIDR | Example | Addresses | Use it for |
|---|---|---|---|
| `/8` | `10.0.0.0/8` | 16,777,216 | A very large private network |
| `/16` | `10.0.0.0/16` | 65,536 | One VPC |
| `/24` | `10.0.1.0/24` | 256 | One subnet |
| `/32` | `203.0.113.7/32` | 1 | One machine, such as your own IP |

**Say:**
- A VPC is your private network in the cloud. A subnet is a slice of it.
- The cloud reserves a few addresses in every subnet, so you get fewer than you count.
- The range `10.0.0.0/8` is private. The internet does not route it.
- `0.0.0.0/0` means every address. Use it only for a public web port.
- Our plan: one VPC `10.0.0.0/16`, one subnet `10.0.1.0/24`, one VM in it.
- The SSH rule uses your IP as `/32`. The web rule uses `0.0.0.0/0`.

**Show:** Exercise. Ask the viewer: how many addresses are in a `/24`? Pause. Answer: 256.

## 17:00 Private Addresses and DNS

**Say:**
- Three address ranges are reserved for private networks. They never appear on the public internet. This is RFC1918.
- Your VPC uses one of them.

**Show:** Table:

| Range | Addresses |
|---|---|
| `10.0.0.0/8` | `10.x.x.x` |
| `172.16.0.0/12` | `172.16.x.x` to `172.31.x.x` |
| `192.168.0.0/16` | `192.168.x.x` |

**Say:**
- Your VM has a private IP inside the VPC. It also needs a public IP so users can reach it from the internet.
- Nobody remembers an IP address. DNS is the internet's phone book. It turns a name into an IP address.
- Look up a name now.

**Show:**

```shell
nslookup github.com
```

**Expect:** One or more IP addresses for `github.com`. The command works on macOS and Windows.

**Say:**
- A domain name points at the public IP of your VM, or at a load balancer in front of it.

## 20:00 Draw the Diagram

**Say:**
- A diagram lets your team check your plan before you build.
- Draw: the internet, the firewall, the VPC, the subnet, the VM, and three containers.
- Mark port 22 and port 8080 on the firewall.
- Write the CIDR range on the VPC and on the subnet.

**Show:** Draw the diagram in a tool of your choice. Save it in `docs/`.

## 22:00 Estimate the Cost

**Say:**
- Cloud bills surprise people. Estimate first.
- Open the Google Cloud pricing calculator.

**Show:**
1. Add Compute Engine.
2. Set 2 vCPUs, 2 GB memory, 20 GB disk.
3. Read the monthly estimate.

**Say:**
- Write the number in your plan. Prices change, so use the calculator, not this video.
- The VM costs money for every hour it runs, even when nobody uses it.

## 24:30 Write the Plan

**Show:** `docs/infrastructure-plan.md` with five sections: parts, size, network (VPC and subnet CIDR), ports, cost. Add one line that states the region and the zone you chose, and the service model (IaaS).

**Expect:** A one-page plan.

## 26:00 Role Insight: Cloud Architect

**Say:**
- Before a build, a Cloud Engineer writes a short design and asks for review.
- A wrong size or an open port found now costs nothing. Found later, it costs an incident.

## 27:00 CV Skills Unlocked

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Capacity planning (CPU, memory, disk) | 7 | Cloud Platforms | Sized a three-tier app from measured memory use before choosing a VM type |
| Cloud cost estimation | 7 | Cloud Platforms | Estimated the monthly cost of a VM with the GCP pricing calculator |
| Cloud service models (IaaS, PaaS, SaaS), regions and zones | 7 | Cloud Platforms | Classified cloud services as IaaS, PaaS, or SaaS and chose a region and zone for a workload |
| Network planning (VPC, subnets, CIDR, firewall rules) | 7 | Networking & Security | Planned a VPC with one subnet and firewall rules by CIDR range, and kept the database private |
| Private address ranges (RFC1918) and DNS | 7 | Networking & Security | Planned a VPC in a private RFC1918 range and traced a DNS name to its public IP with `nslookup` |
| Architecture diagramming | 7 | Cloud Platforms | Drew an architecture diagram for team review |

## 27:30 Common Mistakes

- Sizing from a guess. Measure with `docker stats`.
- Opening port 5432 to the internet. Databases stay private.
- Opening SSH to everyone. Allow your IP only.
- Forgetting the disk in the cost estimate.
- Mixing up `/24` and `/32`. A `/24` is 256 addresses. A `/32` is one address.
- Using `0.0.0.0/0` for SSH. That opens SSH to everyone.
- Picking a public address range for the VPC. Use `10.0.0.0/8`, `172.16.0.0/12`, or `192.168.0.0/16`.
- Thinking an open port means everyone can reach it. The source range decides.

## Outro

**Say:**
- You have a plan.
- In Episode 8, you create your first VM.
- See you there.

**Show:** Next episode preview: a Multipass VM and SSH.
