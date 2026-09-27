from app.models.task import Task
from app.repositories.task_repo import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


class NotFoundError(Exception):
    pass


class TaskService:
    """Business rules live here — keeps routes thin and logic testable."""

    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def list(self, done: bool | None, limit: int, offset: int):
        return self.repo.list(done=done, limit=limit, offset=offset)

    def get(self, task_id: int) -> Task:
        task = self.repo.get(task_id)
        if not task:
            raise NotFoundError(f"Task {task_id} not found")
        return task

    def create(self, data: TaskCreate) -> Task:
        return self.repo.add(Task(**data.model_dump()))

    def update(self, task_id: int, data: TaskUpdate) -> Task:
        task = self.get(task_id)
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(task, k, v)
        return self.repo.save(task)

    def delete(self, task_id: int) -> None:
        self.repo.delete(self.get(task_id))
