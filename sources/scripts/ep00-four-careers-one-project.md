# Episode 0: Four Careers, One Project

**Length:** 14 to 16 minutes

**Focus:** Overview

**Learning goals:**
- Understand the four tech career roles covered in this course
- See the application you will build
- Learn how the CV skills ledger tracks what you practice
- Know what to expect from Acts 1, 2, 3, and 4

**Prerequisites:** None. This episode is an overview.

## 00:00 Hook

**Say:**
- You are a fresh CS graduate. You have a degree and no job yet.
- You know theory. What does a tech job actually look like?
- This course shows you four careers by letting you do the work of each one.
- One small app. Four different jobs.
- You will build a GitHub portfolio and a real CV by the end.

**Show:** Title screen with course name.

**Expect:** Visual introduction.

## 00:40 The Four Roles

**Say:**
- Every software system needs four kinds of engineers.
- They work together, but each has different responsibilities.

**Show:** Table of four roles with icons or diagrams:

| Role | What they do | Acts |
|---|---|---|
| Software Engineer | Write code, test it, package it | Act 1 |
| Cloud Engineer | Plan infrastructure, build VMs | Act 2 |
| DevOps Engineer | Run systems on Kubernetes, scale apps | Act 3 |
| Cybersecurity Engineer | Pentest the app, fix what you find | Act 4 |

**Expect:** Clear visual showing each role and timeline.

**Say:**
- Think of each act as a new job. A different engineer joins the team in each act.
- Each act starts with a briefing: what the team did before, your task, and what done means.
- Each act ends with a review and a CV checkpoint.
- You can start at any act. Only Episode 1 (setup) is required.

## 02:00 Tour of the App

**Say:**
- The app is a task board.
- Simple interface. Three running parts.
- You will add features, containerize it, deploy it to a Kubernetes cluster, and secure it.

**Show:** Screenshot of the task board UI with three tasks listed.

**Expect:** Clean, simple interface.

**Say:**
- The frontend is a static web page. HTML, CSS, JavaScript.
- The backend is a Python REST API.
- The database stores tasks in PostgreSQL.

**Show:** Diagram with three boxes (Frontend, Backend, Database) and arrows showing communication.

**Expect:** Clear architecture diagram.

**Say:**
- Let me show you each endpoint the backend has.

**Show:** Table or screen capture of API endpoints:

```
GET  /healthz              - Process is alive
GET  /readyz               - Database is reachable
GET  /metrics              - Prometheus metrics
GET  /api/tasks            - List all tasks
POST /api/tasks            - Create a task
PATCH /api/tasks/<id>      - Mark task done or not done
DELETE /api/tasks/<id>     - Delete a task (you will add this)
GET  /api/tasks/search?q=  - Search tasks by title
GET  /api/demo/work        - CPU work for load testing
```

**Expect:** Reference table visible on screen.

## 04:30 Act 1: Software Engineer

**Say:**
- In Act 1, you are a software engineer. You write code.
- You add a DELETE endpoint that the frontend calls to remove a task.
- You write unit tests for your endpoint using mocks, so the test does not need a database.
- You package the app in containers: one for the backend, one for the frontend, one for the database.
- You write a docker-compose.yaml file so one command starts the whole stack.
- You set up a GitHub Actions workflow so tests run on every pull request.

**Show:** Screenshot of deleted task in the UI.

**Show:** Code snippet of the DELETE endpoint.

**Show:** Test code snippet with mock.patch.

**Show:** Terminal output of tests passing.

**Show:** Dockerfile and docker-compose.yaml snippets.

**Show:** GitHub Actions workflow in the browser.

**Expect:** Visual confirmation of each concept.

**Say:**
- By the end of Act 1, you have skills like Git, Docker, Python, Flask, SQL, unit testing, and GitHub Actions. You add them to your CV.

## 06:00 Act 2: Cloud Engineer

**Say:**
- In Act 2, you are a cloud engineer. You build infrastructure.
- You plan the resources you need: CPU, memory, storage, firewall rules.
- You write a cloud-init script that runs when a VM starts, so you do not have to click through a setup wizard.
- You use Ansible to configure the VM idempotently, meaning it is safe to run the same script twice.
- You write Terraform code to describe the infrastructure. Terraform creates and destroys resources.
- First you build on Multipass, a local VM tool on your laptop. Then you do the same on Google Cloud.

