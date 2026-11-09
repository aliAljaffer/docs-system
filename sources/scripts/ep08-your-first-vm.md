# Episode 8: Your First VM

**Length:** 24 to 29 minutes

**Focus:** Systems/Linux Engineer

**Learning goals:**
- Create a VM with Multipass
- Configure the first boot with cloud-init
- Log in with an SSH key
- Use basic Linux commands to inspect a server
- Read and change file permissions with `chmod`
- Combine commands with pipes and redirection
- Read an environment variable
- Write and run a short shell script

**Prerequisites:**
- Episode 7 complete
- Multipass installed (Episode 1)

## 00:00 Hook

**Say:**
- A cloud server is a VM that someone else hosts.
- Today you build one on your laptop. The steps are the same in the cloud.

**Show:** Title screen.

## 01:00 What a VM Is

**Say:**
- A VM is a full computer made of software.
- A hypervisor shares the real CPU and memory between VMs.
- Each VM has its own kernel and its own users.
- A container shares the host kernel. A VM does not.

**Show:** Diagram: laptop, hypervisor, VM with its own Linux.

## 03:00 Make an SSH Key

**Say:**
- A password can be guessed. A key pair cannot.
- The private key stays on your laptop. The public key goes on the server.

**Show:**

```shell
ssh-keygen -t ed25519
cat ~/.ssh/id_ed25519.pub
```

On Windows PowerShell, use `type $env:USERPROFILE\.ssh\id_ed25519.pub`.

**Expect:** One line that starts with `ssh-ed25519`.

## 05:00 Write cloud-init

**Say:**
- cloud-init runs once, on the first boot.
- It creates users, installs packages, and sets the host name.
- The first line must be `#cloud-config`.

**Show:** `infra/cloud-init/vm.yaml`:

```yaml
#cloud-config
hostname: taskboard
users:
  - name: student
    groups: [sudo]
    shell: /bin/bash
    sudo: ALL=(ALL) NOPASSWD:ALL
    ssh_authorized_keys:
      - ssh-ed25519 AAAA... you@laptop
package_update: true
packages:
  - curl
  - git
  - htop
timezone: UTC
```

**Say:**
- Paste your own public key.
- `NOPASSWD` is fine for a lab VM. A production server needs a stricter rule.

## 08:00 Launch the VM

**Show:**

```shell
multipass launch 24.04 --name taskboard --cpus 2 --memory 2G --disk 10G --cloud-init infra/cloud-init/vm.yaml
multipass list
```

**Expect:** State `Running` and an IPv4 address. The first launch downloads the image, so it takes a few minutes.

## 10:00 Log In

**Show:**

```shell
ssh student@<vm-ip>
```

**Expect:** A shell prompt `student@taskboard`.

**Say:**
- No password. The key did the work.
- The host name came from cloud-init.

## 11:30 Linux Basics

**Show:** Run each command and explain the output:

```shell
whoami
pwd
ls /
df -h
free -m
systemctl status ssh
sudo apt update
htop
```

**Say:**
- `df` shows disk. `free` shows memory.
- `systemctl` controls services.
- `apt` installs packages.
- Cloud Engineers read these outputs every day.

**Show:** Table of file commands. Run each one in your home folder:

| Command | What it does |
|---|---|
| `cd /var/log` and `cd ..` and `cd ~` | Go to a folder, up one folder, home |
| `mkdir app` | Make a folder |
| `touch notes.txt` | Make an empty file |
| `cat notes.txt` | Print a file |
| `cp a.txt b.txt` and `mv old new` | Copy, move or rename |
| `rm notes.txt` and `rm -r app` | Remove a file, remove a folder |

**Say:**
- Press Tab to complete a name. Press the up arrow to bring back the last command.
- `rm` does not ask. There is no trash can.

## 14:30 File Permissions

**Say:**
- Every file has an owner, a group, and a set of permissions.
- Run `ls -l`. Read the first column: three groups of three letters. Owner, group, others. Each group has r (read), w (write), x (execute).

