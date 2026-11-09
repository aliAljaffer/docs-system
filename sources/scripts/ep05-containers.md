# Episode 5: Containers

**Length:** 15 to 17 minutes

**Focus:** Full-Stack

**Learning goals:**
- Understand Dockerfile layers and build cache
- Write Dockerfiles with non-root users for security
- Understand base images and image tags
- Write docker-compose.yaml to define services
- Use depends_on to control startup order
- Use health checks to know when services are ready
- Build and run a multi-service stack with one command

**Prerequisites:**
- Episode 3 complete: Containers running manually
- Episode 4 complete: Feature is done
- Comfort with the Docker command line

## 00:00 Hook

**Say:**
- In Episode 3, you ran containers manually with long docker run commands.
- That is not scalable. One typo and the app does not work.
- Docker has two tools to solve this:
  - Dockerfiles define how to build an image.
  - docker-compose.yaml defines a multi-service stack.
- One file. One command. Services start in order.

**Show:** Title screen.

**Expect:** Clear introduction.

## 01:00 Dockerfiles and Layers

**Say:**
- A Dockerfile is a recipe for an image.
- Each line creates a layer. Layers are cached.
- If you change line 5, Docker rebuilds from line 5 onward.
- If you change line 20, Docker uses the cache for lines 1 to 19.
- This makes builds fast.

**Show:** Diagram showing layers stacking up, with labels like FROM, RUN, COPY, etc.

**Expect:** Clear visual of layering and caching.

## 02:00 Write the Backend Dockerfile

**Say:**
- Create `backend/Dockerfile`.
- Start from `python:3.12-slim`. This is a base image.

**Show:** Code snippet:

```dockerfile
FROM python:3.12-slim
```

**Say:**
- Set environment variables for Python.

**Show:** Code snippet to add:

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
```

**Say:**
- Set the working directory.

**Show:** Code snippet to add:

```dockerfile
WORKDIR /app
```

**Say:**
- Copy the requirements file and install dependencies. Do this before copying code.
- If code changes, Docker uses the cached layer. If dependencies change, Docker rebuilds.

**Show:** Code snippet to add:

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

**Say:**
- Create a non-root user. Containers should not run as root.

**Show:** Code snippet to add:

```dockerfile
RUN groupadd --system app \
    && useradd --system --gid app --home-dir /app app
```

**Say:**
- Copy the app code.

**Show:** Code snippet to add:

```dockerfile
COPY --chown=app:app app.py .
```

**Say:**
- Switch to the non-root user.

**Show:** Code snippet to add:

```dockerfile
USER app
EXPOSE 8000
```

**Say:**
- The CMD is how the container starts.

**Show:** Code snippet to add:

```dockerfile
CMD ["gunicorn", "--bind=0.0.0.0:8000", "--workers=1", "app:app"]
```

**Say:**
- We use gunicorn instead of Flask's development server. Gunicorn is production-ready.

**Expect:** Dockerfile is complete.

## 03:30 Write the Frontend Dockerfile

**Say:**
- Create `frontend/Dockerfile`.
- Start from `nginx:1.27-alpine`.

**Show:** Code snippet:

```dockerfile
FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html styles.css app.js /usr/share/nginx/html/

EXPOSE 80
```

**Say:**
- Copy the config and the static files.
- Nginx serves them on port 80.
- No build or dependencies. Just copy and serve.

**Expect:** Frontend Dockerfile is complete.

## 04:30 Write the Database Dockerfile

**Say:**
- Create `database/Dockerfile`.
- Start from `postgres:16-alpine`.

**Show:** Code snippet:

```dockerfile
FROM postgres:16-alpine

COPY init.sql /docker-entrypoint-initdb.d/001-init.sql
```

**Say:**
- PostgreSQL runs any .sql files in `/docker-entrypoint-initdb.d/` on first start.
- This creates the tasks table automatically.

**Expect:** Database Dockerfile is complete.

## 05:00 Write the Compose File

**Say:**
- Create `compose.yaml` in the repository root.
- Define three services: database, backend, frontend.

**Show:** Code snippet:

```yaml
services:
  database:
    build: ./database
    environment:
      POSTGRES_DB: tasks
      POSTGRES_USER: tasks
      POSTGRES_PASSWORD: ${DB_PASSWORD:?Set DB_PASSWORD in .env}
    volumes:
      - database-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U tasks -d tasks"]
      interval: 5s
      timeout: 3s
      retries: 10
```

**Say:**
- `build: ./database` tells Compose to build the Dockerfile in the database folder.
- `environment:` sets environment variables inside the container.
- `${DB_PASSWORD:?...}` reads DB_PASSWORD from the .env file. The `:?` means error if it is not set.
- `volumes:` creates a named volume so data persists when the container stops.
- `healthcheck:` runs `pg_isready` every 5 seconds. The backend waits for this to pass.

**Show:** Highlighted YAML in the editor.

**Expect:** database service is defined.

**Say:**
- Add the backend service.

**Show:** Code snippet to add:

```yaml
  backend:
    build: ./backend
    environment:
      DB_HOST: database
      DB_NAME: tasks
      DB_USER: tasks
      DB_PASSWORD: ${DB_PASSWORD:?Set DB_PASSWORD in .env}
    depends_on:
      database:
        condition: service_healthy
