from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_task_service
from app.schemas.task import Page, TaskCreate, TaskOut, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=Page)
def list_tasks(
    done: bool | None = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    svc: TaskService = Depends(get_task_service),
):
    items, total = svc.list(done, limit, offset)
    return Page(items=[TaskOut.model_validate(t) for t in items], total=total, limit=limit, offset=offset)


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, svc: TaskService = Depends(get_task_service)):
    return svc.create(data)


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, svc: TaskService = Depends(get_task_service)):
    return svc.get(task_id)


@router.patch("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, data: TaskUpdate, svc: TaskService = Depends(get_task_service)):
    return svc.update(task_id, data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, svc: TaskService = Depends(get_task_service)):
    svc.delete(task_id)
