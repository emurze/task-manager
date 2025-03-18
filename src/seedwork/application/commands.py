from dataclasses import dataclass

from seedwork.application.messages import Message


@dataclass(frozen=True, kw_only=True)
class Command(Message):
    pass
