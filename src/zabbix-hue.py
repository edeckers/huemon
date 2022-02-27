#!/usr/bin/env python3

from genericpath import isfile
import importlib
import inspect
from os import listdir
from pathlib import Path, PosixPath
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


def get_plugin(module_name: str, path: str, sub_class):
  spec = importlib.util.spec_from_file_location(module_name, path)
  module = importlib.util.module_from_spec(spec)

  spec.loader.exec_module(module)

  hue_commands = list(filter(
      lambda m: inspect.isclass(m[1]) and issubclass(
          m[1], sub_class) and m[1] is not sub_class,
      inspect.getmembers(module)))

  if (len(hue_commands) == 0):
    return None

  _, hue_command_class = hue_commands[0]

  return hue_command_class


if __name__ == "__main__":
  plugins = list(map(lambda p: get_plugin(
      f"commands.{p.stem}", p.absolute(), HueCommand),
      Path(__file__).parent.glob("commands_enabled/*.py")))

  LOG.debug("Running script (parameters=%s)", sys.argv[1:])
  if len(sys.argv) <= 1:
    print("Did not receive enough arguments, expected at least one command argument")
    LOG.error(
        "Did not receive enough arguments (arguments=%s)", sys.argv[1:])
    exit(1)

  command, *arguments = sys.argv[1:]

  api = CachedApi(Api(HUE_HUB_URL), MAX_CACHE_AGE_SECONDS)
  command_handlers = reduce(
      lambda p, c: {**p, c.name(): c(config, api)}, plugins, {})

  LOG.debug("Running command `%s` (arguments=%s)", command, arguments)
  is_valid_command = command in command_handlers
  if not is_valid_command:
    LOG.error("Received unknown command `%s`", command)
    print(
        f"Unexpected command `{command}`, expected one of {list(command_handlers)}")
    exit(1)

  command_handlers[command].exec(arguments)

  LOG.debug("Finished command `%s` (arguments=%s)", command, arguments)
  LOG.debug("Finished script (parameters=%s)", sys.argv[1:])
  exit(0)
