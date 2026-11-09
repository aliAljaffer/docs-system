# Episode 23: Scan and Verify

**Length:** 20 to 23 minutes

**Focus:** Security Engineer (AppSec)

**Learning goals:**
- Catch an injection pattern in source code with Semgrep (SAST)
- Scan images, Dockerfiles, Kubernetes YAML, and Terraform with Trivy (SCA, IaC, secrets)
- Check the running app's HTTP response headers with OWASP ZAP (DAST)
- Wire SAST and SCA into a pull request workflow

**Prerequisites:**
- Episode 22 complete

## 00:00 Hook

**Say:**
- You fixed the bug by reading the code. Today, three tools check that it stays fixed, automatically, on every future commit.
- One tool per layer: source code, supply chain, running app.

**Show:** Title screen.

## 01:00 SAST: Semgrep

**Say:**
- SAST reads source code without running it. Semgrep matches a pattern you describe against every file.
- Write a rule that flags an f-string passed to `.execute(`, the exact shape of the bug from Episode 21.

**Show:**

```yaml
# tools/semgrep/sql-injection.yml
rules:
  - id: fstring-sql-query
    languages: [python]
    severity: ERROR
    message: Do not build a SQL query with an f-string. Use a parameterized query.
    patterns:
      - pattern: $CONN.execute(f"...")
```

```shell
docker compose -f tools/compose.yaml run --rm semgrep \
  semgrep scan --config tools/semgrep/sql-injection.yml backend/
```

**Expect:** No findings on the fixed code. Temporarily put the f-string back, run it again, and watch Semgrep flag the exact line. Revert the change.

## 04:30 SCA, IaC, and Secrets: Trivy

**Say:**
- Trivy checks three different things with one tool: known vulnerabilities in packages and images, misconfigurations in Dockerfiles, Kubernetes YAML, and Terraform, and credentials accidentally committed to the repository.
- The `trivy` service mounts your Docker socket, so it can inspect a local image by name without a registry.

**Show:**

```shell
docker build -t tutorial-backend:local ./backend

docker compose -f tools/compose.yaml run --rm trivy image tutorial-backend:local
docker compose -f tools/compose.yaml run --rm trivy config kubernetes/
docker compose -f tools/compose.yaml run --rm trivy fs --scanners secret .
```

**Expect:** A vulnerability report for the base image, a misconfiguration report for the manifests, and a clean secret scan, since this course never commits credentials. Record any finding you do not fix today, and say why.

## 08:00 DAST: OWASP ZAP

**Say:**
- DAST tests the running app over HTTP, the same way an attacker or a user would, with no view of the source code.
- The baseline scan is passive by default: it crawls and checks headers and cookies, not full active attacks, so it is safe to run against your own app repeatedly.
- That also sets its limit. It cannot prove the SQL injection fix. `sqlmap` proved that in Episode 21, and Semgrep now guards the pattern in source. ZAP covers the HTTP layer around it: the headers every browser receives.
- Target the frontend, not the backend. The backend has no page at `/`, and its responses carry Flask headers. The headers in this episode live in `frontend/nginx.conf`, so the scan must go through Nginx.
- Run it as a Pod inside the cluster, the same reasoning as `sqlmap`: it reaches the app by Service name, nothing exposed beyond the cluster.

**Show:**

```shell
minikube kubectl -- create configmap zap-rules -n app --from-file=rules.tsv=tools/zap/rules.tsv
```

```yaml
# zap-scan-pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: zap-scan
  namespace: app
  labels:
    app.kubernetes.io/name: scanner
spec:
  restartPolicy: Never
  containers:
    - name: zap
      image: ghcr.io/zaproxy/zaproxy:stable
      imagePullPolicy: IfNotPresent
      command:
        - zap-baseline.py
        - -I
        - -t
        - "http://frontend.app.svc.cluster.local/"
        - -c
        - /zap/rules/rules.tsv
      volumeMounts:
        - name: rules
          mountPath: /zap/rules
        - name: wrk
          mountPath: /zap/wrk
  volumes:
    - name: rules
      configMap:
        name: zap-rules
    - name: wrk
      emptyDir: {}
```

```shell
minikube kubectl -- apply -f zap-scan-pod.yaml
minikube kubectl -- wait --for=jsonpath='{.status.phase}'=Succeeded pod/zap-scan -n app --timeout=300s
minikube kubectl -- logs zap-scan -n app
minikube kubectl -- delete pod zap-scan -n app
```

