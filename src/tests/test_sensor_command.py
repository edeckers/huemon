# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import unittest
from unittest.mock import MagicMock, patch

from huemon.commands.command_handler import (
    CommandHandler,
    create_name_to_command_mapping,
)
from huemon.commands_available.sensor_command import SensorCommand
from tests.fixtures import MutableApi, read_result

CACHE_VALIDITY_INFINITE_SECONDS = 1_000_000
CACHE_VALIDITY_ZERO_SECONDS = 0


SOME_SENSOR_MAC_0 = "SO:ME:SE:NS:OR:MA:C0"
SOME_SENSOR_MAC_1 = "SO:ME:SE:NS:OR:MA:C1"

#        "battery:level": HueCommand._mapper("config.battery", float),
#        "light:level": HueCommand._mapper("state.lightlevel", float),
#        "presence": HueCommand._mapper("state.presence", int),
#        "reachable": HueCommand._mapper("config.reachable", int),
#        "temperature": lambda device: float(device["state"]["temperature"] / 100),


class TestSensorCommand(unittest.TestCase):
    def test_when_sensor_doesnt_exist(self):
        mutable_api = MutableApi()
        mutable_api.set_sensors([])

        command_handler = CommandHandler(
            create_name_to_command_mapping({}, mutable_api, [SensorCommand])
        )

        with self.assertRaises(Exception):
            command_handler.exec("sensor", [SOME_SENSOR_MAC_0, "battery:level"])

    @patch("builtins.print")
    def test_when_sensor_exists_return_battery_level(self, mock_print: MagicMock):
        some_level_0 = 80
        some_level_1 = 1

        mutable_api = MutableApi()
        mutable_api.set_sensors(
            [
                {
                    "uniqueid": SOME_SENSOR_MAC_0,
                    "config": {
                        "battery": some_level_0,
                    },
                },
                {
                    "uniqueid": SOME_SENSOR_MAC_1,
                    "config": {
                        "battery": some_level_1,
                    },
                },
            ]
        )

        command_handler = CommandHandler(
            create_name_to_command_mapping({}, mutable_api, [SensorCommand])
        )

        command_handler.exec("sensor", [SOME_SENSOR_MAC_0, "battery:level"])
        state_sensor_0 = read_result(mock_print)
        command_handler.exec("sensor", [SOME_SENSOR_MAC_1, "battery:level"])
        state_sensor_1 = read_result(mock_print)

        self.assertEqual(some_level_0, state_sensor_0)
        self.assertEqual(some_level_1, state_sensor_1)
