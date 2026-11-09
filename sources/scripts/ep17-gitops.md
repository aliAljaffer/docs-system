# Episode 17: GitOps

**Length:** 20 to 25 minutes

**Focus:** DevOps Engineer

**Learning goals:**
- Explain GitOps
- Install ArgoCD
- Write an ArgoCD Application
- Follow a change from commit to cluster
- Explain self-heal and prune

**Prerequisites:**
- Episode 16 complete
- The fork is public, or ArgoCD has repository credentials
- `monitoring` namespace exists

## 00:00 Hook

**Say:**
- Today you stop running `kubectl apply`.
- Git holds the desired state. A tool in the cluster makes it real.
- This is GitOps.

**Show:**
Title screen.


## 02:00 Push and Pull

**Say:**
- Push: the pipeline connects to the cluster and applies.
- Pull: a tool in the cluster reads Git and applies.
- Pull works with a local cluster. The pipeline needs no access to your laptop.

**Show:**
A diagram of pull-based delivery.


## 05:00 Install ArgoCD

**Show:**

```shell
minikube kubectl -- create namespace argocd
minikube kubectl -- apply --server-side --force-conflicts -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v3.5.1/manifests/install.yaml
minikube kubectl -- get pods -n argocd
```

**Expect:** All Pods `Running` after a few minutes.

## 08:00 Create the Secrets

**Say:**
- Git has no Secrets, so create them first.

**Show:**

```shell
minikube kubectl -- create secret generic app-db -n app --from-literal=username=tutorial --from-literal=password=<choose-a-password>
minikube kubectl -- create secret generic grafana-admin -n monitoring --from-literal=admin-user=admin --from-literal=admin-password=<choose-a-password>
```

**Expect:** If the namespaces do not exist, create them or use `CreateNamespace=true`.

## 10:00 Write the Application

**Say:**
- `source`: repository, revision, path.
- `destination`: cluster and namespace.
- `syncPolicy.automated`: sync on every change.
- `prune`: delete what Git no longer lists.
- `selfHeal`: undo manual changes.

**Show:**
Write `kubernetes/argocd/applications/app.yaml`. Use the path `kubernetes/app`.


## 14:00 Apply

**Show:**

```shell
minikube kubectl -- apply -f kubernetes/argocd/applications/app.yaml
minikube kubectl -- get applications -n argocd
```

**Expect:** The Application becomes `Synced` and `Healthy`.

## 16:00 Open the UI

**Show:**

```shell
minikube kubectl -- port-forward svc/argocd-server -n argocd 8443:443
minikube kubectl -- -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}"
```

**Expect:** Open `https://localhost:8443`. Log in as `admin`. The resource tree shows the app. Decode the password from base64.

## 18:00 Change From Commit to Cluster

**Show:**
- Set `replicas: 3` in the frontend Deployment in `kubernetes/app/04-deployments.yaml`.
- Commit the file.
- Push the commit.
- Watch ArgoCD sync.

**Expect:** New Pods appear without any `kubectl apply`.

## 20:00 Self-heal

**Show:**

```shell
minikube kubectl -- scale deployment/frontend -n app --replicas=1
```

**Expect:** ArgoCD restores the count from Git. The Deployment must declare `replicas` in Git. If Git does not declare it, Git wants one Pod. In that case, there is nothing to restore.

## 22:00 Role Insight: DevOps Engineer

**Say:**
- GitOps gives an audit trail. Every change is a commit.
- Rollback is `git revert`.

## 23:00 CV Skills Unlocked

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| GitOps (ArgoCD) | 17 | CI/CD & Automation | Implemented GitOps with ArgoCD so every change reaches the cluster through a Git commit, with automated sync and self-heal |

## 23:30 Common Mistakes

- ArgoCD cannot read a private repository. Make it public or add credentials.
- Secrets missing. The Pods fail with `CreateContainerConfigError`.
- Changing the cluster by hand and wondering why it reverts.
- The Application `path` points to a folder with no manifests.

## Outro

**Say:**
- The app deploys from Git.
- In Episode 18, you add monitoring.

**Show:** Next episode preview: Observability.
