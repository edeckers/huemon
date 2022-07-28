# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import time
from typing import List

from huemon.api.api_interface import ApiInterface

FIELD_STATE = "state"

FIELD_SYSTEM_IS_UPDATE_AVAILABLE = "is_update_available"
FIELD_SYSTEM_SWUPDATE2 = "swupdate2"
FIELD_SYSTEM_SWUPDATE2_BRIDGE = "bridge"
FIELD_SYSTEM_SWUPDATE2_NOUPDATES = "noupdates"
FIELD_SYSTEM_SWVERSION = "swversion"


def __generate_version():
    return str(time.process_time())


def create_system_config(version: str = None, is_update_available: bool = False):
    return {
        FIELD_SYSTEM_SWUPDATE2: {
            FIELD_SYSTEM_SWUPDATE2_BRIDGE: {
                FIELD_STATE: FIELD_SYSTEM_SWUPDATE2_NOUPDATES
                if is_update_available
                else ""
            }
        },
        FIELD_SYSTEM_SWVERSION: version if version else __generate_version(),
    }


class MutableApi(ApiInterface):
    def __init__(self):
        self.lights = []
        self.sensors = []
        self.system_config = {}

    def set_system_config(self, json_data: dict):
        self.system_config = json_data

    def set_lights(self, json_data: List[dict]):
        self.lights = json_data

    def set_sensors(self, json_data: List[dict]):
        self.sensors = json_data

    def get_system_config(self):
        return self.system_config

    def get_lights(self):
        return self.lights

    def get_sensors(self):
        return self.sensors
