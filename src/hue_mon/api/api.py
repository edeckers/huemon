# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

import json

from urllib.request import urlopen
from hue_mon.api_interface import ApiInterface
from hue_mon.logger_factory import create_logger


LOG = create_logger()


class Api(ApiInterface):
  def __init__(self, hub_url: str):
    self.hub_url = hub_url

  def __hub_url(self, relative_url):
    return "/".join([self.hub_url, relative_url])

  def get_system_config(self):
    with urlopen(self.__hub_url("config")) as response:
      LOG.debug("Retrieving system config from api")
      json_response = json.loads(response.read())
      LOG.debug("Retrieved system config from api")
      return json_response

  def get_lights(self):
    with urlopen(self.__hub_url("lights")) as response:
      LOG.debug("Retrieving lights from api")
      json_response = list(json.loads(response.read()).values())
      LOG.debug("Retrieved lights from api")
      return json_response

  def get_sensors(self):
    with urlopen(self.__hub_url("sensors")) as response:
      LOG.debug("Retrieving sensors from api")
      json_response = list(json.loads(response.read()).values())
      LOG.debug("Retrieved sensors from api")
      return json_response

  def get_batteries(self):
    return list(filter(lambda s: "config" in s and "battery" in s["config"], list(
        self.get_sensors())))
