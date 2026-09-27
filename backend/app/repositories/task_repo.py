from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.task import Task


class TaskRepository:
    """Only layer that talks to the DB. Swap for another store without touching services."""

    def __init__(self, db: Session):
        self.db = db

    def list(self, *, done: bool | None, limit: int, offset: int) -> tuple[list[Task], int]:
        stmt = select(Task)
        if done is not None:
            stmt = stmt.where(Task.done == done)
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
        rows = self.db.scalars(stmt.order_by(Task.id.desc()).limit(limit).offset(offset)).all()
        return list(rows), total

    def get(self, task_id: int) -> Task | None:
        return self.db.get(Task, task_id)

    def add(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def save(self, task: Task) -> Task:
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()
