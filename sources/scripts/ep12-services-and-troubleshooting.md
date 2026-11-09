# Episode 12: Services and Troubleshooting

**Length:** 25 to 30 minutes

**Focus:** Platform Engineer

**Learning goals:**
- Use labels and selectors
- Create ClusterIP, headless, and NodePort Services
- Name the LoadBalancer Service type and say when to use it
- Create a Deployment and a Service from the command line
- Reach the app with `minikube service`
- Debug with `describe`, `logs`, and events

**Prerequisites:**
- Episode 11 complete

## 00:00 Hook

**Say:**
- Pods get new IP addresses every time they restart.
- A Service gives them one stable name.
- Then we break the app on purpose and fix it.

**Show:**
Title screen.


## 02:00 Labels and Annotations

**Say:**
- Labels identify resources. Selectors use them.
- Annotations store extra information. Selectors do not use them.
- We use `app.kubernetes.io/name` and `app.kubernetes.io/part-of`.
- Other tools read annotations. For example, `external-dns` reads an annotation on a Service and creates a DNS record for it.

**Show:**
- Open `04-deployments.yaml`: the labels on the Pod template.
- Run `kubectl get pods -n app --show-labels`.
- Run `kubectl get pods -n app -l app.kubernetes.io/name=backend`.


## 05:00 Service Types

**Say:**
- ClusterIP: reachable inside the cluster only. The default.
- Headless (`clusterIP: None`): gives a DNS name for each Pod. The database uses it in Episode 14.
- NodePort: opens a port on the node. We use it for the frontend.
- LoadBalancer: asks the cloud for a real load balancer in front of the Pods. On Google Cloud it creates one for you. We do not use it on Minikube.

**Show:**
Write `02-services.yaml` with `frontend` (NodePort 30080), `backend`, and `postgres`.


## 09:00 Apply and Check

**Show:**

```shell
minikube kubectl -- apply -n app -f kubernetes/app/02-services.yaml
minikube kubectl -- get services -n app
minikube kubectl -- get endpoints -n app
```

**Expect:** Endpoints list the Pod IPs. An empty list means the selector does not match.

## 11:00 The Command Line Way

**Say:**
- You can create the same objects without YAML.
- Use this for a quick test. Keep the YAML for real work.

**Show:** Table:

| Command | Does |
|---|---|
| `kubectl run` | One bare Pod, no self-healing |
| `kubectl create deployment` | A Deployment: Pods that are replaced if they die |
| `kubectl expose` | A Service: one stable address in front of the Pods |
| `kubectl get`, `describe`, `logs` | Look, look closer, read the output |
| `kubectl delete` | Remove it |

```shell
minikube kubectl -- create deployment scratch --image=nginx -n app
minikube kubectl -- expose deployment scratch --port=80 -n app
minikube kubectl -- get deployment,service scratch -n app
minikube kubectl -- delete deployment,service scratch -n app
```

**Expect:** `kubectl expose` makes a ClusterIP Service. Delete both objects when you finish.

## 14:00 Open the App

**Say:**
- On the Docker driver, the node port is not reachable from the host. `minikube service` opens a tunnel.
- Keep the command running.

**Show:**

```shell
minikube service frontend -n app --url
```

**Expect:** A URL such as `http://127.0.0.1:<port>`. The page loads. The API still fails because there is no database yet.

## 16:00 Break It: Wrong Image

**Show:**
- Change the backend image tag to one that does not exist. Apply.
- Run `kubectl get pods -n app`.
- Run `kubectl describe pod <name> -n app` and read the Events at the bottom.
- Fix the tag.

**Expect:** `ImagePullBackOff`. The Events show `Failed to pull image`.

## 19:00 Break It: Wrong Selector

**Show:**
- Change the Service selector to a label that no Pod has.
- Run `kubectl get endpoints backend -n app`.
- Fix the selector.

**Expect:** `<none>` in ENDPOINTS.

## 21:00 The Debug Loop

**Say:**
- Four commands, in order: `get`, `describe`, `logs`, `events`.

**Show:**

```shell
minikube kubectl -- get pods -n app
minikube kubectl -- describe pod <name> -n app
minikube kubectl -- logs <name> -n app
minikube kubectl -- get events -n app --sort-by=.lastTimestamp
```


## 24:00 Role Insight: Platform Engineer

**Say:**
- Most on-call work starts with these four commands.
- Read the Events first. They name the cause in most cases.

## 25:30 CV Skills Unlocked

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Kubernetes (Pods, Deployments, Services) | 11, 12 | Containers & Orchestration | Deployed a three-tier app to Kubernetes with Deployments and Services, and debugged it with `describe`, logs, and events |
| Service types (ClusterIP, NodePort, LoadBalancer) and annotations | 12 | Containers & Orchestration | Exposed workloads with ClusterIP and NodePort Services, and explained when a LoadBalancer Service replaces them |

## 26:00 Common Mistakes

- Selector and Pod labels do not match. Check the endpoints.
- Reading `logs` of a Pod that never started. Use `describe`.
- Closing the `minikube service` terminal. The URL stops working.
- Editing the live resource with `kubectl edit`. Edit the file and apply.
- Forgetting to delete the scratch Deployment and Service.
- Expecting `LoadBalancer` to work on Minikube. Use NodePort and `minikube service`.

## Outro

**Say:**
- The app has no configuration and no database.
- In Episode 13, you add ConfigMaps and Secrets.

**Show:** Next episode preview: ConfigMaps and Secrets.
