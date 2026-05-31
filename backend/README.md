# Kuta WasteSense API

FastAPI backend for the React/Vite dashboard.

## Local Development

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8000
```

Run the commands above from the project root. This avoids conflict with the legacy Streamlit `app.py` file.

API docs:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```
