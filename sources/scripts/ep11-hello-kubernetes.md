# Episode 11: Hello, Kubernetes

**Length:** 22 to 26 minutes

**Focus:** Platform Engineer

**Learning goals:**
- Explain what Kubernetes does and why one VM is not enough
- Explain desired state and the control loop
- Start Minikube with Calico
- Create a Namespace, a Pod, and a Deployment
- Explain why a Deployment replaces a bare Pod

**Prerequisites:**
- Episode 10 complete
- Multipass VMs stopped: `multipass stop --all` (Minikube needs the memory)
- Docker Desktop running in Linux-container mode

## 00:00 Hook

**Say:**
- Last episode ended with four limits of one VM.
- Kubernetes fixes them: it restarts failed apps, scales them, and updates them without downtime.
- Today we run the first workloads.

**Show:**
Title screen, then the four limits from Episode 10.


## 01:30 Act 3 Briefing

**Say:**
- Welcome to Act 3. You are the new DevOps Engineer.
- Previously, the software team delivered tested container images. The cloud team ran them on one VM, built with Ansible and Terraform.
- That VM has four limits: one point of failure, resizing by hand, a playbook run for each update, and manual rollbacks.
- Your task: move the app from one VM to Kubernetes, and make delivery and monitoring automatic.
- Your goal: deploy to Minikube, scale on load, publish images from CI, deliver changes with Git, and alert on failures.
- Done when: the app scales from 2 to 6 replicas under load, ArgoCD syncs it from Git, Grafana shows a dashboard, and Discord receives an alert.
- Start here if you want only this role. Copy `act-2-cloud-engineer/` from the solved repository. You need Docker Desktop and Minikube. You do not need Multipass or GCP.

**Show:** A briefing card with four lines: Role, Task, Goal, Done when.

## 03:30 Desired State

**Say:**
- You do not tell Kubernetes the steps. You declare the desired state: "run 3 copies of this image."
- Kubernetes runs a loop forever. It compares what runs with what you asked for. It fixes any difference.
- This is a thermostat. You set the temperature once. The thermostat keeps correcting.
- Self-healing is this loop at work. A crashed container is replaced by the loop, not by a script you wrote.

**Show:**

```text
loop forever:
  reality = what runs now
  desired = what you declared
  if reality != desired: fix it
```

## 05:00 Cluster Concepts

**Say:**
- A cluster is a set of machines that run containers.
- The control plane decides. The nodes run the Pods.
- A Pod is one or more containers that run together.
- Minikube makes a one-node cluster on your laptop.

**Show:**
A diagram: control plane, node, Pod.


## 07:00 Start Minikube

**Say:**
- Calico is the network plugin. It enforces NetworkPolicies in Act 4.
- Warning: on Windows, run Minikube from PowerShell, not WSL.

**Show:**

```shell
minikube start --driver=docker --cni=calico --cpus=6 --memory=6144
minikube addons enable metrics-server
minikube kubectl -- get nodes
```

**Expect:** One node with status `Ready`. The first start takes a few minutes.

## 10:00 Namespace

**Say:**
- A Namespace groups resources. We use `app`, `monitoring`, and `argocd`.

**Show:**

```shell
minikube kubectl -- apply -f kubernetes/app/namespace.yaml
minikube kubectl -- get namespaces
```

**Expect:** Namespace `app` is `Active`.

## 12:00 A Bare Pod

**Say:**
- We write a Pod for the frontend image. One container, one port.

**Show:**
- Write `pod.yaml` with `apiVersion`, `kind`, `metadata`, and `spec`.
- Apply it in the `app` namespace.
- Run `kubectl get pods -n app -w`.

**Say:**
- You can also create a Pod in one line, with no file: `kubectl run frontend --image=<image> -n app`. This is the imperative way.
- Imperative commands are fast for a test. A YAML file is better for real work, because Git stores it and ArgoCD applies it in Episode 17.

**Expect:** The Pod reaches `Running`.

## 15:00 Delete the Pod

**Say:**
- Delete the Pod. Nothing brings it back.
- This is the problem a Deployment solves.

**Show:**

```shell
minikube kubectl -- delete pod frontend -n app
minikube kubectl -- get pods -n app
```

**Expect:** No Pods.

## 16:30 Deployment

**Say:**
- A Deployment keeps a set number of Pod copies running.
- It uses a label selector to find its Pods.
- It handles rolling updates.

**Show:**
- Write the frontend Deployment in `kubernetes/app/04-deployments.yaml`.
- Apply the file.
- Delete one Pod.
- Change `replicas` to 3 in the file.
- Apply the file again.
- Keep the value in Git. Episode 17 uses it for the self-heal demo.

**Expect:** The Deployment creates a new Pod after each delete. Three Pods run after the change.

## 20:00 Local Images

**Say:**
- Minikube cannot see your local Docker images. Load them first.

**Show:**

```shell
docker build -t tutorial-frontend:local ./frontend
minikube image load tutorial-frontend:local
```

**Expect:** `ErrImagePull` goes away once the image is loaded.

## 22:00 Role Insight: Platform Engineer

**Say:**
- A DevOps Engineer rarely creates a bare Pod. The team owns Deployments.
- The first debugging question is always: what does the cluster say? Next episode covers the tools for that.

## 23:00 CV Skills Unlocked

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Kubernetes (Pods, Deployments, Services) | 11, 12 | Containers & Orchestration | Deployed a three-tier app to Kubernetes with Deployments and Services, and debugged it with `describe`, logs, and events |
| Desired state and self-healing | 11 | Containers & Orchestration | Explained the Kubernetes control loop and showed a Deployment replacing a deleted Pod |
| Imperative and declarative `kubectl` | 11, 12 | Containers & Orchestration | Used `kubectl run`, `create`, and `expose` for quick tests and YAML manifests for real work |

## 23:30 Common Mistakes

- Starting Minikube without enough memory. Use the Docker Desktop settings.
- Using the `latest` tag. Kubernetes then pulls every time. Use `:local` or a SHA.
- Forgetting `-n app`. The command then looks in the `default` namespace.
- Leaving the Multipass VMs running.
- Treating a bare Pod as safe. Nothing restarts it.

## Outro

**Say:**
- You have a cluster and a Deployment, but nothing can reach it.
- In Episode 12, you add Services and learn to troubleshoot.

**Show:** Next episode preview: Services and `kubectl describe`.
