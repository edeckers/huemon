# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from functools import reduce

from huemon.api.api_interface import ApiInterface
from huemon.infrastructure.logger_factory import create_logger
from huemon.util import exit_fail

LOG = create_logger()


def create_name_to_command_mapping(config: dict, api: ApiInterface, plugins: list):
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
