#!/usr/bin/env python3

import json
import sys

from functools import reduce
from urllib.request import urlopen

import config


class Api:
  __HUE_HUB_URL = f"http://{config.IP}/api/{config.KEY}"

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

  def __print_discover_batteries():
    Discover.__print_array_as_discovery(Api.get_batteries())

  def __print_discover_lights():
    Discover.__print_array_as_discovery(Api.get_lights())

  def __print_discover_sensors_type(field_name):
    if field_name not in ["presence", "light", "temperature"]:
      return

    Discover.__print_array_as_discovery(filter(
        Discover.__has_state_field(
            "lightlevel" if field_name == "light" else field_name),
        Api.get_sensors()))

  __DISCOVERY_HANDLERS = {
      "batteries": lambda _: Discover.__print_discover_batteries(),
      "lights": lambda _: Discover.__print_discover_lights(),
      "sensors": __print_discover_sensors_type
  }

  def discover(discovery_type):
    target, maybe_sub_target, *_ = discovery_type.split(":") + [None]

    if target not in Discover.__DISCOVERY_HANDLERS:
      return

    Discover.__DISCOVERY_HANDLERS[target](maybe_sub_target)


class Command:
  def __get_light(unique_id):
    return list(filter(
        lambda info: info["uniqueid"] == unique_id,
        Api.get_lights()))[0]

  def __get_sensor(device_id):
    return list(filter(
        lambda info: "uniqueid" in info and info["uniqueid"] == device_id,
        Api.get_sensors()))[0]

  def __map_value(value, path, type):
    return type(reduce(lambda p, field: p[field], path.split("."), value))

  def __mapper(path, type):
    return lambda v: Command.__map_value(v, path, type)

  def __map_config(mapper):
    return mapper(Api.get_system_config())

  def __map_light(unique_id, mapper):
    return mapper(Command.__get_light(unique_id))

  def __map_sensor(unique_id, mapper):
    return mapper(Command.__get_sensor(unique_id))

  __MAPPER_BATTERY = __mapper("config.battery", float)
  __MAPPER_LIGHT_LEVEL = __mapper("state.lightlevel", float)
  __MAPPER_PRESENCE = __mapper("state.presence", int)
  __MAPPER_SENSOR_REACHABLE = __mapper("config.reachable", int)
  __MAPPER_LIGHT_REACHABLE = __mapper("state.reachable", int)
  __MAPPER_STATE_ON = __mapper("state.on", int)
  __MAPPER_VERSION = __mapper("swversion", str)

  def __MAPPER_TEMPERATURE_REACHABLE(device): return float(
      device["state"]["temperature"]/100)

  def __MAPPER_UPDATES_AVAILABLE(light): return int(
      light["swupdate"]["state"] != "noupdates")

  def __MAPPER_SYSTEM_UPGRADE_AVAILABLE(config): return int(
      config["swupdate2"]["state"] != "noupdates")

  def __process(value):
    print(value)

  def __process_light(unique_id: str, mapper):
    Command.__process(Command.__map_light(unique_id, mapper))

  def __process_sensor(unique_id: str, mapper):
    Command.__process(Command.__map_sensor(unique_id, mapper))

  def __process_system(mapper):
    Command.__process(Command.__map_config(mapper))

  def __print_sensor_battery_level(unique_id):
    Command.__process_sensor(unique_id, Command.__MAPPER_BATTERY)

  def __print_sensor_light_level(unique_id):
    Command.__process_sensor(unique_id, Command.__MAPPER_LIGHT_LEVEL)

  def __print_sensor_presence(unique_id):
    Command.__process_sensor(unique_id, Command.__MAPPER_PRESENCE)

  def __print_sensor_reachable(unique_id):
    Command.__process_sensor(unique_id, Command.__MAPPER_SENSOR_REACHABLE)

  def __print_sensor_temperature(unique_id):
    Command.__process_sensor(unique_id, Command.__MAPPER_TEMPERATURE_REACHABLE)

  def __print_light_reachable(unique_id):
    Command.__process_light(unique_id, Command.__MAPPER_LIGHT_REACHABLE)

  def __print_light_status(unique_id):
    Command.__process_light(unique_id, Command.__MAPPER_STATE_ON)

  def __print_light_upgrade_available(unique_id):
    Command.__process_light(unique_id, Command.__MAPPER_UPDATES_AVAILABLE)

  def __print_light_version(unique_id):
    Command.__process_light(unique_id, Command.__MAPPER_VERSION)

  def __print_system_upgrade_available():
    Command.__process_system(Command.__MAPPER_SYSTEM_UPGRADE_AVAILABLE)

  def __print_system_version():
    Command.__process_system(Command.__MAPPER_VERSION)

  def discover(arguments):
    # if (len(arguments) != 1):
    #   print (f"Expected exactly one argument for `discover`, received {len(arguments)}")
    #   exit (1)
    discovery_type = arguments[0]

    Discover.discover(discovery_type)

  def sensor(arguments):
    # if (len(arguments) != 1):
    #   print (f"Expected exactly one argument for `status`, received {len(arguments)}")
    #   exit (1)

    device_id = arguments[0]
    action = arguments[1]

    if (action == "battery:level"):
      Command.__print_sensor_battery_level(device_id)
      return

    if (action == "presence"):
      Command.__print_sensor_presence(device_id)
      return

    if (action == "reachable"):
      Command.__print_sensor_reachable(device_id)
      return

    if (action == "temperature"):
      Command.__print_sensor_temperature(device_id)
      return

    if (action == "light:level"):
      Command.__print_sensor_light_level(device_id)
      return

  def exec(command: str, arguments):
    COMMAND_HANDLERS = {
        "discover": Command.discover,
        "light": Command.light,
        "sensor": Command.sensor,
        "system": Command.system
    }

    is_valid_command = command in COMMAND_HANDLERS
    if not is_valid_command:
      print(
          f"Unexpected command `{command}`, expected one of {list(COMMAND_HANDLERS.keys())}")
      exit(1)

    COMMAND_HANDLERS[command](arguments)

  def light(arguments):
    # if (len(arguments) != 1):
    #   print (f"Expected exactly one argument for `status`, received {len(arguments)}")
    #   exit (1)

    light_id = arguments[0]
    action = arguments[1]

    if (action == "is_upgrade_available"):
      Command.__print_light_upgrade_available(light_id)
      return

    if (action == "reachable"):
      Command.__print_light_reachable(light_id)
      return

    if (action == "status"):
      Command.__print_light_status(light_id)
      return

    if (action == "version"):
      Command.__print_light_version(light_id)
      return

  def system(arguments):
    # if (len(arguments) != 1):
    #   print (f"Expected exactly one argument for `status`, received {len(arguments)}")
    #   exit (1)

    action = arguments[0]

    if (action == "is_upgrade_available"):
      Command.__print_system_upgrade_available()
      return

    if (action == "version"):
      Command.__print_system_version()
      return


if __name__ == "__main__":
  if len(sys.argv) <= 1:
    print("Did not receive enough arguments, expected at least one command argument")
    exit(1)

  command = sys.argv[1]

  arguments = sys.argv[2:]

  Command.exec(command, arguments)
  exit(0)
