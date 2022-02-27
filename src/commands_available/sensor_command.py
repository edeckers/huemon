
from functools import reduce
from api_interface import ApiInterface
from hue_command_interface import HueCommand
from logger_factory import create_logger

LOG = create_logger()


class SensorCommand(HueCommand):
  def __get_sensor(self, device_id):
    return HueCommand.get_by_unique_id(device_id, self.api.get_sensors())

  def __mapper(path, type):
    return lambda value: type(reduce(lambda p, field: p[field], path.split("."), value))

  def __map_sensor(self, unique_id, mapper):
    return mapper(self.__get_sensor(unique_id))

  def __MAPPER_TEMPERATURE(device): return float(
      device["state"]["temperature"]/100)

  __MAPPER_BATTERY = __mapper("config.battery", float)
  __MAPPER_LIGHT_LEVEL = __mapper("state.lightlevel", float)
  __MAPPER_PRESENCE = __mapper("state.presence", int)
  __MAPPER_SENSOR_REACHABLE = __mapper("config.reachable", int)

  __SENSOR_ACTION_MAP = {
      "battery:level": __MAPPER_BATTERY,
      "presence": __MAPPER_PRESENCE,
      "reachable": __MAPPER_SENSOR_REACHABLE,
      "temperature": __MAPPER_TEMPERATURE,
      "light:level": __MAPPER_LIGHT_LEVEL
  }

  def __init__(self, api: ApiInterface, arguments):
    self.api = api
    self.arguments = arguments

  def name():
    return "sensor"

  def exec(self):
    LOG.debug("Running `sensor` command (arguments=%s)", self.arguments)
    if (len(self.arguments) != 2):
      LOG.error(
          "Expected exactly two arguments for `sensor`, received %s", len(self.arguments))
      print(
          f"Expected exactly two arguments for `sensor`, received {len(self.arguments)}")
      exit(1)

    device_id, action = self.arguments

    if action not in SensorCommand.__SENSOR_ACTION_MAP:
      LOG.error("Received unknown action '%s' for `sensor` command", action)
      return

    HueCommand._process(self.__map_sensor(
        device_id, SensorCommand.__SENSOR_ACTION_MAP[action]))
    LOG.debug("Finished `sensor` command (arguments=%s)", self.arguments)
