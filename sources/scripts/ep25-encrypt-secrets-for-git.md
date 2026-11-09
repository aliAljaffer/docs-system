# Episode 25: Encrypt Secrets for Git

**Length:** 30 to 35 minutes

**Focus:** DevOps Engineer

**Learning goals:**
- Explain why plain Kubernetes Secrets cannot go in Git, and why that has kept this app's Secrets outside GitOps since Episode 17
- Install the Sealed Secrets controller and fetch its public certificate
- Encrypt a Secret with `kubeseal`, offline, using only the public certificate
- Explain why `kubeseal` can encrypt but never decrypt
- Let ArgoCD manage a Secret for the first time

**Prerequisites:**
- Episode 24 complete
- A Minikube cluster with the app deployed, from Act 3

## 00:00 Hook

**Say:**
- Since Episode 13, every Secret in this app has been created the same way: by hand, on the command line, never committed. That has worked, but it means ArgoCD has never managed your database password, and now it needs to manage a second secret too.
- Today that changes. The secret stays secret; the file goes in Git.

**Show:** Title screen.

## 01:30 Why Plain Secrets Cannot Go in Git

**Say:**
- A Kubernetes Secret only base64-encodes its value. Base64 is not encryption; anyone who can read the file can read the secret. You learned this in Episode 13.
- GitOps wants everything in Git, including Secrets, but committing a base64 string is the same as committing plaintext.
- `app-db` has always been the exception: created once, by hand, kept out of the repo. `app-auth`, the JWT signing key from Episode 24, has the exact same problem.

**Show:** `scripts/ep13-configuration.md`'s warning about base64, for contrast.

## 04:00 Sealed Secrets, the Idea

**Say:**
- A controller runs in the cluster with a private key it never shares. It publishes the matching public key.
- `kubeseal`, a command-line tool, uses only the public key to encrypt a Secret into a `SealedSecret`. Anyone can encrypt. Only the controller, with the private key, can decrypt.
- A `SealedSecret` is safe to commit. Once applied, the controller decrypts it in-cluster into an ordinary Secret, which your Deployments already read from exactly as before.

**Show:** A diagram: your laptop (public key, encrypt only) &rarr; Git &rarr; ArgoCD &rarr; cluster (private key, decrypt).

## 07:00 Install the Controller

**Show:**

```shell
minikube kubectl -- apply -f kubernetes/sealed-secrets/controller.yaml
minikube kubectl -- -n kube-system rollout status deploy/sealed-secrets-controller
```

**Expect:** The controller becomes available. It lives in `kube-system`, alongside Minikube's own components, not in `app`.

## 09:30 Fetch the Public Certificate

**Say:**
- You need the public certificate exactly once per cluster. After that, sealing works completely offline.

**Show:**

```shell
minikube kubectl -- get secret -n kube-system \
  -l sealedsecrets.bitnami.com/sealed-secrets-key \
  -o jsonpath='{.items[0].data.tls\.crt}' | base64 -d > kubernetes/sealed-secrets/pub-cert.pem
```

**Say:**
- This is the public half of the keypair. Committing it is fine; it can only encrypt, never decrypt.
- Compare: `DB_PASSWORD` and `GOOGLE_APPLICATION_CREDENTIALS` needed a live connection to GCP every time you used them in Episode 10. `kubeseal` needs the cluster exactly once, here.

## 12:00 Seal a Secret

**Show:**

```shell
minikube kubectl -- create secret generic app-db -n app \
  --from-literal=username=tutorial --from-literal=password="$(openssl rand -hex 16)" \
  --dry-run=client -o yaml \
  | docker compose -f tools/compose.yaml run --rm -T kubeseal \
      --cert kubernetes/sealed-secrets/pub-cert.pem --format yaml \
  > kubernetes/app/08-sealed-secrets.yaml
```

**Say:**
- Use the same database username as Episode 13. This example uses `tutorial`. A different name creates a role that PostgreSQL does not have.
- `--dry-run=client -o yaml` builds the plaintext Secret manifest. It does not send the Secret to the cluster. The pipe sends it to `kubeseal`. The file is never written on its own.
- `-T` on `docker compose run` turns off the pseudo-terminal. Piped input then reaches the container.

**Expect:** `kubernetes/app/08-sealed-secrets.yaml` contains a `SealedSecret`, with `encryptedData` instead of `data`. Open it; the values are unreadable ciphertext, not base64.

## 16:00 Prove `kubeseal` Cannot Decrypt

**Show:**

```shell
docker compose -f tools/compose.yaml run --rm kubeseal --help | grep -i decrypt
```

**Expect:** Nothing. There is no decrypt flag, on purpose. The only way back to plaintext is applying the `SealedSecret` to the cluster that holds the matching private key.

## 18:00 Seal the Second Secret

**Say:**
- Episode 24 added `JWT_SECRET`, read by the backend the same way as `DB_PASSWORD`. It needs a Secret and a Deployment env var too.

**Show:** `kubernetes/app/04-deployments.yaml`:

```yaml
- name: JWT_SECRET
  valueFrom:
    secretKeyRef:
      name: app-auth
      key: jwt-secret
```

```shell
minikube kubectl -- create secret generic app-auth -n app \
  --from-literal=jwt-secret="$(openssl rand -hex 32)" \
  --dry-run=client -o yaml \
  | docker compose -f tools/compose.yaml run --rm -T kubeseal \
      --cert kubernetes/sealed-secrets/pub-cert.pem --format yaml \
  >> kubernetes/app/08-sealed-secrets.yaml
```

**Expect:** `08-sealed-secrets.yaml` now holds two YAML documents, separated by `---`: `app-db` and `app-auth`.

