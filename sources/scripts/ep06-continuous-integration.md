# Episode 6: Continuous Integration

**Length:** 20 to 22 minutes

**Focus:** Full-Stack

**Learning goals:**
- Understand GitHub Actions workflows
- Write a CI workflow that tests code and builds images
- Use least-privilege permissions for security
- Understand status checks on pull requests
- Watch tests run and fail, then fix them
- Know what CI does in a professional team

**Prerequisites:**
- Episode 4 complete: Tests are written
- Episode 5 complete: Dockerfiles and docker-compose.yaml are done
- Episode 2 complete: Pull request workflow

## 00:00 Hook

**Say:**
- Every time you push a branch, tests run automatically.
- Every pull request shows if the code is good or broken.
- This is continuous integration, or CI.
- CI catches bugs before they ship.
- CI is the gate between a developer and main.

**Show:** Title screen.

**Expect:** Clear introduction.

## 01:00 What CI Does

**Say:**
- A developer pushes a branch.
- GitHub Actions detects the push.
- A runner (a GitHub-hosted machine) checks out the code.
- The runner runs tests. If any fail, the PR fails.
- The runner builds images. If the build breaks, the PR fails.
- The developer fixes the code and pushes again.
- Tests and builds run again automatically.
- When all checks pass, the PR is approved and merged.

**Show:** Diagram of push to PR to passing checks to merge.

**Expect:** Clear CI flow.

## 02:00 Create the Workflow File

**Say:**
- Create `.github/workflows/ci.yml`.

**Show:** Code snippet (start of file):

```yaml
name: CI

on:
  pull_request:
  push:
    branches:
      - main
```

**Say:**
- `name:` is the workflow name shown in GitHub.
- `on:` says when the workflow runs: on every pull request and on push to main.

**Show:** Highlighted YAML in the editor.

**Expect:** Workflow trigger is defined.

## 02:45 Set Permissions

**Say:**
- A workflow needs permission to do things in the repository.
- Apply least-privilege: give only the permissions you need.
- Tests only read code. Use `contents: read`.

**Show:** Code snippet to add:

```yaml
permissions:
  contents: read
```

**Say:**
- This restricts the workflow. It can read the code but not modify it or push commits.
- That makes it hard for a compromised action to do damage.

**Show:** Highlighted YAML in the editor.

**Expect:** Permissions are set.

## 03:30 Create the Test Job

**Say:**
- Add a job called `test`. A job is a unit of work that runs on a runner.

**Show:** Code snippet:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
```

**Say:**
- `runs-on: ubuntu-latest` means the runner is a Linux machine.

**Show:** Highlighted YAML in the editor.

**Say:**
- Add steps to the test job.

**Show:** Code snippet to add:

```yaml
    steps:
      - uses: actions/checkout@v4
```

**Say:**
- The first step checks out the code from the commit.

**Show:** Highlighted YAML in the editor.

**Say:**
- Set up Python.

**Show:** Code snippet to add:

```yaml
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
```

**Say:**
- This installs Python 3.12 on the runner.

**Show:** Highlighted YAML in the editor.

**Say:**
- Install dependencies and run tests.

**Show:** Code snippet to add:

```yaml
      - run: pip install -r backend/requirements.txt
      - run: python -m unittest discover -s backend -v
```

**Say:**
- `- run:` executes a shell command.
- First, install requirements.
- Then, run all tests in the backend folder with verbose output.

**Show:** Highlighted YAML in the editor.

**Expect:** Test job is complete.

## 05:00 Create the Build Job

**Say:**
- Add a second job called `build` that builds Docker images.

**Show:** Code snippet:

```yaml
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker compose build
        env:
          DB_PASSWORD: ci-only
