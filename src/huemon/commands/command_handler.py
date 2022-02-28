from functools import reduce

from huemon.api_interface import ApiInterface
from huemon.logger_factory import create_logger
from huemon.util import exit_fail

LOG = create_logger()


def create_command_handlers(config: dict, api: ApiInterface, plugins: list):
  return reduce(
      lambda p, c: {**p, c.name(): c(config, api)}, plugins, {})


class CommandHandler:  # pylint: disable=too-few-public-methods
  def __init__(self, handlers):
    self.handlers = handlers

  def available_commands(self):
    return list(self.handlers)

  def exec(self, command: str, arguments):
    LOG.debug("Running command `%s` (arguments=%s)", command, arguments)
    if not command in self.handlers:
      exit_fail(
          "Received unknown command `%s`, expected one of %s",
          command,
          self.available_commands())

    self.handlers[command].exec(arguments)

    LOG.debug("Finished command `%s` (arguments=%s)", command, arguments)
