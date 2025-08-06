# Knowledge Collector

This repository contains a modular data collection system for multiple platforms (Slack, Discord, OneDrive, etc.), with shared utilities for storage, queueing, and database management.

## 📂 Project Structure

```
knowledgecollector/
│
├─ slack_collector/
│   ├─ src/slack_collector/
│   │   ├─ __init__.py
│   │   └─ fetch.py
│   └─ pyproject.toml
│
├─ shared/
│   ├─ src/shared/
│   │   ├─ config.py
│   │   └─ storage.py
│   └─ pyproject.toml
│
├─ docker-compose.yml
├─ .env
└─ .env.age
```

- **slack_collector** – Collects Slack messages and uploads attachments to MinIO.
- **shared** – Common utilities (MinIO storage, Redis queue, MongoDB helpers).
- **docker-compose.yml** – Spins up Redis, Mongo, MinIO, API, and collectors.

---

## ⚡ Running Locally

To run Slack collector locally:

```bash
uv run --package slack-collector python -m slack_collector.fetch
```

This ensures `shared` is properly resolved and available as a dependency.

---

## 🐳 Docker Setup

### 1. Build the Slack Collector Image

From the project root:

```bash
docker build -t slack-collector:latest -f slack_collector/Dockerfile .
```

---

### 2. Environment Variables

All sensitive settings are stored in `.env`:

```
SLACK_BOT_TOKEN=xoxb-...
SLACK_CHANNEL_ID=C12345678
MINIO_ENDPOINT=minio:9000
MINIO_SECURE=false
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=secret123
```

Load them into containers using:

```yaml
env_file:
  - .env
```

---

### 3. Docker Compose

The collector is now included as a service:

```yaml
slack_collector:
  build:
    context: .
    dockerfile: slack_collector/Dockerfile
  container_name: slack_collector
  env_file:
    - .env
  environment:
    MINIO_ENDPOINT: minio:9000
    MINIO_SECURE: "false"
    REDIS_HOST: redis
    REDIS_PORT: 6379
    MONGO_URI: mongodb://mongo:27017/knowledge_db
  depends_on:
    - redis
    - mongo
    - minio
  command: >
    sh -c "
      echo 'Waiting for MinIO...' &&
      until nc -z minio 9000; do sleep 1; done &&
      uv run --package slack-collector python -m slack_collector.fetch
    "
```

---

## 🔐 Encrypting the `.env` File

We use **Age** to encrypt environment files.

### 1. Get Your Public Key

```powershell
type C:\Users\Luka\.config\age\agekey
```

Copy the line starting with `age1...`.

---

### 2. Encrypt `.env`

```bash
age -r age1yourpublickeyhere -o .env.age .env
```

---

### 3. Decrypt When Needed

```bash
age -d -i C:\Users\Luka\.config\age\agekey .env.age > .env
```

---
