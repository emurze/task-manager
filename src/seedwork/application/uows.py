from collections.abc import Callable
from typing import Self, Protocol


class IBaseUnitOfWork(Protocol):
    async def __aenter__(self) -> Self: ...

    async def __aexit__(self, *args): ...

    async def commit(self): ...

    async def rollback(self): ...


class SqlAlchemyUnitOfWork:
    def __init__(
        self,
        session_factory: Callable,
        repositories: dict[str, type],
    ) -> None:
        self.session_factory = session_factory
        self.repositories = repositories

    async def __aenter__(self) -> Self:
        self.session = self.session_factory()
        for field_name, repository in self.repositories.items():
            setattr(self, field_name, repository(self.session))
        return self

    async def __aexit__(self, *args) -> None:
        await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
