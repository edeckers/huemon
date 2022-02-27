from functools import reduce
import json
from api_interface import ApiInterface
from hue_command_interface import HueCommand
from logger_factory import create_logger

LOG = create_logger()


class Discovery:
  def _item_to_discovery(item):
    return {
        "{#NAME}": item["name"],
        "{#UNIQUE_ID}": item["uniqueid"],
    }

  def _has_state_field(field: str):
    return lambda item: \
        "state" in item and \
        field in item["state"] and \
        "recycle" not in item

  def _print_array_as_discovery(items):
    print(json.dumps({"data": reduce(
        lambda p, item: [*p, Discovery._item_to_discovery(item)],
        items,
        [])}))

  def name():
    pass

  def exec(self, arguments=None):
    pass


class BatteriesDiscovery(Discovery):
  def __init__(self, api: ApiInterface):
    self.api = api

  def name():
    return "batteries"

  def exec(self, arguments=None):
    Discovery._print_array_as_discovery(self.api.get_batteries()),


class LightsDiscovery(Discovery):
  def __init__(self, api: ApiInterface):
    self.api = api

  def name():
    return "lights"

  def exec(self, arguments=None):
    Discovery._print_array_as_discovery(self.api.get_lights()),


class SensorsDiscovery(Discovery):
  def __init__(self, api: ApiInterface):
    self.api = api

  def name():
    return "sensors"

  def exec(self, arguments=None):
    sensor_type, *_ = arguments

    LOG.debug(
        "Running `discover sensor:*` command (sensor_type=%s)", sensor_type)
    if sensor_type not in ["presence", "light", "temperature"]:
      LOG.error(
          "Received unknown sensor type '%s' for `discover sensor:*` command", sensor_type)
      return

    Discovery._print_array_as_discovery(filter(
        Discovery._has_state_field(
            "lightlevel" if sensor_type == "light" else sensor_type),
        self.api.get_sensors()))
    LOG.debug(
        "Finished `discover sensor:*` command (sensor_type=%s)", sensor_type)


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
