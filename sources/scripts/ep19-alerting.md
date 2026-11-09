# Episode 19: Alerting

**Length:** 22 to 27 minutes

**Focus:** Site Reliability Engineer (SRE)

**Learning goals:**
- Write a Prometheus alert rule
- Create a Discord webhook
- Route alerts with Alertmanager
- Trigger and resolve an alert
- See the same manifests run on managed Kubernetes (GKE), demo only

**Prerequisites:**
- Episode 18 complete
- A Discord server where you can add a webhook
- The GKE segment is a demo. You can watch it without a Google Cloud account.

## 00:00 Hook

**Say:**
- Dashboards need someone to look at them.
- Alerts come to you.
- Today the app sends a message to Discord when it fails.

**Show:**
Title screen.


## 01:30 How Alerts Work

**Say:**
- Prometheus checks a rule. If it holds for the `for` time, the alert fires.
- Alertmanager groups alerts and sends them to a receiver.

**Show:**
A diagram: rule, Prometheus, Alertmanager, Discord.


## 04:00 Create the Webhook

**Say:**
- Warning: the webhook URL is a secret. Do not show it on screen.

**Show:**
- Discord: Server Settings, Integrations, Webhooks, New Webhook.
- Copy the URL.


## 06:00 Create the Secret

**Show:**

```shell
minikube kubectl -- create secret generic alertmanager-discord -n monitoring --from-literal=webhook_url=<your-webhook-url>
```


## 07:30 Write the Rule

**Show:**
- In `prometheus.yaml`, replace `groups: []` with the `BackendUnavailable` rule.
- Expression: `up{job="backend"} == 0`. For: `1m`.


## 10:00 Write the Receiver

**Show:**
- Set `route.receiver` to `discord`.
- Add the `discord_configs` receiver with `webhook_url_file`.
- Mount the Secret as a volume in the Deployment.


## 12:30 Deploy and Trigger

**Show:**

```shell
git add -A && git commit -m "Add alerting" && git push
minikube kubectl -- rollout restart deployment/prometheus -n monitoring
minikube kubectl -- rollout restart deployment/alertmanager -n monitoring
minikube kubectl -- patch application app -n argocd --type merge -p '{"spec":{"syncPolicy":{"automated":null}}}'
minikube kubectl -- scale deployment/backend -n app --replicas=0
```

**Say:**
- Prometheus and Alertmanager both read their config once, at startup. A synced ConfigMap does not restart the Pod, so restart both by hand after this change.
- Warning: self-heal restores the replica count within seconds, before the alert's one-minute window ever elapses. Pause automated sync first, or the alert never fires.

**Expect:** After about one minute, Discord shows `BackendUnavailable`.

**Show:**

```shell
minikube kubectl -- patch application app -n argocd --type merge -p '{"spec":{"syncPolicy":{"automated":{"prune":true,"selfHeal":true}}}}'
```

**Expect:** Turning automated sync back on restores the replicas. Discord shows the resolved message. If you did not install ArgoCD, scale the Deployment back yourself.

## 16:00 Clean Up

**Show:**

```shell
minikube delete
```

**Expect:** Warning: this deletes the cluster and the database data.

## 17:00 Role Insight: DevOps Engineer

**Say:**
- Good alerts are rare and actionable. Too many alerts teach people to ignore them.
- The on-call engineer decides what pages a person.

## 18:00 Demo Only: The Same App on GKE

**Say:**
- Everything so far ran on Minikube, a single-node cluster on your laptop.
- Production Kubernetes is usually managed. GKE, EKS, and AKS run the control plane for you.
- This part is a demo. It is not required to finish the course. There is nothing to submit.
- These commands are presenter-only. The presenter needs `gcloud` and `kubectl` on the host.
- Warning: this needs a Google Cloud free trial. It creates real billable resources. Set a budget alert before you create anything.

**Show:**
- Google Cloud Console: Billing, then Budgets and alerts. Create a budget with a low amount.

```shell
gcloud container clusters create-auto gke-demo --region us-central1
gcloud container clusters get-credentials gke-demo --region us-central1
gcloud components install kubectl
```

