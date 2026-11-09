# Episode 16: Publish Images

**Length:** 18 to 22 minutes

**Focus:** Release Engineer

**Learning goals:**
- Explain a container registry
- Build multi-arch images in GitHub Actions
- Tag images with the commit SHA
- Update manifests without a workflow loop
- Pull private images with a classic PAT

**Prerequisites:**
- Episode 15 complete
- Your fork is on GitHub

## 00:00 Hook

**Say:**
- Until now, we loaded images by hand.
- A real cluster pulls from a registry.
- Today a push to `main` builds and publishes the images.

**Show:**
Title screen.


## 01:30 Registries and Tags

**Say:**
- GHCR is the GitHub registry. It is free for public repositories.
- A tag names an image version.
- `latest` moves. A commit SHA never changes. Use the SHA.

**Show:**
The image name form: `ghcr.io/<owner>/<repo>/backend:<sha>`.


## 04:00 Multi-arch

**Say:**
- Macs with Apple chips use ARM64. Most servers use AMD64.
- One tag can hold both. Docker picks the right one.

**Show:**
The `platforms` line in the workflow: `linux/amd64,linux/arm64`.


## 06:00 Write the Workflow

**Show:**
- `on: push` to `main` with a `paths` filter.
- `permissions`: `contents: write` and `packages: write`.
- Steps: checkout, tests, QEMU, Buildx, login to GHCR, three `build-push-action` steps, update manifests.

**Expect:** Copy `act-3-devops-engineer/.github/workflows/publish.yml` from the solved repository and fix the paths.

## 12:00 Update the Manifests

**Say:**
- The last step writes the new SHA into the manifests.
- It commits as `github-actions[bot]` and pushes.

**Show:**
The `sed` commands that replace the image tags.


## 14:00 Avoid the Loop

**Say:**
- The bot commit changes only manifests.
- The `paths` filter does not list manifests. So the bot commit does not start the workflow.


## 15:30 Run It

**Show:**
- Change a file in `backend/`. Commit and push.
- Open the Actions tab and watch the run.
- Open the Packages page.

**Expect:** Three packages. A new bot commit appears in the history.

## 18:00 Private Images

**Say:**
- Packages from a private repository are private.
- Docs section: create a classic PAT with `read:packages` and a pull Secret.
- Or make the repository and packages public.

**Show:**
`docs/act3-devops-engineer.md`: the PAT section.


## 20:00 Role Insight: Release Engineer

**Say:**
- Image tags tied to a commit let you trace a running Pod to the exact code.
- Rollback means pointing the manifest at an older SHA.

## 21:00 CV Skills Unlocked

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Container registries, multi-arch builds | 16 | CI/CD & Automation | Built and published multi-architecture images to GHCR, tagged by commit SHA, with GitHub Actions |

## 21:30 Common Mistakes

- Using `latest`. You cannot tell what runs.
- A workflow that triggers itself. Check the `paths` filter.
- Missing `packages: write`. The push fails with `denied`.
- A PAT with too many scopes. Use only `read:packages`.
- Committing the PAT.

## Outro

**Say:**
- Images are in a registry. Nothing deploys them yet.
- In Episode 17, ArgoCD deploys them from Git.

**Show:** Next episode preview: GitOps with ArgoCD.
