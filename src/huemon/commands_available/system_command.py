# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import sys
from huemon.api_interface import ApiInterface
from huemon.const import EXIT_FAIL
from huemon.hue_command_interface import HueCommand
from huemon.logger_factory import create_logger
from huemon.util import exit_fail

LOG = create_logger()


class SystemCommand(HueCommand):
  def __init__(self, config: dict, api: ApiInterface):
    self.api = api

  def __map_config(self, mapper):
    return mapper(self.api.get_system_config())

  def __MAPPER_SYSTEM_UPGRADE_AVAILABLE(config): return int(
      config["swupdate2"]["state"] != "noupdates")
  __MAPPER_VERSION = HueCommand._mapper("swversion", str)

  __SYSTEM_ACTION_MAP = {
      "is_upgrade_available": __MAPPER_SYSTEM_UPGRADE_AVAILABLE,
      "version": __MAPPER_VERSION,
  }

  def name():
    return "system"

  def exec(self, arguments):
    LOG.debug("Running `system` command (arguments=%s)", arguments)
    if (len(arguments) != 1):
      exit_fail(
          "Expected exactly one argument for `system`, received %s", len(arguments))

    action, *_ = arguments

    if action not in self.__SYSTEM_ACTION_MAP:
      LOG.error("Received unknown action '%s' for `system` command", action)
      return

    HueCommand._process(self.__map_config(self.__SYSTEM_ACTION_MAP[action]))
    LOG.debug("Finished `system` command (arguments=%s)", arguments)
