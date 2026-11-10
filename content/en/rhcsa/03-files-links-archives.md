# 3. Files, Links, and Archives

**Goal:** Copy, find, link, and archive files.

## Copy and find

Copy a directory and its contents:

```bash
cp -r <dir>
```

Find files larger than 100 MB under `/etc` that contain the word `student`:

```bash
find /etc -type f -size +100M -exec grep -l student {} \;
```

| Part | Meaning |
|------|---------|
| `-type f` | Match files only |
| `-size +100M` | Match files larger than 100 MB |
| `-exec ... {} \;` | Run the command on each result. `{}` is the result. `\;` ends the command. |

`xargs` passes the output of one command as arguments to another:

```bash
find / -name '*' -type f | xargs grep "127.0.0.1"
```

## Inodes, hard links, and soft links

An inode is a pointer to a file on the disk.

| | Soft link (`ln -s`) | Hard link (`ln`) |
|---|---------------------|------------------|
| Points to | The file path. Use the full path. | The inode |
| If the original is removed or renamed | The link stays but cannot reach the content. | The link keeps the content. |
| Partition limit | None in the notes | Works only on the same partition |

A copy (`cp`) gets a new inode with the same content. A hard link shares the inode of the original.

```bash
ln -s /full/path/to/file softlink
ln /full/path/to/file hardlink
```

## Archives with tar

`tar` does not compress by default.

```bash
tar -cvf my_arch.tar /home/etc
tar -tvf my_arch.tar
tar -xvf my_arch.tar
tar -xvf my_arch.tar -C <dir>
```

| Command | Action |
|---------|--------|
| `-cvf` | Create an archive |
| `-tvf` | List the contents of an archive |
| `-xvf` | Extract to the current directory |
| `-C <dir>` | Extract to `<dir>` |

Add a compression flag to the command:

| Flag | Compression | Notes |
|------|-------------|-------|
| `-z` | gzip | Fastest |
| `-j` | bzip2 | |
| `-J` | xz | Very good compression, slow |

```bash
tar -czvf my_arch.tar.gz /home/etc
```

Other compression tools: `gzip` (most common), `bzip2`, and `zip`.

## Exam tips

- Remember that `tar` does not compress by default.
- Use the full path for soft links.
- Hard links work only on the same partition.
- Know the difference between a copy and a hard link.

[Next: Users and Groups](04-users-and-groups.md)
