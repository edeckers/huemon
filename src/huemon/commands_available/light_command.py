# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from huemon.api_interface import ApiInterface
from huemon.commands_available.sensor_command import SensorCommand
from huemon.hue_command_interface import HueCommand
from huemon.logger_factory import create_logger
from huemon.util import assert_num_args, exit_fail

LOG = create_logger()


class LightCommand(HueCommand):
  def __init__(self, config: dict, api: ApiInterface):
    self.api = api

  __LIGHT_ACTION_MAP = {
      "is_upgrade_available": lambda light: int(light["swupdate"]["state"] != "noupdates"),
      "reachable": HueCommand._mapper("state.reachable", int),
      "status": HueCommand._mapper("state.on", int),
      "version": HueCommand._mapper("swversion", str),
  }

  def __get_light(self, unique_id):
    return HueCommand.get_by_unique_id(unique_id, self.api.get_lights())

  def __map_light(self, unique_id, mapper):
    return mapper(self.__get_light(unique_id))

  def name():
    return "light"

  def exec(self, arguments):
    LOG.debug(
        "Running `%s` command (arguments=%s)",
        LightCommand.name(),
        arguments)
    assert_num_args(2, arguments, LightCommand.name())

    light_id, action = arguments

    if action not in LightCommand.__LIGHT_ACTION_MAP:
      exit_fail(
          "Received unknown action `%s` for `%s` command",
          action,
          LightCommand.name())

    HueCommand._process(
        LightCommand.__map_light(light_id, LightCommand.__LIGHT_ACTION_MAP[action]))

    LOG.debug(
        "Finished `%s` command (arguments=%s)",
        LightCommand.name(),
        arguments)
