# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import json
import sys
from typing import TypeVar

from huemon.sinks.sink_interface import SinkInterface
from huemon.utils.errors import HueError
from huemon.utils.monads.either import Either

TA = TypeVar("TA")


class StdoutSink(SinkInterface):  # pylint: disable=too-few-public-methods
    def process(self, value: Either[HueError, TA]):
        print(value.either(lambda error: error.message, json.dumps))

        if value.is_left():
            sys.exit(2)
