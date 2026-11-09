# Episode 13: Configuration

**Length:** 15 to 20 minutes

**Focus:** Platform Engineer

**Learning goals:**
- Move settings out of the image into a ConfigMap
- Create a Secret from the command line
- Explain why base64 is not encryption
- Explain why Secrets stay out of Git

**Prerequisites:**
- Episode 12 complete

## 00:00 Hook

**Say:**
- The same image must run in every environment.
- Only the configuration changes.
- Today we separate the two.

**Show:**
Title screen.


## 01:30 ConfigMap

**Say:**
- A ConfigMap holds plain settings: host, port, database name.

**Show:**
Write `01-configmap.yaml` with `DB_HOST`, `DB_PORT`, `DB_NAME`, and `POSTGRES_DB`.


## 04:00 Use It in the Backend

**Say:**
- `envFrom` loads every key as an environment variable.
- `configMapKeyRef` loads one key.

**Show:**
Add `envFrom` with `configMapRef` to the backend container.


## 06:30 Secret

**Say:**
- A Secret holds the database username and password.
- Warning: never write a password in a manifest that goes to Git.

**Show:**

```shell
minikube kubectl -- create secret generic app-db -n app --from-literal=username=tutorial --from-literal=password=<choose-a-password>
minikube kubectl -- get secret app-db -n app -o yaml
```

**Expect:** The values show as base64 text.

## 09:30 Base64 Is Not Encryption

**Show:**

```shell
echo <value> | base64 --decode
```

**Expect:** The password appears in plain text.

## 11:00 Who Can Read a Secret

**Say:**
- Anyone with read access to the Secret reads the password.
- Kubernetes stores Secrets unencrypted by default. Real clusters add encryption at rest and access rules.


## 13:00 Use the Secret

**Say:**
- `secretKeyRef` loads one key from a Secret.

**Show:**
Add `DB_USER` and `DB_PASSWORD` to the backend from `app-db`.


## 15:00 Why Secrets Stay Out of Git

**Say:**
- Git keeps history. A pushed password stays in the history after you delete it.
- ArgoCD syncs from Git, so we create Secrets on the command line.
- Teams use tools such as Sealed Secrets or an external secrets manager. We keep it simple.


## 17:00 Role Insight: Platform Engineer

**Say:**
- Rotating a leaked secret is expensive. Prevention is cheap.
- Teams scan repositories for committed secrets. You do this in Act 4.

## 18:00 CV Skills Unlocked

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Kubernetes configuration (ConfigMaps, Secrets) | 13 | Containers & Orchestration | Separated configuration and credentials from images with ConfigMaps and Secrets created outside Git |

## 18:30 Common Mistakes

- Committing a Secret manifest with real values.
- Creating the Secret in the wrong namespace. The Pod then shows `CreateContainerConfigError`.
- Changing a ConfigMap and expecting a running Pod to update. Restart the Deployment.
- Thinking base64 protects the value.

## Outro

**Say:**
- The backend can read its settings, but the database does not exist yet.
- In Episode 14, you run PostgreSQL with a StatefulSet.

**Show:** Next episode preview: State and storage.