```

**Say:**
- `docker compose build` builds all images without starting services.
- `env:` sets an environment variable for this step. Compose needs DB_PASSWORD.
- Use a dummy password. This is for build only, not a real secret.

**Show:** Highlighted YAML in the editor.

**Expect:** Build job is complete.

## 05:45 Commit and Push

**Say:**
- Create a branch for the workflow. Use the branch name `add-ci`. A direct commit to main skips the pull request checks.

**Show:** Code snippet:

```shell
git switch -c add-ci
git add .github/workflows/ci.yml
git commit -m "Add CI workflow"
```

**Say:**
- Push it.

**Show:** Code snippet:

```shell
git push -u origin add-ci
```

**Expect:** Workflow file is pushed.

## 06:30 Open a Pull Request

**Say:**
- Go to GitHub.
- Open a pull request for this branch to main.

**Show:** Screenshot of opening a PR.

**Expect:** PR is open.

## 07:00 Watch the Workflow Run

**Say:**
- Scroll down to see "Checks". You will see:
  - CI / test
  - CI / build

**Show:** Screenshot of checks running.

**Say:**
- Click "Details" to see logs.
- Watch the test job: checkout, setup Python, install, run tests.
- Watch the build job: build all three images.

**Show:** Terminal output of workflow steps.

**Expect:** Both jobs run. Tests pass. Images build.

## 08:00 Check Passes

**Say:**
- Both checks turn green (passed).
- At the bottom of the PR, you can merge.

**Show:** Screenshot of green checks and merge button.

**Expect:** PR can be merged.

## 08:30 Merge the PR

**Say:**
- Merge the PR.

**Show:** Screenshot of merge button being clicked.

**Expect:** PR is merged. Workflow runs again on the merged commit.

## 09:00 Break a Test on Purpose

**Say:**
- Go back to main.

**Show:** Code snippet:

```shell
git switch main
git pull
```

**Say:**
- Create a new branch to break a test on purpose, so you can see what happens.

**Show:** Code snippet:

```shell
git switch -c break-test
```

**Say:**
- Open `backend/test_app.py`.
- Change one of the test assertions to make it fail.

**Show:** Example: change `self.assertEqual(response.status_code, 200)` to `self.assertEqual(response.status_code, 201)`.

**Expect:** Test is broken.

## 09:45 Push and Watch It Fail

**Say:**
- Commit the broken test.

**Show:** Code snippet:

```shell
git add backend/test_app.py
git commit -m "Break the test intentionally"
git push -u origin break-test
```

**Say:**
- Open a pull request.

**Show:** Screenshot of PR.

**Say:**
- Watch the CI workflow.
- The test job fails.
- The build job may still pass (unless the failure prevents Docker from building).

**Show:** Screenshot of red X next to CI / test.

**Expect:** Check is red. PR cannot be merged.

## 11:00 Fix the Test

**Say:**
- Fix the assertion back to the correct value.

**Show:** Code snippet:

```shell
git add backend/test_app.py
git commit -m "Fix the test"
git push
```

**Say:**
- No need for `-u`. The branch is already tracked.
- The workflow runs again automatically.

**Show:** Terminal showing push.

**Expect:** New commit is pushed.

## 11:30 Watch It Pass Again

**Say:**
- Go back to GitHub.
- The workflow runs again automatically.
- This time, checks pass.

**Show:** Screenshot of green checks.

**Expect:** PR is now mergeable.

## 12:00 Do Not Merge

**Say:**
- Close the PR without merging. Delete the branch.
- The main branch stays clean.

**Show:** Screenshot of close button and delete branch button.

**Expect:** PR is closed. Branch is deleted.

## 12:30 Workflow File Concepts

**Say:**
- Workflow: A CI/CD pipeline defined in YAML.
- Job: A unit of work that runs on a runner.
- Step: A single action or command in a job.
- Runner: The machine that runs the workflow (GitHub-hosted or self-hosted).
- Trigger: When the workflow starts (on push, on PR, on schedule, manually).
- Permissions: What the workflow is allowed to do.
- Action: A reusable step, like `actions/checkout`.
- Env: Environment variables passed to steps.

**Show:** Diagram or glossary.

**Expect:** Concepts are clear.

## 13:30 Role Insight: Software Engineer

**Say:**
- Professional teams do not run tests manually.
- CI runs tests on every commit.
- If tests fail, the developer fixes them before anyone else sees the code.
- CI is a safety net. It prevents bad code from reaching main.
- You just set up what teams use in production.

## 14:00 Act 1 Review

**Say:**
- The task was: users could not delete a task, and the app had no tests, no images, and no automated checks.
- What you did: added a DELETE endpoint with a mocked unit test, wrote Dockerfiles and a Compose file, and built a CI workflow in GitHub Actions.
- What you achieved: the app is tested, packaged, starts with one command, and every pull request is checked.
- Next, the Cloud Engineer must find a place to run it.

**Show:** Three columns: Task, What you did, What you achieved.

## 16:00 Your Resume After Act 1

**Say:**
- You can now put these skills on your CV.
- Suggested headline: Junior Software Engineer
- If you stop here, this is a complete CV for this role.

**Show:**

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Git, GitHub | 2 | Programming & Tools | Managed changes with feature branches and pull requests on GitHub |
| Docker | 3, 5 | Containers & Orchestration | Containerized a three-tier app (Nginx, Flask, PostgreSQL) with non-root images |
| Python, Flask | 4 | Programming & Scripting | Built a REST endpoint in Flask with input validation and correct status codes |
| SQL, PostgreSQL | 3, 4 | Programming & Scripting | Wrote parameterized SQL queries against PostgreSQL |
| Unit testing (unittest, mocks) | 4 | Programming & Scripting | Covered API behavior with unit tests that mock the database layer |
| Docker Compose | 5 | Containers & Orchestration | Defined a multi-service stack with health checks and startup order in Docker Compose |
| GitHub Actions, CI | 6 | CI/CD & Automation | Built a CI pipeline in GitHub Actions that tests and builds every pull request |

## 18:00 CV Skills Unlocked

Add to your skills ledger:

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| GitHub Actions, CI | 6 | CI/CD & Automation | Built a CI pipeline in GitHub Actions that tests and builds every pull request |

## 18:30 Common Mistakes

- Forgetting to set `DB_PASSWORD` in the build job. Compose will fail.
- Using too many permissions. Request only what you need (contents: read).
- Hardcoding secrets in the workflow. Never put real credentials in a YAML file.
- Not setting `on:` to both `pull_request` and `push` to `main`. Tests should run on both.
- Forgetting `actions/checkout@v4`. Without it, the runner has no code.
- Using `python:latest` in setup-python. Pin a version like `3.12`.
- Not reading workflow logs. When a job fails, look at the logs to find out why.
- Windows-specific: Forgetting that the runner is Linux. If your code is Windows-only, CI will fail.

## Outro

**Say:**
- You have a CI pipeline. Tests and builds run automatically.
- That finishes Act 1: Software Engineer.
- You have added a feature, tested it, containerized it, and set up CI.
- In Act 2, you become a Cloud Engineer. You plan and build virtual machines with cloud-init and Ansible.
- See you in the next act.

**Show:** Next act preview: Cloud Engineer, VMs, Terraform, and cloud infrastructure.

**Expect:** Teaser for Act 2.
