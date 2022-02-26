#!/usr/bin/env python3

import json
import logging
import logging.config
import sys
import yaml

from functools import reduce
from pathlib import Path
from urllib.request import urlopen

with open("/".join([str(Path(__file__).parent), "config.yml"]), "r") as f:
  config = yaml.safe_load(f.read())
  logging.config.dictConfig(config)


logger = logging.getLogger("hue")


class Api:
  __HUE_HUB_URL = f"http://{config['ip']}/api/{config['key']}"

  def __hue_url(relative_url):
    return "/".join([Api.__HUE_HUB_URL, relative_url])

  def get_system_config():
    with urlopen(Api.__hue_url("config")) as response:
      return json.loads(response.read())

  def get_lights():
    with urlopen(Api.__hue_url("lights")) as response:
      return list(json.loads(response.read()).values())

  def get_sensors():
    with urlopen(Api.__hue_url("sensors")) as response:
      return list(json.loads(response.read()).values())

  def get_batteries():
    return list(filter(lambda s: "config" in s and "battery" in s["config"], list(
        Api.get_sensors())))


class Discover:
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

  def __print_discover_sensors_type(sensor_type):
    logger.debug(
        "Running `discover sensor:*` command (sensor_type=%s)", sensor_type)
    if sensor_type not in ["presence", "light", "temperature"]:
      logger.error(
          "Received unknown sensor type '%s' for `discover sensor:*` command", sensor_type)
      return

    Discover.__print_array_as_discovery(filter(
        Discover.__has_state_field(
            "lightlevel" if sensor_type == "light" else sensor_type),
        Api.get_sensors()))
    logger.debug(
        "Finished `discover sensor:*` command (sensor_type=%s)", sensor_type)

  __DISCOVERY_HANDLERS = {
      "batteries": lambda _: Discover.__print_array_as_discovery(Api.get_batteries()),
      "lights": lambda _: Discover.__print_array_as_discovery(Api.get_lights()),
      "sensors": __print_discover_sensors_type
  }

  def discover(discovery_type):
    logger.debug(
        "Running `discover` command (discovery_type=%s)", discovery_type)
    target, maybe_sub_target, *_ = discovery_type.split(":") + [None]

    if target not in Discover.__DISCOVERY_HANDLERS:
      logger.error(
          "Received unknown target '%s' for `discover` command", target)
      return

    Discover.__DISCOVERY_HANDLERS[target](maybe_sub_target)
    logger.debug(
        "Finished `discover` command (discovery_type=%s)", discovery_type)


