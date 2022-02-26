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
    Discover.__print_array_as_discovery(filter(
        Discover.__has_state_field(field_name),
        Api.get_sensors()))

  def discover(discovery_type):
    if discovery_type == "batteries":
      Discover.__print_discover_batteries()

    if discovery_type == "lights":
      Discover.__print_discover_lights()
      return

    if discovery_type == "sensors:presence":
      Discover.__print_discover_sensors_type("presence")
      return

    if discovery_type == "sensors:light":
      Discover.__print_discover_sensors_type("lightlevel")
      return

    if discovery_type == "sensors:temperature":
      Discover.__print_discover_sensors_type("temperature")
      return


class Command:
  def __get_light(unique_id):
    return list(filter(
        lambda info: info["uniqueid"] == unique_id,
        Api.get_lights()))[0]

  def __get_sensor(device_id):
    return list(filter(
        lambda info: "uniqueid" in info and info["uniqueid"] == device_id,
        Api.get_sensors()))[0]

  def __print_sensor_battery_level(unique_id):
    device = Command.__get_sensor(unique_id)

    print(float(device["config"]["battery"]))

  def __print_sensor_light_level(unique_id):
    device = Command.__get_sensor(unique_id)

    print(float(device["state"]["lightlevel"]))

  def __print_sensor_presence(unique_id):
    device = Command.__get_sensor(unique_id)

    print(int(device["state"]["presence"]))

  def __print_sensor_reachable(unique_id):
    device = Command.__get_sensor(unique_id)

    print(int(device["config"]["reachable"]))

  def __print_sensor_temperature(unique_id):
    device = Command.__get_sensor(unique_id)

    print(float(device["state"]["temperature"]/100))

  def __print_light_reachable(unique_id):
    light = Command.__get_light(unique_id)

    print(int(light["state"]["reachable"]))

  def __print_light_status(unique_id):
    light = Command.__get_light(unique_id)

    print(int(light["state"]["on"]))

  def __print_light_upgrade_available(unique_id):
    light = Command.__get_light(unique_id)

    print(int(light["swupdate"]["state"] != "noupdates"))

  def __print_light_version(unique_id):
    light = Command.__get_light(unique_id)

    print(light["swversion"])

  def __print_system_upgrade_available():
    config = Api.get_system_config()

    print(int(config["swupdate2"]["state"] != "noupdates"))

  def __print_system_version():
    config = Api.get_system_config()

    print(config["swversion"])

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
