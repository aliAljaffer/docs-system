# Episode 1: Set Up Your Laptop

**Length:** 15 to 20 minutes

**Focus:** Overview

**Learning goals:**
- Install Git, VS Code, Docker Desktop, Multipass, and Minikube on your system
- Understand why you need each tool
- Pull course container images
- Fork and clone the starter repository

**Prerequisites:** 
- macOS or Windows 10/11
- Administrator access to install software
- 8 GB of memory or more (16 GB is better)
- 30 GB of free disk space

## 00:00 Hook

**Say:**
- Your laptop is a mini data center.
- Five programs. Two of them you use directly. Three are frameworks for running containers.
- By the end of this episode, you are ready to write code, test it, and run services side by side.

**Show:** Title screen.

**Expect:** Clear introduction.

## 01:00 What Each Tool Does

**Say:**
- Git: Version control. You push and pull code from GitHub.
- VS Code: Code editor. You write Python, JavaScript, YAML, Bash.
- Docker Desktop: Runs containers. Python, databases, Kubernetes, and everything else.
- Multipass: Runs Ubuntu VMs on your laptop (Act 2).
- Minikube: Runs a Kubernetes cluster (Acts 3 and 4).

**Show:** Table or icons:

| Tool | Why you need it |
|---|---|
| Git | Version control |
| VS Code | Code editor |
| Docker Desktop | Runs containers |
| Multipass | Runs Ubuntu VMs |
| Minikube | Runs Kubernetes |

**Expect:** Clear purpose of each tool.

## 02:00 macOS: Install with Homebrew

**Say:**
- On macOS, we use Homebrew, a package manager.
- Copy each command and run it in your terminal.

**Show:** Step 1: Check if you have Homebrew.

**Say:**
- If you do not have Homebrew, install it from brew.sh.

**Show:** Code snippet:

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Expect:** Homebrew installation completes in about 1 minute.

**Say:**
- Now install the five programs.

**Show:** Code snippet for macOS:

```shell
brew install git minikube
brew install --cask visual-studio-code docker-desktop multipass
```

**Expect:** All five tools installed in about 5 to 10 minutes.

**Say:**
- Open Docker Desktop once. Accept the license terms. Wait until it says "Engine running". This might take a couple of minutes.

**Show:** Screenshot of Docker Desktop with "Engine running" visible.

**Expect:** Docker is running.

## 04:30 Windows: Install with Winget

**Say:**
- On Windows, we use Winget, the Windows package manager.
- Open PowerShell as Administrator.

**Show:** Right-click PowerShell, select "Run as Administrator".

**Say:**
- First, enable the Virtual Machine Platform. Both Docker and Multipass need it.

**Show:** Code snippet for Windows:

```powershell
wsl --install --no-distribution
```

**Say:**
- This takes about 1 minute.
- When it finishes, restart your computer.

**Expect:** Restart completes.

**Say:**
- Open PowerShell as Administrator again.
- Install the five programs.

**Show:** Code snippet for Windows:

```powershell
winget install -e --id Git.Git
winget install -e --id Microsoft.VisualStudioCode
winget install -e --id Docker.DockerDesktop
winget install -e --id Canonical.Multipass
winget install -e --id Kubernetes.minikube
```

**Expect:** All five tools installed in about 5 to 10 minutes.

**Say:**
- Open Docker Desktop. Make sure it uses Linux containers, not Windows containers. The setting is in the system tray.

**Show:** Screenshot of Docker Desktop settings with "Use Linux containers" enabled.

**Expect:** Docker is running in Linux container mode.

**Say:**
- For all course commands, use PowerShell. Do not run commands inside Windows Subsystem for Linux (WSL), even though you just enabled it.

## 07:00 Check the Install

**Say:**
- Verify that all tools are installed. Run each command. You should see a version number.

**Show:** Code snippet:

```shell
git --version
docker version
multipass version
minikube version
```

