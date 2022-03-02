# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import os
from pathlib import Path

from genericpath import isdir, isfile

from huemon.commands.hue_command_interface import HueCommand
from huemon.infrastructure.logger_factory import create_logger
from huemon.util import (
    assert_num_args,
    exit_fail,
    get_commands_path,
    get_discoveries_path,
)

LOG = create_logger()


def symlink_plugins(plugins_available_path, plugins_enabled_path):
    for plugins_path in [plugins_available_path, plugins_enabled_path]:
        if not isdir(plugins_path):
            exit_fail("Provided path `%s` does not exist", plugins_path)

    available_plugins = list(Path(plugins_available_path).glob("*.py"))

    LOG.debug(
        "Symlinking %s plugins (from=%s,to=%s)",
        len(available_plugins),
        plugins_available_path,
        plugins_enabled_path,
    )
    for plugin_path in available_plugins:
        target_path = os.path.join(plugins_enabled_path, plugin_path.name)

        if isfile(target_path):
            LOG.debug("Skipping `%s`, symlink already exists", target_path)
            continue

        os.symlink(plugin_path.absolute(), target_path)
    LOG.debug(
        "Finished symlinking %s plugins (from=%s,to=%s)",
        len(available_plugins),
        plugins_available_path,
        plugins_enabled_path,
    )


class InstallAvailableCommand(HueCommand):
    def __init__(self, config: dict):
        self.config = config

    @staticmethod
    def name():
        return "install_available"

    def exec(self, arguments):
        LOG.debug(
            "Running `%s` command (arguments=%s)",
            InstallAvailableCommand.name(),
            arguments,
        )
        assert_num_args(1, arguments, InstallAvailableCommand.name())

        target, *_ = arguments

        if target not in ["commands", "discoveries"]:
            exit_fail(
                "Received unknown action `%s` for `%s` command",
                target,
                InstallAvailableCommand.name(),
            )

        if target == "commands":
            commands_enabled_path = get_commands_path(self.config, "enabled")
            commands_available_path = get_commands_path(self.config, "available")

            symlink_plugins(commands_available_path, commands_enabled_path)

        if target == "discoveries":
            discoveries_enabled_path = get_discoveries_path(self.config, "enabled")
            discoveries_available_path = get_discoveries_path(self.config, "available")

            symlink_plugins(discoveries_available_path, discoveries_enabled_path)

        LOG.debug(
            "Finished `%s` command (arguments=%s)",
            InstallAvailableCommand.name(),
            arguments,
        )
