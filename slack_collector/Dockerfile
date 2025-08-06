FROM python:3.13.1-slim@sha256:031ebf3cde9f3719d2db385233bcb18df5162038e9cda20e64e08f49f4b47a2f

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates netcat-openbsd && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/0.7.3/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY shared ./shared
COPY slack_collector ./slack_collector

RUN uv sync --package slack-collector --frozen --no-dev

CMD ["uv", "run", "--package", "slack-collector", "python", "-m", "slack_collector.fetch"]