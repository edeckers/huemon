# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import json
from urllib.request import urlopen

from huemon.api.api_interface import ApiInterface
from huemon.infrastructure.logger_factory import create_logger

LOG = create_logger()


class Api(ApiInterface):
    def __init__(self, hub_url: str):
        self.hub_url = hub_url

    def __hub_url(self, relative_url):
        return "/".join([self.hub_url, relative_url])

    def __get_resource(self, resource):
        # B310:blacklist audit url open for permitted schemes handled by urllib_safe_opener
        with urlopen(self.__hub_url(resource)) as response:  # nosec
            LOG.debug("Retrieving `%s` from api", resource)
            json_response = json.loads(response.read())
            LOG.debug("Retrieved `%s` from api", resource)
            return json_response

    def get_system_config(self):
        return self.__get_resource("config")

    def get_lights(self):
        return list(self.__get_resource("lights").values())

    def get_sensors(self):
        return list(self.__get_resource("sensors").values())

    def get_batteries(self):
        return list(
            filter(
                lambda s: "config" in s and "battery" in s["config"],
                list(self.get_sensors()),
            )
        )
