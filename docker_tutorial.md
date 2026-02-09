# Docker Tutorial: Building and Running the Book API

This guide walks you through converting the Dockerfile into a Docker image and running it as a container.

## Prerequisites

- Docker Desktop installed and running
- Terminal/Command Prompt open in the project directory (`c:\Users\Faraz\Desktop\Docker`)

---

## The Dockerfile

```dockerfile
# Base image - Using slim version of Python 3.12 for smaller image size
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install uv package manager
RUN pip install --no-cache-dir uv

# Copy dependency files first (better Docker cache)
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Expose the application port
EXPOSE 8000

# Image metadata
LABEL NAME="FastAPI Application" \
      VERSION="1.0" \
      DESCRIPTION="A FastAPI application running in a Docker container" \
      AUTHOR="Faraz Ahmed"

# Start the application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**Key Instructions Explained:**

| Instruction | Purpose |
|-------------|---------|
| `FROM` | Specifies the base image (Python 3.12 slim) |
| `WORKDIR` | Sets the working directory inside the container |
| `RUN` | Executes commands during image build |
| `COPY` | Copies files from host to container |
| `EXPOSE` | Documents which port the container listens on |
| `LABEL` | Adds metadata to the image |
| `CMD` | Default command to run when container starts |

---

## Step 1: Verify Docker is Running

```bash
docker --version
```

You should see output like `Docker version 24.x.x` confirming Docker is installed.

---

## Step 2: Build the Docker Image

Run the following command from the project root (where the Dockerfile is located):

```bash
docker build -t book-api .
```

Or with a specific tag to version your image:

```bash
docker build -t cloud-native-fastapi:dev .
```

> If you don't specify a tag, Docker will tag it as `latest` by default.

To use a custom Dockerfile (e.g., for development), use the `-f` flag:

```bash
docker build -f Dockerfile.DEV -t book-api:dev .
```

**Explanation:**

| Part | Meaning |
|-----------|---------|
| `docker build` | Command to build an image from a Dockerfile |
| `-t book-api` | Tags/names the image as "book-api" |
| `-f Dockerfile.DEV` | Specifies a custom Dockerfile instead of the default `Dockerfile` |
| `.` | Build context — tells Docker to use the current directory for the Dockerfile and all files needed during the build |

**Image Naming Rules:**

- Allowed: lowercase letters, numbers, hyphens (`-`), underscores (`_`)
- Not allowed: spaces or uppercase letters

**Expected output:**

```
[+] Building 45.2s (10/10) FINISHED
 => [internal] load build definition from Dockerfile
 => [1/5] FROM python:3.12-slim
 => [2/5] WORKDIR /app
 => [3/5] RUN pip install --no-cache-dir uv
 => [4/5] COPY pyproject.toml uv.lock ./
 => [5/5] RUN uv sync --frozen --no-dev
 => [6/6] COPY . .
 => exporting to image
 => naming to docker.io/library/book-api
```

---

## Step 3: Verify the Image Was Created

```bash
docker images
```

Look for `book-api` in the list:

```
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
book-api     latest    abc123def456   10 seconds ago   250MB
```

---

## Step 4: Run the Container

```bash
docker run -p 8000:8000 book-api
```

**Explanation:**

| Part | Meaning |
|------|---------|
| `docker run` | Command to create and start a container |
| `-p 8000:8000` | Maps port 8000 on your machine to port 8000 in the container |
| `book-api` | The image name to run |

> **`docker run` vs `docker start`:**
>
> | Command | What it does |
> | -------------- | ------------------------------------------ |
> | `docker run` | Creates a **new** container from an image |
> | `docker start` | Restarts an **existing** stopped container |
>
> Use `docker run` the first time. After that, use `docker start <container-name>` to restart the same container without creating a duplicate.

---

## Step 5: Access the Application

Open your browser and navigate to:

- **API Root:** <http://localhost:8000>
- **Swagger Docs:** <http://localhost:8000/docs>
- **ReDoc:** <http://localhost:8000/redoc>

---

## Step 6: Stop the Container

Press `Ctrl + C` in the terminal where the container is running.

---   

## Additional Commands

### Run in Detached Mode (Background)

```bash
docker run -d -p 8000:8000 --name book-api-container book-api
```

| Flag | Meaning |
|------|---------|
| `-d` | Run in detached/background mode |
| `--name book-api-container` | Assign a name to the container |

### View Running Containers

```bash
docker ps
```

### Stop a Detached Container

```bash
docker stop book-api-container
```

### Remove a Container

```bash
docker rm book-api-container
```

### Remove the Image

```bash
docker rmi book-api
```

### Rebuild After Code Changes

```bash
docker build -t book-api .
docker run -p 8000:8000 book-api
```

---

## Quick Reference

| Action | Command |
|--------|---------|
| Build image | `docker build -t book-api .` |
| Build image with tag | `docker build -t cloud-native-fastapi:dev .` |
| Run container | `docker run -p 8000:8000 book-api` |
| Run in background | `docker run -d -p 8000:8000 --name book-api-container book-api` |
| List images | `docker images` |
| List running containers | `docker ps` |
| List all containers | `docker ps -a` |
| Stop container | `docker stop <container-name>` |
| Remove container | `docker rm <container-name>` |
| Remove image | `docker rmi book-api` |
| View container logs | `docker logs <container-name>` |

## My Docker Image Diagram

## Error Diagram

![alt text](image.png)

## Build Image Diagram

![Build Image](build-image.png)

---

## Terminal Output Behavior in Docker

### Seeing output from a stopped container

`docker start` runs in detached mode by default — you won't see any output. Use the `-a` flag to **attach** your terminal:

```bash
docker start -a <container-name>
```

You can also view output **after** a container has finished:

```bash
docker logs <container-name>
```

### Python output buffering issue

By default, Python **buffers stdout** when it detects it's not writing to a real terminal (which is the case inside Docker). This means all `print()` output gets collected in memory and dumped at the end — instead of appearing line by line in real time.

**Fix — add one of these to your Dockerfile:**

```dockerfile
# Option 1: Environment variable (recommended — applies to entire container)
ENV PYTHONUNBUFFERED=1

