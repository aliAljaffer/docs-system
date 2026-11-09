# Episode 24: Broken Access Control

**Length:** 30 to 35 minutes

**Focus:** Security Engineer (defensive)

**Learning goals:**
- Explain OWASP A01, Broken Access Control, and IDOR (Insecure Direct Object Reference) as one named pattern
- Add real users: registration with bcrypt-hashed passwords, login with a signed JWT
- Explain why "the request was authenticated" and "the request was authorized" are different questions
- Reproduce an IDOR step by step, then close it with an ownership check
- Choose 404 over 403 so a fix does not leak which objects exist

**Prerequisites:**
- Episode 23 complete
- `docker compose up --build` working from Episode 3

## 00:00 Hook

**Say:**
- The SQL injection was a classic beginner bug. This one is more common, and far easier to miss: the app has no concept of "mine" versus "yours."
- Today you add real users, then watch one user delete another user's task using nothing but their own valid login.

**Show:** Title screen.

## 01:00 OWASP A01: Broken Access Control

**Say:**
- Authentication answers "who are you?" Authorization answers "are you allowed to do this?" An app can get the first one right and still fail the second.
- OWASP ranks Broken Access Control as the number one web application risk, ahead of injection.
- Today's specific bug has a name: IDOR, Insecure Direct Object Reference. The app takes an ID straight from the request and acts on it, without checking that the caller owns the thing that ID points to.

**Show:** The OWASP Top 10 list from Episode 20, with A01 highlighted.

## 03:00 Before You Start

**Say:**
- This episode changes the database schema. It adds two Python packages. It adds one environment variable. Do these steps before you continue. The stack will not start if you skip them.

**Show:**
1. Add the two packages to `backend/requirements.txt`:

```text
bcrypt>=4.2,<5
PyJWT>=2.9,<3
```

2. Add `JWT_SECRET` to `.env`:

```text
JWT_SECRET=change-me-locally-too
```

Episode 5 copied `.env` from `.env.example`. If you change only the example, your `.env` does not change.

3. Reset the database volume:

Warning: this command deletes all data in your local database.

```shell
docker compose down -v
```

PostgreSQL runs `init.sql` only on an empty data directory. `docker compose up --build` alone keeps the old schema. The `users` table and the `owner_id` column do not appear.

4. Add the `/pentest` page files to `frontend/`:
   - `pentest.html`
   - `pentest.css`
   - `pentest.js`

If your fork does not have these files, copy them from `act-4-cybersecurity-engineer/frontend/` in the solved repository.

5. Add the three files to the `COPY` line in `frontend/Dockerfile`.

**Expect:** The stack builds. The database has the new schema. The frontend serves `/pentest`.

## 04:00 Add Users

**Say:**
- The app has never had users. Add a users table. Add a registration endpoint.

**Show:** `database/init.sql`:

```sql
CREATE TABLE users (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username varchar(32) NOT NULL UNIQUE,
    password_hash text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE tasks (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    owner_id integer NOT NULL REFERENCES users (id),
    title varchar(120) NOT NULL,
    done boolean NOT NULL DEFAULT false,
    created_at timestamptz NOT NULL DEFAULT now()
);
```

The `owner_id` column is new. The volume reset above is what makes this schema take effect.

`backend/app.py`:

```python
@app.post("/api/auth/register")
def register():
    data = request.get_json(silent=True)
    username = data.get("username") if isinstance(data, dict) else None
    password = data.get("password") if isinstance(data, dict) else None

    if not isinstance(username, str) or not 3 <= len(username) <= 32:
        return jsonify(error="Username must contain 3 to 32 characters."), 400
    if not isinstance(password, str) or len(password) < 8:
        return jsonify(error="Password must contain at least 8 characters."), 400

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    ...
```

**Say:**
- Never store a password itself. `bcrypt.hashpw` stores a salted hash; even you, reading the database, cannot recover the original password.

## 07:00 Add Login and JWT Bearer Tokens

**Show:** `backend/app.py`:

```python
@app.post("/api/auth/login")
def login():
    ...
    if user is None or not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return jsonify(error="Invalid username or password."), 401

    token = jwt.encode(
        {"sub": str(user["id"]), "exp": expires_at}, get_jwt_secret(), algorithm="HS256"
    )
    return jsonify(token=token)
```

**Say:**
- A JWT is a signed claim, not a secret the server stores per session. Anyone with the signing key can verify a token is genuine, but nobody without it can forge one.
- `JWT_SECRET` is a new environment variable, read the same way `DB_PASSWORD` is: required, never defaulted, never committed.

**Show:** Add `JWT_SECRET` to `.env.example` and `compose.yaml`, the same pattern as `DB_PASSWORD`.

## 10:00 Require a Token

**Show:** `backend/app.py`, a decorator applied to every task endpoint:

```python
def require_auth(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return jsonify(error="Authentication required."), 401
        try:
            payload = jwt.decode(header.removeprefix("Bearer "), get_jwt_secret(), algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return jsonify(error="Invalid or expired token."), 401
        g.user_id = int(payload["sub"])
        return view(*args, **kwargs)
    return wrapped
```

