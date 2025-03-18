from collections.abc import Callable
from typing import Any


class Provider:
    def __init__(self, _callable: Callable, *args, **kw) -> None:
        self._callable = _callable
        self.args = args
        self.kw = kw

    def __call__(self) -> Any:
        return self._callable(*self.args, **self.kw)
