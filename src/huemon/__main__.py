# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import sys

from huemon.api.api_factory import create_api
from huemon.commands.command_handler import CommandHandler, create_name_to_command_mapping
from huemon.commands_internal.install_available_command import InstallAvailableCommand
from huemon.infrastructure.config_factory import create_config
from huemon.const import EXIT_OK

from huemon.commands.hue_command_interface import HueCommand
from huemon.infrastructure.logger_factory import bootstrap_logger
from huemon.plugin_loader import load_plugins
from huemon.util import exit_fail, get_commands_path

CONFIG = create_config()
COMMAND_PLUGINS_PATH = get_commands_path(CONFIG, "enabled")
LOG = bootstrap_logger(CONFIG)


def load_command_plugins():
  LOG.debug("Loading command plugins (path=%s)", COMMAND_PLUGINS_PATH)
  command_handler_plugins =  \
      create_name_to_command_mapping(
          CONFIG,
          create_api(CONFIG),
          load_plugins("command", COMMAND_PLUGINS_PATH, HueCommand))
  LOG.debug("Finished loading command plugins (path=%s)", COMMAND_PLUGINS_PATH)

  return command_handler_plugins


def load_plugins_and_hardwired_handlers():
  return {
      **load_command_plugins(),
      InstallAvailableCommand.name(): InstallAvailableCommand(CONFIG)
  }


def create_default_command_handler():
  return CommandHandler(load_plugins_and_hardwired_handlers())


class Main:  # pylint: disable=too-few-public-methods
  @staticmethod
  def main(argv):
    LOG.debug("Running script (parameters=%s)", argv[1:])

    command_handler = create_default_command_handler()

    if len(argv) <= 1:
      exit_fail(
          "Did not receive enough arguments, expected one of %s (arguments=%s)",
          command_handler.available_commands(),
          argv[1:])

    command, *arguments = argv[1:]

    command_handler.exec(command, arguments)

    LOG.debug("Finished script (parameters=%s)", argv[1:])
    sys.exit(EXIT_OK)


if __name__ == "__main__":
  Main.main(sys.argv)
