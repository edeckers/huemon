# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import sys

from huemon.api.api import Api
from huemon.api.cached_api import CachedApi
from huemon.commands.command_handler import CommandHandler, create_command_handlers
from huemon.commands_internal.install_available_command import InstallAvailableCommand
from huemon.config_factory import create_config
from huemon.const import EXIT_OK

from huemon.commands.hue_command_interface import HueCommand
from huemon.logger_factory import bootstrap_logger
from huemon.plugin_loader import load_plugins
from huemon.util import exit_fail, get_commands_path

CONFIG = create_config()
COMMAND_PLUGINS_PATH = get_commands_path(CONFIG, "enabled")
HUE_HUB_URL = f"http://{CONFIG['ip']}/api/{CONFIG['key']}"
LOG = bootstrap_logger(CONFIG)
DEFAULT_MAX_CACHE_AGE_SECONDS = 10


def create_api(config: dict):
  enable_cache = \
      "cache" in config and \
      "enable" in config["cache"] and \
      bool(config["cache"]["enable"])

  is_cache_age_configured = \
      "cache" in config and \
      "max_age_seconds" in config["cache"]

  max_cache_age_seconds = \
      int(config["cache"]["max_age_seconds"]) if \
      is_cache_age_configured else \
      DEFAULT_MAX_CACHE_AGE_SECONDS

  api = Api(HUE_HUB_URL)

  return CachedApi(api, max_cache_age_seconds) if enable_cache else api


class Main:  # pylint: disable=too-few-public-methods
  @staticmethod
  def main(argv):
    LOG.debug("Running script (parameters=%s)", argv[1:])

    LOG.debug("Loading command plugins (path=%s)", COMMAND_PLUGINS_PATH)
    command_handler_plugins =  \
        create_command_handlers(
            CONFIG,
            create_api(CONFIG),
            load_plugins("command", COMMAND_PLUGINS_PATH, HueCommand))
    LOG.debug("Finished loading command plugins (path=%s)",
              COMMAND_PLUGINS_PATH)

    command_handler = CommandHandler({
        **command_handler_plugins,
        InstallAvailableCommand.name(): InstallAvailableCommand(CONFIG)
    })

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
