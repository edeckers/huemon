#!/usr/bin/env python3

import json
import sys

from functools import reduce
from api.api import Api
from api.cached_api import CachedApi
from api_interface import ApiInterface
from config_factory import create_config

from hue_command_interface import HueCommand
from logger_factory import create_logger

config = create_config()

LOG = create_logger()

HUE_HUB_URL = f"http://{config['ip']}/api/{config['key']}"

MAX_CACHE_AGE_SECONDS = int(config["cache"]["max_age_seconds"])


class Discover:
  def __init__(self, api: ApiInterface):
    self.api = api

  def __item_to_discovery(item):
    return {
        "{#NAME}": item["name"],
        "{#UNIQUE_ID}": item["uniqueid"],
    }

  def __has_state_field(field: str):
    return lambda item: \
        "state" in item and \
        field in item["state"] and \
        "recycle" not in item

  def __print_array_as_discovery(items):
    print(json.dumps({"data": reduce(
        lambda p, item: [*p, Discover.__item_to_discovery(item)],
        items,
        [])}))

  def __print_discover_sensors_type(api, sensor_type):
    LOG.debug(
        "Running `discover sensor:*` command (sensor_type=%s)", sensor_type)
    if sensor_type not in ["presence", "light", "temperature"]:
      LOG.error(
          "Received unknown sensor type '%s' for `discover sensor:*` command", sensor_type)
      return

    Discover.__print_array_as_discovery(filter(
        Discover.__has_state_field(
            "lightlevel" if sensor_type == "light" else sensor_type),
        api.get_sensors()))
    LOG.debug(
        "Finished `discover sensor:*` command (sensor_type=%s)", sensor_type)

  __DISCOVERY_HANDLERS = {
      "batteries": lambda api, _: Discover.__print_array_as_discovery(api.get_batteries()),
      "lights": lambda api, _: Discover.__print_array_as_discovery(api.get_lights()),
      "sensors": __print_discover_sensors_type
  }

  def discover(self, discovery_type):
    LOG.debug(
        "Running `discover` command (discovery_type=%s)", discovery_type)
    target, maybe_sub_target, *_ = discovery_type.split(":") + [None]

    if target not in Discover.__DISCOVERY_HANDLERS:
      LOG.error(
          "Received unknown target '%s' for `discover` command", target)
      return

    Discover.__DISCOVERY_HANDLERS[target](self.api, maybe_sub_target)
    LOG.debug(
        "Finished `discover` command (discovery_type=%s)", discovery_type)


class DiscoverCommand(HueCommand):
  def __init__(self, api: ApiInterface, arguments):
    self.arguments = arguments
    self.discovery = Discover(api)

  def exec(self):
    LOG.debug("Running `discover` command (arguments=%s)", self.arguments)
    if (len(self.arguments) != 1):
      LOG.error(
          "Expected exactly one arguments for `discover`, received %s", len(self.arguments))
      print(
          f"Expected exactly one argument for `discover`, received {len(self.arguments)}")
      exit(1)
    discovery_type, *_ = self.arguments

    self.discovery.discover(discovery_type)
    LOG.debug("Finished `discover` command (arguments=%s)", self.arguments)


class SensorCommand(HueCommand):
  def __get_sensor(self, device_id):
    return CommandHandler.get_by_unique_id(device_id, self.api.get_sensors())

  def __mapper(path, type):
    return lambda value: type(reduce(lambda p, field: p[field], path.split("."), value))

  def __map_sensor(self, unique_id, mapper):
    return mapper(self.__get_sensor(unique_id))

  def __MAPPER_TEMPERATURE(device): return float(
      device["state"]["temperature"]/100)

  __MAPPER_BATTERY = __mapper("config.battery", float)
  __MAPPER_LIGHT_LEVEL = __mapper("state.lightlevel", float)
  __MAPPER_PRESENCE = __mapper("state.presence", int)
  __MAPPER_SENSOR_REACHABLE = __mapper("config.reachable", int)

  __SENSOR_ACTION_MAP = {
      "battery:level": __MAPPER_BATTERY,
      "presence": __MAPPER_PRESENCE,
      "reachable": __MAPPER_SENSOR_REACHABLE,
      "temperature": __MAPPER_TEMPERATURE,
      "light:level": __MAPPER_LIGHT_LEVEL
  }

  def __init__(self, api: ApiInterface, arguments):
    self.api = api
    self.arguments = arguments

  def name():
    return "sensor"

  def exec(self):
    LOG.debug("Running `sensor` command (arguments=%s)", self.arguments)
    if (len(self.arguments) != 2):
      LOG.error(
          "Expected exactly two arguments for `sensor`, received %s", len(self.arguments))
      print(
          f"Expected exactly two arguments for `sensor`, received {len(self.arguments)}")
      exit(1)

    device_id, action = self.arguments

    if action not in SensorCommand.__SENSOR_ACTION_MAP:
      LOG.error("Received unknown action '%s' for `sensor` command", action)
      return

    HueCommand._process(self.__map_sensor(
        device_id, SensorCommand.__SENSOR_ACTION_MAP[action]))
    LOG.debug("Finished `sensor` command (arguments=%s)", arguments)


