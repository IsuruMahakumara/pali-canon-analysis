# Sutta Reader

FastAPI app for reading Pali Canon suttas.

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -e ../
uv pip install -e .
```

## Run

```bash
cd sutta-reader
uv run uvicorn main:app --reload
```

The app will be available at http://localhost:8000


```bash
cd svelte-app
npm run dev
```

The app will be available at http://localhost:7000



Clear Porst

```bash
lsof -ti :8000 | xargs kill -9  
lsof -ti :7000 | xargs kill
```

-9 will force kill