---
title: Project
category: DevOps
description: You’re the core tech team at a company that migrated a legacy app from
  a single on-prem VM to Azure because the old setup failed on scalability, availability,
  and security.
tags:
- devops
---

<!-- imported from ObsidianVault/studies/DevOps Bootcamp/Week6/Project.md. Edit the source, then run sync.py. -->

# Project

`devops`

You’re the core tech team at a company that migrated a legacy app from a single on-prem VM to Azure because the old setup failed on **scalability, availability, and security**.
Right now, infra provisioning and code deploys are manual. Your job is to **design, automate, and prove** a production-style 3-tier architecture on Azure.
> **Goal:** A working web app exposed only via **Application Gateway (WAF v2)**, with private networking end-to-end, full automation (Terraform + Ansible + GitHub Actions), and actionable monitoring.
## Learning Objectives  -  What you’ll be able to do
1. **Design** a production-style **3-tier** Azure reference architecture (web, API, data) with private networking.
2. **Provision** Azure SQL Database with **Private Endpoint** and **Public network access: Disabled**.
3. **Deploy** a (React, TypeScript, and Vite) frontend and Java-Maven backend Application as **separate services**.
4. **Network & Secure** tiers using VNet/subnets, NSGs, Private Endpoints.
5. **Expose only one public entry** via **Application Gateway (WAF v2)**:
    - `/` → frontend
    - `/api/*` → backend No direct public access to compute or SQL.
6. **Validate & Monitor** with Application Insights + Log Analytics, health probes, metrics, logs, and **alerting**.
7. **Automate Infra** with **Terraform** (remote state, modules, variables, workspaces).
8. **Automate Sonarqube Setup** on a virtual machine using Ansible
9. **Automate Deploy** with **GitHub Actions** (build → test → scan → package → deploy).
10. **Automate Infrastructure Provisioning** with **Github Actions** (terraform init → plan → apply)
## Reference Application (What you’ll deploy)
- **Frontend:** React, TypeScript, and Vite.
- **Backend:** Maven-Java [[rest|REST API]].
- **Database:** Azure SQL Database (single DB is fine) or Postgres Database.
> Keep frontend and backend as **independent deployables** (separate repos or folders, separate pipelines).

Code repository can be accessed from here - [Project 2 Code Repository](https://github.com/saurabhd2106/devops-project2-ih.git)
The code is breifed in the README.md file
## Design Specs
### 1) Accessibility
- Only **Application Gateway public IP / custom domain** is exposed.
- **No direct public access** to VMs/ContainerApps/WebApps, default URLs, or SQL.
- Optional: Bring your own domain + TLS (Key Vault-backed cert for App Gateway).
### 2) Scalability [Optional]
- Start with 1 VM per tier; design for **horizontal scale** (VMSS stretch):
    
    - Autoscale on CPU > 60% (avg 10 min), scale out by 1, max 3.
    - App Gateway backend pool points to the ILB/private IP targets.
### 3) Security (Top Priority)
- Compute **no public IPs**; ingress only from App Gateway subnet (NSGs).
- SQL: **Public network disabled**; only via **Private Endpoint**.
- Key Vault: Private Endpoint + access policies / RBAC.
- System updates via Ansible; lock down SSH to **snet-ops** (runner/Bastion only).
- Use **Managed Identity** on VMs to fetch secrets from Key Vault (optional stretch).
### 4) Monitoring & Observability
- **Application Insights** for both apps (requests, failures, dependencies).
- **Log Analytics** for platform diagnostics (App GW, NSG flow logs optional).
- **Alerts** (at least three):
    - App Gateway **Backend Health** < 100% for 5 min.
    - VM/VMSS/ACA/WebApp **CPU > 70%** for 5 min.
    - SQL **DTU / vCore utilization > 80%** (or failed requests > threshold).
- **Dashboards**: Azure Dashboard snapshot + Kusto queries in README.
## Acceptance Criteria (What “done” means)
1. **Architecture diagram** clearly showing Resource Group, VNet, subnets, App GW, Compute Instances, SQL PE, Private DNS.
2. **No public access** to compute or SQL (verified):
    - VMs have no public IPs; NSGs restrict access.
    - SQL public network disabled; resolved via Private DNS only.
3. **App Gateway routing works**:
    - `/` → frontend (healthy probe)
    - `/api/*` → backend (healthy probe)
4. **Monitoring in place**:
    - App Insights + Log Analytics connected.
    - **≥ 3 Alerts** implemented and demonstrable (screenshots + short note of trigger logic).
5. **Functional test** proves end-to-end:
    - Homepage loads via **gateway** URL.
    - API writes & reads from SQL (show a created record and retrieval).
6. **Automation**:
    - Terraform applies from clean state.
    - Ansible configures machines idempotently.
    - GitHub Actions deploys both services.
    - GitHub Actions executes the terraform workflow

## Deliverables & Submission

1. **Repo(s) structure** (example):
```bash
/infra/terraform/...
/config/ansible/
  ├─ inventories/{dev,prod}
  ├─ roles/{all_required_roles}
/apps/frontend/...
/apps/backend/...
/.github/workflows/{infra.yml,frontend.yml,backend.yml}
/docs/architecture-diagram.png
/docs/runbook.md
/README.md
```
- **README.md** with:
    - Prereqs (Azure CLI, permissions, budgets/quotas)
    - How to provision (Terraform)
    - How to configure (Ansible)
    - How to deploy (GitHub Actions)
    - How to validate (URLs, test steps, sample curl/Postman)
- **Architecture diagram** (PNG/SVG) and **screenshots**:
    - Working app via **App Gateway** URL
    - Azure resources view (RG showing expected services)
    - Alerts/metrics dashboards
- **Short demo script** (bullets) for a 3–5 min walkthrough.
