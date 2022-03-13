# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import unittest
from typing import List
from unittest.mock import MagicMock, call, patch

from huemon.commands.command_handler import (
    CommandHandler,
    create_name_to_command_mapping,
)
from huemon.commands.internal.sensor_command import SensorCommand
from huemon.sinks.stdout_sink import StdoutSink
from tests.fixtures import MutableApi

SOME_SENSOR_MAC_0 = "SO:ME:SE:NS:OR:MA:C0"
SOME_SENSOR_MAC_1 = "SO:ME:SE:NS:OR:MA:C1"


def _ch(sensors: List[dict]):
    mutable_api = MutableApi()
    mutable_api.set_sensors(sensors)

    return CommandHandler(
        create_name_to_command_mapping({}, mutable_api, StdoutSink(), [SensorCommand])
    )


class TestSensorCommand(unittest.TestCase):
    def test_when_sensor_doesnt_exist(self):
        command_handler = _ch([])

        with self.assertRaises(Exception):
            command_handler.exec("sensor", [SOME_SENSOR_MAC_0, "battery:level"])

    @staticmethod
    @patch("builtins.print")
    def test_when_sensor_exists_return_battery_level(mock_print: MagicMock):
        some_level_0 = 80
        some_level_1 = 1

        command_handler = _ch(
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

        command_handler.exec("sensor", [SOME_SENSOR_MAC_0, "battery:level"])
        command_handler.exec("sensor", [SOME_SENSOR_MAC_1, "battery:level"])

        mock_print.assert_has_calls(list(map(call, [some_level_0, some_level_1])))

    @staticmethod
    @patch("builtins.print")
    def test_when_sensor_exists_return_light_level(mock_print: MagicMock):
        some_level_0 = 80
        some_level_1 = 1

        command_handler = _ch(
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

        command_handler.exec("sensor", [SOME_SENSOR_MAC_0, "light:level"])
        command_handler.exec("sensor", [SOME_SENSOR_MAC_1, "light:level"])

        mock_print.assert_has_calls(list(map(call, [some_level_0, some_level_1])))

    @staticmethod
    @patch("builtins.print")
    def test_when_sensor_exists_return_temperature(mock_print: MagicMock):
        some_temperature_0 = 80
        some_temperature_1 = 1

        command_handler = _ch(
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

        command_handler.exec("sensor", [SOME_SENSOR_MAC_0, "temperature"])
        command_handler.exec("sensor", [SOME_SENSOR_MAC_1, "temperature"])

        mock_print.assert_has_calls(
            list(map(call, [some_temperature_0 * 0.01, some_temperature_1 * 0.01]))
        )

    @staticmethod
    @patch("builtins.print")
    def test_when_sensor_exists_return_presence(mock_print: MagicMock):
        some_presence_0 = 80
        some_presence_1 = 1

        command_handler = _ch(
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

        command_handler.exec("sensor", [SOME_SENSOR_MAC_0, "presence"])
        command_handler.exec("sensor", [SOME_SENSOR_MAC_1, "presence"])

        mock_print.assert_has_calls(list(map(call, [some_presence_0, some_presence_1])))

    @staticmethod
    @patch("builtins.print")
    def test_when_sensor_exists_return_reachable(mock_print: MagicMock):
        some_reachability_0 = 0
        some_reachability_1 = 1

        command_handler = _ch(
            [
                {
                    "uniqueid": SOME_SENSOR_MAC_0,
                    "config": {
                        "reachable": some_reachability_0,
                    },
                },
                {
                    "uniqueid": SOME_SENSOR_MAC_1,
                    "config": {
                        "reachable": some_reachability_1,
                    },
                },
            ]
        )

        command_handler.exec("sensor", [SOME_SENSOR_MAC_0, "reachable"])
        command_handler.exec("sensor", [SOME_SENSOR_MAC_1, "reachable"])

        mock_print.assert_has_calls(
            list(map(call, [some_reachability_0, some_reachability_1]))
        )
