# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import sys
from huemon.api_interface import ApiInterface
from huemon.const import EXIT_FAIL
from huemon.discovery_interface import Discovery
from huemon.logger_factory import create_logger

LOG = create_logger()


class SensorsDiscovery(Discovery):
  def __init__(self, api: ApiInterface):
    self.api = api

  def name():
    return "sensors"

  def exec(self, arguments=None):
    if not arguments or len(arguments) == 0:
      LOG.error(
          "Did not receive enough arguments for `discover sensor:*`, expected 1 received 0")
      print("Did not receive enough arguments for `discover sensor:*`, expected 1 received 0")
      sys.exit(EXIT_FAIL)

    sensor_type, *_ = arguments

    LOG.debug(
        "Running `discover sensor:*` command (sensor_type=%s)", sensor_type)
    if sensor_type not in ["presence", "light", "temperature"]:
      LOG.error(
          "Received unknown sensor type '%s' for `discover sensor:*` command", sensor_type)
      return

    Discovery._print_array_as_discovery(filter(
        Discovery._has_state_field(
            "lightlevel" if sensor_type == "light" else sensor_type),
        self.api.get_sensors()))
    LOG.debug(
        "Finished `discover sensor:*` command (sensor_type=%s)", sensor_type)
