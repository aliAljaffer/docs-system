# Episode 20: Think Like an Attacker

**Length:** 20 to 24 minutes

**Focus:** Penetration Tester

**Learning goals:**
- Write a scope and rules of engagement before testing anything
- Map the OWASP Top 10 onto a real three-tier app
- Read an API by hand with curl
- Map an attack surface with Burp Suite

**Prerequisites:**
- Episode 19 complete, app running on Minikube
- Burp Suite Community Edition installed (free download, a GUI proxy, this is the one Act 4 tool that runs on the host)

## 00:00 Hook

**Say:**
- Every app you have built so far assumed its users are honest.
- Today you stop assuming that.
- By the end of this act, you will have found a real SQL injection, fixed it, and proven the fix with three different tools.

**Show:** Title screen.

## 01:00 Act 4 Briefing

**Say:**
- Welcome to Act 4. You are the new Cybersecurity Engineer.
- Previously, the DevOps team deployed the app to Kubernetes with GitOps, autoscaling, and monitoring.
- Your task: the backend ships a search endpoint that builds SQL from user input. Nobody has tested it.
- Your goal: think and act like an attacker to find the flaw, then switch hats and fix it, then prove the fix with automated scans.
- Done when: `sqlmap` finds nothing on the fixed endpoint, a Pod without an allow rule cannot reach the database, and Semgrep, Trivy, and ZAP all run.
- Start here if you want only this role. Copy `act-3-devops-engineer/` from the solved repository. You need Docker Desktop and Minikube.

**Show:** A briefing card with four lines: Role, Task, Goal, Done when.

## 03:00 Rules of Engagement

**Say:**
- Warning: never point a security tool at a system you do not own or do not have written permission to test.
- Every hands-on step in this act targets `127.0.0.1`, `localhost`, or your own Minikube cluster's internal network. Nothing else.
- Write a one-page scope before you touch the app: the target, what is in scope, what is out of scope, and when you stop.
- This is not a formality. In a real job, testing without written scope is the line between your job and a crime.

**Show:** A scope document template: Target, In scope, Out of scope, Stop condition.

**Expect:** Students understand this act never touches a system outside their own laptop.

## 05:00 The OWASP Top 10

**Say:**
- The OWASP Top 10 is a list of the most common web application weaknesses.
- Injection is on it. So is security misconfiguration.
- This act gives you one of each: a SQL injection, and a Kubernetes cluster with no NetworkPolicies.

**Show:** The OWASP Top 10 list, with this app's two weaknesses marked next to the matching entries.

**Expect:** Students connect a famous list to the app in front of them.

## 08:00 Read the API With curl

**Say:**
- Before you attack anything, read it. Most of what an attacker needs is already public: the endpoints, the parameters, the status codes.
- Keep this port-forward running in its own terminal for the rest of this act.

**Show:**

```shell
minikube kubectl -- port-forward service/backend -n app 8000:8000
```

```shell
curl http://localhost:8000/healthz
curl http://localhost:8000/readyz
curl http://localhost:8000/api/tasks
curl -G http://localhost:8000/api/tasks/search --data-urlencode "q=groceries"
```

**Expect:** Four endpoints respond. `search` takes a `q` parameter, the first one that takes raw user input and uses it to filter data.

## 12:00 Map the Attack Surface With Burp Suite

**Say:**
- curl shows you one request at a time. A proxy shows you every request your browser makes.
- Burp Suite sits between your browser and the app. It records, replays, and lets you edit requests.

**Show:**
- Set Burp's proxy listener to `127.0.0.1:8080`.
- Point the browser's proxy settings at it.
- Open the frontend, create a task, search for it, mark it done, delete it.
- Open Burp's site map. Point out every request: `GET /`, `GET /api/tasks`, `POST /api/tasks`, `PATCH /api/tasks/<id>`, `GET /api/tasks/search`.

**Expect:** A complete site map. `GET /api/tasks/search?q=` stands out: it is the only endpoint whose parameter directly shapes a database query's `WHERE` clause.

## 16:00 Write the Pentest Notes

**Say:**
- A pentest is worthless if nobody reads it later. Write down what you found, even before you exploit it.
- One line per finding: the endpoint, why it looks interesting, and your next step.

**Show:** A short pentest notes file: endpoint, observation, next step. One row for `/api/tasks/search`.

**Expect:** Students have a written artifact, not just a memory of what they clicked.

## 18:00 Role Insight: Penetration Tester

**Say:**
- A real engagement starts with a signed scope, not a tool.
- The slowest, most valuable step is reading, not attacking. Most real vulnerabilities are found by someone who read the code or the traffic carefully, not by running a scanner on autopilot.

## 19:00 CV Skills Unlocked

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Rules of engagement, authorized testing | 20 | Networking & Security | Defined scope and rules of engagement before testing an application |
| OWASP Top 10 | 20 | Networking & Security | Mapped the OWASP Top 10 to a three-tier application |
| API reconnaissance (curl) | 20 | Networking & Security | Enumerated API endpoints and parameters with curl |
| Attack surface mapping (Burp Suite) | 20 | Networking & Security | Mapped an application's attack surface with Burp Suite |

## 19:30 Common Mistakes

- Testing without a written scope. Write it first, even as a student.
- Forgetting the port-forward. If curl hangs, check it is still running.
- Leaving the browser proxy pointed at Burp after this episode. Turn it off before normal browsing.
- Skipping the read-only recon and jumping straight to exploitation. You will miss endpoints.

## Outro

**Say:**
- You have a scope, a map, and one endpoint that stands out.
- In Episode 21, you confirm the SQL injection by hand, then automate the attack with sqlmap.

**Show:** Next episode preview: the search endpoint, broken on purpose.
