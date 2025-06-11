FROM python:3.13.1-slim@sha256:031ebf3cde9f3719d2db385233bcb18df5162038e9cda20e64e08f49f4b47a2f

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application configuration.
COPY .python-version /app/.python-version
COPY ./pyproject.toml /app/pyproject.toml
COPY ./uv.lock /app/uv.lock

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# Copy the application into the container.
COPY . /app

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
