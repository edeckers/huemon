from api_interface import ApiInterface
from hue_command_interface import HueCommand
from logger_factory import create_logger

LOG = create_logger()


class SystemCommand(HueCommand):
  def __map_config(self, mapper):
    return mapper(self.api.get_system_config())

  def __MAPPER_SYSTEM_UPGRADE_AVAILABLE(config): return int(
      config["swupdate2"]["state"] != "noupdates")
  __MAPPER_VERSION = HueCommand._mapper("swversion", str)

  __SYSTEM_ACTION_MAP = {
      "is_upgrade_available": __MAPPER_SYSTEM_UPGRADE_AVAILABLE,
      "version": __MAPPER_VERSION,
  }

  def __init__(self, api: ApiInterface, arguments):
    self.arguments = arguments
    self.api = api

  def name(self):
    return "system"

  def exec(self):
    LOG.debug("Running `system` command (arguments=%s)", self.arguments)
    if (len(self.arguments) != 1):
      LOG.error(
          "Expected exactly one argument for `system`, received %s", len(self.arguments))
      print(
          f"Expected exactly one argument for `system`, received {len(self.arguments)}")
      exit(1)

    action, *_ = self.arguments

    if action not in self.__SYSTEM_ACTION_MAP:
      LOG.error("Received unknown action '%s' for `system` command", action)
      return

    HueCommand._process(self.__map_config(self.__SYSTEM_ACTION_MAP[action]))
    LOG.debug("Finished `system` command (arguments=%s)", self.arguments)