**Show:** Infrastructure diagram with a VM, firewall, and database.

**Show:** snippets of cloud-init, Ansible playbook, and Terraform.

**Show:** GCP console with a running VM.

**Expect:** Visual progression from local to cloud.

**Say:**
- Skills: Multipass, cloud-init, Ansible, Terraform, GCP, Linux administration.

## 07:30 Act 3: DevOps Engineer

**Say:**
- In Act 3, you are a DevOps engineer. You run systems at scale.
- You stop the VMs and move to Kubernetes, a container orchestrator.
- You write Kubernetes manifests: Deployments, Services, ConfigMaps, Secrets, StatefulSets.
- You use Minikube, a local Kubernetes cluster on your laptop.
- You set up Prometheus to collect metrics, Grafana to show dashboards, and Alertmanager to send alerts to Discord.
- You use ArgoCD, a GitOps tool. You push a commit, and ArgoCD pulls that commit into the cluster automatically.
- You configure autoscaling: when the app gets busy, Kubernetes spins up more copies.

**Show:** Kubernetes architecture diagram with Deployment, Service, Pod, and StatefulSet.

**Show:** Prometheus scrape targets and Grafana dashboard.

**Show:** ArgoCD Application manifest.

**Show:** HPA scaling up pods in real time.

**Expect:** Complex but clear system architecture.

**Say:**
- Skills: Kubernetes, Minikube, kubectl, YAML, Prometheus, Grafana, ArgoCD, autoscaling.

## 09:00 Act 4: Cybersecurity Engineer

**Say:**
- In Act 4, you are a cybersecurity engineer. You pentest the app, then you defend it.
- You think like an attacker: you read the API, map the attack surface, and find a SQL injection in a search endpoint.
- You exploit it by hand, then automate the attack with sqlmap.
- You switch hats and fix it: a parameterized query and NetworkPolicies.
- You run Semgrep, Trivy, and ZAP so the fix is checked by tools, not just by eye.

**Show:** NetworkPolicy YAML.

**Show:** Semgrep and Trivy output.

**Show:** ZAP findings.

**Expect:** Security-focused visuals.

**Say:**
- Skills: penetration testing, SQL injection, sqlmap, NetworkPolicies, SAST, SCA, DAST, container security.

## 10:00 How the Course Works

**Say:**
- Each act works as a separate job. You can start at any act.
- Each act opens with a briefing: the task, the goal, and "done when".
- Each act ends with a review and a resume checkpoint.
- A solved repository has one folder for each act. If you skip ahead, copy the folder from the act before.
- Your own repository is a fork of the starter repository.

**Show:** The solved repository layout: `act-1-software-engineer/` to `act-4-cybersecurity-engineer/`.

**Expect:** Students know they can skip ahead.

## 11:30 What You Need

**Say:**
- The core path is free. Everything runs on your laptop.
- Kubernetes runs on Minikube. Virtual machines run on Multipass.
- GitHub, GitHub Actions, and GHCR are free for public repositories.
- Episode 10 uses Google Cloud. It needs a free trial account with a payment card. If you have none, watch the episode and skip the hands-on part.
- Every Google Cloud step sets a budget alert first and ends with `terraform destroy`.
- You need macOS or Windows 10/11, and Docker Desktop.

**Show:** A table: Tool, Used for, Cost.

**Expect:** Students know the cost before they start.

## 13:30 The CV Skills Ledger

**Say:**
- After each episode, you mark a skill you practiced in the skills ledger.
- The ledger is a table in your repository.
- In the last episode, you use this table to fill in your CV.
- Your CV grows act by act. Each act ends with a resume checkpoint you can use on its own.

**Show:** Screenshot of the skills ledger table. Columns: Skill, Episode, CV Section, Example bullet.

**Show:** A few example rows like "Docker", "Python, Flask", "Git, GitHub".

**Expect:** Clear tracking system.

**Say:**
- Each skill has an example bullet point you can adapt for your CV.
- By the end, you have 30+ skills documented with proof you used them.

## Outro

**Say:**
- Four roles. Four acts. One app.
- You will have a GitHub project you own, real work samples, and a CV that speaks for itself.
- In the next episode, we set up your laptop with Git, VS Code, Docker, Multipass, and Minikube.
- See you there.

**Show:** Next episode preview: setup tools on macOS and Windows.

**Expect:** Teaser for the next episode.
