from api_interface import ApiInterface
from discovery_interface import Discovery


class LightsDiscovery(Discovery):
  def __init__(self, api: ApiInterface):
    self.api = api

  def name():
    return "lights"

  def exec(self, arguments=None):
    Discovery._print_array_as_discovery(self.api.get_lights()),