# Option 2: Pass -u flag to python in CMD
CMD ["python", "-u", "app.py"]
```

| Approach | Scope |
|----------|-------|
| `ENV PYTHONUNBUFFERED=1` | All Python processes in the container |
| `python -u` | Only the specific command |

> **Rule of thumb:** Always add `ENV PYTHONUNBUFFERED=1` to any Python Dockerfile. You'll want real-time logs in production for debugging and observability.

---

## Docker Layers — How They Work

Every instruction in a Dockerfile creates a **layer**. Layers are cached and reused to speed up builds.

```
┌─────────────────────────┐
│ Layer 6: COPY . .       │  ← changes often (your code)
├─────────────────────────┤
│ Layer 5: uv sync        │  ← changes rarely
├─────────────────────────┤
│ Layer 4: COPY pyproject │  ← changes rarely
├─────────────────────────┤
│ Layer 3: pip install uv │  ← never changes
├─────────────────────────┤
│ Layer 2: WORKDIR /app   │  ← never changes
├─────────────────────────┤
│ Layer 1: python:3.12    │  ← never changes
└─────────────────────────┘
```

**Key rules:**
1. **Layers are read-only and shared** — 5 images using the same base share Layer 1 on disk
2. **Cache breaks top-to-bottom** — if Layer 4 changes, Layers 5 and 6 also rebuild
3. **Order matters** — put things that change rarely at the top, things that change often at the bottom

This is why we `COPY pyproject.toml` before `COPY . .` — changing your code only rebuilds the last layer instead of reinstalling all packages.

```bash
# See all layers in an image
docker history book-api
```

---

## Multi-Stage Builds with uv (Production-Ready)

A multi-stage build uses two `FROM` statements. Build in a big image, copy only what you need to a small image.

### Why Multi-Stage?

Think of uv like a delivery truck:
- Stage 1: Truck delivers furniture (uv installs packages)
- Stage 2: Truck leaves, only furniture stays (packages without uv)

### Single-Stage (Current Dockerfile — works but not optimized)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Problem: `uv` stays in the final image (~30MB wasted). You don't need it at runtime.

### Multi-Stage (Optimized)

```dockerfile
# ──────────────────────────────
# Stage 1: Install packages
# ──────────────────────────────
FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# ──────────────────────────────
# Stage 2: Clean final image
# ──────────────────────────────
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=builder /app/.venv /app/.venv
COPY . .
EXPOSE 8000
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000"]
```

```
Stage 1 (builder)                    Stage 2 (final)
┌──────────────────────┐            ┌──────────────────────┐
│  pip, uv             │            │  NO pip, NO uv       │
│  build tools         │            │  NO build tools      │
│  .venv/ (packages) ──┼──── COPY ──►  .venv/ (packages)  │
│                      │            │  your FastAPI code   │
└──────────────────────┘            └──────────────────────┘
     THROWN AWAY                        FINAL IMAGE (smaller)
```

**Key lines explained:**

| Line | Purpose |
|------|---------|
| `FROM ... AS builder` | Name Stage 1 so we can reference it later |
| `FROM python:3.12-slim` | Start fresh Stage 2 (clean slate) |
| `COPY --from=builder /app/.venv /app/.venv` | Grab installed packages from Stage 1 |
| `ENV PATH="/app/.venv/bin:$PATH"` | Let the shell find `fastapi`, `uvicorn` without full path |

### Build and Compare Sizes

```bash
# Build single-stage
docker build -t book-api:single .

# Build multi-stage (save as Dockerfile.multi)
docker build -f Dockerfile.multi -t book-api:multi .

# Compare
docker images book-api
```

---

## Volumes — Persisting Data

Containers are **ephemeral** — when you delete a container, all data inside it is lost.

Volumes store data **outside** the container on your host machine. The data survives even if the container is deleted.

### The Problem

```bash
docker rm my-database    # 💀 all data inside is gone forever
```

### The Solution

```bash
# -v volume-name:/path/inside/container
docker run -d \
  --name my-postgres \
  -v my-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:16
```

```
Your Host Machine          Container
┌──────────────┐          ┌──────────────┐
│              │          │              │
│  my-data/  ◄─────────────► /var/lib/   │
│  (persists)  │          │  postgresql/ │
│              │          │              │
└──────────────┘          └──────────────┘
                          Delete container →
                          data survives on host
```

### Recreate Container, Data Still There

```bash
docker rm my-postgres                                    # container gone
docker run -d --name my-postgres -v my-data:/var/lib/postgresql/data postgres:16  # data still here ✅
```

### Accessing Data Inside a Running Container

```bash
# Open a shell inside the container
docker exec -it my-postgres bash

# Run a specific command inside the container
docker exec -it my-postgres psql -U postgres

# From your host machine via mapped port
psql -h localhost -p 5432 -U postgres
```

| Flag | Meaning |
|------|---------|
| `-i` | Interactive (keep stdin open) |
| `-t` | Allocate a terminal |
| `-it` | Both — gives you a live shell |

### Volume Commands

```bash
docker volume ls                  # List all volumes
docker volume inspect my-data     # See where it's stored on host
docker volume rm my-data          # Delete a volume
docker volume prune               # Remove all unused volumes
```

> **Rule of thumb:** Any container that stores data (databases, file uploads, logs) should use a volume.
