# 2. Shell and Text Tools

**Goal:** Find help, redirect output, chain commands, and process text in the shell.

## Get help

```bash
whatis <cmd>
<cmd> --help
man <cmd>
where <cmd>
which <cmd>
```

## Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl-c` | Quit the running process |
| `Ctrl-a` | Move to the start of the line |
| `Ctrl-e` | Move to the end of the line |
| `Ctrl-r` | Search history in reverse |
| `Ctrl-l` | Clear the screen |
| `Ctrl-u` | Clear the line |

## History

Shell history is saved in `~/.bash_history`.

| Command | Action |
|---------|--------|
| `!42` | Repeat command 42 from the history |
| `!b` | Repeat the most recent command that starts with `b` |
| `history -w` | Save the current history to the history file |
| `history -d n` | Delete line `n` from the history |
| `history -c` | Clear the history |

## Redirects and pipes

The shell uses three streams:

| Stream | Number |
|--------|--------|
| Standard input (`stdin`) | 0 |
| Standard output (`stdout`) | 1 |
| Standard error (`stderr`) | 2 |

```bash
ls -lah > directory_listing.txt
ls -lah >> directory_listing.txt
cat < file_1
ls -l /root 2> errorfile
ls -l /root 2> /dev/null
```

!!! warning "Overwrite"
    `>` replaces the content of an existing file. Use `>>` to add to the end of a file.

A pipe sends the output of one command to the input of another:

```bash
cmd1 | cmd2
echo hello | tr a-z A-Z
```

## Text tools

| Command | Use |
|---------|-----|
| `less` | View a file one page at a time |
| `head` | Show the first lines (default 10). Use `-n` to set the count. |
| `tail` | Show the last lines (default 10). Use `-n` to set the count. |
| `cat -A` | Show non-printable characters as `$` |
| `cat -b` | Number the lines |
| `cat -s` | Suppress repeated empty lines |
| `tac` | Show a file in reverse order |
| `cut -d : -f 1 /etc/passwd` | Show the first field, using `:` as the separator |
| `sort` | Sort lines |
| `tr` | Translate characters |

```bash
tr '[:lower:]' '[:upper:]'
```

### grep

Put the regex between single quotes.

| Option | Action |
|--------|--------|
| `-v` | Exclude matching lines |
| `-A n` | Show `n` lines after each match |
| `-B n` | Show `n` lines before each match |
| `-R` | Search recursively |
| `-l` | Show only the names of matching files |

### awk

```bash
awk -F : '{ print $4 }' /etc/passwd
awk -F : '{ print $NF }' /etc/passwd
```

`$NF` is the last field.

### sed

!!! warning "In-place edits"
    `sed -i` changes the file itself. Remove `-i` to see the output without a change.

```bash
sed -i 's/boot/beet/g' users
sed -i -e '10d' users
```

The first command replaces every `boot` with `beet`. The second command deletes line 10.

## Shell expansion

```bash
ls *
touch file{1..9}
```

## Variables

```bash
export x=50
```

A variable set without `export` does not pass to subprocesses. A variable does not persist after you log out and log in again.

## Exam tips

- Use `man` and `--help` to check command syntax.
- Put regex patterns in single quotes.
- Use `2> /dev/null` to hide errors.
- Use `Ctrl-r` to search history.

[Next: Files, Links, and Archives](03-files-links-archives.md)