class LightCommand(HueCommand):
  def __MAPPER_UPDATES_AVAILABLE(light): return int(
      light["swupdate"]["state"] != "noupdates")

  __MAPPER_LIGHT_REACHABLE = HueCommand._mapper("state.reachable", int)
  __MAPPER_STATE_ON = HueCommand._mapper("state.on", int)
  __MAPPER_VERSION = HueCommand._mapper("swversion", str)

  __LIGHT_ACTION_MAP = {
      "is_upgrade_available": __MAPPER_UPDATES_AVAILABLE,
      "reachable": __MAPPER_LIGHT_REACHABLE,
      "status": __MAPPER_STATE_ON,
      "version": __MAPPER_VERSION,
  }

  def __get_light(self, unique_id):
    return CommandHandler.get_by_unique_id(unique_id, self.api.get_lights())

  def __map_light(self, unique_id, mapper):
    return mapper(self.__get_light(unique_id))

  def __init__(self, api: ApiInterface, arguments):
    self.api = api
    self.arguments = arguments

  def name(self):
    return "light"

  def exec(self):
    LOG.debug("Running `light` command (arguments=%s)", self.arguments)
    if (len(self.arguments) != 2):
      LOG.error(
          "Expected exactly two arguments for `light`, received %s", len(self.arguments))
      print(
          f"Expected exactly two arguments for `light`, received {len(self.arguments)}")
      exit(1)

    light_id, action = self.arguments

    if action not in self.__LIGHT_ACTION_MAP:
      LOG.error("Received unknown action '%s' for `light` command", action)
      return

    HueCommand._process(self.__map_light(
        light_id, self.__LIGHT_ACTION_MAP[action]))
    LOG.debug("Finished `light` command (arguments=%s)", arguments)


class SystemCommand(HueCommand):
  def __map_config(self, mapper):
    return mapper(self.api.get_system_config())

  def __MAPPER_SYSTEM_UPGRADE_AVAILABLE(config): return int(
      config["swupdate2"]["state"] != "noupdates")
  __MAPPER_VERSION = HueCommand._mapper("swversion", str)

  __SYSTEM_ACTION_MAP = {
      "is_upgrade_available": __MAPPER_SYSTEM_UPGRADE_AVAILABLE,
      "version": __MAPPER_VERSION,
  }

  def __init__(self, api: ApiInterface, arguments):
    self.arguments = arguments
    self.api = api

  def name(self):
    return "system"

  def exec(self):
    LOG.debug("Running `system` command (arguments=%s)", self.arguments)
    if (len(self.arguments) != 1):
      LOG.error(
          "Expected exactly one argument for `system`, received %s", len(self.arguments))
      print(
          f"Expected exactly one argument for `system`, received {len(self.arguments)}")
      exit(1)

    action, *_ = arguments

    if action not in self.__SYSTEM_ACTION_MAP:
      LOG.error("Received unknown action '%s' for `system` command", action)
      return

    HueCommand._process(self.__map_config(self.__SYSTEM_ACTION_MAP[action]))
    LOG.debug("Finished `system` command (arguments=%s)", arguments)


class CommandHandler:
  def __init__(self, api: ApiInterface):
    self.api = api

  def get_by_unique_id(unique_id: str, items: list) -> list:
    return list(filter(
        lambda info: "uniqueid" in info and info["uniqueid"] == unique_id,
        items))[0]

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
