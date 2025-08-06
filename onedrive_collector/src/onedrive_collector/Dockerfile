FROM python:3.10-slim
WORKDIR /app
RUN pip install uv --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv venv && uv sync
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "worker.py"]
