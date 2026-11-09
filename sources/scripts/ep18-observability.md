# Episode 18: Observability

**Length:** 20 to 25 minutes

**Focus:** Site Reliability Engineer (SRE)

**Learning goals:**
- Explain metrics, and the roles of Prometheus and Grafana
- Add scrape targets
- Read exporters
- Use a dashboard to watch the HPA load test

**Prerequisites:**
- Episode 17 complete
- `grafana-admin` Secret exists in `monitoring`

## 00:00 Hook

**Say:**
- You cannot fix what you cannot see.
- Today you watch the app from the inside.

**Show:**
Title screen.


## 01:30 How Metrics Work

**Say:**
- An app exposes numbers at `/metrics`.
- Prometheus pulls them on a schedule and stores them.
- Grafana draws charts from Prometheus.

**Show:**
A diagram: targets, Prometheus, Grafana.


## 04:00 Exporters

**Say:**
- The backend has `/metrics`.
- Nginx and PostgreSQL need a helper container, called an exporter.
- The exporters are sidecars in the same Pod.

**Show:**
Open the manifests: the `nginx-exporter` and `postgres-exporter` containers.


## 07:00 The Starter

**Show:**
- Open `observability/`: Prometheus, Grafana, Alertmanager, the dashboard JSON.
- Open `prometheus.yaml`: `scrape_configs` has only Prometheus itself.


## 09:00 Add Scrape Targets

**Show:**
- Add jobs `backend`, `frontend`, and `postgres`.
- Use the Service DNS names, such as `backend.app.svc.cluster.local:8000`.

**Say:**
- The frontend and postgres Services need the exporter's port listed too, not only the app's own port. Check `02-services.yaml` if a target will not connect.


## 12:00 Deploy

**Show:**

```shell
minikube kubectl -- apply -k observability
minikube kubectl -- rollout restart deployment/prometheus -n monitoring
minikube kubectl -- port-forward svc/prometheus -n monitoring 9090:9090
```

**Say:**
- Prometheus reads its config once, at startup. A ConfigMap change does not restart the Pod, so restart it yourself every time you edit `scrape_configs` or `rules.yml`.

**Expect:** Open `http://localhost:9090/targets`. Every target is `UP`.

## 14:00 PromQL

**Show:**
- Run `up`.
- Run `rate(app_http_requests_total[5m])`.

**Expect:** A graph of request rate.

## 16:00 Grafana

**Show:**

```shell
minikube kubectl -- port-forward svc/grafana -n monitoring 3000:3000
```

**Expect:** Open `http://localhost:3000`. Log in with the Secret. The provisioned dashboard shows five panels: request rate, latency, frontend connections, database connections, and requests by endpoint.

## 18:00 Watch a Load Test

**Show:**

```shell
minikube kubectl -- scale deployment/load-generator -n monitoring --replicas=6
```

**Expect:** Request rate and latency rise. Stop the load afterward.

## 21:00 GitOps for Monitoring

**Say:**
- Add a second ArgoCD Application for `observability`.
- Monitoring now deploys from Git too.

**Show:**
`monitoring.yaml` with path `observability`.


## 22:30 Role Insight: Site Reliability Engineer (SRE)

**Say:**
- Dashboards tell you that something is wrong. Logs and traces tell you why.
- A good dashboard shows traffic, errors, and latency.

## 23:30 CV Skills Unlocked

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Monitoring (Prometheus, Grafana) | 18 | Monitoring & Observability | Instrumented a Flask API, Nginx, and PostgreSQL with Prometheus exporters and built a Grafana dashboard |

## 24:00 Common Mistakes

- A target `DOWN`. Check the Service name and port.
- Wrong namespace in the DNS name.
- Forgetting the `grafana-admin` Secret. Grafana does not start.
- Leaving the load generator on.

## Outro

**Say:**
- You can see the app. Nobody is watching the dashboard at 3 a.m.
- In Episode 19, you add alerts.

**Show:** Next episode preview: Alerting.
