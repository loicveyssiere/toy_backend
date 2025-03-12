# Python Toy Backend

A pedagogic backend to manager books and book loans.

## Install

```bash
# install dependencies
uv sync
```

## Run backend 

```bash
uv run uvicorn src.server:app --port=8000
```

## Run tests
```bash
uv run pytest --log-cli-level=info -s
```