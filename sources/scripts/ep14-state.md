# Episode 14: State

**Length:** 20 to 25 minutes

**Focus:** Platform Engineer

**Learning goals:**
- Explain why a database needs a StatefulSet
- Explain PVC, PV, and StorageClass
- Run PostgreSQL with a volume claim template
- Prove that data survives a Pod restart

**Prerequisites:**
- Episode 13 complete
- The `app-db` Secret exists

## 00:00 Hook

**Say:**
- A Deployment Pod can be replaced at any time. Its files vanish.
- A database must keep its files.
- Today we give PostgreSQL a disk.

**Show:**
Title screen.


## 02:00 Storage Objects

**Say:**
- PVC: a request for storage.
- PV: the storage itself.
- StorageClass: how Kubernetes creates a PV.
- Minikube has a default StorageClass. It creates PVs on demand.

**Show:**
A diagram: Pod, PVC, PV, disk.


## 05:00 StatefulSet

**Say:**
- A StatefulSet gives each Pod a stable name: `postgres-0`.
- It creates one PVC for each Pod from `volumeClaimTemplates`.
- It works with a headless Service.

**Show:**
Write `03-postgres.yaml`: the database container, the `postgres_exporter` sidecar, the probes, and `volumeClaimTemplates` with 1Gi. Use the `tutorial-database:local` image you build below, not the stock `postgres:16-alpine` image. Only your built image has `init.sql` baked in to create the `tasks` table.


## 11:00 Set `PGDATA`

**Say:**
- PostgreSQL needs an empty directory. The volume root has a `lost+found` folder.
- Set `PGDATA` to a subfolder.

**Show:**
The `PGDATA` environment variable: `/var/lib/postgresql/data/pgdata`.


## 13:00 Apply

**Show:**

```shell
docker build -t tutorial-database:local ./database
minikube image load tutorial-database:local
minikube kubectl -- apply -n app -f kubernetes/app/03-postgres.yaml
minikube kubectl -- get pods,pvc -n app
minikube kubectl -- get pv
```

**Expect:** `postgres-0` runs with 2 of 2 containers ready. The PVC is `Bound`. A PV exists.

## 16:00 Use the App

**Show:**
- Open the app with `minikube service frontend -n app --url`.
- Add two tasks.

**Expect:** The tasks appear.

## 18:00 Prove Persistence

**Show:**

```shell
minikube kubectl -- delete pod postgres-0 -n app
minikube kubectl -- get pods -n app -w
```

**Expect:** Kubernetes creates `postgres-0` again. Refresh the app. The tasks remain.

## 20:30 Limits

**Say:**
- Warning: Minikube storage is for learning. `minikube delete` deletes the data.
- Production needs backups and a managed database or an operator. That is out of scope here.


## 22:00 Role Insight: Platform Engineer

**Say:**
- Teams often avoid running databases in Kubernetes. A managed database is simpler to operate.
- Knowing StatefulSets still matters. Many tools use them.

## 23:00 CV Skills Unlocked

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Stateful workloads (StatefulSet, PVC) | 14 | Containers & Orchestration | Ran PostgreSQL as a StatefulSet with a dynamically provisioned persistent volume |

## 23:30 Common Mistakes

- Missing `PGDATA`. PostgreSQL fails with an initdb error.
- Fixing an image error but leaving the old Pod. Delete `postgres-0` so the StatefulSet recreates it.
- Expecting the PVC to be deleted with the StatefulSet. It stays.
- Treating Minikube storage as a backup.

## Outro

**Say:**
- The full app now runs on Kubernetes.
- In Episode 15, you add limits, probes, and autoscaling.

**Show:** Next episode preview: Scale.
