from typing import TypeVar

from huemon.processors.processor_interface import ProcessorInterface
from huemon.utils.errors import HueError
from huemon.utils.monads.either import Either

TA = TypeVar("TA")


class StdoutProcessor(ProcessorInterface):  # pylint: disable=too-few-public-methods
    def process(self, value: Either[HueError, TA]):
        print(value)
