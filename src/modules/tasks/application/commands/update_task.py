from dataclasses import dataclass
from uuid import UUID

from modules.tasks.application import tasks_module
from modules.tasks.domain.value_objects import TaskName
from seedwork.application.commands import Command


@dataclass(frozen=True)
class UpdateTaskCommand(Command):
    task_id: UUID
    name: str


@tasks_module.handler(UpdateTaskCommand)
async def update_task(command: UpdateTaskCommand, uow) -> None:
    async with uow:
        task = await uow.tasks.get_by_id(command.task_id, for_update=True)
        task.name = TaskName(command.name)
        await uow.commit()
