# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from huemon.api.api_interface import ApiInterface
from huemon.commands.hue_command_interface import HueCommand
from huemon.infrastructure.logger_factory import create_logger
from huemon.util import assert_exists, assert_num_args

LOG = create_logger()


class SensorCommand(HueCommand):
    def __init__(
        self, config: dict, api: ApiInterface
    ):  # pylint: disable=unused-argument
        self.api = api

    def __get_sensor(self, device_id):
        return HueCommand.get_by_unique_id(device_id, self.api.get_sensors())

    def __map_sensor(self, unique_id, mapper):
        return mapper(self.__get_sensor(unique_id))

    __SENSOR_ACTION_MAP = {
        "battery:level": HueCommand._mapper("config.battery", float),
        "light:level": HueCommand._mapper("state.lightlevel", float),
        "presence": HueCommand._mapper("state.presence", int),
        "reachable": HueCommand._mapper("config.reachable", int),
        "temperature": lambda device: float(device["state"]["temperature"] / 100),
    }

    @staticmethod
    def name():
        return "sensor"

    def exec(self, arguments):
        LOG.debug(
            "Running `%s` command (arguments=%s)", SensorCommand.name(), arguments
        )
        assert_num_args(2, arguments, SensorCommand.name())

        device_id, action = arguments

        assert_exists(list(SensorCommand.__SENSOR_ACTION_MAP), action)

        HueCommand._process(
            self.__map_sensor(device_id, SensorCommand.__SENSOR_ACTION_MAP[action])
        )
        LOG.debug(
            "Finished `%s` command (arguments=%s)", SensorCommand.name(), arguments
        )
