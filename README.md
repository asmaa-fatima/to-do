# Tasks — full-stack starter

React (Vite + TS) → FastAPI → PostgreSQL (SQLite for local dev).

## Run everything (Docker)
```bash
docker compose up --build
```
- App: http://localhost:8080
- API docs (Swagger): http://localhost:8000/docs

## Run locally without Docker
```bash
# backend (uses SQLite by default)
cd backend
python -m venv .venv && .venv\Scripts\activate      # Windows  (source .venv/bin/activate on mac/linux)
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
pytest -q

# frontend (new terminal)
cd frontend
npm install
npm run dev        # http://localhost:5173, proxies /api -> :8000
```

## Architecture
```
frontend/src
  api/client.ts       HTTP layer (one place for base URL + error handling)
  useTasks.ts         state + data fetching hook
  components/         dumb UI components
backend/app
  api/                routes (thin) + dependency wiring
  services/           business logic
  repositories/       DB access only
  models/ schemas/    SQLAlchemy tables / Pydantic contracts
  core/config.py      env-driven settings (12-factor)
```

Request flow: `Route → Service → Repository → DB`. Each layer is swappable and testable in isolation.

## Why it scales
- **Stateless API** — run N replicas behind a load balancer; state lives in Postgres.
- **Config via env** — same image for dev/staging/prod.
- **Versioned API** (`/api/v1`) + pagination + filtering built in.
- **Layered backend** — new features = new model/schema/repo/service/router, no touching existing code.
- **Health check** at `/health` for orchestrators (k8s, ECS).

## Next steps for production
1. Alembic migrations (replace `create_all` in `main.py`).
2. Auth (JWT/OAuth) as a FastAPI dependency.
3. Redis cache / background worker (Celery/RQ) when needed.
4. CI: lint + tests + image build; structured logging + metrics.
