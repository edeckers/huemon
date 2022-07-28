# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import unittest
from unittest.mock import MagicMock, call, patch

from huemon.commands.command_handler import (
    CommandHandler,
    create_name_to_command_mapping,
)
from huemon.commands.internal.system_command import SystemCommand
from huemon.sinks.stdout_sink import StdoutSink
from tests.fixtures import MutableApi


def _ch(system_config: dict):
    mutable_api = MutableApi()
    mutable_api.set_system_config(system_config)

    return CommandHandler(
        create_name_to_command_mapping({}, mutable_api, StdoutSink(), [SystemCommand])
    )


class TestCachedApi(unittest.TestCase):
    @staticmethod
    @patch("builtins.print")
    def test_when_system_version_received_print(mock_print: MagicMock):
        some_version = "SOME_VERSION_0"

        command_handler = _ch(
            {
                "swversion": some_version,
            }
        )

        command_handler.exec("system", ["version"])

        mock_print.assert_called_once_with(some_version)

    @staticmethod
    @patch("builtins.print")
    def test_when_system_upgrade_available_print(mock_print: MagicMock):
        command_handler_0 = _ch(
            {
                "swupdate2": {
                    "bridge": {
                        "state": "noupdates",
                    },
                }
            }
        )

        command_handler_1 = _ch(
            {
                "swupdate2": {
                    "bridge": {
                        "state": "updates",
                    },
                }
            }
        )

        command_handler_0.exec("system", ["is_upgrade_available"])
        command_handler_1.exec("system", ["is_upgrade_available"])

        mock_print.assert_has_calls(list(map(call, [0, 1])))
