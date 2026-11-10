# 4. Users and Groups

**Goal:** Create, lock, and configure user accounts and groups.

## Create users and groups

```bash
groupadd heroes
useradd -g superheros -s /bin/bash -c "user description" -m -d /home/spiderman spiderman
```

| Option | Meaning |
|--------|---------|
| `-g` | Primary group |
| `-s` | Login shell |
| `-c` | Description |
| `-m` | Create the home directory |
| `-d` | Home directory path |

Other commands: `userdel`, `groupdel`, `groupmod`, and `usermod`.

## Lock, unlock, and expire accounts

```bash
usermod -L anna
usermod -U anna
usermod -e 2030-01-01 anna
usermod -s /sbin/nologin anna
```

| Command | Action |
|---------|--------|
| `usermod -L anna` | Lock the account |
| `usermod -U anna` | Unlock the account |
| `usermod -e 2030-01-01 anna` | Expire the account on January 1, 2030 |
| `usermod -s /sbin/nologin anna` | Set the shell to `nologin` |

Set password aging with `chage`:

```bash
chage [-m mindays] [-M maxdays] [-d lastday] [-E expiredate] [-W warndays] user
```

Set a password with `passwd user`. See `passwd -x -w -i -n` for related options.

## /etc/passwd

This file stores account information. Each line has seven fields:

1. Name
2. Password
3. User ID (UID)
4. Group ID (GID)
5. GECOS (extra information, optional)
6. Home directory
7. Shell

Regular users use `/bin/bash`. System users use `/sbin/nologin`.

## /etc/shadow

This file stores passwords, expiration times, and related data. A `!` before a password means the account is locked.

## /etc/group

This file stores group information, including secondary groups.

Show all members of a group:

```bash
lid -g groupname
```

Set a primary group for the current session:

```bash
newgrp <groupname>
```

## Defaults for new users

- `/etc/skel` contains files that copy into the home directory of each new user.
- `/etc/login.def` sets password defaults. Settings start with `PASS_`. `UMASK` sets the default permissions for new files.

## Sudo

Edit sudo rules with:

```bash
sudo visudo
```

The default sudo timeout is 5 minutes. This line sets it to 60 minutes:

```bash
Defaults    timestamp_type=global,timestamp_timeout=60
```

## Startup files

| File | Applies to |
|------|------------|
| `/etc/profile` | System settings at login |
| `/etc/bashrc` | Subshells |
| `~/.bash_profile` | One user, at login |
| `~/.bashrc` | One user, in subshells |

## Exam tips

- Know the seven fields in `/etc/passwd`.
- A `!` in `/etc/shadow` means the account is locked.
- Root SSH access is denied by default.
- Edit sudo rules with `sudo visudo`.
- Change `/etc/login.def` to change defaults for new users.

Related: [[principle-of-least-privilege]]

[Next: Permissions and Ownership](05-permissions-and-ownership.md)