- `kubectl config get-contexts`, switch to the new GKE context.
- Apply the same manifests from Episodes 11 to 15: the Namespace, the Deployments, the Services, the Postgres StatefulSet, the ConfigMaps, and the Secrets.
- Change the frontend Service in `kubernetes/app/02-services.yaml` from `type: NodePort` to `type: LoadBalancer` for this demo. This is the only manifest change.
- Apply the manifests, then run `kubectl get nodes`, `kubectl get pods -n app`, and `kubectl get svc -n app`.
- Open the app through the external IP that GKE assigns to the frontend Service.

**Say:**
- The Deployments, StatefulSet, ConfigMaps, and Secrets do not know which cluster runs them.
- What changes on GKE: a managed control plane, automatic node upgrades, and a Service of type `LoadBalancer` that gets a real external IP. Minikube cannot do that last part without MetalLB. A `NodePort` Service never gets an external IP on GKE.
- What does not change: everything else this course already taught you.

**Show:**

```shell
gcloud container clusters delete gke-demo --region us-central1
```

**Expect:** Cluster deleted. Check the Billing page. It must show no running resources.

## 21:00 Act 3 Review

**Say:**
- The task was: one VM was a single point of failure, and updates, scaling, and monitoring were manual.
- What you did: deployed to Kubernetes, added state, autoscaling, and probes, published images from CI, delivered changes with ArgoCD, and added Prometheus, Grafana, and Alertmanager.
- What you achieved: the app heals itself, scales from 2 to 6 replicas under load, every commit reaches the cluster, and Discord gets an alert when the backend fails.
- Next, the Cybersecurity Engineer pentests the app and finds a SQL injection.

**Show:** Three columns: Task, What you did, What you achieved.

## 23:00 Your Resume After Act 3

**Say:**
- You can now put these skills on your CV.
- Suggested headline: Junior DevOps Engineer (Kubernetes, CI/CD, Observability)
- If you stop here, this is a complete CV for this role.

**Show:**

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Kubernetes (Pods, Deployments, Services) | 11, 12 | Containers & Orchestration | Deployed a three-tier app to Kubernetes with Deployments and Services, and debugged it with `describe`, logs, and events |
| Kubernetes configuration (ConfigMaps, Secrets) | 13 | Containers & Orchestration | Separated configuration and credentials from images with ConfigMaps and Secrets created outside Git |
| Stateful workloads (StatefulSet, PVC) | 14 | Containers & Orchestration | Ran PostgreSQL as a StatefulSet with a dynamically provisioned persistent volume |
| Autoscaling (HPA), resource management | 15 | Containers & Orchestration | Set requests, limits, and probes, and configured a CPU-based HPA that scaled the API from 2 to 6 replicas under load |
| Container registries, multi-arch builds | 16 | CI/CD & Automation | Built and published multi-architecture images to GHCR, tagged by commit SHA, with GitHub Actions |
| GitOps (ArgoCD) | 17 | CI/CD & Automation | Implemented GitOps with ArgoCD so every change reaches the cluster through a Git commit, with automated sync and self-heal |
| Monitoring (Prometheus, Grafana) | 18 | Monitoring & Observability | Instrumented a Flask API, Nginx, and PostgreSQL with Prometheus exporters and built a Grafana dashboard |
| Alerting (Alertmanager) | 19 | Monitoring & Observability | Wrote Prometheus alert rules and routed alerts to Discord with Alertmanager |

## 25:00 CV Skills Unlocked

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Alerting (Alertmanager) | 19 | Monitoring & Observability | Wrote Prometheus alert rules and routed alerts to Discord with Alertmanager |

## 25:30 Common Mistakes

- Committing the webhook URL.
- Rule `for` too short. Alerts flap.
- Secret in the wrong namespace. Alertmanager stays in `ContainerCreating`.
- Testing with Prometheus targets still `UP`. Break something first.
- Leaving the GKE demo cluster running. Delete it right after the demo, not at the end of the recording session.

## Outro

**Say:**
- Act 3 is done. You deployed, scaled, published, delivered, and monitored the app.
- In Act 4, you pentest it. Episode 20 starts with thinking like an attacker.

**Show:** Next episode preview: rules of engagement and the OWASP Top 10.
