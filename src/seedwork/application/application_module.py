import logging
from collections import defaultdict
from collections.abc import Callable

from seedwork.application.messages import Message
from seedwork.utils.functional import string_to_kwarg_name

log = logging.getLogger(__name__)


class ApplicationModule:
    def __init__(self, name: str):
        self.name: str = name
        self._handlers: defaultdict[type[Message] | str, set[Callable]] = (
            defaultdict(set)
        )
        self._submodules: set[ApplicationModule] = set()

    @property
    def identifier(self):
        return string_to_kwarg_name(self.name)

    def include_submodule(self, a_module: "ApplicationModule"):
        assert isinstance(
            a_module, ApplicationModule
        ), f"Can only include {ApplicationModule} instances, got {a_module}"
        self._submodules.add(a_module)

    def handler(self, alias: type[Message] | str) -> Callable:
        if isinstance(alias, type):
            is_message_type = issubclass(alias, Message)
        else:
            is_message_type = False

        if callable(alias) and not is_message_type:
            # decorator was called without any argument
            func = alias
            alias = func.__name__
            assert len(self._handlers[alias]) == 0
            self._handlers[alias].add(func)
            return func

        # decorator was called with argument
        # @my_module.handle("my_function")
        # @my_module.handle(MyCommand)
        def decorator(_func):
            """
            Decorator for registering tasks by name
            """
            self._handlers[alias].add(_func)
            return _func

        return decorator

    def iterate_handlers_for(self, alias: type[Message] | str):
        if alias in self._handlers:
            for handler in self._handlers[alias]:
                yield handler
        for submodule in self._submodules:
            try:
                yield from submodule.iterate_handlers_for(alias)
            except KeyError:
                pass

    def get_handlers_for(self, alias: type[Message] | str):
        return list(self.iterate_handlers_for(alias))

    def __repr__(self):
        return f"<{self.name} {object.__repr__(self)}>"
