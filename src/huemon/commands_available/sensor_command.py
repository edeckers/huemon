# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from functools import reduce
from huemon.api_interface import ApiInterface
from huemon.hue_command_interface import HueCommand
from huemon.logger_factory import create_logger
from huemon.util import exit_fail

LOG = create_logger()


class SensorCommand(HueCommand):
  def __init__(self, config: dict, api: ApiInterface):
    self.api = api

  def __get_sensor(self, device_id):
    return HueCommand.get_by_unique_id(device_id, self.api.get_sensors())

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

  def name():
    return "sensor"

  def exec(self, arguments):
    LOG.debug("Running `sensor` command (arguments=%s)", arguments)
    if (len(arguments) != 2):
      exit_fail(
          "Expected exactly two arguments for `sensor`, received %s", len(arguments))

    device_id, action = arguments

    if action not in SensorCommand.__SENSOR_ACTION_MAP:
      LOG.error("Received unknown action '%s' for `sensor` command", action)
      return

    HueCommand._process(self.__map_sensor(
        device_id, SensorCommand.__SENSOR_ACTION_MAP[action]))
    LOG.debug("Finished `sensor` command (arguments=%s)", arguments)
