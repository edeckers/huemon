# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from functools import reduce

from huemon.api.api_factory import create_api
from huemon.api.api_interface import ApiInterface
from huemon.commands.hue_command_interface import HueCommand
from huemon.commands_internal.install_available_command import InstallAvailableCommand
from huemon.infrastructure.logger_factory import create_logger
from huemon.plugin_loader import load_plugins
from huemon.util import exit_fail

LOG = create_logger()


def create_name_to_command_mapping(config: dict, api: ApiInterface, plugins: list):
    return reduce(lambda p, c: {**p, c.name(): c(config, api)}, plugins, {})


def __load_command_plugins(config: dict, command_plugins_path: str):
    LOG.debug("Loading command plugins (path=%s)", command_plugins_path)
    command_handler_plugins = create_name_to_command_mapping(
        config,
        create_api(config),
        load_plugins("command", command_plugins_path, HueCommand),
    )
    LOG.debug("Finished loading command plugins (path=%s)", command_plugins_path)

    return command_handler_plugins


def __load_plugins_and_hardwired_handlers(config: dict, command_plugins_path: str):
    return {
        **__load_command_plugins(config, command_plugins_path),
        InstallAvailableCommand.name(): InstallAvailableCommand(config),
    }


def create_default_command_handler(config: dict, command_plugins_path: str):
    return CommandHandler(
        __load_plugins_and_hardwired_handlers(config, command_plugins_path)
    )


class CommandHandler:  # pylint: disable=too-few-public-methods
    def __init__(self, handlers):
        self.handlers = handlers

    def available_commands(self):
        return list(self.handlers)

    def exec(self, command: str, arguments):
        LOG.debug("Running command `%s` (arguments=%s)", command, arguments)
        if not command in self.handlers:
            exit_fail(
                "Received unknown command `%s`, expected one of %s",
                command,
                self.available_commands(),
            )

        self.handlers[command].exec(arguments)

        LOG.debug("Finished command `%s` (arguments=%s)", command, arguments)
