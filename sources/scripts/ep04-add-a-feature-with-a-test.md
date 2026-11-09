# Episode 4: Add a Feature with a Test

**Length:** 15 to 17 minutes

**Focus:** Backend, then Frontend

**Learning goals:**
- Write a new REST endpoint: DELETE /api/tasks/<id>
- Write unit tests that mock the database
- Understand HTTP status codes and REST semantics
- Test the feature by hand and in code
- Follow the Git workflow to open a pull request
- Understand test-first thinking

**Prerequisites:**
- Episode 2 complete: Git workflow
- Episode 3 complete: App running locally
- Python familiarity

## 00:00 Hook

**Say:**
- A feature is not done until it is tested.
- Tests let you change code without breaking old behavior.
- Tests also document what the API is supposed to do.
- You will write a test before you write the endpoint. That is test-first thinking.

**Show:** Title screen.

**Expect:** Clear introduction.

## 01:00 The Feature: Delete a Task

**Say:**
- The task board can create and update tasks.
- It cannot delete them.
- Add a DELETE endpoint: `DELETE /api/tasks/<id>`.
- A delete of an existing task returns status 200 and the deleted task as JSON.
- A delete of a missing task returns status 404.
- The frontend will show a delete button for each task.

**Show:** Diagram of the endpoint with request and response examples.

**Expect:** Clear API specification.

## 02:00 Create a Branch

**Say:**
- Start a new branch for this feature.

**Show:** Code snippet:

```shell
git switch -c delete-task
```

**Expect:** You are on the `delete-task` branch.

## 02:30 Write the Test First

**Say:**
- Open `backend/test_app.py`.
- At the top, change the import to `from unittest.mock import MagicMock, patch`.
- Above the `AppTests` class, add the fake database helper:
- First test: delete an existing task. It should return 200 and the task as JSON.

```python
def fake_database(row):
    connection = MagicMock()
    connection.__enter__.return_value.execute.return_value.fetchone.return_value = row
    return connection
```

- At the bottom of the AppTests class, add two test methods.

**Show:** Code snippet to add:

```python
def test_delete_task_returns_deleted_task(self):
    task = {"id": 7, "title": "Write tests", "done": False}

    with patch("app.connect_to_database", return_value=fake_database(task)):
        response = self.client.delete("/api/tasks/7")

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json, task)
```

**Say:**
- The test uses `patch` to replace the `connect_to_database` function with a fake one.
- The fake returns a mock connection that returns the task.
- We call `self.client.delete()` to make a DELETE request.
- We assert that the status code is 200 and the response is the task.

**Show:** Highlighted code in the editor.

**Expect:** Test is added.

**Say:**
- Add a second test: delete a missing task. It should return 404.

**Show:** Code snippet to add:

```python
def test_delete_missing_task_returns_404(self):
    with patch("app.connect_to_database", return_value=fake_database(None)):
        response = self.client.delete("/api/tasks/999")

    self.assertEqual(response.status_code, 404)
```

**Say:**
- When the database returns None (task not found), the endpoint should return 404.

**Show:** Highlighted code in the editor.

**Expect:** Second test is added.

## 04:00 Run the Tests (They Will Fail)

**Say:**
- Run the tests. They will fail because the endpoint does not exist yet.
- That is expected. It is test-first thinking.

**Show:** Code snippet:

```shell
docker compose -f tools/compose.yaml run --rm python-test
```

**Expect:** Tests run and two tests fail with errors about the endpoint not existing.

## 05:00 Write the Endpoint

**Focus:** Backend Engineer task.

**Say:**
- Open `backend/app.py`.
- Find the `update_task` function. Use it as a model.
- Add a delete function after it.

**Show:** Code snippet to add:

```python
@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    with connect_to_database() as connection:
        task = connection.execute(
            "DELETE FROM tasks WHERE id = %s RETURNING id, title, done",
            (task_id,),
        ).fetchone()

    if task is None:
        return jsonify(error="Task not found."), 404
    return jsonify(task)
```

**Say:**
- `@app.delete()` is the route decorator. It maps HTTP DELETE requests to this function.
- The SQL `DELETE ... RETURNING` deletes and returns the row in one query.
- If the query returns None, the task was not found. Return 404.
- If the task was found, return 200 (default) and the task as JSON.

**Show:** Highlighted code in the editor.

**Expect:** Endpoint is added.

