# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from huemon.commands.hue_command_interface import HueCommand
from huemon.infrastructure.logger_factory import create_logger
from huemon.utils.assertions import assert_exists_e, assert_num_args_e

LOG = create_logger()


class LightCommand(HueCommand):
    __LIGHT_ACTION_MAP = {
        "is_upgrade_available": lambda light: int(
            light["swupdate"]["state"] != "noupdates"
        ),
        "reachable": HueCommand._mapper("state.reachable", int),
        "status": HueCommand._mapper("state.on", int),
        "version": HueCommand._mapper("swversion", str),
    }

    def __get_light(self, unique_id):
        return HueCommand.get_by_unique_id(unique_id, self.api.get_lights())

    def __map_light(self, unique_id, mapper):
        return mapper(self.__get_light(unique_id))

    @staticmethod
    def name():
        return "light"

    def exec(self, arguments):
        LOG.debug("Running `%s` command (arguments=%s)", LightCommand.name(), arguments)
        assert_num_args_e(2, arguments, LightCommand.name())

        light_id, action = arguments

        assert_exists_e(list(LightCommand.__LIGHT_ACTION_MAP), action)

        self._process(
            self.__map_light(light_id, LightCommand.__LIGHT_ACTION_MAP[action])
        )

        LOG.debug(
            "Finished `%s` command (arguments=%s)", LightCommand.name(), arguments
        )
