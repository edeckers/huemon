# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from huemon.api.api_interface import ApiInterface
from huemon.discoveries.discovery_interface import Discovery
from huemon.infrastructure.logger_factory import create_logger
from huemon.utils.errors import exit_fail

LOG = create_logger()

TYPE_LIGHT = "light"
TYPE_PRESENCE = "presence"
TYPE_TEMPERATURE = "temperature"

SENSOR_TYPES = [TYPE_LIGHT, TYPE_PRESENCE, TYPE_TEMPERATURE]


class SensorsDiscovery(Discovery):
    def __init__(self, api: ApiInterface):
        self.api = api

    @staticmethod
    def name():
        return "sensors"

    def exec(self, arguments=None):
        if not arguments or len(arguments) == 0:
            exit_fail(
                "Did not receive enough arguments for `discover sensor:*`, expected 1 received 0"
            )

        sensor_type, *_ = arguments

        LOG.debug("Running `discover sensor:*` command (sensor_type=%s)", sensor_type)
        if sensor_type not in SENSOR_TYPES:
            exit_fail(
                "Received unknown sensor type '%s' for `discover sensor:*` command (expected=%s)",
                sensor_type,
                SENSOR_TYPES,
            )

        Discovery._print_array_as_discovery(
            filter(
                Discovery._has_state_field(
                    "lightlevel" if sensor_type == "light" else sensor_type
                ),
                self.api.get_sensors(),
            )
        )
        LOG.debug("Finished `discover sensor:*` command (sensor_type=%s)", sensor_type)
