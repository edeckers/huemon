#!/usr/bin/env python3

import json
import sys

from functools import reduce
from urllib.request import urlopen

import config

COMMANDS = ["battery", "discover", "light", "system", "test"]
HUE_HUB_URL = f"http://{config.IP}/api/{config.KEY}"

TYPE_SENSOR_LIGHT = "ZLLLightLevel"
TYPE_SENSOR_PRESENCE = "ZLLPresence"
TYPE_SWITCH = "ZLLSwitch"

def hue_url(relative_url):
  return "/".join([HUE_HUB_URL, relative_url])

def get_system_config():
  with urlopen(hue_url("config")) as response:
     return json.loads(response.read())

def get_all_lights():
  with urlopen(hue_url("lights")) as response:
     return list(json.loads(response.read()).values())

def get_light(unique_id):
  return list(filter( \
      lambda info:info["uniqueid"] == unique_id, \
      get_all_lights()))[0]

def get_battery_devices():
  with urlopen(hue_url("sensors")) as response:
    return filter( \
            lambda s:"config" in s and "battery" in s["config"], \
            list(json.loads(response.read()).values()))

def get_battery_device(device_id):
  return list(filter( \
      lambda info:info["uniqueid"] == device_id, \
      get_battery_devices()))[0]

def print_battery_level(unique_id):
  device = get_battery_device(unique_id)

  print (float(device["config"]["battery"]))

def print_light_status(unique_id):
  light = get_light(unique_id)

  print (int(light["state"]["on"]))

def print_light_upgrade_available(unique_id):
  light = get_light(unique_id)

  print (int(light["swupdate"]["state"] != "noupdates"))

def print_light_version(unique_id):
  light = get_light(unique_id)

  print (light["swversion"])

def print_system_upgrade_available():
  config = get_system_config()

  print (int(config["swupdate2"]["state"] != "noupdates"))

def print_system_version():
  config = get_system_config()

  print (config["swversion"])

def print_discover_batteries():
  with urlopen(hue_url("sensors")) as response:
    batteries = filter(lambda s:"config" in s and "battery" in s["config"], list(json.loads(response.read()).values()))

    print (json.dumps({"data":reduce( \
            lambda p, light:[*p, {
                "{#NAME}": light["name"],
                "{#UNIQUE_ID}": light["uniqueid"],
            }], \
            batteries, \
            [])}))

def print_discover_lights():
    print (json.dumps({"data":reduce( \
            lambda p, light:[*p, {
                "{#NAME}": light["name"],
                "{#UNIQUE_ID}": light["uniqueid"],
            }], \
            get_all_lights(), \
            [])}))

def print_discover2():
  with urlopen(hue_url("sensors")) as response:
      sensors = filter(lambda s:"uniqueid" in s and not "recycle" in s, list(json.loads(response.read()).values()))

      print (sensors)
      print (json.dumps({"data":reduce( \
              lambda p, light:[*p, {
                  "{#NAME}": light["name"],
                  "{#UNIQUE_ID}": light["uniqueid"],
              }], \
              sensors, \
              [])}))

def handle_discover_command(arguments):
  # if (len(arguments) != 1):
  #   print (f"Expected exactly one argument for `discover`, received {len(arguments)}")
  #   exit (1)
  discovery_type = arguments[0]

  if discovery_type == "lights":
    print_discover_lights()
    return

  if discovery_type == "batteries":
    print_discover_batteries()

def handle_battery_command(arguments):
  # if (len(arguments) != 1):
  #   print (f"Expected exactly one argument for `status`, received {len(arguments)}")
  #   exit (1)

  device_id = arguments[0]

  print_battery_level(device_id)

def handle_light_command(arguments):
  # if (len(arguments) != 1):
  #   print (f"Expected exactly one argument for `status`, received {len(arguments)}")
  #   exit (1)

  light_id = arguments[0]
  action = arguments[1]

  if (action == "is_upgrade_available"):
    print_light_upgrade_available(light_id)
    return

  if (action == "status"):
    print_light_status(light_id)
    return

  if (action == "version"):
    print_light_version(light_id)
    return


def handle_system_command(arguments):
  # if (len(arguments) != 1):
  #   print (f"Expected exactly one argument for `status`, received {len(arguments)}")
  #   exit (1)

  action = arguments[0]

  if (action == "is_upgrade_available"):
      print_system_upgrade_available()
      return

  if (action == "version"):
      print_system_version()
      return

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print ("Did not receive enough arguments, expected at least one command argument")
        exit (1)

    command = sys.argv[1]

    is_valid_command = command in COMMANDS
    if not is_valid_command:
        print (f"Unexpected command `{command}`, expected one of {COMMANDS}")
        exit (1)


    arguments = sys.argv[2:]
    if (command == "battery"):
        handle_battery_command(arguments)
        exit (0)

    if (command == "discover"):
        handle_discover_command(arguments)
        exit (0)

    if (command == "light"):
        handle_light_command(arguments)
        exit (0)

    if (command == "system"):
        handle_system_command(arguments)
        exit (0)

    if (command == "test"):
        print_discover2()
        exit (0)

    print ("Something unexpected went wrong")