## 06:00 Run the Tests (They Will Pass)

**Say:**
- Run the tests again.

**Show:** Code snippet:

```shell
docker compose -f tools/compose.yaml run --rm python-test
```

**Expect:** All tests pass. You see "Ran X tests ... OK".

## 06:30 Concepts: REST and HTTP Status Codes

**Say:**
- REST is a style of API design.
- Each HTTP method means something:
  - GET: retrieve data
  - POST: create data
  - PATCH: update data
  - DELETE: remove data
- Status codes tell the client if the request succeeded:
  - 200: OK, request succeeded
  - 201: Created, a new resource was created
  - 400: Bad request, client sent invalid data
  - 404: Not found, the resource does not exist
  - 500: Server error

**Show:** Table of HTTP methods and status codes.

**Expect:** Concepts are clear.

## 07:30 Add the Delete Button to the Frontend

**Focus:** Frontend Engineer task.

**Say:**
- Open `frontend/app.js`.
- Find the `renderTask` function or similar.
- Add a button that calls the DELETE endpoint.

**Show:** Code snippet (example JavaScript):

```javascript
const deleteButton = document.createElement("button");
deleteButton.textContent = "Delete";
deleteButton.onclick = async () => {
  const response = await fetch(`/api/tasks/${task.id}`, {
    method: "DELETE"
  });
  if (response.ok) {
    loadTasks();
  }
};
taskElement.appendChild(deleteButton);
```

**Say:**
- The button calls `fetch()` with method DELETE.
- If the response is OK (status 200), reload the task list.
- The frontend will show a Delete button on each task.

**Show:** Highlighted code in the editor.

**Expect:** Button is added.

## 08:30 Test by Hand

**Say:**
- Start the full app like in Episode 3.

**Show:** Commands to start database, backend, frontend.

**Say:**
- Open the browser. Add a task.
- Click the Delete button.
- The task is gone.

**Show:** Screenshot of task being deleted from the UI.

**Expect:** Delete works end to end.

## 09:30 Commit and Push

**Say:**
- All the changes are ready.
- Stage all files.

**Show:** Code snippet:

```shell
git add backend/app.py backend/test_app.py frontend/app.js
```

**Say:**
- Commit with a clear message.

**Show:** Code snippet:

```shell
git commit -m "Add DELETE endpoint for tasks"
```

**Say:**
- Push the branch.

**Show:** Code snippet:

```shell
git push -u origin delete-task
```

**Expect:** Branch is pushed.

## 10:30 Open a Pull Request

**Say:**
- Go to GitHub and open a pull request.
- Title: "Add DELETE endpoint for tasks".
- Description: explain what changed and why (e.g., "Users can now delete tasks from the UI").
- Link to the episode or issue if you have one.

**Show:** Screenshot of pull request on GitHub.

**Expect:** Pull request is open.

## 11:00 Review and Merge

**Say:**
- Review the changes yourself. In a team, this is when a teammate would review it.
- If you are happy, merge it.

**Show:** Screenshot of merge button.

**Expect:** PR is merged.

## 11:30 Role Insight: Software Engineer

**Say:**
- Software Engineers write tests alongside the code they write.
- Tests are not optional. They are part of the job.
- When a change breaks a test, the CI system alerts the team before the code is merged.
- You just practiced the discipline that ships reliable software.

## 12:00 CV Skills Unlocked

Add to your skills ledger:

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Python, Flask | 4 | Programming & Scripting | Built a REST endpoint in Flask with input validation and correct status codes |
| Unit testing (unittest, mocks) | 4 | Programming & Scripting | Covered API behavior with unit tests that mock the database layer |

## 13:00 Common Mistakes

- Writing the endpoint before the tests. Test first. It clarifies what the endpoint should do.
- Mocking the wrong function. Make sure the mock path matches the import. Use `patch("app.connect_to_database")`.
- Forgetting to check the status code in the test. Always assert the HTTP status. It is part of the contract.
- Not testing the error case. A test that only tests success is incomplete. Test 404, 400, and other errors.
- Forgetting to commit the test file. Tests are code. They go in Git.

## Outro

**Say:**
- You wrote code and proved it works with tests.
- In Episode 5, you package the app: write Dockerfiles for each service, write docker-compose.yaml, and start the whole stack with one command.
- See you there.

**Show:** Next episode preview: Dockerfiles and Docker Compose.

**Expect:** Teaser for the next episode.
