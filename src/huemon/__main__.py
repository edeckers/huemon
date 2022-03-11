# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import sys

from huemon.commands.command_handler import create_default_command_handler
from huemon.infrastructure.bootstrapper import bootstrap
from huemon.infrastructure.config_factory import create_config
from huemon.infrastructure.logger_factory import bootstrap_logger
from huemon.utils.const import EXIT_OK
from huemon.utils.errors import exit_fail
from huemon.utils.plugins import get_command_plugins_path

CONFIG = create_config()
LOG = bootstrap_logger(CONFIG)


class Main:  # pylint: disable=too-few-public-methods
    @staticmethod
    def main(argv):
        LOG.debug("Running script (parameters=%s)", argv[1:])
        bootstrap()

        command_handler = create_default_command_handler(
            CONFIG, get_command_plugins_path(CONFIG)
        )

        if len(argv) <= 1:
            exit_fail(
                "Did not receive enough arguments, expected one of %s (arguments=%s)",
                command_handler.available_commands(),
                argv[1:],
            )

        command, *arguments = argv[1:]

        command_handler.exec(command, arguments)

        LOG.debug("Finished script (parameters=%s)", argv[1:])
        sys.exit(EXIT_OK)


if __name__ == "__main__":
    Main.main(sys.argv)
