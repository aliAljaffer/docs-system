# Episode 10: Now in the Cloud

**Length:** 26 to 31 minutes

**Focus:** Cloud Engineer

**Learning goals:**
- Create a budget alert before any resource
- Describe a VM and a firewall in Terraform
- Run `plan`, `apply`, and `destroy`
- Reuse the Ansible playbook on a cloud VM
- Explain the limits of one VM
- Recognize a load balancer, a reverse proxy, and a CDN

**Prerequisites:**
- Episode 9 complete
- A Google Cloud free trial account (viewers without one watch only)
- Read `docs/costs-and-free-options.md`

## 00:00 Hook

**Say:**
- A cloud VM is the same as your Multipass VM. Someone else owns the hardware.
- Today we create one with code.
- Warning: cloud resources cost money while they run. We set an alert first and destroy everything at the end.

**Show:** Title screen.

## 01:30 Budget Alert First

**Say:**
- A budget alert sends an email when spending passes a limit.
- It does not stop the spending. You still destroy resources at the end.

**Show:**
1. Create a Google Cloud project. Note the project ID.
2. Open Billing, then Budgets and alerts.
3. Create a budget with a low amount, for example 5 USD.

## 04:00 Sign In

**Show:**

```shell
docker compose -f tools/compose.yaml run --rm gcloud gcloud auth application-default login
docker compose -f tools/compose.yaml run --rm gcloud gcloud services enable compute.googleapis.com --project <project-id>
```

**Expect:** A browser window opens. Then a success message.

## 06:00 What Terraform Does

**Say:**
- You write the state you want in `.tf` files.
- `plan` shows what will change. `apply` makes the change. `destroy` removes it.
- Terraform keeps a state file. It lists what Terraform created.

**Show:** `infra/terraform/gcp/versions.tf`: the Google provider.

## 08:00 Write the Resources

**Show and explain each file:**

- `variables.tf`: project ID, region, zone, machine type, SSH public key, your IP in CIDR form.
- `main.tf`:
  - a network
  - a firewall rule for port 22, from your IP only
  - a firewall rule for port 8080
  - a Compute Engine VM with Ubuntu 24.04, 20 GB disk, and a public IP
- The reference network uses auto mode. It does not create the Episode 7 subnet. Add a `google_compute_subnetwork` resource if you want the exact plan.
- `outputs.tf`: the VM IP and the app URL.

**Say:**
- These rules match the plan from Episode 7.
- The ports are the same ones UFW opens on the VM.
- Tags connect the firewall rules to the VM.

**Show:** `terraform.tfvars` with your values.

**Say:**
- This file holds your project ID and your IP. It is in `.gitignore`. Never commit it.

## 13:00 Plan and Apply

**Show:**

```shell
docker compose -f tools/compose.yaml run --rm terraform init
docker compose -f tools/compose.yaml run --rm terraform validate
docker compose -f tools/compose.yaml run --rm terraform plan
docker compose -f tools/compose.yaml run --rm terraform apply
```

**Expect:** The plan lists four resources to add. Apply asks for `yes`. The output shows the IP and the URL.

## 16:00 Run the Same Playbook

**Say:**
- Only the IP address changes.

**Show:**
1. Put the VM IP in `inventory.ini`. Set `ansible_user=student`.
2. Run the playbook from Episode 9.
3. Open the app URL.

**Expect:** The task board runs on Google Cloud. If SSH fails, wait one minute. The VM needs time to boot.

## 19:00 Destroy

**Say:**
- We are done. Remove everything.

**Show:**

```shell
docker compose -f tools/compose.yaml run --rm terraform destroy
```

**Expect:** Four resources destroyed. Open the Billing page and the Compute Engine page. Both must show nothing running.

## 20:30 The Limits of One VM

**Say:**
- If the VM fails, the app is down. One point of failure.
- If traffic grows, you resize by hand.
- Each update needs a playbook run.
- Rollbacks are manual.
- Act 3 uses Kubernetes to solve these problems.

**Show:** List of four limits.

## 22:00 Words to Recognize

