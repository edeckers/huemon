from api_interface import ApiInterface
from discoveries_available.batteries_discovery import BatteriesDiscovery
from discoveries_available.lights_discovery import LightsDiscovery
from discoveries_available.sensors_discovery import SensorsDiscovery
from hue_command_interface import HueCommand
from logger_factory import create_logger

LOG = create_logger()


class Discover:
  def __init__(self, api: ApiInterface):
    self.api = api

  __DISCOVERY_HANDLERS = {
      "batteries": lambda api, _: BatteriesDiscovery(api).exec(),
      "lights": lambda api, _: LightsDiscovery(api).exec(),
      "sensors": lambda api, arguments: SensorsDiscovery(api).exec(arguments)
  }

  def discover(self, discovery_type):
    LOG.debug(
        "Running `discover` command (discovery_type=%s)", discovery_type)
    target, maybe_sub_target, *_ = discovery_type.split(":") + [None]

    if target not in Discover.__DISCOVERY_HANDLERS:
      LOG.error(
          "Received unknown target '%s' for `discover` command", target)
      return

    Discover.__DISCOVERY_HANDLERS[target](
        self.api, [maybe_sub_target] if maybe_sub_target else [])
    LOG.debug(
        "Finished `discover` command (discovery_type=%s)", discovery_type)


class DiscoverCommand(HueCommand):
  def __init__(self, config: dict, api: ApiInterface):
    self.discovery = Discover(api)

  def name():
    return "discover"

  def exec(self, arguments):
    LOG.debug("Running `discover` command (arguments=%s)", arguments)
    if (len(arguments) != 1):
      LOG.error(
          "Expected exactly one arguments for `discover`, received %s", len(arguments))
      print(
          f"Expected exactly one argument for `discover`, received {len(arguments)}")
      exit(1)
    discovery_type, *_ = arguments

    self.discovery.discover(discovery_type)
    LOG.debug("Finished `discover` command (arguments=%s)", arguments)
