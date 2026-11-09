# Episode 3: Run the App

**Length:** 16 to 18 minutes

**Focus:** Full-Stack

**Learning goals:**
- Understand containers and images
- Create a custom Docker network so containers find each other by name
- Run PostgreSQL, Python Flask, and Nginx in containers on the same network
- Call the API with curl
- Understand environment variables and volume mounts
- Clean up containers and networks

**Prerequisites:**
- Episode 1 complete: Docker Desktop is installed and running
- Episode 2 complete: You have cloned the repository
- Comfort with the terminal or PowerShell

## 00:00 Hook

**Say:**
- Containers are lightweight, isolated environments.
- You can run three services (database, backend, frontend) on your laptop, isolated from each other and from your system.
- One network. Three containers. They find each other by name.

**Show:** Title screen.

**Expect:** Clear introduction.

## 01:00 Containers and Images

**Say:**
- An image is a template. It defines what goes in the container.
- A container is a running instance of an image, like a process.
- When you stop a container, it is gone. Images stay around.
- We use pre-built images from Docker Hub: python, postgres, nginx.

**Show:** Diagram with Image on left (says "blueprint"), Container on right (says "running").

**Expect:** Clear distinction between image and container.

## 02:00 Create a Docker Network

**Say:**
- Docker containers can talk to the internet, but not to each other by default.
- Create a network so three containers can find each other by name.

**Show:** Code snippet:

```shell
docker network create taskboard
```

**Expect:** Network is created. Command prints a network ID.

## 02:30 Start the Database

**Say:**
- Start PostgreSQL. It reads an init file that creates the tasks table.
- Type this command in one line (shown here split into multiple lines for readability).

**Show:** Code snippet:

```shell
docker run -d --name database --network taskboard -e POSTGRES_DB=tasks -e POSTGRES_USER=tasks -e POSTGRES_PASSWORD=change-me -v "${PWD}/database/init.sql:/docker-entrypoint-initdb.d/001-init.sql:ro" postgres:16-alpine
```

**Say:**
- `-d` means "run detached" (in the background).
- `--name database` gives the container a name so other containers can find it.
- `--network taskboard` puts it on the network.
- `-e` sets an environment variable. Three of them set up PostgreSQL.
- `-v` mounts a file. The init.sql file is read-only (`:ro`).

**Expect:** Container starts. Command prints a container ID.

## 04:00 Start the Backend

**Say:**
- Start the Flask API.
- It needs the database host and password as environment variables.
- The backend code is in the `backend/` folder. We mount it as a volume so changes take effect without rebuilding.

**Show:** Code snippet:

```shell
docker run -d --name backend --network taskboard -p 8000:8000 -e DB_HOST=database -e DB_PASSWORD=change-me -v "${PWD}/backend:/app" -w /app python:3.12-slim sh -c "pip install -r requirements.txt && python app.py"
```

**Say:**
- `-p 8000:8000` publishes port 8000. The first number is on your laptop. The second is inside the container.
- `-e DB_HOST=database` tells Flask where the database is. It uses the container name.
- `-v "${PWD}/backend:/app"` mounts the backend folder into the container.
- `-w /app` sets the working directory.
- `sh -c "..."` runs two commands: install requirements, then start Flask.

**Expect:** Backend container starts. Flask begins listening on port 8000.

## 05:30 Start the Frontend

**Say:**
- Start Nginx. It serves static files (HTML, CSS, JavaScript) and forwards `/api/` requests to the backend.

**Show:** Code snippet:

```shell
docker run -d --name frontend --network taskboard -p 8080:80 -v "${PWD}/frontend/nginx.conf:/etc/nginx/conf.d/default.conf:ro" -v "${PWD}/frontend:/usr/share/nginx/html:ro" nginx:1.27-alpine
```

**Say:**
- Port 8080 on your laptop maps to port 80 in the container.
- Two volumes: one for the Nginx config, one for the static files.

**Expect:** Frontend container starts. Nginx is ready.

## 06:30 Check if the Backend is Ready

**Say:**
- The backend needs time to install dependencies and start Flask.
- Call the `/readyz` endpoint. Repeat until it returns "ready".

**Show:** Code snippet (macOS and Linux):

```shell
curl http://localhost:8000/readyz
```

