# Episode 26: Build Your CV

**Length:** 18 to 21 minutes

**Focus:** Overview

**Learning goals:**
- Turn skills ledger rows into CV bullets
- Build the CV from `cv/template.tex` with a Docker LaTeX image
- Polish a GitHub profile so it backs up the CV
- Prepare a short talk track for each role you practiced

**Prerequisites:**
- At least one act complete, with its skills ledger rows filled in

## 00:00 Hook

**Say:**
- You started this course with a degree and no job yet.
- You finish it with four roles practiced, a GitHub project you own, and proof for every line you are about to write.
- Today that proof becomes a CV.

**Show:** The skills ledger, four act sections, each with a resume checkpoint.

## 01:00 Gather Your Skills Ledger

**Say:**
- Open `cv/skills-ledger.md`. Only use the acts you completed; each one stands on its own.
- Each row has a skill, the episode where you practiced it, a CV section, a proof, and an example bullet.

**Show:** The ledger, scrolled from Act 1 through whichever act the student reached.

**Expect:** Students see every skill they can now claim, with a specific proof behind each one.

## 03:00 Fill in the Template

**Say:**
- `cv/template.tex` already has the right section headings: the ones the ledger's **CV section** column points to.
- Copy each skill from the ledger's **TECHNICAL SKILLS** rows into the matching section. Keep the tool names, drop the ones you did not practice.

**Show:**
- Open `cv/template.tex`.
- Match `Containers & Orchestration`, `Infrastructure as Code`, `CI/CD & Automation`, `Monitoring & Observability`, `Programming & Scripting`, `Networking & Security`, and `Operating Systems` against the ledger's section names.
- Replace the placeholder name, contact line, and the example job entries with real ones, or delete a section you do not need yet.

**Expect:** A filled-in skills section and a cleared-out experience section the student will write next.

## 07:00 Build the PDF

**Say:**
- LaTeX needs a full install to render a PDF. This course runs it as a Docker image instead, the same way it ran Ansible and Terraform.

**Show:**

```shell
docker compose -f tools/compose.yaml run --rm latex pdflatex template.tex
```

**Expect:** `cv/template.pdf` appears. Open it and check the layout did not break.

## 09:00 Write Strong Bullets

**Say:**
- Use the ledger's form: **I did X, using Y, which resulted in Z.**
- X is what you built. Y is the tools and methods. Z is the result, with a number when you have one.
- The ledger's example bullets are a starting point, not a copy-paste. Adjust them to match what you actually did, especially if you changed anything from the course.

**Show:** Two ledger bullets rewritten in the student's own words, side by side with the original.

**Expect:** Students see the form holds even when the wording changes.

## 13:00 Polish Your GitHub Profile

**Say:**
- A CV line like "Containerized a three-tier app" is a claim. Your GitHub repository is the proof.
- Three changes make the repository read well to someone who was not in this course: a clear `README.md` at the top, pull request history that shows real review, not just solo commits, and a pinned repository on your GitHub profile.

**Show:**
- The repository's `README.md`, open at the top.
- The merged pull requests from Episodes 2, 4, and 6.
- The GitHub profile page, with this repository pinned.

**Expect:** A reviewer can land on the profile and find the project in one click.

## 16:00 Prepare a Talk Track for Each Role

**Say:**
- An interview asks about a role, not a repository. Prepare one short answer per act you completed: the task, what you built, and one number or result.
- Four acts, four thirty-second answers. You do not perform all four in one interview; you pick the one that matches the job.

**Show:** Four short talk tracks, one per act, each following: task, what you built, result.

**Expect:** Students leave with spoken answers ready, not just written ones.

## 19:00 CV Skills Unlocked

| Skill | Episodes | CV Section | Example bullet |
|---|---|---|---|
| Technical documentation | 7, 26 | Programming & Scripting | Documented architecture, runbooks, and trade-offs for a multi-tier system |

## 19:30 Common Mistakes

- Copying every ledger bullet word for word. Adjust them to match what you actually built.
- Leaving placeholder names or emails in `cv/template.tex`.
- Listing a tool you read about but never used in this course. Only list what the ledger's proof backs up.
- A CV with no matching GitHub activity. Merge your pull requests before you apply anywhere.

## Outro

**Say:**
- Four careers, one project, one CV. You built a task board, ran it on a VM, moved it to Kubernetes, then found and fixed a real vulnerability in it.
- Whichever role you choose next, you now have proof, not just a claim.
- That is the course. Good luck.

**Show:** The four act headlines, side by side: Junior Software Engineer, with Cloud and Infrastructure as Code, Junior DevOps Engineer, Junior Cybersecurity Engineer.
