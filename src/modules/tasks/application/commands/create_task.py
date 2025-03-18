from dataclasses import dataclass
from uuid import UUID

from modules.tasks.application import tasks_module
from modules.tasks.domain.entities import Task
from modules.tasks.domain.value_objects import TaskName
from seedwork.application.commands import Command


@dataclass(frozen=True)
class CreateTaskCommand(Command):
    name: str


@tasks_module.handler(CreateTaskCommand)
async def create_task(command: CreateTaskCommand, uow) -> UUID:
    async with uow:
        task = Task(name=TaskName(command.name))
        uow.tasks.add(task)
        await uow.commit()
        return task.id
