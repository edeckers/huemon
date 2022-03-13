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
from huemon.commands.internal.system_command import SystemCommand
from huemon.sinks.stdout_sink import StdoutSink
from huemon.utils.const import EXIT_FAIL
from tests.fixtures import MutableApi, create_system_config


def _ch(system_config: dict):
    mutable_api = MutableApi()
    mutable_api.set_system_config(system_config)

    return CommandHandler(
        create_name_to_command_mapping({}, mutable_api, StdoutSink(), [SystemCommand])
    )


class TestCachedApi(unittest.TestCase):
    def test_when_command_is_loaded_it_should_be_listed_as_available(self):
        vanilla_command_handler = CommandHandler([])

        command_handler = _ch({})

        expected_command = SystemCommand.name()

        self.assertIn(
            expected_command,
            command_handler.available_commands(),
            "The command should be known by the CommandHandler",
        )
        self.assertNotIn(
            expected_command,
            vanilla_command_handler.available_commands(),
            "The command should not be known by the CommandHandler",
        )

    @staticmethod
    @patch("builtins.print")
    def test_when_cache_not_expired_return_cache(mock_print: MagicMock):
        some_version = "TEST_VERSION"

        command_handler = _ch(create_system_config(version=some_version))

        command_handler.exec("system", ["version"])

        mock_print.assert_called_once_with(some_version)

    def test_when_unknown_command_received_system_exit_is_called(self):
        vanilla_command_handler = CommandHandler([])

        with self.assertRaises(SystemExit) as failed_call_context:
            vanilla_command_handler.exec("system", ["version"])

        self.assertEqual(
            EXIT_FAIL,
            failed_call_context.exception.code,
            f"Exit code should equal {EXIT_FAIL}",
        )