**Say:**
- Three ideas appear when an app grows past one VM. You do not build them in this course. You must recognize them.
- A load balancer sits in front of many servers. It spreads traffic across them, so no server is overwhelmed. It also skips a server that is down. On Google Cloud it is Cloud Load Balancing.
- A reverse proxy forwards requests to another server. Our frontend Nginx already does this. It forwards `/api` to the backend.
- A CDN (Content Delivery Network) keeps copies of your files in cities around the world. Users load them from a nearby city. On Google Cloud it is Cloud CDN.
- In Act 3, a Kubernetes Service does the load-balancing job for Pods.

**Show:** Diagram: users, load balancer, three VMs. Next to it, the Nginx `proxy_pass` line from `frontend/nginx.conf`.

## 23:30 Role Insight: Cloud Engineer

**Say:**
- A Cloud Engineer reviews `terraform plan` the way a Software Engineer reviews a pull request.
- Cost control is part of the job. Unused resources are waste.

## 24:30 Act 2 Review

**Say:**
- The task was: the app ran only on laptops.
- What you did: planned size, ports, and cost, built a VM with cloud-init and Ansible, then built the same on Google Cloud with Terraform and destroyed it.
- What you achieved: a server you can rebuild from code. A second playbook run changes nothing. Only the needed ports are open. No resources are left running.
- Next, the DevOps Engineer fixes the limits of one VM.

**Show:** Three columns: Task, What you did, What you achieved.

## 26:30 Your Resume After Act 2

**Say:**
- You can now put these skills on your CV.
- Suggested headline: Junior Software Engineer with Cloud and Infrastructure as Code skills
- If you stop here, this is a complete CV for this role.

**Show:**

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Capacity planning, cost estimation | 7 | Cloud & Infrastructure | Sized a three-tier app from measured memory use and estimated its monthly cost with the GCP pricing calculator |
| Linux administration, SSH | 8 | Cloud & Infrastructure | Provisioned Ubuntu VMs with cloud-init and key-only SSH access |
| Ansible | 9 | Cloud & Infrastructure | Wrote an idempotent Ansible playbook that installs Docker, sets the firewall, and deploys a Compose stack |
| Firewalls (UFW, VPC rules) | 9, 10 | Cloud & Infrastructure | Closed all ports except SSH and HTTP with UFW and GCP firewall rules |
| Terraform, Google Cloud | 10 | Cloud & Infrastructure | Created a Compute Engine VM and firewall rules with Terraform and destroyed them after use |
| Cloud cost control | 10 | Cloud & Infrastructure | Set budget alerts and removed resources with `terraform destroy` to stay within the free trial |
| Load balancers, reverse proxies, CDNs (concepts) | 10 | Cloud Platforms | Explained how a load balancer, a reverse proxy, and a CDN remove the single point of failure and speed up delivery |

## 28:30 CV Skills Unlocked

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Terraform, Google Cloud | 10 | Cloud & Infrastructure | Created a Compute Engine VM and firewall rules with Terraform and destroyed them after use |
| Cloud cost control | 10 | Cloud & Infrastructure | Set budget alerts and removed resources with `terraform destroy` to stay within the free trial |
| Load balancers, reverse proxies, CDNs (concepts) | 10 | Cloud Platforms | Explained how a load balancer, a reverse proxy, and a CDN remove the single point of failure and speed up delivery |

## 29:00 Common Mistakes

- Creating resources before the budget alert.
- Forgetting `destroy`. The VM keeps billing.
- Committing `terraform.tfvars` or the state file.
- Using `0.0.0.0/0` for SSH. Use your IP.
- Wrong IP in the CIDR. Use the form `203.0.113.7/32`.
- Skipping the Compute Engine API step.
- Windows: not setting `$env:HOME`. The container cannot find your gcloud login.

## Outro

**Say:**
- Act 2 is done. You planned, built, configured, and destroyed infrastructure.
- Before Act 3, delete the Multipass VM. Minikube needs the memory.
- In Episode 11, you start with Kubernetes.

**Show:** Next episode preview: Minikube and your first Pod.
