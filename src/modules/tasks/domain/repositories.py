import uuid
from typing import Protocol

from modules.tasks.domain.entities import Task


class ITaskRepository(Protocol):
    def add(self, task: Task) -> None:
        """Adds a new task to the repository."""

    async def get_by_id(
        self,
        task_id: uuid.UUID,
        for_update: bool = False,
    ) -> Task | None:
        """Fetches a task by ID, returns None if not found."""

    async def delete_by_id(self, task_id: uuid.UUID) -> None:
        """Deletes a task by ID if it exists."""