**Expect:** Every `/api/tasks*` route now needs `Authorization: Bearer <token>`. `/healthz`, `/readyz`, `/metrics`, and `/api/demo/work` stay public on purpose: probes and the load generator have no login.

## 12:00 Scope Tasks to Their Owner

**Say:**
- Add `owner_id` to the `tasks` table. List, create, and search now filter by the caller, not the whole table.

**Show:**

```python
@app.get("/api/tasks")
@require_auth
def list_tasks():
    with connect_to_database() as connection:
        tasks = connection.execute(
            "SELECT id, title, done FROM tasks WHERE owner_id = %s ORDER BY id DESC",
            (g.user_id,),
        ).fetchall()
    return jsonify(tasks)
```

**Expect:** Two different users see two different, non-overlapping task lists.

## 14:30 Reproduce the IDOR, Step by Step

**Say:**
- The list is scoped correctly. The bug is somewhere else: the endpoints that take a task ID directly. Let's find it, the same way a real attacker would, with two real accounts.

**Show:**

```shell
docker compose up --build -d
```

**Say:**
- The command blocks in this episode are bash. On Windows PowerShell 5.1, use `curl.exe`. Do not use `curl`. Set variables with `$env:ALICE_TOKEN = ...`. If `python3` is not on PATH, use `python`.

**Step 1: register two users.**

```shell
curl -s -XPOST -H 'Content-Type: application/json' \
  -d '{"username":"alice","password":"correct-horse-batt"}' \
  localhost:8080/api/auth/register
```

**Expect:** `{"id":1,"username":"alice"}`

```shell
curl -s -XPOST -H 'Content-Type: application/json' \
  -d '{"username":"bob","password":"correct-horse-batt"}' \
  localhost:8080/api/auth/register
```

**Expect:** `{"id":2,"username":"bob"}`

**Step 2: log in as both, and save each token.**

```shell
ALICE_TOKEN=$(curl -s -XPOST -H 'Content-Type: application/json' \
  -d '{"username":"alice","password":"correct-horse-batt"}' \
  localhost:8080/api/auth/login | python3 -c "import sys,json;print(json.load(sys.stdin)['token'])")

BOB_TOKEN=$(curl -s -XPOST -H 'Content-Type: application/json' \
  -d '{"username":"bob","password":"correct-horse-batt"}' \
  localhost:8080/api/auth/login | python3 -c "import sys,json;print(json.load(sys.stdin)['token'])")
```

**Step 3: alice creates a task. Save its ID.**

```shell
TASK=$(curl -s -XPOST -H "Authorization: Bearer $ALICE_TOKEN" -H 'Content-Type: application/json' \
  -d '{"title":"Alice secret plan"}' localhost:8080/api/tasks)
echo "$TASK"
TASK_ID=$(printf '%s' "$TASK" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])")
echo "Alice task id: $TASK_ID"
```

**Expect:** `{"done":false,"id":<id>,"title":"Alice secret plan"}`. The ID is 1 only on a brand new database. Use the value you just saved.

**Step 4: confirm bob's own list is empty.** This proves the list endpoint is correctly scoped; the bug is not there.

```shell
curl -s -H "Authorization: Bearer $BOB_TOKEN" localhost:8080/api/tasks
```

**Expect:** `[]`

**Step 5: bob deletes Alice's task, using only his own valid token. He never saw this task in his own list.**

```shell
curl -s -o /dev/null -w "status=%{http_code}\n" \
  -XDELETE -H "Authorization: Bearer $BOB_TOKEN" localhost:8080/api/tasks/$TASK_ID
```

**Expect:** `status=200`. Bob deleted Alice's task. He is authenticated as himself and authorized for nothing of hers, and the app let him anyway.

**Say:**
- Task IDs are sequential integers, starting at 1. Bob did not need to guess Alice's ID; he could enumerate every ID from 1 upward and delete or modify whatever existed. That is what makes this an IDOR, not a one-off mistake: the object reference itself is the attack surface.

## 19:30 The Same Attack, in the Security Console

**Say:**
- Everything you just typed is also one page: `/pentest`, served by the same frontend you already have running. It calls the same API over the same origin, nothing simulated.
- The same page has a first panel for the Episode 21 SQL injection, with normal, tautology, and UNION presets. Since that bug is already fixed as of Episode 22, running it now proves the fix still holds; it is a quick regression check, not a re-enactment of the original exploit.

**Show:** Open `http://localhost:8080/pentest`.
- In the "User A" panel, register and log in as `alice`, then create a task.
- In the "User B" panel, register and log in as `bob`.
- In User B's panel, enter the task ID from User A's list and select "Delete this task ID."

**Expect:** The verdict line reads "VULNERABLE: User B deleted a task they do not own," in red, with the raw `200` response underneath.

**Say:**
- This page does not change when the fix ships. Rebuild the backend after the next section and run the exact same clicks again; the verdict turns green. That is the proof the fix works, not a new test written to match the fix.

## 20:30 Fix: Check Ownership, Not Just Existence

**Show:** `backend/app.py`, before and after:

