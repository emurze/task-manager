import uuid

from sqlalchemy.orm import Mapped

from modules.tasks.domain.entities import Task
from modules.tasks.domain.value_objects import TaskName
from seedwork.infra.db import Base
from seedwork.infra.repositories import SqlAlchemyGenericRepository


class TaskModel(Base):
    id: Mapped[uuid.UUID]
    name: Mapped[str]

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.name}>"


class TaskDataMapper:
    model_class = TaskModel
    entity_class = Task

    def entity_to_model(self, entity: Task) -> TaskModel:
        return self.model_class(
            id=entity.id,
            name=entity.name.as_generic_type(),
        )

    def model_to_entity(self, model: TaskModel) -> Task:
        return self.entity_class(
            id=model.id,
            name=TaskName(model.name),
        )


class TaskSQLAlchemyRepository(SqlAlchemyGenericRepository):
    mapper_class = TaskDataMapper
    model_class = TaskModel