**Say:**
- `-I` keeps the Pod successful when the only result is warnings. Without it, `zap-baseline.py` exits 2 and `kubectl wait` never sees `Succeeded`.
- Read the findings from the Pod log. Do not use `kubectl cp` after the scan: the container has exited, so `cp` cannot start a process in it.
- The `wrk` volume is required even without `-r`. The image runs from `/zap/wrk`, and `zap-baseline.py` refuses to start with a file based option when that directory is not a mount.
- The Pod is labeled `app.kubernetes.io/name: scanner`. The `scanner` NetworkPolicy lets that label reach the frontend; without it, the default-deny egress rule blocks the scan and the Pod fails with `Connect timed out`.
- `tools/zap/rules.tsv` silences two informational findings: cacheable content and modern web application. Every header finding still reports.

**Expect:** The log lists the missing anti-clickjacking and `X-Content-Type-Options` headers, CSP, Permissions Policy, and the Nginx version leak. It reports no injection: this scan does not send injection payloads.

## 15:00 Nginx Security Headers

**Say:**
- These headers close the rest of the report. One stops the browser guessing a file's type, one stops the page being framed by another site, one limits where the page may load code from, and one switches off browser APIs this app does not use.
- `server_tokens off` removes the version banner from the `Server` header and from Nginx error pages.

**Show:**

```nginx
server_tokens off;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header Referrer-Policy "no-referrer" always;
add_header Content-Security-Policy "default-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'; object-src 'none'" always;
add_header Permissions-Policy "geolocation=(), camera=(), microphone=()" always;
```

**Say:**
- Add them to the `server` block in `frontend/nginx.conf`, rebuild the frontend image, redeploy it, and re-run the same ZAP Pod.
- The CSP needs the `base-uri`, `form-action`, and `object-src` fallbacks. Without them ZAP raises rule 10055, `CSP: Failure to Define Directive with No Fallback`.

**Expect:** The anti-clickjacking, `X-Content-Type-Options`, CSP, Permissions Policy, and version leak findings disappear. One Low finding remains, `Cross-Origin-*-Policy Header Missing or Invalid` (90004). Record it and leave it: those policies need every cross-origin resource to cooperate, and this app loads none.

## 17:00 Write the Security Workflow

**Say:**
- Semgrep and Trivy need no running app, so they run on every pull request. ZAP needs the app running, which a GitHub Actions runner does not have by default in this course, so it stays a manual, documented step.

**Show:**
- Add `.github/workflows/security.yml`: on `pull_request`, run the Semgrep scan command and the Trivy image and config scans from this episode.
- Use your own rule file, `tools/semgrep/sql-injection.yml`, not only Semgrep's registry rules. The registry rules may not catch this exact f-string pattern.
- The solved reference also has a DAST job that starts the Compose stack and runs ZAP. It is optional. If you keep ZAP as a manual step, omit that job.

**Expect:** A pull request that reintroduces the f-string fails the workflow before it can be merged.

## 19:00 Role Insight: Security Engineer (AppSec)

**Say:**
- No single scanner catches everything. SAST reads code that never ran. DAST tests what actually runs. Trivy watches the supply chain neither one looks at.
- An AppSec Engineer's job is wiring these together so a fix stays fixed, not re-finding the same bug by hand every time.

## 20:00 CV Skills Unlocked

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| SAST (Semgrep) | 23 | Networking & Security | Found a SQL injection pattern in source code with Semgrep |
| SCA, IaC, and secret scanning (Trivy) | 23 | Networking & Security | Scanned images, Dockerfiles, Kubernetes YAML, and Terraform with Trivy |
| DAST (OWASP ZAP) | 23 | Networking & Security | Hardened the Nginx response headers and verified them with an OWASP ZAP baseline scan |

## 21:00 Common Mistakes

- Scanning the backend API and expecting Nginx header findings. Scan the frontend; that is where Nginx answers.
- Waiting for `Succeeded` without `-I`. Warnings make `zap-baseline.py` exit 2, so the Pod ends `Failed` even though the report is complete.
- Treating a clean ZAP report as proof of safety. It is a passive baseline scan, not a full penetration test.
- Treating a ZAP report as proof of the SQL injection fix. A passive scan sends no payloads; `sqlmap` and Semgrep cover that.
- Wiring ZAP into the pull request workflow. It needs a running app; keep it manual and documented instead.
- Leaving a Trivy finding unrecorded. Note every finding you do not fix, and why.

## Outro

**Say:**
- You built it, deployed it, broke it, and fixed it. Two more weaknesses are worth finding before you call this done.
- In Episode 24, a second real vulnerability: broken access control.

**Show:** Next episode preview: two users, one missing ownership check.