```python
# Before
"DELETE FROM tasks WHERE id = %s RETURNING id, title, done", (task_id,)

# After
"DELETE FROM tasks WHERE id = %s AND owner_id = %s RETURNING id, title, done", (task_id, g.user_id)
```

Same change on `PATCH`.

**Say:**
- A task that exists but belongs to someone else, and a task that does not exist at all, now look identical to the caller: both return 404.
- Returning 403 instead would confirm "this task exists, you just can't touch it," which hands an attacker a free existence check across every ID. 404 gives away nothing.

## 23:00 Re-run the Exact Same Attack

**Show:**

```shell
docker compose up --build -d backend

SECOND=$(curl -s -XPOST -H "Authorization: Bearer $ALICE_TOKEN" -H 'Content-Type: application/json' \
  -d '{"title":"Alice second secret"}' localhost:8080/api/tasks)
echo "$SECOND"
SECOND_ID=$(printf '%s' "$SECOND" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])")

curl -s -o /dev/null -w "status=%{http_code}\n" \
  -XDELETE -H "Authorization: Bearer $BOB_TOKEN" localhost:8080/api/tasks/$SECOND_ID
```

**Expect:** `status=404`. Same attacker, same valid token, same endpoint. The task survives.

**Show:**

```shell
curl -s -XDELETE -H "Authorization: Bearer $ALICE_TOKEN" localhost:8080/api/tasks/$SECOND_ID
```

**Show:** Reload `http://localhost:8080/pentest`, repeat the same clicks from the earlier section: User A creates a task, User B tries to delete it by ID.

**Expect:** The verdict line now reads "Safe: the ownership check blocked this (404, task untouched)," in green. Same page, same clicks, opposite result.

**Expect:** Alice can still delete her own task. The fix removes one specific permission, not the feature.

## 26:00 Write the Regression Test

**Say:**
- Add the test imports. Add the token helper. Add the auth header helper. Then add the test.

**Show:** `backend/test_app.py`:

```python
import os
from unittest.mock import MagicMock, patch

os.environ.setdefault("JWT_SECRET", "test-secret-at-least-32-bytes-long")

import jwt

from app import JWT_ALGORITHM, get_jwt_secret


def make_token(user_id):
    return jwt.encode({"sub": str(user_id)}, get_jwt_secret(), algorithm=JWT_ALGORITHM)


def auth_header(user_id):
    return {"Authorization": f"Bearer {make_token(user_id)}"}
```

```python
@patch("app.connect_to_database")
def test_delete_task_is_scoped_to_the_caller(self, mock_connect_to_database):
    mock_connection = MagicMock()
    mock_connection.execute.return_value.fetchone.return_value = None
    mock_connect_to_database.return_value.__enter__.return_value = mock_connection

    response = self.client.delete("/api/tasks/1", headers=auth_header(user_id=42))

    self.assertEqual(response.status_code, 404)
    sql, params = mock_connection.execute.call_args.args
    self.assertIn("owner_id", sql)
    self.assertEqual(params, (1, 42))
```

**Say:**
- The assertion checks the SQL and its parameters, not only the response. A test that only checks "200 or not" would pass even if the ownership filter were quietly removed again, as long as some database state happened to return the right status.

## 28:00 Role Insight: Security Engineer (defensive)

**Say:**
- This bug shipped because building the feature and securing the feature felt like the same task, so the second half got skipped.
- Every endpoint that accepts an ID from the caller needs the same question asked of it: does this caller own this object? List endpoints are easy to get right because they start from "what is mine." Direct-access endpoints are easy to get wrong because they start from "what is this ID."

## 29:00 CV Skills Unlocked

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| OWASP A01, Broken Access Control, IDOR | 24 | Networking & Security | Identified and reproduced an Insecure Direct Object Reference end to end |
| Authentication (bcrypt, JWT) | 24 | Programming & Scripting | Implemented registration and login with bcrypt-hashed passwords and signed JWT bearer tokens |
| Authorization (ownership checks) | 24 | Programming & Scripting | Added per-object ownership checks that stopped one authenticated user from modifying another's data |
| Secure error design (404 vs. 403) | 24 | Networking & Security | Chose a response code that fixed an access control bug without creating an object-existence oracle |

## 30:00 Common Mistakes

- Scoping the list endpoint and assuming every other endpoint is now safe by association. Check each endpoint that takes an ID on its own.
- Returning 403 for an object the caller does not own. It confirms the object exists; prefer 404.
- Testing only "did the request succeed," never which row the query actually touched.
- Storing a password instead of a hash, or hashing without a per-password salt. `bcrypt.gensalt()` handles this; never write your own.
- Opening `/pentest` with a static-file previewer like VS Code's Live Server instead of `docker compose up`. A plain static server has no `/api/` proxy; register and login return `405`, because the previewer itself rejects POST, not because the app is broken. Always load `/pentest` from `http://localhost:8080`.

## Outro

**Say:**
- Two real users, one line of SQL missing an owner check, one authenticated attacker. You found it, reproduced it, and fixed it.
- In Episode 25, the app gets a second real secret, its JWT signing key, and you learn to commit a secret to Git safely, encrypted.

**Show:** Next episode preview: Sealed Secrets.
