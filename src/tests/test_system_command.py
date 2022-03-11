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
from tests.fixtures import MutableApi


class TestCachedApi(unittest.TestCase):
    @staticmethod
    @patch("builtins.print")
    def test_when_system_version_received_print(mock_print: MagicMock):
        some_version = "SOME_VERSION_0"

        mutable_api = MutableApi()
        mutable_api.set_system_config(
            {
                "swversion": some_version,
            }
        )

        command_handler = CommandHandler(
            create_name_to_command_mapping({}, mutable_api, [SystemCommand])
        )

        command_handler.exec("system", ["version"])

        mock_print.assert_called_once_with(some_version)

    @staticmethod
    @patch("builtins.print")
    def test_when_system_upgrade_available_print(mock_print: MagicMock):
        mutable_api_0 = MutableApi()
        mutable_api_0.set_system_config(
            {
                "swupdate2": {
                    "state": "noupdates",
                }
            }
        )

        mutable_api_1 = MutableApi()
        mutable_api_1.set_system_config(
            {
                "swupdate2": {
                    "state": "updates",
                }
            }
        )

        command_handler_0 = CommandHandler(
            create_name_to_command_mapping({}, mutable_api_0, [SystemCommand])
        )
        command_handler_1 = CommandHandler(
            create_name_to_command_mapping({}, mutable_api_1, [SystemCommand])
        )

        command_handler_0.exec("system", ["is_upgrade_available"])
        command_handler_1.exec("system", ["is_upgrade_available"])

        mock_print.assert_has_calls(map(call, [0, 1]))
