# Episode 2: Git and GitHub

**Length:** 15 to 17 minutes

**Focus:** Full-Stack

**Learning goals:**
- Fork and clone a repository
- Create a branch to isolate your changes
- Commit changes with clear messages
- Push your branch to GitHub
- Open a pull request
- Merge your pull request
- Understand the workflow that professional teams use

**Prerequisites:**
- Episode 1 complete: Git and GitHub installed, repository forked and cloned
- A text editor or VS Code
- Familiarity with the terminal or PowerShell

## 00:00 Hook

**Say:**
- Git is version control. GitHub is where you back up your work and collaborate.
- The workflow is: branch, commit, push, pull request, merge.
- Thousands of teams use this flow. You are learning what professionals do every day.

**Show:** Title screen.

**Expect:** Clear introduction.

## 01:00 Act 1 Briefing

**Say:**
- Welcome to Act 1. You are the new Software Engineer.
- Previously: Episode 0 showed the four roles. Episode 1 set up your laptop.
- Your task: the task board app works, but users cannot delete a task. It has no tests, no container images, and no automated checks.
- Your goal: ship a delete feature with a test, package the app in containers, and run checks on every pull request.
- Done when: a merged pull request, a stack that starts with one command, and a green CI check.
- Start here if you want only this role. Act 1 needs nothing from other acts, only Episode 1.

**Show:** A briefing card with four lines: Role, Task, Goal, Done when.

## 03:00 The Branch Workflow

**Say:**
- The main branch is production code. You never change it directly.
- For every change, you create a branch.
- A branch is a copy of main where you work safely.
- When the change is ready, you ask for a review with a pull request.
- A teammate looks at it, approves it, and merges it back to main.

**Show:** Diagram of branches: main with two branches (add-readme-note, another-feature) coming off it, then merging back.

**Expect:** Clear visual of the branching model.

## 04:00 Create a Branch

**Say:**
- You are in the `minikube-project` folder.
- Create a branch named `add-readme-note`.

**Show:** Code snippet:

```shell
git switch -c add-readme-note
```

**Say:**
- `git switch` changes which branch you are on.
- `-c` means create a new branch if it does not exist.
- You are now on the `add-readme-note` branch.

**Show:** Terminal output showing branch changed.

**Expect:** Prompt now shows `(add-readme-note)` or similar.

## 05:00 Make a Change

**Say:**
- Open the README.md file in VS Code.
- Add a note at the top: a comment about the course.

**Show:** Screenshot of README.md open in VS Code. Add a line like:

```
<!-- This is my learning project for the four tech careers course. -->
```

**Say:**
- Save the file.

**Expect:** File is modified. VS Code shows a dot on the file tab.

## 05:30 Commit the Change

**Say:**
- Stage the file for commit.

**Show:** Code snippet:

```shell
git add README.md
```

**Say:**
- Now commit with a clear message.

**Show:** Code snippet:

```shell
git commit -m "Add a note to the README"
```

**Say:**
- A commit is a snapshot of your changes.
- The message is short and describes what you did, not how.

**Expect:** Terminal shows "1 file changed, 1 insertion(+)".

## 06:30 Push the Branch

**Say:**
- Your change is saved locally. Now push it to GitHub.

**Show:** Code snippet:

```shell
git push -u origin add-readme-note
```

**Say:**
- `origin` is GitHub, the remote repository.
- `-u` means "set upstream", so the branch tracks the remote.
- Your branch is now on GitHub.

**Expect:** Terminal shows the branch was pushed.

## 07:30 Open a Pull Request

**Say:**
- Go to GitHub.com and open your fork.
- You will see a yellow banner asking if you want to open a pull request.
- Click it. Or click the Pull Requests tab, then New Pull Request.

**Show:** Screenshots of GitHub showing the pull request creation flow.

**Say:**
- The PR is from your `add-readme-note` branch to the `main` branch of your fork.
- Add a title and description. Keep them clear.

**Show:** Screenshot of pull request form with title "Add a note to the README" and a short description.

**Expect:** Pull request is open.

## 08:30 Review and Merge

**Say:**
- In a team, someone else reviews your PR.
- They read your code, ask questions, suggest improvements.
- Since this is your fork, you can review it yourself.
- If you are happy with it, click Merge Pull Request.

**Show:** Screenshot of merge button in the PR.

**Say:**
- The branch is merged into main.
- You can delete the branch now.

**Expect:** PR is closed. Branch is merged.

## 09:30 Switch Back to Main

**Say:**
- Switch back to the main branch to see your change.

**Show:** Code snippet:

```shell
git switch main
git pull
```

**Say:**
- `git pull` fetches the latest changes from GitHub.
- Your README note is now in main.

**Expect:** Local main branch is up to date.

## 10:00 Concepts

**Say:**
- Repository: A folder that Git tracks. Your code lives here.
- Commit: A snapshot of your changes. Each commit has a unique ID.
- Branch: A separate line of work. You can have many branches.
- Remote: GitHub, where your repository is backed up.
- Fork: Your own copy of someone else's repository.
- Pull Request: A way to ask for a code review before merging.
- Merge: Combine changes from one branch into another.

**Show:** Diagram or table of terms with examples.

**Expect:** Glossary is clear and visual.

## 11:00 Role Insight: Software Engineer

**Say:**
- Software Engineers use this workflow many times a day.
- Every change goes through a pull request. No one commits directly to main.
- This is how teams stay organized and catch bugs before they ship.
- You just practiced what your team will expect of you.

## 12:00 CV Skills Unlocked

Add to your skills ledger:

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Git, GitHub | 2 | Programming & Tools | Managed changes with feature branches and pull requests on GitHub |

## 13:00 Common Mistakes

- Committing to main instead of a branch. Always create a branch first.
- Forgetting `-u` when pushing. Your next push will fail because the branch is not tracked.
- Writing unclear commit messages like "fix stuff" or "asdf". Use clear, present-tense messages: "Add delete endpoint", "Fix race condition in startup".
- Merging without reviewing your own code. Always read diffs before merging.
- Windows: Using the wrong `curl`. Use `curl.exe` if the command asks for a URL.

## Outro

**Say:**
- You know the Git workflow now.
- In Episode 3, you run the app. The backend, the database, and the frontend all run in containers on one network.
- See you there.

**Show:** Next episode preview: running containers and calling the API.

**Expect:** Teaser for the next episode.
