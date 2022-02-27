#!/usr/bin/env python3

from fcntl import LOCK_EX, LOCK_NB, flock
import json
import logging
import logging.config
import os
import sys
from tempfile import mkstemp
import tempfile
import time
import yaml

from functools import reduce
from os.path import exists
from pathlib import Path
from urllib.request import urlopen

with open("/".join([str(Path(__file__).parent), "config.yml"]), "r") as f:
  config = yaml.safe_load(f.read())
  logging.config.dictConfig(config)


LOG = logging.getLogger("hue")

HUE_HUB_URL = f"http://{config['ip']}/api/{config['key']}"

MAX_CACHE_AGE_SECONDS = int(config["cache"]["max_age_seconds"])


class ApiInterface:
  def get_system_config():
    pass

  def get_lights():
    pass

  def get_sensors():
    pass


class Api(ApiInterface):
  def __init__(self, hub_url: str):
    self.hub_url = hub_url

  def __hub_url(self, relative_url):
    return "/".join([self.hub_url, relative_url])

  def get_system_config(self):
    with urlopen(self.__hub_url("config")) as response:
      LOG.debug("Retrieving system config from api")
      r = json.loads(response.read())
      LOG.debug("Retrieved system config from api")
      return r

  def get_lights(self):
    with urlopen(self.__hub_url("lights")) as response:
      LOG.debug("Retrieving lights from api")
      r = list(json.loads(response.read()).values())
      LOG.debug("Retrieved lights from api")
      return r

  def get_sensors(self):
    with urlopen(self.__hub_url("sensors")) as response:
      LOG.debug("Retrieving sensors from api")
      r = list(json.loads(response.read()).values())
      LOG.debug("Retrieved sensors from api")
      return r

  def get_batteries(self):
    return list(filter(lambda s: "config" in s and "battery" in s["config"], list(
        self.get_sensors())))


class CachedApi(ApiInterface):
  def __init__(self, api: ApiInterface):
    self.api = api

  def __tf(filename):
    return "/".join([tempfile.gettempdir(), filename])

  def __cache(self, type: str, fn_call):
    temp_filename = f"zabbix-hue.{type}"
    cache_file_path = CachedApi.__tf(f"{temp_filename}.json")
    lock_file = CachedApi.__tf(f"{temp_filename}.lock")

    does_cache_file_exist = exists(cache_file_path)
    cache_age_seconds = time.time(
    ) - os.path.getmtime(cache_file_path) if does_cache_file_exist else 0
    is_cache_file_expired = not does_cache_file_exist or cache_age_seconds >= MAX_CACHE_AGE_SECONDS
    is_cache_hit = not is_cache_file_expired

    if is_cache_hit:
      with open(cache_file_path, "r") as f_json:
        LOG.debug("Cache hit (type=%s,age_seconds=%s,max_cache_age_seconds=%s)",
                  type, round(cache_age_seconds, 1), MAX_CACHE_AGE_SECONDS)
        return json.loads(f_json.read())

    with open(lock_file, "w") as f_lock:
      try:
        flock(f_lock.fileno(), LOCK_EX | LOCK_NB)
        LOG.debug("Acquired lock successfully (file=%s)", lock_file)

        fd, tmp_file_path = mkstemp()
        with open(tmp_file_path, "w") as f_tmp:
          f_tmp.write(json.dumps(fn_call()))

        os.close(fd)

        os.rename(tmp_file_path, cache_file_path)

        with open(cache_file_path) as f_json:
          return json.loads(f_json.read())
      except:
        LOG.debug("Failed to acquire lock, cache hit (file=%s)", lock_file)

    if not does_cache_file_exist:
      return []

    with open(cache_file_path) as f_json:
      return json.loads(f_json.read())

  def get_system_config(self):
    return self.__cache("system", self.api.get_system_config)

  def get_lights(self):
    return self.__cache("lights", self.api.get_lights)

  def get_sensors(self):
    return self.__cache("sensors", self.api.get_sensors)

  def get_batteries(self):
    return self.__cache("batteries", self.api.get_batteries)


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


class HueCommand:
  def _process(value):
    print(value)

  def _mapper(path, type):
    return lambda value: type(reduce(lambda p, field: p[field], path.split("."), value))

  def name(self):
    pass

  def exec(self):
    pass


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

  def __init__(self, api, arguments):
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

  def __init__(self, api, arguments):
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
    self.discovery = Discover(api)

  def get_by_unique_id(unique_id: str, items: list) -> list:
    return list(filter(
        lambda info: "uniqueid" in info and info["uniqueid"] == unique_id,
        items))[0]

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

  def __process(value):
    print(value)

  def discover(self, arguments):
    LOG.debug("Running `discover` command (arguments=%s)", arguments)
    if (len(arguments) != 1):
      LOG.error(
          "Expected exactly one arguments for `discover`, received %s", len(arguments))
      print(
          f"Expected exactly one argument for `discover`, received {len(arguments)}")
      exit(1)
    discovery_type, *_ = arguments

    self.discovery.discover(discovery_type)
    LOG.debug("Finished `discover` command (arguments=%s)", arguments)

  def sensor(self, arguments):
    LOG.debug("Running `sensor` command (arguments=%s)", arguments)
    if (len(arguments) != 2):
      LOG.error(
          "Expected exactly two arguments for `sensor`, received %s", len(arguments))
      print(
          f"Expected exactly two arguments for `sensor`, received {len(arguments)}")
      exit(1)

    device_id, action = arguments

    if action not in CommandHandler.__SENSOR_ACTION_MAP:
      LOG.error("Received unknown action '%s' for `sensor` command", action)
      return

    CommandHandler.__process(self.__map_sensor(
        device_id, CommandHandler.__SENSOR_ACTION_MAP[action]))
    LOG.debug("Finished `sensor` command (arguments=%s)", arguments)

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

  CommandHandler(CachedApi(Api(HUE_HUB_URL))).exec(command, arguments)
  LOG.debug("Finished script (parameters=%s)", sys.argv[1:])
  exit(0)
