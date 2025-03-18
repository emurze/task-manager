import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.dependencies import get_application
from api.tasks.schemas import TaskRead, TaskCreate, TaskUpdate
from modules.tasks.application.commands import (
    CreateTaskCommand,
    DeleteTaskCommand,
    UpdateTaskCommand,
)
from modules.tasks.application.queries import (
    GetTasksQuery,
    GetTaskDetailsQuery,
)
from seedwork.application.application import Application

lg = logging.getLogger(__name__)
router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskRead,
)
async def get_task_details(
    task_id: UUID,
    app: Application = Depends(get_application),
):
    task = await app.handle(GetTaskDetailsQuery(task_id=task_id))

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",  # TODO
        )

    return task


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[TaskRead],
)
async def get_tasks(app: Application = Depends(get_application)):
    return await app.handle(GetTasksQuery())


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UUID,
)
async def create_task(
    dto: TaskCreate,
    app: Application = Depends(get_application),
):
    return await app.handle(CreateTaskCommand(name=dto.name))


@router.put(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_task(
    task_id: UUID,
    dto: TaskUpdate,
    app: Application = Depends(get_application),
) -> None:
    await app.handle(UpdateTaskCommand(task_id=task_id, name=dto.name))


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: UUID,
    app: Application = Depends(get_application),
) -> None:
    await app.handle(DeleteTaskCommand(task_id=task_id))
