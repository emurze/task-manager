import uuid
from dataclasses import dataclass, field

from modules.tasks.domain.value_objects import TaskName


@dataclass(kw_only=True)
class Task:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: TaskName
