#!/usr/bin/env python3

import os
from pathlib import Path
import sys

from functools import reduce
from hue_mon.api.api import Api
from hue_mon.api.cached_api import CachedApi
from hue_mon.api_interface import ApiInterface
from hue_mon.config_factory import create_config

from hue_mon.hue_command_interface import HueCommand
from hue_mon.logger_factory import create_logger
from hue_mon.plugin_loader import load_plugins

COMMAND_PLUGINS_PATH = str(os.path.join(
    Path(__file__).parent.parent.absolute(), "commands_enabled"))
CONFIG = create_config()
HUE_HUB_URL = f"http://{CONFIG['ip']}/api/{CONFIG['key']}"
LOG = create_logger()
MAX_CACHE_AGE_SECONDS = int(CONFIG["cache"]["max_age_seconds"])


def create_command_handlers(config: dict, api: ApiInterface, plugins: dict):
  return reduce(
      lambda p, c: {**p, c.name(): c(config, api)}, plugins, {})


class CommandHandler: # pylint: disable=too-few-public-methods
  def __init__(self, handlers):
    self.handlers = handlers

  def exec(self, command: str, arguments):
    LOG.debug("Running command `%s` (arguments=%s)", command, arguments)
    if not command in self.handlers:
      LOG.error("Received unknown command `%s`", command)
      print(
          f"Unexpected command `{command}`, expected one of {list(self.handlers)}")
      sys.exit(1)

    self.handlers[command].exec(arguments)

    LOG.debug("Finished command `%s` (arguments=%s)", command, arguments)


class Main: # pylint: disable=too-few-public-methods
  @staticmethod
  def main(argv):
    LOG.debug("Running script (parameters=%s)", argv[1:])
    if len(argv) <= 1:
      print("Did not receive enough arguments, expected at least one command argument")
      LOG.error(
          "Did not receive enough arguments (arguments=%s)", argv[1:])
      sys.exit(1)

    command, *arguments = argv[1:]

    LOG.debug("Loading command plugins (path=%s)", COMMAND_PLUGINS_PATH)
    command_handler_plugins =  \
        create_command_handlers(
            CONFIG,
            CachedApi(Api(HUE_HUB_URL), MAX_CACHE_AGE_SECONDS),
            load_plugins("command", COMMAND_PLUGINS_PATH, HueCommand))
    LOG.debug("Finished loading command plugins (path=%s)",
              COMMAND_PLUGINS_PATH)

    CommandHandler(command_handler_plugins).exec(command, arguments)

    LOG.debug("Finished script (parameters=%s)", argv[1:])
    sys.exit(0)


if __name__ == "__main__":
  Main.main(sys.argv)