## 21:00 Apply and Verify

**Show:**

```shell
minikube kubectl -- apply -f kubernetes/app/08-sealed-secrets.yaml
minikube kubectl -- get secrets -n app
minikube kubectl -- get secret app-db -n app -o jsonpath='{.data.password}' | base64 -d
```

**Expect:** Two ordinary Secrets now exist in `app`, created by the controller, not by you directly. The password decodes to the real value you sealed.

## 24:00 Let ArgoCD Manage It

**Say:**
- `kubernetes/argocd/applications/app.yaml` already points at the whole `kubernetes/app` folder. `08-sealed-secrets.yaml` is just another file in it now.

**Show:**

```shell
git add kubernetes/app/08-sealed-secrets.yaml kubernetes/app/04-deployments.yaml kubernetes/sealed-secrets
git commit -m "Seal app-db and app-auth, manage them with ArgoCD"
git push
```

**Expect:** ArgoCD syncs the `SealedSecret` like any other manifest. For the first time, a secret's lifecycle lives in Git, not only on your command-line history.

## 26:30 Role Insight: DevOps Engineer

**Say:**
- GitOps promises one thing: the cluster matches Git. An exception you create for Secrets, "except these, created by hand," is a gap someone eventually forgets to re-apply after rebuilding a cluster.
- Sealed Secrets closes that gap without weakening it: the ciphertext in Git is genuinely useless to anyone without the one cluster's private key.

## 27:30 Act 4 Review

**Say:**
- The task was: a search endpoint built SQL from user input, untested and unfixed, and no part of the app checked who was allowed to change what.
- What you did: found and exploited the SQL injection by hand and with sqlmap, fixed it with a parameterized query, added NetworkPolicies, checked the result with Semgrep, Trivy, and a ZAP baseline scan, added real users and reproduced and fixed an IDOR, then encrypted two secrets for Git with Sealed Secrets.
- What you achieved: the app resists the injection, every workload runs with least privilege, a Pod without an allow rule cannot reach the database, every future commit is checked by the same scans, one user can no longer touch another's data, and every secret this app needs is safe to commit.
- This is the last act. Episode 26 is the finale: your CV.

**Show:** Three columns: Task, What you did, What you achieved.

## 29:30 Your Resume After Act 4

**Say:**
- You can now put these skills on your CV.
- Suggested headline: Junior Cybersecurity Engineer (Penetration Testing and Application Security)
- If you stop here, this is a complete CV for this role.

**Show:**

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Rules of engagement, authorized testing | 20 | Networking & Security | Defined scope and rules of engagement before testing an application |
| OWASP Top 10 | 20 | Networking & Security | Mapped the OWASP Top 10 to a three-tier application |
| API reconnaissance (curl) | 20 | Networking & Security | Enumerated API endpoints and parameters with curl |
| Attack surface mapping (Burp Suite) | 20 | Networking & Security | Mapped an application's attack surface with Burp Suite |
| SQL injection (manual exploitation) | 21 | Networking & Security | Confirmed and exploited a SQL injection by hand |
| Automated exploitation (sqlmap) | 21 | Networking & Security | Automated SQL injection data extraction with sqlmap |
| Secure coding (parameterized queries) | 22 | Programming & Scripting | Fixed a SQL injection with parameterized queries and verified the fix |
| Network segmentation (NetworkPolicies) | 22 | Networking & Security | Isolated tiers with default-deny NetworkPolicies and explicit allow rules |
| SAST (Semgrep) | 23 | Networking & Security | Found a SQL injection pattern in source code with Semgrep |
| SCA, IaC, and secret scanning (Trivy) | 23 | Networking & Security | Scanned images, Dockerfiles, Kubernetes YAML, and Terraform with Trivy |
| DAST (OWASP ZAP) | 23 | Networking & Security | Hardened the Nginx response headers and verified them with an OWASP ZAP baseline scan |
| OWASP A01, Broken Access Control, IDOR | 24 | Networking & Security | Identified and reproduced an Insecure Direct Object Reference end to end |
| Authentication (bcrypt, JWT) | 24 | Programming & Scripting | Implemented registration and login with bcrypt-hashed passwords and signed JWT bearer tokens |
| Authorization (ownership checks) | 24 | Programming & Scripting | Added per-object ownership checks that stopped one authenticated user from modifying another's data |
| Secure error design (404 vs. 403) | 24 | Networking & Security | Chose a response code that fixed an access control bug without creating an object-existence oracle |
| Secrets encryption for GitOps (Sealed Secrets) | 25 | Networking & Security | Encrypted Kubernetes Secrets with Sealed Secrets so they could be committed to Git and managed by ArgoCD |
| Asymmetric encryption, applied | 25 | Networking & Security | Explained and used a public/private keypair where only the cluster could decrypt, and the CLI tool could only encrypt |

## 32:00 CV Skills Unlocked

See the full table above.

## 32:30 Common Mistakes

- Running `kubeseal` without `--cert`. It then tries to reach the cluster directly, which defeats the point of offline sealing and needs credentials you should not hand the tool.
- Forgetting `-T` on `docker compose run`, so the piped plaintext Secret never reaches `kubeseal`'s stdin.
- Committing the plaintext `--dry-run=client -o yaml` output by mistake, instead of the sealed one. Always check for `encryptedData`, not `data`, before `git add`.
- Reinstalling the controller on a new cluster and expecting an old `SealedSecret` to decrypt. Each cluster has its own keypair; reseal for the new cluster.

## Outro

**Say:**
- Every secret in this app now has a safe home, in the cluster and in Git.
- In Episode 26, you take every skill from all four acts and build the CV.

**Show:** Next episode preview: the skills ledger and the CV template.
