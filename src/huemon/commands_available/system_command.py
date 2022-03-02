# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from huemon.api.api_interface import ApiInterface
from huemon.commands.hue_command_interface import HueCommand
from huemon.infrastructure.logger_factory import create_logger
from huemon.util import assert_exists, assert_num_args

LOG = create_logger()


class SystemCommand(HueCommand):
    def __init__(
        self, config: dict, api: ApiInterface
    ):  # pylint: disable=unused-argument
        self.api = api

    def __map_config(self, mapper):
        return mapper(self.api.get_system_config())

    __SYSTEM_ACTION_MAP = {
        "is_upgrade_available": lambda config: int(
            config["swupdate2"]["state"] != "noupdates"
        ),
        "version": HueCommand._mapper("swversion", str),
    }

    @staticmethod
    def name():
        return "system"

    def exec(self, arguments):
        LOG.debug(
            "Running `%s` command (arguments=%s)", SystemCommand.name(), arguments
        )
        assert_num_args(1, arguments, SystemCommand.name())

        action, *_ = arguments

        assert_exists(list(SystemCommand.__SYSTEM_ACTION_MAP), action)

        HueCommand._process(self.__map_config(self.__SYSTEM_ACTION_MAP[action]))
        LOG.debug(
            "Finished `%s` command (arguments=%s)", SystemCommand.name(), arguments
        )
