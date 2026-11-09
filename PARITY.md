# Episode page standard

Every episode page must give a reader the same knowledge as the video. The video shows slides and the apply steps. The page must carry the explanation, the steps, the expected output, and the traps.

Canonical location: `four-hats/docs/episodes/epNN-slug.md`.
Assets: `four-hats/docs/assets/diagrams/`.
Source of truth for explanation: `hq-main/scripts/epNN-slug.md`.
Source of truth for verified steps: `four-hats/docs/actN-*.md`.

## Required sections

| Section | Purpose | Gate |
|---|---|---|
| H1 | `CODE-NN: Title` | Required |
| Meta table | Act, focus, time, what you need, what you build, done when | Required |
| What you will be able to do | Learning goals from the script, as outcomes | At least 3 |
| Before you start | Prerequisites from the script | Required for episodes 1 and later |
| Explanation | Why the topic exists, how it works, with a diagram when one exists | At least 300 words |
| Steps | Numbered, imperative, one action per step | At least 2 for hands-on episodes |
| Expected output | The exact result the reader should see, for commands that print | Required when a step runs a command |
| Common mistakes | Traps the video calls out, plus verified failure modes | At least 3 |
| Check your work | Testable checklist | At least 3 boxes |
| CV table | Skill, episode, CV section, example bullet | Required |
| Next | Link to the next episode | Required except the last |

## Rules

- One instruction per sentence. Imperative voice.
- Do not hide required code in a collapsed block. A reader must see the code the video shows.
- Do not write a step the E2E report marks as failing.
- Do not use a command without the expected output.
- Do not present base64 as encryption.
- Keep terms stable: Pod, Deployment, Service, Secret, ConfigMap, MinIO, not synonyms.
- No em dashes.

## Parity gates

`check_parity.py` checks every page against the script:

1. Every learning goal in the script appears as an outcome in the page.
2. Every `Expect:` in the script maps to an expected output in the page.
3. Every code block in the script appears in the page, unless it is a presenter-only direction.
4. Every diagram PNG with an episode prefix appears in the page.
5. The page has the required sections and minimum counts.

A page that fails a gate is not done.
