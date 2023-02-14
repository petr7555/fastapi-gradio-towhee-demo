# FastAPI, Gradio and Towhee demo

# How to run

## Install dependencies

- `poetry install`

## Run server

### Gradio only

- `poetry run python gradio_only.py`

### FastAPI + Gradio

- `poetry run uvicorn fastapi_gradio:app --reload`

### Towhee only

- `poetry run python towhee_only.py` or
- `poetry run uvicorn towhee_only:app --reload` and send `POST` requests with text body.

### Towhee + Gradio

- `docker compose up -d`
- `poetry run python fill_embeddings.py`
- `poetry run python towhee_gradio.py`
