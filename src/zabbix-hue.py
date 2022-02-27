#!/usr/bin/env python3

import sys

from functools import reduce
from api.api import Api
from api.cached_api import CachedApi
from api_interface import ApiInterface
from commands_available.discover_command import DiscoverCommand
from commands_available.light_command import LightCommand
from commands_available.sensor_command import SensorCommand
from commands_available.system_command import SystemCommand
from config_factory import create_config

from hue_command_interface import HueCommand
from logger_factory import create_logger

config = create_config()

LOG = create_logger()

HUE_HUB_URL = f"http://{config['ip']}/api/{config['key']}"

MAX_CACHE_AGE_SECONDS = int(config["cache"]["max_age_seconds"])


class CommandHandler:
  def __init__(self, api: ApiInterface):
    self.api = api

  def discover(self, arguments):
    return DiscoverCommand(self.api, arguments).exec()

  def sensor(self, arguments):
    return SensorCommand(self.api, arguments).exec()

  def light(self, arguments):
    return LightCommand(self.api, arguments).exec()

  def system(self, arguments):
    return SystemCommand(self.api, arguments).exec()

  __COMMAND_HANDLERS = {
      "discover": discover,
      "light": light,
      "sensor": sensor,
      "system": system
  }

  def exec(self, command: str, arguments):
    LOG.debug("Running command `%s` (arguments=%s)", command, arguments)
    is_valid_command = command in CommandHandler.__COMMAND_HANDLERS
    if not is_valid_command:
      LOG.error("Received unknown command `%s`", command)
      print(
          f"Unexpected command `{command}`, expected one of {list(CommandHandler.__COMMAND_HANDLERS.keys())}")
      exit(1)

    CommandHandler.__COMMAND_HANDLERS[command](self, arguments)
    LOG.debug("Finished command `%s` (arguments=%s)", command, arguments)


if __name__ == "__main__":
  LOG.debug("Running script (parameters=%s)", sys.argv[1:])
  if len(sys.argv) <= 1:
    print("Did not receive enough arguments, expected at least one command argument")
    LOG.error(
        "Did not receive enough arguments (arguments=%s)", sys.argv[1:])
    exit(1)

  command, *arguments = sys.argv[1:]

  CommandHandler(CachedApi(Api(HUE_HUB_URL), MAX_CACHE_AGE_SECONDS)).exec(
      command, arguments)
  LOG.debug("Finished script (parameters=%s)", sys.argv[1:])
  exit(0)
