# Episode 9: Configuration as Code

**Length:** 20 to 25 minutes

**Focus:** Platform Engineer

**Learning goals:**
- Explain configuration management and idempotence
- Write an Ansible inventory and playbook
- Run Ansible from a container
- Set a firewall with UFW
- Pass a secret without writing it in Git

**Prerequisites:**
- Episode 8 complete: a running VM with your SSH key
- Docker Desktop running

## 00:00 Hook

**Say:**
- Imagine you have to set up ten servers by hand.
- You will forget a step on server seven.
- Ansible does the same steps on every server, every time.

**Show:** Title screen.

## 01:30 Ansible in a Container

**Say:**
- We do not install Ansible on the laptop. It runs as a Docker image.
- The image comes from `tools/ansible/Dockerfile`.
- Ansible connects to the VM over SSH. It needs nothing installed on the VM.

**Show:**

```shell
docker compose -f tools/compose.yaml run --rm ansible ansible --version
```

On Windows PowerShell, run `$env:HOME = $env:USERPROFILE` first.

## 03:30 The Inventory

**Say:**
- The inventory lists your servers.

**Show:**

```shell
cp infra/ansible/inventory.example.ini infra/ansible/inventory.ini
```

Edit the IP address. Then:

```shell
docker compose -f tools/compose.yaml run --rm ansible ansible taskboard -m ping
```

**Expect:** `SUCCESS` and `"ping": "pong"`.

## 05:30 Write the Playbook

**Say:**
- A playbook is a list of tasks. Each task calls a module.
- You describe the state you want. Ansible decides what to change.
- We write the tasks in six groups.

**Show and explain, one group at a time:**

1. Install packages with `ansible.builtin.apt`: `docker.io`, `docker-compose-v2`, `ufw`, `rsync`.
2. Start Docker and enable it at boot with `ansible.builtin.service`.
3. Add the login user to the `docker` group with `ansible.builtin.user`.
4. Firewall with `community.general.ufw`: allow 22 and 8080, then turn UFW on with policy `deny`.
5. Copy the app with `ansible.posix.synchronize`. Skip `.git`, `infra`, and `.env`. Set `become: false` on this one task.
6. Write `.env` with `ansible.builtin.copy`. Set mode `0600` and `no_log: true`.
7. Start the stack with `community.docker.docker_compose_v2`.

**Say:**
- Allow SSH before you turn the firewall on. Otherwise you lock yourself out.
- `synchronize` under `become: true` writes files as root, which fights the ownership the directory task set. Turn privilege escalation off for just this one task, or the playbook never settles.
- The password comes from the `DB_PASSWORD` environment variable. It is never in Git.
- `no_log: true` hides the password from the output.

## 13:00 Check and Run

**Show:**

```shell
docker compose -f tools/compose.yaml run --rm ansible ansible-playbook --syntax-check playbook.yml
export DB_PASSWORD=choose-a-password
docker compose -f tools/compose.yaml run --rm -e DB_PASSWORD ansible ansible-playbook playbook.yml
```

**Expect:** Each task shows `ok` or `changed`. The recap shows `failed=0`. The run takes a few minutes, because the VM builds the images.

## 17:00 Test the App

**Show:** Open `http://<vm-ip>:8080`. Add a task.

**Show:** Port 8000 is closed:

```shell
curl -m 3 http://<vm-ip>:8000/api/tasks
```

**Expect:** The command times out.

**Say:**
- The firewall works. Only the ports from our plan are open.
- This only holds because `compose.yaml` never publishes a backend port. A published container port bypasses UFW entirely, because Docker writes its own rules ahead of it.

## 18:30 Idempotence

**Say:**
- Run the playbook again.

**Show:**

```shell
docker compose -f tools/compose.yaml run --rm -e DB_PASSWORD ansible ansible-playbook playbook.yml
```

**Expect:** `changed=0`.

**Say:**
- Nothing changed, because the VM already has the wanted state.
- This is idempotence. You can run the playbook any time.

## 20:00 Role Insight: Platform Engineer

**Say:**
- The playbook is documentation that runs.
- A teammate reads it in Git and sees how the server is set up.
- When a server breaks, you rebuild it from the playbook.

## 21:00 CV Skills Unlocked

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Ansible | 9 | Cloud & Infrastructure | Wrote an idempotent Ansible playbook that installs Docker, sets the firewall, and deploys a Compose stack |
| Firewalls (UFW, VPC rules) | 9, 10 | Cloud & Infrastructure | Closed all ports except SSH and HTTP with UFW and GCP firewall rules |

## 22:00 Common Mistakes

- Turning UFW on before you allow port 22. SSH stops working.
- Wrong IP address in `inventory.ini`. Run `multipass list`.
- Committing `inventory.ini` or `.env`. Both are in `.gitignore`.
- Forgetting `-e DB_PASSWORD`. The container cannot see the variable.
- YAML indentation errors. Run `--syntax-check`.
- Windows: not setting `$env:HOME`. Compose cannot find your SSH key.
- A private key with a passphrase. The Ansible container has no ssh-agent. It cannot unlock the key. Create the key without a passphrase: `ssh-keygen -t ed25519 -N ""`. As an alternative, load the key into an agent on the host.

## Outro

**Say:**
- One command now builds the server.
- In Episode 10, you run the same playbook on a VM in Google Cloud. Terraform creates that VM.
- See you there.

**Show:** Next episode preview: Terraform and GCP.
