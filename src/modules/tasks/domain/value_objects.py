from dataclasses import dataclass


@dataclass(frozen=True)
class TaskName:
    value: str

    def as_generic_type(self) -> str:
        return self.value
