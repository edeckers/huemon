# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from huemon.discoveries.discovery_interface import Discovery
from huemon.utils.monads.either import right


class BatteriesDiscovery(Discovery):
    @staticmethod
    def name():
        return "batteries"

    def exec(self, arguments=None):
        self.sink.process(
            right(Discovery._array_as_discovery(self.api.get_batteries()))
        )
