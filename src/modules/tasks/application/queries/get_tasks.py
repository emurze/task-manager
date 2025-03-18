from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.tasks.application import tasks_module
from modules.tasks.application.queries.map_task_to_dto import map_task_to_dto
from modules.tasks.infra.repositories import TaskModel
from seedwork.application.queries import Query


@dataclass(frozen=True)
class GetTasksQuery(Query):
    pass


@tasks_module.handler(GetTasksQuery)
async def get_tasks(_: GetTasksQuery, session: AsyncSession) -> list[dict]:
    query = select(TaskModel)
    res = await session.execute(query)
    return [map_task_to_dto(task) for task in res.scalars()]