**Show:**

```shell
ls -l notes.txt
chmod 400 notes.txt
chmod 755 notes.txt
chmod +x notes.txt
```

**Say:**
- The number form adds r=4, w=2, x=1 for each group.
- `400` means only the owner can read. `755` means the owner can do all, and others can read and run.
- SSH refuses a private key that others can read. A key with mode `644` is not private. Use `600` or `400`.
- A private key must not be executable. A script must be. The same `x` bit, opposite needs.

## 17:00 Pipes and Redirection

**Say:**
- A pipe `|` sends the output of one command into the next.
- `>` writes output to a file and replaces the file. `>>` adds to the end.

**Show:**

```shell
cat /etc/passwd | grep student
history | grep ssh
echo "hello cloud" > hello.txt
echo "another line" >> hello.txt
cat hello.txt
```

**Expect:** Two lines in `hello.txt`.

**Say:**
- Mixing up `>` and `>>` overwrites a file you meant to extend.

## 19:30 Environment Variables

**Say:**
- An environment variable is a named value that programs can read.
- The task board reads `DB_PASSWORD` this way. Your Ansible playbook writes it into `.env` in Episode 9.

**Show:**

```shell
export NAME="Task Board"
echo "Hello, $NAME"
echo $HOME
env
```

**Expect:** `Hello, Task Board`, then your home folder, then the full list.

## 21:00 Your First Script

**Say:**
- A shell script is a text file of commands.
- The first line `#!/bin/bash` names the interpreter.
- `$1` is the first argument. `${1:-world}` uses `world` if you give none.

**Show:** `report.sh`:

```bash
#!/bin/bash
echo "Report for ${1:-world} on $(hostname)"
echo "Date: $(date)"
df -h / | tail -n 1
free -m | grep Mem
```

```shell
chmod +x report.sh
./report.sh student
./report.sh student > report.txt
cat report.txt
```

**Expect:** Host name, date, one disk line, one memory line. The same text is in `report.txt`.

**Say:**
- You used four ideas: permissions, a pipe, a redirect, and a variable.
- A script like this is the first step to automation. Ansible, in Episode 9, is the same idea at larger scale.

## 24:30 Role Insight: Systems/Linux Engineer

**Say:**
- You will not log in to fix servers by hand for long.
- Each hand fix is a change nobody wrote down.
- Next episode, a tool does the setup, so you can repeat it.

## 25:30 CV Skills Unlocked

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Linux administration, SSH | 8 | Cloud & Infrastructure | Provisioned Ubuntu VMs with cloud-init and key-only SSH access |
| Linux file permissions (`chmod`) | 8 | Operating Systems | Set file permissions with `chmod` and explained why SSH rejects an open private key |
| Shell (pipes, redirection, environment variables) | 8 | Operating Systems | Combined Linux commands with pipes and redirection and configured programs with environment variables |
| Bash scripting | 8 | Programming & Scripting | Wrote a Bash script that reports host, disk, and memory use |

## 26:00 Common Mistakes

- Pasting the private key into cloud-init. Paste the `.pub` file.
- Wrong YAML indentation. cloud-init ignores a broken file. Check the first line and the spaces.
- Missing `#cloud-config` on the first line.
- Editing `vm.yaml` and expecting a running VM to change. cloud-init runs once. Delete the VM and launch again.
- Windows: using `~/.ssh` in PowerShell. Use `$env:USERPROFILE\.ssh`.
- Using `>` when you mean `>>`. The file loses its old content.
- Running `./report.sh` without `chmod +x`. The shell answers `Permission denied`.
- Leaving a space around `=` in `NAME="x"`. The shell reads it as a command.
- Running `rm -r` in the wrong folder. Check with `pwd` first.

## Outro

**Say:**
- You have a VM. It is empty.
- In Episode 9, you use Ansible to set it up with one command.
- Keep the VM running.

**Show:** Next episode preview: an Ansible playbook.
