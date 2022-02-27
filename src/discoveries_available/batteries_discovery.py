from hue_mon.api_interface import ApiInterface
from hue_mon.discovery_interface import Discovery


class BatteriesDiscovery(Discovery):
  def __init__(self, api: ApiInterface):
    self.api = api

  def name():
    return "batteries"

  def exec(self, arguments=None):
    Discovery._print_array_as_discovery(self.api.get_batteries()),
