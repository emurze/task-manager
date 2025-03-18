from dataclasses import dataclass
from uuid import UUID

from modules.tasks.application import tasks_module
from seedwork.application.commands import Command


@dataclass(frozen=True)
class DeleteTaskCommand(Command):
    task_id: UUID


@tasks_module.handler(DeleteTaskCommand)
async def delete_task(command: DeleteTaskCommand, uow) -> None:
    async with uow:
        await uow.tasks.remove_by_id(command.task_id)
        await uow.commit()
