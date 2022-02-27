from api_interface import ApiInterface
from hue_command_interface import HueCommand
from logger_factory import create_logger

LOG = create_logger()


class LightCommand(HueCommand):
  def __MAPPER_UPDATES_AVAILABLE(light): return int(
      light["swupdate"]["state"] != "noupdates")

  __MAPPER_LIGHT_REACHABLE = HueCommand._mapper("state.reachable", int)
  __MAPPER_STATE_ON = HueCommand._mapper("state.on", int)
  __MAPPER_VERSION = HueCommand._mapper("swversion", str)

  __LIGHT_ACTION_MAP = {
      "is_upgrade_available": __MAPPER_UPDATES_AVAILABLE,
      "reachable": __MAPPER_LIGHT_REACHABLE,
      "status": __MAPPER_STATE_ON,
      "version": __MAPPER_VERSION,
  }

  def __get_light(self, unique_id):
    return HueCommand.get_by_unique_id(unique_id, self.api.get_lights())

  def __map_light(self, unique_id, mapper):
    return mapper(self.__get_light(unique_id))

  def __init__(self, api: ApiInterface, arguments):
    self.api = api
    self.arguments = arguments

  def name(self):
    return "light"

  def exec(self):
    LOG.debug("Running `light` command (arguments=%s)", self.arguments)
    if (len(self.arguments) != 2):
      LOG.error(
          "Expected exactly two arguments for `light`, received %s", len(self.arguments))
      print(
          f"Expected exactly two arguments for `light`, received {len(self.arguments)}")
      exit(1)

    light_id, action = self.arguments

    if action not in self.__LIGHT_ACTION_MAP:
      LOG.error("Received unknown action '%s' for `light` command", action)
      return

    HueCommand._process(self.__map_light(
        light_id, self.__LIGHT_ACTION_MAP[action]))
    LOG.debug("Finished `light` command (arguments=%s)", self.arguments)