class Command:
  def __get_by_unique_id(unique_id: str, items: list) -> list:
    return list(filter(
        lambda info: "uniqueid" in info and info["uniqueid"] == unique_id,
        items))[0]

  def __get_light(unique_id):
    return Command.__get_by_unique_id(unique_id, Api.get_lights())

  def __get_sensor(device_id):
    return Command.__get_by_unique_id(device_id, Api.get_sensors())

  def __mapper(path, type):
    return lambda value: type(reduce(lambda p, field: p[field], path.split("."), value))

  def __map_config(mapper):
    return mapper(Api.get_system_config())

  def __map_light(unique_id, mapper):
    return mapper(Command.__get_light(unique_id))

  def __map_sensor(unique_id, mapper):
    return mapper(Command.__get_sensor(unique_id))

  def __MAPPER_TEMPERATURE(device): return float(
      device["state"]["temperature"]/100)

  def __MAPPER_UPDATES_AVAILABLE(light): return int(
      light["swupdate"]["state"] != "noupdates")

  def __MAPPER_SYSTEM_UPGRADE_AVAILABLE(config): return int(
      config["swupdate2"]["state"] != "noupdates")

  __MAPPER_BATTERY = __mapper("config.battery", float)
  __MAPPER_LIGHT_LEVEL = __mapper("state.lightlevel", float)
  __MAPPER_PRESENCE = __mapper("state.presence", int)
  __MAPPER_SENSOR_REACHABLE = __mapper("config.reachable", int)
  __MAPPER_LIGHT_REACHABLE = __mapper("state.reachable", int)
  __MAPPER_STATE_ON = __mapper("state.on", int)
  __MAPPER_VERSION = __mapper("swversion", str)

  __LIGHT_ACTION_MAP = {
      "is_upgrade_available": __MAPPER_UPDATES_AVAILABLE,
      "reachable": __MAPPER_LIGHT_REACHABLE,
      "status": __MAPPER_STATE_ON,
      "version": __MAPPER_VERSION,
  }
  __SENSOR_ACTION_MAP = {
      "battery:level": __MAPPER_BATTERY,
      "presence": __MAPPER_PRESENCE,
      "reachable": __MAPPER_SENSOR_REACHABLE,
      "temperature": __MAPPER_TEMPERATURE,
      "light:level": __MAPPER_LIGHT_LEVEL
  }
  __SYSTEM_ACTION_MAP = {
      "is_upgrade_available": __MAPPER_SYSTEM_UPGRADE_AVAILABLE,
      "version": __MAPPER_VERSION,
  }

  def __process(value):
    print(value)

  def discover(arguments):
    logger.debug("Running `discover` command (arguments=%s)", arguments)
    if (len(arguments) != 1):
      logger.error(
          "Expected exactly one arguments for `discover`, received %s", len(arguments))
      print(
          f"Expected exactly one argument for `discover`, received {len(arguments)}")
      exit(1)
    discovery_type, *_ = arguments

    Discover.discover(discovery_type)
    logger.debug("Finished `discover` command (arguments=%s)", arguments)

  def sensor(arguments):
    logger.debug("Running `sensor` command (arguments=%s)", arguments)
    if (len(arguments) != 2):
      logger.error(
          "Expected exactly two arguments for `sensor`, received %s", len(arguments))
      print(
          f"Expected exactly two arguments for `sensor`, received {len(arguments)}")
      exit(1)

    device_id, action = arguments

    if action not in Command.__SENSOR_ACTION_MAP:
      logger.error("Received unknown action '%s' for `sensor` command", action)
      return

    Command.__process(Command.__map_sensor(
        device_id, Command.__SENSOR_ACTION_MAP[action](device_id)))
    logger.debug("Finished `sensor` command (arguments=%s)", arguments)

  def light(arguments):
    logger.debug("Running `light` command (arguments=%s)", arguments)
    if (len(arguments) != 2):
      logger.error(
          "Expected exactly two arguments for `light`, received %s", len(arguments))
      print(
          f"Expected exactly two arguments for `light`, received {len(arguments)}")
      exit(1)

    light_id, action = arguments

    if action not in Command.__LIGHT_ACTION_MAP:
      logger.error("Received unknown action '%s' for `light` command", action)
      return

    Command.__process(Command.__map_light(
        light_id, Command.__LIGHT_ACTION_MAP[action]))
    logger.debug("Finished `light` command (arguments=%s)", arguments)

  def system(arguments):
    logger.debug("Running `system` command (arguments=%s)", arguments)
    if (len(arguments) != 1):
      logger.error(
          "Expected exactly one argument for `system`, received %s", len(arguments))
      print(
          f"Expected exactly one argument for `system`, received {len(arguments)}")
      exit(1)

    action, *_ = arguments

    if action not in Command.__SYSTEM_ACTION_MAP:
      logger.error("Received unknown action '%s' for `system` command", action)
      return

    Command.__process(Command.__map_config(
        Command.__SYSTEM_ACTION_MAP[action]))
    logger.debug("Finished `system` command (arguments=%s)", arguments)

  __COMMAND_HANDLERS = {
      "discover": discover,
      "light": light,
      "sensor": sensor,
      "system": system
  }

  def exec(command: str, arguments):
    logger.debug("Running command `%s` (arguments=%s)", command, arguments)
    is_valid_command = command in Command.__COMMAND_HANDLERS
    if not is_valid_command:
      logger.error("Received unknown command `%s`", command)
      print(
          f"Unexpected command `{command}`, expected one of {list(Command.__COMMAND_HANDLERS.keys())}")
      exit(1)

    Command.__COMMAND_HANDLERS[command](arguments)
    logger.debug("Finished command `%s` (arguments=%s)", command, arguments)


if __name__ == "__main__":
  logger.debug("Running script (parameters=%s)", sys.argv[1:])
  if len(sys.argv) <= 1:
    print("Did not receive enough arguments, expected at least one command argument")
    logger.error(
        "Did not receive enough arguments (arguments=%s)", sys.argv[1:])
    exit(1)

  command, *arguments = sys.argv[1:]

  Command.exec(command, arguments)
  logger.debug("Finished script (parameters=%s)", sys.argv[1:])
  exit(0)
