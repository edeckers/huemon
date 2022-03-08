# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import uvicorn

from huemon.api.api_interface import ApiInterface
from huemon.api_server import HuemonServerFactory
from huemon.commands.hue_command_interface import HueCommand
from huemon.infrastructure.logger_factory import create_logger
from huemon.util import assert_exists, assert_num_args

LOG = create_logger()


class MyServer:  # pylint: disable=too-few-public-methods
    @staticmethod
    def start(config: dict):
        host = config["host"] if "host" in config else "127.0.0.1"
        port = int(config["port"]) if "port" in config else 8000

        uvicorn.run(HuemonServerFactory.create(config), host=host, port=port)


class AgentCommand(HueCommand):
    __SYSTEM_ACTION_MAP = {
        "start": MyServer.start,
    }

    def __init__(
        self, config: dict, _: ApiInterface
    ):  # pylint: disable=unused-argument
        self.config = config

    @staticmethod
    def name():
        return "agent"

    def exec(self, arguments):
        LOG.debug("Running `%s` command (arguments=%s)", AgentCommand.name(), arguments)
        assert_num_args(1, arguments, AgentCommand.name())

        action, *_ = arguments

        assert_exists(list(AgentCommand.__SYSTEM_ACTION_MAP), action)

        HueCommand._process(self.__SYSTEM_ACTION_MAP[action](self.config))
        LOG.debug(
            "Finished `%s` command (arguments=%s)", AgentCommand.name(), arguments
        )
