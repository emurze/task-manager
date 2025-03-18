import inspect
from typing import Any, Union, NoReturn, Callable

from seedwork.application.application_module import ApplicationModule
from seedwork.application.commands import Command
from seedwork.application.messages import Message
from seedwork.application.providers import Provider
from seedwork.application.queries import Query


class Application(ApplicationModule):
    def __init__(
        self,
        name: str = "application",
        dependencies: dict | None = None,
    ):
        super().__init__(name)
        self._dependencies = dependencies or {}

    def __setitem__(self, key: str, value: Any) -> None:
        self._dependencies[key] = value

    def __getitem__(self, key: str) -> Any:
        return self._dependencies[key]

    def _get_provider_dependencies(self) -> dict:
        return {
            name: provider()
            for name, provider in self._dependencies.items()
            if isinstance(provider, Provider)
        }

    def _get_dependencies(self) -> dict:
        return self._dependencies | self._get_provider_dependencies()

    async def handle(self, message: Message) -> Union[Any, NoReturn]:
        if isinstance(message, Command):
            return await self.handle_command(message)
        elif isinstance(message, Query):
            return await self.handle_query(message)
        else:
            raise TypeError(
                f"Unsupported message type: {type(message).__name__}"
            )

    async def handle_query(self, query: Query) -> Any | NoReturn:
        for handler in self.iterate_handlers_for(type(query)):
            async with self._dependencies["session_factory"]() as session:
                deps = self._get_dependencies() | {"session": session}
                injected_handler = inject_dependencies(handler, deps)
                return await injected_handler(query)

    async def handle_command(self, command: Command) -> Any | NoReturn:
        for handler in self.iterate_handlers_for(type(command)):
            deps = self._get_dependencies()
            injected_handler = inject_dependencies(handler, deps)
            return await injected_handler(command)


def inject_dependencies(handler: Callable, dependencies: dict) -> Callable:
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)
