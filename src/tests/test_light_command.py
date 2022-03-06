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
from huemon.commands_available.light_command import LightCommand
from tests.fixtures import MutableApi, read_result

CACHE_VALIDITY_INFINITE_SECONDS = 1_000_000
CACHE_VALIDITY_ZERO_SECONDS = 0


SOME_LIGHT_MAC_0 = "SO:ME:LI:GH:TM:AC:00"
SOME_LIGHT_MAC_1 = "SO:ME:LI:GH:TM:AC:01"


class TestLightCommand(unittest.TestCase):
    @patch("builtins.print")
    def test_when_light_exists_return_status(self, mock_print: MagicMock):
        mutable_api = MutableApi()
        mutable_api.set_lights(
            [
                {
                    "uniqueid": SOME_LIGHT_MAC_0,
                    "state": {
                        "on": 1,
                    },
                },
                {
                    "uniqueid": SOME_LIGHT_MAC_1,
                    "state": {
                        "on": 0,
                    },
                },
            ]
        )

        command_handler = CommandHandler(
            create_name_to_command_mapping({}, mutable_api, [LightCommand])
        )

        command_handler.exec("light", [SOME_LIGHT_MAC_0, "status"])
        state_light_0 = read_result(mock_print)
        command_handler.exec("light", [SOME_LIGHT_MAC_1, "status"])
        state_light_1 = read_result(mock_print)

        self.assertEqual(1, state_light_0)
        self.assertEqual(0, state_light_1)

    @patch("builtins.print")
    def test_when_light_exists_return_is_upgrade_available(self, mock_print: MagicMock):
        mutable_api = MutableApi()
        mutable_api.set_lights(
            [
                {
                    "uniqueid": SOME_LIGHT_MAC_0,
                    "swupdate": {
                        "state": "noupdates",
                    },
                },
                {
                    "uniqueid": SOME_LIGHT_MAC_1,
                    "swupdate": {
                        "state": "update-available",
                    },
                },
            ]
        )

        command_handler = CommandHandler(
            create_name_to_command_mapping({}, mutable_api, [LightCommand])
        )

        command_handler.exec("light", [SOME_LIGHT_MAC_0, "is_upgrade_available"])
        state_light_0 = read_result(mock_print)
        command_handler.exec("light", [SOME_LIGHT_MAC_1, "is_upgrade_available"])
        state_light_1 = read_result(mock_print)

        self.assertEqual(0, state_light_0)
        self.assertEqual(1, state_light_1)

    @patch("builtins.print")
    def test_when_light_exists_return_is_reachable(self, mock_print: MagicMock):
        mutable_api = MutableApi()
        mutable_api.set_lights(
            [
                {"uniqueid": SOME_LIGHT_MAC_0, "state": {"reachable": 0}},
                {
                    "uniqueid": SOME_LIGHT_MAC_1,
                    "state": {
                        "reachable": 1,
                    },
                },
            ]
        )

        command_handler = CommandHandler(
            create_name_to_command_mapping({}, mutable_api, [LightCommand])
        )

        command_handler.exec("light", [SOME_LIGHT_MAC_0, "reachable"])
        state_light_0 = read_result(mock_print)
        command_handler.exec("light", [SOME_LIGHT_MAC_1, "reachable"])
        state_light_1 = read_result(mock_print)

        self.assertEqual(0, state_light_0)
        self.assertEqual(1, state_light_1)

    @patch("builtins.print")
    def test_when_light_exists_return_version(self, mock_print: MagicMock):
        some_version_0 = "some_version_0"
        some_version_1 = "some_version_1"

        mutable_api = MutableApi()
        mutable_api.set_lights(
            [
                {
                    "uniqueid": SOME_LIGHT_MAC_0,
                    "swversion": some_version_0,
                },
                {
                    "uniqueid": SOME_LIGHT_MAC_1,
                    "swversion": some_version_1,
                },
            ]
        )

        command_handler = CommandHandler(
            create_name_to_command_mapping({}, mutable_api, [LightCommand])
        )

        command_handler.exec("light", [SOME_LIGHT_MAC_0, "version"])
        state_light_0 = read_result(mock_print)
        command_handler.exec("light", [SOME_LIGHT_MAC_1, "version"])
        state_light_1 = read_result(mock_print)

        self.assertEqual(some_version_0, state_light_0)
        self.assertEqual(some_version_1, state_light_1)
