from uuid import UUID

from api.schemas import Schema


class TaskRead(Schema):
    id: UUID
    name: str


class TaskCreate(Schema):
    name: str


class TaskUpdate(Schema):
    name: str
