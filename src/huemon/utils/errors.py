# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import sys
from typing import NamedTuple

from huemon.infrastructure.logger_factory import create_logger
from huemon.utils.const import EXIT_FAIL

LOG = create_logger()

E_CODE_PLUGIN_LOADER = -2


class HueError(NamedTuple):
    code: int
    message: str = ""
    context: dict = {}


def exit_fail(message, *arguments):
    LOG.error(message, *arguments)
    print(message % tuple(arguments))

    sys.exit(EXIT_FAIL)
