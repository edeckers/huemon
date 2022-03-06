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

    @patch("builtins.print")
    def test_when_sensor_exists_return_light_level(self, mock_print: MagicMock):
        some_level_0 = 80
        some_level_1 = 1

        mutable_api = MutableApi()
        mutable_api.set_sensors(
            [
                {
                    "uniqueid": SOME_SENSOR_MAC_0,
                    "state": {
                        "lightlevel": some_level_0,
                    },
                },
                {
                    "uniqueid": SOME_SENSOR_MAC_1,
                    "state": {
                        "lightlevel": some_level_1,
                    },
                },
            ]
        )

        command_handler = CommandHandler(
            create_name_to_command_mapping({}, mutable_api, [SensorCommand])
        )

        command_handler.exec("sensor", [SOME_SENSOR_MAC_0, "light:level"])
        state_sensor_0 = read_result(mock_print)
        command_handler.exec("sensor", [SOME_SENSOR_MAC_1, "light:level"])
        state_sensor_1 = read_result(mock_print)

        self.assertEqual(some_level_0, state_sensor_0)
        self.assertEqual(some_level_1, state_sensor_1)

    @patch("builtins.print")
    def test_when_sensor_exists_return_temperature(self, mock_print: MagicMock):
        some_temperature_0 = 80
        some_temperature_1 = 1

        mutable_api = MutableApi()
        mutable_api.set_sensors(
            [
                {
                    "uniqueid": SOME_SENSOR_MAC_0,
                    "state": {
                        "temperature": some_temperature_0,
                    },
                },
                {
                    "uniqueid": SOME_SENSOR_MAC_1,
                    "state": {
                        "temperature": some_temperature_1,
                    },
                },
            ]
        )

        command_handler = CommandHandler(
            create_name_to_command_mapping({}, mutable_api, [SensorCommand])
        )

        command_handler.exec("sensor", [SOME_SENSOR_MAC_0, "temperature"])
        state_sensor_0 = read_result(mock_print)
        command_handler.exec("sensor", [SOME_SENSOR_MAC_1, "temperature"])
        state_sensor_1 = read_result(mock_print)

        self.assertEqual(some_temperature_0, state_sensor_0 * 100)
        self.assertEqual(some_temperature_1, state_sensor_1 * 100)

    @patch("builtins.print")
    def test_when_sensor_exists_return_presence(self, mock_print: MagicMock):
        some_presence_0 = 80
        some_presence_1 = 1

        mutable_api = MutableApi()
        mutable_api.set_sensors(
            [
                {
                    "uniqueid": SOME_SENSOR_MAC_0,
                    "state": {
                        "presence": some_presence_0,
                    },
                },
                {
                    "uniqueid": SOME_SENSOR_MAC_1,
                    "state": {
                        "presence": some_presence_1,
                    },
                },
            ]
        )

        command_handler = CommandHandler(
            create_name_to_command_mapping({}, mutable_api, [SensorCommand])
        )

        command_handler.exec("sensor", [SOME_SENSOR_MAC_0, "presence"])
        state_sensor_0 = read_result(mock_print)
        command_handler.exec("sensor", [SOME_SENSOR_MAC_1, "presence"])
        state_sensor_1 = read_result(mock_print)

        self.assertEqual(some_presence_0, state_sensor_0)
        self.assertEqual(some_presence_1, state_sensor_1)

    @patch("builtins.print")
    def test_when_sensor_exists_return_reachable(self, mock_print: MagicMock):
        some_presence_0 = 0
        some_presence_1 = 1

        mutable_api = MutableApi()
        mutable_api.set_sensors(
            [
                {
                    "uniqueid": SOME_SENSOR_MAC_0,
                    "config": {
                        "reachable": some_presence_0,
                    },
                },
                {
                    "uniqueid": SOME_SENSOR_MAC_1,
                    "config": {
                        "reachable": some_presence_1,
                    },
                },
            ]
        )

        command_handler = CommandHandler(
            create_name_to_command_mapping({}, mutable_api, [SensorCommand])
        )

        command_handler.exec("sensor", [SOME_SENSOR_MAC_0, "reachable"])
        state_sensor_0 = read_result(mock_print)
        command_handler.exec("sensor", [SOME_SENSOR_MAC_1, "reachable"])
        state_sensor_1 = read_result(mock_print)

        self.assertEqual(some_presence_0, state_sensor_0)
        self.assertEqual(some_presence_1, state_sensor_1)