**Say:**
- On Windows PowerShell 5.1, use `curl.exe` instead of `curl`.

**Show:** Code snippet (Windows PowerShell):

```powershell
curl.exe http://localhost:8000/readyz
```

**Say:**
- Keep running the command until the response is `{"status":"ready"}`.

**Expect:** `{"status":"ready"}` is printed. This means the database is reachable and the backend is up.

## 07:30 Open the App in a Browser

**Say:**
- Open http://localhost:8080 in your browser.
- You see a task board with an input field and an empty list.

**Show:** Screenshot of the task board UI.

**Expect:** Frontend is loaded and styled.

**Say:**
- Add a task. Type a title and press the button.

**Show:** Screenshot of a task being added.

**Expect:** Task appears in the list.

## 08:30 Call the API Directly

**Say:**
- The frontend calls the same API you can call from the command line.
- List all tasks.

**Show:** Code snippet (macOS and Linux):

```shell
curl http://localhost:8000/api/tasks
```

**Show:** Code snippet (Windows PowerShell):

```powershell
curl.exe http://localhost:8000/api/tasks
```

**Expect:** Response is a JSON array of task objects:

```json
[
  {
    "id": 1,
    "title": "Learn Docker",
    "done": false
  }
]
```

**Say:**
- The API returns JSON. The frontend parses it and renders it as a table.

## 09:30 Understand Health Checks

**Say:**
- The backend has a `/healthz` endpoint that just says it is alive.
- The `/readyz` endpoint checks if the database is reachable.
- Apps use these endpoints to know when they are ready for traffic.

**Show:** Code snippet:

```shell
curl http://localhost:8000/healthz
```

**Expect:** Response is `{"status":"ok"}`.

## 10:00 View Logs

**Say:**
- Containers have logs. See what the backend is printing.

**Show:** Code snippet:

```shell
docker logs backend
```

**Expect:** Output shows Flask startup messages and request logs.

## 10:30 Clean Up

**Say:**
- Stop and remove the containers.

**Show:** Code snippet:

```shell
docker rm -f frontend backend database
```

**Say:**
- `-f` forces removal even if the container is running.
- `-f frontend backend database` removes three containers in one command.

**Expect:** All three containers are removed.

**Say:**
- Remove the network.

**Show:** Code snippet:

```shell
docker network rm taskboard
```

**Expect:** Network is removed.

## 11:00 Concepts

**Say:**
- Container: A running instance of an image.
- Image: A template that defines what the container contains.
- Port mapping: Forward a port from your laptop to the container.
- Volume mount: Share a file or folder between your laptop and the container.
- Environment variable: Configuration passed into the container.
- Container network: A virtual network so containers can talk to each other.
- Health check: An endpoint that tells if the service is ready.

**Show:** Diagram or glossary table.

**Expect:** Concepts are clear.

## 12:00 Role Insight: Software Engineer

**Say:**
- In a team, every engineer has the full stack running locally.
- You change code and see the result immediately.
- When you are done, you push a commit and the CI system runs the same tests and containers automatically.
- This episode is the foundation for everything else.

## 13:00 CV Skills Unlocked

Add to your skills ledger:

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Docker | 3 | Containers & Orchestration | Containerized a three-tier app (Nginx, Flask, PostgreSQL) with non-root images |
| SQL, PostgreSQL | 3 | Programming & Scripting | Wrote parameterized SQL queries against PostgreSQL |

## 14:00 Common Mistakes

- Windows: Forgetting to use `curl.exe`. The `curl` alias in PowerShell 5.1 does not work the same way.
- Typos in container names. If you use `--name db` but reference `database`, the containers cannot find each other.
- Forgetting to create the network first. Containers on different networks cannot communicate.
- Running out of disk space. Images can be large. Use `docker image prune` to clean up old images.
- Port conflicts: If port 8080 is already in use on your laptop, the frontend will not start. Change `-p 8080:80` to a different port like `-p 8888:80`.

## Outro

**Say:**
- You have the full app running locally.
- In Episode 4, you add a feature: a DELETE endpoint. You write a test for it. You open a pull request.
- See you there.

**Show:** Next episode preview: adding a feature and writing tests.

**Expect:** Teaser for the next episode.
