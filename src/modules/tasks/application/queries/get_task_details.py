import uuid
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from modules.tasks.application import tasks_module
from modules.tasks.application.queries.map_task_to_dto import map_task_to_dto
from modules.tasks.infra.repositories import TaskModel
from seedwork.application.queries import Query


@dataclass(frozen=True)
class GetTaskDetailsQuery(Query):
    task_id: uuid.UUID


@tasks_module.handler(GetTaskDetailsQuery)
async def get_task_details(
    query: GetTaskDetailsQuery,
    session: AsyncSession,
) -> dict | None:
    task: TaskModel | None = await session.get(TaskModel, query.task_id)

    if not task:
        return None

    return map_task_to_dto(task)


# TODO: Try replication and materialized views (NO-SQL) FOR PERFORMANCE
