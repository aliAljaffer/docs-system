# 1. Linux Basics

**Goal:** Know the root directory layout and how to mount a device.

## Everything is a file

In Linux, everything is a file.

## Root directories

| Directory | Purpose |
|-----------|---------|
| `/bin` | Binaries |
| `/sbin` | Superuser binaries |
| `/etc` | Configuration files |
| `/var` | Temporary files and logs. journald is taking over logs. |
| `/tmp` | Temporary files. Any user can write to it. |

For more detail, run:

```bash
man hier
```

## Mounting filesystems

A device must connect to a directory before you can access it. This connection is called mounting.

1. List all devices, including unmounted ones:

    ```bash
    lsblk
    ```

2. Mount a device to a directory:

    ```bash
    mount /dev/<device_name> /<dir_name>
    ```

3. List all mounted devices:

    ```bash
    findmnt
    ```

4. Unmount a device with `umount`.

## Exam tips

- Know what each root directory holds.
- Use `lsblk` to find devices that are not mounted. Use `findmnt` to find mounted devices.
- Use `man hier` to review the file hierarchy.

[Next: Shell and Text Tools](02-shell-and-text.md)
