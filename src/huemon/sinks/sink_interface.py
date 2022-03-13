# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from typing import Generic, TypeVar

from huemon.utils.errors import HueError
from huemon.utils.monads.either import Either

TA = TypeVar("TA")


class SinkInterface(Generic[TA]):  # pylint: disable=too-few-public-methods
    def process(self, value: Either[HueError, TA]):
        raise NotImplementedError("Processor process implementation missing")
