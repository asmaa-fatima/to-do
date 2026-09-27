from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.api import tasks
from app.core.config import get_settings
from app.db.session import Base, engine
from app.services.task_service import NotFoundError

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Fine for a starter; move to Alembic migrations before production.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware, allow_origins=settings.cors_origins, allow_methods=["*"], allow_headers=["*"]
)


@app.exception_handler(NotFoundError)
def not_found_handler(_: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.get("/health", tags=["ops"])
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok"}


app.include_router(tasks.router, prefix="/api/v1")
