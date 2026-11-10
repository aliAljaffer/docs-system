# 5. Permissions and Ownership

**Goal:** Set the owner, group, and permissions of files and directories.

!!! warning "Order"
    Set ownership before permissions.

## Ownership

Change the owner and group:

```bash
chown user[:group] file
```

Change the group:

```bash
chgrp <group> <file>
```

## Permission values

| Permission | Value |
|------------|-------|
| `r` (read) | 4 |
| `w` (write) | 2 |
| `x` (execute) | 1 |

Change permissions with `chmod`.

## umask

`UMASK` is subtracted from the default permissions:

| Item | Default | Result |
|------|---------|--------|
| Files | 666 | Default minus `UMASK` |
| Directories | 777 | Default minus `UMASK` |

- `UMASK` is set in `/etc/bashrc`.
- `umask` is also a shell setting.

New permissions equal the default permissions minus the umask.

## Shared group directories

Set the setgid bit on a directory. New files in the directory inherit the directory's group:

```bash
chmod g+s mydir
```

Set the sticky bit. Only the user who created a file can delete it:

```bash
chmod +t mydir
```

## Exam tips

- Set ownership before permissions.
- Know the values: `r` is 4, `w` is 2, and `x` is 1.
- `UMASK` is subtracted from 666 for files and 777 for directories.
- Use the sticky bit on shared group directories.

[Next: Networking](06-networking.md)
