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
from huemon.commands.internal.light_command import LightCommand
from huemon.processors.stdout_processor import StdoutProcessor
from huemon.utils.const import EXIT_FAIL
from tests.fixtures import MutableApi

SOME_LIGHT_MAC_0 = "SO:ME:LI:GH:TM:AC:00"
SOME_LIGHT_MAC_1 = "SO:ME:LI:GH:TM:AC:01"


def _ch(lights: List[dict]):
    mutable_api = MutableApi()
    mutable_api.set_lights(lights)

    return CommandHandler(
        create_name_to_command_mapping(
            {}, mutable_api, StdoutProcessor(), [LightCommand]
        )
    )


class TestLightCommand(unittest.TestCase):
    def test_when_light_doesnt_exist_raise(self):
        command_handler = _ch([])

        with self.assertRaises(Exception):
            command_handler.exec("light", [SOME_LIGHT_MAC_0, "status"])

    def test_when_not_enough_parameters_raise(self):
        command_handler = _ch([])

        with self.assertRaises(SystemExit) as failed_call_context:
            command_handler.exec("light", [])

        self.assertEqual(
            EXIT_FAIL,
            failed_call_context.exception.code,
            f"Exit code should equal {EXIT_FAIL}",
        )

    def test_when_unknown_action_raise(self):
        command_handler = _ch([])

        with self.assertRaises(SystemExit) as failed_call_context:
            command_handler.exec("light", [SOME_LIGHT_MAC_0, "some_unknown_action"])

        self.assertEqual(
            EXIT_FAIL,
            failed_call_context.exception.code,
            f"Exit code should equal {EXIT_FAIL}",
        )

    @staticmethod
    @patch("builtins.print")
    def test_when_light_exists_return_status(mock_print: MagicMock):
        command_handler = _ch(
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

        command_handler.exec("light", [SOME_LIGHT_MAC_0, "status"])
        command_handler.exec("light", [SOME_LIGHT_MAC_1, "status"])

        mock_print.assert_has_calls(list(map(call, [1, 0])))

    @staticmethod
    @patch("builtins.print")
    def test_when_light_exists_return_is_upgrade_available(mock_print: MagicMock):
        command_handler = _ch(
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

        command_handler.exec("light", [SOME_LIGHT_MAC_0, "is_upgrade_available"])
        command_handler.exec("light", [SOME_LIGHT_MAC_1, "is_upgrade_available"])

        mock_print.assert_has_calls(list(map(call, [0, 1])))

    @staticmethod
    @patch("builtins.print")
    def test_when_light_exists_return_is_reachable(mock_print: MagicMock):
        command_handler = _ch(
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

        command_handler.exec("light", [SOME_LIGHT_MAC_0, "reachable"])
        command_handler.exec("light", [SOME_LIGHT_MAC_1, "reachable"])

        mock_print.assert_has_calls(list(map(call, [0, 1])))

    @staticmethod
    @patch("builtins.print")
    def test_when_light_exists_return_version(mock_print: MagicMock):
        some_version_0 = "some_version_0"
        some_version_1 = "some_version_1"

        command_handler = _ch(
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

        command_handler.exec("light", [SOME_LIGHT_MAC_0, "version"])
        command_handler.exec("light", [SOME_LIGHT_MAC_1, "version"])

        mock_print.assert_has_calls(list(map(call, [some_version_0, some_version_1])))
