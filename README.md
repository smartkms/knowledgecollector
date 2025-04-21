# uv  minimal example

This is a minimal example of a Python application that exposes an endpoint.

## Local development

1. First, install `uv`: https://github.com/astral-sh/uv?tab=readme-ov-file#installation
2. Then, install the Python dependencies using `uv sync` (if you don't have the right Python version installed, you can install it using `uv python install 3.13`).
3. Then, copy the `.env.example` file to `.env` - in this example repo, `.env.example` holds valid values.
4. Finally, to run the application, run `fastapi dev uv_minimal_example/main.py`.

### Committing

If you want to use this repo as a basis for your own project,
make sure to also run the following command in the new repo after copying this repo:

```bash
pre-commit install
```

## Docker

You can also run the application using Docker:

1. Build the Docker image using `docker build -t uv-minimal-example .`
2. Run the Docker container using `docker run -p 8000:8000 uv-minimal-example`
3. Now you can access the documentation at http://localhost:8000/docs.