```

**Say:**
- `depends_on:` with `condition: service_healthy` tells Compose: start backend only after database is healthy.
- This prevents the backend from trying to connect to a database that is not ready.

**Show:** Highlighted YAML in the editor.

**Expect:** backend service is defined.

**Say:**
- Add the frontend service.

**Show:** Code snippet to add:

```yaml
  frontend:
    build: ./frontend
    ports:
      - "8080:80"
    depends_on:
      - backend
```

**Say:**
- `ports:` maps port 8080 on your laptop to port 80 in the container.
- `depends_on:` with just a list (not condition) means "start after backend".

**Show:** Highlighted YAML in the editor.

**Expect:** frontend service is defined.

**Say:**
- At the end, define the named volume.

**Show:** Code snippet to add:

```yaml
volumes:
  database-data:
```

**Expect:** compose.yaml is complete.

## 06:30 Create the .env File

**Say:**
- Copy the example environment file.

**Show:** Code snippet:

```shell
cp .env.example .env
```

**Say:**
- The `.env` file is in the .gitignore. It has secrets. Never commit it.
- It sets DB_PASSWORD for Compose to read.

**Expect:** .env file exists.

## 07:00 Build and Start

**Say:**
- Build the images and start the services.

**Show:** Code snippet:

```shell
docker compose up --build
```

**Say:**
- `--build` rebuilds images if Dockerfiles changed.
- Compose creates a network, starts services in order, and shows logs.
- Wait until you see lines like "backend listening" or similar.

**Show:** Terminal output of Compose starting services.

**Expect:** All three services start and are healthy.

## 08:30 Test the App

**Say:**
- Open http://localhost:8080 in the browser.
- Add a task. Delete it.
- All features work.

**Show:** Screenshot of the task board with a task being added and deleted.

**Expect:** App works end to end.

## 09:00 View Logs

**Say:**
- While `docker compose up` is running, logs from all services appear on screen.
- To see logs from one service:

**Show:** Code snippet (in another terminal):

```shell
docker compose logs backend -f
```

**Say:**
- `-f` means "follow", like `tail -f`. New lines appear as they happen.

**Expect:** Backend logs are shown.

## 09:30 Stop the Stack

**Say:**
- In the terminal where `docker compose up` is running, press Ctrl+C.
- Compose stops all services.

**Show:** Terminal showing services stopping.

**Expect:** All containers are stopped.

## 10:00 Clean Up

**Say:**
- Delete the volume so data does not persist to the next run.
- Useful for testing. You start with a clean database each time.

**Show:** Code snippet:

```shell
docker compose down -v
```

**Say:**
- `-v` means "remove volumes".
- Without `-v`, the volume persists. Good for development. With `-v`, good for test scenarios.

**Expect:** Containers are removed. Volume is deleted.

## 10:30 Concepts

**Say:**
- Dockerfile: A recipe for an image.
- Layer: A step in a Dockerfile. Layers are cached.
- Base image: An existing image you build on top of (python, nginx, postgres).
- Image tag: A name and version for an image (python:3.12-slim, nginx:1.27-alpine).
- Non-root user: Running as a regular user instead of root is more secure.
- Compose service: An entry in docker-compose.yaml that defines one container.
- Named volume: A volume that persists data between container restarts.
- Depends_on: Control the startup order of services.
- Health check: A test to see if a service is ready.

**Show:** Diagram or glossary.

**Expect:** Concepts are clear.

## 11:30 Role Insight: Software Engineer

**Say:**
- Software Engineers write Dockerfiles and Compose files so others can run the app locally.
- A new team member can clone the repo, run `docker compose up`, and have the full stack in seconds.
- This is what removes friction from development.

## 12:00 CV Skills Unlocked

Add to your skills ledger:

| Skill | Episode | CV Section | Example bullet |
|---|---|---|---|
| Docker | 5 | Containers & Orchestration | Containerized a three-tier app (Nginx, Flask, PostgreSQL) with non-root images |
| Docker Compose | 5 | Containers & Orchestration | Defined a multi-service stack with health checks and startup order in Docker Compose |

## 13:00 Common Mistakes

- Copying code before installing dependencies. Install dependencies first so the layer can be cached.
- Running the container as root. Always create a non-root user.
- Using the wrong base image tag. `python:latest` changes. Use `python:3.12-slim` to pin a version.
- Forgetting `--build` when rebuilding. `docker compose up --build` rebuilds. `docker compose up` uses the cached image.
- Not mounting code as a volume in development. Changes to code inside the container are lost when it stops.
- Committing .env to Git. It has secrets. Use .env.example as a template.
- Windows: Using PowerShell variable syntax instead of .env. Use `${VAR}` not `$VAR` in compose.yaml.

## Outro

**Say:**
- You have a Compose file. One command starts the full stack.
- In Episode 6, you set up GitHub Actions. Tests and builds run automatically on every pull request.
- See you there.

**Show:** Next episode preview: CI/CD and GitHub Actions.

**Expect:** Teaser for the next episode.
