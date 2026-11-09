# Episode 15: Scale

**Length:** 25 to 30 minutes

**Focus:** Site Reliability Engineer (SRE)

**Learning goals:**
- Set resource requests and limits
- Add readiness and liveness probes
- Scale a Deployment by hand
- Create an HPA
- Tune how fast the HPA scales up and down
- Trigger scaling with a load generator

**Prerequisites:**
- Episode 14 complete
- `metrics-server` enabled

## 00:00 Hook

**Say:**
- One VM could not scale. Kubernetes scales itself.
- But it needs to know how much each Pod needs.
- Today we measure, limit, and scale.

**Show:**
Title screen.


## 02:00 Requests and Limits

**Say:**
- Request: what the scheduler reserves.
- Limit: the most the container may use.
- CPU over the limit is throttled. Memory over the limit kills the container.

**Show:**
The `resources` block in the backend Deployment: `100m` and `96Mi` requests, `500m` and `256Mi` limits.


## 05:30 Probes

**Say:**
- Readiness: is the Pod ready for traffic?
- Liveness: should Kubernetes restart it?
- Startup: wait for slow starts.

**Show:**
The backend probes: `/readyz` and `/healthz`.


## 08:00 Break a Probe

**Show:**
- Change the readiness path to `/nope`. Apply.
- Run `kubectl get pods -n app`.
- Fix the path.

**Expect:** The Pod shows `0/1` ready. It receives no traffic. The Events show the probe failure.

## 10:30 Scale by Hand

**Say:**
- You can set the replica count yourself. You are the thermostat.
- This works, but you must notice the load and type the command each time.
- The HPA does this for you.

**Show:**

```shell
minikube kubectl -- scale deployment/backend -n app --replicas=4
minikube kubectl -- get pods -n app --watch
minikube kubectl -- scale deployment/backend -n app --replicas=2
```

**Expect:** Four backend Pods, then two.

**Say:**
- If an HPA owns the Deployment, it sets the count back. Apply the HPA next.

## 12:30 HPA

**Say:**
- An HPA changes the replica count from a metric.
- It needs CPU requests, because the percentage is of the request.
- We target 50% CPU, from 2 to 6 replicas.
- A one-line form exists: `kubectl autoscale deployment backend --cpu-percent=50 --min=2 --max=6`. We use YAML, so Git can store it.

**Show:**

```shell
minikube kubectl -- apply -n app -f kubernetes/app/05-hpa.yaml
minikube kubectl -- top pods -n app
minikube kubectl -- get hpa -n app
```

**Expect:** The TARGETS column shows a percentage after about one minute. `<unknown>` means the metrics are not ready.

## 14:30 Tune the HPA

**Say:**
- By default, the HPA scales up fast and scales down slowly. It waits 5 minutes before it removes Pods. This stops replicas from going up and down on every small change.
- That is good in production. It is slow to watch in a video.
- The `behavior` block changes this for one HPA. `kubectl autoscale` cannot set it. You write it in YAML.

**Show:** A short form of the `behavior` block in `kubernetes/app/05-hpa.yaml`:

```yaml
behavior:
  scaleUp:
    stabilizationWindowSeconds: 0
    policies:
      - type: Percent
        value: 100
        periodSeconds: 15
  scaleDown:
    stabilizationWindowSeconds: 0
    policies:
      - type: Percent
        value: 100
        periodSeconds: 15
```

**Say:**
- `stabilizationWindowSeconds` is how long the HPA waits before it acts on a lower number.
- `policies` limit how fast the count changes. This one may double the Pods every 15 seconds.
- A production service would use a longer scale-down window.

## 17:00 Load Generator

**Say:**
- The backend has `/api/demo/work`. It does bounded CPU work.
- The load generator calls it in a loop. Tools such as `hey` do the same from the command line.

**Show:**

```shell
minikube kubectl -- create namespace monitoring
minikube kubectl -- apply -n monitoring -f observability/load-generator.yaml
minikube kubectl -- scale deployment/load-generator -n monitoring --replicas=6
minikube kubectl -- get hpa backend -n app --watch
```

**Expect:** CPU rises above 50%. Replicas grow from 2 to 6.

## 21:00 Stop the Load

**Show:**

```shell
minikube kubectl -- scale deployment/load-generator -n monitoring --replicas=0
```

**Expect:** CPU falls. The replicas return to 2. This takes a few minutes.

## 23:00 What the HPA Does Not Do

**Say:**
- The HPA protects the app from load.
- It does not fix slow code. It adds copies.


## 24:30 Role Insight: Site Reliability Engineer (SRE)

**Say:**
- Right-sizing is a daily task. Too high wastes money. Too low causes outages.
- Teams read the dashboards to set the numbers. That is Episode 18.

## 25:30 CV Skills Unlocked

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Autoscaling (HPA), resource management | 15 | Containers & Orchestration | Set requests, limits, and probes, and configured a CPU-based HPA that scaled the API from 2 to 6 replicas under load |
| HPA tuning (scale behavior, stabilization window) | 15 | Containers & Orchestration | Tuned HPA scale-up and scale-down policies to control how fast the API reacts to load |

## 26:00 Common Mistakes

- No CPU request. The HPA shows `<unknown>`.
- Limits set too low. The container restarts with `OOMKilled`.
- A liveness probe that is too strict. Kubernetes restarts healthy Pods.
- Leaving the load generator running.
- Scaling a Deployment by hand while an HPA owns it. The HPA overrides your number.
- Expecting `kubectl autoscale` to set the `behavior` block. Write the HPA in YAML.
- Copying a zero-second scale-down window into production. The count then changes on every spike.

## Outro

**Say:**
- The app scales on your laptop.
- In Episode 16, you publish images so a cluster anywhere can pull them.

**Show:** Next episode preview: Publish images.
