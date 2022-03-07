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
from huemon.commands_available.system_command import SystemCommand
from tests.fixtures import MutableApi, read_result


class TestCachedApi(unittest.TestCase):
    @patch("builtins.print")
    def test_when_system_version_received_print(self, mock_print: MagicMock):
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
        state_light_0 = read_result(mock_print)

        self.assertEqual(some_version, state_light_0)

    @patch("builtins.print")
    def test_when_system_upgrade_available_print(self, mock_print: MagicMock):
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
        system_is_upgrade_0 = read_result(mock_print)
        command_handler_1.exec("system", ["is_upgrade_available"])
        system_is_upgrade_1 = read_result(mock_print)

        self.assertEqual(0, system_is_upgrade_0)
        self.assertEqual(1, system_is_upgrade_1)
