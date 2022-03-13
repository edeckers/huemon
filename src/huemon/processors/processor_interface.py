from typing import Generic, TypeVar

from huemon.utils.errors import HueError
from huemon.utils.monads.either import Either

TA = TypeVar("TA")


class ProcessorInterface(Generic[TA]):  # pylint: disable=too-few-public-methods
    def process(self, value: Either[HueError, TA]):
        raise NotImplementedError("Processor process implementation missing")
