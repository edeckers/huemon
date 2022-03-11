# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import sys

from huemon.infrastructure.logger_factory import create_logger
from huemon.utils.const import EXIT_FAIL

LOG = create_logger()


def exit_fail(message, *arguments):
    LOG.error(message, *arguments)
    print(message % tuple(arguments))

    sys.exit(EXIT_FAIL)
