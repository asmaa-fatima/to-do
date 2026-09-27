import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient  # noqa: E402
from app.main import app  # noqa: E402
from app.db.session import Base, engine  # noqa: E402


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_crud_flow():
    with TestClient(app) as c:
        r = c.post("/api/v1/tasks", json={"title": "Write tests"})
        assert r.status_code == 201
        tid = r.json()["id"]

        assert c.get("/api/v1/tasks").json()["total"] == 1
        assert c.patch(f"/api/v1/tasks/{tid}", json={"done": True}).json()["done"] is True
        assert c.get("/api/v1/tasks?done=false").json()["total"] == 0
        assert c.delete(f"/api/v1/tasks/{tid}").status_code == 204
        assert c.get(f"/api/v1/tasks/{tid}").status_code == 404


def test_validation():
    with TestClient(app) as c:
        assert c.post("/api/v1/tasks", json={"title": ""}).status_code == 422


def test_health():
    with TestClient(app) as c:
        assert c.get("/health").json() == {"status": "ok"}
