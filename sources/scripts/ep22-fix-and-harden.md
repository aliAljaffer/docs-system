# Episode 22: Fix and Harden

**Length:** 14 to 16 minutes

**Focus:** Security Engineer (defensive)

**Learning goals:**
- Fix a SQL injection with a parameterized query
- Isolate tiers with default-deny NetworkPolicies

**Prerequisites:**
- Episode 21 complete
- A second, free Minikube profile for the policy check later in this episode

## 00:00 Hook

**Say:**
- Last episode you broke it. Today you fix it, then make sure a compromised Pod cannot just walk over to the database.

**Show:** Title screen.

## 01:00 Fix the Query

**Say:**
- The fix is one change: pass `q` as a parameter, the same way every other endpoint already does.

**Show:**

```python
tasks = connection.execute(
    "SELECT id, title, done FROM tasks WHERE title LIKE %s ORDER BY id DESC",
    (f"%{term}%",),
).fetchall()
```

**Say:**
- psycopg sends the query text and the value separately. The database never treats the value as part of the SQL.

**Expect:** Students see the fix is small: one query, two lines.

## 03:30 Verify the Fix

**Show:**

```shell
curl -G http://localhost:8000/api/tasks/search --data-urlencode "q=nonexistent' OR '1'='1' --"

minikube kubectl -- run sqlmap-verify -n app --image=tools-sqlmap:local --image-pull-policy=Never --labels=app.kubernetes.io/name=scanner --restart=Never -- \
  -u "http://backend.app.svc.cluster.local:8000/api/tasks/search?q=test" --batch --level=2 --risk=1
minikube kubectl -- logs sqlmap-verify -n app
minikube kubectl -- delete pod sqlmap-verify -n app
```

**Expect:** The curl payload now returns an empty list. `sqlmap` reports the parameter is not injectable.

**Say:**
- Do not run `sqlmap` from a laptop container against the port-forward. `kubectl port-forward` listens on `127.0.0.1` only. `host.docker.internal` cannot reach it. Run the scan as a Pod. Use the same Pod command as Episode 21.

## 06:00 NetworkPolicies

**Say:**
- Right now, every Pod in `app` can reach every other Pod. A compromised frontend could talk to the database directly.
- Default-deny first, then add only the paths the app needs.

**Show:**
- Write `kubernetes/app/07-networkpolicy.yaml`. Start with a default-deny policy for all ingress and egress in `app`.
- Add three allow rules to the same file:
  - The frontend accepts ingress from anywhere.
  - The backend accepts ingress from Pods labeled `app.kubernetes.io/name: frontend`.
  - The backend accepts ingress from Pods labeled `app.kubernetes.io/name: scanner`.
  - The database accepts ingress from Pods labeled `app.kubernetes.io/name: backend`.
- Use the labels in `04-deployments.yaml` and `03-postgres.yaml`. A label such as `app: frontend` matches no Pod.
- Add a DNS egress rule. Allow UDP and TCP port 53 to `kube-system`.

```shell
minikube kubectl -- apply -n app -f kubernetes/app/07-networkpolicy.yaml
```

**Expect:** The frontend still answers in the browser. DNS lookups inside Pods still work.

## 10:00 Verify on a Second Profile

**Say:**
- Prove the default-deny rule with a Pod that has no allow rule. Use a throwaway cluster. Do not disturb the cluster you record on.
- The second profile needs the same CPU and memory as the first. On an 8 GB laptop, stop the main profile first. Run `minikube stop`. Start `act4-check`. Start the main profile again after the check.

**Show:**

```shell
minikube start -p act4-check --driver=docker --cni=calico --cpus=6 --memory=6144
minikube kubectl -p act4-check -- apply -f kubernetes/app
minikube kubectl -p act4-check -- run probe --image=busybox -n app --rm -it --restart=Never \
  -- wget -qO- --timeout=2 postgres.app.svc.cluster.local:5432
```

**Expect:** The probe times out. A Pod with no explicit allow rule cannot reach the database.

```shell
minikube delete -p act4-check
```

## 13:00 Role Insight: Security Engineer (defensive)

**Say:**
- Defense in depth: the parameterized query closes this bug. Network segmentation limits the next one you have not found yet.
- Least privilege is not paranoia. It is the default assumption that something, eventually, gets compromised.

## 14:00 CV Skills Unlocked

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Secure coding (parameterized queries) | 22 | Programming & Scripting | Fixed a SQL injection with parameterized queries and verified the fix |
| Network segmentation (NetworkPolicies) | 22 | Networking & Security | Isolated tiers with default-deny NetworkPolicies and explicit allow rules |

## 14:30 Common Mistakes

- Forgetting the DNS egress rule. Default-deny blocks `kube-dns` too, and lookups fail everywhere.
- Testing the default-deny rule on the cluster you record on. Use a second profile and delete it after.

## Outro

**Say:**
- The query is fixed and the network is segmented. Next episode proves it with tools instead of by hand.
- In Episode 23, Semgrep, Trivy, and ZAP each check a different layer.

**Show:** Next episode preview: SAST, SCA, and DAST scans.
