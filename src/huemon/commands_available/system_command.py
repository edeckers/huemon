# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from huemon.api_interface import ApiInterface
from huemon.hue_command_interface import HueCommand
from huemon.logger_factory import create_logger
from huemon.util import exit_fail

LOG = create_logger()


class SystemCommand(HueCommand):
  def __init__(self, config: dict, api: ApiInterface):
    self.api = api

  def __map_config(self, mapper):
    return mapper(self.api.get_system_config())

  __SYSTEM_ACTION_MAP = {
      "is_upgrade_available": lambda config: int(config["swupdate2"]["state"] != "noupdates"),
      "version": HueCommand._mapper("swversion", str),
  }

  def name():
    return "system"

  def exec(self, arguments):
    LOG.debug(
        "Running `%s` command (arguments=%s)",
        SystemCommand.name(),
        arguments)
    if (len(arguments) != 1):
      exit_fail(
          "Expected exactly one argument for `%s` command, received %s",
          SystemCommand.name(),
          len(arguments))

    action, *_ = arguments

    if action not in self.__SYSTEM_ACTION_MAP:
      exit_fail(
          "Received unknown action `%s` for `%s` command",
          action,
          SystemCommand.name())

    HueCommand._process(self.__map_config(self.__SYSTEM_ACTION_MAP[action]))
    LOG.debug(
        "Finished `%s` command (arguments=%s)",
        SystemCommand.name(),
        arguments)