**Expect:** Version output for each tool. If you see an error, go back and check the install step.

## 08:00 Configure Docker Desktop Resources

**Say:**
- Kubernetes needs CPU and memory. In Docker Desktop, open Settings and go to Resources.

**Show:** Steps to open Docker Desktop Settings on macOS and Windows.

**Say:**
- Set CPUs to 6 or more.
- Set memory to 8 GB or more.

**Show:** Docker Desktop Resources window with sliders set to 6 CPUs and 8 GB.

**Expect:** New settings are applied. Docker may restart.

**Say:**
- If your laptop has less than 8 GB total memory, you can still do Acts 1 and 2. See the Costs and Free Options doc for alternatives.

## 09:30 Pull the Course Images

**Say:**
- Container images are big. Pulling them now means the episodes do not wait for downloads.

**Show:** Code snippet:

```shell
docker pull python:3.12-slim
docker pull postgres:16-alpine
docker pull nginx:1.27-alpine
```

**Say:**
- These images are used in Acts 1 and 2.
- Acts 3 and 4 add more images. You will pull those in later episodes.

**Expect:** All three images downloaded. This takes about 3 to 5 minutes depending on your internet speed.

## 11:00 Fork the Repository

**Say:**
- Go to GitHub and sign in with your account.
- Open the starter repository: github.com/alialjaffer/minikube-project
- Click Fork. This creates a copy of the repository under your account.

**Show:** GitHub Fork button and confirmation dialog.

**Expect:** You now have your own copy of the repository.

**Say:**
- Clone your fork to your laptop.

**Show:** Code snippet (replace YOUR-USERNAME with your GitHub username):

```shell
git clone https://github.com/YOUR-USERNAME/minikube-project.git
cd minikube-project
```

**Expect:** Repository is cloned. You have a folder called `minikube-project`.

**Say:**
- Open the folder in VS Code. It suggests a set of extensions for this repository: Docker, YAML, Kubernetes, Terraform, Ansible, GitHub Actions, and Semgrep. Select Install All.
- Later episodes use each one. You will not need to hunt for them yourself.

**Show:** The VS Code extension recommendation prompt.

**Expect:** Extensions install in the background.

## 12:30 Verify the Setup

**Say:**
- Run a quick check. Start a course tool from the command line.

**Show:** Code snippet:

```shell
docker compose -f tools/compose.yaml run --rm python-test
```

**Say:**
- This command runs the Python test tool. The starter has three tests. The command must print `Ran 3 tests` and `OK`. Episode 4 adds the first test for a task feature.

**Expect:** Command completes and shows test output. If this works, your Docker setup is correct.

## 13:30 Role Insight: Software Engineer

**Say:**
- A Software Engineer uses these exact tools every day.
- Git to manage code changes. VS Code to write. Docker to run services locally so you do not break your laptop. GitHub to back up your work and review code with teammates.
- You can start coding now. You have everything you need.

## 14:00 CV Skills Unlocked

No skills ledger entries for this episode. You are setting up, not yet building skills. The skills start in Episode 2.

## 15:00 Common Mistakes

- Windows: Running Minikube inside WSL instead of PowerShell. Use PowerShell for all commands.
- Windows: Using `curl` in PowerShell 5.1 without `.exe`. PowerShell aliases `curl` to a different command. Use `curl.exe` or `Invoke-WebRequest`.
- Forgetting to open Docker Desktop after installing. It must be running.
- Running out of disk space during pulls or builds. Delete old images with `docker image prune` if needed.
- Memory: If Docker Desktop gets less than 8 GB, Kubernetes in Act 3 will be slow or fail to start.

## Outro

**Say:**
- You are set up.
- In Episode 2, you learn Git: fork, branch, commit, push, pull request. You make your first contribution.
- See you next time.

**Show:** Next episode preview: Git and GitHub workflow.

**Expect:** Teaser for the next episode.
