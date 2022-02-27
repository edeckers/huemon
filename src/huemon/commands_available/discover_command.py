# Copyright (c) Ely Deckers.
#
# This source code is licensed under the MPL-2.0 license found in the
# LICENSE file in the root directory of this source tree.

from functools import reduce
from huemon.api_interface import ApiInterface
from huemon.config_factory import create_config
from huemon.discovery_interface import Discovery
from huemon.hue_command_interface import HueCommand
from huemon.logger_factory import create_logger
from huemon.plugin_loader import load_plugins
from huemon.util import DEFAULT_COMMANDS_ENABLED_PATH, get_discoveries_path

DISCOVERY_PLUGINS_PATH = get_discoveries_path(
    create_config(), "enabled", DEFAULT_COMMANDS_ENABLED_PATH)

LOG = create_logger()


def create_discovery_handlers(api: ApiInterface, plugins: dict):
  return reduce(
      lambda p, c: {**p, c.name(): c(api)}, plugins, {})


class DiscoveryHandler:
  def __init__(self, handlers):
    self.handlers = handlers

  def exec(self, discovery_type):
    LOG.debug(
        "Running `discover` command (discovery_type=%s)", discovery_type)
    target, maybe_sub_target, *_ = discovery_type.split(":") + [None]

    if target not in self.handlers:
      LOG.error(
          "Received unknown target '%s' for `discover` command", target)
      return

    self.handlers[target].exec([maybe_sub_target] if maybe_sub_target else [])

    LOG.debug(
        "Finished `discover` command (discovery_type=%s)", discovery_type)


class Discover:
  def __init__(self, api: ApiInterface):
    self.api = api

  def discover(self, discovery_type):
    LOG.debug("Loading command plugins (path=%s)", DISCOVERY_PLUGINS_PATH)
    discovery_handler_plugins =  \
        create_discovery_handlers(
            self.api,
            load_plugins("command", DISCOVERY_PLUGINS_PATH, Discovery))
    LOG.debug("Finished loading command plugins (path=%s)",
              DISCOVERY_PLUGINS_PATH)

    DiscoveryHandler(discovery_handler_plugins).exec(discovery_type)


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