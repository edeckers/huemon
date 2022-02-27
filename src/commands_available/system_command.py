from hue_mon.api_interface import ApiInterface
from hue_mon.hue_command_interface import HueCommand
from hue_mon.logger_factory import create_logger

LOG = create_logger()


class SystemCommand(HueCommand):
  def __init__(self, config: dict, api: ApiInterface):
    self.api = api

  def __map_config(self, mapper):
    return mapper(self.api.get_system_config())

  def __MAPPER_SYSTEM_UPGRADE_AVAILABLE(config): return int(
      config["swupdate2"]["state"] != "noupdates")
  __MAPPER_VERSION = HueCommand._mapper("swversion", str)

  __SYSTEM_ACTION_MAP = {
      "is_upgrade_available": __MAPPER_SYSTEM_UPGRADE_AVAILABLE,
      "version": __MAPPER_VERSION,
  }

  def name():
    return "system"

  def exec(self, arguments):
    LOG.debug("Running `system` command (arguments=%s)", arguments)
    if (len(arguments) != 1):
      LOG.error(
          "Expected exactly one argument for `system`, received %s", len(arguments))
      print(
          f"Expected exactly one argument for `system`, received {len(arguments)}")
      exit(1)

    action, *_ = arguments

    if action not in self.__SYSTEM_ACTION_MAP:
      LOG.error("Received unknown action '%s' for `system` command", action)
      return

    HueCommand._process(self.__map_config(self.__SYSTEM_ACTION_MAP[action]))
    LOG.debug("Finished `system` command (arguments=%s)", arguments)
