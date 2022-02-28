import os
from pathlib import Path
import sys

from huemon.const import EXIT_FAIL
from huemon.infrastructure.logger_factory import create_logger


def create_local_path(relative_path: str):
  return str(os.path.join(
      Path(__file__).parent.absolute(), relative_path))


LOG = create_logger()

DEFAULT_COMMANDS_AVAILABLE_PATH = create_local_path("commands_available")
DEFAULT_COMMANDS_ENABLED_PATH = create_local_path("commands_enabled")
DEFAULT_DISCOVERIES_AVAILABLE_PATH = create_local_path("discoveries_available")
DEFAULT_DISCOVERIES_ENABLED_PATH = create_local_path("discoveries_enabled")

PLUGIN_TYPE_MAPPING = {
    "commands": {
        "available": DEFAULT_COMMANDS_AVAILABLE_PATH,
        "enabled": DEFAULT_COMMANDS_ENABLED_PATH,
    },
    "discoveries": {
        "available": DEFAULT_DISCOVERIES_AVAILABLE_PATH,
        "enabled": DEFAULT_DISCOVERIES_ENABLED_PATH,
    },
}


def __create_plugins_path(plugin_type: str, config: dict, path_type: str, fallback_path: str = None):
  return config[plugin_type][path_type] if \
      plugin_type in config and path_type in config[plugin_type] else \
      (fallback_path or PLUGIN_TYPE_MAPPING[plugin_type][path_type])


def get_commands_path(config: dict, path_type: str, fallback_path: str = None):
  return __create_plugins_path("commands", config, path_type, fallback_path)


def get_discoveries_path(config: dict, path_type: str, fallback_path: str = None):
  return __create_plugins_path("discoveries", config, path_type, fallback_path)


def exit_fail(message, *arguments):
  LOG.error(message, *arguments)
  print(message % tuple(arguments))

  sys.exit(EXIT_FAIL)


def assert_num_args(expected_number_of_arguments: int, arguments: list, context: str):
  if len(arguments) != expected_number_of_arguments:
    argument_text = "argument" if expected_number_of_arguments == 1 else "arguments"

    exit_fail(
        "Expected exactly %s %s for `%s`, received %s",
        expected_number_of_arguments,
        argument_text,
        context,
        len(arguments))


def assert_exists(expected_values: list, value: str):
  if value not in expected_values:
    exit_fail(
        "Received unknown value `%s` (expected=%s)",
        value,
        expected_values)
